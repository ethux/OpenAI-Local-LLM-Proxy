from flask import Flask, request, jsonify, abort
import uuid
import time
import os
from datetime import datetime
from modules import openllmapi, textgenapi, embeddings
from flask_cors import CORS
from dotenv import load_dotenv

API_PROVIDER = os.environ['API_PROVIDER']

app = Flask(__name__)
CORS(app)

load_dotenv()

@app.route('/v1/chat/completions', methods=['POST'])
def chat():
    authorization = request.headers['Authorization'] #Not used yet
    messages = request.json['messages']
    model = request.json['model']
    
    if API_PROVIDER == 'OpenLLM':
        response = openllmapi.chat(messages)
    elif API_PROVIDER == 'TextGenUI':
        response = textgenapi.pipeline(messages)
    else:
        abort(400)
    
    assistant_reply = response
    print(assistant_reply)
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



@app.route('/v1/embeddings', methods=['POST'])
def embedding():
    if not request.json or not 'messages' in request.json:
        abort(400)
    sentences = request.json['messages']
    output = embeddings.embeddings(sentences)
    return (output) #Output needs to be changed to right format


#@app.route('/v1/completions', methods=['POST'])


@app.route('/v1/models', methods=['GET'])
def models():
    response = {
        "object": "list",
        "data": [
            {
                "id": "gpt-4-0613",
                "object": "model",
                "created": 0,
                "owned_by": "openai",
                "permission": [
                    {
                        "id": "modelperm-0",
                        "object": "model_permission",
                        "created": 0,
                        "allow_create_engine": False,
                        "allow_sampling": False,
                        "allow_logprobs": False,
                        "allow_search_indices": False,
                        "allow_view": False,
                        "allow_fine_tuning": False,
                        "organization": "*",
                        "group": None,
                        "is_blocking": False
                    }
                ],
                "root": "gpt-4-0613",
                "parent": None
            },
            {
                "id": "gpt-3.5-turbo-0613",
                "object": "model",
                "created": 0,
                "owned_by": "openai",
                "permission": [
                    {
                        "id": "modelperm-0",
                        "object": "model_permission",
                        "created": 0,
                        "allow_create_engine": False,
                        "allow_sampling": True,
                        "allow_logprobs": True,
                        "allow_search_indices": False,
                        "allow_view": True,
                        "allow_fine_tuning": False,
                        "organization": "*",
                        "group": None,
                        "is_blocking": False
                    }
                ],
                "root": "gpt-3.5-turbo-0613",
                "parent": None
            }
        ]
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, port=8000)