import logging
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from .app_db import create_db
from fastapi.responses import JSONResponse
import sqlite3


log = logging.getLogger(__name__)
router = APIRouter()  # this establishes what router we are using (i.e FLASK)
df = pd.read_csv("data/cannabis_final.csv", index_col='strain_id')
#df = df.drop('Unnamed: 0', axis=1)
print(df.head())


def searchfunc(user_input, num_results=1):  # this is the function steve and jeremy will give me, used in ML training
    """Flexible function that searches for cannabis strains.
    ### Request Body
    - user_input str
    - num_results int: default 10
    ### Response
    - `strain_recommendation`: dictionary of strain recommendations
    """
    user_input = [user_input]
    nlp = English()
    #tokenizer = Tokenizer(nlp.vocab)
    tf = TfidfVectorizer(stop_words='english')
    print(df.head())
    dtm = tf.fit_transform(df['ailment_tokens'])
    dtm = pd.DataFrame(dtm.todense(), columns=tf.get_feature_names())
    nr = num_results
    nn = NearestNeighbors(n_neighbors=nr, algorithm='ball_tree')
    nn.fit(dtm)
    dtf = tf.transform(user_input)
    _, output = nn.kneighbors(dtf.todense())
    return output
    # recommendations = []
    # for n in output:
    #     for row in n:
    #         recommendations.append(row)
    # result = []
    # for i in recommendations:
    #     data = (df.loc[i, :])
    #     result.append(data)
    # #return {'strain_recommendations': result}
    # return result


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    symptoms: str


@router.post('/predict')
async def predict(item: Item):
    """
      # Make random baseline predictions for classification problem 🔮
      """

    pred = searchfunc(item.symptoms)
    print(pred)

    conn = sqlite3.connect('data/cannabis.sqlite3')
    curs = conn.cursor()

    curs.execute(f"SELECT * FROM Cannabis WHERE strain_id == {pred[0][0]}")

    strain = curs.fetchall()

    keys = ['ID', 'Name', 'Rating', 'Type', 'Ailments', 'Positive_Effects', 'Negative_Effects', 'Description', 'Effects', 'Flavors', 'Strain_ID']
    suggestion = {k: v for k, v in zip(keys, strain[0])}
    # for key in ['Ailments', 'Positive_Effects', 'Negative_Effects', 'Effects', 'Flavors']:
    #     suggestion[key] = suggestion[key].split(',')

    return JSONResponse(suggestion)



@router.get('/createDB')
async def make_db():
    create_db()
    return "Database Created!"
