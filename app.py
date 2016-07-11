# -*- coding: utf-8 -*-
"""
Created on Tue Jul 05 12:35:41 2016

@author: mattf
"""

from flask import Flask, render_template, request, json, redirect, session
import MySQLdb


app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

@app.route("/")
def main():
    return render_template('index.html')
    
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')
    
@app.route('/signUp',methods=['POST'])
def signUp():
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    # create user code will be here !!
    if _name and _email and _password:
        db = MySQLdb.connect("localhost","newuser","password","BucketList" )
        cursor = db.cursor()
        cursor.callproc('sp_createUser',(_name,_email,_password))
        
        data = cursor.fetchall()
         
        if len(data) is 0:
            db.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})        
        
        return json.dumps({'html':'<span>All fields good !!</span>'})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})
        
@app.route('/showSignin')
def showSignin():
    return render_template('signin.html')    
    
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']
 
    
        db = MySQLdb.connect("localhost","newuser","password","BucketList" )
        cursor = db.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()
        
        if len(data) > 0:
            if (str(data[0][3])==str(_password)):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')
    except Exception as e:
        return render_template('error.html',error = str(e))        
    finally:
        cursor.close()
        db.close()
        
@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')
        
@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')
        
@app.route('/showAddWish')
def showAddWish():
    return render_template('addWish.html')        
    
@app.route('/addWish',methods=['POST'])
def addWish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _description = request.form['inputDescription']
            _user = session.get('user')
 
            db = MySQLdb.connect("localhost","newuser","password","BucketList" )
            cursor = db.cursor()
            cursor.callproc('sp_addWish',(_title,_description,_user))
            data = cursor.fetchall()
 
            if len(data) is 0:
                db.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        db.close()
        
@app.route('/getWish')
def getWish():
    try:
        if session.get('user'):
            _user = session.get('user')
            # Connect to MySQL and fetch data
            db = MySQLdb.connect("localhost","newuser","password","BucketList" )
            cursor = db.cursor()
            cursor.callproc('sp_GetWishByUser',(_user,))
            wishes = cursor.fetchall()
            
            wishes_dict = []
            for wish in wishes:
                wish_dict = {
                    'Id': wish[0],
                    'Title': wish[1],
                    'Description': wish[2],
                    'Date': wish[4]}
                wishes_dict.append(wish_dict)
            print wishes_dict
            return json.dumps(wishes_dict)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html', error = str(e))        
        
if __name__ == "__main__":
    print 'here'
    app.run(debug=True)