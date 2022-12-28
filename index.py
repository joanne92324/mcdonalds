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
    homepage = "<h1>麥當勞資料讀取5</h1>"
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
    info = ""
    if (action == "McDetails"):
        Hamburger =  req.get("queryResult").get("parameters").get("Hamburger")
        #info = "食物類型：" + Hamburger  
        collection_ref = db.collection("麥當勞")
        docs = collection_ref.get()
        found = False
        for doc in docs:
            if Hamburger in doc.to_dict()["product"]:
                found = True 
                info += "您要查詢" + Hamburger + "的什麼資訊?" + "\n" 
        if not found:
            info += "很抱歉，目前無符合這個關鍵字的相關食物喔"
    elif (action == "Mc"): 
        cond =  req.get("queryResult").get("parameters").get("McdonaldQ")
        McdonaldQ =  req.get("queryResult").get("parameters").get("McdonaldQ")
        if(cond == "熱量")
        collection_ref = db.collection("麥當勞")
        docs = collection_ref.get()
        found = False
        for doc in docs:
            if Hamburger in doc.to_dict()["product"]:
                found = True 
                info += "品名：" + doc.to_dict()["product"] + "\n"
                info += "熱量：" + doc.to_dict()["kcal"] + "大卡" + "\n" 
        if not found:
            info += "很抱歉，目前無符合這個關鍵字的相關食物喔"
    return make_response(jsonify({"fulfillmentText": info}))

if __name__ == "__main__":
   app.run()