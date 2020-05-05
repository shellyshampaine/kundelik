import telebot
import datetime
from kunapipy.kundelik import kundelik
import random
import requests
import json

TOKEN = '792704732:AAHBTUYMzth_hk4gaptyTUUJaA5sxghTrYY'
chat_id = None
bot = telebot.TeleBot(TOKEN)

login = 'zarazhotabaeva'
password = 'test123'
user_token = 'dv4LSjMGdagqlAowpm2l606U6ARwfoQw'
class_id = '1565042653527550944'
user_id = '1000004914080'
person_id = '1000006849522'
school_id = '1000004956244'


random_answers = ['Бла-бла-бла, не понимаю',
                  'Сори, не знаю такой команды',
                  'Проверь правописание',
                  'И что ты хотел этим сказать?',
                  'Непонел']


@bot.message_handler(commands=['i_need_help'], content_types=['text'])
def i_need_help(message):
    bot.send_message(message.chat.id, str(message.from_user.first_name) + ', спасибо за то, что не боишься обратиться за помощью. '
                                                                          'У всех нас бывают проблемы, даже у ботов, как я, и это нормально - чувстовать себя'
                                                                          ' подавленно. Для меня важно знать, что ты, мой друг, в порядке. Мы находимся на территории'
                                                                          ' РК, а значит, у нас есть действующая горячая линия, телефон доверия, куда ты можешь '
                                                                          ' обратиться за помощью, если ты оказался в сложной жизненной ситуации или'
                                                                          ' особенно, если к тебе применяется насилие.'
                                                                          'Помни, насилие - это во всех формах насилие, будь то твой родной человек или чужой одноклассник, '
                                                                          'никто не имеет права причинять тебе боль. Номер горячей линии - "150" или "8-708-106-08-10". '
                                                                          'Если ты чувствуешь себя нехорошо из-за конфликта с родителем или проблем в школе, ты также '
                                                                          'можешь обратииться по этой горячей линии. Также каждая школа обязана иметь в штате сотрудников '
                                                                          'школьного психолога, к которому ты также можешь обратиться за помощью. Обращаться за помощью'
                                                                          ' к психологу - абсолютно нормально, что бы там ни говорили, это нужно и важно делать для твоего '
                                                                          'самочувствия, ровно также, как делать прививки от гриппа осенью. Помни, что ты не виноват в том,'
                                                                          ' что происходит в твоей жизни, что у тебя все получится. Твой верный друг, бот :)')


@bot.message_handler(commands=['start'], content_types=['text'])
def welcome(message):
    global chat_id
    sticker = open('C:\Kundelik\hello_sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    chat_id = message.chat.id
    bot.send_message(message.chat.id, "Привет, я Oqu_bot! Я умею удаленно работать с системой Kundelik "
                                      "и помогу упростить твоё взаимодействие с ней через понятную и "
                                      "привычную всем социальную сеть Telegramm. Хочу уточнить, что "
                                      "ты можешь использовать команду /summative_marks вместе с предметом, "
                                      "чтобы получить оценки именно это данный предмет. Для этого надо в одном "
                                      "сообщении набрать команду и через пробел название предмета. Чтобы не ошибиться,"
                                      " ты можешь проверить название своих предметов с помощью функции /my_subjects."
                                      " Также, чтобы использовать функцию /login, в том же сообщении ты должен ввести"
                                      " свои данные в формате “login:mylogin password:mypassword” через пробел после"
                                      " самой команды (в одном сообщении!). Пример - «/login login:ivanivanov password:test123»."
                                      " Что ж, теперь мы точно знакомы, приятно познакомится! :wave:")


@bot.message_handler(commands=['summative_marks'], content_types=['text'])
def summative_marks(message):
    global login, password, user_token, random_answers, \
        person_id, user_id, class_id, school_id
    bot.send_message(message.chat.id, "Что ж, посмотрим на твои оценки..." + '\n')
    if len(message.text.split()) == 1:
        url = 'https://api.kundelik.kz/v2.0/edu-group/' + class_id + '/person/' + person_id + '/criteria-marks'
        res = requests.get(url, headers={'Access-Token': user_token}).json()
        for subject in res:
            bot.send_message(message.chat.id,
                             get_subject_name(class_id=class_id, user_token=user_token, subject_id=subject['subject']))
            if subject['personmarks']:
                str_marks = ''
                for mark in subject['personmarks'][0]['criteriamarks']:
                    str_marks += str(mark['value']) + ' '
                bot.send_message(message.chat.id, str_marks)
            else:
                bot.send_message(message.chat.id, 'За этот предмет нет оценок')

    elif len(message.text.split()) == 2:
        subject_name = message.text.split()[1]
        print(subject_name)
        url = 'https://api.kundelik.kz/v2.0/edu-group/' + class_id + '/person/' + person_id + '/criteria-marks'
        res = requests.get(url, headers={'Access-Token': user_token}).json()
        if not get_subject_id(subject_name=subject_name, user_token=user_token, class_id=class_id):
            bot.send_message(message.chat.id, 'Кажется ты неправильно ввел имя предмета, '
                                              'воспользуйся функцией </my_subjects> и попробуй заново.')
            return 0

        for subject in res:
            if subject['subject'] == get_subject_id(subject_name=subject_name, user_token=user_token, class_id=class_id):
                if subject['personmarks']:
                    str_marks = ''
                    for mark in subject['personmarks'][0]['criteriamarks']:
                        str_marks += 'Балл: ' + str(mark['value']) + ' дата: ' + str(mark['date'])[:10] + '\n'
                    bot.send_message(message.chat.id, str_marks)
                else:
                    bot.send_message(message.chat.id, 'За этот предмет нет оценок')


@bot.message_handler(commands=['schedule'], content_types=['text'])
def schedule(message):
    global login, password, user_token, random_answers, \
        person_id, user_id, class_id, school_id
    bot.send_message(message.chat.id, "Что у нас завтра?" + '\n')
    start_date = str(datetime.date.today() + datetime.timedelta(days=1))
    end_date = str(datetime.date.today() + datetime.timedelta(days=2))
    url = 'https://api.kundelik.kz/v2.0/persons/' + person_id + '/groups/' + class_id + '/' \
          'schedules?startDate=' + start_date + '&endDate=' + end_date
    schedule = requests.get(url, headers={'Access-Token': user_token}).json()['days'][0]['lessons']
    for lesson in schedule:
        bot.send_message(message.chat.id,str(lesson['number']) + ')' + str(lesson['hours']) + ' - ' +
                         get_lesson_information(user_token=user_token, lesson_id=lesson['id'])['subject']['name'])


@bot.message_handler(commands=['my_subjects'], content_types=['text'])
def my_subjects(message):
    global login, password, user_token, random_answers, \
        person_id, user_id, class_id, school_id
    bot.send_message(message.chat.id, "Список всех предметов твоей школы" + '\n')
    subjects = get_subject_name(class_id=class_id, user_token=user_token)
    bot.send_message(message.chat.id, 'Твои предметы:' + '\n' + '\n')
    answer = ''
    for subject in subjects:
        answer += subject['name'] + '\n'
    bot.send_message(message.chat.id, answer)



@bot.message_handler(commands=['week_grades', 'month_grades', 'day_grades'], content_types=['text'])
def week_grades(message):
    global login, password, user_token, random_answers, \
        person_id, user_id, class_id, school_id

    bad = False
    sat = False

    if message.text == '/week_grades':
        start_date = str(datetime.date.today() - datetime.timedelta(days=7))
    if message.text == '/month_grades':
        start_date = str(datetime.date.today() - datetime.timedelta(days=30))
    if message.text == '/day_grades':
        start_date = str(datetime.date.today() - datetime.timedelta(days=1))

    end_date = str(datetime.date.today())
    current_marks = show_marks_in_period(person_id=person_id, start_date=start_date,
                                         school_id=school_id, end_date=end_date, user_token=user_token)
    for mark in current_marks:
        url = 'https://api.kundelik.kz/v2.0/lessons/' + mark['lesson_str']
        subject = requests.get(url, headers={'Access-Token': user_token}).json()
        if str(mark['value']) == 'ПЛХ':
            bad = True
        if str(mark['value']) == 'УДВ':
            sat = True
        marks_answer = str(subject['subject']['name']) + ' - ' + str(mark['value'])
        bot.send_message(message.chat.id, marks_answer)

    if bad:
        bot.send_message(message.chat.id, 'Похоже на то, что у тебя есть двойки! Но не расстраивайся, '
                                          'все твои пятерки еще впереди, надо лишь приложить немного усилий!')

    if  not bad and not sat and current_marks:
        bot.send_message(message.chat.id, 'Похоже на то, что у тебя ни одной тройки и двойки! '
                                          'Машинка, что сказать. Так держать.')
    if not current_marks:
        bot.send_message(message.chat.id, 'Ты еще не успел получить ни одной оценки')


@bot.message_handler(commands=['week_attend', 'month_attend', 'day_attend'], content_types=['text'])
def attendance(message):
    global login, password, user_token, random_answers, \
        person_id, user_id, class_id, school_id
    if message.text == '/week_attend':
        start_date = str(datetime.date.today() - datetime.timedelta(days=7))
    if message.text == '/month_attend':
        start_date = str(datetime.date.today() - datetime.timedelta(days=30))
    if message.text == '/day_attend':
        start_date = str(datetime.date.today() - datetime.timedelta(days=1))

    end_date = str(datetime.date.today())
    current_attendance = show_attendance_in_period(person_id=person_id, start_date=start_date,
                                                   end_date=end_date, user_token=user_token)
    try:
        logEntries = current_attendance['logEntries']

    except Exception as e:
        bot.send_message(message.chat.id, 'Нет записей за этот период')
        return 0

    if not logEntries:
        bot.send_message(message.chat.id, 'Нет записей за этот период')
    else:
        for note in logEntries:
            status = note['status']
            subject = get_lesson_information(lesson_id=str(note['lesson']), user_token=user_token)['subject']['name']
            if status == 'Pass':
                bot.send_message(message.chat.id, 'прогулял урок: ' + subject)
            if status == 'Absent':
                bot.send_message(message.chat.id, 'пропустил урок: ' + subject)
            if status == 'NotSet':
                pass
            if status == 'Ill':
                bot.send_message(message.chat.id, 'не присутствовал по болезни: ' + subject)
            if status == 'Late':
                bot.send_message(message.chat.id, 'опоздал на урок: ' + subject)


@bot.message_handler(commands=['class_average_mark'], content_types=['text'])
def class_average_mark(message):
    global login, password, user_token, random_answers, \
        person_id, user_id, class_id, school_id

    bot.send_message(message.chat.id, 'Будет показан средний балл класса с начала года то сегодняшнего дня')
    url = 'https://api.kundelik.kz/v2.0/edu-groups/' + class_id + '/avg-marks/2020-04-01/2020-05-01'
    average_mark = requests.get(url, headers={'Access-Token': user_token}).json()
    all_marks = []
    print(average_mark)
    print(user_token)
    for student in average_mark:
        for subject in student['per-subject-averages']:
            all_marks.append(float(subject['avg-mark-value'].replace(',', '.',)))
    answer = sum(all_marks) / len(all_marks)
    url = 'https://api.kundelik.kz/v2.0/edu-groups/1565042653527550944'
    class_name = (requests.get(url, headers={'Access-Token': user_token}).json())['name']
    bot.send_message(message.chat.id, 'Средний балл класса ' + str(class_name) + ' равен ' + str(answer))


@bot.message_handler(commands=['login'], content_types=['text'])
def answer(message):
    if len(message.text.split()) == 3 and (message.text.split())[0] == '/login':
        login = (message.text.split())[1][6:]
        password = (message.text.split())[2][9:]
        print(login)
        print(password)
        try:

            dn = kundelik.KunAPI(login=login, password=password)

            user_token = dn.get_token(login=login, password=password)
            user_id = str(dn.get_info()['id'])
            person_id = str(dn.get_info()['personId'])
            data = get_user_information(user_token=user_token, user_id=user_id)
            school_id = str(data['schools'][0]['id'])
            class_id = data['eduGroups'][0]['id_str']
            bot.send_message(message.chat.id, text="Вход успешно произведен! Что ты хочешь сделать дальше?")

        except Exception as e:
            bot.send_message(message.chat.id, e)

    elif message.text == 'Спасибо!':
        bot.send_message(message.chat.id, 'Обращайся!')
    else:
        bot.send_message(message.chat.id, random.choice(random_answers))

def get_lesson_information(lesson_id, user_token):
    url = 'https://api.kundelik.kz/v2.0/lessons/' + str(lesson_id)
    res = requests.get(url, headers={'Access-Token': user_token}).json()

    return res


def get_user_information(user_token, user_id):
    url = 'https://api.kundelik.kz/v2.0/users/' + str(user_id) + '/context'
    res = requests.get(url, headers={'Access-Token': user_token})

    return json.loads(res.text)


def show_marks_in_period(person_id, school_id, start_date, end_date, user_token):
    url_mark = 'https://api.kundelik.kz/v2.0/persons/' + person_id + '/schools' \
                                                                '/' + school_id + '/marks/' + start_date + '/' \
                                                                + end_date
    res = requests.get(url_mark, headers={'Access-Token': user_token}).json()

    return res


def show_attendance_in_period(person_id, start_date, end_date, user_token):
    url = 'https://api.kundelik.kz/v2.0/persons/' + person_id + '/lesson-log-entries?startDate=' \
           + start_date + '&endDate=' + end_date
    res = requests.get(url, headers={'Access-Token': user_token}).json()

    return res


def get_subject_name(class_id, user_token, subject_id=0):
    url = 'https://api.kundelik.kz/v2.0/edu-groups/' + class_id + '/subjects'
    res = requests.get(url, headers={'Access-Token': user_token}).json()
    if subject_id == 0:
        return res
    for subject in res:
        if subject['id'] == subject_id:
            return subject['name']

    return None


def get_subject_id(subject_name, user_token, class_id):
    url = 'https://api.kundelik.kz/v2.0/edu-groups/' + class_id + '/subjects'
    res = requests.get(url, headers={'Access-Token': user_token}).json()
    for subject in res:
        if subject['name'] == subject_name:
            return subject['id']

    return False


bot.polling(none_stop=True, timeout=3.5)



