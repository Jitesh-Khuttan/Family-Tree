from code.db.alchemy_db import db

class EmailDetail(db.Model):

	__tablename__ = 'email_detail'
	id = db.Column(db.Integer, primary_key=True)
	member_id = db.Column(db.Integer, db.ForeignKey('member.member_id', ondelete="CASCADE"), nullable=False)
	email_id = db.Column(db.String(60), nullable=False)

	def to_json(self):
		return self.email_id

	@classmethod
	def find_by_member_and_email(cls, member_id, email):
		return cls.query.filter_by(member_id=member_id, email_id=email).first()

	def add_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()