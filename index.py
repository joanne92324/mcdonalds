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
    if(action == "McDetails"):
       Hamburger = req.get("queryResult").get("parameters").get("Hamburger")
        if(Hamburger == "漢堡"):
            Hamburger = "麥香雞"
        elif(Hamburger == "大麥克"):
            Hamburger = "大麥克"
        info = "您選擇的食物是: " + Hamburger 
        if(cond == "品名"):
            collection_ref = db.collection("麥當勞")
            docs = collection_ref.get()
            found = False
            for doc in docs:
                dict = doc.to_dict()
                if keyword in dict["product"]:
                    found True
                    info += "品名: " + dict["product"] + "\n"
                    info += "網站: " + dict["hyperlink"] + "\n"
                    info += "熱量: " + dict["kcal"] + "\n"
                    info += "分類: " + dict["meat"] + "\n"
                if not found:
                    info += "很抱歉，目前無符合這個關鍵字的相關電影喔"
    return make_response(jsonify({"fulfillmentText": info}))

#if __name__ == "__main__":
#   app.run()