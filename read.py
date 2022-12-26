import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

collection_ref = db.collection("麥當勞")
docs = collection_ref.order_by("kcal", direction=firestore.Query.DESCENDING).get()
for doc in docs:
	print("{}\n".format(doc.to_dict()))

