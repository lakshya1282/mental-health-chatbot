import logging
from typing import Dict, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class EmergencyHandler:
    def __init__(self):
        """Initialize emergency handler with crisis resources and protocols."""
        
        # Crisis hotlines and resources
        self.crisis_resources = {
            'us': {
                'suicide_prevention': {
                    'name': 'National Suicide Prevention Lifeline',
                    'phone': '988',
                    'text': 'Text "HELLO" to 741741',
                    'website': 'https://suicidepreventionlifeline.org'
                },
                'crisis_text_line': {
                    'name': 'Crisis Text Line',
                    'text': 'Text HOME to 741741',
                    'website': 'https://www.crisistextline.org'
                },
                'emergency': {
                    'name': 'Emergency Services',
                    'phone': '911',
                    'description': 'For immediate danger or medical emergency'
                }
            },
            'international': {
                'suicide_prevention': {
                    'name': 'International Association for Suicide Prevention',
                    'website': 'https://www.iasp.info/resources/Crisis_Centres/',
                    'description': 'Find crisis centers worldwide'
                },
                'befrienders': {
                    'name': 'Befrienders Worldwide',
                    'website': 'https://www.befrienders.org',
                    'description': 'Emotional support worldwide'
                }
            }
        }
        
        # Crisis indicators and severity levels
        self.crisis_indicators = {
            'immediate_danger': [
                'kill myself', 'end my life', 'suicide', 'want to die',
                'better off dead', 'no point living', 'taking my life',
                'ending it all', 'can\'t go on', 'giving up on life'
            ],
            'self_harm': [
                'hurt myself', 'harm myself', 'cut myself', 'injure myself',
                'self harm', 'self injury', 'want to hurt', 'cutting myself'
            ],
            'severe_distress': [
                'can\'t take it anymore', 'breaking point', 'falling apart',
                'losing control', 'going crazy', 'can\'t handle', 'overwhelmed completely',
                'nothing matters', 'hopeless', 'trapped', 'no way out'
            ],
            'substance_crisis': [
                'overdose', 'too many pills', 'drinking to forget',
                'using drugs to cope', 'can\'t stop drinking', 'substance abuse'
            ]
        }
        
        # De-escalation techniques
        self.de_escalation_responses = [
            "I'm really concerned about you right now. Your life has value, and you matter.",
            "I can hear that you're in tremendous pain. You don't have to face this alone.",
            "What you're feeling right now is overwhelming, but these feelings can change.",
            "I want to help you find support right away. You deserve to be safe and cared for.",
            "This crisis you're experiencing is temporary, even though it doesn't feel that way right now."
        ]
        
        # Safety planning elements
        self.safety_planning = {
            'immediate_actions': [
                "Remove any means of self-harm from your immediate environment",
                "Go to a safe space where you're not alone, if possible",
                "Call a trusted friend, family member, or crisis helpline",
                "Focus on your breathing - take slow, deep breaths",
                "Ground yourself: name 5 things you can see, 4 you can hear, 3 you can touch"
            ],
            'coping_strategies': [
                "Call or text a crisis helpline - they're available 24/7",
                "Use ice cubes on your skin for intense physical sensation without harm",
                "Take a cold shower or splash cold water on your face",
                "Do intense exercise like running in place or doing jumping jacks",
                "Listen to loud music or watch funny videos to change your mental state"
            ],
            'support_contacts': [
                "Emergency services (911) for immediate danger",
                "National Suicide Prevention Lifeline: 988",
                "Crisis Text Line: Text HOME to 741741",
                "A trusted friend or family member",
                "Your therapist, counselor, or doctor"
            ]
        }
    
    def assess_crisis_level(self, message: str, analysis: Dict) -> str:
        """
        Assess the crisis level based on message content and analysis.
        
        Args:
            message (str): User's message
            analysis (Dict): Message analysis results
            
        Returns:
            str: Crisis level ('none', 'low', 'moderate', 'high', 'emergency')
        """
        message_lower = message.lower()
        
        # Check for immediate danger indicators
        immediate_danger_count = sum(1 for indicator in self.crisis_indicators['immediate_danger'] 
                                   if indicator in message_lower)
        
        self_harm_count = sum(1 for indicator in self.crisis_indicators['self_harm'] 
                            if indicator in message_lower)
        
        severe_distress_count = sum(1 for indicator in self.crisis_indicators['severe_distress'] 
                                  if indicator in message_lower)
        
        substance_crisis_count = sum(1 for indicator in self.crisis_indicators['substance_crisis'] 
                                   if indicator in message_lower)
        
        # Get sentiment analysis
        sentiment_score = analysis.get('sentiment', {}).get('compound', 0)
        risk_indicators = analysis.get('risk_indicators', [])
        
        # Determine crisis level
        if immediate_danger_count >= 1 or 'suicidal_ideation' in risk_indicators:
            return 'emergency'
        elif self_harm_count >= 1 or 'self_harm' in risk_indicators:
            return 'high'
        elif severe_distress_count >= 2 or sentiment_score < -0.8:
            return 'moderate'
        elif severe_distress_count >= 1 or sentiment_score < -0.5:
            return 'low'
        else:
            return 'none'
    
    def handle_crisis(self, message: str, analysis: Dict) -> str:
        """
        Handle crisis situation with appropriate response.
        
        Args:
            message (str): User's message
            analysis (Dict): Message analysis results
            
        Returns:
            str: Crisis response message
        """
        crisis_level = self.assess_crisis_level(message, analysis)
        
        # Log crisis situation (anonymized)
        logger.warning(f"Crisis level {crisis_level} detected at {datetime.now()}")
        
        if crisis_level == 'emergency':
            return self._handle_emergency_crisis(message)
        elif crisis_level == 'high':
            return self._handle_high_crisis(message)
        elif crisis_level == 'moderate':
            return self._handle_moderate_crisis(message)
        elif crisis_level == 'low':
            return self._handle_low_crisis(message)
        else:
            return self._handle_general_support(message)
    
    def _handle_emergency_crisis(self, message: str) -> str:
        """Handle emergency-level crisis."""
        response = """🚨 **EMERGENCY SUPPORT NEEDED** 🚨

I'm very concerned about you right now. Your life matters, and you deserve immediate support.

**PLEASE REACH OUT RIGHT NOW:**
• **Call 911** if you're in immediate danger
• **Call 988** (National Suicide Prevention Lifeline) - available 24/7
• **Text HOME to 741741** (Crisis Text Line) - available 24/7
• **Go to your nearest emergency room**

**You are not alone.** Trained professionals are ready to help you through this crisis.

**If you can't make the call, ask someone to help you or call for you.**

**Remember:** This intense pain you're feeling right now is temporary. There are people who want to help you through this."""
        
        return response
    
    def _handle_high_crisis(self, message: str) -> str:
        """Handle high-level crisis involving self-harm thoughts."""
        response = """🔴 **URGENT: Please Get Support Now** 🔴

I can see that you're going through an extremely difficult time, and I'm worried about you.

**IMMEDIATE RESOURCES:**
• **National Suicide Prevention Lifeline: 988** (24/7)
• **Crisis Text Line: Text HOME to 741741**
• **Call a trusted friend, family member, or mental health professional**

**RIGHT NOW, PLEASE:**
1. Remove any means of harm from your area
2. Go somewhere safe, preferably with others
3. Reach out to one of the resources above
4. Focus on your breathing - take deep, slow breaths

**Remember:** These overwhelming feelings are temporary. You deserve support and care. Professional help is available right now."""
        
        return response
    
    def _handle_moderate_crisis(self, message: str) -> str:
        """Handle moderate crisis level."""
        import random
        
        de_escalation = random.choice(self.de_escalation_responses)
        
        response = f"""🟡 **You Need Support Right Now** 🟡

{de_escalation}

**HELPFUL RESOURCES:**
• **Talk to someone now: 988** (National Suicide Prevention Lifeline)
• **Text support: HOME to 741741** (Crisis Text Line)
• **Online chat: suicidepreventionlifeline.org**

**IMMEDIATE COPING STRATEGIES:**
• Take 10 deep breaths, counting slowly
• Use the 5-4-3-2-1 grounding technique
• Call someone you trust
• Remove yourself from stressful situations if possible

**Remember:** You don't have to handle this alone. Reaching out for help is a sign of strength, not weakness."""
        
        return response
    
    def _handle_low_crisis(self, message: str) -> str:
        """Handle low-level crisis."""
        response = """🟠 **Let's Get You Some Support** 🟠

I can hear that you're struggling, and I want you to know that what you're feeling is valid.

**SUPPORT OPTIONS:**
• **If you need to talk to someone: 988** (National Suicide Prevention Lifeline)
• **Text support: HOME to 741741** (Crisis Text Line)
• **Consider reaching out to a counselor or therapist**

**COPING STRATEGIES TO TRY NOW:**
• Practice deep breathing or meditation
• Take a walk or do some gentle exercise
• Reach out to a trusted friend or family member
• Engage in a comforting activity

**Remember:** It's okay to not be okay. You're taking a positive step by recognizing these feelings and seeking support."""
        
        return response
    
    def _handle_general_support(self, message: str) -> str:
        """Provide general supportive response."""
        return """💙 **You're Not Alone** 💙

Thank you for sharing your feelings with me. It takes courage to express when you're struggling.

**ALWAYS AVAILABLE:**
• **988** - National Suicide Prevention Lifeline (24/7)
• **Text HOME to 741741** - Crisis Text Line (24/7)

**Building Your Support Network:**
• Consider talking to a counselor or therapist
• Connect with trusted friends or family
• Look into local support groups
• Practice regular self-care

Remember: Mental health struggles are common, and seeking help is a sign of wisdom and self-care."""
    
    def get_safety_plan(self) -> str:
        """Generate a safety planning guide."""
        return """🛡️ **Personal Safety Plan** 🛡️

**WHEN CRISIS FEELINGS START:**

**1. Warning Signs to Watch For:**
• Feeling hopeless or trapped
• Thinking about death or suicide
• Feeling like a burden to others
• Extreme mood swings
• Withdrawing from others

**2. Internal Coping Strategies:**
• Deep breathing exercises
• Progressive muscle relaxation
• Mindfulness or meditation
• Positive self-talk
• Grounding techniques (5-4-3-2-1)

**3. People and Places for Distraction:**
• Call a supportive friend or family member
• Go to a public place (coffee shop, library, park)
• Engage in a favorite hobby or activity
• Watch funny videos or uplifting content

**4. Professional Support Contacts:**
• National Suicide Prevention Lifeline: 988
• Crisis Text Line: Text HOME to 741741
• Your therapist/counselor: [Your Number]
• Your doctor: [Your Number]
• Local emergency room: [Your Local ER]

**5. Making Your Environment Safe:**
• Remove or secure any means of self-harm
• Ask someone to stay with you
• Avoid alcohol and drugs
• Take prescribed medications as directed

**Remember:** Having a plan helps you respond to crisis situations more effectively. Keep this information easily accessible."""
    
    def get_crisis_resources_by_location(self, country: str = 'us') -> str:
        """Get crisis resources based on location."""
        if country.lower() in self.crisis_resources:
            resources = self.crisis_resources[country.lower()]
        else:
            resources = self.crisis_resources['international']
        
        response = f"**Crisis Resources:**\n\n"
        
        for resource_type, resource_info in resources.items():
            response += f"**{resource_info['name']}**\n"
            if 'phone' in resource_info:
                response += f"📞 {resource_info['phone']}\n"
            if 'text' in resource_info:
                response += f"💬 {resource_info['text']}\n"
            if 'website' in resource_info:
                response += f"🌐 {resource_info['website']}\n"
            if 'description' in resource_info:
                response += f"ℹ️ {resource_info['description']}\n"
            response += "\n"
        
        return response
    
    def log_crisis_interaction(self, crisis_level: str, message_hash: str):
        """Log crisis interaction for monitoring (anonymized)."""
        try:
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'crisis_level': crisis_level,
                'message_hash': message_hash,  # Anonymous hash
                'action_taken': 'crisis_response_provided'
            }
            
            # In a real implementation, this would go to a secure logging system
            logger.warning(f"Crisis interaction logged: {json.dumps(log_entry)}")
            
        except Exception as e:
            logger.error(f"Error logging crisis interaction: {e}")
    
    def get_post_crisis_followup(self) -> str:
        """Provide post-crisis follow-up guidance."""
        return """💚 **After a Crisis - Taking Care of Yourself** 💚

**IMMEDIATE SELF-CARE:**
• Be gentle with yourself - you've been through something difficult
• Stay hydrated and try to eat something nourishing
• Get rest when you can, but don't isolate yourself completely
• Avoid alcohol and drugs, which can worsen mood

**FOLLOW-UP ACTIONS:**
• Schedule an appointment with a mental health professional
• Check in with the people who supported you during the crisis
• Consider joining a support group
• Keep taking any prescribed medications as directed

**BUILDING RESILIENCE:**
• Create a routine that includes self-care activities
• Practice stress-reduction techniques regularly
• Build and maintain your support network
• Learn to recognize your warning signs

**REMEMBER:**
• Recovery is not linear - there may be ups and downs
• Seeking help was a brave and important step
• You have survived difficult times before and can do so again
• Professional support is available whenever you need it

**If crisis feelings return, don't hesitate to reach out immediately.**"""
