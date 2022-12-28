elif (action == "Mc"): 
        cond =  req.get("queryResult").get("parameters").get("McdonaldQ")
        keyword =  req.get("queryResult").get("parameters").get("any")
        info = "您要查詢食物的" + cond + "，關鍵字是：" + keyword + "\n\n"
        if (cond == "品名"):
            collection_ref = db.collection("麥當勞")
            docs = collection_ref.order_by("kcal").get()
            found = False
            for doc in docs:
                if keyword in doc.to_dict()["product"]:
                    found = True 
                    info += "品名：" + doc.to_dict()["product"] + "\n" 
                    info += "食物介紹：" + doc.to_dict()["hyperlink"] + "\n"
                    info += "熱量：" + doc.to_dict()["kcal"] + "\n" 
                    info += "分類：" + doc.to_dict()["meat"] + "\n\n"
            if not found:
                info += "很抱歉，目前無符合這個關鍵字的相關食物喔"



                elif (action == "Mc"): 
        cond =  req.get("queryResult").get("parameters").get("McdonaldQ")
        info += "好的，為您查詢" + "\n\n"
        collection_ref = db.collection("麥當勞")
            docs = collection_ref.get()
            found = False
            for doc in docs:
                if cond in doc.to_dict()["product"]:
                    found = True 
                    info += "熱量：" + doc.to_dict()["kcal"] + "\n" 
            if not found:
                info += "很抱歉，目前無符合這個關鍵字的相關食物喔"