import json
from flask import jsonify, request, Response
from lib import APP, AUTH
from lib.auth import Authentication
from lib.models.mongo import Asset, Job, User
from mongoengine.errors import NotUniqueError

@APP.route('/user', methods=['GET'])
@AUTH.requires_auth
def user_api_status():

    return Response(json.dumps({'message': "user api is live"}), 200)

@APP.route('/user', methods=['POST'])
@AUTH.requires_auth
def create_user():
    try:
        new_id = User.objects.order_by("-user_id").limit(-1).first().user_id+1
    except AttributeError:
        new_id = 0

    request_dict = request.form.to_dict()
    request_dict['user_id'] = new_id
    new_user = User(**request_dict)
    try:
        new_user.save()
    except NotUniqueError:
        return Response(json.dumps({'message': "That user is already registered."}), 400)
    return Response(new_user.to_json(), 201)

@APP.route('/user/<int:user_id>', methods=['GET'])
@AUTH.requires_auth
def read_user(user_id):

    user = User.objects(user_id=user_id).first()
    if user is not None:
        return Response(user.to_json(), 200)
    else:
        return Response(json.dumps({'message': "user {} does not exist".format(user_id)}), 204)

@APP.route('/user/<int:user_id>', methods=['DELETE'])
@AUTH.requires_auth
def delete_user(user_id):
    user = User.objects(user_id=user_id).first().delete()
    return Response(json.dumps({'message':"Deleted user {}".format(user_id)}), 200)

@APP.route('/user/<int:user_id>', methods=['PUT'])
@AUTH.requires_auth
def update_user(user_id):

    request_dict = request.form.to_dict()

    user = User.objects(user_id=user_id).first()

    user.email = request_dict['email']
    user.first_name = request_dict['first_name']
    user.last_name = request_dict['last_name']
    user.password = request_dict['password']
    user.favorite_rock = request_dict['favorite_rock']
    user.yesterday_lunch = request_dict['yesterday_lunch']
    user.save()

    return Response(user.to_json(),200)

@APP.route('/users', methods=['GET'])
@AUTH.requires_auth
def all_users():

    users = User.objects()
    return Response(users.to_json(),200)
