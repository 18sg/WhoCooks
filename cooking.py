import pymongo
from bson.objectid import ObjectId
import datetime

def last_cooked(db, pid):
	cookings = db.cooked.find({"chef": pid}).sort("time", pymongo.DESCENDING).limit(1)
	return cookings[0]["time"] if cookings.count() else None

def times_eaten_since_cooked(db, pid):
	t = last_cooked(db, pid)
	if t is not None:
		return db.cooked.find({"eaters": pid, "time": {"$gt": t}}).count()
	else:
		return db.cooked.find({"eaters": pid}).count()

def priorities(db):
	names = [(p["_id"], p["username"]) for p in db.people.find()]
	
	priorities = [(name, times_eaten_since_cooked(db, pid)) for pid, name in names]
	
	return sorted(priorities, key=lambda p: p[1], reverse=True)

def insert(db, chef, eaters):
	db.cooked.insert(
		{"chef": username_to_id(db, chef),
		 "eaters": [username_to_id(db, e) for e in eaters],
		 "time": datetime.datetime.now()})

def recent(db, n=10):
	return [(id_to_username(db, r["chef"]),
	         [id_to_username(db, e) for e in r["eaters"]],
	         str(r["time"]),
	         str(r["_id"]))
	        for r in db.cooked.find().sort("time", pymongo.DESCENDING).limit(n)]

def remove(db, oid):
	assert oid is not None # Would remove the entire collection :s
	db.cooked.remove(ObjectId(oid))

def username_to_id(db, uname):
	return db.people.find_one({"username": uname})["_id"]

def id_to_username(db, pid):
	return db.people.find_one({"_id": pid})["username"]

def connect():
	return pymongo.Connection()["18sg"]

if __name__ == "__main__":
	print priorities(connect())

