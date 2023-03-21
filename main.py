import requests
import datetime
import os

API_ID  = os.getenv('API_ID')
API_KEY  = os.getenv('API_KEY')
NUTRITIONIX_ENDPONT ='https://trackapi.nutritionix.com/v2/natural/exercise'
SHEETY_ENDPOINT = os.getenv('SHEETY_ENDPOINT')
SHEETY_AUTH= os.getenv('SHEETY_AUTH')

print(API_ID)

USER_DATA ={
    'query': '',
    'gender':'male',
    'weight_kg':73,
    'height_cm':176,
    'age':25
}




def get_exercise_result(user_exercises) -> list:
    """Get the result of the exercises from the API"""
    headers = {
        'x-app-id': API_ID,
        'x-app-key':API_KEY,
        'x-remote-user-id':'0',
        'Content-Type': 'application/json'
    }
    parameters_exer = {
        'query' : user_exercises,
        'gender': USER_DATA['gender'],
        'weight_kg': USER_DATA['weight_kg'],
        'height_cm': USER_DATA['height_cm'],
        'age': USER_DATA['age']
    }

    nutritionx_res = requests.post(url=NUTRITIONIX_ENDPONT, json=parameters_exer, headers=headers)
    nutritionx_res.raise_for_status()
    result_exercises = nutritionx_res.json()['exercises']
    return result_exercises


user_input = input('Tell me which exercises you did: ')
result = get_exercise_result(user_exercises=user_input)


current_time = datetime.datetime.now().strftime("%H:%M:%S")
current_date = datetime.date.today().strftime("%d/%m/%Y")
record ={'date': current_date, 'time':current_time}

for exercise in result:
    """Update the record with the result of the exercises"""
    duration = exercise['duration_min']
    calories = exercise['nf_calories']
    training = exercise['name'].title()

    record.update({'duration':duration, 'calories':calories,'exercise':training})
    headers = {"Authorization": SHEETY_AUTH}
    parameters_sheety = {
        'workout': record
    }
    """Send the record to the API"""
    sheety_response = requests.post(url=SHEETY_ENDPOINT, json=parameters_sheety, headers=headers)
    sheety_response.raise_for_status()
    print(sheety_response.text)




