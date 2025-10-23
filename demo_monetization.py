#!/usr/bin/env python3
"""
Demo of monetization features
Shows how subscription tiers and feature gating work
"""

import os
os.environ['GROQ_API_KEY'] = 'demo_key_for_testing'

from user_manager import User, UserManager, FeatureGate
from payments import SubscriptionTier, UsageTracker, compare_plans
from admin_dashboard import AdminDashboard


def print_section(title):
    """Print section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_subscription_plans():
    """Demonstrate subscription plans"""
    print_section("SUBSCRIPTION PLANS")
    
    plans = compare_plans()
    for plan in plans:
        print(f"\n🔥 {plan['name'].upper()} - ${plan['price']:.2f}/month")
        print(f"   {plan['description']}")
        print(f"   • Messages: {plan['messages_per_day'] if plan['messages_per_day'] != -1 else 'Unlimited'} per day")
        print(f"   • Personalities: {', '.join(plan['personalities_available'])}")
        print(f"   • Streaming: {'✓' if plan['streaming'] else '✗'}")


def demo_user_features():
    """Demonstrate user features by tier"""
    print_section("USER FEATURES BY TIER")
    
    # Create users with different tiers
    free_user = User("user1", "free@example.com", SubscriptionTier.FREE)
    premium_user = User("user2", "premium@example.com", SubscriptionTier.PREMIUM)
    vip_user = User("user3", "vip@example.com", SubscriptionTier.VIP)
    
    users = [
        ("FREE", free_user),
        ("PREMIUM", premium_user),
        ("VIP", vip_user)
    ]
    
    personalities = ["Flirty", "Romantic", "Adventurous", "Mysterious", "Playful"]
    
    for tier_name, user in users:
        print(f"\n{tier_name} User:")
        print(f"  Daily Messages: {user.get_daily_message_limit() if user.get_daily_message_limit() != -1 else 'Unlimited'}")
        print(f"  Streaming: {'✓' if user.has_streaming() else '✗'}")
        print(f"  Available Personalities:")
        for personality in personalities:
            access = "✓" if user.can_access_personality(personality) else "✗"
            print(f"    {access} {personality}")


def demo_feature_gating():
    """Demonstrate feature gating"""
    print_section("FEATURE GATING DEMO")
    
    free_user = User("user1", "free@example.com", SubscriptionTier.FREE)
    
    print("\nFREE user trying to access premium features:")
    
    # Try to access locked personality
    print("\n1. Accessing 'Romantic' personality (Premium feature):")
    if not FeatureGate.check_personality_access(free_user, "Romantic"):
        print(f"   {FeatureGate.get_upgrade_prompt(free_user, 'personality')}")
    
    # Try to use streaming
    print("\n2. Using streaming (Premium feature):")
    if not FeatureGate.check_streaming_access(free_user):
        print(f"   {FeatureGate.get_upgrade_prompt(free_user, 'streaming')}")
    
    # Try to exceed message limit
    print("\n3. Checking message limits:")
    print(f"   Current usage: 5/10")
    print(f"   Within limit: {FeatureGate.check_message_limit(free_user, 5)}")
    print(f"   Current usage: 12/10")
    print(f"   Within limit: {FeatureGate.check_message_limit(free_user, 12)}")
    if not FeatureGate.check_message_limit(free_user, 12):
        print(f"   {FeatureGate.get_upgrade_prompt(free_user, 'limit')}")


def demo_usage_tracking():
    """Demonstrate usage tracking"""
    print_section("USAGE TRACKING DEMO")
    
    tracker = UsageTracker()
    user_id = "demo_user_123"
    
    print("\nSimulating message usage:")
    for i in range(1, 6):
        tracker.track_message(user_id)
        usage = tracker.get_usage(user_id)
        print(f"  Message {i}: Usage now at {usage}")
    
    print(f"\nChecking limits:")
    print(f"  Within limit of 10: {tracker.check_limit(user_id, 10)}")
    print(f"  Within limit of 3: {tracker.check_limit(user_id, 3)}")
    print(f"  Unlimited (-1): {tracker.check_limit(user_id, -1)}")


def demo_admin_dashboard():
    """Demonstrate admin dashboard"""
    print_section("ADMIN DASHBOARD DEMO")
    
    # Create temporary user data
    import tempfile
    temp_dir = tempfile.mkdtemp()
    
    # Setup users
    user_manager = UserManager(data_dir=temp_dir)
    user_manager.create_user("free1@example.com", SubscriptionTier.FREE)
    user_manager.create_user("free2@example.com", SubscriptionTier.FREE)
    user_manager.create_user("premium1@example.com", SubscriptionTier.PREMIUM)
    user_manager.create_user("premium2@example.com", SubscriptionTier.PREMIUM)
    user_manager.create_user("vip1@example.com", SubscriptionTier.VIP)
    
    # Generate dashboard report
    dashboard = AdminDashboard(data_dir=temp_dir)
    print(dashboard.generate_report())
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


def demo_upgrade_flow():
    """Demonstrate upgrade flow"""
    print_section("UPGRADE FLOW DEMO")
    
    print("\nSimulating user upgrade from FREE to PREMIUM:")
    
    import tempfile
    temp_dir = tempfile.mkdtemp()
    
    # Create FREE user
    user_manager = UserManager(data_dir=temp_dir)
    user = user_manager.create_user("upgrade@example.com", SubscriptionTier.FREE)
    
    print(f"\n1. Initial state:")
    print(f"   Tier: {user.subscription_tier.value.upper()}")
    print(f"   Messages: {user.get_daily_message_limit()}/day")
    print(f"   Streaming: {'✓' if user.has_streaming() else '✗'}")
    
    # Upgrade to PREMIUM
    print(f"\n2. Upgrading to PREMIUM...")
    from payments import PaymentProcessor
    processor = PaymentProcessor()
    customer = processor.create_customer(user.email)
    subscription = processor.create_subscription(customer['id'], SubscriptionTier.PREMIUM)
    
    user_manager.update_subscription(
        user.user_id,
        SubscriptionTier.PREMIUM,
        customer_id=customer['id'],
        subscription_id=subscription['id']
    )
    
    # Get updated user
    updated_user = user_manager.get_user(user.user_id)
    
    print(f"\n3. After upgrade:")
    print(f"   Tier: {updated_user.subscription_tier.value.upper()}")
    print(f"   Messages: {updated_user.get_daily_message_limit()}/day")
    print(f"   Streaming: {'✓' if updated_user.has_streaming() else '✗'}")
    print(f"   Available personalities: {len(updated_user.get_features()['personalities_available'])}")
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_dir)


def main():
    """Run all demos"""
    print("=" * 60)
    print("  🔥 1-800-PHONESEX MONETIZATION DEMO")
    print("=" * 60)
    
    demo_subscription_plans()
    demo_user_features()
    demo_feature_gating()
    demo_usage_tracking()
    demo_admin_dashboard()
    demo_upgrade_flow()
    
    print("\n" + "=" * 60)
    print("  ✅ DEMO COMPLETE")
    print("=" * 60)
    print("\nMonetization features demonstrated:")
    print("  ✓ Three-tier subscription model")
    print("  ✓ Feature gating and access control")
    print("  ✓ Usage tracking and limits")
    print("  ✓ Admin dashboard and analytics")
    print("  ✓ User upgrade flow")
    print("\nFor more details, see MONETIZATION.md")
    print()


if __name__ == "__main__":
    main()
