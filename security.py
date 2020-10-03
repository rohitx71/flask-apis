from werkzeug.security import safe_str_cmp
from resources.user import UserModel


def authenticate(username, password):
	user = UserModel.find_by_username(username)
	if user and safe_str_cmp(password, user.password):
		return user


def identity(payload):
	user_id = payload['identity']
	return UserModel.get_by_user_id(user_id)
