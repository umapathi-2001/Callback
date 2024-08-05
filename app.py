from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

client_id = 'XU01403-100'  # Your Fyers client ID with the required suffix
secret_key = 'XCUZMZV0UF'  # Your Fyers secret key
redirect_uri = 'https://flask-quiet-fog-1403.fly.dev/callback'  # Your actual Fly.io URL

@app.route('/callback', methods=['GET'])
def callback():
    auth_code = request.args.get('code')
    state = request.args.get('state')

    # Logging the received parameters
    app.logger.info(f"Callback hit with auth_code: {auth_code}, state: {state}")

    if auth_code:
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

        app.logger.info(f"Response from token request: {response_data}")

        return jsonify({
            "auth_code": auth_code,
            "state": state,
            "access_token": access_token,
            "response_data": response_data
        })

    return jsonify({"auth_code": auth_code, "state": state, "error": "No auth code found"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
