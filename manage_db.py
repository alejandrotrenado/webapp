import mysql.connector

def check_db():

    dbconfig = {'host': '127.0.0.1', 
                'user': 'root', 
                'password': 'M4n0l0My$QL',}

    myconn = mysql.connector.connect(**dbconfig)

    mycursor = myconn.cursor(buffered=True)

    mycursor.execute("SHOW DATABASES")


    if ("search_log",) not in mycursor:
        mycursor.execute("CREATE DATABASE search_log")
        myconn.commit()

    #end connection

    mycursor.close()
    myconn.close()
    check_tables()

def check_tables():
    dbconfig = {'host': '127.0.0.1', 
                'user': 'root', 
                'password': 'M4n0l0My$QL', 
                'database': 'search_log',}
    myconn = mysql.connector.connect(**dbconfig)

    mycursor = myconn.cursor(buffered = True)


    mycursor.execute("SHOW TABLES")

    tables = []

    for x in mycursor:
        tables.append(x[0])
    

    if "users" not in tables:
        
        mycursor.execute("CREATE TABLE users \
                            (id INT AUTO_INCREMENT PRIMARY KEY,\
                            mail VARCHAR(255),\
                            pwd VARCHAR(255))")
        myconn.commit()
        print("creada tabla users")

    if "log" not in tables:
        mycursor.execute("CREATE TABLE log \
                            (id INT AUTO_INCREMENT PRIMARY KEY,\
                            ts timestamp default current_timestamp,\
                            phrase varchar(128),\
                            letters varchar(32),\
                            ip varchar(16) not null,\
                            browser_string varchar(256) not null,\
                            results varchar(64) not null,\
                            user_id INT,\
                            FOREIGN KEY(user_id) REFERENCES users(id) ) ")
        myconn.commit()
        print("creada tabla log")

    if "counter" not in tables:
        mycursor.execute("CREATE TABLE counter \
                            (visit INT,\
                            user_id INT,\
                            FOREIGN KEY(user_id) REFERENCES users(id) ) ")
        myconn.commit()
        print("creada tabla counter")

    mycursor.close()
    myconn.close()

if __name__ == "__main__":
    check_db()
