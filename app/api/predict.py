import logging
import pandas as import pd
import sqlite3

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

from .app_db import create_db
from .model import searchfunc


log = logging.getLogger(__name__)
router = APIRouter()  # this establishes what router we are using (i.e FLASK)
df = pd.read_csv("data/cannabis_final.csv", index_col='strain_id')
print(df.head())


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    symptoms: str = Field(..., example='pain')
    results: int = Field(..., example=5)


@router.post('/predict')
async def predict(item: Item):
    """
      # Make random baseline predictions for classification problem 🔮
      """

    pred = searchfunc(user_input=item.symptoms, num_results=item.results)
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
