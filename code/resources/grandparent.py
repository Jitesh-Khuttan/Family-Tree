from flask_restful import Resource
from code.models.parent_child import ParentChildModel
from code.models.member import MemberModel


class RetrieveGrandParent(Resource):

	def get(self, member_id):
		member = MemberModel.find_by_member_id(member_id)
		if member:
			grandparent = member.get_grandparents(to_json=True)
			return grandparent, 200

		return {"message": f"No member found with given id - {member_id}. Please provide valid member id."}


