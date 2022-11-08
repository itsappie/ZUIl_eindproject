"""
    Alle invoer wordt gesorteerd en opgeslagen in een dictionary

    [DONE] * {'Bericht': 'waarde(len = 140)'} = De reiziger moet een invoervakje krijgen om zijn bericht in te
    voeren met een limitatie van 140 karakters, alles wat na die 140 karakters wordt ingetypt wordt
    niet opgeslagen en weergegeven.

    [DONE] * {'naam': 'waarde'/anoniem'} = De reiziger moet een invoervakje krijgen om zijn naam in te
    voeren, indien de invoer leeg is dan wordt de waarde 'anoniem' aan de sleutel 'naam' gehecht.

    [DONE] * {'stationNaam': 'waarde (random)'} = .randomsample moet drie stations kiezen uit de lijst
    en daaruit moet randomchoice één station kiezen. Om gebruik te maken van randomsample en randomchoice moet je de
    randombibliotheek importeren.

    [DONE] * {'datum_tijd': 'waarde'} = Uit de datetime- en timebibliotheek de huidig datum en tijd hechten aan de
    datumwaarde in de dictionary.

    Nadat alle gegevens opgeslagen zijn in een dictionary moeten die gegevens in een csv-vorm komen. Dat is te doen met
    de csv-bibliotheek.
"""

import random
import time
import string
import csv

metadata_en_bericht = {}
meb = []
velden = ['naam', 'bericht', 'tijd', 'datum', 'naamStation']


def bericht():
    status = 1
    file = open('Stationsnamen.txt', 'r+')
    stt_namen_lst = file.read().split('\n')
    drie_rndm_stt = random.sample(stt_namen_lst, 3)
    rnd_stt = random.choice(drie_rndm_stt)
    file.close()

    scherm = open('Module3Stationshalscherm.py', 'r+')
    scherm.write('stt_naam = ' + "'" + rnd_stt + "," + " NL" + "'\n")
    scherm.close()

    tijd = time.strftime('%H:%M')
    datum = time.strftime('%d-%m-%Y')
    print(tijd + ' | ' + datum + ' | U bevindt zich op station: ' + rnd_stt + '\n')

    while status > 0:
        vraagbericht = input('Wij waarderen we uw mening.'
                             ' \nWilt u een bericht achterlaten? ')
        if vraagbericht == 'Ja' or vraagbericht == 'ja':
            bericht_raw = input('\nVoer hier uw bericht in: ')
            bericht_trimmed = bericht_raw[:139]
            metadata_en_bericht['rnd_nr'] = {}
            metadata_en_bericht['rnd_nr']['bericht'] = bericht_trimmed

            vraagnaam = input('\nWilt u, uw naam hierbij invullen? ')
            if vraagnaam == 'Ja' or vraagnaam == 'ja':
                naam = string.capwords(input('\nVoer hier uw naam in: '))
                metadata_en_bericht['rnd_nr']['tijd'] = tijd
                metadata_en_bericht['rnd_nr']['datum'] = datum
                metadata_en_bericht['rnd_nr']['naam'] = naam
                metadata_en_bericht['rnd_nr']['naamStation'] = rnd_stt
                meb.append(metadata_en_bericht['rnd_nr'])
                print('\n------------------Bedankt!-----------------\n\n\n\n\n')

                csvfile = open('Bericht_&_metadata.csv', 'w')
                writer = csv.DictWriter(csvfile, fieldnames=velden)
                writer.writeheader()
                writer.writerows(meb)
                csvfile.close()
                bericht()

            if vraagnaam == 'Nee' or vraagnaam == 'nee':
                naam = 'Anoniem'
                metadata_en_bericht['rnd_nr']['tijd'] = tijd
                metadata_en_bericht['rnd_nr']['datum'] = datum
                metadata_en_bericht['rnd_nr']['naam'] = naam
                metadata_en_bericht['rnd_nr']['naamStation'] = rnd_stt
                print('\n------------------Bedankt!-----------------\n\n\n\n\n')
                meb.append(metadata_en_bericht['rnd_nr'])

                csvfile = open('Bericht_&_metadata.csv', 'w')
                writer = csv.DictWriter(csvfile, fieldnames=velden)
                writer.writeheader()
                writer.writerows(meb)
                csvfile.close()
                bericht()

        if vraagbericht == 'Nee' or vraagbericht == 'nee':
            print('\nBedankt!')


bericht()


def schrijven():
    csvfile = open('Bericht_&_metadata.csv', 'w', newline='')
    writer = csv.DictWriter(csvfile, fieldnames=velden)
    writer.writeheader()
    for dictio in meb:
        writer.writerows(dictio)


schrijven()
