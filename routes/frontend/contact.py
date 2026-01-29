from app import app, render_template
import requests
from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_wtf import FlaskForm
@app.route('/contact')
def contact():
    form = FlaskForm()
    return render_template('frontend/contact.html', form=form)

token = '8427622540:AAHL6RawAHwLCQWqBNEbndZQU3FOIrlxvXo'
chat_id = "@chanrathan_bot"
user_agent = 'Rathana Telegram Bot With Python'

def sendSMS(token: str, chat_id: str, text: str):
    """Send message via Telegram bot"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "text": text,
        "chat_id": chat_id,
        "disable_notification": False,
        "parse_mode": "HTML"
    }
    headers = {
        "accept": "application/json",
        "User-Agent": user_agent,
        "content-type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}


@app.route('/send', methods=['POST'])
def send():
    email = request.form.get('email')
    message = request.form.get('msg')

    # Basic validation
    if not email or not message:
        flash('Please fill in all fields correctly.', 'error')
        return redirect(url_for('contact'))

    # Format message for Telegram (HTML format)
    telegram_message = f"""
📧 New Contact Form Submission
Email: {email}
Message: {message}
""".strip()

    # Send to Telegram
    result = sendSMS(token, chat_id, telegram_message)

    if result and result.get('ok'):
        flash('Thank you! Your message has been sent successfully.', 'success')
    else:
        flash('Sorry, there was an error sending your message. Please try again.', 'error')

    return redirect(url_for('contact'))
