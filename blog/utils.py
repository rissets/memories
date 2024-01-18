import math
import random
import re
import string

from django.utils import html
from django.utils.html import strip_tags

from sklearn import metrics
import numpy as np

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text as text 


def count_words(html_string):
    word_string = strip_tags(html_string)
    matching_words = re.findall(r'\w+', word_string)
    count = len(matching_words)
    return count


def read_time(html_string):
    count = count_words(html_string)
    read_time_min = math.ceil(count / 200.0)  # assuming 200wpm reading
    return int(read_time_min)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def user_directory_path(instance, filename):
    return "posts/{0}/{1}".format(instance.pub_date.strftime('%m-%d-%Y'), filename)





# def get_bert_embeddings(text):
#     preprocessor, encoder = load_models()
#     print(preprocessor)
#     text_input = tf.constant([text])
#     print(text_input)
#     encoder_inputs = preprocessor(text_input)
#     outputs = encoder(encoder_inputs)
#     print(outputs['pooled_output'])
#     embedding_model = tf.keras.Model(encoder_inputs, outputs['pooled_output'])
#     return embedding_model.predict(text_input)
#
# def calculate_similarity(encoding1, encoding2):
#     return metrics.pairwise.cosine_similarity(encoding1, encoding2)[0][0]

def get_bert_embeddings(text):
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string)
    preprocessor = hub.KerasLayer("https://kaggle.com/models/tensorflow/bert/frameworks/TensorFlow2/variations/en-uncased-preprocess/versions/3")
    encoder_inputs = preprocessor(text_input)
    encoder = hub.KerasLayer("https://www.kaggle.com/models/tensorflow/bert/frameworks/TensorFlow2/variations/bert-en-uncased-l-10-h-128-a-2/versions/2", trainable=True)
    outputs = encoder(encoder_inputs)
    embedding_model = tf.keras.Model(text_input, outputs['pooled_output'])
    embedding_model.compile(optimizer='adam', loss='mse')
    sentences = tf.constant([text])
    emb = embedding_model(sentences).numpy()
    print(emb)
    return emb


def preprocess_text(text):
    text = text.lower()
    text = re.sub('[^A-Za-z0-9]+', ' ', text)
    return text


def get_similarity(query_text):
    import pandas as pd
    df = pd.read_csv("models/output_dataset.csv")
    query_text = preprocess_text(query_text)
    print(f"Query Text: {query_text}")
    query_encoding = get_bert_embeddings(query_text)

    df['encodings'] = df['encodings'].apply(lambda x: np.fromstring(x.strip('[]'), sep=' '))
    df['similarity_score'] = df['encodings'].apply(lambda x: metrics.pairwise.cosine_similarity(x.reshape(1, -1), query_encoding.reshape(1, -1))[0][0])
    df_results = df.sort_values(by=['similarity_score'], ascending=False)

    return list(df_results['id'][0:10])
#
#
# def get_recommendations(text, encoding):

    # encodings = encoding.apply(lambda x: np.fromstring(x.strip('[]'), sep=' '))
    # query_text = preprocess_text(text)
    # query_encoding = get_bert_embeddings(query_text)
    # df['similarity_score'] = df['encodings'].apply(
    #     lambda x: metrics.pairwise.cosine_similarity(x.reshape(1, -1), query_encoding.reshape(1, -1))[0][0])
    # df_results = df.sort_values(by=['similarity_score'], ascending=False)
    # return df_results

