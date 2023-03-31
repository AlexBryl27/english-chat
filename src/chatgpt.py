import requests
import json
# import openai
import os


class ChatGPTEngine:

    def __init__(self):

        key = os.environ['OPENAI_API_KEY']

        self.url = "https://api.openai.com/v1/chat/completions"
        self.session = requests.Session()
        self.session.auth = ("Bearer", key)
        self.query = {
            "model": "gpt-3.5-turbo",
            "messages": [],
            "temperature": 0.8
        }

    def process(self, message: str, role: str = "user") -> str:

        self.query['messages'].append({"role": role, "content": message})
        response = self.session.post(self.url, json=self.query)
        if response.status_code == 200:
            reply = json.loads(response.text)['choices'][0]['message']['content']
            self.query['messages'].append({"role": "assistant", "content": reply})
            return reply

        return f"Something went wrong. {response.text}"

    def reset(self) -> None:

        self.query['messages'] = []

        return
