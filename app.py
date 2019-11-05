import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from dateutil.parser import parse

from flask import Flask, jsonify
import pandas as pd
import numpy as np
import datetime as dt

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
   
    return (
        f"Available API Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

##########################################################    

#Convert the query results to a Dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")

def query1():

    last_data_point = session.query(func.max(Measurement.date)).scalar()
    last_date = dt.datetime.strptime(last_data_point, '%Y-%m-%d')
    last_date_year = last_date - dt.timedelta(days=365)
    percip_data = session.query(Measurement.date , Measurement.prcp).filter(Measurement.date > last_date_year).order_by(Measurement.date).all()
    percip_df = pd.DataFrame(percip_data)
    perp = percip_df.to_dict()
            
    return(jsonify(perp))

@app.route("/api/v1.0/stations")

def query2():

    stations = session.query(Station).count() 

    return(jsonify(stations))


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")

def calc_temps(start, end):

    temperature = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    #print(temperature)
    return(jsonify(temperature))

if __name__ == '__main__':
    app.run(debug=True)