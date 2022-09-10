import os
import sys

import pandas as pd
import time
from datetime import datetime
from datetime import timedelta
import mysql.connector
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# make sure the column in the database is excists this is not adding new columns

country_excode = ["EUR", "JPY", "CHF", "CAD", "AUD", "USD", "PLN", "DKK", "NOK", "SEK", "ZAR"]

dates =[]

# dates = ["2021-04-30"] #if you need load of date just add here the dates
yesterday = (datetime.today() - timedelta(days=1)).date()
dates.append(yesterday)


def Email(messages: str):

    towho = os.getenv('GROUP_EMAIL')
    s = smtplib.SMTP(host='smtp.office365.com', port=587)
    s.starttls()
    s.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
    msg = MIMEMultipart()
    msg['From'] = os.getenv('EMAIL_USER')
    msg['To'] = towho
    msg['Subject'] = "Exchange Rate Webscrape "
    msg.attach(MIMEText(messages, 'html'))
    s.send_message(msg)
    del msg
    s.quit()

def getdata():

    for k in dates:
        website = "https://xe.com/currencytables/?from=GBP&date={}#table-section".format(k)
        # read the html table
        content = pd.read_html(website)
        # get the first table
        content = pd.DataFrame(content[0])
        # filter the rows to the currency we need
        content = content[content.Currency.isin(country_excode)]
        # add the target currency name to the data
        content["Currency"] = content["Currency"].apply(lambda x: "GBP_" + str(x))
        #  drop name column
        content.drop(columns="Name", inplace=True)
        # reset the currency as the index
        content = content.set_index("Currency").T.rename_axis("Date").reset_index()
        #  add the date to the data
        content["Date"] = k
        content = content[content.index == 0]
        # check database and insert the data
        connect_the_database_to_match(content)

def connect_the_database_to_match(data):

    # Obtain connection string information from the portal
    config = {
        'host': 'test77.mysql.database.azure.com',
        'user': os.environ.get('DATABASE_LOGIN'),
        'password': os.environ.get('DATABASE_PASSWORD'),
        'database': 'test77',
    }
    # Construct connection string

    values = data.values.tolist()
    cols = data.columns.tolist()
    # checking before insert if exists then update the line where the date is the same
    # add the new column into the database to able to insert; if need different currency
    # add the new currency into the list above
    try:
        # connect to the database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        try:
            cursor.execute("Select Date from exchange_table where Date = '" + str(values[0][0]) + "'")
            isexists = [item[0] for item in cursor.fetchall()]
            # get the client number form the client table not needed DB doit on trigger need to check.
        except (mysql.connector.Error, mysql.connector.Warning, mysql.connector.errors.ProgrammingError) as e:
            Email(e) # send email if there is an error of the statement
            sys.exit()
        if not isexists:
            # if not exists then insert the data
            try:
                insert = 'insert ignore into exchange_table ({}) values ({})'.format(','.join(cols),
                                                                                     ','.join(["%s"] * len(values[0])))
                cursor.execute(insert, values[0])
            except mysql.connector.errors.ProgrammingError as e:
                Email(str(e))
            conn.commit()
            conn.close()
        else:
            try:
                k = 1
                # update the database with the new data
                for s in cols[1:]:
                    sql = "update exchange_table set {} = {} where date = '{}';".format(s, values[0][1:][k-1], values[0][0])
                    cursor.execute(sql)
                    k = k + 1
                    time.sleep(0.1)
                conn.commit()
                conn.close()
            except mysql.connector.errors.ProgrammingError as e:
                Email(str(e))
    except mysql.connector.Error as err:
        Email(str(err))


getdata()

print("done")
