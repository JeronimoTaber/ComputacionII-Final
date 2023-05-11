import os
import openai
import asyncio
import uuid 
# Load your API key
# from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")
model_engine = 'gpt-3.5-turbo'
interview_history = []

async def sendMessage(message):
    completion = await openai.ChatCompletion.create(
            model=model_engine,
            messages=message
        )
    print(message)
    return completion.choices[0].message.content.strip()