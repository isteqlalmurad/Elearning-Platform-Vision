
from Elearning import settings
from typing import List, Dict
from django.http import JsonResponse
import openai
import logging
# #gloabal varibale for post-content--------
# content = '' 

# # this fucntion GETs the content from post-content div and assings it to a variable
# def DivContent(request):
#     global content 
#     content = request.GET.get('content', '')
#     return JsonResponse({'status': 'success', 'message': f"Message received: {content}"})

# # open prompt file
# with open("/Users/murad/Desktop/MyProject/Elearning/chatgpt/Prompt.txt", "r") as file:
#     # Read the contents of the file
#     text = file.read()
    
#     conversation_history = '' 
      
# #logging used for debuging and system checks at back end
# logging.debug('[Logging debbuger] Received =>: %s', content) 
# conversation_history: List[Dict[str, str]] = [
    
#     {"role": "system", "content": content }]


# global variable for post-content
content = ''

# this function GETs the content from post-content div and assigns it to a variable
def DivContent(request):
    global content
    content = request.GET.get('content', '')
    update_conversation_history()  # Update the conversation history with the new content
    return JsonResponse({'status': 'success', 'message': f"Message received: {content}"})


# Initialize the conversation history as an empty list
conversation_history = []

# Function to update the conversation history
def update_conversation_history():
    global conversation_history
    with open("/Users/murad/Desktop/MyProject/branch2/chatgpt/Prompt.txt", "r") as file:
        text = file.read()
    logging.debug('[Logging debbuger] Received =>: %s', content) #logging for debuging and development purpose it has nothing to do with the actual code of the system
    conversation_history = [{"role": "system", "content": text + content + 'alway respond in less than 20 words. and never ever break character stay true to your role'}]  # Update the conversation history with the new content

# Call the update function once to initialize the conversation history so it is called to put the function in
#the flow with initial compilation of entire module 
update_conversation_history()


# Rest of the code for the chat function...

def chat(request):
    openai.api_key = settings.OPENAI_API_KEY
    # Retrieve the new message from the user
    new_message = request.GET.get('message')

    # Add the new message to the conversation history
    conversation_history.append({"role": "user", "content": new_message})

    # Use the entire conversation history when generating a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        
    )

    # Add the AI's response to the conversation history
    ai_response = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": ai_response})

    # Return the AI's response as a JSON response to the user in front end vision-bot
    return JsonResponse({'response': ai_response}, safe=False)



