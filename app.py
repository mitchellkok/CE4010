from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import csv
import re
import os

#Main App Directory
app = Flask(__name__)
monitor = 0

@app.route("/")
def index():
    return render_template('index.html')

    # Route for handling the login page logic

@app.route('/register', methods = ['GET', 'POST'])
def register(): 
    error = None 
    if request.method == 'POST':
        with open('users-mj.csv', mode = 'a') as csvfile: 
            fields = []
            fields.append('Student')
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if (re.fullmatch(regex,request.form['username'])):
                fields.append(request.form['username'])
                if (request.form['pw1'] == request.form['pw2']):
                    fields.append(request.form['pw1'])
                    for element in fields: 
                        csvfile.write(element + ',')
                    csvfile.write('\n')
                    error = 'Account created. Proceed to Login.'
                    csvfile.close()
                    return render_template('register.html', error=error)
                else: 
                    error = 'Passwords do not match. Please try again'
                    csvfile.close()
                    return render_template('register.html', error=error)
            else:
                error = 'Invalid Email. Please try again'
                return render_template('register.html', error=error)
    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #print(request.form['username'])
        #print(request.form['password'])
        validated = 0
        with open('users-mj.csv', mode = 'r') as csvfile: 
            reader = csv.reader(csvfile)
            for row in reader: 
                print(row[0])
                print("un: ", row[1])
                print("pw: ", row[2])
                print('user:', request.form['user'])
                print("enter un: ", request.form['username'])
                print("enter pw: ", request.form['password'])
                if row[0] == request.form['user'] and row[1] == request.form['username'] and row[2] == request.form['password']:
                    #session["username"] = request.form['username']
                    validated = 1 
                    continue
        print('validted = ', validated)           
        if validated == 1: 
            user = request.form['user']
            username = request.form['username']
            csvfile.close()
            if user == 'Student':
                return redirect(url_for('home',username=username))
            elif user == 'Staff':
                return redirect(url_for('staff',username=username))
        else:    
            error = 'Invalid Credentials. Please try again.'
            csvfile.close()
            return render_template('login.html', error=error)
    return render_template('login.html', error=error)

@app.route('/home/<username>')
def home(username): 
    with open('posts.csv', mode = 'r') as posts:
        reader = csv.reader(posts, delimiter = ',')
        i = 1
        postinfo = {}
        username = username
        for row in reader:
            title = row[1]
            text = row[2]
            postinfo[title] = text
            i = i+1
    return render_template('home.html', **locals())

@app.route('/staff/<username>')
def staff(username): 
    with open('posts.csv', mode = 'r') as posts:
        reader = csv.reader(posts, delimiter = ',')
        i = 1
        postinfo = {}
        username = username
        for row in reader:
            title = row[1]
            text = row[2]
            postinfo[title] = text
            i = i+1
    return render_template('staff.html', **locals())

@app.route('/add/<username>', methods = ['GET', 'POST'])
def add(username):
    error = None 
    auths = []
    with open('authorities.csv', mode = 'r') as authlist: 
        reader = csv.reader(authlist)
        for row in reader: 
            print(row)
            rowtext = str(row) [2:-2]
            print(rowtext)
            auths.append(rowtext)
    print(auths)
    if request.method == 'POST':
        with open('posts.csv', mode = 'a') as csvfile: 
            fields = []
            print(request.form['auth'])
            fields.append(request.form['auth'])
            fields.append(request.form['title'])
            fields.append(request.form['confession'])
            fields.append(username)
            for element in fields: 
                csvfile.write(element + ',')
            csvfile.write('\n')
            error = 'Post created.'
            csvfile.close()
            return render_template('confession.html', **locals())
    return render_template('confession.html', **locals())

@app.route('/redress/<username>', methods = ['GET', 'POST'])
def redress(username):
    with open('users-mj.csv', mode = 'r') as identity: 
        readuser = csv.reader(identity, delimiter = ',')
        for row in readuser: 
            if row[1] == username: 
                name = row[3]
                print(name)
                continue
    with open('posts.csv', mode = 'r') as posts:
        reader = csv.reader(posts, delimiter = ',')
        i = 1
        postinfo = {}
        username = username
        for row in reader:
            if row[0] == name:
                title = row[1]
                text = row[2]
                postinfo[title] = text
                i = i+1
        if len(postinfo) == 0: 
            postinfo['No Confessions for Me!'] = '' 
    return render_template('redress.html', **locals())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)