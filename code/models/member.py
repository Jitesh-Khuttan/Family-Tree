from code.db.alchemy_db import db
import itertools

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
				"first_name": self.first_name, "last_name": self.last_name, "birth_date": self.birth_date.strftime("%d-%m-%Y")}

	def get_parents(self, to_json=False):
		if to_json:
			return [{"member_id": p.member_id, "first_name": p.first_name, "last_name": p.last_name} for p in self.parents]
		
		return self.parents

	def get_children(self, to_json=False):
		if to_json:
			return [{"member_id": c.member_id, "first_name": c.first_name, "last_name": c.last_name} for c in self.children]

		return self.children

	def get_siblings(self, to_json=False):
		_siblings = list(set(itertools.chain.from_iterable([parent.get_children() for parent in self.parents])))
		if _siblings:
			_siblings.remove(self)

		if to_json:
			return [{"member_id": s.member_id, "first_name": s.first_name, "last_name": s.last_name} for s in _siblings]

		return _siblings

	def get_grandparents(self, to_json=False):
		_grandparents = list(set(itertools.chain.from_iterable([parent.get_parents() for parent in self.parents])))

		if to_json:
			return [{"member_id": g.member_id, "first_name": g.first_name, "last_name": g.last_name} for g in _grandparents]

		return _grandparents

	def get_cousins(self, to_json=False):
		_cousins = list(set(itertools.chain.from_iterable([uncle_aunt.get_children() for parent in self.parents for uncle_aunt in parent.get_siblings()])))

		if to_json:
			return [{"member_id": c.member_id, "first_name": c.first_name, "last_name": c.last_name} for c in _cousins]

		return _cousins

	def get_member_id(self):
		return self.member_id

	def add_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by_family_id(cls, family_id):
		return cls.query.filter_by(family_id=family_id).first()

	@classmethod
	def find_by_member_id(cls, member_id):
		return cls.query.filter_by(member_id=member_id).first()

	@classmethod
	def find_by_first_name(cls, first_name):
		return cls.query.filter_by(first_name=first_name)

	@classmethod
	def find_by_last_name(cls, last_name):
		return cls.query.filter_by(last_name=last_name)


