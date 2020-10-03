import sqlite3
from flask_restful import Resource, reqparse
from models.user_model import UserModel


class UserRegister(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument("username", type=str, required=True, help="This field cannot be left blank")
	parser.add_argument("password", type=str, required=True, help="This field cannot be left blank")

	def post(self):
		data = UserRegister.parser.parse_args()
		user = UserModel.find_by_username(data["username"])
		if user:
			return {"message": "Username already exists!"}, 400
		UserModel(**data).save_to_db()
		return {"message": "User created successfully"}, 201
