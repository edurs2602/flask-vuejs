from . import db

class UserPreferences(db.EmbeddedDocument):
    timezone = db.StringField(required=True)

class User(db.Document):
    username = db.StringField(required=True)
    password = db.StringField(required=True)
    roles = db.ListField(db.StringField(), default=list)
    preferences = db.EmbeddedDocumentField(UserPreferences, required=True)
    active = db.BooleanField(default=True)
    created_ts = db.FloatField(required=True)