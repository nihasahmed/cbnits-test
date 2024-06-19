## Auth0 User CRUD Operations Service

This repository contains a Python-based service for handling CRUD operations within the Auth0 database. It contains files required for local deployment using Docker, Kubernetes and deployment using Terraform on Azure using the Container Instance service. This code can also be run in the terminal by passing arguments to do the same operations like API.

### API reference

| Method   | Endpoint  |  Description |
| ------------ | ------------ | ------------ |
|  GET | /get_token   | to get access token  |
|  GET | /get_user/< user_id >  |  to get details of a user |
|  POST | /create_user  | to create a user  |
| DELETE  | /delete_user/< user_id >  | to delete a user  |   |

#### API Access Token 

All the APIs can be called without an authorisation header. But this will cause the app to make two call per operation. One for getting token, second for the actual operation. This doubles the latency. So it is recommended to call /get_token API first and use the access token from response as authorisation header for subsequent calls. 

### Curl commands

- To get token: `curl --location 'http://< api server url >/get_token'`
- To get a user using id: `curl --location 'http://< api server url >/get_user/< id >' \
--header 'Authorization: bearer < access token >'`
- To create a user with email and password: 
```bash
curl --location 'http://< api server url >/create_user' \
--header 'Authorization: bearer < access token >' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "<email>",
    "password": "<password>"
}'
```
- To delete a user using id: `curl --location 'http://< api server url >/delete_user/< id >' \
--header 'Authorization: bearer < access token >'`

### How to deploy API server locally 

#### Prerequisites

- Python
- Docker
- Kubernetes with a cluster set up

#### Using Docker

To build locally and deploy local image
- From root of this repo run `docker build -t < image name > . `
- Run the image and pass required credentials as environment variables for the container `docker run -t  -e AUTH0_DOMAIN=< domain > -e AUTH0_CLIENT_ID=< client id > -e AUTH0_CLIENT_SECRET= < secret > < image name >`

To download and run public image from docker hub
- Run  `docker run -t  -e AUTH0_DOMAIN=< domain > -e AUTH0_CLIENT_ID=< client id > -e AUTH0_CLIENT_SECRET= < secret > nihasahmeda/app-auth0:v1`

#### Using Kubernetes connected to a cluster

- Add the values of environment variables under image spec in deployment definition and run `kubectl apply -f app-k8s.yaml `

### How to deploy in Azure using Azure Container Instance service

- Login to azure CLI
- cd into terraform folder and create a new file called secrets.auto.tfvars
- Add variables and values like below


    auth0_domain = "domain value"
    auth0_client_id = "client_id value"
    auth0_client_secret = "secret value"
- Run following commands
	- `terraform init`
	- `terraform apply` - respond with yes once satisfied with the plan
- In the output, container_ip_address show the IP address which is publicly accessible and can be used as API server address like http://< container_ip_address >:5000/get_user/123

### Run locally as a python script in terminal

You can also do the operations by just calling the main python file (app/main,py). Pass arguments below as per need. Run `python3 app/main,py -h` in case you need help with arguments. The first time an operation is called without token, the script generates a new token and outputs the token to the terminal. This can be used with --token argument in subsequent calls to eliminate multiple internal API calls.

Run `python3 app/main.py` with
- --mode MODE          Tells the script to run as an API (--mode=api) or a function call(--mode=func)
-  --action ACTION      Describe the action you want to perform ie: create/get/delete
-  --email EMAIL        Email id of the user. Required while creating the user
-  --password PASSWORD  Password of the user. Required while creating the user. Use a strong password to avoid errors.
-  --id ID              User id of the user against which action is to be perform ie get/delete
-  --token TOKEN        Pass the token value to not generate a new token (reduces internal api calls)





