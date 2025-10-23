#!/usr/bin/env python3
"""
Payment Processing Module for 1-800-PHONESEX
Handles Stripe integration, subscriptions, and payment processing
"""

import os
import json
from typing import Dict, Optional, List
from enum import Enum
from datetime import datetime, timedelta


class SubscriptionTier(Enum):
    """Subscription tier definitions"""
    FREE = "free"
    PREMIUM = "premium"
    VIP = "vip"


class SubscriptionPlans:
    """Subscription plan configurations"""
    
    FREE = {
        "name": "Free",
        "price": 0.00,
        "currency": "USD",
        "messages_per_day": 10,
        "personalities_available": ["Flirty"],
        "streaming": False,
        "priority_support": False,
        "custom_personalities": False,
        "description": "Try the basic experience - 10 messages per day with Flirty personality"
    }
    
    PREMIUM = {
        "name": "Premium",
        "price": 9.99,
        "currency": "USD",
        "billing_period": "monthly",
        "messages_per_day": 100,
        "personalities_available": ["Flirty", "Romantic", "Adventurous", "Mysterious", "Playful"],
        "streaming": True,
        "priority_support": True,
        "custom_personalities": False,
        "description": "Full access to all 5 operators with unlimited streaming - 100 messages/day"
    }
    
    VIP = {
        "name": "VIP",
        "price": 29.99,
        "currency": "USD",
        "billing_period": "monthly",
        "messages_per_day": -1,  # Unlimited
        "personalities_available": ["Flirty", "Romantic", "Adventurous", "Mysterious", "Playful"],
        "streaming": True,
        "priority_support": True,
        "custom_personalities": True,
        "custom_personality_slots": 3,
        "description": "Ultimate experience - unlimited messages, all operators, custom personalities"
    }


class PaymentProcessor:
    """Handles payment processing operations"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize payment processor"""
        self.api_key = api_key or os.getenv("STRIPE_API_KEY")
        self.webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        self.test_mode = os.getenv("STRIPE_TEST_MODE", "true").lower() == "true"
        
        # In a real implementation, we would initialize Stripe here
        # import stripe
        # stripe.api_key = self.api_key
    
    def create_customer(self, email: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Create a new customer in the payment system
        
        Args:
            email: Customer email address
            metadata: Additional customer metadata
        
        Returns:
            Customer data dictionary
        """
        # Mock implementation for demo
        customer = {
            "id": f"cus_{'test' if self.test_mode else 'live'}_{datetime.now().timestamp()}",
            "email": email,
            "metadata": metadata or {},
            "created": datetime.now().isoformat()
        }
        
        # In real implementation:
        # customer = stripe.Customer.create(email=email, metadata=metadata)
        
        return customer
    
    def create_subscription(self, customer_id: str, plan: SubscriptionTier) -> Dict:
        """
        Create a subscription for a customer
        
        Args:
            customer_id: Customer ID
            plan: Subscription tier
        
        Returns:
            Subscription data dictionary
        """
        plan_config = self._get_plan_config(plan)
        
        subscription = {
            "id": f"sub_{'test' if self.test_mode else 'live'}_{datetime.now().timestamp()}",
            "customer_id": customer_id,
            "plan": plan.value,
            "status": "active",
            "current_period_start": datetime.now().isoformat(),
            "current_period_end": (datetime.now() + timedelta(days=30)).isoformat(),
            "amount": plan_config["price"],
            "currency": plan_config["currency"],
            "created": datetime.now().isoformat()
        }
        
        # In real implementation:
        # subscription = stripe.Subscription.create(
        #     customer=customer_id,
        #     items=[{"price": plan_config["stripe_price_id"]}]
        # )
        
        return subscription
    
    def cancel_subscription(self, subscription_id: str) -> Dict:
        """
        Cancel a subscription
        
        Args:
            subscription_id: Subscription ID to cancel
        
        Returns:
            Cancellation result
        """
        result = {
            "id": subscription_id,
            "status": "canceled",
            "canceled_at": datetime.now().isoformat()
        }
        
        # In real implementation:
        # subscription = stripe.Subscription.delete(subscription_id)
        
        return result
    
    def create_payment_intent(self, amount: float, currency: str = "usd", 
                            customer_id: Optional[str] = None) -> Dict:
        """
        Create a payment intent for one-time payments
        
        Args:
            amount: Amount in currency units
            currency: Currency code
            customer_id: Optional customer ID
        
        Returns:
            Payment intent data
        """
        payment_intent = {
            "id": f"pi_{'test' if self.test_mode else 'live'}_{datetime.now().timestamp()}",
            "amount": int(amount * 100),  # Convert to cents
            "currency": currency,
            "customer_id": customer_id,
            "status": "requires_payment_method",
            "created": datetime.now().isoformat()
        }
        
        # In real implementation:
        # payment_intent = stripe.PaymentIntent.create(
        #     amount=int(amount * 100),
        #     currency=currency,
        #     customer=customer_id
        # )
        
        return payment_intent
    
    def process_webhook(self, payload: str, signature: str) -> Dict:
        """
        Process webhook events from payment provider
        
        Args:
            payload: Webhook payload
            signature: Webhook signature for verification
        
        Returns:
            Processed event data
        """
        # In real implementation:
        # event = stripe.Webhook.construct_event(
        #     payload, signature, self.webhook_secret
        # )
        
        # Mock event processing
        event = json.loads(payload) if isinstance(payload, str) else payload
        
        event_handlers = {
            "payment_intent.succeeded": self._handle_payment_success,
            "payment_intent.failed": self._handle_payment_failure,
            "customer.subscription.created": self._handle_subscription_created,
            "customer.subscription.updated": self._handle_subscription_updated,
            "customer.subscription.deleted": self._handle_subscription_deleted,
        }
        
        handler = event_handlers.get(event.get("type"))
        if handler:
            return handler(event)
        
        return {"status": "unhandled", "type": event.get("type")}
    
    def _get_plan_config(self, plan: SubscriptionTier) -> Dict:
        """Get configuration for a subscription plan"""
        plans = {
            SubscriptionTier.FREE: SubscriptionPlans.FREE,
            SubscriptionTier.PREMIUM: SubscriptionPlans.PREMIUM,
            SubscriptionTier.VIP: SubscriptionPlans.VIP
        }
        return plans.get(plan, SubscriptionPlans.FREE)
    
    def _handle_payment_success(self, event: Dict) -> Dict:
        """Handle successful payment"""
        return {
            "status": "success",
            "message": "Payment processed successfully",
            "event_type": "payment_success",
            "data": event
        }
    
    def _handle_payment_failure(self, event: Dict) -> Dict:
        """Handle failed payment"""
        return {
            "status": "failed",
            "message": "Payment processing failed",
            "event_type": "payment_failure",
            "data": event
        }
    
    def _handle_subscription_created(self, event: Dict) -> Dict:
        """Handle subscription creation"""
        return {
            "status": "success",
            "message": "Subscription created",
            "event_type": "subscription_created",
            "data": event
        }
    
    def _handle_subscription_updated(self, event: Dict) -> Dict:
        """Handle subscription update"""
        return {
            "status": "success",
            "message": "Subscription updated",
            "event_type": "subscription_updated",
            "data": event
        }
    
    def _handle_subscription_deleted(self, event: Dict) -> Dict:
        """Handle subscription cancellation"""
        return {
            "status": "success",
            "message": "Subscription canceled",
            "event_type": "subscription_deleted",
            "data": event
        }


class UsageTracker:
    """Tracks user usage and enforces limits"""
    
    def __init__(self):
        """Initialize usage tracker"""
        self.usage_data = {}
    
    def track_message(self, user_id: str) -> bool:
        """
        Track a message and check if within limits
        
        Args:
            user_id: User identifier
        
        Returns:
            True if message is allowed, False if limit exceeded
        """
        today = datetime.now().date().isoformat()
        
        if user_id not in self.usage_data:
            self.usage_data[user_id] = {}
        
        if today not in self.usage_data[user_id]:
            self.usage_data[user_id][today] = 0
        
        self.usage_data[user_id][today] += 1
        return True
    
    def get_usage(self, user_id: str, date: Optional[str] = None) -> int:
        """
        Get usage count for a user on a specific date
        
        Args:
            user_id: User identifier
            date: Date string (ISO format), defaults to today
        
        Returns:
            Number of messages used
        """
        date = date or datetime.now().date().isoformat()
        return self.usage_data.get(user_id, {}).get(date, 0)
    
    def check_limit(self, user_id: str, limit: int) -> bool:
        """
        Check if user is within their message limit
        
        Args:
            user_id: User identifier
            limit: Daily message limit (-1 for unlimited)
        
        Returns:
            True if within limit, False if exceeded
        """
        if limit == -1:  # Unlimited
            return True
        
        current_usage = self.get_usage(user_id)
        return current_usage < limit
    
    def reset_usage(self, user_id: str, date: Optional[str] = None):
        """
        Reset usage for a user on a specific date
        
        Args:
            user_id: User identifier
            date: Date string (ISO format), defaults to today
        """
        date = date or datetime.now().date().isoformat()
        if user_id in self.usage_data and date in self.usage_data[user_id]:
            self.usage_data[user_id][date] = 0


def get_plan_features(tier: SubscriptionTier) -> Dict:
    """
    Get features for a subscription tier
    
    Args:
        tier: Subscription tier
    
    Returns:
        Dictionary of plan features
    """
    plans = {
        SubscriptionTier.FREE: SubscriptionPlans.FREE,
        SubscriptionTier.PREMIUM: SubscriptionPlans.PREMIUM,
        SubscriptionTier.VIP: SubscriptionPlans.VIP
    }
    return plans.get(tier, SubscriptionPlans.FREE)


def compare_plans() -> List[Dict]:
    """
    Get comparison of all subscription plans
    
    Returns:
        List of plan details for comparison
    """
    return [
        SubscriptionPlans.FREE,
        SubscriptionPlans.PREMIUM,
        SubscriptionPlans.VIP
    ]
