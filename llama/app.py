from transformers import pipeline
import os
import torch

# Load Llama 3 model from Hugging Face
llama3_model = pipeline("text-generation", model="meta-llama/Meta-Llama-3.1-8B", model_kwargs={"torch_dtype": torch.bfloat16}, device_map="auto")

prompt = "How many months are there in a year?"
response = llama3_model(prompt, max_length=50, truncation=True)

print(response[0]['generated_text'])