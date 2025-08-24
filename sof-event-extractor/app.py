"""
SoF Event Extractor - Main Flask Application
Maritime document processing and event extraction system
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import logging
from datetime import datetime
import uuid

from config import Config
from models import db, Document, Event
from services.document_processor import DocumentProcessor
from services.event_extractor import EventExtractor
from services.ai_service import AIService
from utils.helpers import allowed_file, get_file_hash

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:5500", "*"])

# Initialize services
document_processor = DocumentProcessor()
event_extractor = EventExtractor()
ai_service = AIService()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Upload and process SoF document"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF, DOC, DOCX allowed'}), 400
        
        # Check file size (10MB limit)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            return jsonify({'error': 'File size exceeds 10MB limit'}), 400
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Calculate file hash for deduplication
        file_hash = get_file_hash(file_path)
        
        # Check if document already processed
        existing_doc = Document.query.filter_by(file_hash=file_hash).first()
        if existing_doc:
            logger.info(f"Document already processed: {existing_doc.id}")
            return jsonify({
                'document_id': existing_doc.id,
                'message': 'Document already processed',
                'events': [event.to_dict() for event in existing_doc.events]
            })
        
        # Create document record
        document = Document(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            file_hash=file_hash
        )
        
        db.session.add(document)
        db.session.commit()
        
        logger.info(f"Document uploaded: {document.id}")
        
        return jsonify({
            'document_id': document.id,
            'message': 'Document uploaded successfully',
            'filename': filename,
            'size': file_size
        })
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Upload failed'}), 500

@app.route('/api/process/<document_id>', methods=['POST'])
def process_document(document_id):
    """Process document and extract events"""
    try:
        document = Document.query.get_or_404(document_id)
        
        if document.status == 'processed':
            return jsonify({
                'message': 'Document already processed',
                'events': [event.to_dict() for event in document.events]
            })
        
        # Update status
        document.status = 'processing'
        db.session.commit()
        
        # Process document
        logger.info(f"Processing document: {document_id}")
        
        # Extract text from document
        text_content = document_processor.extract_text(document.file_path)
        document.text_content = text_content
        
        # Extract events using AI
        extracted_events = event_extractor.extract_events(text_content)
        
        # Save events to database
        for event_data in extracted_events:
            event = Event(
                document_id=document.id,
                event_type=event_data['event_type'],
                event_name=event_data['event'],
                start_time=event_data.get('start_time'),
                end_time=event_data.get('end_time'),
                duration=event_data.get('duration'),
                location=event_data.get('location'),
                remarks=event_data.get('remarks'),
                confidence=event_data.get('confidence', 0.0)
            )
            db.session.add(event)
        
        # Update document status
        document.status = 'processed'
        document.processed_at = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Document processed successfully: {document_id}")
        
        return jsonify({
            'message': 'Document processed successfully',
            'events': [event.to_dict() for event in document.events],
            'total_events': len(document.events)
        })
        
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        document.status = 'failed'
        db.session.commit()
        return jsonify({'error': 'Processing failed'}), 500

@app.route('/api/documents/<document_id>/events', methods=['GET'])
def get_events(document_id):
    """Get extracted events for a document"""
    try:
        document = Document.query.get_or_404(document_id)
        
        # Filter by event type if specified
        event_type = request.args.get('type')
        events = document.events
        
        if event_type and event_type != 'all':
            events = [e for e in events if e.event_type == event_type]
        
        return jsonify({
            'events': [event.to_dict() for event in events],
            'total': len(events)
        })
        
    except Exception as e:
        logger.error(f"Get events error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve events'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """AI chat endpoint for document queries"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        document_id = data.get('document_id')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get document context if provided
        document = None
        if document_id:
            document = Document.query.get(document_id)
        
        # Generate AI response
        response = ai_service.generate_response(message, document)
        
        logger.info(f"Chat query: {message[:50]}...")
        
        return jsonify({
            'response': response,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        return jsonify({'error': 'Chat service unavailable'}), 500

@app.route('/api/export/<document_id>/<format>', methods=['GET'])
def export_data(document_id, format):
    """Export document events in CSV or JSON format"""
    try:
        document = Document.query.get_or_404(document_id)
        
        # Get export options
        include_confidence = request.args.get('confidence', 'true').lower() == 'true'
        include_remarks = request.args.get('remarks', 'true').lower() == 'true'
        include_metadata = request.args.get('metadata', 'false').lower() == 'true'
        
        if format.lower() == 'csv':
            file_path = ai_service.export_to_csv(
                document, include_confidence, include_remarks, include_metadata
            )
            return send_file(file_path, as_attachment=True, download_name=f"{document.original_filename}_events.csv")
        
        elif format.lower() == 'json':
            file_path = ai_service.export_to_json(
                document, include_confidence, include_remarks, include_metadata
            )
            return send_file(file_path, as_attachment=True, download_name=f"{document.original_filename}_events.json")
        
        else:
            return jsonify({'error': 'Invalid format. Use csv or json'}), 400
            
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        return jsonify({'error': 'Export failed'}), 500

@app.route('/api/documents/<document_id>/summary', methods=['GET'])
def get_summary(document_id):
    """Get document processing summary and statistics"""
    try:
        document = Document.query.get_or_404(document_id)
        
        if document.status != 'processed':
            return jsonify({'error': 'Document not yet processed'}), 400
        
        # Calculate statistics
        events = document.events
        event_types = {}
        total_duration = 0
        
        for event in events:
            event_type = event.event_type
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            # Calculate duration if available
            if event.duration:
                try:
                    # Parse duration (assuming format like "1:30:00")
                    parts = event.duration.split(':')
                    if len(parts) == 3:
                        hours = int(parts[0])
                        minutes = int(parts[1])
                        total_duration += hours * 60 + minutes
                except:
                    pass
        
        summary = {
            'document_info': {
                'filename': document.original_filename,
                'size': document.file_size,
                'processed_at': document.processed_at.isoformat() if document.processed_at else None,
                'total_events': len(events)
            },
            'statistics': {
                'event_distribution': event_types,
                'total_duration_minutes': total_duration,
                'average_confidence': sum(e.confidence for e in events) / len(events) if events else 0
            },
            'timeline': {
                'first_event': events[0].start_time if events else None,
                'last_event': events[-1].end_time or events[-1].start_time if events else None
            }
        }
        
        return jsonify(summary)
        
    except Exception as e:
        logger.error(f"Summary error: {str(e)}")
        return jsonify({'error': 'Failed to generate summary'}), 500

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all processed documents"""
    try:
        documents = Document.query.order_by(Document.created_at.desc()).all()
        
        return jsonify({
            'documents': [doc.to_dict() for doc in documents],
            'total': len(documents)
        })
        
    except Exception as e:
        logger.error(f"List documents error: {str(e)}")
        return jsonify({'error': 'Failed to retrieve documents'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)