from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import csv
import re
import sys

from fernet import *

#Main App Directory
app = Flask(__name__)
monitor = 0

users_symkey_fn = 'files/u_symkey.key'
posts_symkey_fn = 'files/p_symkey.key'

users_fn = 'files/users.csv'
posts_fn = 'files/posts.csv'
authorities_fn = 'files/authorities.csv'

def csv_to_str(reader):
    new_string = ""
    for row in reader:

        joined_string = ",".join(map(str,row))
        new_string = new_string + "\n" + joined_string

    return new_string.lstrip()

@app.route("/")
def index():
    return render_template('index.html')

    # Route for handling the login page logic

@app.route('/register', methods = ['GET', 'POST'])
def register(): 
    symkey_fn = users_symkey_fn
    target_fn = users_fn

    error = None 
    if request.method == 'POST':
        reader = fernet_read_file(symkey_fn, target_fn)
        old_string = csv_to_str(reader)

        fields = []
        fields.append('Student')
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if (re.fullmatch(regex,request.form['username'])):
            fields.append(request.form['username'])
            if (request.form['pw1'] == request.form['pw2']):
                fields.append(request.form['pw1'])
                
                new_string = ""
                for element in fields: 
                    print(element)
                    new_string = new_string + element + ","
                new_string =  old_string + "\n" + new_string
                fernet_write_file(symkey_fn, target_fn, new_string.lstrip())

                error = 'Account created. Proceed to Login.'

            else: 
                error = 'Passwords do not match. Please try again'

        else:
            error = 'Invalid Email. Please try again'

    return render_template('register.html', error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    symkey_fn = users_symkey_fn
    target_fn = users_fn
    
    error = None
    if request.method == 'POST':
        validated = 0
        reader = fernet_read_file(symkey_fn, target_fn)
        print("enter un: ", request.form['username'])
        print("enter pw: ", request.form['password'])
        for row in reader: 
            print("\n" + row[0])
            print("un: ", row[1])
            print("pw: ", row[2])
            print('user:', request.form['user'])
            if row[0] == request.form['user'] and row[1] == request.form['username'] and row[2] == request.form['password']:
                #session["username"] = request.form['username']
                validated = 1 
                continue
        print('validted = ', validated)           
        if validated == 1: 
            user = request.form['user']
            username = request.form['username']

            if user == 'Student':
                return redirect(url_for('home',username=username))
            elif user == 'Staff':
                return redirect(url_for('staff',username=username))
        else:    
            error = 'Invalid Credentials. Please try again.'

            return render_template('login.html', error=error)
    return render_template('login.html', error=error)

@app.route('/home/<username>', methods = ['GET','POST'])
def home(username): 
    symkey_fn = posts_symkey_fn
    target_fn = posts_fn

    #when user likes a post
    if request.method == 'POST':
        lines = fernet_read_file(symkey_fn, target_fn)
        print('line',lines)
        new_string = ""
        for row in lines: 
            print('row:',row)
            if int(row[7]) == int(request.form['id']):
                if request.form['category'] == 'post':
                    likeslist = row[3]+username+';' 
                    newrow = row
                    newrow[3] = likeslist
                    joined_string = ",".join(map(str,newrow))

                    new_string = new_string + "\n" + joined_string
                elif request.form['category'] == 'redressal':
                    likeslist = row[6]+username+';' 
                    newrow = row
                    newrow[6] = likeslist
                    joined_string = ",".join(map(str,newrow))

                    new_string = new_string + "\n" + joined_string
            else: 
                joined_string = ",".join(map(str,row))
                new_string = new_string + "\n" + joined_string
        
        print('new_string:',new_string)
        fernet_write_file(symkey_fn, target_fn, new_string.lstrip())

    #display posts
    reader = fernet_read_file(symkey_fn, target_fn)
    i = 1
    postinfo = {}
    username = username
    for row in reader:
        title = row[1]
        text = row[2]
        likesnumber = len(row[3].split(';'))-1
        redressal = row[5]
        redressallikes = len(row[6].split(';'))-1
        id = row[7]
        if username in row[3]:
            likedbyme = 1
        else: 
            likedbyme = 0
        if username in row[6]:
            r_likedbyme = 1
        else: 
            r_likedbyme = 0
        post = {}
        post['Title'] = title
        post['Text'] = text
        post['Likes'] = likesnumber
        post['Liked'] = likedbyme
        post['Redressal'] = redressal
        post['R_likes'] = redressallikes
        post['R_likedbyme'] = r_likedbyme
        post['id'] = id
        postinfo[i] = post
        i = i+1

    return render_template('home.html', **locals())

@app.route('/staff/<username>', methods = ['GET','POST'])
def staff(username): 
    symkey_fn = posts_symkey_fn
    target_fn = posts_fn

    #when user likes a post
    if request.method == 'POST':
        if request.method == 'POST':
            lines = fernet_read_file(symkey_fn, target_fn)
            print('line',lines)
            new_string = ""
            for row in lines: 
                print('row:',row)
                if int(row[7]) == int(request.form['id']):
                    if request.form['category'] == 'post':
                        likeslist = row[3]+username+';' 
                        newrow = row
                        newrow[3] = likeslist
                        joined_string = ",".join(map(str,newrow))

                        new_string = new_string + "\n" + joined_string
                    elif request.form['category'] == 'redressal':
                        likeslist = row[6]+username+';' 
                        newrow = row
                        newrow[6] = likeslist
                        joined_string = ",".join(map(str,newrow))

                        new_string = new_string + "\n" + joined_string
                else: 
                    joined_string = ",".join(map(str,row))
                    new_string = new_string + "\n" + joined_string
            
            print('new_string:',new_string)
            fernet_write_file(symkey_fn, target_fn, new_string.lstrip())

    #display posts
    reader = fernet_read_file(symkey_fn, target_fn)
    i = 1
    postinfo = {}
    username = username
    for row in reader:
        title = row[1]
        text = row[2]
        likesnumber = len(row[3].split(';'))-1
        redressal = row[5]
        redressallikes = len(row[6].split(';'))-1
        id = row[7]
        if username in row[3]:
            likedbyme = 1
        else: 
            likedbyme = 0
        if username in row[6]:
            r_likedbyme = 1
        else: 
            r_likedbyme = 0
        post = {}
        post['Title'] = title
        post['Text'] = text
        post['Likes'] = likesnumber
        post['Liked'] = likedbyme
        post['Redressal'] = redressal
        post['R_likes'] = redressallikes
        post['R_likedbyme'] = r_likedbyme
        post['id'] = id
        postinfo[i] = post
        i = i+1

    return render_template('staff.html', **locals())

@app.route('/add/<username>', methods = ['GET', 'POST'])
def add(username):
    symkey_fn = posts_symkey_fn
    target_fn = posts_fn

    error = None 
    auths = []
    #to generate list of authorities option
    with open(authorities_fn, mode = 'r') as authlist: 
        reader = csv.reader(authlist)
        for row in reader: 
            print(row)
            rowtext = str(row) [2:-2]
            print(rowtext)
            auths.append(rowtext)
        authlist.close()
    print(auths)
    if request.method == 'POST':
        #to determine ID
        reader = fernet_read_file(symkey_fn, target_fn)
        old_string = csv_to_str(reader)

        i = 1
        reader = fernet_read_file(symkey_fn, target_fn)
        for row in reader:
            i += 1
        print("i = ", i)

        #Format: Authority,Title,Post,PostLikes,Email,Redressal,RedressalLikes,ID
        new_string = ""
        fields = []
        print(request.form['auth'])
        fields.append(request.form['auth'])
        fields.append(request.form['title'])
        fields.append(request.form['confession'])
        likes = ""
        fields.append(likes)
        fields.append(username)
        redressal = ""
        fields.append(redressal)
        redressallikes = ""
        fields.append(redressallikes)
        fields.append(str(i))
        print(fields)
        for element in fields: 
            print(element)
            new_string = new_string + element + ","
    
        new_string =  old_string + "\n" + new_string
        fernet_write_file(symkey_fn, target_fn, new_string.lstrip())
        error = 'Post created.'

    return render_template('confession.html', **locals())

@app.route('/redress/<username>', methods = ['GET', 'POST'])
def redress(username):
    p_symkey_fn = posts_symkey_fn
    p_target_fn = posts_fn
    u_symkey_fn = users_symkey_fn
    u_target_fn = users_fn
    
    #when authority redresses a post
    if request.method == 'POST':
        lines = fernet_read_file(p_symkey_fn, p_target_fn)
        print('line',lines)
        new_string = ""
        for row in lines: 
            print('row:',row)
            if int(row[7]) == int(request.form['id']):
                redressal = request.form['redressal']
                newrow = row
                newrow[5] = redressal
                print('newrow',newrow)
                joined_string = ",".join(map(str,newrow))


                new_string = new_string + "\n" + joined_string
            else: 
                joined_string = ",".join(map(str,row))
                new_string = new_string + "\n" + joined_string
        
        print('new_string:',new_string)
        fernet_write_file(p_symkey_fn, p_target_fn, new_string.lstrip())

    name = ''
    readuser = fernet_read_file(u_symkey_fn, u_target_fn)
    for row in readuser:
        if row[1] == username: 
            name = row[3]
            print(name, type(name))
            continue

    reader = fernet_read_file(p_symkey_fn, p_target_fn)
    i = 1
    postinfo = {}
    username = username
    pendingredressals = 0
    for row in reader:
        if row[0] == name:
            title = row[1]
            text = row[2]
            likesnumber = len(row[3].split(';'))-1
            redressal = row[5]
            if redressal == "": 
                pendingredressals = pendingredressals + 1
            redressallikes = len(row[6])
            id = row[7]
            if username in row[3]:
                likedbyme = 1
            else: 
                likedbyme = 0
            if username in row[6]:
                r_likedbyme = 1
            else: 
                r_likedbyme = 0
            post = {}
            post['Title'] = title
            post['Text'] = text
            post['Likes'] = likesnumber
            post['Liked'] = likedbyme
            post['Redressal'] = redressal
            post['R_likes'] = redressallikes
            post['R_likedbyme'] = r_likedbyme
            post['id'] = id
            postinfo[i] = post
            i = i+1
    if len(postinfo) == 0: 
        postinfo['No Confessions for Me!'] = '' 

    return render_template('redress.html', **locals())

if __name__ == "__main__":
    fernet_verify_file(posts_symkey_fn, posts_fn)
    fernet_verify_file(users_symkey_fn, users_fn)

    app.run(host='0.0.0.0', port=1025)