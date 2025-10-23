#!/usr/bin/env python3
"""
Admin Dashboard Utilities for 1-800-PHONESEX
Provides tools for managing users, subscriptions, and viewing analytics
"""

import os
import sys
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict

from user_manager import User, UserManager
from payments import SubscriptionTier, PaymentProcessor, UsageTracker


class AdminDashboard:
    """Admin dashboard for managing the application"""
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize admin dashboard
        
        Args:
            data_dir: Directory containing user data
        """
        self.user_manager = UserManager(data_dir=data_dir)
        self.payment_processor = PaymentProcessor()
        self.usage_tracker = UsageTracker()
    
    def get_user_stats(self) -> Dict:
        """
        Get overall user statistics
        
        Returns:
            Dictionary with user statistics
        """
        total_users = self.user_manager.get_user_count()
        free_users = self.user_manager.get_user_count(SubscriptionTier.FREE)
        premium_users = self.user_manager.get_user_count(SubscriptionTier.PREMIUM)
        vip_users = self.user_manager.get_user_count(SubscriptionTier.VIP)
        
        return {
            "total_users": total_users,
            "free_users": free_users,
            "premium_users": premium_users,
            "vip_users": vip_users,
            "conversion_rate": (premium_users + vip_users) / total_users * 100 if total_users > 0 else 0
        }
    
    def get_revenue_stats(self) -> Dict:
        """
        Calculate revenue statistics
        
        Returns:
            Dictionary with revenue statistics
        """
        premium_users = self.user_manager.get_user_count(SubscriptionTier.PREMIUM)
        vip_users = self.user_manager.get_user_count(SubscriptionTier.VIP)
        
        monthly_recurring_revenue = (premium_users * 9.99) + (vip_users * 29.99)
        annual_recurring_revenue = monthly_recurring_revenue * 12
        
        return {
            "mrr": monthly_recurring_revenue,
            "arr": annual_recurring_revenue,
            "average_revenue_per_user": monthly_recurring_revenue / max(premium_users + vip_users, 1)
        }
    
    def get_usage_analytics(self) -> Dict:
        """
        Get usage analytics
        
        Returns:
            Dictionary with usage statistics
        """
        users = self.user_manager.list_users()
        total_messages = 0
        active_users = 0
        
        today = datetime.now().date().isoformat()
        
        for user in users:
            usage = self.usage_tracker.get_usage(user.user_id, today)
            total_messages += usage
            if usage > 0:
                active_users += 1
        
        return {
            "total_messages_today": total_messages,
            "active_users_today": active_users,
            "average_messages_per_active_user": total_messages / max(active_users, 1)
        }
    
    def list_users_detailed(self, tier: Optional[SubscriptionTier] = None) -> List[Dict]:
        """
        Get detailed user list
        
        Args:
            tier: Optional filter by subscription tier
        
        Returns:
            List of user details
        """
        users = self.user_manager.list_users(tier)
        
        user_details = []
        for user in users:
            today = datetime.now().date().isoformat()
            usage = self.usage_tracker.get_usage(user.user_id, today)
            
            user_details.append({
                "user_id": user.user_id,
                "email": user.email,
                "subscription_tier": user.subscription_tier.value,
                "created_at": user.created_at,
                "last_login": user.last_login,
                "messages_today": usage,
                "daily_limit": user.get_daily_message_limit()
            })
        
        return user_details
    
    def upgrade_user(self, user_id: str, new_tier: SubscriptionTier) -> bool:
        """
        Upgrade a user's subscription (admin override)
        
        Args:
            user_id: User ID to upgrade
            new_tier: New subscription tier
        
        Returns:
            True if successful, False otherwise
        """
        user = self.user_manager.get_user(user_id)
        if not user:
            return False
        
        # In production, would create actual subscription
        customer = self.payment_processor.create_customer(user.email)
        subscription = self.payment_processor.create_subscription(
            customer['id'], 
            new_tier
        )
        
        return self.user_manager.update_subscription(
            user_id,
            new_tier,
            customer_id=customer['id'],
            subscription_id=subscription['id']
        )
    
    def downgrade_user(self, user_id: str, new_tier: SubscriptionTier) -> bool:
        """
        Downgrade a user's subscription
        
        Args:
            user_id: User ID to downgrade
            new_tier: New subscription tier
        
        Returns:
            True if successful, False otherwise
        """
        user = self.user_manager.get_user(user_id)
        if not user:
            return False
        
        # Cancel existing subscription if exists
        if user.subscription_id:
            self.payment_processor.cancel_subscription(user.subscription_id)
        
        return self.user_manager.update_subscription(user_id, new_tier)
    
    def get_churn_risk_users(self) -> List[User]:
        """
        Identify users at risk of churning
        
        Returns:
            List of users who haven't logged in recently
        """
        users = self.user_manager.list_users()
        at_risk = []
        
        threshold = datetime.now() - timedelta(days=7)
        
        for user in users:
            if user.last_login:
                last_login_dt = datetime.fromisoformat(user.last_login)
                if last_login_dt < threshold and user.subscription_tier != SubscriptionTier.FREE:
                    at_risk.append(user)
        
        return at_risk
    
    def generate_report(self) -> str:
        """
        Generate a comprehensive admin report
        
        Returns:
            Formatted report string
        """
        user_stats = self.get_user_stats()
        revenue_stats = self.get_revenue_stats()
        usage_stats = self.get_usage_analytics()
        churn_risk = len(self.get_churn_risk_users())
        
        report = []
        report.append("=" * 60)
        report.append("📊 1-800-PHONESEX ADMIN DASHBOARD")
        report.append("=" * 60)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        report.append("\n📈 USER STATISTICS")
        report.append("-" * 60)
        report.append(f"Total Users:       {user_stats['total_users']}")
        report.append(f"FREE Users:        {user_stats['free_users']}")
        report.append(f"PREMIUM Users:     {user_stats['premium_users']}")
        report.append(f"VIP Users:         {user_stats['vip_users']}")
        report.append(f"Conversion Rate:   {user_stats['conversion_rate']:.2f}%")
        
        report.append("\n💰 REVENUE STATISTICS")
        report.append("-" * 60)
        report.append(f"MRR:               ${revenue_stats['mrr']:.2f}")
        report.append(f"ARR:               ${revenue_stats['arr']:.2f}")
        report.append(f"ARPU:              ${revenue_stats['average_revenue_per_user']:.2f}")
        
        report.append("\n💬 USAGE ANALYTICS")
        report.append("-" * 60)
        report.append(f"Messages Today:    {usage_stats['total_messages_today']}")
        report.append(f"Active Users:      {usage_stats['active_users_today']}")
        report.append(f"Avg Msgs/User:     {usage_stats['average_messages_per_active_user']:.1f}")
        
        report.append("\n⚠️  CHURN RISK")
        report.append("-" * 60)
        report.append(f"Users at Risk:     {churn_risk}")
        
        report.append("\n" + "=" * 60)
        
        return "\n".join(report)


def print_menu():
    """Print admin menu"""
    print("\n" + "=" * 60)
    print("🔧 ADMIN DASHBOARD MENU")
    print("=" * 60)
    print("1. View Summary Report")
    print("2. List All Users")
    print("3. List Users by Tier")
    print("4. User Statistics")
    print("5. Revenue Statistics")
    print("6. Usage Analytics")
    print("7. Churn Risk Users")
    print("8. Upgrade User")
    print("9. Downgrade User")
    print("0. Exit")
    print("=" * 60)


def main():
    """Main admin dashboard interface"""
    print("=" * 60)
    print("🔧 1-800-PHONESEX ADMIN DASHBOARD")
    print("=" * 60)
    print()
    
    dashboard = AdminDashboard()
    
    while True:
        print_menu()
        choice = input("\nSelect option: ").strip()
        
        if choice == "0":
            print("\n👋 Goodbye!\n")
            break
        
        elif choice == "1":
            print("\n" + dashboard.generate_report())
        
        elif choice == "2":
            users = dashboard.list_users_detailed()
            print(f"\n📋 ALL USERS ({len(users)} total)")
            print("-" * 60)
            for user in users:
                print(f"\nUser ID: {user['user_id']}")
                print(f"  Email: {user['email']}")
                print(f"  Tier: {user['subscription_tier'].upper()}")
                print(f"  Created: {user['created_at'][:10]}")
                print(f"  Last Login: {user['last_login'][:10] if user['last_login'] else 'Never'}")
                print(f"  Messages Today: {user['messages_today']}/{user['daily_limit'] if user['daily_limit'] != -1 else 'Unlimited'}")
        
        elif choice == "3":
            print("\nSelect tier:")
            print("1. FREE")
            print("2. PREMIUM")
            print("3. VIP")
            tier_choice = input("Choice: ").strip()
            
            tier_map = {
                "1": SubscriptionTier.FREE,
                "2": SubscriptionTier.PREMIUM,
                "3": SubscriptionTier.VIP
            }
            
            tier = tier_map.get(tier_choice)
            if tier:
                users = dashboard.list_users_detailed(tier)
                print(f"\n📋 {tier.value.upper()} USERS ({len(users)} total)")
                print("-" * 60)
                for user in users:
                    print(f"{user['email']}: {user['messages_today']} messages today")
        
        elif choice == "4":
            stats = dashboard.get_user_stats()
            print("\n📈 USER STATISTICS")
            print("-" * 60)
            print(f"Total Users:       {stats['total_users']}")
            print(f"FREE Users:        {stats['free_users']}")
            print(f"PREMIUM Users:     {stats['premium_users']}")
            print(f"VIP Users:         {stats['vip_users']}")
            print(f"Conversion Rate:   {stats['conversion_rate']:.2f}%")
        
        elif choice == "5":
            stats = dashboard.get_revenue_stats()
            print("\n💰 REVENUE STATISTICS")
            print("-" * 60)
            print(f"Monthly Recurring Revenue: ${stats['mrr']:.2f}")
            print(f"Annual Recurring Revenue:  ${stats['arr']:.2f}")
            print(f"Average Revenue Per User:  ${stats['average_revenue_per_user']:.2f}")
        
        elif choice == "6":
            stats = dashboard.get_usage_analytics()
            print("\n💬 USAGE ANALYTICS")
            print("-" * 60)
            print(f"Total Messages Today:      {stats['total_messages_today']}")
            print(f"Active Users Today:        {stats['active_users_today']}")
            print(f"Avg Messages per User:     {stats['average_messages_per_active_user']:.1f}")
        
        elif choice == "7":
            at_risk = dashboard.get_churn_risk_users()
            print(f"\n⚠️  CHURN RISK USERS ({len(at_risk)} total)")
            print("-" * 60)
            for user in at_risk:
                days_inactive = (datetime.now() - datetime.fromisoformat(user.last_login)).days
                print(f"{user.email} ({user.subscription_tier.value.upper()}) - {days_inactive} days inactive")
        
        elif choice == "8":
            email = input("\nEnter user email: ").strip()
            user = dashboard.user_manager.get_user_by_email(email)
            if not user:
                print("❌ User not found")
                continue
            
            print(f"\nCurrent tier: {user.subscription_tier.value.upper()}")
            print("\nSelect new tier:")
            print("1. FREE")
            print("2. PREMIUM")
            print("3. VIP")
            tier_choice = input("Choice: ").strip()
            
            tier_map = {
                "1": SubscriptionTier.FREE,
                "2": SubscriptionTier.PREMIUM,
                "3": SubscriptionTier.VIP
            }
            
            new_tier = tier_map.get(tier_choice)
            if new_tier:
                if dashboard.upgrade_user(user.user_id, new_tier):
                    print(f"✅ User upgraded to {new_tier.value.upper()}")
                else:
                    print("❌ Upgrade failed")
        
        elif choice == "9":
            email = input("\nEnter user email: ").strip()
            user = dashboard.user_manager.get_user_by_email(email)
            if not user:
                print("❌ User not found")
                continue
            
            print(f"\nCurrent tier: {user.subscription_tier.value.upper()}")
            print("\nSelect new tier:")
            print("1. FREE")
            print("2. PREMIUM")
            print("3. VIP")
            tier_choice = input("Choice: ").strip()
            
            tier_map = {
                "1": SubscriptionTier.FREE,
                "2": SubscriptionTier.PREMIUM,
                "3": SubscriptionTier.VIP
            }
            
            new_tier = tier_map.get(tier_choice)
            if new_tier:
                if dashboard.downgrade_user(user.user_id, new_tier):
                    print(f"✅ User changed to {new_tier.value.upper()}")
                else:
                    print("❌ Change failed")
        
        else:
            print("\n❌ Invalid option")


if __name__ == "__main__":
    # Mock API key for testing
    os.environ.setdefault('GROQ_API_KEY', 'test_key')
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting admin dashboard...\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
