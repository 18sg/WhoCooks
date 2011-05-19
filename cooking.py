import pymongo
import datetime
import functools

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
	names = [p["username"] for p in db.people.find()]
	
	priorities = [(p, times_eaten_since_cooked(db, p)) for p in names]

	return sorted(priorities, key=lambda p: p[1])

def insert(db, chef, eaters):
	db.cooked.insert(
		{"chef": username_to_id(db, chef),
		 "eaters": [username_to_id(db, e) for i in eaters],
		 "time": datetime.datetime.now()})

def username_to_id(db, uname):
	return db.cooked.find_one({"username": uname})["_id"]

if __name__ == "__main__":
	db = pymongo.Connection()
	print priorities(db.test)
