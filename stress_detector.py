import re
import nltk
from typing import List, Dict, Tuple
import numpy as np
from collections import defaultdict, Counter
from datetime import datetime

class StressDetector:
    def __init__(self):
        """Initialize stress detection with comprehensive patterns and indicators."""
        
        # Stress-related keywords and patterns
        self.stress_patterns = {
            'work_stress': [
                r'\b(work|job|boss|deadline|overtime|meeting|project|workload)\b',
                r'\b(too much work|work pressure|work stress|job stress)\b'
            ],
            'academic_stress': [
                r'\b(exam|test|homework|assignment|grade|study|studying|school|university|college)\b',
                r'\b(academic pressure|study stress|exam anxiety)\b'
            ],
            'financial_stress': [
                r'\b(money|debt|bills|rent|mortgage|financial|budget|broke|poor)\b',
                r'\b(financial stress|money problems|can\'t afford)\b'
            ],
            'relationship_stress': [
                r'\b(relationship|marriage|divorce|breakup|family|friend|partner|spouse)\b',
                r'\b(relationship problems|family issues|conflict with)\b'
            ],
            'health_stress': [
                r'\b(sick|illness|disease|doctor|hospital|medical|health|pain|surgery)\b',
                r'\b(health problems|medical issues|chronic pain)\b'
            ],
            'social_stress': [
                r'\b(social|people|friends|party|social media|networking|public speaking)\b',
                r'\b(social anxiety|afraid of people|social pressure)\b'
            ]
        }
        
        # Physical stress symptoms
        self.physical_symptoms = {
            'sleep_issues': [
                r'\b(can\'t sleep|insomnia|sleepless|tired|exhausted|fatigue|no energy)\b',
                r'\b(sleep problems|sleeping too much|wake up tired)\b'
            ],
            'appetite_changes': [
                r'\b(not hungry|no appetite|eating too much|binge eating|lost weight|gained weight)\b',
                r'\b(appetite changes|stress eating|comfort food)\b'
            ],
            'physical_tension': [
                r'\b(headache|muscle tension|back pain|neck pain|stomach ache|nausea)\b',
                r'\b(tight chest|heart racing|palpitations|sweating|trembling)\b'
            ],
            'cognitive_symptoms': [
                r'\b(can\'t concentrate|memory problems|confused|forgetful|distracted)\b',
                r'\b(brain fog|can\'t think|overwhelmed|racing thoughts)\b'
            ]
        }
        
        # Emotional indicators
        self.emotional_indicators = {
            'anxiety_markers': [
                r'\b(anxious|worried|nervous|panic|fear|scared|terrified|dread)\b',
                r'\b(what if|worst case|catastrophic thinking|overthinking)\b'
            ],
            'depression_markers': [
                r'\b(sad|depressed|hopeless|empty|worthless|numb|nothing matters)\b',
                r'\b(don\'t care|giving up|no point|why bother)\b'
            ],
            'anger_markers': [
                r'\b(angry|frustrated|irritated|furious|rage|mad|annoyed)\b',
                r'\b(can\'t stand|fed up|had enough|losing patience)\b'
            ],
            'overwhelm_markers': [
                r'\b(overwhelmed|too much|can\'t handle|breaking point|at my limit)\b',
                r'\b(everything is falling apart|can\'t keep up|drowning)\b'
            ]
        }
        
        # Behavioral changes
        self.behavioral_changes = {
            'withdrawal': [
                r'\b(isolating|avoiding|withdrawing|staying home|don\'t want to see)\b',
                r'\b(hiding away|keeping to myself|don\'t go out)\b'
            ],
            'procrastination': [
                r'\b(procrastinating|putting off|avoiding|can\'t start|delaying)\b',
                r'\b(keep postponing|making excuses|running behind)\b'
            ],
            'substance_use': [
                r'\b(drinking|alcohol|smoking|drugs|medication|pills)\b',
                r'\b(need a drink|self medicating|using substances)\b'
            ],
            'compulsive_behaviors': [
                r'\b(can\'t stop|addicted|compulsive|obsessive|checking constantly)\b',
                r'\b(scrolling endlessly|binge watching|shopping therapy)\b'
            ]
        }
        
        # Crisis indicators
        self.crisis_indicators = {
            'suicidal_thoughts': [
                r'\b(suicide|kill myself|end it all|want to die|better off dead)\b',
                r'\b(no reason to live|can\'t go on|thinking about ending)\b'
            ],
            'self_harm': [
                r'\b(hurt myself|harm myself|cut myself|self injury|self harm)\b',
                r'\b(want to hurt myself|thinking about hurting)\b'
            ],
            'severe_hopelessness': [
                r'\b(no hope|hopeless|pointless|nothing will change|stuck forever)\b',
                r'\b(no way out|trapped|nothing helps|given up completely)\b'
            ]
        }
        
        # Positive coping indicators
        self.positive_coping = {
            'seeking_help': [
                r'\b(therapy|counseling|therapist|psychologist|support group)\b',
                r'\b(talking to someone|getting help|reached out)\b'
            ],
            'self_care': [
                r'\b(exercise|meditation|yoga|relaxation|deep breathing|mindfulness)\b',
                r'\b(taking care of myself|self care|healthy habits)\b'
            ],
            'problem_solving': [
                r'\b(making a plan|taking steps|working on it|finding solutions)\b',
                r'\b(trying to fix|addressing the issue|taking action)\b'
            ]
        }
    
    def detect_stress_signals(self, text: str) -> List[str]:
        """
        Detect stress signals in the given text.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            List[str]: List of detected stress indicators
        """
        if not text:
            return []
        
        text_lower = text.lower()
        detected_signals = []
        
        # Check all pattern categories
        all_patterns = {
            **self.stress_patterns,
            **self.physical_symptoms,
            **self.emotional_indicators,
            **self.behavioral_changes
        }
        
        for category, patterns in all_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    detected_signals.append(category)
                    break  # Only add category once
        
        return detected_signals
    
    def assess_stress_level(self, text: str) -> Dict:
        """
        Assess overall stress level based on detected indicators.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            Dict: Stress assessment results
        """
        stress_signals = self.detect_stress_signals(text)
        crisis_signals = self.detect_crisis_indicators(text)
        coping_signals = self.detect_positive_coping(text)
        
        # Calculate stress score
        stress_score = len(stress_signals)
        crisis_score = len(crisis_signals) * 3  # Weight crisis indicators heavily
        coping_score = len(coping_signals) * -0.5  # Positive coping reduces score
        
        total_score = stress_score + crisis_score + coping_score
        
        # Determine stress level
        if crisis_signals or total_score >= 8:
            stress_level = 'critical'
        elif total_score >= 5:
            stress_level = 'high'
        elif total_score >= 3:
            stress_level = 'moderate'
        elif total_score >= 1:
            stress_level = 'mild'
        else:
            stress_level = 'low'
        
        return {
            'stress_level': stress_level,
            'stress_score': total_score,
            'stress_signals': stress_signals,
            'crisis_signals': crisis_signals,
            'coping_signals': coping_signals,
            'signal_count': len(stress_signals),
            'recommendations': self.generate_recommendations(stress_level, stress_signals)
        }
    
    def detect_crisis_indicators(self, text: str) -> List[str]:
        """Detect crisis indicators that require immediate attention."""
        text_lower = text.lower()
        crisis_signals = []
        
        for category, patterns in self.crisis_indicators.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    crisis_signals.append(category)
                    break
        
        return crisis_signals
    
    def detect_positive_coping(self, text: str) -> List[str]:
        """Detect positive coping strategies mentioned in text."""
        text_lower = text.lower()
        coping_signals = []
        
        for category, patterns in self.positive_coping.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    coping_signals.append(category)
                    break
        
        return coping_signals
    
    def analyze_burnout_risk(self, text: str, conversation_history: List[str] = None) -> Dict:
        """
        Analyze risk of burnout based on text and conversation history.
        
        Args:
            text (str): Current message
            conversation_history (List[str]): Previous messages for trend analysis
            
        Returns:
            Dict: Burnout risk assessment
        """
        # Burnout-specific indicators
        burnout_patterns = {
            'exhaustion': r'\b(exhausted|drained|burned out|no energy|depleted|worn out)\b',
            'cynicism': r'\b(don\'t care|what\'s the point|nothing matters|why bother)\b',
            'inefficacy': r'\b(not good enough|failing|can\'t do anything right|useless)\b',
            'detachment': r'\b(disconnected|going through motions|autopilot|numb)\b'
        }
        
        text_lower = text.lower()
        burnout_indicators = []
        
        for indicator, pattern in burnout_patterns.items():
            if re.search(pattern, text_lower, re.IGNORECASE):
                burnout_indicators.append(indicator)
        
        # Analyze conversation history for chronic patterns
        chronic_stress = False
        if conversation_history:
            stress_mentions = sum(1 for msg in conversation_history[-10:] 
                                if any(re.search(pattern, msg.lower()) 
                                      for patterns in self.stress_patterns.values() 
                                      for pattern in patterns))
            chronic_stress = stress_mentions >= 5
        
        # Calculate burnout risk
        if len(burnout_indicators) >= 3 or chronic_stress:
            risk_level = 'high'
        elif len(burnout_indicators) >= 2:
            risk_level = 'moderate'
        elif len(burnout_indicators) >= 1:
            risk_level = 'mild'
        else:
            risk_level = 'low'
        
        return {
            'burnout_risk': risk_level,
            'burnout_indicators': burnout_indicators,
            'chronic_stress_detected': chronic_stress,
            'recommendations': self.generate_burnout_recommendations(risk_level)
        }
    
    def analyze_anxiety_patterns(self, text: str) -> Dict:
        """Analyze anxiety-specific patterns in the text."""
        anxiety_types = {
            'generalized_anxiety': [
                r'\b(worry about everything|constantly worried|anxiety about|what if)\b',
                r'\b(can\'t stop worrying|anxious all the time|general anxiety)\b'
            ],
            'social_anxiety': [
                r'\b(afraid of people|scared of judgment|fear of embarrassment)\b',
                r'\b(social anxiety|afraid to speak up|nervous around people)\b'
            ],
            'panic_anxiety': [
                r'\b(panic attack|can\'t breathe|heart racing|chest tight)\b',
                r'\b(feeling like dying|losing control|panic disorder)\b'
            ],
            'performance_anxiety': [
                r'\b(test anxiety|presentation anxiety|performance fear)\b',
                r'\b(afraid of failing|nervous about performance|stage fright)\b'
            ]
        }
        
        text_lower = text.lower()
        detected_types = []
        
        for anxiety_type, patterns in anxiety_types.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    detected_types.append(anxiety_type)
                    break
        
        # Calculate anxiety severity
        anxiety_intensity_markers = [
            r'\b(extremely|severely|overwhelming|unbearable|intense)\b',
            r'\b(can\'t function|paralyzing|debilitating|constant)\b'
        ]
        
        high_intensity = any(re.search(marker, text_lower) 
                           for marker in anxiety_intensity_markers)
        
        return {
            'anxiety_types': detected_types,
            'high_intensity': high_intensity,
            'severity': 'high' if high_intensity else 'moderate' if detected_types else 'low'
        }
    
    def generate_recommendations(self, stress_level: str, stress_signals: List[str]) -> List[str]:
        """Generate personalized recommendations based on stress assessment."""
        recommendations = []
        
        if stress_level == 'critical':
            recommendations.extend([
                "Please consider reaching out to a mental health professional immediately",
                "Contact a crisis helpline if you're having thoughts of self-harm",
                "Reach out to a trusted friend or family member for support"
            ])
        
        elif stress_level == 'high':
            recommendations.extend([
                "Consider speaking with a therapist or counselor",
                "Practice deep breathing or meditation techniques",
                "Prioritize rest and sleep"
            ])
        
        elif stress_level == 'moderate':
            recommendations.extend([
                "Try stress-reduction techniques like mindfulness or yoga",
                "Ensure you're getting adequate sleep and exercise",
                "Consider talking to someone you trust about your concerns"
            ])
        
        # Specific recommendations based on detected signals
        if 'work_stress' in stress_signals:
            recommendations.append("Consider setting boundaries at work and taking regular breaks")
        
        if 'sleep_issues' in stress_signals:
            recommendations.append("Focus on improving sleep hygiene and establishing a bedtime routine")
        
        if 'social_stress' in stress_signals:
            recommendations.append("Practice gradual exposure to social situations you find comfortable")
        
        return recommendations
    
    def generate_burnout_recommendations(self, risk_level: str) -> List[str]:
        """Generate burnout-specific recommendations."""
        recommendations = []
        
        if risk_level == 'high':
            recommendations.extend([
                "Consider taking time off work if possible",
                "Speak with a healthcare provider about burnout",
                "Reassess your workload and priorities",
                "Engage in activities that bring you joy and meaning"
            ])
        elif risk_level == 'moderate':
            recommendations.extend([
                "Set clearer boundaries between work and personal time",
                "Practice regular self-care activities",
                "Consider delegating tasks when possible"
            ])
        else:
            recommendations.extend([
                "Maintain work-life balance",
                "Continue practicing stress management techniques"
            ])
        
        return recommendations
    
    def get_stress_summary(self, text: str, conversation_history: List[str] = None) -> Dict:
        """Get comprehensive stress analysis summary."""
        stress_assessment = self.assess_stress_level(text)
        burnout_analysis = self.analyze_burnout_risk(text, conversation_history)
        anxiety_analysis = self.analyze_anxiety_patterns(text)
        
        return {
            'overall_assessment': stress_assessment,
            'burnout_analysis': burnout_analysis,
            'anxiety_analysis': anxiety_analysis,
            'timestamp': datetime.now().isoformat(),
            'requires_immediate_attention': (
                stress_assessment['stress_level'] == 'critical' or
                len(stress_assessment['crisis_signals']) > 0
            )
        }
