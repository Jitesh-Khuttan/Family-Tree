from flask_restful import Resource
from code.models.parent_child import ParentChildModel
from code.models.member import MemberModel


class RetrieveCousin(Resource):

	def get(self, member_id):
		member = MemberModel.find_by_member_id(member_id)
		if member:
			cousins = member.get_cousins(to_json=True)
			return cousins, 200

		return {"message": f"No member found with given id - {member_id}. Please provide valid member id."}


