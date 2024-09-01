import os
from together import Together

client = Together(api_key="107b85c9560ee933d8ac05aa0aca730a29000f1b56f68f0ad9c8d3de6345ed77")
response = client.chat.completions.create(
  model="meta-llama/Llama-3-70b-chat-hf",
  messages=[{
    "role": "user", 
    "content": "Explain Gen AI"}],
)
print(response.choices[0].message.content)