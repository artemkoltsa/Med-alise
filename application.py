# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}

choice_buttons = [  # кнопки действий
    {
        'title': 'Нет',
        'hide': True
    },
    {
        'title': 'Я чувствую жар',
        'hide': True
    },
    {
        'title': 'Мне жарко',
        'hide': True
    }
]

temp_buttons = [  # кнопки действий
    {
        'title': 'До 37,0',
        'hide': True
    },
    {
        'title': 'От 37,0 до 38,5',
        'hide': True
    },
    {
        'title': 'Больше 38,5',
        'hide': True
    }
]

# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])

def main():
# Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )

# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }

        no_no = [ {'title': "Нет", 'hide': True} ]

        res['response']['text'] = 'Здравствуйте, это первая медицинская помощь от Алисы. Я объясню Вам принципы оказания первой помощи. Чем я могу Вам помочь?'
        res['response']['buttons'] = choice_buttons
        return

    if req['request']['original_utterance'] == 'Я чувствую жар' or 'Мне жарко':
        res['response']['text'] = 'Померьте температуру и напишите в градусах Цельсия через запятую. Пример: 36,6.'
        res['response']['buttons'] = temp_buttons

    if req['request']['original_utterance'] == 'Нет':
        res['response']['text'] = 'Спасибо, что обратились ко мне за первой помощью!'
        res['response']['end_session'] = True

    if req['request']['original_utterance'] == 'До 37,0':
        res['response']['text'] = 'У Вас нормальная температура тела. ' \
                                  'Я могу Вам предложить выпить прохладной воды. ' \
                                  'Если вы в здании, то советую Вам проветрить помещение. ' \
                                  'Чем я могу быть Вам еще полезна?'
        res['response']['buttons'] = choice_buttons

    if req['request']['original_utterance'] == 'От 37,0 до 38,5':
        res['response']['text'] = 'У Вас повышенная температура тела. ' '\n' \
                                  'Для начала используйте физические методы снижения температуры. ' '\n' \
                                  'К ним относятся: снижение температуры в комнате, доступ свежего воздуха, обильное питье прохладной воды, протирания физиологических складок тканью смоченной в прохладной воде (коленные и локтевые сгибы, шея, затылок, подмышечные впадины, ступни). ' \
                                  'Влажное полотенце смоченное прохладной водой положите на лоб. ' '\n' \
                                  'Если чувствуете ухудшения состояния или присоединения других симптомов заболеваний, то вызовите медицинскую Скорую Помощь по номеру телефона - 103. ' \
                                  'Или 112 - это единая служба спасения, которая переведет Вас на линию Скорой Помощи. ' '\n' \
                                  'Могу ли Вам еще чем-то помочь?'
        res['response']['buttons'] = choice_buttons

    if req['request']['original_utterance'] == 'Больше 38,5':
        res['response']['text'] = 'У Вас высокая температура тела. ' '\n' \
                                  'Необходимо использовать медикаментозные способы понижения температуры тела. ' \
                                  'Для этого подойдут жаропонижающие препараты.' '\n' \
                                  ' Например: Парацетамол, Ибупрофен, Нимесулид, Терафлю. ' '\n' \
                                  'ВАЖНО: не каждое лекарство подходит детям, больным сахарным диабетом, беременным и кормящим женщинам. ' '\n' \
                                  'Обязательно изучите инструкцию перед применением лекарственного средства. ' \
                                  'Совместно с медикаментозными способами можно использовать физические методы охлаждения. ' '\n' \
                                  'Если чувствуете ухудшения состояния или присоединения других симптомов заболеваний, то немедленно вызовите медицинскую скорую помощь по номеру телефона - 103. ' \
                                  'Или 112 - это единая служба спасения, которая переведет Вас на линию Скорой Помощи.' '\n' \
                                  'Могу ли Вам еще чем-то помочь?'
        res['response']['buttons'] = choice_buttons
        return

    # if req['request']['original_utterance'] == ['Я чувствую жар', 'Мне жарко']:
    #     res['response']['text'] = 'Померьте температуру и напишите в градусах Цельсия через запятую. Пример: 36,6.'
    #     res['response']['buttons'] = temp_buttons
    #     return
    # Обрабатываем ответ пользователя.
    # if req['request']['original_utterance'].lower() in [
    #     'нет',
    #     'нет, спасибо',
    #     'до свидания',
    #     'пока',
    # ]:
    #     # Пользователь согласился, прощаемся.
    #     res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
    #     return

    # Если нет, то убеждаем его купить слона!
    # res['response']['text'] = 'Померьте температуру и напишите в градусах Цельсия через запятую. Пример: "36,6".'
    # res['response']['buttons'] = get_suggests(user_id)

    # Пользователь согласился, прощаемся.
    # res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'


    # res['response']['buttons'] = get_suggests(user_id)
#
# def temp(user_id):
def no(user_id):
    no_no = [{'title': "Нет", 'hide': True}]
    return no_no
# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    # Убираем первую подсказку, чтобы подсказки менялись каждый раз.
    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    # Если осталась только одна подсказка, предлагаем подсказку
    # со ссылкой на Яндекс.Маркет.
    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": "https://market.yandex.ru/search?text=слон",
            "hide": True
        })

    return suggests

if __name__ == "__main__":
    app.run()