from flask import Flask, render_template, request, redirect, escape, session
from search4letters import search4letters, log_request
from DBcm import SQLError, UseDatabase, ConnectionError, CredentialsError
from collections import Counter

app = Flask(__name__)

app.secret_key = "YouWillNeverGuess"

def check_logged_in():
    if "logged_in" in session:
        return True
    return False

@app.route("/login")
def do_login():
    session["logged_in"] = True
    return "You are now logged in"

@app.route("/logout")
def do_logout():
    session.pop("logged_in")
    return "You are now logged out"

@app.route("/setuser/<user>")
def setuser(user):
    session["user"] = user
    return "User value set to: "+ session["user"]

@app.route("/getuser")
def getuser():
    return "User value is currently set to: " + session["user"]

@app.route("/")
def hello():
    return redirect("/entry")

@app.route("/stats")
def stats():
    contents = []
    contents.append(list())
    ips = list()
    browser = list()
    letters = ""
    dbconfig = {'host': '127.0.0.1', 
                'user': 'root', 
                'password': 'M4n0l0My$QL', 
                'database': 'search_log',}

    with UseDatabase(dbconfig) as cursor:
        cursor.execute("""select count(*) from log""")
        contents[0].append( cursor.fetchall()[0][0])
        cursor.execute("""select letters, ip, browser_string from log""")
        aux = cursor.fetchall()

        for lista in aux:
            letters = letters+lista[0]
            ips.append(lista[1])
            browser.append(lista[2].split("/")[0])

        contents[0].append(Counter(letters).most_common(1)[0][0])
        contents[0].append( ''.join(max(set(ips), key = ips.count)))
        contents[0].append(''.join(max(set(browser), key = browser.count)))



    titles = ("Count", "Most common letter", "Most common IP", "Most common browser")
    return render_template("viewlog.html",
                            the_title = "Stats",
                            the_row_titles = titles,
                            the_data = contents)

@app.route("/viewlog")
def view_the_log():
    if not check_logged_in():
        return " you are NOT logged in."

    
    dbconfig = {'host': '127.0.0.1', 
                'user': 'root', 
                'password': 'M4n0l0My$QL', 
                'database': 'search_log',}
    try:
        with UseDatabase(dbconfig) as cursor:

            cursor.execute("""select phrase, letters, ip, browser_string, results from log""")
            contents = cursor.fetchall()


        titles = ("Phrase", "Letters", "Remote_addr", "User_agent", "Results")
        return render_template("viewlog.html",
                                the_title = "View Log",
                                the_row_titles = titles,
                                the_data = contents)

    except ConnectionError as err:
        print("Is your database switched on? Error: " + str(err))
        return "Connection Error"

    except SQLError as err:
        print("SQLError. Error: "+ str(err))
        return "sql error"

    except CredentialsError as err:
        print("User-id/Password issues. Error: "+ str(err))
        return "credential error"
    
    except Exception as err:
        print('Something went wrong: '+ str(err))
        return "Error"

@app.route("/search", methods = ["POST"])
def do_search():
    phrase = request.form["phrase"]
    letters = request.form["letters"]
    results = str(search4letters(phrase,letters))

    #tratamiento de errores de log in
    try:
        log_request(request,results)
    except Exception as err: 
        print('***** Logging failed with error: ' + str(err))

    return render_template("results.html",the_title = "Here are your results",the_letters=letters,\
        the_phrase = phrase, the_results = results)




@app.route("/entry")
def entry_page():
    return render_template("entry.html",
                            the_title = "Welcome to search for letters on the web!")
    
if __name__=="__main__":
    app.run(debug=True)