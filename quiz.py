from flask import Flask, request, redirect, url_for, session, render_template, Response
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)
app.secret_key = "your_secret_key"


# ------------------------------
# FORM CLASS
# ------------------------------
class RegisterForm(FlaskForm):
    username = StringField(
        "Full Name",
        validators=[
            DataRequired(message="name cannot be empty"),
            Length(min=3, max=10, message="Name must be between 3 to 10 characters"),
        ],
    )
    roll = StringField(
        "Roll No",
        validators=[
            DataRequired(message="The roll no must be mp 10 digits"),
            Length(min=10, max=10, message="Roll no must be exactly 10 characters"),
        ],
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    ans = RadioField(
        "Do you want to play?",
        choices=[("yes", "Yes"), ("no", "No")],
        validators=[DataRequired()],
    )
    city = SelectField(
        "select your city",
        choices=[("hyderabad", "Hyderabad"), ("cyberabad", "Cyberabad")],
        validators=[DataRequired()],
    )


# ------------------------------
# VALID USERS
# ------------------------------
valid_users = {
    "TEJA": "24881A05X5",
    "HARSH": "24881A05U0",
    "ABDUL": "24881A05R9",
}


# ------------------------------
# HOME ROUTE
# ------------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    form = RegisterForm()
    return render_template("quizlog.html", form=form)


# ------------------------------
# QUIZ ROUTE (Login)
# ------------------------------
@app.route("/quiz", methods=["POST","GET"])
def quiz():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data.strip().upper()  # FIX: Make username uppercase
        roll = form.roll.data.strip()
        ans = form.ans.data

        # FIX: Check username and roll
        if username in valid_users and roll == valid_users[username]:
            if ans == "yes":
                session["user"] = username  # Store username in session
                return redirect(url_for("en"))
            else:
                return Response("get the hell out of here", status=401)
        else:
            return Response("get the hell out of here", status=401)  # FIX: Show error for wrong credentials

    # Render form again if validation fails
    return render_template("quizlog.html", form=form)


# ------------------------------
# EN ROUTE (Marks page)
# ------------------------------
@app.route("/en", methods=["GET", "POST"])
def en():
    username = session.get("user", "Guest")  # FIX: Get username from session
    return render_template("marks.html", username=username)


# ------------------------------
# MK ROUTE (Marks calculation)
# ------------------------------
@app.route("/mk", methods=["POST", "GET"])
def mk():
    c = 0
    q1 = request.form.get("one")
    q2 = request.form.get("two")
    q3 = request.form.get("three")

    if q1 == "yes":
        c += 1
    if q2 == "yes":
        c += 1
    if q3 == "yes":
        c += 1

    username = session.get("user", "fuest")
    return render_template("result.html", username=username, score=c)


# ------------------------------
# LOGOUT ROUTE
# ------------------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    app.run(debug=True)
