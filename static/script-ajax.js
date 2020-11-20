const button = document.querySelector('#checkout-button');

button.addEventListener('click', event => {
    fetch('/stripe-pay')
        .then((result) => { return result.json(); })
        .then((data) => {
            var stripe = Stripe(data.checkout_public_key);
            stripe.redirectToCheckout({
            // ----------------------------
            // ----------------------------
            // ----------------------------
            sessionId: data.checkout_session_id
        }).then(function (result) {
            // ----------------------------
            // ----------------------------
            // ----------------------------
        });
    })
});