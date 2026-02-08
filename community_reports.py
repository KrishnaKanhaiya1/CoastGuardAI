"""
Community Knowledge Management System
Enables fishermen and communities to report observations and have them validated
integrated into risk assessment via Traditional Knowledge Modifier
"""

import json
import sqlite3
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import hashlib

# ==================== DATABASE SCHEMA ====================
def initialize_community_db(db_path='Data/community_observations.db'):
    """Initialize SQLite database for community observations"""
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Observations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS observations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                observer_id TEXT,
                observer_name TEXT,
                location_lat REAL,
                location_lon REAL,
                observation_type TEXT,
                description TEXT,
                confidence_level REAL,
                timestamp DATETIME,
                severity TEXT,
                validated INTEGER DEFAULT 0,
                validator_id TEXT,
                validation_timestamp DATETIME,
                reliability_score REAL DEFAULT 0.0
            )
        ''')
        
        # Observers (Community members) table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS observers (
                observer_id TEXT PRIMARY KEY,
                name TEXT,
                role TEXT,
                location_lat REAL,
                location_lon REAL,
                total_observations INTEGER DEFAULT 0,
                accuracy_score REAL DEFAULT 0.5,
                registration_date DATETIME,
                is_verified INTEGER DEFAULT 0
            )
        ''')
        
        # Observation validation history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS validation_history (
                validation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                observation_id INTEGER,
                validator_id TEXT,
                validation_date DATETIME,
                validation_result TEXT,
                reliability_adjustment REAL,
                notes TEXT,
                FOREIGN KEY(observation_id) REFERENCES observations(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error initializing database: {e}")
        return False

# ==================== OBSERVATION TYPES & INDICATORS ====================
OBSERVATION_TYPES = {
    'anomalous_waves': {
        'description': 'Unusual wave patterns or heights',
        'indicators': ['unusually high waves', 'rapid wave changes', 'strange wave direction'],
        'high_risk_phrases': ['giant waves', 'wall of water', 'never seen before']
    },
    'wind_pattern_shift': {
        'description': 'Sudden or abnormal wind direction/speed changes',
        'indicators': ['wind direction change', 'sudden gust', 'persistent wind'],
        'high_risk_phrases': ['violent wind', 'whirlwind', 'hurricane-force']
    },
    'tidal_anomaly': {
        'description': 'Unusual tidal behavior or timing deviations',
        'indicators': ['early/late tide', 'higher than usual', 'tide didnt recede'],
        'high_risk_phrases': ['catastrophic surge', 'no low tide', 'water level rising']
    },
    'wildlife_behavior': {
        'description': 'Unusual bird, fish, or animal behavior',
        'indicators': ['birds fleeing', 'fish moving inland', 'marine animals missing'],
        'high_risk_phrases': ['mass migration', 'unusual behavior', 'animals avoided area']
    },
    'coastal_erosion': {
        'description': 'Rapid erosion or land loss',
        'indicators': ['sand loss', 'beach erosion', 'land subsiding'],
        'high_risk_phrases': ['dramatic erosion', 'houses falling', 'total washout']
    },
    'mangrove_stress': {
        'description': 'Health issues or changes in mangrove ecosystem',
        'indicators': ['tree loss', 'disease', 'salt intrusion', 'reduced density'],
        'high_risk_phrases': ['mangrove dying', 'large-scale loss', 'complete loss']
    }
}

SEVERITY_LEVELS = {
    'LOW': 0.2,
    'MODERATE': 0.5,
    'HIGH': 0.75,
    'CRITICAL': 0.95
}

# ==================== COMMUNITY OBSERVATION VALIDATOR ====================
class CommunityObservationValidator:
    """Validates and scores community observations"""
    
    def __init__(self, db_path='Data/community_observations.db'):
        self.db_path = db_path
        initialize_community_db(db_path)
    
    def register_observer(self, observer_id: str, name: str, role: str, lat: float, lon: float):
        """
        Register a new community observer
        
        Args:
            observer_id: Unique identifier
            name: Observer's name
            role: 'fisherman', 'farmer', 'collector', 'elder', etc.
            lat, lon: Location coordinates
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR IGNORE INTO observers 
                (observer_id, name, role, location_lat, location_lon, registration_date, accuracy_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (observer_id, name, role, lat, lon, datetime.now().isoformat(), 0.5))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Error registering observer: {e}")
            return False
    
    def submit_observation(self, observer_id: str, obs_type: str, description: str,
                          location: Tuple[float, float], severity: str = 'MODERATE',
                          confidence: float = 0.7) -> int:
        """
        Submit a community observation
        
        Args:
            observer_id: Observer's ID
            obs_type: Observation type key
            description: Detailed description
            location: (lat, lon) tuple
            severity: 'LOW', 'MODERATE', 'HIGH', 'CRITICAL'
            confidence: Observer's confidence (0-1)
        
        Returns:
            observation_id if successful, -1 if failed
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get observer name
            cursor.execute('SELECT name FROM observers WHERE observer_id = ?', (observer_id,))
            result = cursor.fetchone()
            observer_name = result[0] if result else 'Anonymous'
            
            cursor.execute('''
                INSERT INTO observations
                (observer_id, observer_name, location_lat, location_lon, observation_type,
                 description, confidence_level, timestamp, severity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (observer_id, observer_name, location[0], location[1], obs_type,
                  description, confidence, datetime.now().isoformat(), severity))
            
            observation_id = cursor.lastrowid
            
            # Update observer's total observations
            cursor.execute(
                'UPDATE observers SET total_observations = total_observations + 1 WHERE observer_id = ?',
                (observer_id,)
            )
            
            conn.commit()
            conn.close()
            
            return observation_id
        
        except Exception as e:
            print(f"Error submitting observation: {e}")
            return -1
    
    def validate_observation(self, observation_id: int, validator_id: str, is_valid: bool,
                            reliability_adjustment: float = 0.0, notes: str = '') -> bool:
        """
        Validate a submitted observation
        
        Args:
            observation_id: ID of observation to validate
            validator_id: Validator's ID (Elder, expert, or admin)
            is_valid: Whether observation is valid
            reliability_adjustment: Score adjustment (-1 to +1)
            notes: Validation notes
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Update observation
            cursor.execute('''
                UPDATE observations
                SET validated = ?, validator_id = ?, validation_timestamp = ?
                WHERE id = ?
            ''', (1 if is_valid else 0, validator_id, datetime.now().isoformat(), observation_id))
            
            # Record validation history
            cursor.execute('''
                INSERT INTO validation_history
                (observation_id, validator_id, validation_date, validation_result, 
                 reliability_adjustment, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (observation_id, validator_id, datetime.now().isoformat(),
                  'VALID' if is_valid else 'INVALID', reliability_adjustment, notes))
            
            conn.commit()
            conn.close()
            return True
        
        except Exception as e:
            print(f"Error validating observation: {e}")
            return False
    
    def calculate_observation_reliability(self, observation_id: int) -> float:
        """
        Calculate reliability score for an observation
        
        Factors:
        - Observer's historical accuracy
        - Severity/confidence level
        - Validation status
        - Corroboration with other observations
        
        Returns:
            Float (0-1): Reliability score
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get observation details
            cursor.execute('''
                SELECT o.observer_id, o.confidence_level, o.severity, o.validated, c.accuracy_score
                FROM observations o
                JOIN observers c ON o.observer_id = c.observer_id
                WHERE o.id = ?
            ''', (observation_id,))
            
            result = cursor.fetchone()
            if not result:
                return 0.0
            
            observer_id, confidence, severity, validated, observer_accuracy = result
            
            # Base score from observer's accuracy
            base_score = observer_accuracy
            
            # Adjustment for observation confidence
            base_score *= confidence
            
            # Adjustment for severity
            severity_weight = SEVERITY_LEVELS.get(severity, 0.5)
            base_score = base_score * 0.7 + severity_weight * 0.3
            
            # Validation boost
            if validated:
                base_score = min(base_score + 0.15, 1.0)  # Cap at 1.0
            
            # Check for corroborating observations
            cursor.execute('''
                SELECT COUNT(*) FROM observations
                WHERE location_lat BETWEEN ? AND ?
                AND location_lon BETWEEN ? AND ?
                AND observation_type = (SELECT observation_type FROM observations WHERE id = ?)
                AND id != ?
                AND validated = 1
            ''', (
                # 10km search radius (~0.09 degrees)
                cursor.execute('SELECT location_lat FROM observations WHERE id = ?', (observation_id,)).fetchone()[0] - 0.09,
                cursor.execute('SELECT location_lat FROM observations WHERE id = ?', (observation_id,)).fetchone()[0] + 0.09,
                cursor.execute('SELECT location_lon FROM observations WHERE id = ?', (observation_id,)).fetchone()[0] - 0.09,
                cursor.execute('SELECT location_lon FROM observations WHERE id = ?', (observation_id,)).fetchone()[0] + 0.09,
                observation_id, observation_id
            ))
            
            corroboration_count = cursor.fetchone()[0]
            if corroboration_count > 0:
                base_score = min(base_score + (corroboration_count * 0.05), 1.0)
            
            # Update reliability score
            cursor.execute(
                'UPDATE observations SET reliability_score = ? WHERE id = ?',
                (base_score, observation_id)
            )
            
            conn.commit()
            conn.close()
            
            return round(base_score, 3)
        
        except Exception as e:
            print(f"Error calculating reliability: {e}")
            return 0.0
    
    def get_recent_observations(self, days=7, obs_type=None, min_reliability=0.3):
        """
        Get recent validated observations
        
        Args:
            days: Look back period
            obs_type: Filter by observation type (None = all)
            min_reliability: Minimum reliability score
        
        Returns:
            DataFrame with recent observations
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = '''
                SELECT * FROM observations
                WHERE timestamp > datetime('now', ? || 'days')
                AND validated = 1
                AND reliability_score >= ?
            '''
            params = [f'-{days}', min_reliability]
            
            if obs_type:
                query += ' AND observation_type = ?'
                params.append(obs_type)
            
            query += ' ORDER BY timestamp DESC'
            
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()
            
            return df
        
        except Exception as e:
            print(f"Error retrieving observations: {e}")
            return pd.DataFrame()

# ==================== TRADITIONAL KNOWLEDGE INTEGRATION ====================
class TraditionalKnowledgeModifier:
    """
    Integrates validated community observations into risk assessment.
    Produces Indigenous Observations Score for hybrid risk calculation.
    """
    
    def __init__(self, validator: CommunityObservationValidator):
        self.validator = validator
    
    def calculate_indigenous_score_from_observations(self, location: Tuple[float, float],
                                                    hours_back=24) -> Dict:
        """
        Calculate Indigenous Observations Score from recent validated observations
        
        Args:
            location: (lat, lon) tuple
            hours_back: Look back window in hours
        
        Returns:
            Dictionary with component scores and total indigenous score
        """
        # Get observations within 50km radius
        search_radius = 0.45  # ~50km in degrees
        
        try:
            conn = sqlite3.connect(self.validator.db_path)
            
            query = '''
                SELECT observation_type, severity, reliability_score, description
                FROM observations
                WHERE location_lat BETWEEN ? AND ?
                AND location_lon BETWEEN ? AND ?
                AND validated = 1
                AND timestamp > datetime('now', '-' || ? || ' hours')
                ORDER BY reliability_score DESC
            '''
            
            params = [
                location[0] - search_radius, location[0] + search_radius,
                location[1] - search_radius, location[1] + search_radius,
                hours_back
            ]
            
            df = pd.read_sql_query(query, conn, params=params)
            conn.close()
            
            if df.empty:
                return {
                    'wave_anomaly_score': 0.0,
                    'wind_anomaly_score': 0.0,
                    'tidal_anomaly_score': 0.0,
                    'ecosystem_stress_score': 0.0,
                    'total_indigenous_score': 0.0,
                    'confidence': 0.0,
                    'num_observations': 0
                }
            
            # Aggregate by observation type
            scores = {
                'anomalous_waves': 0.0,
                'wind_pattern_shift': 0.0,
                'tidal_anomaly': 0.0,
                'wildlife_behavior': 0.0,
                'coastal_erosion': 0.0,
                'mangrove_stress': 0.0
            }
            
            for _, row in df.iterrows():
                obs_type = row['observation_type']
                severity_weight = SEVERITY_LEVELS.get(row['severity'], 0.5)
                reliability = row['reliability_score']
                
                contribution = severity_weight * reliability
                scores[obs_type] += contribution
            
            # Map observation types to risk components
            wave_score = min(scores['anomalous_waves'] / 3, 0.4)  # Cap at 0.4
            wind_score = min(scores['wind_pattern_shift'] / 3, 0.3)
            tidal_score = min(scores['tidal_anomaly'] / 3, 0.25)
            ecosystem_score = min((scores['wildlife_behavior'] + scores['coastal_erosion'] + scores['mangrove_stress']) / 9, 0.2)
            
            # Total indigenous score
            total_score = wave_score + wind_score + tidal_score + ecosystem_score
            total_score = min(total_score, 1.0)  # Cap at 1.0
            
            # Confidence based on number of observations
            confidence = min(len(df) / 5, 1.0)
            
            return {
                'wave_anomaly_score': round(wave_score, 3),
                'wind_anomaly_score': round(wind_score, 3),
                'tidal_anomaly_score': round(tidal_score, 3),
                'ecosystem_stress_score': round(ecosystem_score, 3),
                'total_indigenous_score': round(total_score, 3),
                'confidence': round(confidence, 3),
                'num_observations': len(df),
                'observations_summary': df.to_dict('records')
            }
        
        except Exception as e:
            print(f"Error calculating indigenous score: {e}")
            return {
                'total_indigenous_score': 0.0,
                'confidence': 0.0,
                'num_observations': 0
            }

# Global instances
validator = CommunityObservationValidator()
tk_modifier = TraditionalKnowledgeModifier(validator)

def submit_community_report(observer_id: str, obs_type: str, description: str,
                           location: Tuple[float, float], severity='MODERATE'):
    """Submit a community observation"""
    return validator.submit_observation(observer_id, obs_type, description, location, severity)

def get_indigenous_risk_score(location: Tuple[float, float], hours_back=24):
    """Get indigenous observations score for risk assessment"""
    return tk_modifier.calculate_indigenous_score_from_observations(location, hours_back)
