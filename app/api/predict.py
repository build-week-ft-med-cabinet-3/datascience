import logging
import random
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import spacy
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
import sqlite3
from .app_db import create_db


log = logging.getLogger(__name__)
router = APIRouter()  # this establishes what router we are using (i.e FLASK)
df = pd.read_csv("data/cannabis_final.csv")


def searchfunc(user_input, num_results=10):  # this is the function steve and jeremy will give me, used in ML training
    """Flexible function that searches for cannabis strains.
    ### Request Body
    - user_input str
    - num_results int: default 10
    ### Response
    - `strain_recommendation`: dictionary of strain recommendations
    """
    user_input = [user_input]
    nlp = English()
    tokenizer = Tokenizer(nlp.vocab)
    tf = TfidfVectorizer(stop_words='english')
    dtm = tf.fit_transform(df['ailment_tokens'])
    dtm = pd.DataFrame(dtm.todense(), columns=tf.get_feature_names())
    nr = num_results
    nn = NearestNeighbors(n_neighbors=nr, algorithm='ball_tree')
    nn.fit(dtm)
    dtf = tf.transform(user_input)
    _, output = nn.kneighbors(dtf.todense())
    recommendations = []
    for n in output:
        for row in n:
            recommendations.append(row)
    result = []
    for i in recommendations:
        data = (df.loc[i, :])
        result.append(data)
    return {'strain_recommendations': result}


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    symptoms: str = Field(..., example='insomia')  # this takes any symptom as a string
    # can also put a field for 'effects', 'flavors', 'strain', (if they do not concatnate the strings for us)

    def to_df(self):  # this will take our symptoms and takes it as a dictionary and makes it a dataframe for the model
                      # to use
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

    # @validator('x1')
    # def x1_must_be_positive(cls, value):
    #     """Validate that x1 is a positive number."""
    #     assert value > 0, f'x1 == {value}, must be > 0'
    #     return value


@router.post('/predict')
async def predict(item: Item):
    """
      # Make random baseline predictions for classification problem 🔮
      """

    X_new = item.to_df()
    log.info(X_new)
    return {'recommendations': searchfunc(item.symptoms, num_results=5)}


@router.get('/createDB')
async def make_db():
    create_db()
    return "Database Created!"
