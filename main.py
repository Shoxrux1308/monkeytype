import requests
import csv
from html2image import Html2Image

def get_wpm_accuracy(username:str,time:int)->dict:
    url = f'https://api.monkeytype.com/users/{username}/profile'
    response = requests.get(url)
    # Get the JSON data from the response
    data = response.json() 
    print(username)
    time = data['data']['personalBests']['time'].get(str(time),0)

    if time == 0:
        return {'wpm':0,'accuracy':0}
    # Get accuracy
    accuracy = time[0].get('acc')
    # Get wpm
    wpm = time[0].get('wpm')
    return {'wpm':wpm,'accuracy':accuracy}
    

# Read users info from csv file
def get_user_info(file_path:str)->list:
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
        data = get_wpm_accuracy(user['username'],time)
        users_wpm_accuracy.append(
            {
                'full_name': user['full_name'],
                'username': user['username'],
                'wpm': data['wpm'],
                'accuracy': data['accuracy']
            }
        )
    # Sort users by wpm
    users_wpm_accuracy.sort(key=lambda x: x['wpm'], reverse=True)
    return users_wpm_accuracy

def get_users_html_convert(user_data: list, result_image_path: str):
    results = """"""
    for idx,user in enumerate(user_data):
        results += f"""
            <tr>
                <td>{"🥇 "+user['full_name'] if idx==0 else "🥈 "+user['full_name'] if idx==1 else "🥉 "+user['full_name'] if idx==2 else str(idx+1)+'. '+user['full_name']}</td>
                <td>{user['wpm']}</td>
                <td>{user['accuracy']}</td>
            </tr>
            """
    html_file_str = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WPM and Accuracy Table</title>
        <link rel="stylesheet" href="style.css">
    </head>
    <body>
        <div>
            <h2>Typing Test Leaderboard by 60 seconds</h2>
            <table>
                <tr>
                    <th>Full Name</th>
                    <th>WPM</th>
                    <th>Accuracy</th>
                </tr>
                {results}
            </table>
        </div>
    </body>
    </html>
        
    """
    with open("index.html", "w", encoding="utf-8") as file_html:
        file_html.write(html_file_str)

    html_image = Html2Image()
    html_image = Html2Image(size=(430, 1080))
    image_conv = html_image.screenshot(
        html_file='index.html',
        css_file='style.css',
        save_as = result_image_path
    )
    return image_conv



