""" webapp created with flask can receive requests from the browser and send responses back to the browser """

from flask import Flask, request, jsonify, render_template, abort
from flask import session,redirect,url_for
import hashlib
from sqlite3 import dbapi2 as sqlite3



# create the database if not exist
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect('webapp/database.db')
    rv.row_factory = sqlite3.Row
    return rv


# create the clienttable if not exist
def init_clienttable():
    """Initializes the database."""
    db = connect_db()
    db.execute('create table if not exists clienttable (id text primary key, email text, password text, name text, address text, phone text)')
    db.commit()
    db.close()

init_clienttable()

def get_clienttable(email, password):
    db = connect_db()
    cur = db.execute('select * from clienttable where email = ? and password = ?', [email, password])
    entries = cur.fetchall()
    entries = [dict(id=row[0], email=row[1], password=row[2], name=row[3], address=row[4], phone=row[5]) for row in entries][0]
    return entries

def insert_clienttable(id, email, password, name, phone):
    db = connect_db()
    db.execute('insert into clienttable (id, email, password, name, phone) values (?, ?, ?, ?, ?)',
                 [id, email, password, name, phone])
    db.commit()
    db.close()
    return "Successfull Register"


clients = []




app = Flask(__name__)
app.secret_key = "mysecretkey"
datainfo = []
session = {}





@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if "Client" in session:
        return redirect(url_for("user"))

    elif request.method == 'POST' :
        data = request.form.to_dict()
        data["password"] = hashlib.sha256(data["password"].encode()).hexdigest()
        all_data = get_clienttable(data["email"], data["password"])
        if len(all_data) > 0:
            session["Client"] = all_data["id"]
            return redirect(url_for("user"))
        else:
            return redirect("/login")

    elif request.method == 'GET':
        return render_template("login.html")
    
# register on the webpages
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        data["password"] = hashlib.sha256(data["password"].encode()).hexdigest()
        data["id"] = hashlib.sha256(data["email"].encode()).hexdigest()
        insert_clienttable(data["id"], data["email"], data["password"], data["username"], data["phone"])

        return redirect("/login")
    elif request.method == 'GET':
        return render_template("register.html")
    else:
        "redirect to login"
        return redirect("/login", code=400)
    
@app.route('/user', methods=['GET'])
def user():
    if "Client" in session:
        return render_template("admin.html", data=session["Client"])
    else:
        return redirect("/login")

@app.route('/logout', methods=['POST'])
def logout():
    session.pop("Client", None)
    return redirect("/login")

@app.route('/post', methods=['POST'])
def posting():
    print("request.headers", request.headers)

    def Auth():
        if app.secret_key == request.headers["Authorization"]:
            return True
        else:
            return False

    if Auth():
        # get auth session key 
        # if session key is not in session then create a new session key
        session["Client"] = 123
        return jsonify({"status": "OK"})
       
    else :
        return jsonify({'Authorization': 'Faild!'})

@app.route('/query', methods=['POST'])
def query():
    query = request.json['query']
    # Connect to database and execute query
    conn = sqlite3.connect("webapp/database.db")
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    #get the column names
    colnames = [desc[0] for desc in cursor.description] 
    # add the column names to the result 1st item   
    result.insert(0, colnames)
    
    # Return result as JSON
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)

    





