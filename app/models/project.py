from mongokat import Collection, Document
from .db import client

class ProjectDocument(Document):
	pass

class ProjectCollection(Collection):
	pass

projects = ProjectCollection(collection=client.main.projects)