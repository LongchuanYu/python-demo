from pymongo import MongoClient
cliend = MongoClient()
db = cliend.test
ret = db.test.find()
t = list(ret[0]['a'])
print(t)