from code.db.alchemy_db import db

class AddressDetail(db.Model):

	__tablename__ = 'address_detail'
	id = db.Column(db.Integer, primary_key=True)
	member_id = db.Column(db.Integer, db.ForeignKey('member.member_id', ondelete="CASCADE"), nullable=False)
	address = db.Column(db.String(60), nullable=False)

	def to_json(self):
		return self.address

	@classmethod
	def find_by_member_and_address(cls, member_id, address):
		return cls.query.filter_by(member_id=member_id, address=address).first()

	def add_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()