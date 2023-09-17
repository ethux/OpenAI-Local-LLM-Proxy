import os
import openllm
from modules.prompt import Prompt
from dotenv import load_dotenv
load_dotenv()

class Pipeline:
    def chat(messages):
            output_msg = Prompt.prepare(messages)
            print(output_msg)
            client = openllm.client.HTTPClient(os.environ['API_URL'])
            response = client.query(output_msg)
            return response