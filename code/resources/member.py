from datetime import datetime
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask import request
from code.models.member import MemberModel
from code.models.address_detail import AddressDetail
from code.models.email_detail import EmailDetail
from code.models.phone_detail import PhoneDetail
from code.utils.parsers import ( get_member_request_parser, get_member_post_later_data_request_parser,
	get_member_update_data_request_parser, get_member_delete_parser )

_member_parser = get_member_request_parser()
_member_optional_parser = get_member_post_later_data_request_parser()
_member_update_parser = get_member_update_data_request_parser()
_member_del_parser = get_member_delete_parser()


class Member(Resource):

	def post(self):
		request_data = _member_parser.parse_args()
		try:
			request_data['birth_date'] = datetime.strptime(request_data['birth_date'], "%d-%m-%Y")
		except Exception as exp:
			return {"message": "Invalid date format! Please provide birth date in DD-MM-YYYY format."}, 400
		
		try:
			required_details = {k:request_data[k] for k in ["family_id", "first_name", "last_name", "birth_date"]}
			member = MemberModel(**required_details)
			member.add_to_db()
		except Exception as exp:
			return {"message": "Failed to add member.", "error": str(exp)}, 400

		if request_data.get("address"):
			AddressDetail(member_id=member.get_member_id(), address=request_data["address"]).add_to_db()

		if request_data.get("email"):
			EmailDetail(member_id=member.get_member_id(), email_id=request_data["email"]).add_to_db()

		if request_data.get("phone_number"):
			EmailDetail(member_id=member.get_member_id(), phone_number=request_data["phone_number"]).add_to_db()

		return member.to_json(), 201
	
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



class MemberDetails(Resource):

	def post(self):
		"""
		Used to insert data for member if it was skipped while registering member. "member_id" is required.
		"""
		request_data = _member_optional_parser.parse_args()
		member = MemberModel.find_by_member_id(request_data["member_id"])

		if not member:
			return {"message": f"Member with id {request_data['member_id']} not found!"}, 404

		if request_data.get("address"):
			AddressDetail(member_id=member.get_member_id(), address=request_data["address"]).add_to_db()

		if request_data.get("email"):
			EmailDetail(member_id=member.get_member_id(), email_id=request_data["email"]).add_to_db()

		if request_data.get("phone_number"):
			PhoneDetail(member_id=member.get_member_id(), phone_number=request_data["phone_number"]).add_to_db()

		return {"message": "Data added successfully!"}, 201

	def put(self):
		request_data = _member_update_parser.parse_args()
		member = MemberModel.find_by_member_id(request_data["member_id"])

		if not member:
			return {"message": f"Member with id {request_data['member_id']} not found!"}, 404

		if request_data.get("current_address") and request_data.get("new_address"):
			address_info = AddressDetail.find_by_member_and_address(member_id=member.get_member_id(), address=request_data['current_address'])
			if address_info:
				address_info.address = request_data['new_address']
				address_info.add_to_db()

		if request_data.get("current_email") and request_data.get("new_email"):
			email_info = EmailDetail.find_by_member_and_email(member_id=member.get_member_id(), email=request_data['current_email'])
			if email_info:
				email_info.email_id = request_data['new_email']
				email_info.add_to_db()

		if request_data.get("current_phone_number") and request_data.get("new_phone_number"):
			phone_info = PhoneDetail.find_by_member_and_phone(member_id=member.get_member_id(), phone_number=request_data['current_phone_number'])
			if phone_info:
				phone_info.phone_number = request_data['new_phone_number']
				phone_info.add_to_db()

		return {"message": "Data updated successfully!"}, 201