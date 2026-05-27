import requests
import json

url = "https://api.openai.com/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
   }

data = {
    "model" : "gpt-4o-mini",
    "messages": [
        {"role": "user" , "content":"Which is used most frequently, top k or top p, among many large language models?"}
    ]
}

response = requests.post(url, headers=headers, json=data)

result =response.json()

print(result["choices"][0]["message"]["content"])