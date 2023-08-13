from fastapi import FastAPI, Request
import os
import openai
import requests
from twilio.rest import Client
from pydantic import BaseModel

from twilio.twiml.messaging_response import MessagingResponse
openai.api_key = os.getenv('openapikey')
account_sid=os.getenv('twiliosessionid')
auth_token=os.getenv('twilioauthtoken')

client = Client(account_sid, auth_token)

twilio_phone_number = "whatsapp:+14155238886"

app = FastAPI()
print("ehl")

class Message(BaseModel):
    body: str


@app.get("/")
async def root():
    return {"message": "Hello World"}

def generate_answer(message):
    try:

        completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": message}
        ]
        )

    # completion = openai.Completion.create(
    # model="text-davinci-003",
    # prompt=message,
    # max_tokens=100,
    # temperature=0,
    # n=1,

    
    # stop = None
    # )
        print(completion.choices[0].message['content'])
        return completion.choices[0].message['content']
    except:
        pass
@app.post("/whatsapp")
async def whatsapp_reply(request: Request):
    try:

        form_data = await request.form()
        query = form_data.get("Body", "").lower()
        sender_number = form_data.get("From")
        print("sender   : ", sender_number)
    
   
        print("query: ", query)
        twilio_response = MessagingResponse()
        reply = twilio_response.message(generate_answer(query))
    # answer = generate_answer(query)
    # reply.body(answer)
        recipient_phone_number = sender_number
        message = client.messages.create(
        from_=twilio_phone_number,
        to=recipient_phone_number,
        body=str(generate_answer(query))
        )
        return str(twilio_response)
    except:
        pass

print("Public URL:", public_url)

    


