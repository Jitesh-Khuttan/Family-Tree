from flask_restful import reqparse


def get_user_credential_parser():	
	_user_parser = reqparse.RequestParser()
	_user_parser.add_argument('username', type=str, required=True, help="Please provide the username")
	_user_parser.add_argument('password', type=str, required=True, help="Please provide the password.")

	return _user_parser


def get_family_request_parser():	
	_family_parser = reqparse.RequestParser()
	_family_parser.add_argument('family_name', type=str, required=True, help="Please provide the family name.")

	return _family_parser

def get_parentchild_request_parser():	
	_pc_parser = reqparse.RequestParser()
	_pc_parser.add_argument('parent_id', type=str, required=True, help="Please provide the parent_id.")
	_pc_parser.add_argument('child_id', type=str, required=True, help="Please provide the child id.")

	return _pc_parser


def get_member_request_parser():
	_member_parser = reqparse.RequestParser()
	_member_parser.add_argument('family_id', type=str, required=True, help="Please provide the family id.")
	_member_parser.add_argument('first_name', type=str, required=True, help="Please provide the first name.")
	_member_parser.add_argument('last_name', type=str, required=True, help="Please provide the last name.")
	_member_parser.add_argument('birth_date', type=str, required=True, help="Please provide the birth date.")

	return _member_parser