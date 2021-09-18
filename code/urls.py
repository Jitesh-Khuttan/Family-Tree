from flask_restful import Api
from code.resources.user import UserRegister, User, UserLogin
from code.resources.family import RegisterFamily, Family
from code.resources.member import MemberRegister, Member


def initialize_urls(app):
	api = Api(app)

	#User APIs
	api.add_resource(UserRegister, '/user/register')
	api.add_resource(UserLogin, '/login')
	api.add_resource(User, '/user/<string:name>')

	#Family APIs
	api.add_resource(RegisterFamily, '/family/register')
	api.add_resource(Family, '/family/<family_id>')

	#Member APIs
	api.add_resource(MemberRegister, '/member/register')
	api.add_resource(Member, '/member')

	return app