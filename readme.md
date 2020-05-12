# URL Shortener 
Group 6

Dependencies: 
- Python 3 
- Flask
- Django (for URL validation)
- JWT

## Docker commands
Building
```
docker build -t url-shortener:1 url-shortener/.
docker build -t auth-app:1 auth-app/.
docker build -t nginx-test nginx/.
```
Creating network
```
docker network create dev
```
Running
```
docker run -d -p 5001:5001 --net dev --net-alias auth-app auth-app:1
docker run -d -p 5001:5001 --net dev --net-alias auth-app auth-app:1
docker run -i -p 80:80 --net dev nginx-test
```

## Kubernetes
Running the pods, deployments and services:
```
kubectl create -f pod.yaml
kubectl create -f deployment.yaml
kubectl create -f service.yaml
```

## Running the services

### Running the authentication service
1. Change directory to the `url-shortener` directory of the project
2. Create a virtual environment (optional, example command: `virtualenv testing`, then activate `source testing/bin/activate`)
3. Install requirements: `pip install -r requirements.txt`
4. Set following environment variables: 
```
FLASK_APP=auth_app.py
FLASK_ENV=development
FLASK_DEBUG=0
```
5. Run command `python -m flask run -p 5001`, where 5001 might be replaced with a different port number

### Running the URL-shortener service
(First three steps overlap with the authentication service)

1. Change directory to the `url-shortener` directory of the project
2. Create a virtual environment (optional, example command: `virtualenv testing`, then activate `source testing/bin/activate`)
3. Install requirements: `pip install -r requirements.txt`
4. Set following environment variables: 
```
FLASK_APP = shortener_app.py
FLASK_ENV = development
FLASK_DEBUG = 0
```
5. Run command `python -m flask run -p 5000`, where 5001 might be replaced with a different port number

### Running the Nginx reverse proxy
Requires Nginx server to be installed at the machine.
1. Add to the configuration file: 
    ```
    server {
            listen 80;
            server_name localhost;
    
            location /user {
            proxy_pass http://127.0.0.1:5001;
            }
    
            location / {
            proxy_pass http://127.0.0.1:5000;
            }
        }
    ```
2. Modify values in the excerpt above:
    * 80 to port on which the reverse proxy should be running, 
    * localhost to the domain or other server name at which server will be listening 
    * proxy_pass to the local addresses and ports on which services run:
        * auth_app for /user
        * shortener_app for /
3. Start the Nginx server
