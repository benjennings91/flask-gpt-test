from flask import Flask, session, render_template
app = Flask(__name__)
import os
from forms import LoginForm
PASSWORD = os.getenv("PASSWORD")
app.secret_key = os.getenv("secret_key")

@app.route('/')
def index():
    from openai import OpenAI
    if session["authenticated"]:
        client = OpenAI()

        response = client.responses.create(
            model="gpt-4.1",
            input="Write a one-sentence description of AI."
        )

        return response.output_text
    else:
        return "Access Denied"

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', form=form)
