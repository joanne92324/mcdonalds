import requests
#from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>麥當勞資料讀取</h1>"
    homepage += "<br><a href=/read>麥當勞</a><br>"
    homepage += "<br><a href=/webhook>麥當勞資料查詢</a><br>"
    return homepage

@app.route("/read")
def read():
    Result = ""     
    collection_ref = db.collection("麥當勞")    
    docs = collection_ref.order_by("kcal", direction=firestore.Query.DESCENDING).get()    
    for doc in docs:         
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result

@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    action =  req["queryResult"]["action"]
    #msg =  req["queryResult"]["queryText"]
    #info = "動作 :" + action+"; 查詢內容 :" + msg
        collection_ref = db.collection("麥當勞")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if rate in dict["Hamburger"]:
                result += "品名：" + dict["product"] + "\n"
                result += "介紹：" + dict["hyperlink"] + "\n"
                result += "熱量：" + dict["kcal"] + "\n"
                result += "分類：" + dict["meat"] + "\n\n"
       info +=result

    return make_response(jsonify({"fulfillmentText": info}))

#if __name__ == "__main__":
#   app.run()