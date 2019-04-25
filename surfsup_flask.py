import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
from flask import Flask, jsonify
from sqlalchemy.orm import Session

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

inspector = inspect(engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)

#Route 1
#all available api routes
@app.route("/")  
def homepage():
	return(f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
	)

#Route 2
#query to dictionary
#date as key and prcp as value; return as JSON
@app.route("/api/v1.0/precipitation")
def precipitation():
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

	prcp_data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()

	prcp_dict = {}

	for row in prcp_data:
		prcp_dict["Date"]=row.date
		prcp_dict["Precipitation"]=row.prcp

        #all_tobs.append(all_tobs_dict)
	return jsonify(prcp_dict)


#Route 3
#get jsonified station list
@app.route("/api/v1.0/stations")
def station():

	station_data = session.query(Station.station).all()
	stn_list=list(np.ravel(station_data))

	return jsonify(stn_list)

#Route 4
#query for the dates and temperature observations from a year from the last data point.
#Return a JSON list of Temperature Observations (tobs) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
	results = session.query(Measurement.tobs).\
        filter(Measurement.date >= prev_year).all()

	result_list = list(np.ravel(results))

	return jsonify(result_list)

#Route 5
#when given start date print all stats greater than or equal to
#when given end date print stats b/w start and end date
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):

	

	if not end:
		results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
		filter(Measurement.date >= start).all()


		summary = list(np.ravel(results))

		return jsonify(summary)


	results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
		filter(Measurement.date >= start).\
		filter(Measurement.date <= end).all()


	summary = list(np.ravel(results))

	return jsonify(summary)


#Route 6

if __name__ == '__main__':
    app.run(debug=True)





















