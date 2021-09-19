from flask_restful import Resource
from flask_jwt_extended import jwt_required
from code.models.parent_child import ParentChildModel
from code.models.member import MemberModel
from code.utils.parsers import get_sibling_request_parser
import logging
logging.basicConfig(level=2)


_sibling_parser = get_sibling_request_parser()


class Sibling(Resource):

	def post(self):
		request_data = _sibling_parser.parse_args()
		sibling_1 = MemberModel.find_by_member_id(request_data['sibling_id1'])
		parents = sibling_1.get_parents()

		if not parents:
			return {"message": f"No parent found for sibling id - {request_data['sibling_id1']}. Hence can't add sibling."}, 400

		for parent in parents:
			pc_relation = ParentChildModel(parent_id=parent.get_member_id(), child_id=request_data['sibling_id2'])
			pc_relation.add_to_db()

		return {"message": "Successfully added sibling relation."}

	@jwt_required()
	def delete(self):
		request_data = _sibling_parser.parse_args()
		logging.error(f"Request:- {request_data}")
		sibling_1 = MemberModel.find_by_member_id(request_data['sibling_id1'])
		parents = sibling_1.get_parents()

		if not parents:
			return {"message": f"No parent found for sibling id - {request_data['sibling_id1']}. Hence can't remove sibling."}, 400

		for parent in parents:
			pc_relation = ParentChildModel.find_relation_by_ids(pid=parent.get_member_id(), cid=request_data['sibling_id2'])
			logging.error(f"Found- {pc_relation}")
			if pc_relation:
				for pc in pc_relation:
					pc.delete_from_db()

		return {"message": "Sibling removed successfully!"}, 200



class RetrieveSibling(Resource):

	def get(self, member_id):
		member = MemberModel.find_by_member_id(member_id)
		if member:
			siblings = member.get_siblings(to_json=True)
			return siblings, 200

		return {"message": f"No member found with given id - {member_id}. Please provide valid member id."}


