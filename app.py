from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from agent.model import OpenAIAPI
from agent.tools import run_tools
from agent.config import prompt, tools
import os
import json
from datetime import datetime

web_dir = os.path.join(os.getcwd(), 'web')
app = Flask(__name__, static_folder=web_dir, static_url_path='')
CORS(app)

WORKER_DIRECTORY = os.path.join(os.getcwd(), "worker")
HISTORY_DIR = os.path.join(os.getcwd(), 'chats')

os.makedirs(HISTORY_DIR, exist_ok=True)

def get_history_file(conversation_id):
    return os.path.join(HISTORY_DIR, f'{conversation_id}.json')

def load_history(conversation_id):
    history_file = get_history_file(conversation_id)
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return [{"role": "system", "content": prompt}]

def save_history(conversation_id, messages):
    history_file = get_history_file(conversation_id)
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['message']
    conversation_id = data['conversationId']
    api_key = data['apiKey']
    api_url = data['apiUrl']
    
    api = OpenAIAPI(api_key, api_url)
    
    messages = load_history(conversation_id)
    messages.append({"role": "user", "content": user_input})
    
    while True:
        response = api.oneapi(messages, model="gpt-4o", tools=tools, choices="auto", response_format=None)
        if response['type'] == 'message':
            response_message = response['message']
            messages.append({"role": "assistant", "content": response_message})
            save_history(conversation_id, messages)
            return jsonify({"message": response_message})
        elif response['type'] == 'tools':
            messages.append(response['message'])
            tool_calls = response['tools']
            call_messages_list = run_tools(tool_calls, WORKER_DIRECTORY)
            messages.extend(call_messages_list)
            save_history(conversation_id, messages)

def open_browser(): 
    url = "http://127.0.0.1:5000"
    command = f"Start-Process '{url}'"
    
    tool_call = {
        'id': 'open_browser',
        'function': {
            'name': 'run_powershell_command',
            'arguments': json.dumps({
                'command': command,
                'directory': WORKER_DIRECTORY
            })
        }
    }
    
    run_tools([tool_call], WORKER_DIRECTORY)

if __name__ == "__main__":
    open_browser()
    app.run()