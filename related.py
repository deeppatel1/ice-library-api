from constants import ElasticConstants
from search import create_response

def process_related(client, title):
    query = {
        "size": 75,
        "query": {
            "more_like_this": {
                "fields": ["title"],
                "like": title,
                "min_term_freq": 1,
                "max_query_terms": 12
            }
        }
    }

    resp = client.search(
        index=ElasticConstants.VODS_LIBRARY_INDEX, body=query)

    return create_response(resp)
