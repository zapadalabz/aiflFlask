from flask import Flask, jsonify, request
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # load environment variables from .env file

OPENAI_ENDPOINT = "https://" + os.environ.get("OPENAI_RESOURCE") + ".openai.azure.com/"

client = AzureOpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.environ.get("OPENAI_KEY"),
    api_version=os.environ.get("OPENAI_API_VERSION"),
    azure_endpoint= OPENAI_ENDPOINT,
)

deployment_name = os.environ.get("OPENAI_DEPLOYMENT")

app = Flask(__name__)

port = os.environ.get("PORT")


@app.route('/')
def hello():
    response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": "Who were the founders of Microsoft?"}
    ]
    )
    print(response.model_dump_json(indent=2))
    print(response.choices[0].message.content)
    return response.choices[0].message.content

@app.route('/postMessage', methods=['POST'])
def process_message():
    data = request.get_json()
    message = data['message']
    model = data['model']

    response = client.chat.completions.create(
        model=model,
        messages=message
    )

    print(response.model_dump_json(indent=2))
    print(response.choices[0].message.content)
    return response.choices[0].message.content


@app.route('/postPrompt/<prompt>', methods=['GET'])
def post_prompt(prompt):
    response = client.chat.completions.create(
    model=deployment_name,
    messages=[
        {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
        {"role": "user", "content": prompt}
    ]
    )
    print(response.model_dump_json(indent=2))
    print(response.choices[0].message.content)
    return response.choices[0].message.content


if __name__ == '__main__':
    app.run(port=port, debug=True)
