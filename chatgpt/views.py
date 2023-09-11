from openai.error import (APIError, Timeout, RateLimitError,
                          APIConnectionError, InvalidRequestError,
                          AuthenticationError, ServiceUnavailableError)
from Elearning import settings
from django.http import JsonResponse
import openai
import tiktoken
import logging

# logger instance associated with the name of the current module
logger = logging.getLogger(__name__)


def ensure_conversation_history(request):
    if 'conversation_history' not in request.session:
        request.session['conversation_history'] = []


def DivContent(request):
    request.session['content'] = request.GET.get('content', '')
    content = request.session['content']
    # Update the conversation history with the new content
    update_conversation_history(request, content)
    return JsonResponse({'status': 'success', 'message': f"Message received: {content}"})


def update_conversation_history(request, content):
    # ensuring if the conversation history exists in the session if not one will be created a harmless edge case function don't mind it
    ensure_conversation_history(request)
# read the system role promt for the file
    with open("/Users/murad/Desktop/MyProject/branch2/chatgpt/Prompt.txt", "r") as file:
        text = file.read()
    # Update the user's conversation history in the session
    request.session['conversation_history'].append({
        "role": "system",
        "content": text + content + 'Always respond in less than 20 words. And never ever break character, stay true to your role'
    })
    # Mark the session as modified to ensure it gets saved
    request.session.modified = True


def get_total_tokens_in_history(conversation_history):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    total_tokens = 0
    for message in conversation_history:
        total_tokens += len(encoding.encode(message["content"]))
    return total_tokens


def chat(request):
    # ensuring if the conversation history exists in the session if not one will be created a harmless edge case function don't mind it
    ensure_conversation_history(request)

    openai.api_key = settings.OPENAI_API_KEY
    new_message = request.GET.get('message')

    # Initialize conversation history for the user if it doesn't exist
    if 'conversation_history' not in request.session:
        request.session['conversation_history'] = []

    # Add the new message to the user's conversation history in the session
    request.session['conversation_history'].append(
        {"role": "user", "content": new_message})
    logger.info(
        f"befor deletion converation token count : {get_total_tokens_in_history(request.session['conversation_history'])}")

    # Ensure conversation_history is within token limits
    while get_total_tokens_in_history(request.session['conversation_history']) > 3000:
        del request.session['conversation_history'][0]
        logger.info(
            f'After message deleteion token count: {get_total_tokens_in_history(request.session["conversation_history"])}')

    try:
        # Use the user's conversation history in the session when generating a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=request.session['conversation_history'],
        )
    except Exception as e:
        logger.error(f"OpenAI API call failed: {str(e)}")

    # Add the AI's response to the user's conversation history in the session
    ai_response = response['choices'][0]['message']['content']
    request.session['conversation_history'].append(
        {"role": "assistant", "content": ai_response})
    # logs the response from OpenAI
    logger.info(f" AI Response =>: {ai_response}")

    # logs the token usage
    tokens_used = response['usage']['total_tokens']
    tokens_in_history = get_total_tokens_in_history(
        request.session['conversation_history'])
    logger.info(f"Tokens used in this request: {tokens_used}")
    logger.info(f"Total tokens in conversation history: {tokens_in_history}")

    # Mark the session as modified to ensure it gets saved
    request.session.modified = True

    # Return the AI's response as a JSON response to the user in front end vision-bot
    return JsonResponse({'response': ai_response}, safe=False)
