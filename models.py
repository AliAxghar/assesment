from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    referrals = db.relationship("Referral", backref="referrer", lazy=True)


class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_id = db.Column(db.Integer, db.ForeignKey("client.id"), nullable=False)
    referred_email = db.Column(db.String(120), nullable=False)


class PointTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=True)
    points = db.Column(db.Integer, default=0)
