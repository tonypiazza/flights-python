"""
     Provides access to application data
"""

import csv
from collections import namedtuple
from config import Config
from rx import Observable


Airport = namedtuple("Airport", ["iata", "airport", "city", "state", "country",
                                 "lat", "long"])

Flight = namedtuple("Flight", ["Year", "Month", "DayofMonth", "DayOfWeek",
                               "DepTime", "CRSDepTime", "ArrTime",
                               "CRSArrTime", "UniqueCarrier", "FlightNum",
                               "TailNum", "ActualElapsedTime", "CRSElapsedTime",
                               "AirTime", "ArrDelay", "DepDelay", "Origin",
                               "Dest", "Distance", "TaxiIn", "TaxiOut",
                               "Cancelled", "CancellationCode", "Diverted",
                               "CarrierDelay", "WeatherDelay", "NASDelay",
                               "SecurityDelay", "LateAircraftDelay"])


class Repository(object):
    config = Config()

    def airports_file(self):
        return open(self.config.airportPath)

    def airports_observable(self):
        reader = csv.reader(self.airports_file())
        reader.__next__()   # skip the header
        return Observable.from_(Airport._make(row) for row in reader)

    def flights_file(self, year):
        return open(self.config.flightPaths[year], buffering=10000000)

    def flights_observable(self, year):
        reader = csv.reader(self.flights_file(year))
        reader.__next__()   # skip the header
        return Observable.from_(Flight._make(row) for row in reader)
