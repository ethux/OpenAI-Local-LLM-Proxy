**GPT API Interface/Faker** 

This project goal is to test existing projects on Github or you made yourself how they perform with other LLM's.
We do this by creating a Nginx proxy, self signed certificate and editing the host file of your Linux machine.
The Python flask API (the application in this repo) will receive the requests instead of the OpenAI API, and will send the request to OpenLLM or Text Generation Webui API.



How to install and test this project:

chmod +x selfcert.sh
./selfcert.sh 

When running selfcert.sh you get asked for where you life etc, you can fill in fake information there.
Except this question 'Common Name (e.g. server FQDN or YOUR name) []: api.openai.com' fill in api.openai.com like stated in this example.

