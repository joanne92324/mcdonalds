import requests
#from bs4 import BeautifulSoup

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

from flask import Flask, render_template, request, make_response, jsonify
from datetime import datetime, timezone, timedelta

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, LocationSendMessage 
)

line_bot_api = LineBotApi("UFdywBXGQuOh7Str7v4ypcoxIUnrQoD6GRcnxbtrZvCm4UFl/1rPDnIx7kHm9X8Cb2Vqz5Tgbm4iY3KFf6/GO6M4K63D22fmmnFLF0wR1A8hhHYtKvsNniLo0dpw4FHlePJvjrm9s8DFcSZbw3XWagdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler("43135f8efee8efe044fbf99076a02e41")

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>麥當勞資料讀取</h1>"
    homepage += "<br><a href=/read>麥當勞</a><br>"
    return homepage

@app.route("/read")
def read():
    Result = ""     
    collection_ref = db.collection("麥當勞")    
    docs = collection_ref.order_by("kcal", direction=firestore.Query.DESCENDING).get()    
    for doc in docs:         
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result

@app.route("/search", methods=["POST","GET"])
def search():
    if request.method == "POST":
        Mcdonaldproduct = request.form["Mcdonaldproduct"]

        info = ""     
        collection_ref = db.collection("麥當勞")
        #docs = collection_ref.where("title","==", "喜悅：達賴喇嘛遇見屠圖主教").get()
        docs = collection_ref.order_by("kcal").get()
        for doc in docs:
            if Mcdonaldproduct in doc.to_dict()["product"]: 
                info += "品名：" + doc.to_dict()["product"] + "<br>" 
                info += "熱量：" + doc.to_dict()["kcal"] + "<br>"
                info += "食物介紹：" + doc.to_dict()["hyperlink"] + "<br>"
                info += "分類：" + doc.to_dict()["meat"] + "<br><br>"       
        return info
    else:  
        return render_template("input.html")

@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text= "我是食物機器人，您輸入的是：" + event.message.text + "。祝福您有個美好的一天！" ))

def searchMcdonald(keyword):
    info = "您要查詢食物，關鍵字為：\n" + keyword
    collection_ref = db.collection("麥當勞")
    docs = collection_ref.order_by("kcal").get()
    found = False
    for doc in docs:
        if keyword in doc.to_dict()["product"]:
            found = True 
            info += "品名：" + doc.to_dict()["product"] + "\n" 
            info += "熱量：" + doc.to_dict()["kcal"] + "\n"
            info += "食物介紹：" + doc.to_dict()["hyperlink"] + "\n"
            info += "分類：" + doc.to_dict()["meat"] + "\n" 
    if not found:
       info += "很抱歉，目前無符合這個關鍵字的相關食物喔"                   
    return info

@app.route("/webhook", methods=["POST"])
def webhook():
    # build a request object
    req = request.get_json(force=True)
    # fetch queryResult from json
    action =  req.get("queryResult").get("action")
    #msg =  req.get("queryResult").get("queryText")
    #info = "動作：" + action + "； 查詢內容：" + msg
    if (action == "rateChoice"):
        McDonald =  req.get("queryResult").get("parameters").get("McDonald")
        if (McDonald == "牛"):
            McDonald = "牛肉"
        elif (McDonald == "雞"):
            McDonald = "雞"
        elif (McDonald == "魚"):
            McDonald = "魚"
        elif (McDonald == "漢堡"):
            McDonald = "漢堡"
        elif (McDonald == "派"):
            McDonald = "蘋果派"
        elif (McDonald == "雞腿"):
            McDonald = "雞腿"
        elif (McDonald == "雞翅"):
            McDonald = "雞翅"
        elif (McDonald == "薯條"):
            McDonald = "薯條"
        elif (McDonald == "沙拉"):
            McDonald = "沙拉"
        elif (McDonald == "雞塊"):
            McDonald = "雞塊"
        info = "您選擇的食物分類是：" + McDonald + "，相關食物：\n"

        collection_ref = db.collection("麥當勞")
        docs = collection_ref.get()
        result = ""
        for doc in docs:
            dict = doc.to_dict()
            if McDonald in dict["McDonald"]:
                result += "品名：" + dict["product"] + "\n"
                result += "熱量：" + dict["kcal"] + "\n"
                result += "分類：" + dict["meat"] + "\n"
                result += "細項：" + dict["hyperlink"] + "\n\n"
        info += result
    elif (action == "McdonaldDetail"): 
        cond =  req.get("queryResult").get("parameters").get("McDonald")
        keyword =  req.get("queryResult").get("parameters").get("any")
        info = "您要查詢品名的" + cond + "，關鍵字是：" + keyword + "\n\n"
        if (cond == "品名"):
            collection_ref = db.collection("麥當勞")
            docs = collection_ref.get()
            found = False
            for doc in docs:
                dict = doc.to_dict()
                if keyword in dict["product"]:
                    found = True 
                    info += "品名：" + dict["product"] + "\n"
                    info += "熱量：" + dict["kcal"] + "\n"
                    info += "細項：" + dict["hyperlink"] + "\n"
                    info += "分類：" + dict["meat"] + " \n"
            if not found:
                info += "很抱歉，目前無符合這個關鍵字的相關食物喔"

    return make_response(jsonify({"fulfillmentText": info}))

#if __name__ == "__main__":
#    app.run()