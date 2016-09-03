import base64
import json
import os
from flask import Response
from werkzeug.utils import secure_filename

from conf.settings import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from lib.models.mongo import Asset, User

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def prepare_params_for_writing_to_disk(request_dict, filename):
    asset_type = request_dict['asset_type']
    asset_params = {'asset_type' : asset_type}

    try:
        new_id = Asset.objects.order_by("-asset_id").limit(-1).first().asset_id+1
    except AttributeError:
        new_id = 0

    asset_params['status'] = 'uploaded'
    asset_params['asset_id'] = new_id
    asset_params['key'] = UPLOAD_FOLDER
    asset_params['filename'] = filename

    email = request_dict['user']

    asset_params['user'] = User.objects(email=email).first()

    return asset_params

def save_asset_to_disk(asset, filename):
    asset = asset.encode()
    with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as filehandler:
        filehandler.write(base64.decodestring(asset))

def save_asset_to_database(asset_params):
    new_asset = Asset(**asset_params)

    try:
        new_asset.save()
    except NotUniqueError:
        return Response(json.dumps({'message': "That asset is already registered."}), 400)
    return Response(new_asset.to_json(), 201)

def validate_upload_metadata(request_dict):
    if 'asset' not in request_dict:
        return Response(json.dumps({'message': "Please include a file."}), 400)

    asset = request_dict['asset']

    if 'filename' not in request_dict:
        return Response(json.dumps({'message': "Please include an appropriate filename."}), 400)
    else:
        filename = request_dict['filename']

    if not allowed_file(filename):
        return Response(json.dumps({
            'message' :
            "Please submit one of:" + str(ALLOWED_EXTENSIONS)
            }), 415)

    return asset, secure_filename(filename)
