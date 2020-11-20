import os
import stripe
from flask import Flask, render_template, url_for, jsonify, request, abort

app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51HneiuAOOs5JBQO5XW5hY2wFqvLhuDlOWrjqSZ8ypbGC6sFSh2nBoCydEiwSDAzvScispC3gR5dMpo4T2jayHz0b004dOBHGZ6'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51HneiuAOOs5JBQO5mdMvwahOIyKJmTVp8VyNG9imGlVOTU7rxaq7FEtCKfZCF9w2dQc3xQjYD68aMzlBwDsYpPBB00WaPoaafF'

stripe.api_key = app.config['STRIPE_SECRET_KEY']


@app.route('/')
def index():
    '''
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1GtKWtIdX0gthvYPm4fJgrOr',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    '''
    return render_template(
        'checkout.html',
        #checkout_session_id=session['id'],
        #checkout_public_key=app.config['STRIPE_PUBLIC_KEY']
    )


@app.route('/stripe-pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1Ho2YfAOOs5JBQO5WAha5556',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index', _external=True),
    )
    return {
        'checkout_session_id': session['id'],
        'checkout_public_key': app.config['STRIPE_PUBLIC_KEY']
    }


@app.route('/thanks')
def thanks():
    return render_template('success.html')


@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_e5bQ2kotM90U6lrVMDKzt5wbopw7dJG2'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])

    return {}

if __name__ == '__main__':
    app.run(debug=True)
