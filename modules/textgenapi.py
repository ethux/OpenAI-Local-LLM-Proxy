import json
import requests
import os
from modules.prompt import Prompt
from dotenv import load_dotenv

load_dotenv()

# For local streaming, the websockets are hosted without ssl - http://
#HOST = 'localhost:5000'

HOST = os.environ['API_URL']
URI = f'{HOST}/api/v1/chat'

def pipeline(messages, max_new_tokens=100):
    output_msg = Prompt.prepare(messages)
    print(output_msg)

    request = {
        'user_input': output_msg,
        'max_new_tokens': max_new_tokens,
        'auto_max_new_tokens': False,
        #'history': history,
        'mode': 'instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
        #'character': 'Example',
        #'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
        #'your_name': 'USER',
        # 'name1': 'name of user', # Optional
        # 'name2': 'name of character', # Optional
        #'context': template, # Optional
        #'greeting': 'Thank you for asking!', # Optional
        # 'name1_instruct': 'You', # Optional
        # 'name2_instruct': 'Assistant', # Optional
        #'context_instruct': template, # Optional
        # 'turn_template': 'turn_template', # Optional
        'regenerate': False,
        '_continue': False,
        'stop_at_newline': False,
        'chat_generation_attempts': 1,
        'chat_instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.1,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'guidance_scale': 1,
        'negative_prompt': '',

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    response = requests.post(URI, json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['history']
        print(json.dumps(result, indent=4))
        print()
        print(result['visible'][-1][1])
    else:
        print(response.status_code)
        print(response.text)
    answer = result['visible'][-1][1]
    return answer