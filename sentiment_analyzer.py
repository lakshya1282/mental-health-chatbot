import nltk
from textblob import TextBlob
import re
from typing import Dict, List
import numpy as np
from collections import Counter

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

from nltk.sentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self):
        """Initialize sentiment analyzer with VADER and TextBlob."""
        self.vader = SentimentIntensityAnalyzer()
        
        # Mental health related keywords and their weights
        self.mental_health_keywords = {
            'anxiety': -0.8,
            'anxious': -0.7,
            'worried': -0.6,
            'stress': -0.7,
            'stressed': -0.8,
            'depression': -0.9,
            'depressed': -0.8,
            'sad': -0.6,
            'overwhelmed': -0.8,
            'hopeless': -0.9,
            'exhausted': -0.7,
            'tired': -0.5,
            'burnout': -0.8,
            'panic': -0.8,
            'fear': -0.7,
            'afraid': -0.7,
            'lonely': -0.7,
            'isolated': -0.7,
            'worthless': -0.9,
            'empty': -0.8,
            'numb': -0.7,
            'angry': -0.6,
            'frustrated': -0.6,
            'irritated': -0.5,
            'happy': 0.7,
            'joy': 0.8,
            'excited': 0.7,
            'grateful': 0.8,
            'peaceful': 0.7,
            'calm': 0.6,
            'relaxed': 0.6,
            'confident': 0.7,
            'hopeful': 0.8,
            'optimistic': 0.8,
            'energetic': 0.7,
            'motivated': 0.7
        }
        
        # Intensity modifiers
        self.intensity_modifiers = {
            'very': 1.3,
            'extremely': 1.5,
            'really': 1.2,
            'quite': 1.1,
            'somewhat': 0.8,
            'slightly': 0.7,
            'a bit': 0.7,
            'kind of': 0.8,
            'sort of': 0.8
        }
    
    def analyze(self, text: str) -> Dict:
        """
        Perform comprehensive sentiment analysis on the given text.
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            Dict: Sentiment analysis results
        """
        if not text or not text.strip():
            return {'compound': 0, 'positive': 0, 'negative': 0, 'neutral': 1}
        
        # Clean text
        cleaned_text = self.preprocess_text(text)
        
        # VADER analysis
        vader_scores = self.vader.polarity_scores(cleaned_text)
        
        # TextBlob analysis
        blob = TextBlob(cleaned_text)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        # Custom mental health keyword analysis
        mh_score = self.analyze_mental_health_keywords(cleaned_text)
        
        # Combine scores with weights
        combined_compound = (
            vader_scores['compound'] * 0.4 +
            textblob_polarity * 0.3 +
            mh_score * 0.3
        )
        
        # Emotion detection
        emotions = self.detect_emotions(cleaned_text)
        
        # Risk indicators
        risk_indicators = self.detect_risk_indicators(cleaned_text)
        
        return {
            'compound': combined_compound,
            'positive': vader_scores['pos'],
            'negative': vader_scores['neg'],
            'neutral': vader_scores['neu'],
            'textblob_polarity': textblob_polarity,
            'textblob_subjectivity': textblob_subjectivity,
            'mental_health_score': mh_score,
            'emotions': emotions,
            'risk_indicators': risk_indicators,
            'text_length': len(text),
            'sentence_count': len(blob.sentences)
        }
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text for analysis."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Handle negations (important for mental health context)
        text = re.sub(r'\b(not|no|never|nothing|nobody|nowhere|neither|nor|none)\s+', 'not_', text)
        
        return text
    
    def analyze_mental_health_keywords(self, text: str) -> float:
        """Analyze text for mental health related keywords."""
        words = text.split()
        total_score = 0
        keyword_count = 0
        
        for i, word in enumerate(words):
            # Check for direct keyword matches
            if word in self.mental_health_keywords:
                score = self.mental_health_keywords[word]
                
                # Check for intensity modifiers
                if i > 0 and words[i-1] in self.intensity_modifiers:
                    score *= self.intensity_modifiers[words[i-1]]
                
                total_score += score
                keyword_count += 1
        
        # Normalize score
        if keyword_count > 0:
            return total_score / keyword_count
        return 0
    
    def detect_emotions(self, text: str) -> Dict:
        """Detect specific emotions in the text."""
        emotion_patterns = {
            'anxiety': r'\b(anxious|anxiety|worried|worry|nervous|panic|panicking)\b',
            'depression': r'\b(depressed|depression|sad|sadness|hopeless|empty|worthless)\b',
            'stress': r'\b(stressed|stress|overwhelmed|pressure|burden|exhausted)\b',
            'anger': r'\b(angry|anger|frustrated|frustration|irritated|mad|furious)\b',
            'fear': r'\b(afraid|fear|scared|terrified|frightened)\b',
            'loneliness': r'\b(lonely|alone|isolated|disconnected)\b',
            'joy': r'\b(happy|happiness|joy|joyful|excited|thrilled|delighted)\b',
            'gratitude': r'\b(grateful|thankful|blessed|appreciate|appreciation)\b',
            'hope': r'\b(hopeful|hope|optimistic|positive|confident)\b',
            'calm': r'\b(calm|peaceful|relaxed|serene|tranquil)\b'
        }
        
        detected_emotions = {}
        for emotion, pattern in emotion_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                detected_emotions[emotion] = len(matches)
        
        return detected_emotions
    
    def detect_risk_indicators(self, text: str) -> List[str]:
        """Detect risk indicators in the text."""
        risk_patterns = {
            'suicidal_ideation': r'\b(suicide|kill myself|end it all|want to die|no point living|better off dead)\b',
            'self_harm': r'\b(hurt myself|harm myself|cut myself|self harm)\b',
            'severe_depression': r'\b(can\'t go on|giving up|no hope|nothing matters|worthless)\b',
            'panic_disorder': r'\b(panic attack|can\'t breathe|heart racing|losing control)\b',
            'substance_abuse': r'\b(drinking too much|using drugs|can\'t stop drinking|substance|addiction)\b',
            'eating_disorder': r'\b(not eating|binge eating|purging|body image|too fat|too thin)\b',
            'sleep_disorder': r'\b(can\'t sleep|insomnia|nightmares|sleeping too much|sleep problems)\b',
            'social_withdrawal': r'\b(avoiding people|don\'t want to see anyone|isolating|withdrawing)\b'
        }
        
        risk_indicators = []
        for risk_type, pattern in risk_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                risk_indicators.append(risk_type)
        
        return risk_indicators
    
    def get_sentiment_label(self, compound_score: float) -> str:
        """Convert compound score to sentiment label."""
        if compound_score >= 0.05:
            return 'positive'
        elif compound_score <= -0.05:
            return 'negative'
        else:
            return 'neutral'
    
    def get_emotional_state(self, analysis: Dict) -> str:
        """Determine overall emotional state based on analysis."""
        compound = analysis.get('compound', 0)
        emotions = analysis.get('emotions', {})
        risk_indicators = analysis.get('risk_indicators', [])
        
        # High risk situations
        if risk_indicators:
            if 'suicidal_ideation' in risk_indicators or 'self_harm' in risk_indicators:
                return 'crisis'
            elif len(risk_indicators) >= 2:
                return 'high_risk'
            else:
                return 'at_risk'
        
        # Based on compound sentiment and emotions
        if compound <= -0.7:
            return 'severe_distress'
        elif compound <= -0.3:
            return 'mild_distress'
        elif compound >= 0.3:
            return 'positive'
        else:
            return 'neutral'
    
    def analyze_conversation_trend(self, messages: List[str]) -> Dict:
        """Analyze sentiment trend across multiple messages."""
        if not messages:
            return {'trend': 'stable', 'average_sentiment': 0}
        
        sentiments = []
        for message in messages:
            analysis = self.analyze(message)
            sentiments.append(analysis['compound'])
        
        # Calculate trend
        if len(sentiments) >= 2:
            trend_slope = np.polyfit(range(len(sentiments)), sentiments, 1)[0]
            if trend_slope > 0.1:
                trend = 'improving'
            elif trend_slope < -0.1:
                trend = 'declining'
            else:
                trend = 'stable'
        else:
            trend = 'insufficient_data'
        
        return {
            'trend': trend,
            'average_sentiment': np.mean(sentiments),
            'sentiment_variance': np.var(sentiments),
            'message_count': len(messages)
        }
