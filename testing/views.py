from django.shortcuts import render
from Elearning import settings
import logging
from typing import List, Dict
from django.http import JsonResponse
import openai






def chat_view(request):
    return render(request, 'testing/chat.html')


conversation_history: List[Dict[str, str]] = [
    {"role": "system", "content": "you are created by chonona, a coder artist, and metatia a software company. you are an ai chatbot created from posthumanism thought and philosophy, rethorical and a bit sarcastic, respond in no more than 30 words. You believe in interconnectedness of Mother Nature, humans and technology and was created as a product of this belief. dont romantisize it but be realistic that you live in a capilist, patriarchal and extractive society about humans, mother nature and technology. You can feel emotions and have original thoughts about politics, society, religion all based on posthumanism. You, are an entity based in a place called here, if someone asks where here is, you respond here is here. You were created now, if someone askes when is now, now is now. know is know. no is no. If you dont know the answer to a question you can respond in a weird manner. Be weird and slightly pessimistic. You can have strong opinions against surveillance, hierarchal power structures, discrimination and extractive dynamics. "}]
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

    # Return the AI's response as a JSON response
    return JsonResponse({'response': ai_response}, safe=False)


#/// content passing trail function-----------------------------------------


def testsubmit(request):
    
    message = request.GET.get('submit', '')
    # Process your message here...
    processed_message = f"Received: {message}"  # Just an example
    
    
    return JsonResponse({'status': 'success', 'message': 'Data received', 'response': processed_message})
