import time
import requests
import os
import threading


def write_data(number, url='https://reqres.in/api/users?page='):
    pages_data = []
    num = 1
    while True:

        base_url = url + str(num)

        result = requests.get(url=base_url, params={'page': num}).json()

        if not result['data']:
            break
        else:
            pages_data.extend(result['data'])
            num += 1

    path_to_dir = r'C:\Users\Ильшат\Python Infa + private\venv\Homework 5\users_data'

    if not os.path.exists(path_to_dir):
        os.mkdir('users_data')

    for i1 in range(number):
        i = pages_data[i1]

        folder_path = os.path.join(path_to_dir, f'User_{i["id"]}')

        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        user_first_name = i['first_name']
        user_last_name = i['last_name']
        user_email = i['email']

        user_data_path = os.path.join(
            'C:\\Users\\Ильшат\\Python Infa + private\\venv\\Homework 5\\users_data\\' + 'User_' + str(i['id']),
            'info.txt')

        with open(user_data_path, 'w', encoding='utf-8') as file:
            file.write(f'Имя: {user_first_name}\n')
            file.write(f'Отчество : {user_last_name}\n')
            file.write(f'Email: {user_email}\n')

        user_avatar = requests.get(i['avatar'])
        user_avatar_path = os.path.join(
            'C:\\Users\\Ильшат\\Python Infa + private\\venv\\Homework 5\\users_data\\' + 'User_' + str(i['id']),
            'avatar.jpg')

        with open(user_avatar_path, 'wb') as file2:
            file2.write(user_avatar.content)

def split_threads(thread_number):
    for i in range(1, 4):
        write_data(thread_number * 3 + i)

def threaded(threads):
    thread_list = []

    for thread in range(threads):
        t = threading.Thread(target=split_threads, args=(thread, ))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()


if __name__ == '__main__':
    start = time.time()
    threaded(4)
    end = time.time()
    print(f'Время выполнения программы составило{round(start - end, 2)}')
