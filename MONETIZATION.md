# 💳 Monetization Features Guide

## Overview

1-800-PHONESEX now includes comprehensive monetization features with payment processing, subscription management, and premium user features.

## Subscription Tiers

### 🆓 FREE
- **Price**: $0/month
- **Messages**: 10 per day
- **Operators**: Flirty only
- **Streaming**: No (standard responses)
- **Support**: Community support
- **Custom Personalities**: No

Perfect for trying out the service and getting a taste of what's available.

### 💎 PREMIUM - $9.99/month
- **Messages**: 100 per day
- **Operators**: All 5 (Flirty, Romantic, Adventurous, Mysterious, Playful)
- **Streaming**: Yes (real-time responses)
- **Support**: Priority email support
- **Custom Personalities**: No

Ideal for regular users who want the full experience with all operators and unlimited streaming.

### 👑 VIP - $29.99/month
- **Messages**: Unlimited
- **Operators**: All 5 plus custom personalities
- **Streaming**: Yes (real-time responses)
- **Support**: Priority 24/7 support
- **Custom Personalities**: Yes (3 custom slots)

The ultimate experience for power users who want unlimited access and the ability to create their own custom operators.

## Features

### Payment Processing
- Secure Stripe integration
- Support for credit cards, debit cards, and digital wallets
- Automatic recurring billing
- Easy subscription management
- Instant payment confirmation
- Webhook support for real-time updates

### User Management
- Secure user authentication
- Session management
- Profile management
- Subscription history tracking
- Usage statistics

### Usage Tracking
- Real-time message counting
- Daily limit enforcement
- Historical usage data
- Analytics and insights

### Feature Gating
- Intelligent feature access control
- Automatic tier-based restrictions
- Upgrade prompts when accessing premium features
- Seamless upgrade experience

## Installation & Configuration

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `.env.example` to `.env` and configure:

```bash
# GROQ API (Required)
GROQ_API_KEY=your_groq_api_key_here

# Stripe Payment Processing (Optional for monetization)
STRIPE_API_KEY=your_stripe_api_key_here
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret_here
STRIPE_TEST_MODE=true

# User Data Storage
USER_DATA_DIR=./user_data
```

### 3. Get Your API Keys

#### GROQ API Key (Required)
1. Visit https://console.groq.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy to your `.env` file

#### Stripe API Keys (Optional - for payments)
1. Visit https://dashboard.stripe.com/
2. Sign up or log in
3. Get your API keys from Developers > API keys
4. For testing, use test mode keys
5. For production, use live mode keys
6. Copy to your `.env` file

## Usage

### Running the Application
```bash
python chatline.py
```

### New Commands
- `/plans` - View all subscription plans
- `/upgrade` - Get upgrade information
- `/stats` - View usage statistics (now includes subscription info)

### Example Session with Monetization
```
🔥 1-800-PHONESEX - Your Late Night Fantasy Line 🔥
💋 Welcome to the hottest AI phone sex experience!
📞 Connected to: Flirty
💳 Current Plan: FREE

You: /plans

💳 SUBSCRIPTION PLANS
============================================================

🔥 FREE - $0.00/month
   Try the basic experience - 10 messages per day with Flirty personality
   
   Features:
   • 10 messages per day
   • Operators: Flirty
   • Streaming: ✗
   • Priority Support: ✗
   • Custom Personalities: ✗

🔥 PREMIUM - $9.99/month
   Full access to all 5 operators with unlimited streaming - 100 messages/day
   
   Features:
   • 100 messages per day
   • Operators: Flirty, Romantic, Adventurous, Mysterious, Playful
   • Streaming: ✓
   • Priority Support: ✓
   • Custom Personalities: ✗

🔥 VIP - $29.99/month
   Ultimate experience - unlimited messages, all operators, custom personalities
   
   Features:
   • Unlimited messages per day
   • Operators: Flirty, Romantic, Adventurous, Mysterious, Playful
   • Streaming: ✓
   • Priority Support: ✓
   • Custom Personalities: ✓

You: /personalities

💋 Choose Your Operator:
  💋 1. Flirty - Sultry seduction specialist
  ❤️  2. Romantic - Passionate lover with X-rated intensity 🔒
  🔥 3. Adventurous - Kinky fantasy expert 🔒
  🌙 4. Mysterious - Enigmatic late-night seductress 🔒
  😈 5. Playful - Naughty tease with dirty mind 🔒

  ★ Currently talking to: Flirty

You: /stats

🔥 Your Session Stats:
  Exchanges: 3
  Operator: Flirty
  Line: llama-3.1-70b-versatile

💳 Subscription Info:
  Plan: FREE
  Messages Today: 3/10
```

## API Reference

### Payment Module (`payments.py`)

#### SubscriptionTier
```python
class SubscriptionTier(Enum):
    FREE = "free"
    PREMIUM = "premium"
    VIP = "vip"
```

#### PaymentProcessor
```python
processor = PaymentProcessor(api_key="sk_test_...")

# Create customer
customer = processor.create_customer(email="user@example.com")

# Create subscription
subscription = processor.create_subscription(
    customer_id=customer['id'],
    plan=SubscriptionTier.PREMIUM
)

# Create one-time payment
payment = processor.create_payment_intent(
    amount=9.99,
    currency="usd",
    customer_id=customer['id']
)

# Cancel subscription
result = processor.cancel_subscription(subscription_id)

# Process webhook
result = processor.process_webhook(payload, signature)
```

#### UsageTracker
```python
tracker = UsageTracker()

# Track a message
tracker.track_message(user_id="user123")

# Get usage
usage = tracker.get_usage(user_id="user123")

# Check limit
within_limit = tracker.check_limit(user_id="user123", limit=10)

# Reset usage
tracker.reset_usage(user_id="user123")
```

### User Management Module (`user_manager.py`)

#### User
```python
user = User(
    user_id="user123",
    email="user@example.com",
    subscription_tier=SubscriptionTier.PREMIUM
)

# Get features
features = user.get_features()

# Check personality access
can_access = user.can_access_personality("Romantic")

# Get message limit
limit = user.get_daily_message_limit()

# Check streaming access
has_streaming = user.has_streaming()
```

#### UserManager
```python
manager = UserManager(data_dir="./user_data")

# Create user
user = manager.create_user(
    email="user@example.com",
    subscription_tier=SubscriptionTier.FREE
)

# Get user
user = manager.get_user(user_id="user123")
user = manager.get_user_by_email("user@example.com")

# Update subscription
manager.update_subscription(
    user_id="user123",
    subscription_tier=SubscriptionTier.PREMIUM,
    customer_id="cus_...",
    subscription_id="sub_..."
)

# Session management
token = manager.create_session(user_id="user123")
user_id = manager.validate_session(token)
manager.end_session(token)

# List users
all_users = manager.list_users()
premium_users = manager.list_users(SubscriptionTier.PREMIUM)
count = manager.get_user_count()
```

#### FeatureGate
```python
# Check personality access
can_access = FeatureGate.check_personality_access(user, "Romantic")

# Check streaming access
has_streaming = FeatureGate.check_streaming_access(user)

# Check message limit
within_limit = FeatureGate.check_message_limit(user, current_usage=5)

# Get upgrade prompt
prompt = FeatureGate.get_upgrade_prompt(user, "personality")
```

## Webhook Integration

### Setting Up Webhooks

1. **Configure Stripe Webhook Endpoint**
   - Go to Stripe Dashboard > Developers > Webhooks
   - Add endpoint: `https://yourdomain.com/webhook/stripe`
   - Select events to listen for

2. **Handle Webhook Events**
```python
from payments import PaymentProcessor

processor = PaymentProcessor()

# In your webhook handler
@app.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.data
    signature = request.headers.get('Stripe-Signature')
    
    result = processor.process_webhook(payload, signature)
    return jsonify(result), 200
```

### Supported Events
- `payment_intent.succeeded` - Payment completed successfully
- `payment_intent.failed` - Payment failed
- `customer.subscription.created` - New subscription created
- `customer.subscription.updated` - Subscription modified
- `customer.subscription.deleted` - Subscription canceled

## Testing

### Run All Tests
```bash
# Test monetization features
python test_monetization.py

# Test original chatline features
python test_chatline.py
```

### Test Coverage
- ✅ Subscription plan configurations
- ✅ Payment processing (customer, subscriptions, payments)
- ✅ Usage tracking and limits
- ✅ User creation and management
- ✅ Feature access control
- ✅ Session management
- ✅ Webhook processing

## Security Considerations

### API Keys
- Never commit API keys to version control
- Use environment variables for all sensitive data
- Rotate keys regularly
- Use test mode keys for development

### User Data
- User data stored in `./user_data/` directory
- Directory is gitignored by default
- Contains user profiles and sessions
- Back up regularly
- Consider encryption for production

### Payment Security
- All payment processing handled by Stripe
- PCI DSS compliant
- No credit card data stored locally
- Secure webhook signature verification

## Production Deployment

### Requirements
- Python 3.8+
- GROQ API key
- Stripe account (for payments)
- SSL certificate (for webhooks)
- Secure server environment

### Checklist
- [ ] Set all environment variables
- [ ] Configure production Stripe keys
- [ ] Set up webhook endpoints
- [ ] Configure SSL/TLS
- [ ] Set up user data backup
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Test all payment flows
- [ ] Verify webhook signatures
- [ ] Set STRIPE_TEST_MODE=false

## Support

### For Users
- Email: support@1800phonesex.example.com
- Free users: Community forum
- Premium users: Priority email (24-48h response)
- VIP users: Priority 24/7 support

### For Developers
- GitHub Issues: https://github.com/MIHAchoppa/phonesex/issues
- Documentation: This file
- API Reference: See above
- GROQ Docs: https://console.groq.com/docs
- Stripe Docs: https://stripe.com/docs/api

## Roadmap

Future enhancements planned:
- [ ] Web dashboard for subscription management
- [ ] Mobile app integration
- [ ] Annual subscription discounts
- [ ] Referral program
- [ ] Team/family plans
- [ ] Gift subscriptions
- [ ] Analytics dashboard for users
- [ ] Advanced usage reports
- [ ] Multi-currency support
- [ ] International payment methods

## License

This monetization system is part of the 1-800-PHONESEX project and follows the same license terms.

⚠️ **CONTENT WARNING**: This application contains explicit adult content. 18+ only.
