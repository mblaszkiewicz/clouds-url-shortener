# URL Shortener 
Group 6

Dependencies: 
- Python 3 
- Flask
- Django (for URL validation)
- JWT

## Running the services

### Running the authorization service
1. Change directory to the `url-shortener` directory of the project
2. Set following environment variables: 
```
FLASK_APP = auth_app.py
FLASK_ENV = development
FLASK_DEBUG = 0
```
3. Run command `python -m flask run -p 5001`, where 5001 might be replaced with a different port number

### Running the URL-shortener service
1. Change directory to the `url-shortener` directory of the project
2. Set following environment variables: 
```
FLASK_APP = shortener_app.py
FLASK_ENV = development
FLASK_DEBUG = 0
```
3. Run command `python -m flask run -p 5000`, where 5001 might be replaced with a different port number

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