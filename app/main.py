from email import header
from lib2to3.pgen2 import token
from operator import mod
from urllib import response
from webbrowser import get
import requests, json, sys, os, argparse
from flask import Flask, request, jsonify

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')

parser = argparse.ArgumentParser()

parser.add_argument("--mode", help="Tells the script to run as an API (--mode=api) or a function call(--mode=func)")
parser.add_argument("--action", help="Describe the action you want to perform ie: create/get/delete")
parser.add_argument("--email", help="Email id of the user. Required while creating the user")
parser.add_argument("--password", help="Password of the user. Required while creating the user. Use a strong password to avoid errors.")
parser.add_argument("--id", help="User id of the user against which action is to be perform ie get/delete")
parser.add_argument("--token", help="Pass the token value to not generate a new token")

app = Flask(__name__)

def get_management_api_token():
    url = f'https://{AUTH0_DOMAIN}/oauth/token'
    headers = {'content-type': 'application/json'}
    payload = {
        'client_id': AUTH0_CLIENT_ID,
        'client_secret': AUTH0_CLIENT_SECRET,
        'audience': 'https://dev-jurvj62bq0e2lqz2.us.auth0.com/api/v2/',
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()

def create_user(email, password, token):
    url = f'https://{AUTH0_DOMAIN}/api/v2/users'
    headers = {'authorization': f'Bearer {token}', 'content-type': 'application/json'}
    payload = {
        'email': email,
        'password': password,
        'connection': 'Username-Password-Authentication'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

def get_user(user_id, token):
    url = f'https://{AUTH0_DOMAIN}/api/v2/users/auth0|{user_id}'
    headers = {'authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)
    return response.json()

def delete_user(user_id, token):
    url = f'https://{AUTH0_DOMAIN}/api/v2/users/auth0|{user_id}'
    headers = {'authorization': f'Bearer {token}'}
    response = requests.delete(url, headers=headers)
    if response.status_code==204:
        print("Operation Successful")
        return {'statusCode': 204, 'error': '', 'message': f'Successfully deleted user {user_id} from Auth0 database', 'errorCode': ''}
    else:
        return response.json()

def function_checker(args):
    action = args.action
    if args.token:
        token = args.token
    else: 
        token = get_management_api_token()['access_token']
        print(f'Use following token for further function calls using --token argument to reduce API calls \n Token: {token}')

    if action == 'create':
        email = args.email
        password = args.password
        print(create_user(email, password, token))
    elif action == 'get':
        user_id = args.id
        print(get_user(user_id, token))
    elif action == 'delete':
        user_id = args.id
        print(delete_user(user_id, token))
    else:
        print("Invalid action. Use create, get, or delete. Please refer documentation or run 'main.py -h'.")

def get_token(request):
    headers = request.headers
    if 'Authorization' in headers:
        bearer = headers.get('Authorization') 
        token = bearer.split()[1]
    else:
        token = get_management_api_token()['access_token']
    return token

@app.route('/get_token', methods=['GET'])
def generate_token_for_api():
    response = get_management_api_token()
    return jsonify(response)

@app.route('/create_user', methods=['POST'])
def create_user_endpoint():
    token = get_token(request)
    data = request.json
    result = create_user(data['email'], data['password'], token)
    return jsonify(result)

@app.route('/get_user/<user_id>', methods=['GET'])
def get_user_endpoint(user_id):
    token = get_token(request)
    result = get_user(user_id, token)
    return jsonify(result)

@app.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user_endpoint(user_id):
    token = get_token(request)
    result = delete_user(user_id, token)
    return result


if __name__ == '__main__':
    args=parser.parse_args()
    if args.mode not in ["api", "func"]:
        print("Please provide a correct mode to run, 'api' to run as an api server and 'func' to run as a function from console itself with required params. Please refer documentation or run 'main.py -h'")
        exit()
    if args.mode == "api":
        app.run(host='0.0.0.0', port=5000)
    elif args.mode == "func":
        function_checker(args)