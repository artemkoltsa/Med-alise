import logging
from alice_scripts import Skill, request, say, suggest
skill = Skill(__name__)

logging.basicConfig(level=logging.DEBUG)

@skill.script
def run_script():
    yield say('Добрый день! Как вас зовут?')
    name = request.command

    yield say('Сколько вам лет?')
    while not request.matches(r'\d+'):
        yield say('Я вас не поняла. Скажите число')
    age = int(request.command)

    yield say('Вы любите кошек или собак?',
              suggest('Обожаю кошечек', 'Люблю собак'))
    while not request.has_lemmas('кошка', 'кошечка',
                                 'собака', 'собачка'):
        yield say('У вас только два варианта - кошки или собаки')
    loves_cats = request.has_lemmas('кошка', 'кошечка')

    yield say(f'Рада познакомиться, {name}! Когда вам '
              f'исполнится {age + 1}, я могу подарить '
              f'{"котёнка" if loves_cats else "щенка"}!',
              end_session=True)

# # coding: utf-8
# # Импортирует поддержку UTF-8.
# from __future__ import unicode_literals
#
# # Импортируем модули для работы с JSON и логами.
# import json
# import logging
#
# # Импортируем подмодули Flask для запуска веб-сервиса.
# from flask import Flask, request
# app = Flask(__name__)
#
#
# logging.basicConfig(level=logging.DEBUG)
#
# # Хранилище данных о сессиях.
# sessionStorage = {}
#
# # Задаем параметры приложения Flask.
# @app.route("/", methods=['POST'])
#
# def main():
# # Функция получает тело запроса и возвращает ответ.
#     logging.info('Request: %r', request.json)
#
#     response = {
#         "version": request.json['version'],
#         "session": request.json['session'],
#         "response": {
#             "end_session": False
#         }
#     }
#
#     handle_dialog(request.json, response)
#
#     logging.info('Response: %r', response)
#
#     return json.dumps(
#         response,
#         ensure_ascii=False,
#         indent=2
#     )
#
# # Функция для непосредственной обработки диалога.
# def handle_dialog(req, res):
#     user_id = req['session']['user_id']
#
#     if req['session']['new']:
#         # Это новый пользователь.
#         # Инициализируем сессию и поприветствуем его.
#         sessionStorage[user_id] = {
#             'suggests': [
#                 "Не хочу.",
#                 "Не буду.",
#                 "Отстань!",
#             ]
#         }
#
#         # no[user_id] = 'Нет'
#
#
#         res['response']['text'] = 'Здравствуйте, это первая медицинская помощь от Алисы. Я объясню Вам принципы оказания первой помощи. Чем я могу Вам помочь?'
#         res['response']['buttons'] = get_suggests(user_id)
#         return
#
#     # Обрабатываем ответ пользователя.
#     if req['request']['original_utterance'].lower() in [
#         'нет',
#         'нет, спасибо',
#         'до свидания',
#         'пока',
#     ]:
#         # Пользователь согласился, прощаемся.
#         res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
#         return
#
#     # Если нет, то убеждаем его купить слона!
#     res['response']['text'] = 'Померьте температуру и напишите в градусах Цельсия через запятую. Пример: "36,6".'
#     res['response']['buttons'] = get_suggests(user_id)
#
#     # Пользователь согласился, прощаемся.
#     res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
#
#
#     # res['response']['buttons'] = get_suggests(user_id)
# #
# # def temp(user_id):
#
#
# # Функция возвращает две подсказки для ответа.
# def get_suggests(user_id):
#     session = sessionStorage[user_id]
#
#     # Выбираем две первые подсказки из массива.
#     suggests = [
#         {'title': suggest, 'hide': True}
#         for suggest in session['suggests'][:2]
#     ]
#
#     # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
#     session['suggests'] = session['suggests'][1:]
#     sessionStorage[user_id] = session
#
#     # Если осталась только одна подсказка, предлагаем подсказку
#     # со ссылкой на Яндекс.Маркет.
#     if len(suggests) < 2:
#         suggests.append({
#             "title": "Ладно",
#             "url": "https://market.yandex.ru/search?text=слон",
#             "hide": True
#         })
#
#     return suggests