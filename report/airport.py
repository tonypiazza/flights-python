"""
    Functions and classes used by implementations of Airport reports.
"""

from geopy.distance import vincenty
from repository import Repository
from report.metrics import FlightBasedMetrics


class AirportReports(object):
    """Definitions for airport-related reports"""

    def report_airports_for_state(self, ctx):
        raise NotImplementedError

    def report_airports_near_location(self, ctx):
        raise NotImplementedError

    def report_airport_metrics(self, ctx):
        raise NotImplementedError

    def report_airports_with_highest_cancellation_rate(self, ctx):
        raise NotImplementedError

    def distance(self, location1, location2, units='miles'):
        return vincenty(location1, location2).__getattribute__(units)


class AirportMetrics(FlightBasedMetrics):
    """Airport-related metrics based on flight data"""
    def __init__(self, subject):
        super().__init__(subject)
        self.totalCancelledCarrier = 0
        self.totalCancelledWeather = 0
        self.totalCancelledNAS = 0
        self.totalCancelledSecurity = 0
        self.totalOrigins = 0
        self.totalDestinations = 0

    def add_flight(self, flight):
        """Aggregate various metrics based on the specified flight"""
        self.totalFlights += 1
        if flight.Origin == self.subject.iata:
            self.totalOrigins += 1
            # cancellations are counted only for the origin airport
            if flight.Cancelled:
                self.totalCancelled += 1
                if flight.CancellationCode == 'A':
                    self.totalCancelledCarrier += 1
                elif flight.CancellationCode == 'B':
                    self.totalCancelledWeather += 1
                elif flight.CancellationCode == 'C':
                    self.totalCancelledNAS += 1
                elif flight.CancellationCode == 'D':
                    self.totalCancelledSecurity += 1
        elif flight.Dest == self.subject.iata:
            self.totalDestinations += 1
            # diversions are counted only for the destination airport
            if flight.Diverted:
                self.totalDiverted += 1


class ReportContext(object):
    """Simple wrapper around various properties needed during report execution"""
    def __init__(self):
        self.limit = None
        self.state = None
        self.location = None
        self.distance = None
        self.year = None
        self.repo = Repository()
