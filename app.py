from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps

app = Flask(__name__)

# config
import os
app.config.from_object(os.environ['APP_SETTINGS'])

# data
from dicts import dynamicOfficeDict 


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        if request.form['adduser'] == 'yes' or request.form['adduser'] == 'Yes':
            return redirect(url_for('useradd'))
        else:
            return redirect(url_for('goodbye'))
    return render_template("index.html")


@app.route('/useradd', methods=['GET', 'POST'])
@login_required
def useradd():
    error = None
    if request.method == 'POST':
        if request.form['addeduser'] and request.form['city'] == 'ERMKT':
            CITYVAR = dynamicOfficeDict[request.form['city']][0]
            USERNAMEVAR = request.form['addeduser'] 
            DISPLNAMEVAR = request.form['addeduser']
            GIVENNAMEVAR = None 
            SURNAMEVAR = None
            TITLEVAR = None 
            UPNVAR = None 
            flash('Ah, ERM.  Paste this into powershell: New-ADUser -Name ' + DISPLNAMEVAR + ' -City ' + CITYVAR)
            return redirect(url_for('powershell'))
        elif request.form['addeduser'] and request.form['city']:
#            CITYVAR = dynamicOfficeDict[cityInput][0]
#            COMPANYVAR = dynamicOfficeDict[cityInput][1] 
#            COUNTRYVAR = dynamicOfficeDict[cityInput][2]
#            DEPTVAR = dynamicOfficeDict[cityInput][3]
#            DESCRVAR = dynamicOfficeDict[cityInput][4]
#            OFFICEVAR = dynamicOfficeDict[cityInput][5]
#            ORGANIZATIONVAR = dynamicOfficeDict[cityInput][6]
#            ZIPVAR = dynamicOfficeDict[cityInput][7]
#            SCRIPTVAR = dynamicOfficeDict[cityInput][8]
#            SERVERVAR = dynamicOfficeDict[cityInput][9]
#            STATEVAR = dynamicOfficeDict[cityInput][10]
#            ADDRESSVAR = dynamicOfficeDict[cityInput][11]
#            PASSWORDVAR = ourHash(dynamicOfficeDict[cityInput][12]) 
            USERNAMEVAR = request.form['addeduser'] 
            DISPLNAMEVAR = request.form['addeduser']
            GIVENNAMEVAR = None 
            SURNAMEVAR = None
            TITLEVAR = None 
            UPNVAR = None 

            flash('Paste this into powershell: New-ADUser -Name ' + DISPLNAMEVAR + ' -City ' + request.form['city'])
            return redirect(url_for('powershell'))
        else:
            error = 'Please add both values; they are required.'
    return render_template('useradd.html', error=error)

@app.route('/powershell')
def powershell():
    return render_template("powershell.html")

@app.route('/goodbye')
def goodbye():
    return render_template("goodbye.html") 


@app.route('/welcome')
def welcome():
    return render_template("welcome.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentials.  Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))


if __name__ == '__main__':
    app.run()
