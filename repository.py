"""
     Define functions and classes to support data access.
"""

import csv
from config import Config
from rx import Observable


class Airport(object):
    def __init__(self, iata, airport, city, state, country, lat, long):
        self.iata = iata
        self.airport = airport
        self.city = city
        self.state = state
        self.country = country
        self.lat = lat
        self.long = long
        self.distance = None


def convert_value(value):
    return value if len(value) or 'NA' != value else None


def convert_bool(value):
    return bool(int(value))


class Flight(object):
    def __init__(self, year, month, dayofmonth, dayofweek, deptime, crsdeptime,
                 arrtime, crsarrtime, uniquecarrier, flightnum, tailnum,
                 actualelapsedtime, crselapsedtime, airtime, arrdelay, depdelay,
                 origin, dest, distance, taxiin, taxiout, cancelled,
                 cancellationcode, diverted, carrierdelay, weatherdelay,
                 nasdelay, securitydelay, lateaircraftdelay):
        self.Year = year
        self.Month = month
        self.DayofMonth = dayofmonth
        self.DayOfWeek = dayofweek
        self.DepTime = convert_value(deptime)
        self.CRSDepTime = crsdeptime
        self.ArrTime = convert_value(arrtime)
        self.CRSArrTime = crsarrtime
        self.UniqueCarrier = uniquecarrier
        self.FlightNum = flightnum
        self.TailNum = convert_value(tailnum)
        self.ActualElapsedTime = convert_value(actualelapsedtime)
        self.CRSElapsedTime = convert_value(crselapsedtime)
        self.AirTime = convert_value(airtime)
        self.ArrDelay = convert_value(arrdelay)
        self.DepDelay = convert_value(depdelay)
        self.Origin = origin
        self.Dest = dest
        self.Distance = distance
        self.TaxiIn = convert_value(taxiin)
        self.TaxiOut = convert_value(taxiout)
        self.Cancelled = convert_bool(cancelled)
        self.CancellationCode = convert_value(cancellationcode)
        self.Diverted = convert_bool(diverted)
        self.CarrierDelay = convert_value(carrierdelay)
        self.WeatherDelay = convert_value(weatherdelay)
        self.NASDelay = convert_value(nasdelay)
        self.SecurityDelay = convert_value(securitydelay)
        self.LateAircraftDelay = convert_value(lateaircraftdelay)


class Repository(object):
    config = Config()

    def airports_file(self):
        return open(self.config.airportPath)

    def airports_observable(self):
        reader = csv.reader(self.airports_file())
        reader.__next__()   # skip the header
        return Observable.from_(Airport(*row) for row in reader)

    def flights_file(self, year):
        return open(self.config.flightPaths[year], buffering=10000000)

    def flights_observable(self, year):
        reader = csv.reader(self.flights_file(year))
        reader.__next__()   # skip the header
        return Observable.from_(Flight(*row) for row in reader)
