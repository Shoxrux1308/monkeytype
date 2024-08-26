import requests
import csv

def get_wpm_accuracy(username:str,time:int)->dict:
    url = f'https://api.monkeytype.com/users/{username}/profile'
    response = requests.get(url)
    # Get the JSON data from the response
    data = response.json()
 
    time = data['data']['personalBests']['time'].get(str(time),0)
    # Get time
    
    # time = time.get(str(time),0)
    
    if time == 0:
        return {'wpm':0,'accuracy':0}
    # Get accuracy
    accuracy = time[0].get('acc')
    # Get wpm
    wpm = time[0].get('wpm')
    return {'wpm':wpm,'accuracy':accuracy}
    
# Read users info from csv file
def get_user_info(file_path:str)->dict:
    users = []
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        # Skip the header
        next(csv_reader)
        for row in csv_reader:
            users.append(
                {
                    'full_name': row[1],
                    'username': row[2],
                }
            )
    return users
    
def get_users_wpm_accuracy(users:dict,time:int)->dict:
    users_wpm_accuracy = []
    for user in users:
        data= get_wpm_accuracy(user['username'],time)
        users_wpm_accuracy.append(
            {
                'full_name': user['full_name'],
                'username': user['username'],
                'wpm': data['wpm'],
                'accuracy': data['accuracy']
            }
        )
    return users_wpm_accuracy




# print(users_wpm_accuracy)
# # print(get_wpm_accuracy(username,15))