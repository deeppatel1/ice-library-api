from elasticsearch.exceptions import NotFoundError
from constants import ElasticConstants

def get_details(client, video_id):
    # get requested video, document id being the video id
    
    try:
        resp = client.get(index=ElasticConstants.VODS_LIBRARY_INDEX, id=video_id)
    except NotFoundError:
        return {'message': "index or document not found"}, 404

    return resp.get("_source")