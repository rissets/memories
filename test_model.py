import pandas as pd
import numpy as np

from sklearn import metrics


df = pd.read_csv('models/output_dataset.csv')


#%%

df['encodings'] = df['encodings'].apply(lambda x: np.fromstring(x.strip('[]'), sep=' '))
#%%
import tensorflow as tf
import tensorflow_hub as hub

preprocessor = hub.KerasLayer("models/bert_preprocessor")
encoder = hub.KerasLayer("models/bert_encoder", trainable=True)

def get_bert_embeddings(text, preprocessor, encoder):
    text_input = tf.keras.layers.Input(shape=(), dtype=tf.string)
    encoder_inputs = preprocessor(text_input)
    outputs = encoder(encoder_inputs)
    embedding_model = tf.keras.Model(text_input, outputs['pooled_output'])
    embedding_model.compile(optimizer='adam', loss='mse')
    sentences = tf.constant([text])
    emb = embedding_model(sentences).numpy()
    print(emb)
    return emb

#%%