import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from time import time
from datetime import datetime, time

import random
import time

import requests
from bs4 import BeautifulSoup

vk_session = vk_api.VkApi(token='5dd42713ad38fae2ebe6382d7d4004220a481beaae995e4f589e3d9d341b9bdffe0b08c6f0eba82e73987')
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

check = False
main_check = False

class User():
    def __init__(self, id, name, form, letter, access, mode):
        self.id = id
        self.name = name
        self.form = form
        self.letter = letter
        self.access = access
        self.mode = mode

days = {"понедельник": 'pnd', "вторник": 'vtr', "среда": 'srd', "четверг": 'tht', 'пятница': 'ptn', "суббота": 'sbb', \
        "пн": 'pnd', "вт": 'vtr', "ср": 'srd', "чт": 'tht', 'пт': 'ptn', "суб": 'sbb', \
        0:'pnd', 1: 'vtr', 2: 'srd', 3: 'tht', 4: 'ptn', 5: 'sbb', 6: 'pnd', 7: 'pnd'}
days_eng = ["Monday", "Tuesday", "Wednesday", "Thursday", 'Friday', "Saturday", "Sunday"]
numbers = ['5','6','7','8','9','10','11']
letters = ['а', 'б', 'в', 'г', 'д']
letters = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g'}
subjects = ['русский', 'английский', 'матеша', '1']
users = []
HEADERS = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; AskTB5.6)', 'accept': '*/*'}

URL_for_vip = "http://showid.ru/names/{0}".format(id)

def check_registration(id):
    members = vk_session.method('groups.getMembers', {'group_id': 192828594})['items']
    return True

def sender(session_api, peer_id, message, keyboard=None):
    session_api.messages.send(peer_id=peer_id, message=message, keyboard=keyboard, random_id=random.randint(-20000, +200000))
    time.sleep(0.2)

def get_name(id):
    data = vk_session.method("users.get", {"user_ids": id})[0]
    return "{0} {1}".format(data["first_name"], data["last_name"])

def get_keyboard(buts): # функция создания клавиатур
	nb = []
	color = ''
	for i in range(len(buts)):
		nb.append([])
		for k in range(len(buts[i])):
			nb[i].append(None)
	for i in range(len(buts)):
		for k in range(len(buts[i])):
			text = buts[i][k][0]
			color = {'зеленый' : 'positive', 'красный' : 'negative', 'синий' : 'primary', 'белый' : 'secondary'}[buts[i][k][1]]
			nb[i][k] = {"action": {"type": "text", "payload": "{\"button\": \"" + "1" + "\"}", "label": f"{text}"}, "color": f"{color}"}
	first_keyboard = {'one_time': False, 'buttons': nb}
	first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
	first_keyboard = str(first_keyboard.decode('utf-8'))
	return first_keyboard

def timetable(session_api, peer_id, keyboard = None):
    global URL
    global URL_optional
    global use_url
    global day
    for user in users:
        form = user.form + user.letter

    URL = 'http://orichisc.edu.ru/timetable/timetable/{0}/{1}_{0}.hrasp'.format(day, form)
    URL_optional = 'http://orichisc.edu.ru/timetable/timetable/{0}/{1}_{0}_v.hrasp'.format(day, form)
    use_url = URL
    parse_timetable()
    use_url = URL_optional
    parse_timetable()
    return

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    if soup.find('table') != None:
        items = soup.find('table').get_text(strip=True)
        table = str(items)
        sender(session_api, peer_id=id, message=table.replace('#ПредметКабинетВремя', '').replace('НД','').replace("1", '1 ').replace("2", '\n2 ').replace("3", '\n3 ').replace("4", '\n4 ').replace("5", '\n5 ').replace("6", '\n6 ').replace("7", '\n7 ').replace("8", '\n8 ').replace("9", '\n9 '), keyboard=main)
        if str(soup)[str(soup).find('Примечания: </b>'):str(soup).rfind('br/')-1].replace('</b>','') != '':
            sender(session_api, peer_id=id, message=str(soup)[str(soup).find('Примечания: </b>'):str(soup).rfind('br/')-1].replace('</b>',''))
        else:
            sender(session_api,peer_id=id, message='Примачаний не указано')
        return
    if soup.find('table') == None:
        if use_url == URL:
            sender(session_api, peer_id=id, message='Расписания нет', keyboard=main)
        else:
            sender(session_api, peer_id=id, message='Изменений нет', keyboard=main)
        return

def get_html(url, params = None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

def parse_timetable():
    html = get_html(use_url)
    if html.status_code == 200:
        get_content(html.text)
        pass
    else:
        sender(session_api, peer_id=id, message='Не удалось выполнить запрос', keyboard=main)
        pass

timetable_main = get_keyboard([
	[('Пн', 'белый'), ('Вт', 'белый'), ('Ср', 'белый'), ('Чт', 'белый'), ('Пт', 'белый'), ('Суб', 'белый')]
])

def create_keyboard_day(msg):
    keyboard_day = VkKeyboard(one_time=True)
    if msg != '':
        keyboard_day.add_button('ПН', color=VkKeyboardColor.PRIMARY)
        keyboard_day.add_button('ВТ', color=VkKeyboardColor.PRIMARY)
        keyboard_day.add_button('СР', color=VkKeyboardColor.PRIMARY)
        keyboard_day.add_line()
        keyboard_day.add_button('ЧТ', color=VkKeyboardColor.PRIMARY)
        keyboard_day.add_button('ПТ', color=VkKeyboardColor.PRIMARY)
        keyboard_day.add_button('СУБ', color=VkKeyboardColor.PRIMARY)
        keyboard_day = keyboard_day.get_keyboard()
        return keyboard_day

main = get_keyboard([
	[('Расписание', 'белый'), ('Завтра', 'белый'), ('Мой класс','белый')]
])

def create_keyboard_numbers(msg):
    keyboard_numbers = VkKeyboard(one_time=True)
    if msg != '':
        keyboard_numbers.add_button('5', color=VkKeyboardColor.PRIMARY)
        keyboard_numbers.add_button('6', color=VkKeyboardColor.PRIMARY)
        keyboard_numbers.add_button('7', color=VkKeyboardColor.PRIMARY)
        keyboard_numbers.add_button('8', color=VkKeyboardColor.PRIMARY)
        keyboard_numbers.add_line()
        keyboard_numbers.add_button('9', color=VkKeyboardColor.PRIMARY)
        keyboard_numbers.add_button('10', color=VkKeyboardColor.PRIMARY)
        keyboard_numbers.add_button('11', color=VkKeyboardColor.PRIMARY)
        keyboard_numbers.add_button('Назад', color=VkKeyboardColor.PRIMARY)
        keyboard_numbers = keyboard_numbers.get_keyboard()
        return keyboard_numbers

keyboard_letters = get_keyboard([
    [('А', "белый"), ('Б', "белый"), ('В', "белый"), ('Г', "белый")]
])

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:

            id = event.user_id
            msg = event.text.lower()
            keyboard_day = create_keyboard_day(msg)
            keyboard_numbers = create_keyboard_numbers(msg)

            print(str(datetime.now())[0:19], get_name(id), '-' ,msg)

            if msg == "начать":
                print(str(datetime.now())[0:19], event.raw)
                if check_registration(id):
                    flag = 0
                    for user in users:
                        if user.id == id:
                            flag = 1
                            break
                    if not(flag):
                        print(str(datetime.now())[0:19], 'user created -', get_name(id), 'https://vk.com/id'+str(id))
                        users.append(User(id=id, name=get_name(id), form='', letter='', access='vip', mode= 'main'))
                        sender(session_api, peer_id=id, message='Вы успешно зарегались в системе!\nНе забудь указать свой класс.', keyboard=main)
                    elif flag:
                        # print(flag)
                        for user in users:
                            if user.id == id:
                                # print('есть подписка')
                                # print(users)
                                user.mode = 'main'
                else:
                    sender(session_api, peer_id=id, message='Вы не подписаны D:')
            else:
                for user in users:
                    if user.id == id:

                        if user.mode == 'main':
                            if msg == 'расписание':
                                if user.letter != '':
                                    sender(session_api, id, message='Выберите день', keyboard=keyboard_day)
                                    user.mode = 'timetable_main'
                                else:
                                    sender(session_api, id, message='Укажите, пожалуйста, ваш класс в настройках', keyboard=main)

                            if msg == 'мой класс':
                                message = 'Ваш класс: ' + user.form + user.letter + '\nЕсли желаете поменять класс - выберите число на клавиатуре.\
                                                                                \nЧтобы вернуться в главное меню - нажмите на кнопку "Назад"'
                                sender(session_api, id, message=message, keyboard=keyboard_numbers)
                                user.mode = 'choose_number'

                            if msg == 'завтра':
                                if user.letter != '':
                                    current_date = datetime.now().strftime('%A')
                                    day = (days_eng.index(current_date) + 1) % 7
                                    day = days[day]
                                    timetable(session_api, peer_id=id)
                                    user.mode = 'main'
                                else:
                                    sender(session_api, id, message='Укажите, пожалуйста, ваш класс в настройках', keyboard=main)

                        elif user.mode == 'timetable_main':
                            if msg in days:
                                day = days[msg]
                                timetable(session_api, peer_id=id)
                                user.mode = 'main'
                            else:
                                user.mode = 'main'
                                sender(session_api, peer_id=id, message='такого дня нет', keyboard=main)

                        elif user.mode == 'choose_number':
                            if msg in numbers:
                                sender(session_api, id, message='Напиши букву', keyboard=keyboard_letters)
                                user.mode = 'choose_letter'
                                user.form = msg
                            elif msg == 'назад':
                                sender(session_api, id, message='Вы в главном меню', keyboard=main)
                                user.mode = 'main'
                            else:
                                sender(session_api, id, message='Ты дурак? Такого класса нет', keyboard=main)
                                user.mode = 'main'

                        elif user.mode == 'choose_letter':
                            if msg in letters:

                                user.letter = letters[msg]
                                message = 'Класс успешно изменен! Вы в ' + user.form + user.letter
                                sender(session_api, id, message=message, keyboard=main)
                                user.mode = 'main'
                            else:
                                sender(session_api, id, message='Ты дурак? Такого класса нет', keyboard=main)
                                user.mode = 'main'