"""
    Interactive Airport reports
"""

import climenu
import prompt

from report.airport import ReportContext
from report.pandas.airport import PandasAirportReports
from report.rxpy.airport import RxPyAirportReports

pandasImpl = PandasAirportReports()
rxpyImpl = RxPyAirportReports()


@climenu.menu()
def report_airports_for_state():
    """List airports for a specific state"""
    context = ReportContext()
    context.state = prompt.string("State abbreviation: ").upper()

    print("\nIATA\tAirport Name\t\t\t\t\tCity")
    print("-" * 77)

    #get_impl().report_airports_for_state(context)
    rxpyImpl.report_airports_for_state(context)


@climenu.menu()
def report_airports_near_location():
    """List airports near specified geolocation"""
    context = ReportContext()
    context.location = (prompt.real("Latitude: "), prompt.real("Longitude: "))
    context.distance = prompt.integer("Distance (in miles): ")

    print("IATA\tAirport Name\t\t\t\t\tState\tCity\t\t\t\tDistance")
    print("-" * 105)

    #get_impl().report_airports_near_location(context)
    rxpyImpl.report_airports_near_location(context)


@climenu.menu()
def report_airport_metrics():
    """List metrics for all airports"""
    context = ReportContext()
    context.year = prompt.integer("Year: ")

    print("IATA\tAirport Name\t\t\t\t    Total\tCancelled %\tDiverted %")
    print("-" * 91)

    #get_impl().report_airport_metrics(context)
    rxpyImpl.report_airport_metrics(context)


@climenu.menu()
def report_airports_with_highest_cancellation_rate():
    """List airports with highest cancellation rates"""
    context = ReportContext()
    context.year = prompt.integer("Year: ")
    context.limit = prompt.integer("Limit: ")

    print("IATA\tAirport Name\t\t\t\tCancelled %")
    print("-" * 60)

    #get_impl().report_airports_with_highest_cancellation_rate(context)
    rxpyImpl.report_airports_with_highest_cancellation_rate(context)


def get_impl():
    return pandasImpl

if __name__ == "__main__":
    climenu.settings.clear_screen = False
    climenu.run()
