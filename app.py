from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    from openai import OpenAI
    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1",
        input="Write a one-sentence description of AI."
    )

    return response.output_text
