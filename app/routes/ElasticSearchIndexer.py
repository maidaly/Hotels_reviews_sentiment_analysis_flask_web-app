from flask import Blueprint
from pandas import read_csv
import config
import utlis
from elasticsearch import Elasticsearch

indexing_endpoint = Blueprint('indexing_endpoint', __name__)

def check_elasticsearch_connection(es):
    if not es.ping():
        raise ValueError("Connection failed to ElasticSearch host")

@indexing_endpoint.route("/indexing")
def index_data():
    try:
        result_df = read_csv(config.TONE_ANALYSER_RESULTS+"hotels_data_with_tone_analysis.csv")
    except:
        print("Check if the resulted file from analysis in its location")
    else:
        index_name = "hotels_data"
        es = Elasticsearch(hosts=config.ElastisSearch_HOST)
        check_elasticsearch_connection(es)
        hotels_groups = result_df.groupby('name')
        i=0
        for hotel_name in hotels_groups.groups.keys():
            hotel_data = hotels_groups.get_group(hotel_name).to_dict('records')
            doc = {'hotel_name': hotel_name, 'hotel_data': str(hotel_data)}
            if doc is not None:
                es.index(index=index_name, id=i, body=doc)
                i += 1
        return("Ended indexing")
 
