from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Table, DateTime
from server.run import db
import datetime

"""
Contains table's models of the web monitoring part.
"""

website_has_name = Table('website_has_name', db.Model.metadata,
                         Column('website_id', Integer, ForeignKey('website.website_id', ondelete='CASCADE'), primary_key=True),
                         Column('user_id', Integer, ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True),
                         Column('name', String(100))
                         )

website_has_notification = Table('website_has_notification', db.Model.metadata,
                                 Column('website_id', Integer, ForeignKey('website.website_id', ondelete='CASCADE'), primary_key=True),
                                 Column('notification_id', Integer, ForeignKey('notification.notification_id', ondelete='CASCADE'),
                                        primary_key=True)
                                 )


class WebSite(db.Model):
    __tablename__ = 'website'
    website_id = Column(Integer, primary_key=True)
    url = Column(String(255), unique=True)
    last_time_monitored = Column(DateTime, unique=False, default=datetime.datetime.now())

    def __init__(self, url=None):
        self.url = url

    def __repr__(self):
        return '<WebSite %r %s>' % (self.website_id, self.url)


class Notification(db.Model):
    __tablename__ = "notification"
    notification_id = Column(Integer, primary_key=True)
    method = Column(String(45))  # phone, email, slack,...
    method_arguments = Column(JSON, unique=False)  # phone number:value, token:value, chanel:value,...
    user_id = Column(Integer, ForeignKey('user.user_id', ondelete='CASCADE'), nullable=False)


    def __init__(self, method=None, method_arguments=None, user_id=None):
        self.method = method
        self.method_arguments = method_arguments
        self.user_id = user_id

    def __repr__(self):
        return '<Notification %r>' % self.notification_id, self.method_arguments, self.argument, self.user_id
