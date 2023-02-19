from random import choice
from flask import Flask, request
import os
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')
completion = openai.Completion()
start_sequence = '\nAI:'
restart_sequence = '\n\nHuman:'
session_prompt = 'The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly. \n\nHuman: Hello, who are you? \nAI: I am an AI created by OpenAI. How can I help you today?'

def ask(question, chat_log=None):
 prompt_text = f'{chat_log}{restart_sequence}: {question}{start_sequence}:'
 response = openai.Completion.create(
 engine='davinci',
 prompt=prompt_text,
 temperature=0.8,
 max_tokens=150,
 top_p=1,
 frequency_penalty=0,
 presence_penalty=0.3,
 stop=['\n'],
 )
 story = response['choices'][0]['text']
 print(story)
 return str(story)
 
def append_interaction_to_chat_log(question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt 
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'