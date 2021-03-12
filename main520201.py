import requests
from bs4 import BeautifulSoup as BS
import re
import sqlite3
import telebot
from time import sleep
import traceback

bot = telebot.TeleBot("1486092253:AAFVMoBeQ5MTKL0kNSiCocp7dVmayYPwNoY")
while True:
    try:
        link = 'http://m.flashscore.ru'
        mass = [ ]
        r = requests.get ( 'http://m.flashscore.ru/basketball/?s=2' )
        soup = BS ( r.content , 'html.parser' )

        for i in soup.findAll ( 'div' , id='score-data' ) :
            for k in i.findAll ( 'a' ) :
                mass.append ( k.get ( 'href' ) )

        for i in mass :
            r = requests.get ( link + i )
            soup = BS ( r.content , 'html.parser' )

            for bib in soup.findAll ( 'h3' ) :
                name = bib.text
                name = name.replace ( "'" , "" )
                print ( name )
            a = soup.findAll ( 'div' , class_='detail' ) [ 0 ].text
            a = a.split ( ' ' )
            a = a [ 2 ]
            a = a.replace ( '(' , '' )
            a = a.replace ( ')' , '' )
            a = a.split ( ',' )
            scores = a
            print ( scores )
            c = False
            col = 0

            status = soup.findAll ( 'span' , class_='live' ) [ 1 ].text
            if len ( scores ) == 2 :
                for k in range ( 2 ) :
                    game = scores [ k ]
                    game = game.split ( ':' )
                    if game [ 0 ] > game [ 1 ] :
                        col += 1
                    else :
                        col -= 1
            if (col == -2) or (col == 2) :
                c = True

            with sqlite3.connect ( 'server.db' ) as conn :
                cursor = conn.cursor ()
                # print(name)
                result = cursor.execute ( f"SELECT names FROM live WHERE names = '{name}'" )
                res = 0
                if result.fetchone () == None :
                    if ('(Ж)' not in name) and (len ( scores ) == 2) and (c == True) and (status == "Перерыв") :
                        cursor.execute (
                            f"""INSERT INTO live(names,href) VALUES ('{str ( name )}','{str ( link ) + str ( i )}')""" )
                        conn.commit ()
                        if col == -2 :
                            message = bot.send_message ( "@mlg_betbot" , name + "\n" + scores [ 0 ] + " " + scores [
                                1 ] + " \nСтавка: П1 (1%) в 3 четверти\nВ случае поражения ставить на 4 четверть П2 (2.5%)" )
                            res = 1
                        elif col == 2 :
                            message = bot.send_message ( "@mlg_betbot" , name + "\n" + scores [ 0 ] + " " + scores [
                                1 ] + " \nСтавка: П2 (1%) в 3 четверти\nВ случае поражения ставить на 4 четверть П1 (2.5%)" )
                            res = 2
                        cursor.execute ( f"UPDATE live SET message_id = {message.message_id},result={res} WHERE names = '{name}'" )
                        conn.commit()
                cursor.execute ( f"SELECT href FROM live" )
                qq = cursor.fetchall ()
                for m in qq :
                    linkend = m [ 0 ]
                    rer = requests.get ( linkend )
                    soupes = BS (rer.content , 'html.parser')
                    cursor.execute ( f"SELECT message_id FROM live WHERE href = '{linkend}'" )
                    qq = cursor.fetchone ()
                    message_id = qq[0]
                    kom = 0
                    for i in soupes.findAll ( 'div' , class_='detail' ):
                        kom += 1
                        if kom == 2:
                            statuses = i.text
                    if statuses == 'Завершен' :
                        a = soupes.findAll ( 'div' , class_='detail' ) [ 0 ].text
                        a = a.split ( ' ' )
                        a = a [ 2 ]
                        a = a.replace ( '(' , '' )
                        a = a.replace ( ')' , '' )
                        a = a.split ( ',' )
                        scoreses = a
                        qq = cursor.execute(f"SELECT result FROM live WHERE href = '{linkend}'").fetchone()
                        k = False
                        print(qq[0])
                        print(scoreses[2])
                        if k == False:
                            resu = scoreses[2]
                            resu = resu.split(':')
                            if ((qq[0] == 1) and (resu[qq[0]-1] > resu[qq[0]])) or ((qq[0] == 2) and (resu[qq[0]-2]) < (resu[qq[0]-1]) ):
                                bot.edit_message_text ( "Победа ✅✅✅\n"+names , "@mlg_betbot" , message_id )
                            else:
                                resu = scoreses [ 3 ]
                                resu = resu.split ( ':' )
                                if ((qq[0] == 1) and (resu[qq[0]-1] > resu[qq[0]])) or ((qq[0] == 2) and (resu[qq[0]-2]) < (resu[qq[0]-1]) ) :
                                    bot.edit_message_text ( "Победа ✅✅✅\n"+names , "@mlg_betbot" , message_id )
                                else:
                                    bot.edit_message_text ( "Поражение ❌❌❌\n"+names , "@mlg_betbot" , message_id )

                        cursor.execute(f"DELETE FROM live WHERE href ='{linkend}'")
                        conn.commit()
                        #bot.edit_message_text ( "Новый автомат" , "@mlg_betbot" , message_id )

        sleep ( 10 )
    except:
        print("-----------------------------------------------------------\n"
              "-------Произошла ошибка, программа продолждает работу------\n"
              "-----------------------------------------------------------")
        traceback.print_exc()
        sleep(30)


        # for b in soup.findAll('div', id='detail-tab-content'):
        # for k in b.findAll('h4'):
        # print(k.text)

    # print("Запущен!")


