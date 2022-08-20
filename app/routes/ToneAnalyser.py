from flask import Blueprint, redirect, request, render_template
import config
from utlis import *


tone_analysis_endpoint = Blueprint('tone_analysis_endpoint', __name__)

def wait_for_analysis():
    return render_template("waiting.html")



@tone_analysis_endpoint.route("/tone-analysis",  methods=['GET', 'POST'])
def analyse_tone():
    if request.method == 'GET':
        return render_template('waiting.html')
    if request.method == 'POST':
        df = read_csv_data()
        selected_hotels_df = select_hotels_category(df).reset_index(drop=True)
        selected_hotels_df = selected_hotels_df.reset_index()
        selected_hotels = get_reviews_predictions(selected_hotels_df[:10])
        aggergate_score_per_hotel_data = aggergate_score_per_hotel(selected_hotels)
        final_data = add_result_to_df(selected_hotels, aggergate_score_per_hotel_data)
        save_as_csv(final_data, "hotels_data_with_tone_analysis.csv")
    return ("done")




