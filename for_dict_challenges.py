# Задание 1
# Дан список учеников, нужно посчитать количество повторений каждого имени ученика
# Пример вывода:
# Вася: 1
# Маша: 2
# Петя: 2

students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Петя'},
]
print('\nЗадание 1')
list_of_names = [x.get('first_name') for x in students]
set_of_unique_names = set(list_of_names)
for name in set_of_unique_names:
    print(f'{name}: {list_of_names.count(name)}')


# Задание 2
# Дан список учеников, нужно вывести самое часто повторящееся имя
# Пример вывода:
# Самое частое имя среди учеников: Маша
students = [
    {'first_name': 'Вася'},
    {'first_name': 'Петя'},
    {'first_name': 'Маша'},
    {'first_name': 'Маша'},
    {'first_name': 'Оля'},
]


def popular_name(data_list: list) -> str:
    list_of_names = [x.get('first_name') for x in data_list]
    set_of_unique_names = set(list_of_names)
    name_counter = {'name': '', 'counter': 0}
    for name in set_of_unique_names:
        if list_of_names.count(name) > name_counter['counter']:
            name_counter['name'] = name
            name_counter['counter'] = list_of_names.count(name)
    return name_counter["name"]


print('\nЗадание 2')
print(f'Самое частое имя среди учеников: {popular_name(students)}')


# Задание 3
# Есть список учеников в нескольких классах, нужно вывести самое частое имя в каждом классе.
# Пример вывода:
# Самое частое имя в классе 1: Вася
# Самое частое имя в классе 2: Маша

school_students = [
    [  # это – первый класс
        {'first_name': 'Вася'},
        {'first_name': 'Вася'},
    ],
    [  # это – второй класс
        {'first_name': 'Маша'},
        {'first_name': 'Маша'},
        {'first_name': 'Оля'},
    ],
    [  # это – третий класс
        {'first_name': 'Женя'},
        {'first_name': 'Петя'},
        {'first_name': 'Женя'},
        {'first_name': 'Саша'},
    ],
]
print('\nЗадание 3')
for index, school_class in enumerate(school_students):
    print(f'Самое частое имя в классе {index + 1}: {popular_name(school_class)}')


# Задание 4
# Для каждого класса нужно вывести количество девочек и мальчиков в нём.
# Пример вывода:
# Класс 2a: девочки 2, мальчики 0
# Класс 2б: девочки 0, мальчики 2

school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '2б', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
    {'class': '2б', 'students': [{'first_name': 'Даша'}, {'first_name': 'Олег'}, {'first_name': 'Маша'}]},
]
is_male = {
    'Олег': True,
    'Маша': False,
    'Оля': False,
    'Миша': True,
    'Даша': False,
}
print('\nЗадание 4')
for school_class in school:
    names_list = [x.get('first_name') for x in school_class['students']]
    girls_counter = 0
    boys_counter = 0
    for name in names_list:
        if is_male.get(name):
            boys_counter += 1
            continue
        girls_counter += 1
    print(f'Класс {school_class["class"]}: девочки {girls_counter}, мальчики {boys_counter}')


# Задание 5
# По информации о учениках разных классов нужно найти класс, в котором больше всего девочек и больше всего мальчиков
# Пример вывода:
# Больше всего мальчиков в классе 3c
# Больше всего девочек в классе 2a

school = [
    {'class': '2a', 'students': [{'first_name': 'Маша'}, {'first_name': 'Оля'}]},
    {'class': '3c', 'students': [{'first_name': 'Олег'}, {'first_name': 'Миша'}]},
]
is_male = {
    'Маша': False,
    'Оля': False,
    'Олег': True,
    'Миша': True,
}
print('\nЗадание 5')
girls_max = {'class': '', 'quantity': 0}
boys_max = {'class': '', 'quantity': 0}
for school_class in school:
    names_list = [x.get('first_name') for x in school_class['students']]
    girls_counter = 0
    boys_counter = 0
    for name in names_list:
        if is_male.get(name):
            boys_counter += 1
            continue
        girls_counter += 1
    if girls_counter > girls_max['quantity']:
        girls_max['class'] = school_class['class']
    if boys_counter > boys_max['quantity']:
        boys_max['class'] = school_class['class']
print(f'Больше всего мальчиков в классе {boys_max["class"]}')
print(f'Больше всего девочек в классе {girls_max["class"]}')
