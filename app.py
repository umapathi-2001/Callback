from flask import Flask, request
import requests
import json

app = Flask(__name__)

client_id = 'XU01403-100'
secret_key = 'XCUZMZV0UF'
redirect_uri = 'https://flask-quiet-fog-1403.fly.dev/callback'  # Update with your actual Fly.io URL

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    if (auth_code):
        # Use the auth_code to request an access token
        data = {
            'client_id': client_id,
            'secret_key': secret_key,
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_uri
        }

        response = requests.post('https://api.fyers.in/api/v2/token', data=json.dumps(data), headers={'Content-Type': 'application/json'})
        response_data = response.json()
        access_token = response_data.get('access_token')

        return f"Access Token: {access_token}\nResponse: {response_data}"
    return "No auth code found", 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
