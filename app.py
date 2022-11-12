import numpy as np
import re
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.sql import exists  

from flask import Flask, jsonify



engine = create_engine("sqlite:///Resources/hawaii.sqlite")


Base = automap_base()

Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
station = Base.classes.station

app = Flask(__name__)



@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)


    results = (session.query(Measurement.date, Measurement.tobs)
                      .order_by(Measurement.date))
    
    precip_date = []
    for row in results:
        dict = {}
        dict["date"] = row.date
        dict["tobs"] = row.tobs
        precip_date.append(dict)

    return jsonify(precip_date)


@app.route("/api/v1.0/stations") 
def stations():

    session = Session(engine)


    results = session.query(station.name).all()


    station_details = list(np.ravel(results))

    return jsonify(station_details)


@app.route("/api/v1.0/tobs") 
def tobs():

    session = Session(engine)


    early_date = (session.query(Measurement.date)
                          .order_by(Measurement.date
                          .desc())
                          .first())
    
    early_date_1 = str(early_date)
    early_date_1 = re.sub("'|,", "",early_date_1)
    early_date_date = dt.datetime.strptime(early_date_1, '(%Y-%m-%d)')
    start_date = dt.date(early_date_date.year, early_date_date.month, early_date_date.day) - dt.timedelta(days=366)
     

    station_list = (session.query(Measurement.station, func.count(Measurement.station))
                             .group_by(Measurement.station)
                             .order_by(func.count(Measurement.station).desc())
                             .all())
    
    station_hno = station_list[0][0]
    print(station_hno)



    results = (session.query(Measurement.station, Measurement.date, Measurement.tobs)
                      .filter(Measurement.date >= start_date)
                      .filter(Measurement.station == station_hno)
                      .all())


    tlist = []
    for result in results:
        line = {}
        line["Date"] = result[1]
        line["station"] = result[0]
        line["Temperature"] = int(result[2])
        tlist.append(line)

    return jsonify(tlist)


@app.route("/api/v1.0/<start>") 
def start_only(start):


    session = Session(engine)


    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date1 = str(latest_date)
    latest_date1 = re.sub("'|,", "",latest_date1)
    print (latest_date1)

    earliest_date = session.query(Measurement.date).first()
    earliest_date1 = str(earliest_date)
    earliest_date1 = re.sub("'|,", "",earliest_date1)
    print (earliest_date1)



    entry = session.query(exists().where(Measurement.date == start)).scalar()
 
    if entry:

    	results = (session.query(func.min(Measurement.tobs)
    				 ,func.avg(Measurement.tobs)
    				 ,func.max(Measurement.tobs))
    				 	  .filter(Measurement.date >= start).all())


   

@app.route("/api/v1.0/<start>/<end>") 
def start_end(start, end):


    session = Session(engine)


    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date1 = str(latest_date)
    latest_date1 = re.sub("'|,", "",latest_date1)
    print (latest_date1)

    earliest_date = session.query(Measurement.date).first()
    earliest_date1 = str(earliest_date)
    earliest_date1 = re.sub("'|,", "",earliest_date1)
    print (earliest_date1)


    entry_beg = session.query(exists().where(Measurement.date == start)).scalar()
 	

    entry_done = session.query(exists().where(Measurement.date == end)).scalar()

    if entry_beg and entry_done:

    	results = (session.query(func.min(Measurement.tobs)
    				 ,func.avg(Measurement.tobs)
    				 ,func.max(Measurement.tobs))
    					  .filter(Measurement.date >= start)
    				  	  .filter(Measurement.date <= end).all())

               
