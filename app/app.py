from elasticsearch import Elasticsearch
from flask import Flask, render_template
from routes.ToneAnalyser import tone_analysis_endpoint
from routes.ElasticSearchIndexer import indexing_endpoint

app = Flask(__name__, template_folder="templates")

app.register_blueprint(tone_analysis_endpoint)
app.register_blueprint(indexing_endpoint)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)