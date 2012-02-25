# encoding: utf-8

import hashlib

import web.core
import mongoengine as db

from datetime import datetime, timedelta



class User(db.Document):
    meta = dict(
            allow_inheritance = False,
            collection = "users",
            indexes = [('handle', '_password')]
        )
    
    id = db.ObjectIdField('_id')
    handle = db.StringField(max_length=64, required=True)
    _password = db.StringField(db_field='password')
    name = db.StringField(max_length=200, required=True)
    email = db.EmailField(required=True)
    
    created = db.DateTimeField(default=datetime.utcnow)
    modified = db.DateTimeField()
    logged = db.DateTimeField()
    
    disabled = db.DateTimeField()
    
    def __repr__(self):
        return "User(%s, %s, \"%s\", %s%s)" % (self.id, self.handle, self.name)
    
    @staticmethod
    def hash(value):
        return hashlib.sha512(web.core.config['quorum.salt'] + value)
    
    @property
    def password(self):
        return self._password
    
    @password.setter
    def password(self, value):
        self._password = self.hash(value)
    
    @classmethod
    def lookup(cls, id):
        return cls.objects(id=id).first()
    
    @classmethod
    def authenticate(cls, handle, password=None, force=False):
        if force:
            user = cls.objects(handle=handle).first()
        
        else:
            user = cls.objects(handle=handle, _password=cls.hash(password)).first()
        
        if not user:
            return None
        
        user.logged = datetime.utcnow()
        user.save()
        
        return user.id, user
