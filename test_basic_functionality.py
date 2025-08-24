#!/usr/bin/env python3
"""
Basic functionality test for SoF Event Extractor
Tests core components without full Docker setup
"""

import sys
import os
import tempfile
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from config import Config
        print("✅ Config import successful")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from models import Document, Event
        print("✅ Models import successful")
    except Exception as e:
        print(f"❌ Models import failed: {e}")
        return False
    
    try:
        from services.document_processor import DocumentProcessor
        print("✅ DocumentProcessor import successful")
    except Exception as e:
        print(f"❌ DocumentProcessor import failed: {e}")
        return False
    
    try:
        from services.event_extractor import EventExtractor
        print("✅ EventExtractor import successful")
    except Exception as e:
        print(f"❌ EventExtractor import failed: {e}")
        return False
    
    try:
        from services.ai_service import AIService
        print("✅ AIService import successful")
    except Exception as e:
        print(f"❌ AIService import failed: {e}")
        return False
    
    try:
        from utils.helpers import allowed_file, get_file_hash
        print("✅ Utils import successful")
    except Exception as e:
        print(f"❌ Utils import failed: {e}")
        return False
    
    return True

def test_file_validation():
    """Test file validation functions"""
    print("\n🔍 Testing file validation...")
    
    try:
        from utils.helpers import allowed_file
        
        # Test valid files
        assert allowed_file('document.pdf') == True
        assert allowed_file('document.doc') == True
        assert allowed_file('document.docx') == True
        print("✅ Valid file extensions accepted")
        
        # Test invalid files
        assert allowed_file('document.txt') == False
        assert allowed_file('document.jpg') == False
        assert allowed_file('') == False
        print("✅ Invalid file extensions rejected")
        
        return True
    except Exception as e:
        print(f"❌ File validation test failed: {e}")
        return False

def test_event_extractor():
    """Test event extraction with sample text"""
    print("\n🔍 Testing event extraction...")
    
    try:
        from services.event_extractor import EventExtractor
        
        extractor = EventExtractor()
        
        # Sample maritime text
        sample_text = """
        MV OCEAN STAR arrived at Singapore anchorage on 15/03/2024 at 06:45.
        Pilot embarked at 08:30 and vessel commenced berthing at 09:15.
        All fast at berth 7 at 10:30. Loading commenced at 11:00.
        Loading suspended due to heavy rain at 18:45 and resumed at 20:15.
        Loading completed at 14:20 on 16/03/2024.
        Vessel sailed at 16:45.
        """
        
        events = extractor.extract_events(sample_text)
        
        if len(events) > 0:
            print(f"✅ Extracted {len(events)} events from sample text")
            for i, event in enumerate(events[:3]):  # Show first 3 events
                print(f"   Event {i+1}: {event.get('event', 'Unknown')} ({event.get('event_type', 'unknown')})")
            return True
        else:
            print("❌ No events extracted from sample text")
            return False
            
    except Exception as e:
        print(f"❌ Event extraction test failed: {e}")
        return False

def test_ai_service():
    """Test AI service responses"""
    print("\n🔍 Testing AI service...")
    
    try:
        from services.ai_service import AIService
        
        ai_service = AIService()
        
        # Test basic response generation
        response = ai_service.generate_response("Hello", None)
        
        if response and len(response) > 0:
            print("✅ AI service generated response")
            print(f"   Sample response: {response[:100]}...")
            return True
        else:
            print("❌ AI service failed to generate response")
            return False
            
    except Exception as e:
        print(f"❌ AI service test failed: {e}")
        return False

def test_document_processor():
    """Test document processor with a simple text file"""
    print("\n🔍 Testing document processor...")
    
    try:
        from services.document_processor import DocumentProcessor
        
        processor = DocumentProcessor()
        
        # Create a temporary text file to test with
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Test maritime document content for processing.")
            temp_file = f.name
        
        try:
            # Test file validation
            validation = processor.validate_document(temp_file)
            print(f"✅ Document validation completed: {validation.get('file_exists', False)}")
            
            return True
        finally:
            # Clean up
            os.unlink(temp_file)
            
    except Exception as e:
        print(f"❌ Document processor test failed: {e}")
        return False

def main():
    """Run all basic functionality tests"""
    print("🚢 SoF Event Extractor - Basic Functionality Test")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("File Validation", test_file_validation),
        ("Event Extraction", test_event_extractor),
        ("AI Service", test_ai_service),
        ("Document Processor", test_document_processor),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic functionality tests PASSED!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
