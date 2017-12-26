"""
    Interactive Airport reports
"""

import climenu
import prompt

from report.airport import ReportContext
from report.pandas.airport import PandasAirportReports
from report.rxpy.airport import RxPyAirportReports
from report.implementation import ImplementationType, ImplementationSelector


impl = ImplementationSelector(
    (ImplementationType.Pandas, PandasAirportReports()),
    (ImplementationType.RxPY, RxPyAirportReports())
)


@climenu.group(title=impl.get_implementation_group_title,
               items_getter=impl.get_implementation_menu_items)
def implementation_group():
    """Implementations"""
    pass


@climenu.group(subtitle=impl.get_report_group_subtitle)
def airport_report_group():
    """Airport Reports"""
    pass


@airport_report_group.menu()
def report_airports_for_state():
    """List airports for a specific state"""
    context = ReportContext()
    context.state = prompt.string("State abbreviation: ").upper()

    print("\nIATA\tAirport Name\t\t\t\t\tCity")
    print("-" * 77)

    impl().report_airports_for_state(context)


@airport_report_group.menu()
def report_airports_near_location():
    """List airports near specified geolocation"""
    context = ReportContext()
    context.location = (prompt.real("Latitude: "), prompt.real("Longitude: "))
    context.distance = prompt.integer("Distance (in miles): ")

    print("IATA\tAirport Name\t\t\t\t\tState\tCity\t\t\t\tDistance")
    print("-" * 105)

    impl().report_airports_near_location(context)


@airport_report_group.menu()
def report_airport_metrics():
    """List metrics for all airports"""
    context = ReportContext()
    context.year = prompt.integer("Year: ")

    print("IATA\tAirport Name\t\t\t\t    Total\tCancelled %\tDiverted %")
    print("-" * 91)

    impl().report_airport_metrics(context)


@airport_report_group.menu()
def report_airports_with_highest_cancellation_rate():
    """List airports with highest cancellation rates"""
    context = ReportContext()
    context.year = prompt.integer("Year: ")
    context.limit = prompt.integer("Limit: ")

    print("IATA\tAirport Name\t\t\t\tCancelled %")
    print("-" * 60)

    impl().report_airports_with_highest_cancellation_rate(context)
