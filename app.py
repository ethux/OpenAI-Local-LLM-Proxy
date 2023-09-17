from flask import Flask, request, jsonify, abort
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from modules import openllmapi, prompt, textgenapi
from flask_cors import CORS
import os
from dotenv import load_dotenv

API_PROVIDER = os.environ['API_PROVIDER']

app = Flask(__name__)
CORS(app)

load_dotenv()

@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    if not request.json or not 'messages' in request.json:
        abort(400)
    #content = request.headers('Content-Type')
    authorization = request.headers['Authorization']
    messages = request.json['messages']
    model = request.json['model']
    if API_PROVIDER == 'OpenLLM':
        response = openllmapi.Pipeline.chat(messages)
    elif API_PROVIDER == 'TextGenUI':
        response = textgenapi.pipeline(messages)
    else:
        abort(400)
    
    return jsonify(response)

#@app.route('/v1/embeddings', methods=['POST'])


#@app.route('/v1/completions', methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, port=8000)