from flask_restful import reqparse, Resource

from backend.models.users import User
from backend.resources.decorators import create_if_not_exists


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="Invalid value for username"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Invalid value for password"
    )

    @create_if_not_exists
    def post(self):
        data = UserResource.parser.parse_args()
        if User.find_by_username(data['username']):
            return {'message': f"user {data['username']} already exists"}, 400
        user = User(username=data['username'], password=data['password'])
        user.add_user()
        return {'username': data['username'], 'password': data['password']}, 201

    @create_if_not_exists
    def delete(self):
        username = UserResource.parser.parse_args()['username']
        user = User.find_by_username(username)
        if not user:
            return {'message': f"user {username} doesn't exist"}, 400
        user.remove_user()
        return {}, 204
