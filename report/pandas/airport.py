"""
    Pandas implementation of Airport reports
"""

import pandas as pd
from collections import OrderedDict
from geopy.distance import vincenty
from report.airport import AirportReports, AirportMetrics


class PandasAirportReports(AirportReports):
    def report_airports_for_state(self, ctx):
        airports = pd.read_csv(ctx.repo.airports_file())
        result = airports[airports.state == ctx.state].sort_values(by='iata')

        for row in result.itertuples():
            print("{0:3}\t{1:<40}\t{2:<20}".format(
                row.iata,
                row.airport,
                row.city)
            )

    def report_airports_near_location(self, ctx):
        airports = pd.read_csv(ctx.repo.airports_file())
        distance = []
        for airport in airports.itertuples():
            distance.append(vincenty((airport.lat, airport.long),
                                     ctx.location).miles)
        airports['distance'] = distance
        result = airports[airports.distance < ctx.distance].sort_values(by='distance')

        for row in result.itertuples():
            print("{0:3}\t{1:<40}\t {2:2}\t{3:<25}\t{4:4.0f}".format(
                row.iata,
                row.airport[:40],
                row.state,
                row.city[:25],
                row.distance)
            )

    def report_airport_metrics(self, ctx):
        repo = ctx.repo
        airports = pd.read_csv(repo.airports_file())
        flights = pd.read_csv(repo.flights_file(ctx.year))
        metrics = self.generate_metrics(flights.itertuples(), airports)
        result = OrderedDict(sorted(metrics.items(),
                                    key=lambda a: a[1].totalFlights,
                                    reverse=True))

        for iata, m in result.items():
            print("{0:3}\t{1:<35}\t{2:>9,d}\t{3:>6.1f}\t\t{4:>6.1f}".format(
                iata,
                m.subject.airport[:35],
                m.totalFlights,
                m.cancellation_rate() * 100.0,
                m.diversion_rate() * 100.0)
            )

    def report_airports_with_highest_cancellation_rate(self, ctx):
        repo = ctx.repo
        airports = pd.read_csv(repo.airports_file())
        flights = pd.read_csv(repo.flights_file(ctx.year))
        metrics = self.generate_metrics(flights.itertuples(), airports)
        result = OrderedDict(sorted(metrics.items(),
                                    key=lambda a: a[1].cancellation_rate(),
                                    reverse=True))

        count = 0
        for iata, m in result.items():
            count += 1
            if count > ctx.limit:
                break
            print("{0:3}\t{1:<35}\t{2:>6.1f}".format(
                iata,
                m.subject.airport[:35],
                m.cancellation_rate() * 100.0)
            )

    def generate_metrics(self, flights_iter, airports):
        metrics = {}
        for row in flights_iter:
            orig = row.Origin
            m1 = metrics.get(orig)
            if m1 is None:
                m1 = self.create_metrics(airports, orig)
                metrics[orig] = m1
            m1.add_flight(row)
            dest = row.Dest
            m2 = metrics.get(dest)
            if m2 is None:
                m2 = self.create_metrics(airports, dest)
                metrics[dest] = m2
            m2.add_flight(row)
        return metrics

    def create_metrics(self, airports, iata):
        for row in airports.loc[airports.iata == iata].itertuples():
            return AirportMetrics(row)
        else:
            raise KeyError("No airport found for " + iata)
