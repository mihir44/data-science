import os
import traceback
from imbox import Imbox
import mysql.connector
import pymongo
import gridfs
# Mongodb connection
def mongoConn():
    try:
        connection = pymongo.MongoClient(host='127.0.0.1', port=27017)
        return connection.grid_file
    except Exception as e:
        print("Error: ",e)

filedb = mongoConn()

db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="mihir123",
  database="invoice"
)

dbCursor = db.cursor()

host = "imap.gmail.com"
username = "aim2care29@gmail.com"
password = 'Aim2Care@123'
download_folder = "download"

if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)

mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)
messages = mail.messages(unread=True) 
for (uid, message) in messages:
    mail.mark_seen(uid) # optional, mark message as read
    data = message.body['plain'][0]
    data = data.split('\r\n')
    details = list(filter(lambda x : len(x) > 0, data))
    obj = {}
    obj['company'] = details[0]
    obj['date'] = details[1][details[1].index(":")+2:]
    obj['invoiceNum'] = details[2][details[2].index(":")+2:]
    obj['order'] = details[3][details[3].index(":")+2:]
    obj['address'] = details[4][details[4].index(":")+2:]
    dbCursor.execute(f""" insert into invoice_data (company, dateOrdered, invoiceNumber, itemOrdered, address) values 
    ('{obj["company"]}','{obj["date"]}','{obj["invoiceNum"]}','{obj["order"]}','{obj["address"]}')""")
    db.commit()
    print("data inserted")
    if(len(message.attachments) != 0):
        for idx, attachment in enumerate(message.attachments):
            try:
                att_fn = attachment.get('filename')
                download_path = f"{download_folder}/{att_fn}"
                print(download_path)
                with open(download_path, "wb") as fp:
                    fp.write(attachment.get('content').read())
                file_data = open(download_path,'rb')
                file = file_data.read()
                fs = gridfs.GridFS(filedb)
                fs.put(file, filename = att_fn)
            except:
                print(traceback.print_exc())
    else:
        print("No file found")
mail.logout()