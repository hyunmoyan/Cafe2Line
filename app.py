from flask import Flask, render_template, jsonify, request
import requests
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import os
app = Flask(__name__)

client = MongoClient('mongodb://test:test@13.209.49.122',27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.cafe_two_line  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


with open('config.json', 'r') as f:
    config = json.load(f)

client_id = config["X-Naver-Client-Id"]  # 'secret-key-of-myapp'
client_secret = config["X-Naver-Client-Secret"]

@app.route('/')
def home():
    return render_template('index4.html')


@app.route('/cafe', methods=['POST'])
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    name_receive = request.form['name_give'].strip()
    station_receive = request.form['station_give'].strip()
    description_receive = request.form['description_give'].strip()

    print(name_receive)
    print(station_receive)
    print(description_receive)

    #api 불러오기


    search = station_receive.rstrip('역')+" "+name_receive
    print(search)
    url = f"https://openapi.naver.com/v1/search/image?query={search}&filter=medium&display=2"  # json 결과

    header = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
    response = requests.get(url, headers=header)
    response_json = json.loads(response.text)

    if not response_json["items"]:
        image_url = "https://images.unsplash.com/photo-1554118811-1e0d58224f24?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&w=1000&q=80"
        print("List is empty")
    else:
        image_url = response_json["items"][0]["link"]
        print(image_url)


    cafe = {'name': name_receive, 'station': station_receive,
            'description': description_receive, 'image_url': image_url}

    db.cafe.insert_one(cafe)
    return jsonify({'result': 'success', 'msg': '업로드 성공!'})


@app.route('/cafe', methods=["GET"])
def read_articles():
    # 1. mongoDB에서 _id 값을 제외한 모든 데이터 조회해오기 (Read)
    search_receive = request.args.get('search_give')
    resultlist = list(db.cafe.find({'station' : search_receive},{"_id":0}))
    # 2. articles라는 키 값으로 article 정보 보내주기
    return jsonify({'result': 'success', 'cafe': resultlist})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
