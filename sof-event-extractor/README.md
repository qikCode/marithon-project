# SoF Event Extractor

## Overview
The SoF Event Extractor is a Flask-based application designed for maritime document processing and event extraction. It allows users to upload documents, processes them to extract relevant events, and provides an interface for querying and exporting the extracted data.

## Project Structure
```
sof-event-extractor
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── models.py               # Database models
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── uploads                 # Directory for uploaded files
├── services                # Service modules for processing
│   ├── __init__.py
│   ├── ai_service.py       # AI service for generating responses and exporting data
│   ├── document_processor.py# Document processing service
│   └── event_extractor.py  # Event extraction service
├── utils                   # Utility functions
│   ├── __init__.py
│   └── helpers.py          # Helper functions for file handling
└── migrations              # Database migrations
```

## Setup Instructions
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd sof-event-extractor
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

5. **Run the application**:
   ```
   python app.py
   ```

## Usage
- **Health Check**: Access the health check endpoint at `/api/health` to verify that the application is running.
- **Upload Document**: Use the `/api/upload` endpoint to upload documents for processing.
- **Process Document**: Trigger event extraction by sending a POST request to `/api/process/<document_id>`.
- **Get Events**: Retrieve extracted events for a document via `/api/documents/<document_id>/events`.
- **Export Data**: Export events in CSV or JSON format using `/api/export/<document_id>/<format>`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.