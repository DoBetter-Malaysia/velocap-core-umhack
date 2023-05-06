from dotenv import load_dotenv

load_dotenv()

from models.setup import setup_models
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS, cross_origin
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.startup import Startup
from models.founder import Founder
from models.news import News
from queries.heuristics import query
from knn.knn_distance_recommender import get_similar_companies


engine = setup_models()

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/startups", methods=["POST"])
@cross_origin()
def startups():
    with engine.connect() as conn:
        result = conn.execute(text(query(request.json)))
        return [r._asdict() for r in result.all()]


@app.route("/startups/<id>")
@cross_origin()
def startup(id):
    session = Session(engine)
    stmt = select(Startup).where(Startup.id == id)
    return jsonify(session.scalars(stmt).first())

@app.route("/recommend/<id>")
@cross_origin()
def recommend(id):
    session = Session(engine)
    stmt = select(Startup).where(Startup.id == id)
    data = session.scalars(stmt).first().__dict__
    predictions=get_similar_companies(data)
    return jsonify(predictions)

@app.route("/news/<company_id>")
@cross_origin()
def news(company_id):
    with Session(engine) as session:
        stmt = (
            select(News)
            .where(News.company_id == company_id)
            .order_by(News.date_posted.desc())
            .limit(3)
        )
        return jsonify(session.scalars(stmt).all())
