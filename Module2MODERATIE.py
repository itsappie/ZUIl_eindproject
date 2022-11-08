import csv
import time
import psycopg2
from random import *

Database_host = 'localhost'
Database_name = 'ZUIL'
Database_user = 'postgres'
passw = 'syria2004'

connect = psycopg2.connect(dbname=Database_name, user=Database_user, password=passw, host=Database_host)
connect.autocommit = True
cur = connect.cursor()
cur.execute('ALTER TABLE bericht_en_meta DROP COLUMN IF EXISTS id;')
lst = []
keuzemenu = input('Wilt u (i)inloggen of (r)registreren: ')


def inloggen():
    moderatie_dtm = time.strftime('%m/%d/%Y')
    moderatie_td = time.strftime('%H:%M:%S')
    mod_email = input('Voer uw e-mail in: ')
    mod_ww = input('Voer je wachtwoord in: ')
    cur.execute('SELECT * FROM "Moderator"')
    modlijst = cur.fetchall()

    for mod in modlijst:
        if mod_email in mod:
            if mod_ww in mod:
                with open('Bericht_&_metadata.csv', 'r+') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        lst.append(row)
                    for r in lst:
                        print('Bericht: ' + r['bericht'])
                        toestemming = input('Toestaan? ')
                        if toestemming == 'ja' or 'Ja':
                            r['toestemming'] = 1
                            r['mod_email'] = mod_email
                            r['mod_datum'] = moderatie_dtm
                            r['mod_tijd'] = moderatie_td
                            print('\n')
                        if toestemming == 'nee' or 'Nee':
                            r['toestemming'] = 0
                            r['mod_email'] = mod_email
                            r['mod_datum'] = moderatie_dtm
                            r['mod_tijd'] = moderatie_td
                            print('\n')

            else:
                print('gegevens niet correct! ')
            f = open('Bericht_&_metadata.csv', 'w+')
            f.close()


def registreren():
    nieuwe_mod_lst = []
    MODdict = {}
    mod_velden = ['naam', 'Email', 'modID', 'wachtwoord']

    nieuwe_mod_naam = input('Voer je naam in: ')
    nieuwe_mod_email = input('Voer je E-mail in: ')
    nieuwe_mod_ww = input('Voer een wachtwoord in: ')
    MODdict['naam'] = nieuwe_mod_naam
    MODdict['Email'] = nieuwe_mod_email
    MODdict['wachtwoord'] = nieuwe_mod_ww
    MODdict['modID'] = int(randrange(100))
    nieuwe_mod_lst.append(MODdict)
    file = open('moderators.csv', 'w', newline='')
    writer = csv.DictWriter(file, fieldnames=mod_velden)
    writer.writeheader()
    for dictio in nieuwe_mod_lst:
        writer.writerow(dictio)
    file.close()

    modfile = open('moderators.csv', 'r')
    next(modfile)
    cur.copy_from(modfile, "Moderator", sep=',')
    # cur.execute('ALTER TABLE "Moderator" ADD COLUMN modID SERIAL PRIMARY KEY;')
    connect.commit()
    file.close()
    print('Registreren gelukt! \n\nLog nu in: \n')
    inloggen()


if keuzemenu == 'i':
    inloggen()
if keuzemenu == 'r':
    registreren()
# ------------------------------------------------------------
velden = ['naam', 'bericht', 'tijd', 'datum', 'naamStation',
          'toestemming', 'mod_email', 'mod_datum', 'mod_tijd']

csvfile = open('MOD_Berichten.csv', 'w', newline='')
writer = csv.DictWriter(csvfile, fieldnames=velden)
writer.writeheader()
for dictio in lst:
    writer.writerow(dictio)
csvfile.close()

# -----------------SQL-Gedeelte-----------------

Database_host = 'localhost'
Database_name = 'ZUIL'
Database_user = 'postgres'
passw = 'syria2004'

connect = psycopg2.connect(dbname=Database_name, user=Database_user, password=passw, host=Database_host)
connect.autocommit = True
cur = connect.cursor()


# cur.execute('DROP TABLE bericht_en_meta')
# cur.execute('CREATE TABLE bericht_en_meta (naam VARCHAR, bericht VARCHAR,\
#   tijd VARCHAR, datum VARCHAR, naamStation VARCHAR,\
#   toestemming VARCHAR, mod_email VARCHAR,\
#   mod_datum VARCHAR, mod_tijd VARCHAR);')
# connect.commit()


def fun1():
    f = open('MOD_Berichten.csv', 'r')
    next(f)  # Skip the header
    cur.copy_from(f, 'bericht_en_meta', sep=',')
    cur.execute('ALTER TABLE bericht_en_meta ADD COLUMN id SERIAL PRIMARY KEY;')
    connect.commit()
    connect.close()

    f.close()
    f = open('MOD_Berichten.csv', 'w+')
    f.close()


fun1()
