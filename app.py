# flask import 하는 부분
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# pymongo import 하는 부분
from pymongo import MongoClient

# bs4 import 하는 부분
from bs4 import BeautifulSoup

# Certifi import 하는 부분 (Port 5000을 사용하기 위해서)
import certifi

ca = certifi.where()

# request import 하는 부분
import requests

# MongoDB client, db 변수 선언
client = MongoClient(
    'mongodb+srv://ibban9810:dltmdfuf8484@cluster0.vfu4hiz.mongodb.net/Cluster0?retryWrites=true&w=majority',
    tlsCAFile=ca)
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')


## POST func.
@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    image = og_image['content']
    title = og_title['content']
    description = og_description['content']

    doc = {
        'image': image,
        'title': title,
        'desc': description,
        'star': star_receive,
        'comment': comment_receive
    }

    db.movies.insert_one(doc)

    return jsonify({'msg': 'POST 연결 완료!'})


## DELETE func.
@app.route("/movie_DEL", methods=["POST"])
def movie_delete():
    title_receive = request.form['title_give']
    db.movies.delete_one({'title': title_receive})
    return jsonify({'msg': '삭제 완료 !'})

## GET func.
@app.route("/movie", methods=["GET"])
def movie_get():
    movies_list = list(db.movies.find({}, {'_id': False}))
    return jsonify({'movies': movies_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
