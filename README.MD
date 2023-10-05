# OpenAI Local LLM Proxy

The goal of this project is to test existing projects on Github or you made yourself how they perform with other LLM's then the ones provided by OpenAI.

We do this by creating a Nginx proxy, self signed certificate and editing the host file of your Linux machine, all API requests will be proxied to the Python flask API (the application in this repo) and will receive the requests instead of the OpenAI API. 
The Flask API will then send the API requests to the Text Generation Webui API or OpenLLM API. One of the few models which will perform well with this project is "FashionGPT v1.1" (fine tuned version of LLaMa-2-70B).

## PLEASE NOTE THIS PROJECT IS STILL WORK IN PROGRESS AND NOT ALL FUNCTIONS WILL WORK CORRECTLY

How to install and test this project:

`chmod +x selfcert.sh`

`./selfcert.sh `

When running selfcert.sh you get asked for where you life etc, you can fill in fake information there.
Except this question 'Common Name (e.g. server FQDN or YOUR name) []: api.openai.com' fill in api.openai.com like stated in this example.


When using python and want to trust those SSL certifcates you have to add this to the request module, don't forget to make a backup of that module.
edit session.py, in my case I had to add the SSL certificates I trusted by hand.

```cat /etc/ssl/certs/nginx-selfsigned.crt >> /home/ethux/.local/lib/python3.10/site-packages/certifi/cacert.pem```


```     
def __init__(self):
self.verify = '/home/ethux/.local/lib/python3.10/site-packages/certifi/cacert.pem'


#: A case-insensitive dictionary of headers to be sent on each
#: :class:`Request <Request>` sent from this
#: :class:`Session <Session>`.
self.headers = default_headers()
```

Now it edit the hosts file in /etc/hosts

`sudo vim /etc/hosts`

And add the following line
`127.0.0.1 https://api.openai.com`

Now create a virtual environment, do this by executing:

`python3 -m venv env` or use conda virtual environments

Activate the virtual environment

`source env/bin/activate`

Install dependencies
`pip3 install -r requirements.txt`

Run app.py
`python3 app.py`

Now you will be able to send post requests to the OpenAI API but will be proxied.

