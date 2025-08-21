import random
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import json

class WellnessRecommender:
    def __init__(self):
        """Initialize wellness recommender with various activities and strategies."""
        
        # Coping strategies by stress level
        self.coping_strategies = {
            'low': [
                "Practice gratitude by writing down three things you're thankful for today",
                "Take a 5-minute walk outside to get some fresh air",
                "Listen to your favorite song and really focus on the melody",
                "Do some gentle stretching or light movement",
                "Call a friend or family member you haven't spoken to in a while",
                "Practice the 5-4-3-2-1 grounding technique: name 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste"
            ],
            'moderate': [
                "Try a 10-minute guided meditation or mindfulness exercise",
                "Practice deep breathing: inhale for 4 counts, hold for 4, exhale for 6",
                "Write in a journal about your thoughts and feelings",
                "Take a warm bath or shower to help relax your muscles",
                "Engage in a creative activity like drawing, coloring, or crafting",
                "Progressive muscle relaxation: tense and release each muscle group",
                "Step away from stressful situations for 15-20 minutes"
            ],
            'high': [
                "Practice box breathing: breathe in for 4, hold for 4, out for 4, hold for 4",
                "Use the STOP technique: Stop, Take a breath, Observe your thoughts, Proceed mindfully",
                "Reach out to a trusted friend, family member, or mental health professional",
                "Try gentle yoga or stretching to release physical tension",
                "Listen to calming music or nature sounds",
                "Practice self-compassion: speak to yourself as you would a good friend",
                "Consider taking a mental health day if possible"
            ],
            'critical': [
                "Reach out to a mental health crisis line or emergency services if needed",
                "Contact a trusted friend, family member, or mental health professional immediately",
                "Practice grounding techniques to stay present and calm",
                "Remove yourself from immediate stressors if safe to do so",
                "Focus on your basic needs: hydration, food, rest",
                "Remember that this feeling is temporary and you can get through this"
            ]
        }
        
        # Activities by emotional state
        self.mood_activities = {
            'anxious': [
                "Try the 4-7-8 breathing technique: inhale for 4, hold for 7, exhale for 8",
                "Practice progressive muscle relaxation starting from your toes",
                "Use the 'worry time' technique: set aside 15 minutes to worry, then move on",
                "Try gentle movement like walking or stretching",
                "Listen to calming music or guided meditations",
                "Challenge anxious thoughts with evidence-based thinking"
            ],
            'depressed': [
                "Engage in a small, achievable activity that usually brings you joy",
                "Step outside for some natural light and fresh air",
                "Reach out to a friend or loved one for connection",
                "Practice gratitude by listing three small things you appreciate",
                "Do a brief physical activity, even just gentle movement",
                "Create something, no matter how small (draw, write, craft)"
            ],
            'overwhelmed': [
                "Break down your tasks into smaller, manageable steps",
                "Practice the 'one thing at a time' mindset",
                "Use the Eisenhower Matrix to prioritize tasks",
                "Take regular breaks (try the Pomodoro Technique)",
                "Say no to non-essential commitments",
                "Delegate tasks when possible"
            ],
            'angry': [
                "Try physical exercise to release built-up energy",
                "Practice deep breathing or counting to 10",
                "Write about your feelings in a journal (you can destroy it after)",
                "Listen to music that matches your energy, then transition to calmer songs",
                "Use the 'RAIN' technique: Recognize, Allow, Investigate, Nurture",
                "Talk to someone you trust about what's bothering you"
            ],
            'lonely': [
                "Reach out to a friend or family member, even with a simple text",
                "Join an online community or forum related to your interests",
                "Consider volunteering for a cause you care about",
                "Practice loving-kindness meditation",
                "Engage with others in your community (grocery store, coffee shop)",
                "Write a letter to someone you care about"
            ]
        }
        
        # Quick mood boosters
        self.mood_boosters = [
            "Watch a funny video or look at memes that make you laugh",
            "Listen to an upbeat song that you love",
            "Do 10 jumping jacks or push-ups to get your blood flowing",
            "Text someone you appreciate and tell them something nice",
            "Look at photos that bring back happy memories",
            "Eat a small piece of your favorite treat mindfully",
            "Pet an animal (yours or a neighbor's, with permission)",
            "Step outside and take five deep breaths of fresh air",
            "Do a quick dance to your favorite song",
            "Write down one thing you're proud of accomplishing today"
        ]
        
        # Long-term wellness habits
        self.wellness_habits = {
            'daily': [
                "Maintain a consistent sleep schedule (7-9 hours per night)",
                "Drink plenty of water throughout the day",
                "Eat nutritious meals at regular times",
                "Take breaks from screens every hour",
                "Practice gratitude - write down 3 things you're grateful for",
                "Do some form of physical movement, even if just stretching"
            ],
            'weekly': [
                "Spend time in nature or outdoors",
                "Connect with friends or family members",
                "Engage in a hobby or creative activity you enjoy",
                "Practice a longer meditation or mindfulness session",
                "Plan and prepare healthy meals for the week",
                "Declutter or organize one area of your living space"
            ],
            'monthly': [
                "Reflect on your mental health goals and progress",
                "Try a new stress-reduction technique or activity",
                "Schedule regular check-ins with a therapist or counselor",
                "Evaluate and adjust your work-life balance",
                "Plan something to look forward to",
                "Review and update your self-care toolkit"
            ]
        }
        
        # Professional help recommendations
        self.professional_resources = {
            'therapy_types': [
                "Cognitive Behavioral Therapy (CBT) - for changing thought patterns",
                "Dialectical Behavior Therapy (DBT) - for emotional regulation",
                "Acceptance and Commitment Therapy (ACT) - for psychological flexibility",
                "Mindfulness-Based Stress Reduction (MBSR) - for stress management",
                "Eye Movement Desensitization and Reprocessing (EMDR) - for trauma"
            ],
            'when_to_seek_help': [
                "When stress interferes with daily functioning",
                "When you're having thoughts of self-harm",
                "When coping strategies aren't working",
                "When symptoms persist for more than two weeks",
                "When relationships are significantly impacted",
                "When you're using substances to cope"
            ]
        }
        
        # Workplace wellness
        self.workplace_strategies = [
            "Take regular breaks, even if just for 2-3 minutes",
            "Practice desk exercises or stretches",
            "Set boundaries with email and communication",
            "Create a calming workspace environment",
            "Use time-blocking for better task management",
            "Practice saying no to additional commitments when overwhelmed",
            "Take your lunch break away from your workspace",
            "Connect with supportive colleagues"
        ]
    
    def get_recommendations(self, user_profile: Dict, analysis: Dict) -> str:
        """
        Get personalized recommendations based on user profile and current analysis.
        
        Args:
            user_profile (Dict): User's mental health profile
            analysis (Dict): Current message analysis
            
        Returns:
            str: Personalized recommendations
        """
        stress_level = user_profile.get('stress_level', 0)
        urgency = analysis.get('urgency_level', 'low')
        emotions = analysis.get('sentiment', {}).get('emotions', {})
        
        # Determine stress category
        if urgency == 'emergency' or stress_level > 8:
            stress_category = 'critical'
        elif urgency == 'high' or stress_level > 6:
            stress_category = 'high'
        elif urgency == 'medium' or stress_level > 3:
            stress_category = 'moderate'
        else:
            stress_category = 'low'
        
        # Get base recommendations
        base_recommendations = self.coping_strategies.get(stress_category, [])
        selected_recommendations = random.sample(base_recommendations, min(2, len(base_recommendations)))
        
        # Add emotion-specific recommendations
        if emotions:
            primary_emotion = max(emotions, key=emotions.get) if emotions else None
            if primary_emotion and primary_emotion in self.mood_activities:
                emotion_rec = random.choice(self.mood_activities[primary_emotion])
                selected_recommendations.append(emotion_rec)
        
        # Add workplace strategies if work stress detected
        stress_indicators = analysis.get('stress_indicators', [])
        if 'work_stress' in stress_indicators:
            workplace_rec = random.choice(self.workplace_strategies)
            selected_recommendations.append(workplace_rec)
        
        # Format recommendations
        if selected_recommendations:
            rec_text = "**Here are some personalized suggestions for you:**\n\n"
            for i, rec in enumerate(selected_recommendations, 1):
                rec_text += f"{i}. {rec}\n"
            
            # Add professional help suggestion for high stress
            if stress_category in ['high', 'critical']:
                rec_text += f"\n💡 **Consider professional support:** If you're consistently experiencing high stress, speaking with a mental health professional can provide personalized strategies and support."
            
            return rec_text
        
        return ""
    
    def daily_wellness_check(self) -> str:
        """Generate a daily wellness check-in message."""
        wellness_checks = [
            "**Daily Wellness Check** 🌟\n\nHow are you feeling today? Remember to:\n• Take deep breaths\n• Stay hydrated\n• Move your body\n• Practice gratitude",
            
            "**Mindful Moment** 🧘‍♀️\n\nTake a moment to check in with yourself:\n• What emotions am I feeling right now?\n• What does my body need?\n• What would be kind to myself today?",
            
            "**Stress Check** 📊\n\nOn a scale of 1-10, how stressed do you feel?\n• If 1-3: Great! Keep up your healthy habits\n• If 4-6: Try a quick stress-relief technique\n• If 7-10: Consider reaching out for support",
            
            "**Self-Care Reminder** 💚\n\nSelf-care isn't selfish. Today, try to:\n• Do something that brings you joy\n• Connect with someone you care about\n• Give yourself permission to rest"
        ]
        
        return random.choice(wellness_checks)
    
    def get_mood_booster(self) -> str:
        """Get a quick mood booster activity."""
        booster = random.choice(self.mood_boosters)
        return f"**Quick Mood Booster** ⚡\n\n{booster}\n\nTry this now and see how you feel afterward!"
    
    def get_breathing_exercise(self) -> str:
        """Get a breathing exercise recommendation."""
        exercises = [
            "**4-7-8 Breathing** 🫁\n\n1. Exhale completely\n2. Inhale through nose for 4 counts\n3. Hold breath for 7 counts\n4. Exhale through mouth for 8 counts\n5. Repeat 3-4 times",
            
            "**Box Breathing** 📦\n\n1. Breathe in for 4 counts\n2. Hold for 4 counts\n3. Breathe out for 4 counts\n4. Hold for 4 counts\n5. Repeat for 5-10 cycles",
            
            "**Deep Belly Breathing** 🤲\n\n1. Place one hand on chest, one on belly\n2. Breathe slowly through nose\n3. Feel your belly rise more than chest\n4. Exhale slowly through mouth\n5. Continue for 5-10 breaths"
        ]
        
        return random.choice(exercises)
    
    def get_grounding_technique(self) -> str:
        """Get a grounding technique for anxiety or overwhelm."""
        techniques = [
            "**5-4-3-2-1 Grounding** 🌍\n\nName:\n• 5 things you can see\n• 4 things you can touch\n• 3 things you can hear\n• 2 things you can smell\n• 1 thing you can taste",
            
            "**Body Scan Grounding** 👤\n\n1. Start at your toes\n2. Notice sensations in each body part\n3. Move slowly up to your head\n4. Don't judge, just observe\n5. This brings you into the present moment",
            
            "**Category Grounding** 📝\n\nQuickly name:\n• 5 animals\n• 5 colors\n• 5 foods\n• 5 countries\n\nThis engages your thinking mind and reduces anxiety"
        ]
        
        return random.choice(techniques)
    
    def get_self_compassion_exercise(self) -> str:
        """Get a self-compassion exercise."""
        exercises = [
            "**Self-Compassion Break** 💝\n\n1. Acknowledge: 'This is a moment of suffering'\n2. Remember: 'Suffering is part of life'\n3. Offer yourself kindness: 'May I be kind to myself'\n4. Place hands on heart if it feels right",
            
            "**Best Friend Technique** 👫\n\nAsk yourself:\n• What would I say to my best friend in this situation?\n• How would I treat them with kindness?\n• Can I offer myself the same compassion?",
            
            "**Loving Kindness for Self** 🤗\n\nRepeat these phrases:\n• May I be happy\n• May I be healthy\n• May I be at peace\n• May I live with ease"
        ]
        
        return random.choice(exercises)
    
    def get_professional_help_guidance(self, stress_level: str) -> str:
        """Provide guidance on seeking professional help."""
        if stress_level in ['critical', 'high']:
            return """
**When to Seek Professional Help** 🏥

Consider reaching out to a mental health professional if:
• You're having thoughts of self-harm
• Stress is interfering with daily life
• You're using substances to cope
• Symptoms persist for more than 2 weeks
• Friends/family have expressed concern

**Types of Support:**
• Crisis hotlines for immediate help
• Therapists for ongoing support
• Support groups for peer connection
• Your primary care doctor for referrals

**Remember:** Seeking help is a sign of strength, not weakness.
"""
        else:
            return """
**Building Your Support Network** 🤝

Mental health is just as important as physical health:
• Regular check-ins with trusted friends/family
• Consider therapy for personal growth
• Join support groups or communities
• Maintain relationship with healthcare providers

**Prevention is key:** Building support before you need it makes it easier to reach out when you do.
"""
    
    def get_sleep_hygiene_tips(self) -> str:
        """Get sleep hygiene recommendations."""
        return """
**Sleep Hygiene Tips** 😴

**Before Bed:**
• Create a consistent bedtime routine
• Avoid screens 1 hour before sleep
• Keep bedroom cool, dark, and quiet
• Try relaxation techniques

**During the Day:**
• Get natural sunlight exposure
• Limit caffeine after 2 PM
• Exercise regularly (but not close to bedtime)
• Manage stress throughout the day

**If You Can't Sleep:**
• Don't watch the clock
• Get up after 20 minutes of not sleeping
• Do a quiet, boring activity until sleepy
• Return to bed when you feel drowsy
"""
    
    def get_nutrition_for_mood_tips(self) -> str:
        """Get nutrition tips for mental health."""
        return """
**Nutrition for Mental Wellness** 🥗

**Foods that Support Mood:**
• Omega-3 rich fish (salmon, sardines)
• Leafy greens and colorful vegetables
• Whole grains for steady energy
• Nuts and seeds for healthy fats
• Fermented foods for gut health

**Habits to Support Mental Health:**
• Eat regular, balanced meals
• Stay hydrated throughout the day
• Limit processed foods and sugar
• Don't skip breakfast
• Consider a vitamin D supplement (consult your doctor)

**Remember:** Food affects mood, but it's just one piece of the mental health puzzle.
"""
