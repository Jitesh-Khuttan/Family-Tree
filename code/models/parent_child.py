from code.db.alchemy_db import db

class ParentChildModel(db.Model):

	__tablename__ = "parent_child"
	parent_id = db.Column(db.Integer, db.ForeignKey('member.member_id', ondelete="CASCADE"), primary_key=True)
	child_id = db.Column(db.Integer, db.ForeignKey('member.member_id', ondelete="CASCADE"),primary_key=True)

	def to_json(self):
		return {"parent_id": self.parent_id, "child_id": self.child_id}

	def add_to_db(self):
		db.session.add(self)
		db.session.commit()