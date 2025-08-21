import openai
import streamlit as st
import pandas as pd
import numpy as np
import json
import logging
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional


# Import custom modules
from sentiment_analyzer import SentimentAnalyzer
from stress_detector import StressDetector
from wellness_recommender import WellnessRecommender
from data_handler import DataHandler
from emergency_handler import EmergencyHandler
from privacy_manager import PrivacyManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MentalHealthChatbot:

    def gpt_health_companion_response(self, message: str, chat_history: list = None) -> str:
        """Use OpenAI GPT API to generate a friendly, context-aware health companion response."""
        openai.api_key = "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"
        system_prompt = (
            "You are MindCare AI, a friendly, supportive, and empathetic mental health companion. "
            "Respond to the user in a conversational, non-repetitive, and impactful way. "
            "Offer encouragement, ask thoughtful questions, and provide emotional support. "
            "If the user expresses distress, respond with extra care and suggest helpful resources."
        )
        messages = [{"role": "system", "content": system_prompt}]
        if chat_history:
            for entry in chat_history:
                messages.append({"role": entry["role"], "content": entry["content"]})
        messages.append({"role": "user", "content": message})
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=200,
                temperature=0.8,
                n=1
            )
            return response.choices[0].message["content"].strip()
        except Exception as e:
            return f"Sorry, I couldn't connect to the health companion service right now. ({e})"
    def __init__(self):
        """Initialize the mental health chatbot with all necessary components."""
        self.sentiment_analyzer = SentimentAnalyzer()
        self.stress_detector = StressDetector()
        self.wellness_recommender = WellnessRecommender()
        self.data_handler = DataHandler()
        self.emergency_handler = EmergencyHandler()
        self.privacy_manager = PrivacyManager()
        
        # Initialize session state
        self.init_session_state()
    
    def init_session_state(self):
        """Initialize Streamlit session state variables."""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'user_profile' not in st.session_state:
            st.session_state.user_profile = {
                'stress_level': 0,
                'anxiety_indicators': [],
                'burnout_risk': 'low',
                'conversation_count': 0,
                'last_check_in': None
            }
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'wellness_streak' not in st.session_state:
            st.session_state.wellness_streak = 0
    
    def analyze_message(self, message: str) -> Dict:
        """
        Analyze user message for mental health indicators.
        
        Args:
            message (str): User's message text
            
        Returns:
            Dict: Analysis results including sentiment, stress indicators, etc.
        """
        try:
            # Sentiment analysis
            sentiment_score = self.sentiment_analyzer.analyze(message)
            
            # Stress detection
            stress_indicators = self.stress_detector.detect_stress_signals(message)
            
            # Context analysis
            context = self.analyze_conversation_context()
            
            analysis = {
                'sentiment': sentiment_score,
                'stress_indicators': stress_indicators,
                'context': context,
                'timestamp': datetime.now(),
                'message_length': len(message),
                'urgency_level': self.assess_urgency(message, sentiment_score, stress_indicators)
            }
            
            # Update user profile
            self.update_user_profile(analysis)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing message: {str(e)}")
            return {'error': str(e)}
    
    def assess_urgency(self, message: str, sentiment: Dict, stress_indicators: List) -> str:
        """Assess the urgency level of the user's message."""
        emergency_keywords = [
            'suicide', 'kill myself', 'end it all', 'no point', 'hopeless',
            'harm myself', 'want to die', 'can\'t go on', 'giving up'
        ]
        
        high_stress_indicators = [
            'panic attack', 'can\'t breathe', 'heart racing', 'overwhelming',
            'breaking down', 'falling apart', 'can\'t cope'
        ]
        
        message_lower = message.lower()
        
        # Check for emergency keywords
        if any(keyword in message_lower for keyword in emergency_keywords):
            return 'emergency'
        
        # Check for high stress indicators
        if any(indicator in message_lower for indicator in high_stress_indicators):
            return 'high'
        
        # Check sentiment and stress levels
        if sentiment.get('compound', 0) < -0.7 or len(stress_indicators) >= 3:
            return 'high'
        elif sentiment.get('compound', 0) < -0.3 or len(stress_indicators) >= 1:
            return 'medium'
        
        return 'low'
    
    def update_user_profile(self, analysis: Dict):
        """Update user profile based on conversation analysis."""
        profile = st.session_state.user_profile
        
        # Update stress level (rolling average)
        if 'sentiment' in analysis:
            new_stress = max(0, min(10, 5 - (analysis['sentiment'].get('compound', 0) * 5)))
            profile['stress_level'] = (profile['stress_level'] * 0.7) + (new_stress * 0.3)
        
        # Update anxiety indicators
        if analysis.get('stress_indicators'):
            profile['anxiety_indicators'].extend(analysis['stress_indicators'])
            # Keep only recent indicators (last 10)
            profile['anxiety_indicators'] = profile['anxiety_indicators'][-10:]
        
        # Update burnout risk
        profile['burnout_risk'] = self.assess_burnout_risk(profile)
        profile['conversation_count'] += 1
        profile['last_check_in'] = datetime.now()
    
    def assess_burnout_risk(self, profile: Dict) -> str:
        """Assess burnout risk based on user profile."""
        stress_level = profile.get('stress_level', 0)
        anxiety_count = len(profile.get('anxiety_indicators', []))
        
        if stress_level > 7 and anxiety_count > 5:
            return 'high'
        elif stress_level > 5 and anxiety_count > 3:
            return 'medium'
        else:
            return 'low'
    
    def analyze_conversation_context(self) -> Dict:
        """Analyze the broader conversation context."""
        messages = st.session_state.messages[-5:]  # Last 5 messages
        
        context = {
            'conversation_length': len(st.session_state.messages),
            'recent_topics': [],
            'mood_trend': 'stable',
            'engagement_level': 'medium'
        }
        
        # Analyze recent topics and mood trends
        if messages:
            sentiments = []
            for msg in messages:
                if msg.get('role') == 'user':
                    sentiment = self.sentiment_analyzer.analyze(msg['content'])
                    sentiments.append(sentiment.get('compound', 0))
            
            if len(sentiments) >= 2:
                if sentiments[-1] < sentiments[0] - 0.2:
                    context['mood_trend'] = 'declining'
                elif sentiments[-1] > sentiments[0] + 0.2:
                    context['mood_trend'] = 'improving'
        
        return context
    
    def generate_response(self, message: str, analysis: Dict) -> str:
        """Generate appropriate response using OpenAI GPT as a health companion, with fallback to local logic."""
        urgency = analysis.get('urgency_level', 'low')
        # Handle emergency situations
        if urgency == 'emergency':
            return self.emergency_handler.handle_crisis(message, analysis)
        # Use OpenAI GPT for dynamic, friendly, and context-aware responses
        chat_history = st.session_state.get('messages', [])
        gpt_response = self.gpt_health_companion_response(message, chat_history)
        # Add wellness recommendations
        recommendations = self.wellness_recommender.get_recommendations(
            st.session_state.user_profile,
            analysis
        )
        if recommendations:
            gpt_response += "\n\n" + recommendations
        return gpt_response
    
    def generate_supportive_response(self, message: str, analysis: Dict) -> str:
        """Generate supportive, friendly, and context-aware response for high-stress situations."""
        import random
        stress_indicators = analysis.get('stress_indicators', [])
        personalized = []
        if 'work_stress' in stress_indicators:
            personalized.append("It sounds like work has been weighing on you lately. That's a lot to carry—I'm here to help you process it.")
        if 'sleep_issues' in stress_indicators:
            personalized.append("Sleep troubles can make everything feel harder. Let's talk about ways to help you rest better.")
        if 'overwhelm' in stress_indicators or 'panic' in message.lower():
            personalized.append("Feeling overwhelmed is tough, but you're not alone in this. Let's take it one step at a time together.")
        base_templates = [
            f"Thank you for opening up to me. I can tell this is a really tough moment for you. {random.choice(personalized) if personalized else ''} Is there something specific that's been on your mind today?",
            f"I'm really glad you reached out. Your feelings are valid, and you deserve support. {random.choice(personalized) if personalized else ''} Would you like to talk more about what's been hardest lately?",
            f"It takes courage to share what you're going through. {random.choice(personalized) if personalized else ''} Remember, I'm here to listen and help however I can.",
            f"What you're experiencing sounds overwhelming. {random.choice(personalized) if personalized else ''} If you want, we can explore some ways to make things feel a bit more manageable."
        ]
        response = random.choice(base_templates).strip()
        # Add a friendly follow-up
        follow_ups = [
            "Would you like to try a calming exercise together?",
            "If you want, I can suggest a small self-care activity right now.",
            "Let me know if you just want to vent or if you'd like some ideas to help cope.",
            "Remember, you can share as much or as little as you want—I'm here for you."
        ]
        if random.random() > 0.5:
            response += "\n\n" + random.choice(follow_ups)
        return response
    
    def generate_empathetic_response(self, message: str, analysis: Dict) -> str:
        """Generate empathetic, conversational, and situation-aware response for negative sentiment."""
        import random
        # Try to echo the user's feeling in a natural way
        feeling_templates = [
            f"It sounds like you're really going through it right now. If you want to share more, I'm here to listen.",
            f"I can sense this hasn't been easy for you. What do you think would help you feel even a little bit better today?",
            f"Thank you for trusting me with how you're feeling. Sometimes just saying it out loud (or typing it!) can help a bit.",
            f"I'm sorry things are feeling heavy. If you want, we can talk through what's been hardest or just chat about anything on your mind."
        ]
        # Add a friendly, human touch
        friendly_addons = [
            "Remember, tough days don't last forever—even if it feels that way right now.",
            "You're not alone, and you don't have to figure everything out at once.",
            "If you want a distraction or a little encouragement, just let me know!",
            "I'm here for you, no judgment—just support."
        ]
        response = random.choice(feeling_templates)
        if random.random() > 0.4:
            response += "\n\n" + random.choice(friendly_addons)
        return response
    
    def generate_encouraging_response(self, message: str, analysis: Dict) -> str:
        """Generate encouraging, friendly, and varied response for neutral/positive interactions."""
        import random
        starters = [
            "It's great to hear from you!",
            "Thanks for checking in today!",
            "I'm glad you're here and taking a moment for yourself.",
            "Hey there!"
        ]
        questions = [
            "What's something that's gone well for you recently?",
            "Is there anything you're looking forward to this week?",
            "How are you feeling about things overall?",
            "Anything on your mind you'd like to talk about or celebrate?"
        ]
        encouragements = [
            "Remember, every step you take for your mental health matters—even the small ones.",
            "Taking care of yourself is a big deal, and I'm here to support you however I can.",
            "If you want to try a new wellness tip or just chat, let me know!",
            "You deserve to feel good about the progress you're making."
        ]
        response = f"{random.choice(starters)} {random.choice(questions)}\n\n{random.choice(encouragements)}"
        return response
    
    def display_dashboard(self):
        """Display user dashboard with mental health metrics."""
        st.sidebar.title("Your Mental Health Dashboard")
        
        profile = st.session_state.user_profile
        
        # Stress level indicator
        stress_color = 'red' if profile['stress_level'] > 6 else 'yellow' if profile['stress_level'] > 3 else 'green'
        st.sidebar.metric(
            "Current Stress Level",
            f"{profile['stress_level']:.1f}/10",
            delta=None
        )
        
        # Burnout risk
        risk_color = {'low': '🟢', 'medium': '🟡', 'high': '🔴'}
        st.sidebar.write(f"Burnout Risk: {risk_color[profile['burnout_risk']]} {profile['burnout_risk'].title()}")
        
        # Wellness streak
        st.sidebar.metric("Wellness Streak", f"{st.session_state.wellness_streak} days")
        
        # Recent check-ins
        if profile['last_check_in']:
            time_since = datetime.now() - profile['last_check_in']
            st.sidebar.write(f"Last check-in: {time_since.days} days ago")
        
        # Conversation count
        st.sidebar.write(f"Total conversations: {profile['conversation_count']}")
    
    def display_analytics(self):
        """Display analytics and trends."""
        if st.sidebar.button("📊 View Analytics"):
            st.subheader("Mental Health Analytics")
            
            # Create sample trend data (in a real app, this would come from stored data)
            dates = pd.date_range(start='2024-01-01', end='2024-01-30', freq='D')
            stress_data = np.random.normal(5, 2, len(dates))
            mood_data = np.random.normal(0, 0.5, len(dates))
            
            # Stress trend chart
            fig_stress = px.line(
                x=dates, y=stress_data,
                title="Stress Level Trend (30 Days)",
                labels={'x': 'Date', 'y': 'Stress Level'}
            )
            st.plotly_chart(fig_stress)
            
            # Mood trend chart
            fig_mood = px.line(
                x=dates, y=mood_data,
                title="Mood Trend (30 Days)",
                labels={'x': 'Date', 'y': 'Mood Score'}
            )
            st.plotly_chart(fig_mood)

def main():
    """Main application function."""
    st.set_page_config(
        page_title="MindCare AI - Mental Health Companion",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    /* Set main background to black and text to white */
    .stApp {
        background-color: #111 !important;
        color: #f5f5f5 !important;
    }
    .main-header {
        text-align: center;
        color: #7ecbff;
        margin-bottom: 30px;
        font-weight: bold;
        text-shadow: 1px 1px 4px #000;
    }
    .chat-message {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        color: #f5f5f5;
    }
    .user-message {
        background-color: #23272b;
        border-left: 4px solid #7ecbff;
    }
    .bot-message {
        background-color: #1a2a1a;
        border-left: 4px solid #7fff7e;
    }
    .emergency-alert {
        background-color: #2d0000;
        border: 2px solid #ff4c4c;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        color: #fff;
    }
    .wellness-tip {
        background-color: #2a1a00;
        border-left: 4px solid #ffc107;
        padding: 15px;
        margin: 10px 0;
        border-radius: 5px;
        color: #fffbe7;
    }
    /* Sidebar background and text */
    section[data-testid="stSidebar"] {
        background-color: #181818 !important;
        color: #f5f5f5 !important;
    }
    /* Metric and button tweaks for dark mode */
    .stMetric {
        color: #fff !important;
    }
    .stButton>button {
        background-color: #222 !important;
        color: #fff !important;
        border: 1px solid #7ecbff !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize chatbot
    chatbot = MentalHealthChatbot()
    
    # Main header
    st.markdown("<h1 class='main-header'>🧠 MindCare AI - Your Mental Health Companion</h1>", unsafe_allow_html=True)
    
    # Display dashboard
    chatbot.display_dashboard()
    
    # Privacy notice
    st.sidebar.markdown("---")
    st.sidebar.markdown("🔒 **Privacy & Security**")
    st.sidebar.markdown("Your conversations are processed securely and anonymously. No personal data is stored permanently.")
    
    # Emergency resources
    st.sidebar.markdown("---")
    st.sidebar.markdown("🚨 **Crisis Resources**")
    st.sidebar.markdown("""
    - **National Suicide Prevention Lifeline**: 988
    - **Crisis Text Line**: Text HOME to 741741
    - **International Association for Suicide Prevention**: https://www.iasp.info/resources/Crisis_Centres/
    """)
    
    # Main chat interface
    st.markdown("### Chat with MindCare AI")
    st.markdown("*I'm here to listen and support your mental wellness journey. Share what's on your mind.*")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message">👤 **You:** {message["content"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message bot-message">🤖 **MindCare AI:** {message["content"]}</div>', 
                           unsafe_allow_html=True)
    
    # Chat input
    if user_input := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Analyze the message
        with st.spinner("Analyzing your message..."):
            analysis = chatbot.analyze_message(user_input)
        
        # Generate response
        response = chatbot.generate_response(user_input, analysis)
        
        # Add bot response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Store conversation data (privacy-compliant)
        chatbot.data_handler.store_conversation_data({
            'timestamp': datetime.now(),
            'sentiment': analysis.get('sentiment', {}),
            'stress_level': st.session_state.user_profile['stress_level'],
            'urgency': analysis.get('urgency_level', 'low')
        })
        
        # Check for emergency situations
        if analysis.get('urgency_level') == 'emergency':
            st.markdown("""
            <div class="emergency-alert">
                <h3>🚨 Emergency Support</h3>
                <p>I'm concerned about you. Please consider reaching out to a mental health professional or crisis hotline immediately.</p>
                <p><strong>National Suicide Prevention Lifeline: 988</strong></p>
                <p><strong>Crisis Text Line: Text HOME to 741741</strong></p>
            </div>
            """, unsafe_allow_html=True)
        
        # Refresh the page to show new messages
        st.rerun()
    
    # Daily wellness check
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯 Daily Wellness Check"):
            wellness_check = chatbot.wellness_recommender.daily_wellness_check()
            st.markdown(f'<div class="wellness-tip">{wellness_check}</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("📱 Quick Mood Booster"):
            mood_booster = chatbot.wellness_recommender.get_mood_booster()
            st.markdown(f'<div class="wellness-tip">{mood_booster}</div>', unsafe_allow_html=True)
    
    # Analytics
    chatbot.display_analytics()

if __name__ == "__main__":
    main()
