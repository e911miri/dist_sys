import datetime
import requests
import time
TINEYE_URL = 'http://joshuacook.webscript.io/tineye'

from lib.models.mongo import Asset, Job, User
from mongoengine import NotUniqueError, register_connection
from os import environ
from redis import StrictRedis
from rq import Queue

REDIS = StrictRedis(host='redis')
Q = Queue(connection=REDIS)
register_connection('default',
                    'onregistry',
                    environ['MONGO_PORT_27017_TCP_ADDR'],
                    27017)

def heartbeat():
    # TODO: query fe database

    # TODO: new_assets = result from fe query

    # TODO: for asset in new_assets:

    asset_from_query = {
                        'filename' : 'my_image.png',
                        'key' : 's3://box.com',
                        'user' : 'me@joshuacook.me',
                        'asset_id' : int(time.time())
                        }

    asset_from_query['status'] = 'received'
    asset_from_query['asset_type'] = 'image'

    new_asset = Asset(**asset_from_query)
    try:
        new_asset.save()
    except NotUniqueError:
        pass

    Q.enqueue(tineye_search, new_asset.asset_id)

    time.sleep(10)
    Q.enqueue(heartbeat)
    return "bump bump"

def tineye_search(asset_id):
    this_asset = Asset.objects(asset_id=asset_id).first()

    resp = requests.post(TINEYE_URL)

    this_job_dict = resp.json()
    this_job_dict['asset'] = this_asset
    this_job_dict['job_type'] = 'tineye search'
    this_job = Job(**this_job_dict)
    this_job.save()

    this_asset.last_search = datetime.datetime.now()

    # TODO: different behavior based upon results of search

    if this_job.total_results > 0:


        Q.enqueue(search_internet_archive)
        this_asset.status = 'matched'
        for match in this_job_dict['results']['matches']:
            for backlink in match['backlinks']:
                Q.enqueue(take_snapshot_of_site,
                          asset_id,
                          backlink['url'],
                          backlink['backlink'],
                          backlink['crawl_date'])
                Q.enqueue(search_internet_archive,
                          asset_id,
                          backlink['url'],
                          backlink['backlink'],
                          backlink['crawl_date'])
    else:
        this_asset.status = 'no match'

    this_asset.save()

    return "Search Completed."

def take_snapshot_of_site(asset_id, url, image_url):
    this_asset = Asset.objects(asset_id=asset_id).first()

    this_job_dict = {}
    this_job_dict['stats'] = {'timestamp' : datetime.datetime.now()}
    this_job_dict['asset'] = this_asset
    this_job_dict['job_type'] = 'snapshot of site'
    this_job = Job(**this_job_dict)
    this_job.save()

    return "Search Completed."

def search_internet_archive(asset_id, url, image_url):
    this_asset = Asset.objects(asset_id=asset_id).first()

    this_job_dict = {}
    this_job_dict['stats'] = {'timestamp' : datetime.datetime.now()}
    this_job_dict['asset'] = this_asset
    this_job_dict['job_type'] = 'internet archive search'
    this_job = Job(**this_job_dict)
    this_job.save()    

    return "Search Completed."
