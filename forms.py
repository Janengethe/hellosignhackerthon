#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo
from wtforms.validators import Email, ValidationError


from database import storage


class RegisterForm(FlaskForm):
    agent_no = StringField(
        validators=[InputRequired(), Length(1, 10)],
        render_kw={"placeholder": "Agent Number"})
    agent_name = StringField(
        validators=[InputRequired(), Length(1, 100)],
        render_kw={"placeholder": "Agent Name"})
    api_key = StringField(
        validators=[InputRequired(), Length(1, 250)],
        render_kw={"placeholder": "HelloSign API Key"})
    password = PasswordField(
        validators=[InputRequired(), Length(min=6, max=20)],
        render_kw={"placeholder": "Password"})
    submit = SubmitField("Sign Up")
    
    def validate_agent(self, agent_no):
        agent = storage.get_agent_by_no(agent_no.data)
        if agent:
            raise ValidationError("Agent Number Already registered!")
        return

class LoginForm(FlaskForm):
    agent_no = StringField(
        validators=[InputRequired(), Length(1, 10)],
        render_kw={"placeholder": "Agent Number"})
    password = PasswordField(
        validators=[InputRequired(), Length(min=6, max=20)],
        render_kw={"placeholder": "Password"})
    submit = SubmitField("Sign In")