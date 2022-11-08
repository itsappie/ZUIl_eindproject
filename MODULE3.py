stt_naam = 'Leeuwarden, NL'

naam = stt_naam.split(',')[0]

import requests
import math
import psycopg2
import time
import tkinter as tk
from tkinter import *
import tkinter.font as TkFont

window = tk.Tk()
window.geometry('700x700')
window.configure(bg='#FFCC18')
font = TkFont.Font(family='NS Sans', weight='bold', size=36)
font1 = TkFont.Font(family='NS Sans', size=15)
font2 = TkFont.Font(family='NS Sans', weight='bold', size=20)

lijn = Frame(window, bg='#003082', height=3, width=700)
lijn.pack()
lijn.place(x=0, y=70)
# -------------------------- API-gedeelte ----------------------------
api_key = '1b5114c372f917b25de79aede39cf40e'
url = 'https://api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}'
stad = stt_naam


def weer(api_key, stad):
    req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={stad}&appid={api_key}').json()
    # print(req)
    dtm_td = time.strftime("\n%d-%m-%Y %H:%M\n")
    td = time.strftime("%H:%M")
    naamSt = req['name']
    T = 'Huidige Tempratuur: ' + str(math.floor(req['main']['temp'] - 273.15)) + '°C'
    GT = 'Voelt Als: ' + str(math.floor(req['main']['feels_like'] - 273.15)) + '°C'
    WS = 'Windsnelheid: ' + str(math.ceil(req['wind']['speed'] * 0.836)) + ' m/s\n'
    weer = 'Weersinformatie:'
    print(naamSt)
    print(dtm_td)
    print(T)
    print(GT)
    print(WS)
    w = tk.Label(window, text=naamSt, font=font, fg='#003082', background='#FFCC18')
    w1 = tk.Label(window, text=td, font=font, fg='#003082', background='#FFCC18')
    w2 = tk.Label(window, text=T, font=font1, fg='#003082', bg='#FFCC18')
    w3 = tk.Label(window, text=GT, font=font1, fg='#003082', bg='#FFCC18')
    w4 = tk.Label(window, text=WS, font=font1, fg='#003082', bg='#FFCC18')
    w5 = tk.Label(window, text=weer, font=font2, fg='#003082', background='#FFCC18')
    w.pack()
    w.place(x=0, y=0)
    w1.pack()
    w1.place(x=568, y=0)
    w2.pack()
    w2.place(x=0, y=135)
    w3.pack()
    w3.place(x=0, y=170)
    w4.pack()
    w4.place(x=0, y=205)
    w5.pack()
    w5.place(x=0, y=100)


weer(api_key, stad)
# --------------------------------------------------------------------


# ---------------- DB-Connectie -----------------

connect = psycopg2.connect(dbname='ZUIL', user='postgres', password='syria2004', host='localhost')
cur = connect.cursor()
x = cur.execute('SELECT * FROM station_service')


# -----------------------------------------------
def database_reader():
    keys = ['station_city', 'country', 'ov_bike', 'elevator', 'toilet', 'park_and_ride']
    dictio = {}
    for table in cur.fetchall():
        if naam in table:
            dictio['station_city'] = table[0]
            dictio['country'] = table[1]
            dictio['ov_bike'] = table[2]
            dictio['elevator'] = table[3]
            dictio['toilet'] = table[4]
            dictio['park_and_ride'] = table[5]
            if dictio['ov_bike']:
                a = 'OV-Bike aanwezig'
                a1 = tk.Label(window, text=a, font=font1, fg='#003082', bg='#FFCC18')
                a1.pack(side=BOTTOM, pady=30)
            if dictio['elevator']:
                b = 'Lift aanwezig'
                b1 = tk.Label(window, text=b, font=font1, fg='#003082', bg='#FFCC18')
                b1.pack(side=BOTTOM)
            if dictio['toilet']:
                c = 'Toilet aanwezig'
                c1 = tk.Label(window, text=c, font=font1, fg='#003082', bg='#FFCC18')
                c1.pack(side=BOTTOM)
            if dictio['park_and_ride']:
                d = 'P+R aanwezig'
                d1 = tk.Label(window, text=d, font=font1, fg='#003082', bg='#FFCC18')
                d1.pack(side=BOTTOM)

            print('\n')


database_reader()

# --------------------------- Recente Berichten ------------------------------
velden = ['naam', 'bericht', 'tijd', 'datum', 'naamStation',
          'toestemming', 'modnaam', 'mod_email', 'mod_datum', 'mod_tijd']
cur.execute('''WITH t AS (
SELECT * FROM bericht_en_meta ORDER BY datum DESC LIMIT 5
)
SELECT * FROM t ORDER BY tijd ASC;''')
recente_vijf = cur.fetchall()
lst = []
for i in recente_vijf:
    naamBr = i[0]
    bericht = i[1]
    tijd = i[2]
    datum = i[3]
    toestemming = i[5]
    # if toestemming == 1:
    rct_berichten = (naamBr + ' zegt: ' + bericht + ' - ' + tijd)
    lst.append(rct_berichten)

w6 = tk.Label(window, text='Laatste opmerkingen: ', font=font2, fg='#003082', background='#FFCC18')
w6.place(x=0, y=260)
for bericht_in_lijst in lst:
    i = tk.Label(window, text=bericht_in_lijst, font=font1, fg='#003082', bg='#FFCC18')
    i.pack()
    s = lst.index(bericht_in_lijst)
    i.place(x=0, y=295 + 35 * s)
    print(s)

# ----------------------------------------------------------------------------
window.mainloop()
