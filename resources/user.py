from flask_restful import Resource, reqparse
from models.user_model import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
	create_access_token,
	create_refresh_token,
	jwt_refresh_token_required,
	get_jwt_identity,
	jwt_required,
	get_raw_jwt
)
from blacklist import BLACKLIST

BLANK_ERROR = "'{}' cannot be blank."
USER_NOT_FOUND = 'User not found'
USER_ALREADY_EXISTS = "A user with name '{}' already exists."
USER_CREATED = "User created successfully"
USER_DELETED = "User deleted successfully"
INSERTION_ERROR = "An error occurred inserting the item."
SUCCESSFULLY_LOGGED_OUT = "Successfully logged out"
INVALID_CREDENTIALS = "Invalid credentials"

_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username", type=str, required=True, help=BLANK_ERROR.format("username"))
_user_parser.add_argument("password", type=str, required=True, help=BLANK_ERROR.format("password"))


class UserRegister(Resource):

	@classmethod
	def post(cls):
		data = _user_parser.parse_args()
		user = UserModel.find_by_username(data["username"])
		if user:
			return {"message": USER_ALREADY_EXISTS.format(data["username"])}, 400
		UserModel(**data).save_to_db()
		return {"message": USER_CREATED}, 201


class User(Resource):

	@classmethod
	def get(cls, user_id: int):
		user = UserModel.find_by_id(user_id)
		if not user:
			return {"message": USER_NOT_FOUND}, 400
		return user.json()

	@classmethod
	def delete(cls, user_id: int):
		user = UserModel.find_by_id(user_id)
		if not user:
			return {"message": USER_NOT_FOUND}, 400
		user.delete_from_db()
		return {"message": USER_DELETED}


class UserLogin(Resource):

	@classmethod
	def post(cls):
		data = _user_parser.parse_args()
		user = UserModel.find_by_username(data['username'])
		if user and safe_str_cmp(user.password, data['password']):
			access_token = create_access_token(identity=user.id, fresh=True)
			refresh_token = create_refresh_token(user.id)
			return {
				'access_token': access_token,
				'refresh_token': refresh_token
			}

		return {"message": INVALID_CREDENTIALS}, 401


class UserLogout(Resource):

	@classmethod
	@jwt_required
	def post(cls):
		jti = get_raw_jwt()['jti']  # JWT ID
		BLACKLIST.add(jti)
		return {"message": SUCCESSFULLY_LOGGED_OUT}, 200


class TokenRefresh(Resource):

	@classmethod
	@jwt_refresh_token_required
	def post(cls):
		current_user = get_jwt_identity()
		new_token = create_access_token(identity=current_user, fresh=False)
		return {'access_token': new_token}
