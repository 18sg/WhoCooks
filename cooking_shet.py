import cooking
from shet.client import ShetClient, shet_action


class CookingClient(ShetClient):
	
	def __init__(self, root, db):
		self.root = root
		self.db = db
		ShetClient.__init__(self)
	
	@shet_action
	def add_event(self, chef, eaters):
		return cooking.insert(self.db, chef, eaters)
	
	@shet_action
	def order(self):
		return cooking.priorities(self.db)
	
	@shet_action
	def recent(self, n=10):
		return cooking.recent(self.db, n)
	
	@shet_action
	def remove(self, oid):
		return cooking.remove(self.db, oid)


if __name__ == "__main__":
	CookingClient("/cooking/", cooking.connect()).run()
