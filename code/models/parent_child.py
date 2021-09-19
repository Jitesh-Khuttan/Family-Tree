from code.db.alchemy_db import db

class ParentChildModel(db.Model):

	__tablename__ = "parent_child"
	parent_id = db.Column(db.Integer, db.ForeignKey('member.member_id', ondelete="CASCADE"), primary_key=True)
	child_id = db.Column(db.Integer, db.ForeignKey('member.member_id', ondelete="CASCADE"), primary_key=True)

	def to_json(self):
		return {"parent_id": self.parent_id, "child_id": self.child_id}

	@classmethod
	def find_relation_by_ids(cls, pid, cid):
		result = cls.query.filter_by(parent_id=pid, child_id=cid).all()
		return result

	def add_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()