import sqlite3
import json
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
from cryptography.fernet import Fernet
import pandas as pd

logger = logging.getLogger(__name__)

class DataHandler:
    def __init__(self, db_path: str = "mental_health_data.db"):
        """Initialize data handler with privacy-focused approach."""
        self.db_path = db_path
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # Initialize database
        self._init_database()
        
        # Privacy settings
        self.data_retention_days = 30  # Delete data older than 30 days
        self.anonymize_after_days = 7   # Anonymize data after 7 days
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for data protection."""
        key_file = "data_encryption.key"
        
        if os.path.exists(key_file):
            with open(key_file, 'rb') as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
            return key
    
    def _init_database(self):
        """Initialize SQLite database with proper schema."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Conversation data table (anonymized)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_hash TEXT NOT NULL,
                        timestamp DATETIME NOT NULL,
                        sentiment_score REAL,
                        stress_level REAL,
                        urgency_level TEXT,
                        emotions TEXT,  -- JSON encoded
                        risk_indicators TEXT,  -- JSON encoded
                        encrypted_content BLOB,  -- Encrypted message content (optional)
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # User analytics table (aggregated, anonymous)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS analytics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE NOT NULL,
                        total_conversations INTEGER DEFAULT 0,
                        avg_sentiment REAL DEFAULT 0,
                        avg_stress_level REAL DEFAULT 0,
                        high_risk_count INTEGER DEFAULT 0,
                        emergency_count INTEGER DEFAULT 0,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                # Wellness activities tracking (anonymous)
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS wellness_activities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_hash TEXT NOT NULL,
                        activity_type TEXT NOT NULL,
                        timestamp DATETIME NOT NULL,
                        effectiveness_rating INTEGER,  -- 1-10 scale
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
    
    def _generate_session_hash(self, identifier: str = None) -> str:
        """Generate anonymous session hash."""
        if identifier:
            # Use provided identifier (could be user ID, session ID, etc.)
            base_string = identifier
        else:
            # Generate random hash for truly anonymous sessions
            import uuid
            base_string = str(uuid.uuid4())
        
        # Add date to ensure hashes change daily for privacy
        date_string = datetime.now().strftime("%Y-%m-%d")
        combined = f"{base_string}_{date_string}"
        
        return hashlib.sha256(combined.encode()).hexdigest()[:16]
    
    def store_conversation_data(self, data: Dict, session_id: str = None) -> bool:
        """
        Store conversation data in privacy-compliant manner.
        
        Args:
            data (Dict): Conversation analysis data
            session_id (str, optional): Session identifier for continuity
            
        Returns:
            bool: Success status
        """
        try:
            session_hash = self._generate_session_hash(session_id)
            
            # Extract and sanitize data
            sentiment_data = data.get('sentiment', {})
            emotions = sentiment_data.get('emotions', {})
            risk_indicators = data.get('risk_indicators', [])
            
            # Encrypt sensitive content if provided
            encrypted_content = None
            if 'message_content' in data:
                content_bytes = data['message_content'].encode('utf-8')
                encrypted_content = self.cipher_suite.encrypt(content_bytes)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO conversations (
                        session_hash, timestamp, sentiment_score, stress_level,
                        urgency_level, emotions, risk_indicators, encrypted_content
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_hash,
                    data.get('timestamp', datetime.now()),
                    sentiment_data.get('compound', 0),
                    data.get('stress_level', 0),
                    data.get('urgency', 'low'),
                    json.dumps(emotions),
                    json.dumps(risk_indicators),
                    encrypted_content
                ))
                
                conn.commit()
                logger.info(f"Conversation data stored successfully for session {session_hash[:8]}...")
                return True
                
        except Exception as e:
            logger.error(f"Error storing conversation data: {e}")
            return False
    
    def store_wellness_activity(self, session_id: str, activity_type: str, 
                              effectiveness_rating: int = None) -> bool:
        """Store wellness activity data."""
        try:
            session_hash = self._generate_session_hash(session_id)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO wellness_activities (
                        session_hash, activity_type, timestamp, effectiveness_rating
                    ) VALUES (?, ?, ?, ?)
                ''', (
                    session_hash,
                    activity_type,
                    datetime.now(),
                    effectiveness_rating
                ))
                
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error storing wellness activity: {e}")
            return False
    
    def get_user_trends(self, session_id: str, days: int = 30) -> Dict:
        """
        Get user trends while maintaining privacy.
        
        Args:
            session_id (str): Session identifier
            days (int): Number of days to analyze
            
        Returns:
            Dict: Trend analysis
        """
        try:
            session_hash = self._generate_session_hash(session_id)
            start_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query('''
                    SELECT 
                        DATE(timestamp) as date,
                        sentiment_score,
                        stress_level,
                        urgency_level,
                        emotions
                    FROM conversations 
                    WHERE session_hash = ? AND timestamp >= ?
                    ORDER BY timestamp
                ''', conn, params=(session_hash, start_date))
            
            if df.empty:
                return {'error': 'No data available for analysis'}
            
            # Calculate trends
            sentiment_trend = df['sentiment_score'].rolling(window=3).mean().iloc[-1]
            stress_trend = df['stress_level'].rolling(window=3).mean().iloc[-1]
            
            # Count urgency levels
            urgency_counts = df['urgency_level'].value_counts().to_dict()
            
            return {
                'data_points': len(df),
                'date_range': f"{df['date'].min()} to {df['date'].max()}",
                'avg_sentiment': df['sentiment_score'].mean(),
                'avg_stress': df['stress_level'].mean(),
                'sentiment_trend': sentiment_trend,
                'stress_trend': stress_trend,
                'urgency_distribution': urgency_counts,
                'improvement_indicators': self._analyze_improvement(df)
            }
            
        except Exception as e:
            logger.error(f"Error getting user trends: {e}")
            return {'error': str(e)}
    
    def _analyze_improvement(self, df: pd.DataFrame) -> Dict:
        """Analyze improvement indicators in user data."""
        if len(df) < 5:
            return {'status': 'insufficient_data'}
        
        # Split data into first half and second half
        mid_point = len(df) // 2
        first_half = df.iloc[:mid_point]
        second_half = df.iloc[mid_point:]
        
        sentiment_improvement = (
            second_half['sentiment_score'].mean() > first_half['sentiment_score'].mean()
        )
        
        stress_improvement = (
            second_half['stress_level'].mean() < first_half['stress_level'].mean()
        )
        
        return {
            'sentiment_improving': sentiment_improvement,
            'stress_reducing': stress_improvement,
            'overall_trend': 'positive' if (sentiment_improvement or stress_improvement) else 'stable'
        }
    
    def get_aggregated_analytics(self, days: int = 30) -> Dict:
        """Get aggregated, anonymous analytics."""
        try:
            start_date = datetime.now() - timedelta(days=days)
            
            with sqlite3.connect(self.db_path) as conn:
                df = pd.read_sql_query('''
                    SELECT 
                        DATE(timestamp) as date,
                        sentiment_score,
                        stress_level,
                        urgency_level
                    FROM conversations 
                    WHERE timestamp >= ?
                ''', conn, params=(start_date,))
            
            if df.empty:
                return {'message': 'No data available'}
            
            # Aggregate statistics
            daily_stats = df.groupby('date').agg({
                'sentiment_score': ['mean', 'count'],
                'stress_level': 'mean',
                'urgency_level': lambda x: (x == 'high').sum()
            }).round(3)
            
            return {
                'total_conversations': len(df),
                'date_range': f"{df['date'].min()} to {df['date'].max()}",
                'average_sentiment': df['sentiment_score'].mean(),
                'average_stress': df['stress_level'].mean(),
                'high_urgency_rate': (df['urgency_level'] == 'high').mean(),
                'daily_trends': daily_stats.to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error getting analytics: {e}")
            return {'error': str(e)}
    
    def cleanup_old_data(self) -> Dict:
        """Clean up old data according to privacy policy."""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.data_retention_days)
            anonymize_date = datetime.now() - timedelta(days=self.anonymize_after_days)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete very old data
                cursor.execute('''
                    DELETE FROM conversations WHERE timestamp < ?
                ''', (cutoff_date,))
                deleted_rows = cursor.rowcount
                
                # Anonymize older data (remove encrypted content)
                cursor.execute('''
                    UPDATE conversations 
                    SET encrypted_content = NULL 
                    WHERE timestamp < ? AND encrypted_content IS NOT NULL
                ''', (anonymize_date,))
                anonymized_rows = cursor.rowcount
                
                conn.commit()
                
                logger.info(f"Cleanup completed: {deleted_rows} deleted, {anonymized_rows} anonymized")
                
                return {
                    'deleted_conversations': deleted_rows,
                    'anonymized_conversations': anonymized_rows,
                    'status': 'success'
                }
                
        except Exception as e:
            logger.error(f"Error during data cleanup: {e}")
            return {'error': str(e)}
    
    def export_user_data(self, session_id: str) -> Dict:
        """Export user's data for transparency/portability."""
        try:
            session_hash = self._generate_session_hash(session_id)
            
            with sqlite3.connect(self.db_path) as conn:
                # Get conversation data
                conversations_df = pd.read_sql_query('''
                    SELECT timestamp, sentiment_score, stress_level, urgency_level, emotions
                    FROM conversations 
                    WHERE session_hash = ?
                    ORDER BY timestamp
                ''', conn, params=(session_hash,))
                
                # Get wellness activities
                activities_df = pd.read_sql_query('''
                    SELECT timestamp, activity_type, effectiveness_rating
                    FROM wellness_activities 
                    WHERE session_hash = ?
                    ORDER BY timestamp
                ''', conn, params=(session_hash,))
            
            return {
                'export_date': datetime.now().isoformat(),
                'session_id': session_hash[:8] + "***",  # Partial hash for privacy
                'conversations': conversations_df.to_dict('records'),
                'wellness_activities': activities_df.to_dict('records'),
                'summary': {
                    'total_conversations': len(conversations_df),
                    'total_activities': len(activities_df),
                    'date_range': f"{conversations_df['timestamp'].min()} to {conversations_df['timestamp'].max()}" if not conversations_df.empty else "No data"
                }
            }
            
        except Exception as e:
            logger.error(f"Error exporting user data: {e}")
            return {'error': str(e)}
    
    def delete_user_data(self, session_id: str) -> bool:
        """Delete all user data (right to be forgotten)."""
        try:
            session_hash = self._generate_session_hash(session_id)
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete from all tables
                cursor.execute('DELETE FROM conversations WHERE session_hash = ?', (session_hash,))
                conversations_deleted = cursor.rowcount
                
                cursor.execute('DELETE FROM wellness_activities WHERE session_hash = ?', (session_hash,))
                activities_deleted = cursor.rowcount
                
                conn.commit()
                
                logger.info(f"User data deleted: {conversations_deleted} conversations, {activities_deleted} activities")
                return True
                
        except Exception as e:
            logger.error(f"Error deleting user data: {e}")
            return False
    
    def get_privacy_report(self) -> Dict:
        """Generate privacy compliance report."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count total records
                cursor.execute('SELECT COUNT(*) FROM conversations')
                total_conversations = cursor.fetchone()[0]
                
                # Count encrypted records
                cursor.execute('SELECT COUNT(*) FROM conversations WHERE encrypted_content IS NOT NULL')
                encrypted_records = cursor.fetchone()[0]
                
                # Count old records that should be cleaned
                old_cutoff = datetime.now() - timedelta(days=self.data_retention_days)
                cursor.execute('SELECT COUNT(*) FROM conversations WHERE timestamp < ?', (old_cutoff,))
                old_records = cursor.fetchone()[0]
                
                return {
                    'total_conversations': total_conversations,
                    'encrypted_records': encrypted_records,
                    'encryption_rate': f"{(encrypted_records/total_conversations)*100:.1f}%" if total_conversations > 0 else "N/A",
                    'old_records_needing_cleanup': old_records,
                    'data_retention_days': self.data_retention_days,
                    'anonymization_days': self.anonymize_after_days,
                    'privacy_compliant': old_records == 0
                }
                
        except Exception as e:
            logger.error(f"Error generating privacy report: {e}")
            return {'error': str(e)}
