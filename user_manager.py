#!/usr/bin/env python3
"""
User Management Module for 1-800-PHONESEX
Handles user authentication, profiles, and subscription management
"""

import os
import json
import hashlib
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path

from payments import SubscriptionTier, get_plan_features


class User:
    """User profile and account information"""
    
    def __init__(self, user_id: str, email: str, subscription_tier: SubscriptionTier = SubscriptionTier.FREE):
        """
        Initialize user
        
        Args:
            user_id: Unique user identifier
            email: User email address
            subscription_tier: User's subscription tier
        """
        self.user_id = user_id
        self.email = email
        self.subscription_tier = subscription_tier
        self.created_at = datetime.now().isoformat()
        self.last_login = None
        self.customer_id = None  # Payment provider customer ID
        self.subscription_id = None  # Payment provider subscription ID
        self.metadata = {}
        
    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "subscription_tier": self.subscription_tier.value,
            "created_at": self.created_at,
            "last_login": self.last_login,
            "customer_id": self.customer_id,
            "subscription_id": self.subscription_id,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'User':
        """Create user from dictionary"""
        user = cls(
            user_id=data["user_id"],
            email=data["email"],
            subscription_tier=SubscriptionTier(data["subscription_tier"])
        )
        user.created_at = data.get("created_at", user.created_at)
        user.last_login = data.get("last_login")
        user.customer_id = data.get("customer_id")
        user.subscription_id = data.get("subscription_id")
        user.metadata = data.get("metadata", {})
        return user
    
    def get_features(self) -> Dict:
        """Get available features for user's subscription tier"""
        return get_plan_features(self.subscription_tier)
    
    def can_access_personality(self, personality_name: str) -> bool:
        """Check if user can access a specific personality"""
        features = self.get_features()
        available = features.get("personalities_available", [])
        return personality_name in available
    
    def get_daily_message_limit(self) -> int:
        """Get user's daily message limit"""
        features = self.get_features()
        return features.get("messages_per_day", 10)
    
    def has_streaming(self) -> bool:
        """Check if user has streaming access"""
        features = self.get_features()
        return features.get("streaming", False)
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.now().isoformat()


class UserManager:
    """Manages user accounts and authentication"""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize user manager
        
        Args:
            data_dir: Directory to store user data (defaults to ./user_data)
        """
        self.data_dir = Path(data_dir or os.getenv("USER_DATA_DIR", "./user_data"))
        self.data_dir.mkdir(exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self.sessions_file = self.data_dir / "sessions.json"
        
        self._load_users()
        self._load_sessions()
    
    def _load_users(self):
        """Load users from storage"""
        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                data = json.load(f)
                self.users = {
                    user_id: User.from_dict(user_data)
                    for user_id, user_data in data.items()
                }
        else:
            self.users = {}
    
    def _save_users(self):
        """Save users to storage"""
        data = {
            user_id: user.to_dict()
            for user_id, user in self.users.items()
        }
        with open(self.users_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_sessions(self):
        """Load active sessions"""
        if self.sessions_file.exists():
            with open(self.sessions_file, 'r') as f:
                self.sessions = json.load(f)
        else:
            self.sessions = {}
    
    def _save_sessions(self):
        """Save sessions to storage"""
        with open(self.sessions_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)
    
    def create_user(self, email: str, subscription_tier: SubscriptionTier = SubscriptionTier.FREE) -> User:
        """
        Create a new user
        
        Args:
            email: User email address
            subscription_tier: Initial subscription tier
        
        Returns:
            Created user object
        """
        # Generate user ID from email
        user_id = hashlib.sha256(email.encode()).hexdigest()[:16]
        
        # Check if user already exists
        if user_id in self.users:
            raise ValueError(f"User with email {email} already exists")
        
        user = User(user_id=user_id, email=email, subscription_tier=subscription_tier)
        self.users[user_id] = user
        self._save_users()
        
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User identifier
        
        Returns:
            User object or None if not found
        """
        return self.users.get(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email
        
        Args:
            email: User email address
        
        Returns:
            User object or None if not found
        """
        user_id = hashlib.sha256(email.encode()).hexdigest()[:16]
        return self.users.get(user_id)
    
    def update_subscription(self, user_id: str, subscription_tier: SubscriptionTier, 
                          customer_id: Optional[str] = None,
                          subscription_id: Optional[str] = None) -> bool:
        """
        Update user's subscription
        
        Args:
            user_id: User identifier
            subscription_tier: New subscription tier
            customer_id: Payment provider customer ID
            subscription_id: Payment provider subscription ID
        
        Returns:
            True if successful, False otherwise
        """
        user = self.get_user(user_id)
        if not user:
            return False
        
        user.subscription_tier = subscription_tier
        if customer_id:
            user.customer_id = customer_id
        if subscription_id:
            user.subscription_id = subscription_id
        
        self._save_users()
        return True
    
    def create_session(self, user_id: str) -> str:
        """
        Create a new session for user
        
        Args:
            user_id: User identifier
        
        Returns:
            Session token
        """
        import secrets
        session_token = secrets.token_urlsafe(32)
        
        self.sessions[session_token] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat()
        }
        
        # Update user's last login
        user = self.get_user(user_id)
        if user:
            user.update_last_login()
            self._save_users()
        
        self._save_sessions()
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[str]:
        """
        Validate session and return user ID
        
        Args:
            session_token: Session token to validate
        
        Returns:
            User ID if valid, None otherwise
        """
        session = self.sessions.get(session_token)
        if not session:
            return None
        
        # Update last activity
        session["last_activity"] = datetime.now().isoformat()
        self._save_sessions()
        
        return session.get("user_id")
    
    def end_session(self, session_token: str):
        """
        End a user session
        
        Args:
            session_token: Session token to end
        """
        if session_token in self.sessions:
            del self.sessions[session_token]
            self._save_sessions()
    
    def list_users(self, subscription_tier: Optional[SubscriptionTier] = None) -> List[User]:
        """
        List all users, optionally filtered by subscription tier
        
        Args:
            subscription_tier: Optional filter by subscription tier
        
        Returns:
            List of users
        """
        users = list(self.users.values())
        
        if subscription_tier:
            users = [u for u in users if u.subscription_tier == subscription_tier]
        
        return users
    
    def get_user_count(self, subscription_tier: Optional[SubscriptionTier] = None) -> int:
        """
        Get count of users
        
        Args:
            subscription_tier: Optional filter by subscription tier
        
        Returns:
            Number of users
        """
        return len(self.list_users(subscription_tier))


class FeatureGate:
    """Controls access to premium features"""
    
    @staticmethod
    def check_personality_access(user: User, personality_name: str) -> bool:
        """
        Check if user can access a personality
        
        Args:
            user: User object
            personality_name: Name of personality to check
        
        Returns:
            True if user has access, False otherwise
        """
        return user.can_access_personality(personality_name)
    
    @staticmethod
    def check_streaming_access(user: User) -> bool:
        """
        Check if user has streaming access
        
        Args:
            user: User object
        
        Returns:
            True if user has streaming, False otherwise
        """
        return user.has_streaming()
    
    @staticmethod
    def check_message_limit(user: User, current_usage: int) -> bool:
        """
        Check if user is within message limit
        
        Args:
            user: User object
            current_usage: Current message count for today
        
        Returns:
            True if within limit, False otherwise
        """
        limit = user.get_daily_message_limit()
        if limit == -1:  # Unlimited
            return True
        return current_usage < limit
    
    @staticmethod
    def get_upgrade_prompt(user: User, feature: str) -> str:
        """
        Get upgrade prompt message for a feature
        
        Args:
            user: User object
            feature: Feature name
        
        Returns:
            Upgrade prompt message
        """
        prompts = {
            "personality": "🔒 This operator is only available to Premium and VIP subscribers. Upgrade to unlock all 5 personalities!",
            "streaming": "🔒 Real-time streaming is a Premium feature. Upgrade to experience instant, flowing conversations!",
            "limit": f"📊 You've reached your daily limit of {user.get_daily_message_limit()} messages. Upgrade to Premium for 100 messages/day or VIP for unlimited!",
            "custom": "🔒 Custom personalities are exclusive to VIP members. Upgrade to create your own unique operators!"
        }
        return prompts.get(feature, "🔒 Upgrade to unlock this premium feature!")
