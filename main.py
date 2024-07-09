from agent.model import OpenAIAPI
from agent.tools import run_tools
from agent.config import prompt, tools

import os

API_KEY = os.getenv('API_KEY')
API_URL = os.getenv('API_URL')

WORKER_DIRECTORY = os.path.join(os.getcwd(), "worker")

def run():
    messages = [{"role": "system", "content": prompt}]
    api = OpenAIAPI(API_KEY, API_URL)

    while True:
        user_input = input("👤: ")
        messages.append({"role": "user", "content": user_input})
        while True:
            response = api.oneapi(messages, model="gpt-4o", tools=tools, choices="auto", response_format=None)
            if response['type'] == 'message':
                response_message = response['message']
                print("🤖:", response_message)
                messages.append({"role": "assistant", "content": response_message})
                break  
            elif response['type'] == 'tools':
                messages.append(response['message'])
                tool_calls = response['tools']
                call_messages_list = run_tools(tool_calls, WORKER_DIRECTORY)
                messages.extend(call_messages_list)

if __name__ == "__main__":
    run()
