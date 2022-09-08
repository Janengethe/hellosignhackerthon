#!/usr/bin/env python3

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import InputRequired, DataRequired, Length, EqualTo
from wtforms.validators import Email, ValidationError


from msahihi.database import storage


class RegisterForm(FlaskForm):
    agent_no = StringField(
        validators=[InputRequired(), Length(1, 10)],
        render_kw={"placeholder": "Agent Number"})
    agent_name = StringField(
        validators=[InputRequired(), Length(1, 100)],
        render_kw={"placeholder": "Agent Name"})
    email = StringField(
        validators=[InputRequired(), Length(1, 250)],
        render_kw={"placeholder": "Email"})
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

class TrnsctnForm(FlaskForm):
    national_id = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "National ID"})
    txn_type =   StringField(
        validators=[InputRequired(), Length(1)],
        render_kw={"placeholder": "Transaction Type"})
    value = IntegerField(
        validators=[InputRequired()],
        render_kw={"placeholder": "Value"})
    txn_id = StringField(
        validators=[InputRequired()],
        render_kw={"placeholder": "Transaction ID"})
    submit = SubmitField("Save Customer")
