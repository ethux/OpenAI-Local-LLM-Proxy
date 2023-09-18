from flask import Flask, request, jsonify, abort
import uuid
import time
import os
from datetime import datetime
from modules import openllmapi, textgenapi
from flask_cors import CORS
from dotenv import load_dotenv

API_PROVIDER = os.environ['API_PROVIDER']

app = Flask(__name__)
CORS(app)

load_dotenv()

@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    if not request.json or not 'messages' in request.json:
        abort(400)
    
    authorization = request.headers['Authorization']
    messages = request.json['messages']
    model = request.json['model']
    
    if API_PROVIDER == 'OpenLLM':
        response = openllmapi.chat(messages)
    elif API_PROVIDER == 'TextGenUI':
        response = textgenapi.pipeline(messages)
    else:
        abort(400)
    
    assistant_reply = response
    response = {
        "id": "chatcmpl-" + str(uuid.uuid4()),
        "object": "chat.completion",
        "created":  int(time.time()),
        "model": model,
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": assistant_reply,
                },
                "finish_reason": "stop",
                "index": "0",
            }
        ],
        "usage": {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0
        },
    }

    return jsonify(response)



#@app.route('/v1/embeddings', methods=['POST'])


#@app.route('/v1/completions', methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, port=8000)