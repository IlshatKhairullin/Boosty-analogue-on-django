from random import randint


class LinkedList:
    head = None

    class Node:
        name = None

        def __init__(self, name, next_node=None):
            self.name = name
            self.next_node = next_node


class Human:

    def __init__(self, name, age, height, weight):
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight

    def introduce(self):  # дополнить год/лет
        return f'Меня зовут {self.name}, мне {self.age}.'

    def bodymassindex(self):
        bmi = self.weight / (self.height * self.height)
        return ('Вес в норме', 'Имеется лишний вес')[bmi * 10000 > 25]

    def birth_year(self):
        return 'Год рождения - ' + str(2022 - self.age)

    def zodiak(self):
        animals = ['Обезьяна', 'Петух', 'Собака', 'Свинья', 'Крыса', 'Бык', 'Тигр', 'Заяц', 'Дракон', 'Змея', 'Лошадь',
                   'Овца']
        return 'Знак зодиака - ' + str(animals[int(2022 - self.age) % 12])

    def place_info(self):
        print(f'Здравствуйте, {self.name}. Вы попали в загадочное место, где существуют только очереди. ',
              f'Вы не можете выбраться, даже не пытайтесь. Выберите пожалуйста очередь.', sep='\n')
        print('1 - очередь к кассе в магазине', '2 - очередь на получение визы в Сербию',
              '3 - очередь в почтовом отделении', sep='\n')

class Queue(LinkedList):  # добавить метод pop на проверку документов, если не норм - то делит

    def __init__(self):
        super().__init__()
        self.count = 0

    def add_person(self, name):
        self.count += 1

        if not self.head:
            self.head = self.Node(name)
            return name
        node = self.head

        while node.next_node:
            node = node.next_node

        node.next_node = self.Node(name)

    def pop(self):
        a = randint(0, 1)
        if a == 1:
            print('Документы проверены. Все хорошо')
            return
        else:
            node = self.head
            prev_node = node
            while node.next_node:
                prev_node = node
                node = node.next_node

            prev_node.next_node = node.next_node
            name = node.name

            del node
            self.count -= 1

            print('Человек не прошел проверку документов. Очередь стала на одного человека меньше...')
            return name

    def line_up(self, num):
        if num == 1:
            print()
            return 'Вы попали в магазин'
        elif num == 3:
            print()
            return 'Ну... вы сами выбрали это место'
        else:
            print()
            raise Exception('Данная очередь недоступна на территории загадочного места, выберете снова')

    def insert_random(self, name):
            index = randint(1, self.count)
            i = 0
            amount = 0
            node = self.head
            prev_node = self.head

            while i < index:
                prev_node = node
                node = node.next_node
                i += 1
                amount += 1

            prev_node.next_node = self.Node(name, next_node=node)

            return str(name) + str(f' прошел вперед на {amount} человека') + '\n' + 'Ваш словарный запас пополнился на 6 слов'

    def show_queue(self):
        node = self.head

        while node.next_node:
            print(node.name)
            node = node.next_node
        print(node.name)

    def get_len(self):
        return self.count


h = Human('Artur', 20, 170, 80)
print(h.introduce())
print(h.bodymassindex())
print(h.birth_year())
print(h.zodiak())
h.place_info()
print()

q = Queue()
print(q.line_up(1))
# print(q.line_up(2))
q.add_person('Artur')
q.add_person('Bob')
q.add_person('Fred')
q.show_queue()
print()
print()
q.pop()
q.show_queue()
print(q.get_len())
print()
print(q.insert_random('Arr'))
print()
q.show_queue()
