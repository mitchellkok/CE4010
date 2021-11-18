from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import csv
import re
import sys

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
        with open('users.csv', mode = 'a') as csvfile: 
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
        with open('users.csv', mode = 'r') as csvfile: 
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

@app.route('/home/<username>', methods = ['GET','POST'])
def home(username): 
    #when user likes a post
    if request.method == 'POST':
        with open ('posts.csv', mode = 'r') as likepost: 
            lines = likepost.readlines()
            likepost.close()
            print('line',lines)
            newfile = open('posts.csv', mode = 'w') 
            for row in lines: 
                row = row.split(',')
                print('row:',row)
                print('row7:', row[7])
                print('req id', request.form['id'])
                if int(row[7]) == int(request.form['id']):
                    if request.form['category'] == 'post':
                        likeslist = row[3]+username+';' 
                        print('likesarray: ',likeslist)
                        newrow = row
                        newrow[3] = likeslist
                        print('newrow',newrow)
                        joined_string = ",".join(map(str,newrow))
                        newfile.write(joined_string)
                    elif request.form['category'] == 'redressal':
                        likeslist = row[6]+username+';' 
                        print('likesarray: ',likeslist)
                        newrow = row
                        newrow[6] = likeslist
                        print('newrow',newrow)
                        joined_string = ",".join(map(str,newrow))
                        newfile.write(joined_string)
                else: 
                    joined_string = ",".join(map(str,row))
                    newfile.write(joined_string)
            newfile.close()
    #display posts
    with open('posts.csv', mode = 'r') as posts:
        reader = csv.reader(posts, delimiter = ',')
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
   #when user likes a post
    if request.method == 'POST':
        with open ('posts.csv', mode = 'r') as likepost: 
            lines = likepost.readlines()
            likepost.close()
            print('line',lines)
            newfile = open('posts.csv', mode = 'w') 
            for row in lines: 
                row = row.split(',')
                print('row:',row)
                print('row7:', row[7])
                print('req id', request.form['id'])
                if int(row[7]) == int(request.form['id']):
                    if request.form['category'] == 'post':
                        likeslist = row[3]+username+';' 
                        print('likesarray: ',likeslist)
                        newrow = row
                        newrow[3] = likeslist
                        print('newrow',newrow)
                        joined_string = ",".join(map(str,newrow))
                        newfile.write(joined_string)
                    elif request.form['category'] == 'redressal':
                        likeslist = row[6]+username+';' 
                        print('likesarray: ',likeslist)
                        newrow = row
                        newrow[6] = likeslist
                        print('newrow',newrow)
                        joined_string = ",".join(map(str,newrow))
                        newfile.write(joined_string)
                else: 
                    joined_string = ",".join(map(str,row))
                    newfile.write(joined_string)
            newfile.close()
    #display posts
    with open('posts.csv', mode = 'r') as posts:
        reader = csv.reader(posts, delimiter = ',')
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
    error = None 
    auths = []
    #to generate list of authorities option
    with open('authorities.csv', mode = 'r') as authlist: 
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
        with open('posts.csv', mode = 'r') as readfile: 
            reader = csv.reader(readfile)
            i = 1
            for row in reader:
                i = i+1
            readfile.close()
        with open('posts.csv', mode = 'a') as csvfile: 
            #Format: Authority,Title,Post,PostLikes,Email,Redressal,RedressalLikes,ID
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
                csvfile.write(element + ',')
            csvfile.write('\n')
            error = 'Post created.'
            csvfile.close()
            return render_template('confession.html', **locals())
    return render_template('confession.html', **locals())

@app.route('/redress/<username>', methods = ['GET', 'POST'])
def redress(username):
    #when authority redresses a post
    if request.method == 'POST':
        with open ('posts.csv', mode = 'r') as redresspost: 
            lines = redresspost.readlines()
            redresspost.close()
            print('line',lines)
            newfile = open('posts.csv', mode = 'w') 
            for row in lines: 
                row = row.split(',')
                print('row:',row)
                print('row7:', row[7])
                print('req id', request.form['id'])
                if int(row[7]) == int(request.form['id']):
                    redressal = request.form['redressal']
                    newrow = row
                    newrow[5] = redressal
                    print('newrow',newrow)
                    joined_string = ",".join(map(str,newrow))
                    newfile.write(joined_string)
                else: 
                    joined_string = ",".join(map(str,row))
                    newfile.write(joined_string)
            newfile.close()

    with open('users.csv', mode = 'r') as identity: 
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
                likesnumber = len(row[3].split(';'))-1
                redressal = row[5]
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
    app.run(host='0.0.0.0', port=80)