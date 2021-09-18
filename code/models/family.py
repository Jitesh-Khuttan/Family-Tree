from code.db.alchemy_db import db

class FamilyModel(db.Model):

	__tablename__ = "family"
	family_id = db.Column(db.Integer, primary_key=True)
	family_name = db.Column(db.String(60), nullable=False)
	members = db.relationship('MemberModel', backref='family_info', lazy=True)


	def to_json(self):
		family_members = [m.to_json() for m in self.members]
		for mem in family_members:
			del mem["family_name"]
			
		return {"family_id": self.family_id, "family_name": self.family_name, 
				"members": family_members}

	def add_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by_id(cls, family_id):
		return cls.query.filter_by(family_id=family_id).first()