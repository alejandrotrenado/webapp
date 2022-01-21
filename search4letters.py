import mysql.connector
from DBcm import UseDatabase

def search4letters(phrase,letters):
    return set(letter for letter in phrase if letter in letters)

# def log_request(req,res):
#     with open("search.log", "a") as log:
#         print(req.form, req.remote_addr, req.user_agent, res, 
#                 file=log, sep='|')

def log_request(req,res):
    dbconfig = {'host': '127.0.0.1', 
                'user': 'root', 
                'password': 'M4n0l0My$QL', 
                'database': 'search_log',}

    with UseDatabase(dbconfig) as cursor:
        _SQL= """insert into log (phrase, letters, ip, browser_string, results) VALUES (%s, %s, %s, %s, %s);"""
        cursor.execute(_SQL,(req.form["phrase"], req.form["letters"], req.remote_addr,str(req.user_agent),res))

if __name__ == "__main__":
    print(search4letters("hola", "aou"))
