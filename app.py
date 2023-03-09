from bson.json_util import dumps
from pymongo import MongoClient  # DB 라이브러리
from bson.objectid import ObjectId
from flask import Flask, render_template, request, jsonify  # 웹개발 라이브러리
from ytmusicapi import YTMusic
import youtube # 크롤링 모듈
app = Flask(__name__)

client = MongoClient(
    'mongodb+srv://sparta:test@cluster0.caexhck.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta  # DB명

#Youtube
from ytmusicapi import YTMusic
ytmusic = YTMusic('headers_auth.json')


@app.route('/')
def home():
    return render_template('index.html')

# 글쓰기 모달창에서 youtube url 받아오기
@app.route("/write", methods=["POST"])
def youtube_url_post():
    url_receive = request.form['youtube_url_give']
    url = ''
    # youtu.be/aa 주소와 youtube.com/aa 주소 둘 다 체크해서 동영상 주소 리턴
    if url_receive.find("youtu.be") == -1:
        url = url_receive.split("watch?v=")[1][0:11]
    elif url_receive.find("youtube.com") == -1:
        url = url_receive.split(".be/")[1]
    
    if youtube.youtube.crawling(request.form['youtube_url_give']) == 'error':
        return jsonify({'receive': 'error'})
    else:
        crawling_receive = youtube.youtube.crawling(request.form['youtube_url_give'])
        crawling = []
        crawling.append(crawling_receive)
    
    artist = crawling[0][1]
    music = crawling[0][0]
    
    return jsonify({'receive': {'url':url,'music': music, 'artist': artist}})

# db에 저장하기
@app.route("/write_main", methods=["POST"])
def smm_post():
    youtube_url_receive = request.form['youtube_url_give']
    music_receive = request.form['music_give']
    artist_receive = request.form['artist_give']
    sort_receive = request.form['sort_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    
    # youtube.com/aa에서 aa만 따로 저장
    url = ''
    if youtube_url_receive.find("youtu.be") == -1:
        url = youtube_url_receive.split("watch?v=")[1][0:11]
    elif youtube_url_receive.find("youtube.com") == -1:
        url = youtube_url_receive.split(".be/")[1]

    doc = {'youtube_url': url,
           'music': music_receive,
           'artist': artist_receive,
           'sort': sort_receive,
           'star': star_receive,
           'comment': comment_receive,
           'like': 0
           }
    db.music.insert_one(doc)

    return jsonify({'msg': '저장완료!!'})


# db에 저장된 데이터 불러와서 index.html로 리턴
@app.route("/smm", methods=["GET"])
def smm_get():
    all_data = list(db.music.find())
    return jsonify({'result': dumps(all_data)})
    
#카테고리별로 정보 내보내기
@app.route("/music", methods=["GET"])
def music_get():
    all_musics = list(db.music.find({},{'_id':False}))
    indi_musics = list(db.music.find({'sort':'인디'},{'_id':False}))
    balad_musics = list(db.music.find({'sort':'발라드'},{'_id':False}))
    dance_musics = list(db.music.find({'sort':'댄스'},{'_id':False}))
    hip_musics = list(db.music.find({'sort':'힙합'},{'_id':False}))
    pop_musics = list(db.music.find({'sort':'팝송'},{'_id':False}))
    rock_musics = list(db.music.find({'sort':'락'},{'_id':False}))

    return jsonify({'result': all_musics,
                    'result2':indi_musics,
                    'result3':balad_musics,
                    'result4':dance_musics,
                    'result5':hip_musics,
                    'result6':pop_musics,
                    'result7':rock_musics})

# like기능
@app.route("/like", methods=["POST"])
def like_up():
    id_receive = request.form['id_give']
    # _id값 매치해서 like값 조회
    present_like = db.music.find_one({"_id": ObjectId(id_receive)},{'_id':False, "like":True})
    print(present_like['like'])
    db.music.update_one({'_id': ObjectId(id_receive)},{'$set':{'like':present_like['like'] + 1}})

    return jsonify({'msg': '추천완료!'})

# 차트
@app.route("/chart", methods=["GET"])
def chart_get():
    all_data = list(db.music.find({}, {'_id':False}).sort([("like", -1)]).limit(5))
    return jsonify({'result': all_data})

if __name__ == '__main__':
    app.run()
