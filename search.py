from array import array
from constants import ElasticConstants
import json


def search_elastic(client, query, type):

    is_clip = False
    is_vid = False
    is_vod = False

    array_types = type.split(",")

    if len(array_types) == 3:
        if array_types[0] == 'true':
            is_clip = True
        if array_types[1] == 'true':
            is_vid = True
        if array_types[2] == 'true':
            is_vod = True

    query_string = get_search_template(query, is_clip, is_vid, is_vod)

    resp = client.search(
        index=ElasticConstants.VODS_LIBRARY_INDEX, body=query_string)

    number_of_hits = resp.get('hits').get('total').get('value')
    hits = resp.get('hits').get('hits')

    for a in range(0, len(hits)):
        hits[a] = hits[a].get("_source")

    return create_response(number_of_hits, hits)


def create_response(number_of_hits, hits):
    resp_dict = {
        "count": number_of_hits,
        "videos": hits
    }

    return resp_dict


def get_search_template(query, is_clip, is_video, is_vod):

    # if clip, only get less than 2 minutes or 120
    # if video, get more than 2 mins, get less than 20 mins
    # if vod, get more than 20 mins

    # if all is true, do nothing

    # vod == gte 20*60
    # vid == gte 120, lte 60*120
    # clip == lte 120

    # vod + vid, gte 120
    # vid + clip, less than 60*120

    duration = {}

    if is_vod and is_video and is_clip:
        duration = duration
    elif is_vod and is_video:
        duration["gte"] = 60*2
    elif is_video and is_clip:
        duration["lte"] = 60*20
    elif is_vod:
        duration["gte"] = 60*20
    elif is_video:
        duration["gte"] = 60*2
        duration["lte"] = 60*120
    elif is_clip:
        duration["lte"] = 60*2

    must_clause = {
        "range": {
            "duration": duration
        }
    }

    return {
        "size": 75,
        "query": {
            "bool": {
                "should": [
                    {
                        "simple_query_string": {
                            "query": query,
                            "fields": [
                                "description",
                                "tags",
                                "title",
                                "from_channel"
                            ],
                            "default_operator": "AND",
                            "boost": 6
                        }
                    },
                    {
                        "multi_match": {
                            "query": query,
                            "fields": [
                                "description",
                                "tags",
                                "title",
                                "from_channel"
                            ],
                            "type": "best_fields",
                            "minimum_should_match": "1<25%",
                            "auto_generate_synonyms_phrase_query": True,
                            "lenient": True,
                            "operator": "OR",
                            "boost": 3
                        }
                    },
                    {
                        "multi_match": {
                            "query": query,
                            "fields": [
                                "description",
                                "tags",
                                "title",
                                "from_channel"
                            ],
                            "type": "best_fields",
                            "minimum_should_match": "1<25%",
                            "auto_generate_synonyms_phrase_query": True,
                            "lenient": True,
                            "operator": "OR",
                            "boost": 2
                        }
                    },
                    {
                        "match": {
                            "tags": {
                                "query": query,
                                "boost": 1.5
                            }
                        }
                    },
                    {
                        "match": {
                            "title": {
                                "query": query
                            }
                        }
                    },
                    {
                        "match": {
                            "title": {
                                "query": query,
                                "operator": "AND",
                                "boost": 2
                            }
                        }
                    }
                ],
                "must": must_clause
            }
        }
    }
