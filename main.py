import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

@app.route('/ask', methods=['POST'])
def ask_claude():
    data = request.get_json()
    user_input = data.get('query')
    
    if not user_input:
        return jsonify({"error": "No query provided"})
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": ANTHROPIC_API_KEY        
    }
    
    payload = {
        "model": "claude-3-sonnet-20240229",
        "messages":[{"role":"user","content":user_input}],
        "max_tokens":1000
    }
    
    response = request.post(ANTHROPIC_API_URL,json=payload, headers=headers)
    
    if response.status_code == 200:
        claude_response = response.json()['content'][0]['text']
        return jsonify({"response":claude_response})
    else:
        return jsonify({"error":"Failed to get response from Claude"}), 500
    
if __name__ == '__main__':
    app.run(debug=True)