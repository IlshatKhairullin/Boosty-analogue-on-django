import requests
import json
import os

def write_data(url):
    base_url = url

    result = json.loads(
        requests.get(url=base_url, params={'page': 2}).text
    )
    print(result)
    path_to_dir = r'C:\Users\Ильшат\Python Infa + private\venv\Homework 4\users_data'  # путь поменять везде

    if not os.path.exists(path_to_dir):
        os.mkdir('users_data')

    for i in result['data']:
        folder_path = os.path.join(path_to_dir, f'User_{i["id"]}')
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        user_first_name = i['first_name']
        user_last_name = i['last_name']
        user_email = i['email']

        user_data_path = os.path.join('C:\\Users\\Ильшат\\Python Infa + private\\venv\\Homework 4\\users_data\\' + 'User_' + str(i['id']),
                                      'info.txt')
        with open(user_data_path, 'w', encoding='utf-8') as file:
            file.write(f'Имя: {user_first_name}\n')
            file.write(f'Отчество : {user_last_name}\n')
            file.write(f'Email: {user_email}\n')

        user_avatar = requests.get(i['avatar'])
        user_avatar_path = os.path.join('C:\\Users\\Ильшат\\Python Infa + private\\venv\\Homework 4\\users_data\\' + 'User_' + str(i['id']),
                                        'avatar.jpg')
        with open(user_avatar_path, 'wb') as file2:
            file2.write(user_avatar.content)


write_data('https://reqres.in/api/users?page=2')
