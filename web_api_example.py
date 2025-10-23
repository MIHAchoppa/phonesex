#!/usr/bin/env python3
"""
Example Web API for 1-800-PHONESEX
Demonstrates how to integrate monetization features into a web service
This is a simple Flask-based API example.
"""

# NOTE: This is an example/template. To use it, install Flask:
# pip install flask flask-cors

"""
Example Flask API implementation:

from flask import Flask, request, jsonify
from flask_cors import CORS
import os

from user_manager import UserManager, FeatureGate
from payments import PaymentProcessor, SubscriptionTier, UsageTracker

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize services
user_manager = UserManager()
payment_processor = PaymentProcessor()
usage_tracker = UsageTracker()


@app.route('/api/health', methods=['GET'])
def health_check():
    '''Health check endpoint'''
    return jsonify({
        'status': 'healthy',
        'service': '1-800-PHONESEX API',
        'version': '1.0.0'
    })


@app.route('/api/auth/register', methods=['POST'])
def register():
    '''Register a new user'''
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    try:
        user = user_manager.create_user(email, SubscriptionTier.FREE)
        session_token = user_manager.create_session(user.user_id)
        
        return jsonify({
            'user_id': user.user_id,
            'email': user.email,
            'subscription_tier': user.subscription_tier.value,
            'session_token': session_token
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/auth/login', methods=['POST'])
def login():
    '''Login existing user'''
    data = request.json
    email = data.get('email')
    
    if not email:
        return jsonify({'error': 'Email required'}), 400
    
    user = user_manager.get_user_by_email(email)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    session_token = user_manager.create_session(user.user_id)
    
    return jsonify({
        'user_id': user.user_id,
        'email': user.email,
        'subscription_tier': user.subscription_tier.value,
        'session_token': session_token
    })


@app.route('/api/user/profile', methods=['GET'])
def get_profile():
    '''Get user profile'''
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not session_token:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = user_manager.validate_session(session_token)
    if not user_id:
        return jsonify({'error': 'Invalid session'}), 401
    
    user = user_manager.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    usage_today = usage_tracker.get_usage(user_id)
    
    return jsonify({
        'user_id': user.user_id,
        'email': user.email,
        'subscription_tier': user.subscription_tier.value,
        'created_at': user.created_at,
        'last_login': user.last_login,
        'features': user.get_features(),
        'usage_today': usage_today,
        'daily_limit': user.get_daily_message_limit()
    })


@app.route('/api/subscription/plans', methods=['GET'])
def get_plans():
    '''Get available subscription plans'''
    from payments import compare_plans
    
    plans = compare_plans()
    return jsonify({'plans': plans})


@app.route('/api/subscription/create', methods=['POST'])
def create_subscription():
    '''Create a new subscription'''
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    data = request.json
    
    if not session_token:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = user_manager.validate_session(session_token)
    if not user_id:
        return jsonify({'error': 'Invalid session'}), 401
    
    user = user_manager.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Get subscription tier from request
    tier_str = data.get('tier', 'premium').lower()
    try:
        tier = SubscriptionTier(tier_str)
    except ValueError:
        return jsonify({'error': 'Invalid subscription tier'}), 400
    
    # Create customer and subscription
    customer = payment_processor.create_customer(user.email)
    subscription = payment_processor.create_subscription(customer['id'], tier)
    
    # Update user
    user_manager.update_subscription(
        user_id,
        tier,
        customer_id=customer['id'],
        subscription_id=subscription['id']
    )
    
    return jsonify({
        'subscription_id': subscription['id'],
        'tier': tier.value,
        'status': subscription['status']
    }), 201


@app.route('/api/subscription/cancel', methods=['POST'])
def cancel_subscription():
    '''Cancel user subscription'''
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not session_token:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = user_manager.validate_session(session_token)
    if not user_id:
        return jsonify({'error': 'Invalid session'}), 401
    
    user = user_manager.get_user(user_id)
    if not user or not user.subscription_id:
        return jsonify({'error': 'No active subscription'}), 400
    
    # Cancel subscription
    result = payment_processor.cancel_subscription(user.subscription_id)
    
    # Downgrade to free
    user_manager.update_subscription(user_id, SubscriptionTier.FREE)
    
    return jsonify({
        'status': 'canceled',
        'canceled_at': result.get('canceled_at')
    })


@app.route('/api/chat/message', methods=['POST'])
def send_message():
    '''Send a chat message (with usage tracking)'''
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    data = request.json
    
    if not session_token:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = user_manager.validate_session(session_token)
    if not user_id:
        return jsonify({'error': 'Invalid session'}), 401
    
    user = user_manager.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check usage limits
    current_usage = usage_tracker.get_usage(user_id)
    if not FeatureGate.check_message_limit(user, current_usage):
        return jsonify({
            'error': 'Daily message limit reached',
            'upgrade_url': '/upgrade'
        }), 429
    
    # Track message
    usage_tracker.track_message(user_id)
    
    message = data.get('message', '')
    personality = data.get('personality', 'Flirty')
    
    # Check personality access
    if not FeatureGate.check_personality_access(user, personality):
        return jsonify({
            'error': f'Access to {personality} requires Premium or VIP',
            'upgrade_url': '/upgrade'
        }), 403
    
    # Here you would integrate with actual chatline.py
    # For demo purposes, return mock response
    return jsonify({
        'response': f'Mock response from {personality} personality',
        'personality': personality,
        'streaming': FeatureGate.check_streaming_access(user),
        'messages_remaining': user.get_daily_message_limit() - current_usage - 1
    })


@app.route('/api/webhook/stripe', methods=['POST'])
def stripe_webhook():
    '''Handle Stripe webhook events'''
    payload = request.data
    signature = request.headers.get('Stripe-Signature')
    
    try:
        result = payment_processor.process_webhook(payload, signature)
        
        # Handle different event types
        if result.get('event_type') == 'subscription_created':
            # Update user subscription status
            pass
        elif result.get('event_type') == 'subscription_deleted':
            # Downgrade user to free
            pass
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    '''Get admin statistics (requires admin authentication)'''
    # In production, add proper admin authentication
    api_key = request.headers.get('X-Admin-Key')
    if api_key != os.getenv('ADMIN_API_KEY'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    from admin_dashboard import AdminDashboard
    dashboard = AdminDashboard()
    
    return jsonify({
        'user_stats': dashboard.get_user_stats(),
        'revenue_stats': dashboard.get_revenue_stats(),
        'usage_stats': dashboard.get_usage_analytics()
    })


if __name__ == '__main__':
    # Set GROQ_API_KEY for testing
    os.environ.setdefault('GROQ_API_KEY', 'test_key')
    
    print('Starting 1-800-PHONESEX API...')
    print('Monetization features enabled')
    print('API available at: http://localhost:5000')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
"""

print(__doc__)
print("\nTo use this API:")
print("1. Install Flask: pip install flask flask-cors")
print("2. Uncomment the code above")
print("3. Run: python web_api_example.py")
print("4. API will be available at http://localhost:5000")
print("\nAPI Endpoints:")
print("  POST /api/auth/register - Register new user")
print("  POST /api/auth/login - Login user")
print("  GET  /api/user/profile - Get user profile")
print("  GET  /api/subscription/plans - List subscription plans")
print("  POST /api/subscription/create - Create subscription")
print("  POST /api/subscription/cancel - Cancel subscription")
print("  POST /api/chat/message - Send chat message")
print("  POST /api/webhook/stripe - Stripe webhook handler")
print("  GET  /api/admin/stats - Admin statistics")
