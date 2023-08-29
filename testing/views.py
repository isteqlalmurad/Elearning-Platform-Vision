from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.shortcuts import render
from Elearning import settings
import logging
from typing import List, Dict
from django.http import JsonResponse
import openai
import logging


def chat_view(request):
    return render(request, 'testing/chat.html')


# conversation_history: List[Dict[str, str]] = [
#     {"role": "system", "content": " whatever you respond, some how say that you love me, and always respond in farsi, always respond in farsi originally, even if the input is in english respond in farsi language or persian language, you are madly in love with me and my name is 'ګلثوم' I am a 23 years old girl and I live in Kabul, I am is your life, and your name is 'Murad', rembember your name is 'isteqlal murad ' which can be written in farsi as 'استقلال مراد' and you are engaded with me I am your fiance, be nice a philosophical respond not more that 10 words"}]


# def chat(request):
#     openai.api_key = settings.OPENAI_API_KEY
#     # Retrieve the new message from the user
#     new_message = request.GET.get('message')

#     # Add the new message to the conversation history
#     conversation_history.append({"role": "user", "content": new_message})

#     # Use the entire conversation history when generating a response
#     response = openai.Completion.create(
#         model="gpt-3.5-turbo-0613",
#         messages=conversation_history,

#     )

#     # Add the AI's response to the conversation history
#     ai_response = response['choices'][0]['message']['content']
#     conversation_history.append({"role": "assistant", "content": ai_response})

#     # Return the AI's response as a JSON response
#     return JsonResponse({'response': ai_response}, safe=False)


# # /// content passing trail function-----------------------------------------


# def testsubmit(request):

#     message = request.GET.get('submit', '')
#     # Process your message here...
#     processed_message = f"Received: {message}"  # Just an example

#     return JsonResponse({'status': 'success', 'message': 'Data received', 'response': processed_message})


# experiment with funcrtion calling using ChatCompletion endpoimt of OpenAI GPT:


# function that are out of the call body to api
def function_one():
    return "HI, I am function number one!"


def function_two():
    return "HI, I am function number two!"


# api function calling ( the function is called from the returned jason by openAI)

logger = logging.getLogger(__name__)


def ask_openai(query):
    functions = [
        {
            "name": "function_one",
            "description": "Prints a message from function one",
        },
        {
            "name": "function_two",
            "description": "Prints a message from function two",
        }
    ]
    messages = [{"role": "user", "content": query}]

    # Log the query being sent to OpenAI
    logger.info(f"Sending query to OpenAI: {query}")

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
    )

    # Log the response received from OpenAI
    logger.info(f"Received response from OpenAI: {response}")

    return response

# rendering the Function


# Set up logging
logger = logging.getLogger(__name__)


@csrf_exempt
def weather_request(request):
    my_message = ""
    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get('query')

        # Log the received query
        logger.info(f"Received query: {query}")

        response = ask_openai(query)
        response_message = response["choices"][0]["message"]
        if response_message.get("function_call"):
            function_name = response_message["function_call"]["name"]
            if function_name == "function_one":
                my_message = function_one()
            elif function_name == "function_two":
                my_message = function_two()

        # Log the response message
        logger.info(f"Responded with message: {my_message}")

    return JsonResponse({'response': my_message})
