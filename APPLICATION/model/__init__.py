from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime, String, Boolean
from datetime import datetime
from sqlalchemy.orm import relationship, backref

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(DateTime, default=datetime.now)
    modified_date = Column(DateTime, default=datetime.now)
    email = Column(String(50), unique=True)
    password = Column(String(80))
    active = Column(Boolean, default=False)
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(DateTime, default=datetime.now)
    modified_date = Column(DateTime, default=datetime.now)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(DateTime, default=datetime.now)
    modified_date = Column(DateTime, default=datetime.now)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))

# class Client(db.Model):
#     __tablename__ = 'client'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     creation_date = Column(DateTime, default=datetime.now())
#     modified_date = Column(DateTime, default=datetime.now())
#     company_name = db.Column(db.String(255), unique=True)
#     shared = db.Column(db.Boolean())
#     user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
#     client_meta = relationship('ClientMeta', backref=backref('client'))
#     client_memo = relationship('ClientMemo', backref=backref('client'))
#
#
# class ClientMeta(db.Model):
#     __tablename__ = 'client_meta'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     creation_date = Column(DateTime, default=datetime.now())
#     modified_date = Column(DateTime, default=datetime.now())
#     meta_id = db.Column(db.String(255))
#     value = db.Column(db.String(255))
#     description = db.Column(db.String(255))
#     type = db.Column(db.String(255))
#     user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
#     client_id = db.Column('client_id', db.Integer(), db.ForeignKey('client.id'))
#
#
# class ClientMemo(db.Model):
#     __tablename__ = 'client_memo'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     creation_date = Column(DateTime, default=datetime.now())
#     modified_date = Column(DateTime, default=datetime.now())
#     value = db.Column(db.String(255))
#     client_id = db.Column('client_id', db.Integer(), db.ForeignKey('client.id'))
#
#
# class Candidat(db.Model):
#     __tablename__ = 'candidat'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     creation_date = Column(DateTime, default=datetime.now())
#     modified_date = Column(DateTime, default=datetime.now())
#     candidat_meta = relationship('CandidatMeta', backref=backref('candidat'))
