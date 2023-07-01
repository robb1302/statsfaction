import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir.replace('scripts',''))

import pickle
import pandas as pd
import tensorflow as tf
import numpy as np
import transformers
from transformers import DistilBertTokenizer
from transformers import TFDistilBertForSequenceClassification
from src.metrics.keras import BinaryF1Score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# TODO:


MODEL_NAME = 'distilbert-base-uncased-finetuned-sst-2-english'


BATCH_SIZE = 64
N_EPOCHS = 1

# get data
df = pd.read_csv("data/myer_briggs/raw/mbti_1.csv")

df_unravelled = pd.DataFrame({
    'type': np.repeat(df['type'], df['posts'].str.count('\|\|\|') + 1),
    'text': df['posts'].str.split('\|\|\|').explode()
})

df_unravelled = df_unravelled.reset_index(drop=True)

for i in ['I','N','T','J','E','S','F','P']:
    df_unravelled[i] = [i in c for c in df_unravelled.type]

for TYPE in ['I','N','T','J','E','S','F','P']:

    df_sample = df_unravelled.sample(64)

    # 
    X = df_sample['text']
    y = df_sample[TYPE]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    # X_train = X_train.apply(lambda x: str(x[0], 'utf-8'))
    # X_test = X_test.apply(lambda x: str(x[0], 'utf-8'))


    # Define a tokenizer object
    tokenizer = DistilBertTokenizer.from_pretrained(MODEL_NAME)

    # Tokenize the text
    train_encodings = tokenizer(list(X_train.values),
                                truncation=True,
                                padding=True)
    test_encodings = tokenizer(list(X_test.values),
                            truncation=True,
                            padding=True)


    # Create TensorFlow datasets
    train_dataset = tf.data.Dataset.from_tensor_slices((dict(train_encodings),
                                                        list(y_train.values)))
    test_dataset = tf.data.Dataset.from_tensor_slices((dict(test_encodings),
                                                    list(y_test.values)))

    #get model
    model = TFDistilBertForSequenceClassification.from_pretrained(MODEL_NAME)

    #chose the optimizer
    optimizerr = tf.keras.optimizers.Adam(learning_rate=5e-5)
    #define the loss function 
    losss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)

    #build the model
    model.compile(optimizer=optimizerr,
                loss=losss,
                metrics=[BinaryF1Score()])
    # train the model 
    model.fit(train_dataset.shuffle(len(X_train)).batch(BATCH_SIZE),
            epochs=N_EPOCHS,
            batch_size=BATCH_SIZE)


    with open(f'data/myer_briggs/model/predict_{TYPE}.pkl', 'wb') as f:
        pickle.dump(model, f)


    preds = model.predict(test_dataset).logits

    # Transform to array with probabilities
    preds  = tf.nn.softmax(preds, axis=1).numpy()
    y_score = np.abs(preds[:,1])
    y_pred = y_score>0.5


    from sklearn.metrics import classification_report

    # Generate the classification report
    report = classification_report(y_test, y_pred,)
    
    np.savetxt(f"classification_report_{TYPE}.txt", [report], fmt="%s")
    print("Feature",TYPE)
    print(report)