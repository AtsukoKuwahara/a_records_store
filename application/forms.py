from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from application.model import User

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=6, max=15), EqualTo('password')])
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=55)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=55)])
    submit = SubmitField("Register Now")

    def validate_email(self, email):
        """
        Custom validator to check if the email is already registered.
        :param email: Email field data
        :raises ValidationError: If the email is already in use
        """
        user = User.objects(email=email.data).first()
        if user:
            raise ValidationError("Email is already in use. Pick another one.")

class CheckoutForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=55)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=55)])
    address = StringField("Address", validators=[DataRequired(), Length(min=5, max=100)])
    city = StringField("City", validators=[DataRequired(), Length(min=2, max=50)])
    province = StringField("Province", validators=[DataRequired(), Length(min=2, max=50)])
    postal_code = StringField("Postal Code", validators=[DataRequired(), Length(min=5, max=10)])
    credit_card_number = StringField("Credit Card Number", validators=[DataRequired(), Length(min=16, max=19)])
    expiry_date = StringField("Expiry Date (MM/YY)", validators=[DataRequired(), Length(min=5, max=5)])
    cvv = IntegerField("CVV", validators=[DataRequired(), NumberRange(min=100, max=999)])
    submit = SubmitField("Place Order")
