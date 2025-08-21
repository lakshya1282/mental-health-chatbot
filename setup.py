#!/usr/bin/env python3
"""
MindCare AI Mental Health Chatbot Setup Script
Automates installation and initial configuration
"""

import os
import sys
import subprocess
import platform
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class MindCareSetup:
    def __init__(self):
        self.python_version = sys.version_info
        self.platform = platform.system()
        self.project_dir = Path(__file__).parent
        self.requirements_file = self.project_dir / 'requirements.txt'
        
    def check_python_version(self):
        """Check if Python version is compatible."""
        logger.info(f"Checking Python version: {self.python_version.major}.{self.python_version.minor}")
        
        if self.python_version.major < 3 or (self.python_version.major == 3 and self.python_version.minor < 8):
            logger.error("Python 3.8 or higher is required.")
            logger.error(f"Current version: {self.python_version.major}.{self.python_version.minor}")
            return False
        
        logger.info("✅ Python version is compatible")
        return True
    
    def install_requirements(self):
        """Install Python dependencies."""
        logger.info("Installing Python dependencies...")
        
        try:
            # Upgrade pip first
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
            
            # Install requirements
            if self.requirements_file.exists():
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', str(self.requirements_file)])
                logger.info("✅ Python dependencies installed successfully")
            else:
                logger.error(f"Requirements file not found: {self.requirements_file}")
                return False
                
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
            
        return True
    
    def download_nltk_data(self):
        """Download required NLTK data."""
        logger.info("Downloading NLTK data...")
        
        try:
            import nltk
            
            # Download required NLTK datasets
            datasets = ['vader_lexicon', 'punkt', 'stopwords']
            
            for dataset in datasets:
                logger.info(f"Downloading {dataset}...")
                nltk.download(dataset, quiet=True)
            
            logger.info("✅ NLTK data downloaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to download NLTK data: {e}")
            return False
    
    def test_imports(self):
        """Test if all required modules can be imported."""
        logger.info("Testing module imports...")
        
        required_modules = [
            'streamlit',
            'pandas',
            'numpy',
            'nltk',
            'textblob',
            'plotly',
            'sklearn',
            'cryptography'
        ]
        
        failed_imports = []
        
        for module in required_modules:
            try:
                __import__(module)
                logger.info(f"✅ {module}")
            except ImportError as e:
                logger.error(f"❌ {module}: {e}")
                failed_imports.append(module)
        
        if failed_imports:
            logger.error(f"Failed to import: {', '.join(failed_imports)}")
            return False
        
        logger.info("✅ All modules imported successfully")
        return True
    
    def create_directories(self):
        """Create necessary directories."""
        logger.info("Creating directories...")
        
        directories = [
            'logs',
            'data',
            'backups'
        ]
        
        for dir_name in directories:
            dir_path = self.project_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            logger.info(f"✅ Created directory: {dir_path}")
        
        return True
    
    def initialize_database(self):
        """Initialize the SQLite database."""
        logger.info("Initializing database...")
        
        try:
            from data_handler import DataHandler
            
            # Initialize data handler (this creates the database)
            data_handler = DataHandler()
            logger.info("✅ Database initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            return False
    
    def run_health_check(self):
        """Run a health check of the application."""
        logger.info("Running health check...")
        
        try:
            # Import and initialize main components
            from sentiment_analyzer import SentimentAnalyzer
            from stress_detector import StressDetector
            from wellness_recommender import WellnessRecommender
            
            # Test sentiment analyzer
            analyzer = SentimentAnalyzer()
            test_result = analyzer.analyze("I am feeling happy today")
            if 'compound' in test_result:
                logger.info("✅ Sentiment analyzer working")
            else:
                logger.error("❌ Sentiment analyzer failed")
                return False
            
            # Test stress detector
            detector = StressDetector()
            stress_signals = detector.detect_stress_signals("I am feeling overwhelmed with work")
            if isinstance(stress_signals, list):
                logger.info("✅ Stress detector working")
            else:
                logger.error("❌ Stress detector failed")
                return False
            
            # Test wellness recommender
            recommender = WellnessRecommender()
            daily_check = recommender.daily_wellness_check()
            if daily_check and isinstance(daily_check, str):
                logger.info("✅ Wellness recommender working")
            else:
                logger.error("❌ Wellness recommender failed")
                return False
            
            logger.info("✅ Health check passed")
            return True
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    def display_completion_message(self):
        """Display setup completion message."""
        print("\n" + "="*60)
        print("🎉 MindCare AI Setup Complete! 🎉")
        print("="*60)
        print("\n📋 Next Steps:")
        print("1. Run the application: streamlit run app.py")
        print("2. Open your browser to: http://localhost:8501")
        print("3. Start chatting with MindCare AI!")
        print("\n🔗 Useful Commands:")
        print("• Start app: streamlit run app.py")
        print("• View logs: tail -f logs/chatbot.log")
        print("• Run tests: python -m pytest tests/")
        print("\n📚 Documentation:")
        print("• README.md - Full documentation")
        print("• Privacy Notice - See privacy_manager.py")
        print("• Crisis Resources - See emergency_handler.py")
        print("\n⚠️  Important Reminders:")
        print("• This chatbot is NOT a replacement for professional care")
        print("• In emergencies, call 911 or your local emergency services")
        print("• Crisis Text Line: Text HOME to 741741")
        print("• National Suicide Prevention Lifeline: 988")
        print("\n" + "="*60)
    
    def run_setup(self):
        """Run the complete setup process."""
        print("🧠 MindCare AI Mental Health Chatbot Setup")
        print("=" * 50)
        
        steps = [
            ("Checking Python version", self.check_python_version),
            ("Installing dependencies", self.install_requirements),
            ("Downloading NLTK data", self.download_nltk_data),
            ("Testing imports", self.test_imports),
            ("Creating directories", self.create_directories),
            ("Initializing database", self.initialize_database),
            ("Running health check", self.run_health_check)
        ]
        
        for step_name, step_function in steps:
            logger.info(f"Step: {step_name}")
            if not step_function():
                logger.error(f"Setup failed at step: {step_name}")
                return False
            print()  # Add spacing between steps
        
        self.display_completion_message()
        return True

def main():
    """Main setup function."""
    setup = MindCareSetup()
    
    try:
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Setup failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
