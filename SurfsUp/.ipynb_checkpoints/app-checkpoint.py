# Import the dependencies.
import os
os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"]="1"
from sqlalchemy import create_engine

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all the available routes."""
    return(
        f"Welcome to the SQL-Alchemy APP API!<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format: yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format: yyyy-mm-dd]/[end_date format: yyyy-mm-dd]<br/>"

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation data"""
    # Query all precipitation
    results = session.query(Measurement.date, Measure.prcp).\
    filter(Measurement.date >= "2016-08-23").\
    all()

    session.close()

    # Convert the list to dictionary
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp

        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations from the dataset"""
    # Query all stations
    results = session.query(Station.station).\
                order_by(Station.station).all()

    session.close()

    # Convert list of tuples into a normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create a session (link) from Python to the DB
    session = Session(engine)

    """Return a list of tobs"""
    # Query all tobs
    results = session.query(Measurement.date, Measurement.tobs, Measurement.prcp).\
                filter(Measurement.date >= "2016-08-23").\
                filter(Measurement.station== "USC00519281").\
                order_by(Measurement.date).all()

    session.close()

    # Convert list of tobs to a Dictionary
    all_tobs = []
    for date, tobs, prcp in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_dict["prcp"] = prcp

        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def Start_date(start_date):
    # Create a session (link) from Python to the DB
    session = Session(engine)

    """Return min, avg and max tobs for specific start date"""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.\
                        max(Measurement.tobs)).filter(Measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to list
    start_date_tobs = []
    for min, avg, and max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min"] = min
        start_date_tobs_dict["avg"] = avg
        start_date_tobs_dict["max"] = max
        start_date_tobs.append(start_date_tobs_dict)
    return jsonify(start_date_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_and_end_date(start_date, end_date):
    # Create a session (link) from Python to the DB
    session = Session(engine)

    """Return a list of min, avg, max tobs for start and end dates"""

    # Query all tobs
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.\
                            max(Measurement.tobs)).filter(Measurement.date >= start_date).\
                            filter(Measurement.date <= end_date).all()

    session.close()

    #Create a dictionary from the row data and append to list
    start_end_tobs = []
    for min, avg, and max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min"] = min
        start_end_tobs_dict["avg"] = avg
        start_end_tobs_dict["max"] = max
        start_end_tobs.append(start_end_tobs_dict)
    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=True)    