import pandas as pd
import config
from flask import render_template
import os
import nltk
import joblib
from nltk.tokenize import word_tokenize

def read_csv_data(df_dir=config.INPUT_DATA_DIR):
    '''
    reads the input CSV as DataFrame
    '''
    df = pd.read_csv('data/7282_1.csv')
    return df

def select_hotels_category(df, category="Hotels"):
   '''
   returns DataFrame that has “Hotels” value in “categories” column
   '''
   return df[df["categories"]==category]


def get_stopwords(file_dir):
    """
    Read and return all the contents of the stop-words-text-file with the given path.
    It is returned as a single string where all lines are concatenated.
    """
    stop_words = []
    with open(file_dir, 'r', encoding='utf-8') as file:
        for line in file:
            stop_words.append(line.strip())
        file.close()
    return stop_words

def tokenize(text_string):
    return word_tokenize(text_string)

def remove_punct(text):
    text  = [''.join(filter( lambda x: x in 'abcdefghijklmnopqrstuvwxyz', word.lower()))
             for word in text]
    return text

def remove_stopwords(text):
    stop_words = get_stopwords('data/stopwords.txt')
    text = [word for word in text if word not in stop_words+['br', 'film', 'movie']]
    return text


def stemming(text):
    stemm = nltk.PorterStemmer()
    text = [stemm.stem(word) for word in text]
    return text


def lemmatizer(text):
    lemm = nltk.WordNetLemmatizer()
    text = [lemm.lemmatize(word) for word in text]
    return text

def clean_text(text):
    text = tokenize(text)
    text = remove_punct(text)
    text = remove_stopwords(text)
    return ' '.join(text)

def load_model(model_dir):
    return joblib.load(model_dir)

def load_tfidf(tfidf_dir):
    return joblib.load(tfidf_dir)

def predict(text):

    model = load_model('model/logisticLearn.model')
    tfidf_vectorizer = load_tfidf('model/tfidf.vector')
    cleaned_text = clean_text(text)
    tfidf_vector = tfidf_vectorizer.transform([cleaned_text])
    prediction = model.predict_proba(tfidf_vector)

    return prediction

def save_as_csv(df, file_name):
    path = config.TONE_ANALYSER_RESULTS+file_name
    return df.to_csv(path, index=False)

def split_prediction(text):
    preds = predict(text)
    pos, neg = format(preds[0][1], ".2f"), format(preds[0][0], ".2f")
    return pos, neg

def get_reviews_predictions(hotels_df):
    hotels_df['postive_score'],  hotels_df['negative_score']= zip(*hotels_df['reviews.text'].fillna(' ').astype(str).map(split_prediction))
    return hotels_df

def aggergate_score_per_hotel(hotels_df):
    '''
    returns DataFrame object with hotel_name, normlized_pos_score and normlized_neg_score for each hotel
    '''

    hotels_groups = hotels_df.groupby(['name'])
    #    hotels_groups['reviews.title'].fillna(' ', inplace = True)
    normlized_score_per_hotel = {'hotel_name':[], 'normlized_pos_score':[], 'normlized_neg_score':[]}
    for hotel_name in hotels_groups.groups.keys():
        hotel_group = hotels_groups.get_group(hotel_name)
        normlized_pos_score =  hotel_group['postive_score'].astype(float).mean()
        normlized_neg_score =  hotel_group['negative_score'].astype(float).mean()
        normlized_score_per_hotel['hotel_name'].append(hotel_name)
        normlized_score_per_hotel['normlized_pos_score'].append(format(normlized_pos_score, '.2f'))
        normlized_score_per_hotel['normlized_neg_score'].append(format(normlized_neg_score, '.2f'))

    return pd.DataFrame(normlized_score_per_hotel)




def add_result_to_df(orginal_df, resultes_df):
    '''
    returns The final Dataframe which contained the reviews tones combined with all other information in the dataset
    '''
    hotels_names = resultes_df['hotel_name'].unique()
    orginal_df["normlized_pos_score"] = [resultes_df[resultes_df['hotel_name']==orginal_df['name'][i]]['normlized_pos_score'].values[0]
                                            if orginal_df['name'][i] in hotels_names 
                                            else pd.NA 
                                            for i in range(len(orginal_df))]

    orginal_df["normlized_neg_score"] = [resultes_df[resultes_df['hotel_name'] == orginal_df['name'][i]]['normlized_neg_score'].values[0]
        if orginal_df['name'][i] in hotels_names
        else pd.NA
        for i in range(len(orginal_df))]


    return orginal_df


