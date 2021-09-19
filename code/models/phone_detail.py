from code.db.alchemy_db import db

class PhoneDetail(db.Model):

	__tablename__ = 'phone_detail'
	id = db.Column(db.Integer, primary_key=True)
	member_id = db.Column(db.Integer, db.ForeignKey('member.member_id', ondelete="CASCADE"))
	phone_number = db.Column(db.String(13))

	def to_json(self):
		return self.phone_number

	@classmethod
	def find_by_member_and_phone(cls, member_id, phone_number):
		return cls.query.filter_by(member_id=member_id, phone_number=phone_number).first()

	def add_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()