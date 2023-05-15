from celery import Celery
import openai_async

from kombu import Connection

BROKER_URL = 'redis://localhost:6379/0'

with Connection(BROKER_URL) as conn:
    print('Connected to Redis:', conn.connected)

app = Celery('tasks', broker=BROKER_URL)
# Define the Celery task for chat completion


@app.task
async def chat_complete_task(messages):
    try:
        completion = await openai_async.chat_complete(
            os.getenv("OPENAI_API_KEY"),
            timeout=2,
            payload={
                "model": "gpt-3.5-turbo",
                "messages": messages,
            },
        )
        response = completion.choices[0].text.strip()
        return response        
    except Exception as e:
        return e