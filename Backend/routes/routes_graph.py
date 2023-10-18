from flask import Blueprint, jsonify, request
from __init__ import db
from sqlalchemy import exc
from models.ratings import Rating
from datetime import datetime,timedelta

graph_bp = Blueprint("graph", __name__)

@graph_bp.route("/graph",methods =["GET"])
def get_graph_data():
  subject_id = request.args.get("subject_id")
  start_date = datetime(datetime.now().year, 10, 1) 
  end_date = start_date + timedelta(weeks=14) 

  results = (
      db.session.query(Rating).filter_by(subject_id = subject_id)
      .filter(Rating.datetime >= start_date, Rating.datetime < end_date)
      .all()
  )

  weekly_ratings = {}
  for result in results:
      week_start = result.datetime - timedelta(days=result.datetime.weekday())
      if week_start not in weekly_ratings:
          weekly_ratings[week_start] = []
      weekly_ratings[week_start].append(result.rating)

  response_list = []
  for date, ratings in weekly_ratings.items():
      response_list.append({"date": date, "rating": sum(ratings) / len(ratings)})

  return response_list
