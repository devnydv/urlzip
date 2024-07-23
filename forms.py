from wtforms import Form, StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class UserForm(Form):
    username = StringField(
        'Username',
        validators=[
            DataRequired(message="Username is required."),
            Length(min=3, max=20, message="Username must be between 3 and 20 characters."),
            Regexp('^[a-zA-Z0-9]*$', message="Username must not contain special characters.")
        ]
    )
    
    email = StringField(
        'Email',
        validators=[
            DataRequired(message="Email is required."),
            Email(message="Invalid email address.")
        ]
    )
    
    short_note = TextAreaField(
        'Short Note',
        validators=[
            Length(max=300, message="Short note must be less than 300 characters.")
        ]
    )
    
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, max=14, message="Password must be more than 6 and less than 14 characters.")
        ]
    )
    
    confirm_password = PasswordField(
        'Confirm-Password',
        validators=[
            DataRequired(message="Please confirm your password."),
            EqualTo('password', message="Passwords must match.")
        ]
    )