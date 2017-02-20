from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Table
from server.run import db

"""
Contains table's models of the web monitoring part.
"""

webSite_has_notificationMethod = Table('webSite_has_notificationMethod', db.Model.metadata,
                                       Column('webSite_id', Integer, ForeignKey('webSite.webSite_id')),
                                       Column('notification_id', Integer,
                                              ForeignKey('notificationMethod.notification_id'))
                                       )


webSite_has_name = Table('webSite_has_name', db.Model.metadata,
                         Column('webSite_id', Integer, ForeignKey('webSite.webSite_id')),
                         Column('user_id', Integer, ForeignKey('user.user_id')),
                         Column('name', String(100))
                         )


class WebSite(db.Model):
    __tablename__ = 'webSite'
    webSite_id = Column(Integer, primary_key=True)
    url = Column(String(255), unique=True)
    name = Column(String(100), unique=False)

    def __init__(self, url=None, name=None):
        self.url = url
        self.name = name

    def __repr__(self):
        return '<WebSite %r %s>' % self.webSite_id, self.url


class NotificationMethod(db.Model):
    __tablename__ = "notificationMethod"
    notification_id = Column(Integer, primary_key=True)
    type = Column(String(45), primary_key=True)
    argument = Column(JSON, unique=False)
    userID = Column(Integer, ForeignKey('user.email'), nullable=False)

    def __init__(self, type=None, argument=None):
        self.type = type
        self.argument = argument

    def __repr__(self):
        return '<NotificationMethod %r>' % self.notification_id
