from flask import Flask, session, render_template, redirect
app = Flask(__name__)
import os
from forms import LoginForm, abcdForm
from pydantic import BaseModel
from flask_session import Session
PASSWORD = os.getenv("PASSWORD")
app.secret_key = os.getenv("secret_key")
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

class FirstResponse(BaseModel):
    title: str
    background: str
    option_choices: list[str]
    score: int
    
class LaterResponse(BaseModel):
    title: str
    player_choice: str
    events: str
    option_choices: list[str]
    score: int

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get("authenticated"):
        return "Access Denied"
    from openai import OpenAI
    client = OpenAI()
    form = abcdForm()
    if not form.validate_on_submit():
        session['history'] = [{ "role": "user", "content": "Please generate a scenario where the UK is under cyber attack. The user will play the role of the UK prime minister having to make choices in response. Initially set the background (~ 250 words) and then at each step give four possible choices (labelled A, B, C, and D) for what choices the user (as PM) can make. Some choices should be good, while others are mistakes. After each step generate what happens next and further choices (both good and bad). The scenario and choices should be understandable by a 14 year old, if there is anything complex, provide an extra explanation. For the first round please generate a scenario title, some background information, and options for what to do, set the player's starting score (that measures how well they are managing the crisis) to 1000. For later rounds (e.g. after the player has responded for the first time) generate a text that gives the players choice, a description of what events happens (~ 150 words) next, and the again options for what to do. Update the player's score based on their choices (a score closer to 1000 indicates perfect handling, a lower score worse handling)."}]
        structure = FirstResponse
        session['round'] = 1
    else:
        choice = form.abcd.data
        session['round'] += 1
        if session.get('round') == 6:
            session['history'].append({"role": "user", "content": str(choice) + " (Next set of choices is final round, acknowledge at start of next set of events.)."})
        else:
            session['history'].append({"role": "user", "content": str(choice)})
        structure = LaterResponse
    response = client.responses.parse(
        model="gpt-4.1-nano",
        input=session['history'],
        text_format = structure
    )
    form.abcd.choices = list(zip(["A","B","C","D"],response.output_parsed.option_choices))
    session['history'].append({"role": "assistant", "content": response.output_parsed.json()})
    print(session['round'])
    return render_template('situation.html', info=response.output_parsed, form = form, round = session['round'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() and form.password.data == os.getenv('PASSWORD'):
        session["authenticated"] = True
        return redirect('/')
    return render_template('login.html', form=form)
