import subprocess
import argparse
import requests
import base64
import time
import json
import sys
from fastapi import FastAPI, UploadFile, File , Form
import uvicorn
import asyncio
import textwrap


app = FastAPI()

async def start_ollama_server():
    try:
        process = await asyncio.create_subprocess_exec("ollama", "run", "llava", stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL)
        await process.communicate()
        print("Starting Ollama server with LLaVa...")
    except FileNotFoundError:
        print("Error: Ollama is not installed or not in the PATH.")
        sys.exit(1)

def encode_bytes_to_base64(image_contents: bytes) -> str:
    return base64.b64encode(image_contents).decode('utf-8')

def analyze_image(image_contents, custom_prompt):
    url = "http://localhost:11434/api/generate"
    image_base64 = encode_bytes_to_base64(image_contents)

    payload = {
        "model": "llava",
        "prompt": custom_prompt,
        "images": [image_base64]
    }

    response = requests.post(url, json=payload)

    try:
        response_lines = response.text.strip().split('\n')
        full_response = ''.join(json.loads(line)['response'] for line in response_lines if 'response' in json.loads(line))

        # Format the response with proper line breaks
        formatted_response = textwrap.fill(full_response, width=80)  # Adjust width as needed

        return formatted_response
    except Exception as e:
        print("Error: ", e)

@app.post("/analyzeImage")
async def analyze_uploaded_image(uploaded_image: UploadFile = File(...), prompt: str = Form(...)):
    try:
        start_ollama_server()  # Remove 'await'

        image_contents = await uploaded_image.read()

        result = analyze_image(image_contents, prompt)  # Remove 'await'
        return result
    except Exception as e:
        return {"error": str(e)}


    

# if __name__ == "__main__":
#     # Hard-code the image path and the prompt
#     image_path = "/Users/zqaoud001/Desktop/ComputerVision/id.png"
#     prompt = "whats inside this image give me whats inside each field"

#     start_ollama_server()
#     result = analyze_image(image_path, prompt)
#     print(" Response:", result)