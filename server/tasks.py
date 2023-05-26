from celery import Celery
import openai_async
import os
import asyncio

# Create a Celery instance
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/1')

#Para limitar el numero de fetchs a openai
# app.conf.worker_prefetch_multiplier = 1

# Define a Celery task
@app.task
def add(x, y):
    return x + y

# Define a helper function to run the coroutine
async def run_chat_complete_task(api_key, messages):
    try:
        completion = await openai_async.chat_complete(
            api_key,
            timeout=20,
            payload={
                "model": "gpt-3.5-turbo",
                "messages": messages,
            },)
        print(completion.json())
        response = completion.json()["choices"][0]["message"]["content"].strip()
        return response        
    except Exception as e:
        return "Error: " + str(e)

@app.task
def chat_complete_task(messages):
    # Get the OpenAI API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        return "Error: OPENAI_API_KEY not set"
    
    # Create an event loop and run the coroutine
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(run_chat_complete_task(api_key, messages))
    
    return result