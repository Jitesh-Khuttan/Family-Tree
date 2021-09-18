from flask_restful import Resource
from code.utils.parsers import get_family_request_parser
from code.models.family import FamilyModel


_family_parser = get_family_request_parser()

class RegisterFamily(Resource):

	def post(self):
		request_data = _family_parser.parse_args()
		family = FamilyModel(**request_data)
		family.add_to_db()

		return family.to_json(), 201

class Family(Resource):

	def get(self, family_id):
		family = FamilyModel.find_by_id(family_id)
		if family:
			return family.to_json(), 200

		return {"message": f"Family with id '{family_id}' not found"}, 404

