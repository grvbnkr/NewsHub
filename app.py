from flask import *
from sqlite3 import *
from flask_mail import Mail, Message
import sqlite3

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'grvbnkr@gmail.com'
app.config['MAIL_PASSWORD'] = 'vgragnntffycwvue'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/', methods=["GET","POST"])
def home():
    if request.method=="POST":
        email = request.form["email"]
        if "sub" in request.form:
            con = None
            try:
                con = connect("kcusers.db")
                cursor = con.cursor()
                sql = "insert into student values('%s')"
                cursor.execute(sql%(email))
                con.commit()
                msg = Message('Hello',sender = 'grvbnkr@gmail.com',recipients=[email])
                msg.body = 'Hello from Django classes Welcome onboard'
                mail.send(msg)
                return render_template("home.html",msg="Congrats")
            except Exception as e:
                con.rollback()
                msg = "issue "+ str(e)
                return render_template("home.html",msg=msg)
            finally:
                if con is not None:
                    con.close()
        else:
            con=None
            try:
                con=connect("kcusers.db")
                cursor=con.cursor()
                sql = "delete from student where email= '%s'"
                cursor.execute(sql%(email))
                rc = cursor.rowcount
                if rc == 1:
                    con.commit()
                    msg = "sorry to let u go"
                    return render_template("home.html",msg=msg)
                else:
                    msg = "tu hain kaun"
                    return render_template("home.html",msg=msg)
            except Exception as e:
                if con is not None:
                    con.close()
    else:
        return render_template("home.html")
    

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)



