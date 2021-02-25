from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import smtplib
import time

app = Flask(__name__)

try:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
except SQLAlchemy.exc.IntegrityError:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todos(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    todos = db.Column(db.String(250), nullable=False)


db.create_all()
# new_book = Todos(id=1, name="book", email="blabla@gmail.com", todos="To buy a new book today.")
# db.session.add(new_book)
# db.session.commit()


@app.route('/', methods=["GET", "POST"])
def hello_world():
    listo = []
    todoo = Todos()
    if request.method == 'GET':
        return render_template("index.html")
    elif request.method == 'POST':
        demo_id = request.form["demo-id"]
        demo_name = request.form["demo-name"]
        demo_email = request.form["demo-email"]
        demo_message = request.form["demo-message"]

        try:
            new_todo = Todos(id=demo_id, name=demo_name, email=demo_email, todos=demo_message)
            db.session.add(new_todo)
            db.session.commit()
            all_todos = db.session.query(Todos).all()
            for todo in all_todos:
                ludo = todo.todos
                listo.append(ludo)
                print(listo)

            # Sending Email with Python

            MY_EMAIL = "akshitgaur.sky21@gmail.com"
            MY_PASSWORD = "8xZ*XHKJ%7eJbB"

            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=todo.email,
                    msg=f"Subject:Your Todo List\n\n {listo}"
                )

        except IntegrityError:
            db.session.rollback()
            return render_template("index.html", error=True)
        return render_template("index.html", msg_sent=True, naam=demo_name, mail=demo_email, mess=demo_message, list=all_todos)


if __name__ == "__main__":
    app.run(debug=True)
