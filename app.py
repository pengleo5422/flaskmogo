import urllib as urllib
from bson.objectid import ObjectId
import pymongo
from flask import Flask, render_template, request, url_for, redirect

# ...

app = Flask(__name__)

password = urllib.parse.quote_plus("7cR2@SVz@4N@Yi6")
client = pymongo.MongoClient(
    "mongodb+srv://pen:%s@cluster0.2bvbuoj.mongodb.net/test?retryWrites=true&w=majority" % (password))
db = client.test
todos = db.book


@app.route('/', methods=('GET', 'POST'))
@app.route('/index.html', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        writer = request.form['writer']
        press = request.form['press']
        date = request.form['date']
        todos.insert_one({'商品名': name, '價格': price, '日期': date, '作者': writer, '出版社': press})
        return redirect(url_for('index'))
    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)


@app.route('/generic.html', methods=('GET', 'POST'))
def generic():
    all_todos = todos.find()
    if request.method == 'POST':
        name = request.form['name']
        ty = request.form['type']
        ser_to = todos.find({ty: {'$regex': name}})
        return render_template('generic.html', todos=all_todos, se=ser_to)
    all_todos = todos.find()
    return render_template('generic.html', todos=all_todos)




@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('generic'))


@app.post('/<id>/update/')
def update(id):
    date = request.form['date']
    todos.update_one({"_id": ObjectId(id)}, {'$set': {'日期': date}})
    return redirect(url_for('generic'))





