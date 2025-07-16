from flask import Flask, session, render_template, redirect, request
app = Flask(__name__)
import os
from forms import LoginForm, abcdForm, tradingForm, pythonMCQForm
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
    #session["authenticated"] = True
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
    
@app.route('/ceo', methods=['GET', 'POST'])
def ceo():
    session["authenticated"] = True
    if not session.get("authenticated"):
        return "Access Denied"
    from openai import OpenAI
    client = OpenAI()
    form = abcdForm()
    if not form.validate_on_submit():
        session['history'] = [{ "role": "user", "content": "Please generate a scenario where player is the CEO of a company coming under cyber attack. Initially set the background (~ 250 words) and then at each step give four possible choices (labelled A, B, C, and D) for what choices the user (as CEO) can make. Some choices should be good, while others are mistakes. After each step generate what happens next and further choices (both good and bad). The scenario and choices should be understandable by a 14 year old, if there is anything complex, provide an extra explanation. For the first round please generate a scenario title, some background information, and options for what to do, set the player's starting score (that measures how well they are managing the crisis) to 1000. For later rounds (e.g. after the player has responded for the first time) generate a text that gives the players choice, a description of what events happens (~ 150 words) next, and the again options for what to do. Update the player's score based on their choices (a score closer to 1000 indicates perfect handling, a lower score worse handling)."}]
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
 
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
@app.route('/decrypt')
def decrypt():
    def generate_random_mapping():
        import random
        alphabet = [l for l in "ABCDEFGHIJKLMNOPQRRSTUVWXYZ"]
        encrypt = alphabet[::]
        random.shuffle(encrypt)
        mapping = dict()
        for i in range(len(alphabet)):
            mapping[alphabet[i]] = encrypt[i]
        return mapping
    task = request.args.get('task')
    if task == "demo":
        plain_text = "I am a man. I see the sun and the sky. The sun is hot and bright. A dog ran to me. It is a big dog. The dog barked at a cat. The cat ran fast into a bush. I went to see the cat, but it was gone. A bird flew up into the tree and sang a short song. I stood and listened for a while.".upper()
    elif task == '1':
        plain_text = "The cat is on the mat. It is a fat cat. I see it run. It ran fast and sat on the mat. A mat is flat. The dog barked at the cat. Then the cat jumped up on a shelf. The dog sniffed the mat and wagged its tail. I laughed as the cat stared down from above. The wind blew the curtain, and the sun shone in.".upper()
    elif task == '2':
        plain_text = "You and I are at the park. The sun is up and the sky is blue. A bird flew by. It was fast and high. The wind moved the leaves on the trees. A squirrel ran across the grass and stopped to look at us. We sat on a bench and watched the ducks swim in the pond. It was calm, and I felt glad to be there with you.".upper()
    else:
        plain_text = "AAAAAAAAAA"
    return render_template('decrypt_challenge.html', plain_text = plain_text, encryption_mapping = generate_random_mapping() )
    
@app.route('/trade', methods=['GET', 'POST'])
def trade():
    form = tradingForm()
    if form.validate_on_submit():
        import csv
        import random
        with open('data/crypto_event_price_effects_50.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            row = random.choice(rows)
            event = row["Description"]
            multiplier = round(float(row["Multiplier"]),2)
        price = float(form.price.data)
        price *= multiplier
        form.price.data = round(price, 2)
    else:
        START_PRICE = 40.0
        START_AMOUNT = 1000.0
        event = f"You've just opened your crypto trading account with £{START_AMOUNT}. The current crypto price is £{START_PRICE}."
        multiplier = 1.0
        form.price.data = START_PRICE
        form.pounds.data = START_AMOUNT
        form.crypto.data = 0
    return render_template('trading.html', form=form, event=event, multiplier=multiplier)
    
@app.route('/next_word')
def next_word():
    topic = request.args.get('topic')
    if topic == "general":
        with open('data/general_sentences.txt') as file:
            texts = file.readlines()
            theme = "General"
    elif topic == "mercia":
        with open('data/mercia_sentences.txt') as file:
            texts = file.readlines()
            theme = "Mercia"
    return render_template('next_word.html', theme=theme, texts=texts)

@app.route('/python_coach', methods=['GET', 'POST'])
def python_coach():
    def random_q(topic=None):
        import csv
        import random
        with open('data/python_fstring_q.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            row = random.choice(rows)
            return row
        
    mode = request.args.get('mode')
    if mode == 'q':
        if form.validate_on_submit():
            pass
        else:
            pass
        question = random_q()
        return render_template('python_drill.html', correct="true", clarification_text="", question=question)
    elif mode == 'mcq':
        question = {"question_text": "Which of these commands is written correctly?", "answers": ["PRINT('Hello World')", "print(Hello World)", "print 'Hello World'", "print('Hello World')"], "correct": 3}
        return render_template('python_mcq.html', correct="false", clarification_text="That doesn't have the correct combination of brackets.", question=question)
    else:
        return "Bad Mode"
        
    
