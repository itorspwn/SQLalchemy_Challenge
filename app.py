import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start_end/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data including date as key and prcp as value """
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary precipitation results
    precip = {}
    for data in results:
        precip[data[0]] = data[1]

    # Return JSON
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Define last 12 months
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    """Return a list of tobs data including date as key and tobs as value  from last 12 months"""
    # Query all tobs
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date > query_date).all()

    session.close()

    # Create a dictionary tobs results
    tobs = {}
    for data in results:
        tobs[data[0]] = data[1]

    # Return JSON
    return jsonify(tobs)


@app.route("/api/v1.0/start/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates"""
    # Query all stations
    results = session.query(Measurement.date).all()

    session.close()

    starts_date = ""

    # Convert list of tuples into normal list
    dates = list(np.ravel(results))
    for date in dates:
        if date == str(start):
            starts_date = date

    if start_date !="":
        session = Session(engine)
        result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
            filter(Measurement.date >= query_date).all()
        session.close()

        strt = list(np.ravel(result))
        return jsonify(strt)

@app.route("/api/v1.0/start_end/<start>/<end>")
def start(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all dates"""
    # Query all stations
    results = session.query(Measurement.date).all()

    session.close()

    start_date = ""
    end_date = ""

    # Convert list of tuples into normal list
    dates = list(np.ravel(results))
    for date in dates:
        if date == str(start):
            start_date = date
        if date == str(end):
            end_date = date

    if ((start_date !="") & (end_date !="")):
        session = Session(engine)
        result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date >= end_date).all()
        session.close()

        start_end = list(np.ravel(result))
        return jsonify(start_end)



if __name__ == '__main__':
    app.run(debug=True)