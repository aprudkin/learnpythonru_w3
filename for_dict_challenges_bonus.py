"""
Пожалуйста, приступайте к этой задаче после того, как вы сделали и получили ревью ко всем остальным задачам
в этом репозитории. Она значительно сложнее.


Есть набор сообщений из чата в следующем формате:

```
messages = [
    {
        "id": "efadb781-9b04-4aad-9afe-e79faef8cffb",
        "sent_at": datetime.datetime(2022, 10, 11, 23, 11, 11, 721),
        "sent_by": 46,  # id пользователя-отправителя
        "reply_for": "7b22ae19-6c58-443e-b138-e22784878581",  # id сообщение, на которое это сообщение является ответом (может быть None)
        "seen_by": [26, 91, 71], # идентификаторы пользователей, которые видели это сообщение
        "text": "А когда ревью будет?",
    }
]
```

Так же есть функция `generate_chat_history`, которая вернёт список из большого количества таких сообщений.
Установите библиотеку lorem, чтобы она работала.

Нужно:
1. Вывести айди пользователя, который написал больше всех сообщений.
2. Вывести айди пользователя, на сообщения которого больше всего отвечали.
3. Вывести айди пользователей, сообщения которых видело больше всего уникальных пользователей.
4. Определить, когда в чате больше всего сообщений: утром (до 12 часов), днём (12-18 часов) или вечером (после 18 часов).
5. Вывести идентификаторы сообщений, который стали началом для самых длинных тредов (цепочек ответов).

Весь код стоит разбить на логические части с помощью функций.
"""
import random
import uuid
import datetime

import lorem


def generate_chat_history():
    messages_amount = random.randint(200, 1000)
    users_ids = list({random.randint(1, 10000) for _ in range(random.randint(5, 20))})
    sent_at = datetime.datetime.now() - datetime.timedelta(days=100)
    messages = []
    for _ in range(messages_amount):
        sent_at += datetime.timedelta(minutes=random.randint(0, 240))
        messages.append({
            "id": uuid.uuid4(),
            "sent_at": sent_at,
            "sent_by": random.choice(users_ids),
            "reply_for": random.choice([None, random.choice([m["id"] for m in messages]) if messages else []]),
            "seen_by": random.sample(users_ids, random.randint(1, len(users_ids))),
            "text": lorem.sentence(),
        })
    return messages


def get_users_statistic(dict_in: dict):
    # создаем список уникальных пользователей:
    all_users_id = [x.get('sent_by') for x in dict_in]
    unique_users = set(all_users_id)

    # из списка уникальных пользователей создаем словарь со статистикой по пользователю
    statistic_dict = {}
    for user in unique_users:
        statistic_dict[user] = {'messages_sent': 0, 'messages_viewed': 0}

    # создаем список из id всех сообщений:
    all_messages_id = [x.get('id') for x in dict_in]
    # из списка всех сообщений создаем словарь со статистикой по сообщению
    messages_dict = {}
    for message in all_messages_id:
        messages_dict[message] = {'author': '', 'reply_counter': 0, 'period': ''}

    # проходим по всем сообщениям и по каждому сообщению заполняем словари со статистиками
    for message in dict_in:
        # заполняем автора в словаре статистики сообщения:
        messages_dict[message['id']]['author'] = message['sent_by']

        # заполняем время дня, по дате сообщения:
        if message['sent_at'].time() < datetime.time(6, 0, 0, 0):
            messages_dict[message['id']]['period'] = 'night'
        elif message['sent_at'].time() < datetime.time(12, 0, 0, 0):
            messages_dict[message['id']]['period'] = 'morning'
        elif message['sent_at'].time() < datetime.time(18, 0, 0, 0):
            messages_dict[message['id']]['period'] = 'day'
        elif message['sent_at'].time() <= datetime.time(23, 59, 59, 999999):
            messages_dict[message['id']]['period'] = 'evening'

        # заполняем статистику по пользователям
        statistic_dict[message['sent_by']]['messages_sent'] += 1
        statistic_dict[message['sent_by']]['messages_viewed'] += len(message['seen_by'])

        # проверяем, является ли это ответом на другое сообщение:
        if message['reply_for']:
            # в статистике для сообщения увеличиваем счетчик:
            messages_dict[message['reply_for']]['reply_counter'] += 1

    # результирующие словари для пользователя, сообщения с ответми и времени дня
    result_users_sent = {'counter': 0, 'winner': ''}
    result_users_views = {'counter': 0, 'winner': ''}
    result_message_reply = {'counter': 0, 'winner': '', 'message_id': ''}
    result_message_period = {'night': 0, 'morning': 0, 'day': 0, 'evening': 0}

    for user in statistic_dict:
        # ищем победителя по кол-ву отправленных сообщений:
        if statistic_dict[user]['messages_sent'] > result_users_sent['counter']:
            result_users_sent['counter'] = statistic_dict[user]['messages_sent']
            result_users_sent['winner'] = user

        # ищем победителя по кол-ву просмотров:
        if statistic_dict[user]['messages_viewed'] > result_users_views['counter']:
            result_users_views['counter'] = statistic_dict[user]['messages_viewed']
            result_users_views['winner'] = user

    for message in messages_dict:
        # ищем самое отвечаемое сообщение (но это не решение задачи, где нужно найти автора, чьи сообщения
        # набрали больше всего ответов):
        if messages_dict[message]['reply_counter'] > result_message_reply['counter']:
            result_message_reply['counter'] = messages_dict[message]['reply_counter']
            result_message_reply['winner'] = messages_dict[message]['author']
            result_message_reply['message_id'] = message

        # заполняем счетчики времени суток:
        result_message_period[messages_dict[message]['period']] += 1

    most_replied = get_most_replied_author(messages_dict)
    most_replied_period = max(result_message_period, key=result_message_period.get)

    longest_thread = find_longest_thread(dict_in)

    print()
    print(f'Всего сообщений: {len(dict_in)}')
    print(f'Уникальных отправителей: {len(unique_users)}')
    print()
    print(f'[1] Пользователь с id {result_users_sent["winner"]} написал больше всего сообщений: {result_users_sent["counter"]}.')
    print(f'[2] На сообщения пользователя с id {most_replied["author"]} ответили сумарно наибольшее колво раз: {most_replied["counter"]}.')
    print(f'[-] На сообщение c message_id {str(result_message_reply["message_id"])[:5]}... пользователя с id {result_message_reply["winner"]} ответили наибольшее количество раз: {result_message_reply["counter"]}.')
    print(f'[3] Coобщения пользователя с id {result_users_views["winner"]} было просмотренно макимальное количество раз: {result_users_views["counter"]}.')
    print(f'[4] Время дня, в которое оставляли больше всего сообщений: {most_replied_period}, общая ст-ка: {result_message_period}')
    if len(longest_thread) == 1:
        print(f'[5] Самая длинная цепочка сообщений начинается с сообщения: {longest_thread[0][-2]} и заканчивается {longest_thread[0][0]}')
        print(f'Длина цепочки: {len(longest_thread[0])} сообщений')
    else:
        print('[5] Самые длинные цепочки сообщений:')
        for row in longest_thread:
            print(f'Начальное сообщение: {row[-2]} и конечное сообщение: {row[0]}')
        print(f'Длина цепочек: {len(longest_thread[0])} сообщений')


def get_most_replied_author(messages_dic: dict) -> dict:
    """Получаем на вход словарь вида:
    {
        'id_сообщения':{
            'author': 'author_id',
            'reply_counter': 123
        },
    }

    Необходимо по нему пройти и для каждого автора посчитать сумму всех ответов.
    """

    authors_dict = {}
    for message in messages_dic:
        authors_dict[messages_dic[message]['author']] = authors_dict.get(messages_dic[message]['author'], 0) + messages_dic[message]['reply_counter']

    current_max = {'author': '', 'counter': 0}
    for author in authors_dict:
        if authors_dict[author] > current_max['counter']:
            current_max['author'] = author
            current_max['counter'] = authors_dict[author]

    return current_max


def find_longest_thread(messages_list: list) -> list:

    # построим вспомогательный словарь с указателями на родителя:
    # {
    #     'message_id': 'parent_id'
    # }
    some_dict = {}
    for message in messages_list:
        if message.get('reply_for'):
            some_dict[str(message['id'])] = str(message.get('reply_for'))
        else:
            some_dict[str(message['id'])] = None

    some_list = []
    iteration_count = 0

    # Создадим первичное наполнение списка из id всех сообщений:
    for message in messages_list:
        some_list.append([str(message['id'])])

    # Для каждой строки в списке, проверим есть ли у нее родительское сообщение (по вспомогательному словарю),
    # если да, то добавим его в слудующую колонку:
    while True:
        parents_flag = False
        for row in some_list:
            # если хотя бы для одного сообщения нашли родителя то ставим флаг продолжения:
            if some_dict.get(row[iteration_count]):
                parents_flag = True

            # заполняем родителей
            row.append(some_dict.get(row[iteration_count]))

        iteration_count += 1

        # выходим если не нашли ни одного родителя
        if not parents_flag:
            break

    resulting_list = []

    for row in some_list:
        if row[iteration_count - 1]:
            resulting_list.append(row)

    return resulting_list


if __name__ == "__main__":
    # print(generate_chat_history())
    generated_history = generate_chat_history()

    get_users_statistic(generated_history)
