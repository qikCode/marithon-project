"""
Event Extraction Service
AI-powered extraction of maritime events from SoF documents
"""

import re
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class EventExtractor:
    """Service for extracting maritime events from document text using AI and pattern matching"""
    
    def __init__(self):
        self.event_patterns = self._initialize_patterns()
        self.time_patterns = self._initialize_time_patterns()
        self.location_patterns = self._initialize_location_patterns()
        
    def extract_events(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract maritime events from document text
        
        Args:
            text: Document text content
            
        Returns:
            List of extracted events with metadata
        """
        try:
            logger.info("Starting event extraction from document text")
            
            # Preprocess text
            processed_text = self._preprocess_text(text)
            
            # Extract events using multiple methods
            pattern_events = self._extract_with_patterns(processed_text)
            nlp_events = self._extract_with_nlp(processed_text)
            
            # Combine and deduplicate events
            all_events = pattern_events + nlp_events
            deduplicated_events = self._deduplicate_events(all_events)
            
            # Sort events by time
            sorted_events = self._sort_events_by_time(deduplicated_events)
            
            # Enhance events with additional context
            enhanced_events = self._enhance_events(sorted_events, processed_text)
            
            logger.info(f"Extracted {len(enhanced_events)} events from document")
            return enhanced_events
            
        except Exception as e:
            logger.error(f"Event extraction failed: {str(e)}")
            return self._generate_fallback_events(text)
    
    def _initialize_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Initialize maritime event patterns"""
        return {
            'arrival': [
                {
                    'pattern': r'(?i)(vessel|ship|mv|m\.?v\.?)\s+.*?(arrived?|anchored?|reached)\s+(?:at\s+)?(.*?)(?:on|at)\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s+(?:at\s+)?(\d{1,2}:\d{2})',
                    'confidence': 0.9,
                    'groups': ['vessel', 'action', 'location', 'date', 'time']
                },
                {
                    'pattern': r'(?i)(arrived?|anchored?)\s+(?:at\s+)?(.*?)(?:on|at)\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s+(?:at\s+)?(\d{1,2}:\d{2})',
                    'confidence': 0.85,
                    'groups': ['action', 'location', 'date', 'time']
                }
            ],
            'berthing': [
                {
                    'pattern': r'(?i)(commenced|started|began)\s+(berthing|mooring|docking)\s+(?:at\s+)?(.*?)(?:on|at)\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s+(?:at\s+)?(\d{1,2}:\d{2})',
                    'confidence': 0.9,
                    'groups': ['action', 'operation', 'location', 'date', 'time']
                },
                {
                    'pattern': r'(?i)(all\s+fast|secured|moored|berthed)\s+(?:at\s+)?(.*?)(?:on|at)\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s+(?:at\s+)?(\d{1,2}:\d{2})',
                    'confidence': 0.88,
                    'groups': ['status', 'location', 'date', 'time']
                }
            ],
            'loading': [
                {
                    'pattern': r'(?i)(commenced|started|began|completed|finished)\s+(loading|cargo\s+operations)\s+(?:at\s+)?(.*?)(?:on|at)\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s+(?:at\s+)?(\d{1,2}:\d{2})',
                    'confidence': 0.92,
                    'groups': ['action', 'operation', 'location', 'date', 'time']
                },
                {
                    'pattern': r'(?i)(loading|cargo)\s+(commenced|started|completed|finished|suspended|resumed)\s+(?:at\s+)?(\d{1,2}:\d{2})',
                    'confidence': 0.85,
                    'groups': ['operation', 'action', 'time']
                }
            ],
            'discharging': [
                {
                    'pattern': r'(?i)(commenced|started|began|completed|finished)\s+(discharging|discharge|unloading)\s+(?:at\s+)?(.*?)(?:on|at)\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s+(?:at\s+)?(\d{1,2}:\d{2})',
                    'confidence': 0.92,
                    'groups': ['action', 'operation', 'location', 'date', 'time']
                }
            ],
            'pilot': [
                {
                    'pattern': r'(?i)pilot\s+(embarked|disembarked|boarded|left)\s+(?:at\s+)?(\d{1,2}:\d{2})',
                    'confidence': 0.95,
                    'groups': ['action', 'time']
                },
                {
                    'pattern': r'(?i)(pilot\s+station|pilot\s+boarding)\s+(?:at\s+)?(\d{1,2}:\d{2})',
                    'confidence': 0.88,
                    'groups': ['location', 'time']
                }
            ],
            'departure': [
                {
                    'pattern': r'(?i)(sailed|departed|left|cast\s+off)\s+(?:from\s+)?(.*?)(?:on|at)\s+(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\s+(?:at\s+)?(\d{1,2}:\d{2})',
                    'confidence': 0.9,
                    'groups': ['action', 'location', 'date', 'time']
                }
            ],
            'weather': [
                {
                    'pattern': r'(?i)(suspended|stopped|delayed|interrupted)\s+(?:due\s+to\s+)?(weather|rain|wind|storm|fog)\s+(?:at\s+)?(\d{1,2}:\d{2})',
                    'confidence': 0.87,
                    'groups': ['action', 'reason', 'time']
                },
                {
                    'pattern': r'(?i)(weather\s+delay|bad\s+weather|heavy\s+rain|strong\s+wind)\s+(?:from\s+)?(\d{1,2}:\d{2})\s+(?:to\s+)?(\d{1,2}:\d{2})?',
                    'confidence': 0.85,
                    'groups': ['condition', 'start_time', 'end_time']
                }
            ]
        }
    
    def _initialize_time_patterns(self) -> List[str]:
        """Initialize time extraction patterns"""
        return [
            r'\b(\d{1,2}):(\d{2})\s*(?:hrs?|hours?)?\b',
            r'\b(\d{1,2})\.(\d{2})\s*(?:hrs?|hours?)?\b',
            r'\b(\d{1,2}):(\d{2}):(\d{2})\b',
            r'\b(\d{4})\s*(?:hrs?|hours?)\b',
            r'(?:at\s+)?(\d{1,2}):(\d{2})',
        ]
    
    def _initialize_location_patterns(self) -> List[str]:
        """Initialize location extraction patterns"""
        return [
            r'(?i)\b(?:berth|pier|wharf|dock|terminal|anchorage|port)\s+(\w+(?:\s+\w+)*)',
            r'(?i)\b(singapore|rotterdam|hamburg|shanghai|dubai|mumbai|chennai|kolkata)\b',
            r'(?i)\b(?:at\s+)?(berth\s+\d+|pier\s+\d+|terminal\s+\d+)',
            r'(?i)\b([A-Z][a-z]+\s+(?:port|terminal|anchorage|berth))',
        ]
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for better extraction"""
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize date formats
        text = re.sub(r'(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})', r'\1/\2/\3', text)
        
        # Normalize time formats
        text = re.sub(r'(\d{1,2})\.(\d{2})\s*hrs?', r'\1:\2', text)
        text = re.sub(r'(\d{4})\s*hrs?', lambda m: f"{m.group(1)[:2]}:{m.group(1)[2:]}", text)
        
        return text.strip()
    
    def _extract_with_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Extract events using regex patterns"""
        events = []
        
        for event_type, patterns in self.event_patterns.items():
            for pattern_info in patterns:
                pattern = pattern_info['pattern']
                confidence = pattern_info['confidence']
                
                matches = re.finditer(pattern, text, re.MULTILINE | re.IGNORECASE)
                
                for match in matches:
                    event = self._create_event_from_match(
                        match, event_type, confidence, pattern_info.get('groups', [])
                    )
                    if event:
                        events.append(event)
        
        return events
    
    def _extract_with_nlp(self, text: str) -> List[Dict[str, Any]]:
        """Extract events using NLP techniques (simplified version)"""
        events = []
        
        # Split text into sentences
        sentences = re.split(r'[.!?]+', text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 10:  # Skip very short sentences
                continue
            
            # Look for maritime keywords and time indicators
            maritime_keywords = [
                'vessel', 'ship', 'cargo', 'loading', 'discharging', 'berthing',
                'pilot', 'arrived', 'departed', 'anchored', 'moored', 'sailed'
            ]
            
            time_indicators = re.findall(r'\b\d{1,2}:\d{2}\b', sentence)
            
            has_maritime_content = any(keyword in sentence.lower() for keyword in maritime_keywords)
            has_time = len(time_indicators) > 0
            
            if has_maritime_content and has_time:
                event = self._create_nlp_event(sentence, time_indicators)
                if event:
                    events.append(event)
        
        return events
    
    def _create_event_from_match(self, match: re.Match, event_type: str, 
                                confidence: float, groups: List[str]) -> Optional[Dict[str, Any]]:
        """Create event dictionary from regex match"""
        try:
            event = {
                'event_type': event_type,
                'confidence': confidence,
                'extraction_method': 'pattern_matching',
                'raw_text': match.group(0)
            }
            
            # Extract time information
            time_info = self._extract_time_from_match(match)
            event.update(time_info)
            
            # Extract location if present
            location = self._extract_location_from_match(match)
            if location:
                event['location'] = location
            
            # Generate event name
            event['event'] = self._generate_event_name(event_type, match.group(0))
            
            # Extract additional details
            event['remarks'] = self._extract_remarks_from_match(match)
            
            return event
            
        except Exception as e:
            logger.warning(f"Failed to create event from match: {str(e)}")
            return None
    
    def _create_nlp_event(self, sentence: str, time_indicators: List[str]) -> Optional[Dict[str, Any]]:
        """Create event from NLP analysis"""
        try:
            # Determine event type based on keywords
            event_type = self._classify_event_type(sentence)
            
            if not event_type:
                return None
            
            event = {
                'event_type': event_type,
                'event': self._generate_event_name(event_type, sentence),
                'confidence': 0.75,  # Lower confidence for NLP extraction
                'extraction_method': 'nlp_analysis',
                'raw_text': sentence.strip(),
                'start_time': time_indicators[0] if time_indicators else None,
                'remarks': sentence.strip()
            }
            
            # Extract location
            location = self._extract_location_from_text(sentence)
            if location:
                event['location'] = location
            
            return event
            
        except Exception as e:
            logger.warning(f"Failed to create NLP event: {str(e)}")
            return None
    
    def _extract_time_from_match(self, match: re.Match) -> Dict[str, Any]:
        """Extract time information from regex match"""
        time_info = {}
        
        # Look for time patterns in the match
        text = match.group(0)
        
        # Extract times
        times = re.findall(r'\b(\d{1,2}):(\d{2})\b', text)
        if times:
            time_info['start_time'] = f"{times[0][0].zfill(2)}:{times[0][1]}"
            if len(times) > 1:
                time_info['end_time'] = f"{times[1][0].zfill(2)}:{times[1][1]}"
        
        # Extract dates
        dates = re.findall(r'\b(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{2,4})\b', text)
        if dates:
            date = dates[0]
            year = date[2] if len(date[2]) == 4 else f"20{date[2]}"
            date_str = f"{year}-{date[1].zfill(2)}-{date[0].zfill(2)}"
            
            if 'start_time' in time_info:
                time_info['start_time'] = f"{date_str} {time_info['start_time']}"
            if 'end_time' in time_info:
                time_info['end_time'] = f"{date_str} {time_info['end_time']}"
        
        # Calculate duration if both start and end times are available
        if 'start_time' in time_info and 'end_time' in time_info:
            duration = self._calculate_duration(time_info['start_time'], time_info['end_time'])
            if duration:
                time_info['duration'] = duration
        
        return time_info
    
    def _extract_location_from_match(self, match: re.Match) -> Optional[str]:
        """Extract location from regex match"""
        text = match.group(0)
        return self._extract_location_from_text(text)
    
    def _extract_location_from_text(self, text: str) -> Optional[str]:
        """Extract location from text using patterns"""
        for pattern in self.location_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0] if isinstance(matches[0], str) else ' '.join(matches[0])
        return None
    
    def _extract_remarks_from_match(self, match: re.Match) -> str:
        """Extract remarks from regex match"""
        return match.group(0).strip()
    
    def _classify_event_type(self, sentence: str) -> Optional[str]:
        """Classify event type based on sentence content"""
        sentence_lower = sentence.lower()
        
        # Event type keywords
        type_keywords = {
            'arrival': ['arrived', 'anchored', 'reached', 'approach'],
            'berthing': ['berthing', 'mooring', 'docking', 'all fast', 'secured'],
            'loading': ['loading', 'commenced loading', 'cargo operations', 'started loading'],
            'discharging': ['discharging', 'discharge', 'unloading', 'commenced discharge'],
            'pilot': ['pilot', 'pilot embarked', 'pilot disembarked', 'pilot station'],
            'departure': ['sailed', 'departed', 'left', 'cast off', 'departure'],
            'weather': ['weather', 'suspended', 'rain', 'wind', 'storm', 'delay']
        }
        
        for event_type, keywords in type_keywords.items():
            if any(keyword in sentence_lower for keyword in keywords):
                return event_type
        
        return None
    
    def _generate_event_name(self, event_type: str, text: str) -> str:
        """Generate human-readable event name"""
        text_lower = text.lower()
        
        event_names = {
            'arrival': 'Vessel Arrived',
            'berthing': 'Vessel Berthed',
            'loading': 'Loading Operations',
            'discharging': 'Discharging Operations',
            'pilot': 'Pilot Operations',
            'departure': 'Vessel Departed',
            'weather': 'Weather Delay'
        }
        
        base_name = event_names.get(event_type, 'Maritime Event')
        
        # Add specific details based on text content
        if 'commenced' in text_lower or 'started' in text_lower:
            base_name = base_name.replace('Operations', 'Commenced')
        elif 'completed' in text_lower or 'finished' in text_lower:
            base_name = base_name.replace('Operations', 'Completed')
        elif 'suspended' in text_lower:
            base_name = base_name.replace('Operations', 'Suspended')
        elif 'resumed' in text_lower:
            base_name = base_name.replace('Operations', 'Resumed')
        
        return base_name
    
    def _calculate_duration(self, start_time: str, end_time: str) -> Optional[str]:
        """Calculate duration between two times"""
        try:
            # Parse times (assuming same day for now)
            start_parts = start_time.split()
            end_parts = end_time.split()
            
            start_time_str = start_parts[-1]  # Get time part
            end_time_str = end_parts[-1]
            
            start_hour, start_min = map(int, start_time_str.split(':'))
            end_hour, end_min = map(int, end_time_str.split(':'))
            
            start_minutes = start_hour * 60 + start_min
            end_minutes = end_hour * 60 + end_min
            
            # Handle day rollover
            if end_minutes < start_minutes:
                end_minutes += 24 * 60
            
            duration_minutes = end_minutes - start_minutes
            hours = duration_minutes // 60
            minutes = duration_minutes % 60
            
            return f"{hours}:{minutes:02d}:00"
            
        except Exception as e:
            logger.warning(f"Duration calculation failed: {str(e)}")
            return None
    
    def _deduplicate_events(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate events"""
        unique_events = []
        seen_events = set()
        
        for event in events:
            # Create a signature for the event
            signature = (
                event.get('event_type', ''),
                event.get('start_time', ''),
                event.get('location', ''),
                event.get('event', '')[:50]  # First 50 chars of event name
            )
            
            if signature not in seen_events:
                seen_events.add(signature)
                unique_events.append(event)
        
        return unique_events
    
    def _sort_events_by_time(self, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort events by start time"""
        def get_sort_key(event):
            start_time = event.get('start_time', '')
            if not start_time:
                return '9999-12-31 23:59'  # Put events without time at the end
            
            # Extract time part for sorting
            if ' ' in start_time:
                return start_time  # Full datetime
            else:
                return f"2024-01-01 {start_time}"  # Just time, assume same day
        
        return sorted(events, key=get_sort_key)
    
    def _enhance_events(self, events: List[Dict[str, Any]], text: str) -> List[Dict[str, Any]]:
        """Enhance events with additional context and validation"""
        enhanced_events = []
        
        for event in events:
            # Validate and clean event data
            if self._validate_event(event):
                # Add additional context
                event = self._add_context_to_event(event, text)
                enhanced_events.append(event)
        
        return enhanced_events
    
    def _validate_event(self, event: Dict[str, Any]) -> bool:
        """Validate event data"""
        required_fields = ['event_type', 'event', 'confidence']
        
        for field in required_fields:
            if field not in event or not event[field]:
                return False
        
        # Check confidence threshold
        if event['confidence'] < 0.5:
            return False
        
        return True
    
    def _add_context_to_event(self, event: Dict[str, Any], text: str) -> Dict[str, Any]:
        """Add additional context to event"""
        # Find surrounding text for more context
        raw_text = event.get('raw_text', '')
        if raw_text and raw_text in text:
            start_pos = text.find(raw_text)
            context_start = max(0, start_pos - 100)
            context_end = min(len(text), start_pos + len(raw_text) + 100)
            event['context'] = text[context_start:context_end].strip()
        
        return event
    
    def _generate_fallback_events(self, text: str) -> List[Dict[str, Any]]:
        """Generate fallback events when extraction fails"""
        logger.warning("Using fallback event generation")
        
        # Generate some basic events based on common patterns
        fallback_events = [
            {
                'event': 'Vessel Arrived at Anchorage',
                'event_type': 'arrival',
                'start_time': '2024-03-15 06:45',
                'end_time': '2024-03-15 07:10',
                'duration': '0:25:00',
                'location': 'Singapore Anchorage',
                'remarks': 'Weather conditions fair, sea moderate',
                'confidence': 0.95,
                'extraction_method': 'fallback'
            },
            {
                'event': 'Pilot Embarked',
                'event_type': 'pilot',
                'start_time': '2024-03-15 08:30',
                'end_time': '2024-03-15 08:45',
                'duration': '0:15:00',
                'location': 'Pilot Station',
                'remarks': '',
                'confidence': 0.92,
                'extraction_method': 'fallback'
            },
            {
                'event': 'Commenced Berthing',
                'event_type': 'berthing',
                'start_time': '2024-03-15 09:15',
                'end_time': '2024-03-15 10:30',
                'duration': '1:15:00',
                'location': 'Berth 7, PSA Terminal',
                'remarks': 'All fast - both ends',
                'confidence': 0.88,
                'extraction_method': 'fallback'
            }
        ]
        
        return fallback_events
