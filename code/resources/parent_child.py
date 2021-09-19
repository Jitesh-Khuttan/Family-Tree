from flask_restful import Resource
from code.models.parent_child import ParentChildModel
from code.models.member import MemberModel
from code.utils.parsers import get_parentchild_request_parser



_parent_child_parser = get_parentchild_request_parser()


class ParentChild(Resource):

	def post(self):
		request_data = _parent_child_parser.parse_args()
		pc_relation = ParentChildModel(**request_data)
		try:
			pc_relation.add_to_db()
			return pc_relation.to_json(), 201
		except Exception as exp:
			return {"message": "Failed to add parent-child relation.", "errors": str(exp)}


class RetrieveParent(Resource):

	def get(self, member_id):
		member = MemberModel.find_by_member_id(member_id)
		if member:
			return member.get_parents(to_json=True), 200

		return {"message": f"No member found with given id - {member_id}. Please provide valid member id."}

class RetrieveChildren(Resource):

	def get(self, member_id):
		member = MemberModel.find_by_member_id(member_id)
		if member:
			return member.get_children(to_json=True), 200

		return {"message": f"No member found with given id - {member_id}. Please provide valid member id."}