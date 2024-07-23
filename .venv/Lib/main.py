from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
from flask_cors import CORS
app = Flask(__name__)

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Karsah_2104'
app.config['MYSQL_DB'] = 'mental_app'
app.config['PORT'] = '3306'

mysql = MySQL(app)
CORS(app)

@app.route('/chats')
def upload():
    file = request.files['file']
    file.save(f'uploads/{file.filename}')


@app.route('/chats/<int:senderID>/<int:receiverID>',methods = ['GET'])
def get_all_msgs(senderID,receiverID):
    try:
        myCursor = mysql.connection.cursor()
        sql = 'SELECT * FROM chats WHERE (SenderID = %s AND ReceiverID = %s) OR (SenderID = %s AND ReceiverID = %s)  '
        val = (senderID,receiverID,receiverID,senderID)
        myCursor.execute(sql,val)
        response = myCursor.fetchall()
        print('pass')
        return jsonify(response),200
    except Exception as e:
        print(e)
        return jsonify('An error occurred'),500


@app.route('/chats', methods=['POST'])
def send_msg():
    try:
        time = request.json['time']
        content = request.json['content']
        senderID = request.json['senderID']
        receiverID = request.json['receiverID']
        myCursor = mysql.connection.cursor()

        sql = 'INSERT INTO chats (MsgTime,MsgContent,SenderID,ReceiverID) VALUES(%s,%s,%s,%s)'
        val = (time,content,senderID,receiverID,)
        myCursor.execute(sql,val)
        mysql.connection.commit()
        return jsonify('Msg sent successfully'),200
    except Exception as e:
        return jsonify('An error has occured'),500

@app.route('/all_users',methods = ['GET'])
def get_allUsers():
    try:
        mycursor = mysql.connection.cursor()
        sql = 'SELECT UserName,UserID FROM users'
        mycursor.execute(sql,)
        response = mycursor.fetchall()
        print(response)
        return jsonify(response),200
    except Exception as e:
        print(e)
        return jsonify('An error has occurred'),500

@app.route('/users', methods=['GET'])
def login():
    try:
        email = request.args.get('email')
        password = request.args.get('password')
        mycursor = mysql.connection.cursor()
        sql = "SELECT UserPassword,UserID,UserName FROM users WHERE UserEmail = %s"
        val = (email,)
        mycursor.execute(sql,val)
        response = mycursor.fetchone()

        print(response)

        if(password == response[0]) :
            return jsonify({'status': 'Login Successful','id' : response[1],'name' : response[2]}),200
        else:
            return jsonify('Login Failed'), 400

    except Exception as e:
        print(e)
        return jsonify('An error has occured'),500

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if data is None:
            return jsonify('No data provided'), 400

        email = request.json['email']
        password = request.json['password']
        name = request.json['name']

        if not email or not password:
            return jsonify('Missing required fields'), 400

        mycursor = mysql.connection.cursor()
        sql = "SELECT * FROM users WHERE UserEmail = %s"
        val = (email,)
        mycursor.execute(sql, val)
        if mycursor.fetchone():
            return jsonify('Email already exists'), 400



        sql = "INSERT INTO users (UserEmail, UserPassword,UserName) VALUES (%s, %s,%s)"
        val = (email,password,name)
        mycursor.execute(sql, val)
        mysql.connection.commit()
        return jsonify('User created successfully'), 201

    except Exception as e:
        return jsonify('An error has occured'),500

if __name__ == '__main__':
    app.run(debug=True)
