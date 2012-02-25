# encoding: utf-8

import hashlib

import web.core
import mongoengine as db

from datetime import datetime, timedelta



class User(db.Document):
    meta = dict(
            allow_inheritance = False,
            collection = 'users',
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
        return "User(%s, %s, \"%s\", %s)" % (self.id, self.handle, self.name, self.email)
    
    @staticmethod
    def hash(value):
        return hashlib.sha512(web.core.config['quorum.salt'] + value).hexdigest()
    
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


class Project(db.Document):
    meta = dict(
            allow_inheritance = False,
            collection = 'projects',
            indexes = ['name']
        )
    
    id = db.ObjectIdField('_id')
    
    name = db.StringField()
    description = db.StringField()
    
    public = db.BooleanField(default=True)
    abstention = db.BooleanField(default=True)
    
    creator = db.ReferenceField(User)
    created = db.DateTimeField(default=datetime.utcnow)
    modified = db.DateTimeField()


class Issue(db.Document):
    meta = dict(
            allow_inheritance = False,
            collection = 'issues',
            indexes = ['priority']
        )
    
    id = db.ObjectIdField('_id')
    
    project = db.ReferenceField(Project)
    name = db.StringField()
    description = db.StringField()
    priority = db.IntField(default=0, choices=[-1,0,1,2]) # Low, Normal, High, Emergency
    
    votes = db.DictField(field=db.BooleanField()) # True = yea, False = nay, None = abstain, missing = not present
    result = db.BooleanField()
    
    creator = db.ReferenceField(User)
    created = db.DateTimeField(default=datetime.utcnow)
    modified = db.DateTimeField()
    closed = db.DateTimeField()


class State(db.Document):
    meta = dict(
            allow_inheritance = True,
            collection = 'workflow',
            indexes = [('category', 'name')]
        )
    
    id = db.ObjectIdField('_id')
    
    previous = db.ReferenceField('self')
    next = db.ReferenceField('self')
    
    category = db.StringField()
    name = db.StringField()
    description = db.StringField()
    
    duration = db.IntField(default=48)
    timeout = db.StringField(default='pass', choices=['fail', 'pass', 'success', 'test'])
    mutable = db.BooleanField(default=True)
    
    creator = db.ReferenceField(User)
    created = db.DateTimeField(default=datetime.utcnow)
    modified = db.DateTimeField()


class TabledState(State):
    pass


class VoteState(State):
    pass


def data():
    start = TabledState(category="Board Vote", name="Proposal", description="Get another board member to second the motion.", duration=24, timeout='fail', mutable=False)
    discuss = State(category="Board Vote", name="Discussion Period", description="Discuss the motion amongst the board members.", duration=24, timeout='pass', mutable=True)
    vote = VoteState(category="Board Vote", name="Voting Period", description="Vote on the motion.", duration=48, timeout='test', mutable=True)
    
    start.save()
    
    discuss.previous = start
    discuss.save()
    
    vote.previous = discuss
    vote.save()
    
    start.next = discuss
    start.save()
    
    discuss.next = vote
    discuss.save()
