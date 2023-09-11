import json
from Elearning import settings
from django.http import JsonResponse
import openai
import logging

from userprofile.models import Progress

from django.shortcuts import render

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
        system_message = "your and expert excersize designer for Native farsi speaking studnet who want to learn english language.  when type go!, present a completion questions JUST ONE AT A TIME from from the SECTION THREE EXCERCISE of this lesson :" + request.session['content'] + \
            ". : after asking the question wait for my respons (if the answer is accurate respond only by saying 'CORRECT 😊'  and proceed to another completion question or voucabulary question ). (if the answer I give is inaccurate respond by saying 'INCORRECT 😔 and then give me a hint to correct answer don't give me the answer in no more than 10 words)."
        conversation_history2.append(
            {"role": "system", "content": system_message})

    # Add the question to the conversation history
    conversation_history2.append({"role": "user", "content": question})

 # Make an API call to OpenAI to generate a response based on the conversation history
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            # model="gpt-3.5-turbo-16k-0613",
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

# for internal use function it returns energypoint from the databsase after authenticating the user


def _fetch_energy_points(request):
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

    return energyPoint


# Function to retrive the the energyPoints from the database model and returns a jasoneresponse catched in the front end
def get_energy_points(request):

    energyPoint = _fetch_energy_points(request)

    return JsonResponse({'energyPoint': energyPoint})


def generate_progress_report(request):
    openai.api_key = settings.OPENAI_API_KEY

    exercise_history = request.session.get('conversation_history2', [])
    print(f'this is the history of excersixe =======>>>>> {exercise_history}')
    chat_history = request.session.get('conversation_history', [])
    energyPoint = _fetch_energy_points(request)

    prompt_text = [{
        "role": "user",
        "content": (f"""
            You are analyzing a Farsi speaking student's performance.
            We are seeking a comprehensive report on our student, {request.user}. Here is the data we have:
            1. **Exercise History**: {exercise_history}
            2. **Chat History with the Bot**: {chat_history}
            3. **Energy Points**: {energyPoint} points (3 energy points are given for successful completion of the lesson)
            Using the above information, please provide a detailed analysis on the student's performance, engagement, and areas of improvement.
        """)}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=prompt_text,

        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    generated_report = response.choices[0].message['content']

    # Check if a Progress entry already exists for this user
    progress_entry = Progress.objects.filter(user=request.user).first()

    if progress_entry:
        # If an entry exists, update the report field
        progress_entry.report = generated_report
        progress_entry.save()
    else:
        # If no entry exists, create a new one
        Progress.objects.create(user=request.user, report=generated_report)

    try:
        with open('progress_analytics/progressReport.txt', "w") as file:
            file.write(generated_report)
        return JsonResponse({'message': 'Report Generated successfully'})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def profile_view_and_report(request):
    # with open('progress_analytics/progressReport.txt', "r") as file:
    #     report = file.read()

    progress_instance = Progress.objects.get(user=request.user)
    report = progress_instance.report

    energy_points = _fetch_energy_points(request)

    context = {
        'report': report,
        'energy_points': energy_points,
        # ... other context variables ...
    }

    return render(request, 'userProfileAndProgress.html', context)
