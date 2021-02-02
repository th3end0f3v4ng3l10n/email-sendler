#Импортирование библиотек
import smtplib #smtp
from email.mime.multipart import MIMEMultipart #Это для сообщений
from email.mime.text import MIMEText #Это тоже для сообщений
from time import sleep #для контроля времени
import configparser #Чтобы читать конфиг
from colorama import Fore, Style #КРАСОТА
import PySimpleGUI as sg
from tkinter import *
import selenium
from selenium import webdriver
import geckodriver_autoinstaller




class Main():
    def __init__(self):
        '''Инициализация'''
        self.config = configparser.ConfigParser()
        self.config.read('config.ini') #Чтение config.ini

        self.login = self.config['MY_DATA']['login'] #берем логин из config.ini
        self.password = self.config['MY_DATA']['password'] #берем пароль из config.ini

        self.message = []
        self.subject = self.config['Message']['subject'] #Берем TITLE Из config.ini

        self.emails = []



    def create_window(self):
        layout = [
                [sg.Text('Адреса: '), sg.InputText(), sg.FileBrowse(key = '-IN-')],
                [sg.Text('Сообщение: '), sg.FileBrowse(key = '-key-')],
                [sg.Output(key='-OUT-', size=(80, 20))],
                [sg.Button('Look'),sg.Button('Sumbit'), sg.Cancel(), sg.Button('Exit')]]
        window = sg.Window('Email Sendler', layout, element_justification='center').finalize()
        window['-OUT-'].TKOut.output.config(wrap='word') # set Output element word wrapping

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                break
                window.close()

            elif event == 'Sumbit':
                with open(values['-key-'], 'r') as f:
                    for line in f:
                        self.message.append(line)

                self.message_string = ' '.join(self.message)

                print('Файл с адресами указан: ', values['-IN-'])
                with open(values['-IN-'], 'r') as f:
                    for line in f:
                        print(line.replace('\n', ''))
                        self.emails.append(line.replace('\n', ''))
                print('Все адреса успешно добавлены =)')

                print('Делаю базу яндекс адресов...')
                f = open('yandex_database.txt','w')
                database_yandex = []
                f.truncate()
                for i in self.emails:
                    if '@yandex' in i:
                        f.write(i+'\n')
                    else:
                        pass

                print('')
                print('[ + ] Начинаю отправлять сообщения...')

                for email in self.emails:
                    msg = MIMEMultipart()
                    msg['From'] = self.login
                    msg['To'] = email # ну тут понятно. Сюда тыкаем email на которой отправляем, но у нас всё в цикле for, который берет email из списка
                    msg['Subject'] = self.subject #TITLE

                    msg.attach(MIMEText(self.message_string, 'html')) #делаем сообещние
                    server = smtplib.SMTP('smtp.gmail.com: 587') #smtp
                    server.starttls()   #стартуем tls
                    server.login(msg['From'], self.password) # логинимся в smtp
                    server.sendmail(msg['From'], msg['To'], msg.as_string()) #отправляем сообщение
                    server.quit() #kill server :)
                    print('Успешно отправлено на адрес.. ', email) # название говорит само за себя
                print('<=====Успешно завершено, хорошей работы=====>')


            elif event == 'Look':
                try:
                    geckodriver_autoinstaller.install()
                except:
                    print("Драйвер не установлен. Свяжитесь с кодером или с ")
                print('Message Preview')
                driver = webdriver.Chrome()
                driver.get('file://'+values['-key-'])

            elif event == 'Exit':
                break
        window.close()





def use_all():
    root = Main()
    root.create_window()

    #root.function()
use_all()
