import os

from flask import Flask, jsonify, request
from openai import OpenAI

# Initialize Flask and set a secret key.
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# Load your OpenAI API key from an environment variable or secret file.
openai_api_key = os.getenv('OPENAI_API_KEY')
# openai.organization = 'your_openai_org_id_here'
# openai.api_key = openai_api_key
client = OpenAI(api_key=openai_api_key)


@app.route('/')
def index():
  return 'Hello, world!'


# Define a route for the weather chatbot.
@app.route('/chat', methods=['POST'])
def chat():
  user_message = request.json.get('message', '')

  try:
    # Call OpenAI API to get the chatbot's response.
    # response = openai.Completion.create(engine="davinci",
    #                                     prompt=user_message,
    #                                     max_tokens=150)
    response = client.chat.completions.create(messages=[{
        "role": "user",
        "content": user_message
    }],
                                              model="gpt-4-1106-preview")
    # The response object is a ChatCompletion object. You need to access its attributes.
    # Access the first choice's text directly.
    message_content = response.choices[0].message.content
    # Return the message content as JSON.
    return jsonify({'response': message_content})
  except Exception as e:
    # Handle errors while calling the OpenAI API.
    return jsonify({'error': str(e)}), 500


# Run the Flask app.
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
