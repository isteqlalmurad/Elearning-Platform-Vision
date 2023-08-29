from Elearning import settings
from django.http import JsonResponse
import openai
import logging
from chatgpt import views
from userprofile.models import Progress

logger = logging.getLogger(__name__)

# this is a new function to create a question  when next lesson btn is clicked the code will go here


def exercise(request):
    openai.api_key = settings.OPENAI_API_KEY

    # Check if the user is authenticated and get the energyPoint from DB
    energyPoint = 0
    progress_instance = None

    # Check if the user is authenticated and retrieve or create their progress instance
    if request.user.is_authenticated:
        progress_instance, created = Progress.objects.get_or_create(
            user=request.user)
        if progress_instance:
            energyPoint = progress_instance.energyPoints
        else:
            # Log an error if there's a problem retrieving or creating the progress instance
            logger.error(
                f"Failed to retrieve or create progress instance for user {request.user.username}")

   # this is the initial go! for the question to be asked from the user, and also the input and go
    question = request.GET.get('answer', '')

    # Get the conversation history from the session
    conversation_history2 = request.session.get('conversation_history2', [])

    # Add a system message to the conversation history only if it's empty
    if not conversation_history2:
        system_message = " when I say go!, Create create JUST ONE questions form this lesson :" + views.content + \
            ",end of lesson. : after asking the question wait for my respons (if the answer is accurate respond only by saying 'CORRECT 😊'  and ask another question from the lesson Section Three بخش سومExercise تمرین). (if the answer I give is inaccurate respond by saying 'INCORRECT 😔 and then give me a hint to correct answer don't give me the answer in no more that 10 words)."
        conversation_history2.append(
            {"role": "system", "content": system_message})

    # Add the question to the conversation history
    conversation_history2.append({"role": "user", "content": question})

 # Make an API call to OpenAI to generate a response based on the conversation history
    try:
        response = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",
            # model="gpt-3.5-turbo-16k-0613",
            model="gpt-4",
            messages=conversation_history2,
            temperature=0,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        ai_response = response['choices'][0]['message']['content']
        conversation_history2.append(
            {"role": "assistant", "content": ai_response})

    except Exception as e:
        # Log any errors that occur during the API call
        logger.error(f"OpenAI API call failed: {str(e)}")
        return JsonResponse({'error': 'Failed to get a response from AI'}, status=500)

    # Store the updated conversation history in the session
    request.session['conversation_history2'] = conversation_history2

    # Log the user information along with the AI response for debuging purposes, will be discarted in production
    if request.user.is_authenticated:
        logger.debug(
            f"[From Exercise session] User {request.user.username} (ID: {request.user.id}) received AI response: {ai_response}")
    else:
        logger.debug(
            f"[From Exercise session] An anonymous user received AI response: {ai_response}")

    # If the AI response is correct, update the user's energy points
    if 'CORRECT 😊' in ai_response and progress_instance:
        energyPoint += 1
        logging_message = f'Your energy points at the moment are: {energyPoint}'
        logger.debug(logging_message)
        progress_instance.energyPoints = energyPoint
        progress_instance.save()

    # Return the AI's response as a JSON response
    return JsonResponse({'response': ai_response}, safe=False)


# Clearning session for the Exercise Modal
def clear_session(request):
    request.session['conversation_history2'] = []
    logging.info('excersise session cleared ')
    return JsonResponse({'message': 'Session cleared successfully'})


# Function to retrive the the energyPoints from the database model
def get_energy_points(request):
    if request.user.is_authenticated:
        try:
            progress_instance = Progress.objects.get(user=request.user)
            energyPoint = progress_instance.energyPoints
        except Progress.DoesNotExist:
            # Default to 0 if no record exists for this user in the Progress model
            energyPoint = 0
    else:
        # For non-authenticated users, you can choose to default to 0 or handle differently
        energyPoint = 0

    return JsonResponse({'energyPoint': energyPoint})
