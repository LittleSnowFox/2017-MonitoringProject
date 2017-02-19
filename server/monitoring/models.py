from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Table
from server.run import db

"""
Contains table's models of the web monitoring part.
"""

webSite_has_notificationMethod = Table('webSite_has_notificationMethod', db.Model.metadata,
                                       Column('webSite_id', Integer, ForeignKey('webSite.ws_id')),
                                       Column('notificationMethod_type', String(45), ForeignKey('notificationMethod.type'))
                                       )


class WebSite(db.Model):
    __tablename__ = 'webSite'
    ws_id = Column(Integer, unique=True, primary_key=True)
    url = Column(String(255), unique=True)
    name = Column(String(100), unique=False)

    def __init__(self, ws_id=None, url=None, name=None):
        self.ws_id = ws_id
        self.url = url
        self.name = name

    def __repr__(self):
        return '<WebSite %r>' % (self.ws_id)


class NotificationMethod(db.Model):
    __tablename__ = "notificationMethod"
    type = Column(String(45), primary_key=True)
    argument = Column(JSON, unique=False)
    userID = Column(Integer, ForeignKey('user.email'))

    def __init__(self, type=None, argument=None):
        self.type = type
        self.argument = argument

    def __repr__(self):
        return '<NotificationMethod %r>' % (self.type)
