from flask import Flask, render_template, request
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']
        GST1 = request.form['GST1']
        Address = request.form['Address']
        
        global x
        x =name

        table = dynamodb.Table('users')
        
        table.put_item(
                Item={
        'name': name,
        'email': email,
        'password': password,
        'password2' : password2,
        'GST1' : GST1,
        'Address' : Address
            }
        )
        
        img = request.files['file']
        if img:
                filename = secure_filename(img.filename)
                img.save(filename)
                s3.upload_file(
                    Bucket = BUCKET_NAME,
                    Filename=filename,
                    Key = filename
                )
        msg = "Registration Complete. Please Login to your account !"
    
        return render_template('login1.html',msg = msg)
    return render_template('signup.html')



@app.route('/check',methods=['GET', 'POST'])
def check():
    if request.method=='POST':
        
        email = request.form['email']
        password = request.form['password']
        

        table = dynamodb.Table('users')
        response = table.query(
                KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        name = items[0]['name']
        print(items[0]['password'])
        if password == items[0]['password']:
            
            return render_template("dashbord2.html",name = name)
    return render_template("login1.html")


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

if __name__ == "__main__":
    
   app.run(host='0.0.0.0', port=80, debug=True)
