from code.db.alchemy_db import db

class MemberModel(db.Model):

	__tablename__ = "member"
	member_id = db.Column(db.Integer, primary_key=True)
	family_id = db.Column(db.Integer, db.ForeignKey('family.family_id'), nullable=False)
	first_name = db.Column(db.String(60), nullable=False)
	last_name = db.Column(db.String(60), nullable=True)
	birth_date = db.Column(db.DateTime, nullable=False)

	parents = db.relationship("MemberModel", secondary="parent_child", primaryjoin="MemberModel.member_id==parent_child.c.child_id", 
							  secondaryjoin="MemberModel.member_id==parent_child.c.parent_id", backref="children", lazy=True)

	def to_json(self):
		return {"member_id": self.member_id, "family_name": self.family_info.family_name,
				"first_name": self.first_name, "last_name": self.last_name, "birth_date": self.birth_date.strftime("%d-%m-%Y"),
				"parents": [{"member_id": p.member_id, "first_name": p.first_name, "last_name": p.last_name} for p in self.parents]}

	def add_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by_id(cls, family_id):
		return cls.query.filter_by(family_id=family_id).first()

	@classmethod
	def find_by_first_name(cls, first_name):
		return cls.query.filter_by(first_name=first_name)

	@classmethod
	def find_by_last_name(cls, last_name):
		return cls.query.filter_by(last_name=last_name)


