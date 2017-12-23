"""
    RxPy implementation of Airport reports
"""

from collections import namedtuple
from geopy.distance import vincenty
from report.airport import AirportReports, AirportMetrics


class RxPyAirportReports(AirportReports):

    def report_airports_for_state(self, ctx):
        ctx.repo \
           .airports_observable() \
           .filter(lambda airport: airport.state == ctx.state) \
           .subscribe(lambda airport:
                      print("{0:3}\t{1:<40}\t{2:<20}".format(
                            airport.iata,
                            airport.airport,
                            airport.city)
                      )
           )

    def report_airports_near_location(self, ctx):
        ctx.repo \
           .airports_observable() \
           .map(lambda airport: self.add_distance(airport, ctx.location)) \
           .filter(lambda airport: airport.distance < ctx.distance) \
           .to_sorted_list(key_selector=lambda airport: airport.distance) \
           .flat_map(lambda airports: airports) \
           .subscribe(lambda airport:
                      print("{0:3}\t{1:<40}\t {2:2}\t{3:<25}\t{4:4.0f}".format(
                            airport.iata,
                            airport.airport[:40],
                            airport.state,
                            airport.city[:25],
                            airport.distance)
                      )
           )

    def report_airport_metrics(self, ctx):
        airports = self.airports_dict(ctx.repo.airports_observable())

        ctx.repo \
           .flights_observable(ctx.year) \
           .reduce(lambda acc, f: self.accumulate(acc, airports, f), {}) \
           .flat_map(lambda metrics:
                     sorted(metrics.values(), key=lambda m: m.subject.iata)) \
           .to_blocking() \
           .for_each(lambda metric:
                     print("{0:3}\t{1:<35}\t{2:>9,d}\t{3:>6.1f}\t\t{4:>6.1f}".format(
                           metric.subject.iata,
                           metric.subject.airport[:35],
                           metric.totalFlights,
                           metric.cancellation_rate() * 100.0,
                           metric.diversion_rate() * 100.0)
                     )
           )

    def report_airports_with_highest_cancellation_rate(self, ctx):
        airports = self.airports_dict(ctx.repo.airports_observable())

        ctx.repo \
           .flights_observable(ctx.year) \
           .reduce(lambda acc, f: self.accumulate(acc, airports, f), {}) \
           .flat_map(lambda metrics:
                     sorted(metrics.values(),
                            key=lambda m: m.cancellation_rate(),
                            reverse=True)) \
           .take(ctx.limit) \
           .to_blocking() \
           .for_each(lambda metric:
                     print("{0:3}\t{1:<35}\t{2:>6.1f}".format(
                           metric.subject.iata,
                           metric.subject.airport[:35],
                           metric.cancellation_rate() * 100.0)
                     )
           )

    # extend Airport by adding distance attribute
    Airport = namedtuple("Airport", ["iata", "airport", "city", "state",
                                     "country", "lat", "long", "distance"])

    def add_distance(self, airport, location):
        values = list(airport)
        values.append(self.distance((airport.lat, airport.long), location))
        return self.Airport._make(values)

    def distance(self, location1, location2, units='miles'):
        result = vincenty(location1, location2)
        return result.__getattribute__(units)

    def airports_dict(self, obs):
        return obs.to_dict(key_selector=lambda airport: airport.iata) \
                  .to_blocking() \
                  .first()

    def accumulate(self, metrics, airports, flight):
        orig = flight.Origin
        m1 = metrics.get(orig)
        if m1 is None:
            m1 = self.create_metrics(airports, orig)
            metrics[orig] = m1
        m1.add_flight(flight)
        dest = flight.Dest
        m2 = metrics.get(dest)
        if m2 is None:
            m2 = self.create_metrics(airports, dest)
            metrics[dest] = m2
        m2.add_flight(flight)
        return metrics

    def create_metrics(self, airports, iata):
        airport = airports[iata]
        if airport is None:
            raise KeyError("No airport found for " + iata)
        else:
            return AirportMetrics(airport)
