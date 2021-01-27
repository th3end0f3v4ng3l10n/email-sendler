#Импортирование библиотек
import smtplib #smtp
from email.mime.multipart import MIMEMultipart #Это для сообщений
from email.mime.text import MIMEText #Это тоже для сообщений
from time import sleep #для контроля времени
import configparser #Чтобы читать конфиг
from colorama import Fore, Style #КРАСОТА
import PySimpleGUI as sg
from tkinter import *
class Interface():
    def main_window(self):
        layout = [
                [sg.Text('Адреса: '), sg.InputText(), sg.FileBrowse()],
                [sg.Output(key='-OUT-', size=(80, 20))],
                [sg.Button('Sumbit'), sg.Cancel(), sg.Button('Exit')]]
        window = sg.Window('Game Finder', layout, element_justification='center').finalize()
        window['-OUT-'].TKOut.output.config(wrap='word') # set Output element word wrapping


        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
                window.close()
            elif event == 'Sumbit':
                root = Main()
                root.create_yandex_database()
                root.function()
            elif event == 'Exit':
                break
        window.close()

class Main():
    def __init__(self):
        '''Инициализация'''
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') #Чтение config.ini

        self.login = self.config['MY_DATA']['login'] #берем логин из config.ini
        self.password = self.config['MY_DATA']['password'] #берем пароль из config.ini

        self.message = self.config['Message']['msg'] #Берем сообещние из config.ini
        self.subject = self.config['Message']['subject'] #Берем TITLE Из config.ini

        self.emails = []

        with open('emails') as f:
            for line in f:
                self.emails.append(line.replace('\n',''))


    def create_yandex_database(self):
        '''Создаёт базу из yandex доменов'''
        f = open('yandex_database.txt','w')
        database_yandex = []
        f.truncate()
        for i in self.emails:
            if '@yandex' in i:
                f.write(i+'\n')

            else:
                pass


        f.close()

    def function(self):
        '''Функция отправляет сообщения'''
        def krasota(email):
            '''Самая красивая функция....'''
            print('[',Fore.GREEN +'+', Style.RESET_ALL+']'," Успешно отправлено на почту... {}".format(email))

        for email in self.emails: #для каждого email в списке self.emails
            msg = MIMEMultipart()
            msg['From'] = self.login
            msg['To'] = email # ну тут понятно. Сюда тыкаем email на которой отправляем, но у нас всё в цикле for, который берет email из списка
            msg['Subject'] = self.subject #TITLE

            msg.attach(MIMEText(self.message, 'plain')) #делаем сообещние
            server = smtplib.SMTP('smtp.gmail.com: 587') #smtp
            server.starttls()   #стартуем tls
            server.login(msg['From'], self.password) # логинимся в smtp
            server.sendmail(msg['From'], msg['To'], msg.as_string()) #отправляем сообщение
            server.quit() #kill server :)
            krasota(email) # название говорит само за себя
def use_all():
    #root = Main()
    #root.function()
    #root.create_yandex_database()
    interface = Interface()
    interface.main_window()
use_all()
