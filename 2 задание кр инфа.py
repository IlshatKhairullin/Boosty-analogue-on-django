import csv


class Human_Sims:
    def __init__(self, name, second_name, age, gender):
        self.name = name
        self.second_name = second_name
        self.age = age
        self.gender = gender

    def eat(self, product_name, count):
        with open('Information_food.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(
                [self.name, product_name, count]
            )


class Sims_Data:
    def __init__(self, file_path, columns):
        self.file_path = file_path
        self.columns = columns

    def get_list_of_food(self):
        with open('Information_food.csv', 'r') as file:
            reader = csv.DictReader(file, delimiter=',', fieldnames=self.columns)
            return [line for line in reader]


data_obj = Sims_Data(  # можно программу не запускать, тк в txt файле уже есть данные
    'Information_food.csv', ['name', 'product', 'count']
)
hum1 = Human_Sims('Jack', 'Junior', 18, 'male')
hum2 = Human_Sims('Jack', 'Junior', 18, 'male')

hum1.eat('rice', 100)
hum1.eat('tomato', 777)
hum2.eat('cabbage', 3)

print(data_obj.get_list_of_food())
