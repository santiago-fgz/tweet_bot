import csv
import pandas as pd
import numpy as np
import random
from getpass import getpass
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from msedge.selenium_tools import Edge, EdgeOptions
from Session import Session
from CSVTweetDigester import CSVTweetDigester
from MarkovTweet import MarkovTweet

def gen_titles(num_words):
    csv_tit = []
    for i in range(num_words):
        st = str(i) + '_tweets.csv'
        csv_tit.append(st)
    return csv_tit

print('Usuario')
user = input()
print('Contraseña')
pword = input()

new_tweet = ' '
print('Secion: [s] | Bot: [b] | Salir: [e]')
curr_act = input()
while curr_act != 'e':
    if curr_act == 's':
        # entrar a twitter
        print('descargar tweets: [d] | tuitear: [t] | atras: [e]')
        ses_act = input()
        while ses_act != 'e':
            if ses_act == 'd': # descargar tuits
                print('nombre del archivo txt')
                txt_title = input()
                print('palabras clave (separadas por espacios)')
                keywordStr = input()
                keywords = keywordStr.split()
                nKw = len(keywords)
                csv_titles = gen_titles(nKw)
                print('min replies')
                #min_replies = 0
                min_replies = input()
                print('min rts')
                #min_rts = 2
                min_rts = input()
                print('min likes')
                #min_likes = 5
                min_likes = input()
                print('min longitud de teto')
                #min_len_txt = 5
                min_len_txt = input()
                # declarar objetos
                session = Session(user,pword)
                session.login()
                digester = CSVTweetDigester()
                # obtener tweets, generar csv's, y transformarlos en texto normalizado
                for i in range(nKw):
                    session.tweet_selection(keywords[i],csv_titles[i])
                    digester.push_csv(csv_titles[i],min_replies,min_rts,min_likes,min_len_txt)
                # generar .txt
                digester.write_txt(txt_title)
            else:
                if ses_act == 't': # tuitear
                    print('¿tuitear?: '+new_tweet)
                    print('sí [s] | no [n]')
                    tuit_act = input()
                    if tuit_act == 's':
                        session = Session(user,pword)
                        session.login()
                        session.tweet(new_tweet)

            print('descargar tweets: [d] | tuitear: [t] | atras: [e]')
            ses_act = input()
    else:
        if curr_act == 'b':
            print('orden')
            od = input()
            od = int(od)
            tuitbot = MarkovTweet(od)
            print('Aprender texto: [a] | Tuit actual [c] | Recordar [f] | salir: [e]')
            bot_act = input()
            while bot_act != 'e':
                if bot_act == 'a':
                    print('Qué archivo?')
                    txt_name = input()
                    tuitbot.learn_text(txt_name)
                else:
                    if bot_act == 'g':
                        print('Máximo de palabras')
                        max_w = input()
                        max_w = int(max_w)
                        new_tweet = tuitbot.tweet(max_w)
                        print(new_tweet)
                    else:
                        if bot_act == 'c':
                            print(new_tweet)
                        else:
                            if bot_act == 'f': # memoria a largo plazoe
                                tuitbot.learn_text('muchos_tweets.txt')
                                tuitbot.learn_text('prueba_2.txt')
                                tuitbot.learn_text('tengo_suenio.txt')
                                tuitbot.learn_text('tweets.txt')

                print('Aprender texto: [a] | generar tuit [g] | Tuit actual [c] | salir: [e]')
                bot_act = input()

    print('Sesion: [s] | Bot: [b] | Salir: [e]')
    curr_act = input()
