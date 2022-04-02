import csv
from datetime import datetime


class User:
    def __init__(self, id, name, second_name, age, gender):
        self.id = id
        self.name = name
        self.second_name = second_name
        self.age = age
        self.gender = gender

    def get_dict_from_user(self):
        return {
            'id': self.id,
            'name': self.name,
            'second_name': self.second_name,
            'age': self.age,
            'gender': self.gender,
        }

    def __repr__(self):
        return f'{self.name} {self.second_name}'

class UsersData:
    def __init__(self, file_path, columns):
        self.file_path = file_path
        self.columns = columns
        self.count = 0

    def add_user(self, user_obj):
        with open(self.file_path, 'a') as file:
            writer = csv.DictWriter(
                file, delimiter=';', fieldnames=self.columns)
            writer.writerow(user_obj.get_dict_from_user())

    def delete_user(self, user_id):
        users_list_csv = self.get_list_of_users()
        index = None
        for idx, user in enumerate(users_list_csv):
            if int(user['id']) == user_id:
                index = idx
        if index is not None:
            users_list_csv.pop(index)
            with open(self.file_path, 'w') as file:
                writer = csv.DictWriter(
                    file, delimiter=';', fieldnames=self.columns)
                writer.writerows(users_list_csv)
        else:
            raise Exception(f'cant find user with id {user_id}')

    def get_list_of_users(self):
        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(
                file, delimiter=';', fieldnames=self.columns)
            return [line for line in reader]

    def send_message(self, user_1, user_2, text):
        with open('messages.csv', 'a') as file:
            fieldnames = ["sender", "recipient", "text", "time"]
            now = datetime.now()
            now = now.strftime('%H:%M %d/%m')

            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if self.count == 0:
                writer.writeheader()
                self.count = 1
            writer.writerow(
                {
                    "sender": user_1,
                    "recipient": user_2,
                    "text": text,
                    "time": now
                }
            )

    def clear_data(self, file_name):  # удаляет всю информацию в заданном файле
        self.count = 0
        try:
            with open(file_name) as in_file:
                with open(file_name, 'w') as out_file:
                    writer = csv.writer(out_file)
                    for row in csv.reader(in_file):
                        if row:
                            writer.writerow(row)
        except:
            raise FileNotFoundError("Данного файла не существует. Проверьте название файла")

    def messages_between_two_user(self, user_1, user_2):  # моежт возникать ошибка, когда первая строка пустая в messages
        with open("messages.csv", newline='') as file:
            reader = csv.DictReader(file)
            for a in reader:
                if a["sender"] == str(user_1) and a["recipient"] == str(user_2) or \
                        a["sender"] == str(user_2) and a["recipient"] == str(user_1):

                    print(a["sender"], a["recipient"], a["text"], a["time"])
            print()


data_obj = UsersData('users.csv', ['id', 'name', 'second_name', 'age', 'gender'])

user1 = User(1, 'Ivan', 'Vaskin', 18, 'female')
user2 = User(2, 'Nezabydka', 'Gromov', 20, 'male')
user3 = User(3, 'Marat', 'Dankovich', 66, 'malemale')

data_obj.add_user(user1)
data_obj.add_user(user2)
data_obj.add_user(user3)

# data_obj.clear_data('users.csv')  # удаляет всё в users

data_obj.send_message(user1, user3, 'Hi!')
data_obj.send_message(user3, user1, 'Hi, what is up?')
data_obj.send_message(user1, user3, 'Fine. Doing my homework...')

data_obj.send_message(user2, user3, 'Hi, Marat. How are you?')
data_obj.send_message(user3, user2, 'Hi, Nezabydka. Good enough')

# data_obj.clear_data('messages.csv')  # удаляет всё в messages

data_obj.messages_between_two_user(user1, user3)

data_obj.messages_between_two_user(user3, user2)
