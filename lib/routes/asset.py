"""Assets Endpoint"""
import json
import os
from flask import jsonify, request, Response
from lib import APP, AUTH, Q, REDIS
from lib.helpers import prepare_params_for_writing_to_disk
from lib.helpers import save_asset_to_database, save_asset_to_disk
from lib.helpers import validate_upload_metadata
from lib.models.mongo import Asset, User
from mongoengine import NotUniqueError
from werkzeug.utils import secure_filename

@APP.route('/asset', methods=['GET'])
@AUTH.requires_auth
def asset_api_is_live():

    return Response(json.dumps({'message': "asset api is live"}), 200)

@APP.route('/asset', methods=['POST'])
@AUTH.requires_auth
def create_asset():

    request_dict = request.form.to_dict()

    validation = validate_upload_metadata(request_dict)
    if type(validation) == Response:
        return validation
    else:
        asset, filename = validation

    save_asset_to_disk(asset, filename)

    asset_params = prepare_params_for_writing_to_disk(request_dict, filename)

    response = save_asset_to_database(asset_params)

    return response

@APP.route('/asset/<int:asset_id>', methods=['GET'])
@AUTH.requires_auth
def read_asset(asset_id):

    asset = Asset.objects(asset_id=asset_id).first()
    if asset is not None:
        return Response(asset.to_json(), 200)
    else:
        return Response(json.dumps({'message': "asset {} does not exist".format(asset_id)}), 204)

@APP.route('/asset/<int:asset_id>', methods=['DELETE'])
@AUTH.requires_auth
def delete_asset(asset_id):

    asset = Asset.objects(asset_id=asset_id).first()
    os.remove(asset.key+'/'+secure_filename(asset.filename))
    asset.delete()
    return Response(jsonify(message="Deleted asset {}".format(asset_id)), 200)

@APP.route('/asset/<int:asset_id>', methods=['PUT'])
@AUTH.requires_auth
def update_asset(asset_id):

    request_dict = request.form.to_dict()

    email = request_dict['user']

    asset = Asset.objects(asset_id=asset_id).first()
    old_filename = asset.filename
    asset.user = User.objects(email=email).first()
    asset.filename = request_dict['filename']
    os.rename(asset.key+'/'+old_filename, asset.key+'/'+secure_filename(asset.filename))
    asset.asset_type = request_dict['asset_type']
    asset.save()

    return Response(asset.to_json(), 200)

@APP.route('/assets', methods=['GET'])
@AUTH.requires_auth
def all_assets():

    assets = Asset.objects()
    return Response(assets.to_json(), 200)
