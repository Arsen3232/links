import sqlite3
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash


try:
    connect = sqlite3.connect('mydatabase.db', check_same_thread=False)
    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE if not exists "users" (
        "id"	INTEGER NOT NULL,
        "login"	TEXT NOT NULL UNIQUE,
        "password"	TEXT NOT NULL UNIQUE,
        PRIMARY KEY("id" AUTOINCREMENT)
    ); ''')
    connect.commit()

    cursor.execute('''CREATE TABLE if not exists "links" (
	"id"	INTEGER UNIQUE,
	"long"	INTEGER,
	"short"	TEXT,
	"access"   INTEGER,
	"count"	INTEGER,
	"owner"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT)
); ''')
    connect.commit()

    cursor.execute('''CREATE TABLE if not exists "access" (
	"id"	INTEGER UNIQUE,
	"access"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
    ); ''')
    connect.commit()



    def authorization(login, pswrd):
        res = cursor.execute('''select * from users where login=?''', (login,)).fetchone()
        if len(res) > 1 and check_password_hash(res[2], pswrd):
            return res
        return res

    def register(login, pswrd):
        check = cursor.execute('''SELECT * FROM users WHERE login=?''',(login, )).fetchall()
        if len(check) < 1:
            cursor.execute('''INSERT INTO users (login, password) VALUES(?,?)''', (login, pswrd,))
            connect.commit()
            return True
        else:
            return False

    def getUser(user_id):
        res = cursor.execute('''SELECT * FROM users WHERE id=?''', (user_id,)).fetchone()
        if not res:
            return False
        return res

    def addLinks(id, long_link, short_link, level):
        level = level
        check = cursor.execute('''SELECT * FROM links WHERE long=?''',(long_link, )).fetchall()
        if len(check) < 1:
            cursor.execute('''INSERT INTO links (long, short, access, count, owner) VALUES(?,?,?,?,?)''', (long_link, short_link, level, 0, id,))
            connect.commit()
            flash('Ссылка успешно создана')
            return True
        else:
            cursor.execute('''INSERT INTO links (long, short, access, count, owner) VALUES(?,?,?,?,?)''',
                        (long_link, short_link, level, 0, id,))
            connect.commit()
            return True
        
    
    def UpdateLink(id, long_link, short_link, access):
        cursor.execute('''UPDATE links SET long=?, short=?, access=? WHERE id=?''',(long_link, short_link, access, id , ))
        connect.commit()
        flash('Запись успешно изменена')
        return 'Запись успешно изменена'
        


    def checkLinks(short_link):
        res = cursor.execute('''SELECT * FROM links WHERE short=? LIMIT 1''',(short_link, )).fetchall()
        return res

    def searchLinks(id_owner):
        res = cursor.execute('''SELECT * FROM links WHERE owner=?''',(id_owner, )).fetchall()
        return res

    def updateCount(id, count):
        count = count + 1
        cursor.execute('''UPDATE links SET count=? WHERE id=?''',(count, id, ))
        connect.commit()

    def getAccess():
        res = cursor.execute('''SELECT * FROM access''').fetchall()
        return res
    
    def getLinks(id):
        res = cursor.execute('''SELECT * FROM links WHERE id=?''',(id , )).fetchall()
        print(res)
        return res
    
    def delLinks(id):
        cursor.execute('''DELETE FROM links WHERE id=?''',(id, ))
        connect.commit()
        flash('Запись успешно удалена')
        return 'Запись удалена'



except sqlite3.Error as error:
    print('Ошибка при подключении к sqlite', error)



