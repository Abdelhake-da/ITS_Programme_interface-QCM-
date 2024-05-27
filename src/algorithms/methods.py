import json
from app.models import Question
from exam_pfe import settings
import openai
from anthropic import Anthropic
import requests
def open_ai_api():
    # Set your API key
    # api_key = "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"

    client = Anthropic(
        # This is the default and can be omitted
        api_key="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",
    )

    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Hello, Claude",
            }
        ],
        model="claude-3-opus-20240229",
    )
    print(message.content)


def open_ai_api1():
    URL = "https://api.openai.com/v1/chat/completions"

    payload = {
        "model": "gpt-3.5-turbo-instruct-0914",
        "messages": [
            {
                "role": "system",
                "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
            },
            {
                "role": "user",
                "content": "Compose a poem that explains the concept of recursion in programming.",
            },
        ],
        "temperature": 1.0,
        "top_p": 1.0,
        "n": 1,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
    }

    response = requests.post(URL, headers=headers, json=payload, stream=False)
    print("------------------------------------------------------------------------------\n")
    print(response)
    print(
        "\n------------------------------------------------------------------------------"
    )

def is_correct(questions, answers: list) -> list: 
    is_answer_true: list = []  
    tup_list = []
    for index, question in enumerate(questions):
        tup = []
        is_answer_true.append(None)
        for answer in answers[index]:
            for ans in  answer:
                if not ans in question[1]["qst_correct_answer"]:
                    is_answer_true[index]=False
                    tup.append((ans,False))
                else:
                    tup.append((ans,True))
        if is_answer_true[index] == None:
            is_answer_true[index]=True
        tup_list.append(tup)
    return is_answer_true,tup_list
def calc_note(response: list):
    num_total = len(response)
    true = response.count(True)
    return format((true * 20) / num_total, ".2f")
