#!/usr/bin/env python

"""
    Interactive Airport reports
"""

import climenu
import prompt

from report.airport import ReportContext
from report.pandas.airport import PandasAirportReports
from report.rxpy.airport import RxPyAirportReports


class __ImplementationSwitcher(object):
    PANDAS_IMPL = PandasAirportReports()
    RXPY_IMPL = RxPyAirportReports()
    impl = None
    report_group_subtitle = None
    implementation_group_title = None

    def __init__(self):
        self.use_pandas_impl()      # default to the Pandas implementation

    def get_impl(self):
        return self.impl

    def use_pandas_impl(self):
        self.impl = self.PANDAS_IMPL
        self.set_implementation_group_title("Pandas")
        self.set_report_group_subtitle("Pandas")

    def use_rxpy_impl(self):
        self.impl = self.RXPY_IMPL
        self.set_implementation_group_title("RxPY")
        self.set_report_group_subtitle("RxPY")

    def get_implementation_group_title(self):
        return self.implementation_group_title

    def get_report_group_subtitle(self):
        return self.report_group_subtitle

    def set_implementation_group_title(self, impl_name):
        self.implementation_group_title = \
            "Implementation Menu (currently using {})".format(impl_name)

    def set_report_group_subtitle(self, impl_name):
        self.report_group_subtitle = \
            "(using {} implementation)".format(impl_name)


switcher = __ImplementationSwitcher()
impl = switcher.get_impl()


@climenu.group(subtitle=switcher.get_report_group_subtitle)
def report_group():
    """Report Menu"""
    pass


@report_group.menu()
def report_airports_for_state():
    """List airports for a specific state"""
    context = ReportContext()
    context.state = prompt.string("State abbreviation: ").upper()

    print("\nIATA\tAirport Name\t\t\t\t\tCity")
    print("-" * 77)

    impl.report_airports_for_state(context)


@report_group.menu()
def report_airports_near_location():
    """List airports near specified geolocation"""
    context = ReportContext()
    context.location = (prompt.real("Latitude: "), prompt.real("Longitude: "))
    context.distance = prompt.integer("Distance (in miles): ")

    print("IATA\tAirport Name\t\t\t\t\tState\tCity\t\t\t\tDistance")
    print("-" * 105)

    impl.report_airports_near_location(context)


@report_group.menu()
def report_airport_metrics():
    """List metrics for all airports"""
    context = ReportContext()
    context.year = prompt.integer("Year: ")

    print("IATA\tAirport Name\t\t\t\t    Total\tCancelled %\tDiverted %")
    print("-" * 91)

    impl.report_airport_metrics(context)


@report_group.menu()
def report_airports_with_highest_cancellation_rate():
    """List airports with highest cancellation rates"""
    context = ReportContext()
    context.year = prompt.integer("Year: ")
    context.limit = prompt.integer("Limit: ")

    print("IATA\tAirport Name\t\t\t\tCancelled %")
    print("-" * 60)

    impl.report_airports_with_highest_cancellation_rate(context)


@climenu.group(title=switcher.get_implementation_group_title)
def implementation_group():
    """Implementation Menu"""
    pass


@implementation_group.menu()
def pandas_impl():
    """Pandas implementation"""
    switcher.use_pandas_impl()


@implementation_group.menu()
def rxpy_impl():
    """RxPY implementation"""
    switcher.use_rxpy_impl()


if __name__ == "__main__":
    climenu.run()
