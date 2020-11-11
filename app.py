from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.cafe_two_line  # 'dbsparta'라는 이름의 db를 만들거나 사용합니다.


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/cafe', methods=['POST'])
def post_article():
    # 1. 클라이언트로부터 데이터를 받기
    name_receive = request.form['name_give']
    station_receive = request.form['station_give']
    map_url_receive = request.form['map_url_give']
    description_receive = request.form['description_give']

<<<<<<< HEAD
    #api 불러오기


    search = name_receive+name_receive+"카페"

    url = f"https://openapi.naver.com/v1/search/image?query={search}&filter=medium&display=1"  # json 결과

    header = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
    response = requests.get(url, headers=header)
=======
    #사진 크롤링
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(map_url_receive, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')
    og_image = soup.select_one('meta[property="og:image"]')
    url_image = og_image['content']
>>>>>>> parent of f107cc3... 네이버 api 구현

    cafe = {'name': name_receive, 'station': station_receive, 'map_url': map_url_receive,
            'description': description_receive, 'image_url': url_image}

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
