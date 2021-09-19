from flask_restful import Resource
from flask_jwt_extended import jwt_required
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

	@jwt_required()
	def delete(self):
		request_data = _parent_child_parser.parse_args()
		pc_relation = ParentChildModel.find_relation_by_ids(pid=request_data['parent_id'], cid=request_data['child_id'])
		try:
			if pc_relation:
				for pc in pc_relation:
					pc.delete_from_db()
				return {"message": "Relation deleted successfully!"}, 200
			return {"message": "No relation found!"}, 404
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