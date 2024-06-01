import os
from openai import AzureOpenAI
    
client = AzureOpenAI(
    api_key=os.getenv("720d8a2f0b0b479cbe2fb58d190f02f8"),  
    api_version="2024-02-01",
    azure_endpoint = os.getenv("https://knowledgegraphopenai.openai.azure.com/")
    )
    
deployment_name='openaiforknowledgegraph' #This will correspond to the custom name you chose for your deployment when you deployed a model. Use a gpt-35-turbo-instruct deployment. 
    
# Send a completion call to generate an answer
print('Sending a test completion job')
start_phrase = 'Write a tagline for an ice cream shop. '
response = client.completions.create(model=deployment_name, prompt=start_phrase, max_tokens=10)
print(start_phrase+response.choices[0].text)