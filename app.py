from flask import Flask, request, url_for, redirect, render_template, session, flash
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
import re
from flask_mail import Mail, Message

import pickle
import numpy as np



model = pickle.load(open('models/framingham.pickle', 'rb'))
model1 = pickle.load(open('models/combine_heart.pickle', 'rb'))
model2 = pickle.load(open('models/diabetes_prediction_rf.pickle', 'rb'))
app = Flask(__name__, template_folder='templates')
bcrypt = Bcrypt(app)
users = []  # Initialize the users list for temporary storage
app.secret_key = 'ThisIsMySicretKey'  # Set a secret key for the app

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Rushikesh@90'
app.config['MYSQL_DB'] = 'myflaskapp'  # Name of your MySQL database
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Return rows as dictionaries
app.config['TESTING']=True

mysql = MySQL(app)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route("/heart")
def heart():
    return render_template('heart.html')

@app.route("/heartframg", methods=['GET'])
def heartf():
    return render_template("heartfram.html")

@app.route("/heartcombine", methods=['GET'])
def heartc():
    return render_template("heartcombined.html")

@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')

@app.route('/healthtips')
def healthtips():
    return render_template('healthtips.html')

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email_or_phone = request.form['email_or_phone']
        password = request.form['password']

        # Check if email or phone number already exists
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email_or_phone = %s", (email_or_phone,))
        existing_user = cur.fetchone()

        if existing_user:
            cur.close()
            flash('This email or phone number is already in use. Please use a different one.', 'error')
            return redirect(url_for('register'))

        # Server-side validation for email or phone number format
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.[\w\.-]+$', email_or_phone) and not re.match(r'^\d{10}$', email_or_phone):
            flash('Please enter a valid email or a 10-digit phone number.', 'error')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # If email or phone number is unique and format is correct, proceed with registration
        cur.execute("INSERT INTO users (name, email_or_phone, password) VALUES (%s, %s, %s)",
                    (name, email_or_phone, hashed_password))
        mysql.connection.commit()
        cur.close()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/send_email', methods=['POST'])
def send_email():
    if request.method == 'POST':
        full_name = request.form['full_name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        address = request.form['address']
        message = request.form['message']

        msg = Message('New Contact Request', recipients=['adityapawar3602@gmail.com'])  # Change this to your recipient email address
        msg.body = f"Full Name: {full_name}\nPhone Number: {phone_number}\nEmail: {email}\nAddress: {address}\nMessage: {message}"

        try:
            mail.send(msg)
            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            flash('An error occurred while sending your message. Please try again later.', 'error')
            app.logger.error(f"Error sending email: {str(e)}")

        return redirect(url_for('index'))  # Redirect the user back to the index page after sending the email

    return redirect(url_for('register'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email_or_phone = request.form['email_or_phone']
        password = request.form['password']

        # MySQL Database Interaction
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email_or_phone = %s", (email_or_phone,))
        user = cur.fetchone()
        cur.close()

        if user:
            if bcrypt.check_password_hash(user['password'], password):
                # Set user information in the session
                session['user_name'] = user['name']
                flash('Login successful. Welcome back!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email/phone or password. Please try again.', 'error')
        else:
            flash('You are not registered. Please register.', 'error')
            return redirect(url_for('register'))  # Redirect to registration page

    return render_template('login.html')


@app.route('/profile')
def profile():
    # Retrieve user information from the session
    user_name = session.get('user_name')

    # Check if user is logged in
    if user_name:
        return render_template('profile.html', user_name=user_name)
    else:
        flash('Please log in to access your profile.', 'error')
        return redirect(url_for('login'))

@app.route("/heartfram", methods=['GET','POST'])
def heartfram():
    if request.method == 'POST':

        gender = int(request.form['gender'])
        if gender == 'Male':
            gender = 1
        else:
            gender = 0
        print(gender)

        age = int(request.form['age'])
        print()
        smoker = request.form['smoker']
        if smoker == 'Yes':
            smoker = 1
        else:
            smoker = 0

        print(smoker)
        cigs = int(request.form['cigs'])
        bp_meds = int(request.form['bp_meds'])
        if bp_meds == 'Yes':
            bp_meds = 1
        else:
            bp_meds = 0
        stroke = int(request.form['stroke'])
        if stroke == 'Yes':
            stroke = 1
        else:
            stroke = 0
        hyp = int(request.form['hyp'])
        if hyp == 'Yes':
            hyp = 1
        else:
            hyp = 0
        dia = 1
        chol = int(request.form['chol'])
        sysBp = int(request.form['sysBp'])
        diaBp = int(request.form['diaBp'])
        height = float(request.form['height'])
        weight = int(request.form['weight'])
        bmi = weight / (height * height)
        rate = int(request.form['rate'])
        glu = float(request.form['glu'])

        prediction = model.predict(np.array([gender, age, smoker, cigs, bp_meds, stroke, hyp, dia, chol, sysBp, diaBp, bmi, rate, glu]).reshape((1, -1)))
        output = round(prediction[0])
        if output == 0:
            return render_template('result.html',prediction="Congratulations, you are not affected with heart disease. Have a good diet.!!")
        else:
            return render_template('result.html',prediction="Sorry ! It looks like you have been affected with heart disease. Please consult doctore as soon as possible, so your treatment starts soon.".format(output))

    else:
        return render_template('heartfram.html')




@app.route('/heartcombined', methods=['GET','POST'])
def heartcombined():
    if request.method == 'POST':
        age = int(request.form['age'])
        sex = int(request.form['sex'])
        if sex == 'Male':
            sex = 1
        else:
            sex = 0
        cpt = int(request.form['cpt'])
        if cpt == "Typical Angina":
            cpt = 0
        elif cpt == "Atypical Angina":
            cpt = 1
        elif cpt == "Non-Anginal Pain":
            cpt = 2
        else:
            cpt = 3
        bp = int(request.form['bp'])
        chol = int(request.form['chol'])
        fbp = int(request.form['fbp'])
        if fbp == "Fasting Blood Sugar < 120 mg/dl":
            fbp = 0
        else:
            fbp = 1
        ecg = int(request.form['ecg'])
        if ecg == "Recting Ecg":
            ecg = 0
        elif ecg == "ST-T wave abnormality":
            ecg = 1
        else:
            ecg = 2
        mhr = int(request.form['mhr'])
        mhr = 220 - age
        exe_angina = int(request.form['exe_angina'])
        if cpt == 4:
            exe_angina = 1
        else:
            exe_angina = 0
        oldpeak = float(request.form['oldpeak'])
        slope = int(request.form['slope'])
        if slope == "Upsloping":
            slope = 1
        elif slope == "Flat":
            slope = 2
        else:
            slope = 3

        prediction1 = model1.predict(np.array([age, sex, cpt, bp, chol, fbp, ecg, mhr, exe_angina, oldpeak, slope]).reshape((1,-1)))
        output = round(prediction1[0])
        if output == 0:
            return render_template('result.html',prediction="Congratulations, you are not affected with heart disease. Have a good diet.!!")
        else:
            return render_template('result.html',prediction="Sorry ! It looks like you have been affected with heart disease. Please consult doctore as soon as possible, so your treatment starts soon.")

    else:
        return render_template('heartcombined.html')

@app.route('/diabetespred', methods=['GET','POST'])
def diabetespred():
    if request.method == 'POST':
        Pregnancies = int(request.form['Pregnancies'])
        Glucose = float(request.form['Glucose'])
        BloodPressure = float(request.form['BloodPressure'])
        Skinthickness = float(request.form['Skinthickness'])
        Insulin = float(request.form['Insulin'])
        BMI = float(request.form['BMI'])
        DiabetesPedigreeFunction = float(request.form['DiabetesPedigreeFunction'])
        Age = int(request.form['Age'])
        
        prediction2 = model2.predict(np.array([Pregnancies, Glucose, BloodPressure, Skinthickness, Insulin, BMI, DiabetesPedigreeFunction, Age]).reshape((1,-1)))
        output = round(prediction2[0])
        if output == 0:
            return render_template('result.html',prediction="Congratulations, you are not affected with diabetes. Have a good diet.!!")
        else:
            return render_template('result.html',prediction="Sorry ! It looks like you have been affected with heart disease. Please consult doctore as soon as possible, so your treatment starts soon.")

    else:
        return render_template('diabetes.html')

    

if __name__ == "__main__":
    app.run(debug=True)




