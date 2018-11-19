from datetime import datetime
from garbageRO import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
	
class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(60), nullable=False)

class Dumpster(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location = db.Column(db.String, nullable=False)
	full = db.Column(db.Boolean, nullable=False)
	onRoute = db.Column(db.Boolean, nullable=False)
	lat = db.Column(db.Float, nullable=False)
	lng = db.Column(db.Float, nullable=False)
	pickups = db.relationship('Pickup', backref='dumpster', lazy=True)
	
	def __repr__(self):
		return f"Dumpster('{self.id}', '{self.location}')"
	
class Pickup(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	time = db.Column(db.String, nullable=True, default='midnight')
	dumpsterLocation = db.Column(db.String, db.ForeignKey('dumpster.location'), nullable=False)
	
	def __repr__(self):
		return f"Pickup('{self.id}', 'dumpster.location', '{self.date}')"