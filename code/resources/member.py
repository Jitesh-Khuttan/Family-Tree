from datetime import datetime
from flask_restful import Resource
from flask import request
from code.models.member import MemberModel
from code.utils.parsers import get_member_request_parser

_member_parser = get_member_request_parser()

class MemberRegister(Resource):

	def post(self):
		request_data = _member_parser.parse_args()
		try:
			request_data['birth_date'] = datetime.strptime(request_data['birth_date'], "%d-%m-%Y")
		except Exception as exp:
			return {"message": "Invalid date format! Please provide birth date in DD-MM-YYYY format."}, 400
		
		try:
			member = MemberModel(**request_data)
			member.add_to_db()
		except Exception as exp:
			return {"message": "Failed to add member.", "error": str(exp)}, 400

		return member.to_json(), 201


class Member(Resource):

	def get(self):
		member_id = request.args.get('memberid')
		first_name = request.args.get('firstname')
		last_name = request.args.get('lastname')

		if member_id:
			member = MemberModel.find_by_member_id(member_id)
			if member:
				return member.to_json(), 200

			return {"message": f"Member with id {member_id} not found!"}, 404

		if first_name:
			members = MemberModel.find_by_first_name(first_name)
			if members:
				return [m.to_json()for m in members], 200

			return {"message": f"No member with first name {first_name} found!"}, 404

		if last_name:
			members = MemberModel.find_by_last_name(last_name)
			if members:
				return [m.to_json()for m in members], 200

			return {"message": f"No member with last name {last_name} found!"}, 404

