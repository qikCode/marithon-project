class AIService:
    def generate_response(self, message, document):
        return f"I understand you're asking about: {message}. Based on the document analysis, I can help you with maritime operations and event timelines."
    
    def export_to_csv(self, document, include_confidence, include_remarks, include_metadata):
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        temp_file.write("Event,Type,Start Time,End Time\n")
        temp_file.write("Sample Event,arrival,2024-03-15 06:45,2024-03-15 07:10\n")
        temp_file.close()
        return temp_file.name
    
    def export_to_json(self, document, include_confidence, include_remarks, include_metadata):
        import tempfile
        import json
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        data = {"events": [{"event": "Sample Event", "type": "arrival"}]}
        json.dump(data, temp_file)
        temp_file.close()
        return temp_file.name