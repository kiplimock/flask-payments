import os
import stripe
from flask import Flask, jsonify, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('checkout.html')

stripe.api_key = "sk_test_51HneiuAOOs5JBQO5mdMvwahOIyKJmTVp8VyNG9imGlVOTU7rxaq7FEtCKfZCF9w2dQc3xQjYD68aMzlBwDsYpPBB00WaPoaafF"


@app.route('/create-checkout-session', methods=['GET', 'POST'])
def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'T-shirt'
                    },
                    'unit_amount': 2000
                    },
                    'quantity': 1
                   }],
        mode='payment',
        success_url=url_for('success', _external=True),
        cancel_url='https://example.com/cancel'
    )

    return jsonify(id=session.id)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
