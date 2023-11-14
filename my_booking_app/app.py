# app.py

from flask import Flask, render_template, redirect, url_for, flash
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectMultipleField, BooleanField
from wtforms.validators import DataRequired, Email
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import Config  # Ensure this line is correct
from models import db, Booking


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)

class BookingForm(FlaskForm):
    service_types = [('FOOTBALL', 'Football'), ('BASKETBALL', 'Basketball'), ('GOLF', 'Golf'), ('THE CAGE', 'The Cage'), ('LEISURE', 'Leisure')]
    service_type = SelectMultipleField('Service Type', choices=service_types, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField('Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    agree_to_terms = BooleanField('Agree to Terms and Conditions', validators=[DataRequired()])

@app.route('/')
def home():
    # Query all bookings from the database
    bookings = Booking.query.all()
    return render_template('home.html', bookings=bookings)

@app.route('/book-now', methods=['GET', 'POST'])
def book_now():
    form = BookingForm()

    if form.validate_on_submit():
        selected_service_types = ', '.join(form.service_type.data)

        if is_date_available(form.date.data, selected_service_types):
            booking = Booking(
                service_type=selected_service_types,
                date=form.date.data,
                email=form.email.data,
                name=form.name.data,
                phone_number=form.phone_number.data
            )
            db.session.add(booking)
            db.session.commit()

            flash('Booking successful!', 'success')

            # Send confirmation email
            send_confirmation_email(booking.email, booking.service_type, booking.date, booking.name)

            # Send notification to admin
            send_notification_to_admin(booking)

            return redirect(url_for('payment_gateway'))

        else:
            flash('This date is not available. Please select another date.', 'error')

    return render_template('book_now.html', form=form)

def is_date_available(selected_date, selected_service_types):
    # Add logic to check if the selected date is available for the chosen service types
    # You need to query your database to check availability
    # Replace the logic below with your actual implementation
    return True  # Placeholder, replace with your actual logic

@app.route('/payment-gateway')
def payment_gateway():
    # Implement Paystack integration here
    # After successful payment, update booking.payment_confirmed and send notification to admin
    # Example: call_paystack_integration_function(booking_id)
    return render_template('payment_gateway.html')

def send_confirmation_email(email, service_type, date, name):
    msg = Message('Booking Confirmation', sender='your_email@example.com', recipients=[email])
    msg.body = f'Thank you, {name}, for booking with us!\n\nService Types: {service_type}\nDate: {date}\n\nYour booking is confirmed.'
    mail.send(msg)

def send_notification_to_admin(booking):
    # Add logic to send notification to admin
    pass  # Replace this with your actual admin notification logic

if __name__ == '__main__':
    print("Starting the Flask app...")
    app.run(debug=True, port=5001)

