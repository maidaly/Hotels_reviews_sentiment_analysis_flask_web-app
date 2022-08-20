                          files-hierarchy


data----|that folder contains the hotel's reviews data
        |
        |---- 7282_1.csv
        |---- stopwords.txt


model---| Contains the model inferences.
        |
        |---- logisticLearn.model
        |---- tfidf.vector


results | Contains the data with inserting the new results into it
        |
        |---- hotels_data_with_tone_analysis.csv


routes  | Contains the code of the two microservices.
        |
        |---- ElasticSearchIndexer.py
        |---- ToneAnalyser.py

statics | Contains the staics files for the falsk app
        | ---- css
        | ---- Images


templates| Contains HTMl templates
         |
         |---- index.html
         |---- waiting.html

app.py --- run file of the flask app

utlis.py ----- file contains some helper functions

config.py ---- configuration file 

Dockerfile --- The docker file could build a docker image to run the app
               (assume that the ElasticSearch runs on localhost:9200 or you can configure the host from config.py file).

requirements.txt --- it contains the needed python libraries needed for running the app with docker.