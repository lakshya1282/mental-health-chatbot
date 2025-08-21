import hashlib
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)

class PrivacyManager:
    def __init__(self):
        """Initialize privacy manager with data protection protocols."""
        
        # Privacy principles
        self.privacy_principles = {
            'data_minimization': 'Collect only necessary data',
            'purpose_limitation': 'Use data only for stated mental health support purposes',
            'transparency': 'Be clear about data collection and use',
            'user_control': 'Give users control over their data',
            'security': 'Protect data with appropriate security measures',
            'retention_limits': 'Delete data after retention period',
            'anonymization': 'Remove identifying information when possible'
        }
        
        # Data categories and retention periods
        self.data_categories = {
            'conversation_content': {
                'retention_days': 7,
                'encryption_required': True,
                'anonymization_after_days': 1,
                'description': 'Raw conversation text'
            },
            'sentiment_analysis': {
                'retention_days': 30,
                'encryption_required': False,
                'anonymization_after_days': 7,
                'description': 'Sentiment scores and emotional indicators'
            },
            'stress_indicators': {
                'retention_days': 30,
                'encryption_required': False,
                'anonymization_after_days': 7,
                'description': 'Detected stress and mental health indicators'
            },
            'wellness_activities': {
                'retention_days': 90,
                'encryption_required': False,
                'anonymization_after_days': 14,
                'description': 'Wellness recommendations and user interactions'
            },
            'crisis_logs': {
                'retention_days': 365,
                'encryption_required': True,
                'anonymization_after_days': 30,
                'description': 'Emergency situation logs (heavily anonymized)'
            }
        }
        
        # Sensitive data patterns to detect and handle
        self.sensitive_patterns = {
            'names': r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b',
            'phone_numbers': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'email_addresses': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'addresses': r'\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Lane|Ln|Drive|Dr|Boulevard|Blvd|Court|Ct)\b',
            'ssn': r'\b\d{3}-?\d{2}-?\d{4}\b',
            'credit_cards': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'dates_of_birth': r'\b\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}\b'
        }
        
        # User rights under privacy laws (GDPR, CCPA, etc.)
        self.user_rights = [
            'right_to_information',
            'right_of_access',
            'right_to_rectification',
            'right_to_erasure',
            'right_to_restrict_processing',
            'right_to_data_portability',
            'right_to_object',
            'right_not_to_be_subject_to_automated_decision_making'
        ]
    
    def sanitize_text(self, text: str) -> str:
        """
        Remove or mask sensitive information from text.
        
        Args:
            text (str): Input text to sanitize
            
        Returns:
            str: Sanitized text with sensitive info removed/masked
        """
        if not text:
            return text
        
        sanitized = text
        
        # Replace sensitive patterns
        for pattern_name, pattern in self.sensitive_patterns.items():
            if pattern_name == 'names':
                # Replace names with generic placeholders
                sanitized = re.sub(pattern, '[NAME]', sanitized)
            elif pattern_name == 'phone_numbers':
                sanitized = re.sub(pattern, '[PHONE]', sanitized)
            elif pattern_name == 'email_addresses':
                sanitized = re.sub(pattern, '[EMAIL]', sanitized)
            elif pattern_name == 'addresses':
                sanitized = re.sub(pattern, '[ADDRESS]', sanitized)
            elif pattern_name == 'ssn':
                sanitized = re.sub(pattern, '[SSN]', sanitized)
            elif pattern_name == 'credit_cards':
                sanitized = re.sub(pattern, '[CARD]', sanitized)
            elif pattern_name == 'dates_of_birth':
                sanitized = re.sub(pattern, '[DOB]', sanitized)
        
        return sanitized
    
    def detect_sensitive_data(self, text: str) -> Dict[str, List[str]]:
        """
        Detect potentially sensitive information in text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict: Dictionary of detected sensitive data types and matches
        """
        if not text:
            return {}
        
        detected = {}
        
        for pattern_name, pattern in self.sensitive_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detected[pattern_name] = matches
        
        return detected
    
    def anonymize_data(self, data: Dict) -> Dict:
        """
        Anonymize data by removing or hashing identifying information.
        
        Args:
            data (Dict): Data to anonymize
            
        Returns:
            Dict: Anonymized data
        """
        anonymized = data.copy()
        
        # Remove or hash sensitive fields
        sensitive_fields = ['user_id', 'session_id', 'ip_address', 'user_agent']
        
        for field in sensitive_fields:
            if field in anonymized:
                if field in ['user_id', 'session_id']:
                    # Hash these fields to maintain some consistency
                    anonymized[field] = hashlib.sha256(str(anonymized[field]).encode()).hexdigest()[:16]
                else:
                    # Remove completely
                    del anonymized[field]
        
        # Sanitize text content
        text_fields = ['message_content', 'response_content', 'notes']
        for field in text_fields:
            if field in anonymized:
                anonymized[field] = self.sanitize_text(anonymized[field])
        
        # Add anonymization timestamp
        anonymized['anonymized_at'] = datetime.now().isoformat()
        
        return anonymized
    
    def generate_privacy_notice(self) -> str:
        """Generate privacy notice for users."""
        return """
**🔒 Privacy Notice - MindCare AI Mental Health Chatbot**

**What Information We Collect:**
• Your conversations with the chatbot (temporarily, for context)
• Sentiment analysis and mental health indicators (anonymized)
• Wellness activity interactions (anonymized)
• Crisis intervention logs (heavily anonymized)

**How We Use Your Information:**
• To provide personalized mental health support and recommendations
• To improve our AI's ability to detect mental health concerns
• To generate anonymized analytics for research purposes
• To ensure appropriate crisis intervention when needed

**Your Privacy Rights:**
• Access your data and see what we've collected
• Correct any inaccurate information
• Delete your data at any time ('right to be forgotten')
• Export your data in a portable format
• Object to certain types of processing

**Data Protection Measures:**
• End-to-end encryption for sensitive conversations
• Automatic deletion of raw conversations after 7 days
• Complete anonymization of all data after 30 days
• No sharing of personal data with third parties
• Secure, encrypted storage of all data

**Data Retention:**
• Conversation content: 7 days (then deleted)
• Analysis data: 30 days (then anonymized)
• Crisis logs: 1 year (heavily anonymized)
• You can request deletion at any time

**Contact Us:**
If you have questions about privacy or want to exercise your rights, 
please contact our privacy team.

**Last Updated:** {date}

By using this chatbot, you acknowledge that you have read and 
understand this privacy notice.
        """.format(date=datetime.now().strftime("%Y-%m-%d"))
    
    def check_data_compliance(self, data_age_days: int, data_type: str) -> Dict:
        """
        Check if data storage complies with privacy policies.
        
        Args:
            data_age_days (int): Age of data in days
            data_type (str): Type of data being checked
            
        Returns:
            Dict: Compliance status and required actions
        """
        if data_type not in self.data_categories:
            return {'status': 'unknown_data_type', 'actions': ['classify_data_type']}
        
        category = self.data_categories[data_type]
        retention_days = category['retention_days']
        anonymization_days = category['anonymization_after_days']
        
        actions = []
        
        # Check if data should be deleted
        if data_age_days > retention_days:
            actions.append('delete_data')
            status = 'non_compliant'
        
        # Check if data should be anonymized
        elif data_age_days > anonymization_days:
            actions.append('anonymize_data')
            status = 'needs_anonymization'
        
        # Data is within compliance
        else:
            status = 'compliant'
        
        return {
            'status': status,
            'data_age_days': data_age_days,
            'retention_limit': retention_days,
            'anonymization_limit': anonymization_days,
            'actions': actions,
            'encryption_required': category['encryption_required']
        }
    
    def generate_data_export(self, user_data: Dict) -> Dict:
        """
        Generate user data export in privacy-compliant format.
        
        Args:
            user_data (Dict): User's data to export
            
        Returns:
            Dict: Formatted data export
        """
        export_data = {
            'export_info': {
                'generated_at': datetime.now().isoformat(),
                'data_controller': 'MindCare AI Mental Health Chatbot',
                'export_format': 'JSON',
                'privacy_notice_version': '1.0'
            },
            'user_rights_info': {
                'rights_available': self.user_rights,
                'contact_for_questions': 'privacy@mindcare-ai.com',
                'data_retention_policy': self.data_categories
            },
            'user_data': user_data
        }
        
        return export_data
    
    def assess_privacy_risk(self, text: str) -> Dict:
        """
        Assess privacy risks in user input.
        
        Args:
            text (str): Text to assess
            
        Returns:
            Dict: Privacy risk assessment
        """
        sensitive_data = self.detect_sensitive_data(text)
        risk_level = 'low'
        recommendations = []
        
        if sensitive_data:
            if any(key in ['ssn', 'credit_cards', 'phone_numbers'] for key in sensitive_data.keys()):
                risk_level = 'high'
                recommendations.extend([
                    'Remove or mask sensitive personal identifiers',
                    'Encrypt this data immediately',
                    'Consider flagging for manual review'
                ])
            elif any(key in ['names', 'addresses', 'email_addresses'] for key in sensitive_data.keys()):
                risk_level = 'medium'
                recommendations.extend([
                    'Anonymize personal identifiers',
                    'Apply data retention limits'
                ])
            else:
                risk_level = 'low'
                recommendations.append('Standard anonymization procedures apply')
        
        return {
            'risk_level': risk_level,
            'sensitive_data_detected': sensitive_data,
            'recommendations': recommendations,
            'requires_manual_review': risk_level == 'high'
        }
    
    def get_consent_form(self) -> str:
        """Generate informed consent form for data processing."""
        return """
**📋 Informed Consent for Mental Health Chatbot**

**Purpose of Data Collection:**
This mental health chatbot collects and processes your conversations to:
• Provide personalized mental health support
• Detect signs of crisis and provide appropriate resources
• Improve the chatbot's ability to help users
• Generate anonymized research insights

**What Data We Collect:**
□ Your text conversations with the chatbot
□ Emotional sentiment analysis from your messages
□ Stress and mental health indicators detected
□ Your interactions with wellness recommendations
□ Crisis situation logs (if applicable)

**Your Rights:**
□ You can withdraw consent at any time
□ You can request deletion of your data
□ You can access and export your data
□ You can correct inaccurate information
□ You will be notified of any data breaches

**Data Security:**
□ All sensitive data is encrypted
□ Data is automatically deleted according to retention policies
□ No personal data is shared with third parties
□ Anonymous analytics may be used for research

**Consent Statement:**
By checking this box and using the chatbot, I confirm that:
□ I am at least 13 years old (or have parental consent)
□ I understand this is not a replacement for professional medical care
□ I understand that in crisis situations, appropriate resources will be provided
□ I consent to the processing of my data as described above
□ I understand I can withdraw consent at any time

**Crisis Situations:**
I understand that if I express thoughts of self-harm or suicide, 
the chatbot will:
• Provide immediate crisis resources
• Log the interaction (anonymously) for safety monitoring
• Encourage me to seek professional help immediately

**Date:** {date}
**Version:** 1.0

□ I AGREE to these terms and consent to data processing
□ I DO NOT AGREE and will not use this service
        """.format(date=datetime.now().strftime("%Y-%m-%d"))
    
    def log_privacy_action(self, action: str, user_id: str = None, details: Dict = None):
        """
        Log privacy-related actions for compliance tracking.
        
        Args:
            action (str): Type of privacy action taken
            user_id (str): User identifier (will be hashed)
            details (Dict): Additional details about the action
        """
        try:
            # Hash user ID for privacy
            hashed_user_id = None
            if user_id:
                hashed_user_id = hashlib.sha256(user_id.encode()).hexdigest()[:16]
            
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'action': action,
                'user_hash': hashed_user_id,
                'details': details or {},
                'compliance_version': '1.0'
            }
            
            logger.info(f"Privacy action logged: {json.dumps(log_entry)}")
            
        except Exception as e:
            logger.error(f"Error logging privacy action: {e}")
    
    def validate_data_processing_purpose(self, data_type: str, processing_purpose: str) -> bool:
        """
        Validate if data processing is for a legitimate purpose.
        
        Args:
            data_type (str): Type of data being processed
            processing_purpose (str): Intended purpose of processing
            
        Returns:
            bool: Whether processing is legitimate
        """
        legitimate_purposes = {
            'conversation_content': [
                'provide_mental_health_support',
                'crisis_detection',
                'conversation_context'
            ],
            'sentiment_analysis': [
                'mental_health_assessment',
                'personalized_recommendations',
                'crisis_detection',
                'anonymous_research'
            ],
            'stress_indicators': [
                'mental_health_assessment',
                'personalized_recommendations',
                'crisis_detection',
                'anonymous_research'
            ],
            'wellness_activities': [
                'track_user_engagement',
                'improve_recommendations',
                'anonymous_research'
            ],
            'crisis_logs': [
                'safety_monitoring',
                'improve_crisis_detection',
                'compliance_reporting'
            ]
        }
        
        if data_type not in legitimate_purposes:
            return False
        
        return processing_purpose in legitimate_purposes[data_type]
