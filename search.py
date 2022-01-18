from constants import ElasticConstants
import json

def search_elastic(client, query):
    query_string = get_search_template(query)

    # print(json.dumps(query_string))

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


def get_search_template(query):
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
                ]
            }
        }
    }
