from .user import UserDocument as User
from ethjsonrpc import wei_to_ether

class Tag:
	pass

class Member(User):

	organization = None
	rights = dict()

	def __init__(self, user):
		super().__init__()

	
	def canDo(self, action):
		pass

	def initFromRights(self, rights):
		if isinstance(rights, dict):
			pass
		elif isinstance(rights, Tag):
			pass
		return None

	def setRight(self, action, right):
		pass

	def setRightFromTag(self, action, tag):
		pass