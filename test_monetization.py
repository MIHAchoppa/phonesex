#!/usr/bin/env python3
"""
Test suite for monetization features
Tests payment processing, subscriptions, and user management
"""

import sys
import os
import tempfile
import shutil
from datetime import datetime

# Mock environment for testing
os.environ['GROQ_API_KEY'] = 'test_key_for_testing'

from payments import (
    SubscriptionTier, SubscriptionPlans, PaymentProcessor, 
    UsageTracker, get_plan_features, compare_plans
)
from user_manager import User, UserManager, FeatureGate


def test_subscription_plans():
    """Test subscription plan configurations"""
    print("Testing Subscription Plans...")
    
    # Test FREE plan
    free = SubscriptionPlans.FREE
    assert free['price'] == 0.00
    assert free['messages_per_day'] == 10
    assert "Flirty" in free['personalities_available']
    assert free['streaming'] == False
    print("  ✓ FREE plan validated")
    
    # Test PREMIUM plan
    premium = SubscriptionPlans.PREMIUM
    assert premium['price'] == 9.99
    assert premium['messages_per_day'] == 100
    assert len(premium['personalities_available']) == 5
    assert premium['streaming'] == True
    print("  ✓ PREMIUM plan validated")
    
    # Test VIP plan
    vip = SubscriptionPlans.VIP
    assert vip['price'] == 29.99
    assert vip['messages_per_day'] == -1  # Unlimited
    assert vip['custom_personalities'] == True
    print("  ✓ VIP plan validated")
    
    print("✓ All subscription plans validated\n")


def test_payment_processor():
    """Test payment processor functionality"""
    print("Testing Payment Processor...")
    
    processor = PaymentProcessor(api_key="test_key")
    assert processor.test_mode == True
    print("  ✓ Payment processor initialized")
    
    # Test customer creation
    customer = processor.create_customer("test@example.com", {"test": "data"})
    assert customer['email'] == "test@example.com"
    assert 'id' in customer
    print("  ✓ Customer creation works")
    
    # Test subscription creation
    subscription = processor.create_subscription(customer['id'], SubscriptionTier.PREMIUM)
    assert subscription['plan'] == "premium"
    assert subscription['status'] == "active"
    assert subscription['amount'] == 9.99
    print("  ✓ Subscription creation works")
    
    # Test payment intent
    payment = processor.create_payment_intent(29.99, "usd", customer['id'])
    assert payment['amount'] == 2999  # In cents
    assert payment['currency'] == "usd"
    print("  ✓ Payment intent creation works")
    
    # Test subscription cancellation
    result = processor.cancel_subscription(subscription['id'])
    assert result['status'] == "canceled"
    print("  ✓ Subscription cancellation works")
    
    print("✓ Payment processor functional\n")


def test_usage_tracker():
    """Test usage tracking functionality"""
    print("Testing Usage Tracker...")
    
    tracker = UsageTracker()
    user_id = "test_user_123"
    
    # Track messages
    tracker.track_message(user_id)
    tracker.track_message(user_id)
    tracker.track_message(user_id)
    
    usage = tracker.get_usage(user_id)
    assert usage == 3
    print("  ✓ Message tracking works")
    
    # Test limit checking
    assert tracker.check_limit(user_id, 10) == True
    assert tracker.check_limit(user_id, 2) == False
    assert tracker.check_limit(user_id, -1) == True  # Unlimited
    print("  ✓ Limit checking works")
    
    # Test reset
    tracker.reset_usage(user_id)
    usage = tracker.get_usage(user_id)
    assert usage == 0
    print("  ✓ Usage reset works")
    
    print("✓ Usage tracker functional\n")


def test_user_management():
    """Test user creation and management"""
    print("Testing User Management...")
    
    # Create temp directory for user data
    temp_dir = tempfile.mkdtemp()
    
    try:
        user_manager = UserManager(data_dir=temp_dir)
        
        # Test user creation
        user = user_manager.create_user("user@example.com", SubscriptionTier.FREE)
        assert user.email == "user@example.com"
        assert user.subscription_tier == SubscriptionTier.FREE
        print("  ✓ User creation works")
        
        # Test user retrieval
        retrieved = user_manager.get_user(user.user_id)
        assert retrieved.email == user.email
        print("  ✓ User retrieval works")
        
        # Test user retrieval by email
        retrieved_by_email = user_manager.get_user_by_email("user@example.com")
        assert retrieved_by_email.user_id == user.user_id
        print("  ✓ User retrieval by email works")
        
        # Test subscription update
        success = user_manager.update_subscription(
            user.user_id, 
            SubscriptionTier.PREMIUM,
            customer_id="cus_test_123",
            subscription_id="sub_test_123"
        )
        assert success == True
        updated_user = user_manager.get_user(user.user_id)
        assert updated_user.subscription_tier == SubscriptionTier.PREMIUM
        assert updated_user.customer_id == "cus_test_123"
        print("  ✓ Subscription update works")
        
        # Test session management
        session_token = user_manager.create_session(user.user_id)
        assert len(session_token) > 0
        print("  ✓ Session creation works")
        
        validated_user_id = user_manager.validate_session(session_token)
        assert validated_user_id == user.user_id
        print("  ✓ Session validation works")
        
        user_manager.end_session(session_token)
        validated_again = user_manager.validate_session(session_token)
        assert validated_again is None
        print("  ✓ Session termination works")
        
        # Test user listing
        user2 = user_manager.create_user("user2@example.com", SubscriptionTier.VIP)
        all_users = user_manager.list_users()
        assert len(all_users) == 2
        print("  ✓ User listing works")
        
        vip_users = user_manager.list_users(SubscriptionTier.VIP)
        assert len(vip_users) == 1
        assert vip_users[0].subscription_tier == SubscriptionTier.VIP
        print("  ✓ Filtered user listing works")
        
    finally:
        # Cleanup temp directory
        shutil.rmtree(temp_dir)
    
    print("✓ User management functional\n")


def test_user_features():
    """Test user feature access"""
    print("Testing User Features...")
    
    # Test FREE user
    free_user = User("user1", "free@example.com", SubscriptionTier.FREE)
    features = free_user.get_features()
    assert features['messages_per_day'] == 10
    assert free_user.can_access_personality("Flirty") == True
    assert free_user.can_access_personality("Romantic") == False
    assert free_user.has_streaming() == False
    print("  ✓ FREE user features correct")
    
    # Test PREMIUM user
    premium_user = User("user2", "premium@example.com", SubscriptionTier.PREMIUM)
    assert premium_user.can_access_personality("Flirty") == True
    assert premium_user.can_access_personality("Romantic") == True
    assert premium_user.has_streaming() == True
    assert premium_user.get_daily_message_limit() == 100
    print("  ✓ PREMIUM user features correct")
    
    # Test VIP user
    vip_user = User("user3", "vip@example.com", SubscriptionTier.VIP)
    assert vip_user.get_daily_message_limit() == -1  # Unlimited
    assert vip_user.can_access_personality("Playful") == True
    vip_features = vip_user.get_features()
    assert vip_features['custom_personalities'] == True
    print("  ✓ VIP user features correct")
    
    print("✓ User features validated\n")


def test_feature_gates():
    """Test feature gating logic"""
    print("Testing Feature Gates...")
    
    free_user = User("user1", "free@example.com", SubscriptionTier.FREE)
    premium_user = User("user2", "premium@example.com", SubscriptionTier.PREMIUM)
    
    # Test personality access
    assert FeatureGate.check_personality_access(free_user, "Flirty") == True
    assert FeatureGate.check_personality_access(free_user, "Romantic") == False
    assert FeatureGate.check_personality_access(premium_user, "Romantic") == True
    print("  ✓ Personality access gates work")
    
    # Test streaming access
    assert FeatureGate.check_streaming_access(free_user) == False
    assert FeatureGate.check_streaming_access(premium_user) == True
    print("  ✓ Streaming access gates work")
    
    # Test message limits
    assert FeatureGate.check_message_limit(free_user, 5) == True
    assert FeatureGate.check_message_limit(free_user, 15) == False
    print("  ✓ Message limit gates work")
    
    # Test upgrade prompts
    prompt = FeatureGate.get_upgrade_prompt(free_user, "personality")
    assert "Premium" in prompt or "VIP" in prompt
    print("  ✓ Upgrade prompts generated")
    
    print("✓ Feature gates functional\n")


def test_helper_functions():
    """Test helper functions"""
    print("Testing Helper Functions...")
    
    # Test get_plan_features
    free_features = get_plan_features(SubscriptionTier.FREE)
    assert free_features['price'] == 0.00
    print("  ✓ get_plan_features works")
    
    # Test compare_plans
    plans = compare_plans()
    assert len(plans) == 3
    assert plans[0]['name'] == "Free"
    assert plans[1]['name'] == "Premium"
    assert plans[2]['name'] == "VIP"
    print("  ✓ compare_plans works")
    
    print("✓ Helper functions validated\n")


def test_webhook_processing():
    """Test webhook event processing"""
    print("Testing Webhook Processing...")
    
    processor = PaymentProcessor(api_key="test_key")
    
    # Test payment success webhook
    event = {
        "type": "payment_intent.succeeded",
        "data": {"amount": 999}
    }
    result = processor.process_webhook(event, "sig_test")
    assert result['status'] == 'success'
    assert result['event_type'] == 'payment_success'
    print("  ✓ Payment success webhook handled")
    
    # Test subscription created webhook
    event = {
        "type": "customer.subscription.created",
        "data": {"subscription_id": "sub_123"}
    }
    result = processor.process_webhook(event, "sig_test")
    assert result['event_type'] == 'subscription_created'
    print("  ✓ Subscription created webhook handled")
    
    # Test unhandled event
    event = {
        "type": "unknown.event",
        "data": {}
    }
    result = processor.process_webhook(event, "sig_test")
    assert result['status'] == 'unhandled'
    print("  ✓ Unhandled events processed correctly")
    
    print("✓ Webhook processing functional\n")


def main():
    """Run all monetization tests"""
    print("=" * 60)
    print("🧪 MONETIZATION FEATURES TEST SUITE")
    print("=" * 60)
    print()
    
    try:
        test_subscription_plans()
        test_payment_processor()
        test_usage_tracker()
        test_user_management()
        test_user_features()
        test_feature_gates()
        test_helper_functions()
        test_webhook_processing()
        
        print("=" * 60)
        print("✅ ALL MONETIZATION TESTS PASSED!")
        print("=" * 60)
        print()
        print("Monetization features successfully implemented:")
        print("  ✓ Payment processing with Stripe integration")
        print("  ✓ Three-tier subscription model (FREE, PREMIUM, VIP)")
        print("  ✓ User management and authentication")
        print("  ✓ Usage tracking and limits")
        print("  ✓ Feature gating logic")
        print("  ✓ Webhook event handling")
        print("  ✓ Session management")
        print()
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
