from flask import Flask, render_template, request, redirect, url_for
from newsapi import NewsApiClient
import os 
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///form.db'
db = SQLAlchemy(app)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'damanpreetsingh1979@gmail.com',
    MAIL_PASSWORD = '*******'
)
mail = Mail(app)
class Form(db.Model):
    user = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.Integer, unique=True, nullable=False)
    textarea = db.Column(db.String(8), unique=True, nullable=False)
    def __repr__(self):
        return '<Form %r>' % self.user

@app.route('/')
def home():
    newsapi = NewsApiClient(api_key="71d45e0dd94e4b2e9e14cb6351b7bf24")
    topheadlines = newsapi.get_top_headlines(sources="bbc-news")
 
 
    articles = topheadlines['articles']
 
    desc = []
    news = []
    img = []
 
 
    for i in range(len(articles)):
        myarticles = articles[i]
 
 
        news.append(myarticles['title'])
        desc.append(myarticles['description'])
        img.append(myarticles['urlToImage'])
 
 
 
    mylist = zip(news, desc, img)
 
 
    return render_template('index.html', context = mylist)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method=='POST':
        try:
            user = request.form.get('user')
            email = request.form.get('email') 
            password = request.form.get('pass') 
            textarea = request.form.get('text')
            msg = Message('New Form Submission', sender='damanpreetsingh1979@gmail.com', recipients=['damanpreetsingh1979@gmail.com, damanjashanpreettakkar@gmail.com, damanjashan25@gmail.com'])
            msg.body = f"Name: {user}, email: {email}, password: {password}, Feedback: {textarea}"
            mail.send(msg)
            form = Form(user=user, email=email, password=password, textarea=textarea)
            db.session.add(form)
            db.session.commit()
            print('message sent') 
            return redirect(url_for('message')) 
        except:
            return redirect(url_for('message')) 
  
    return render_template('contact.html')

@app.route('/message')
def message():
    return render_template('message.html')

if __name__ == "__main__":
    port = (os.environ.get("PORT", 33507))
    app.run(host='0.0.0.0', port=port, debug=True)
    # app.run(debug=True, port=8000)
    
