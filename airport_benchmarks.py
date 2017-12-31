"""
    Benchmark performance of airport reports.
"""

from report.airport import ReportContext
from report.pandas.airport import PandasAirportReports
from report.rxpy.airport import RxPyAirportReports


HOUSTON = (29.7604270, -95.3698030)
PANDAS_IMPL = PandasAirportReports()
RXPY_IMPL = RxPyAirportReports()


def test_pandas_airports_for_state(benchmark):
    context = ReportContext()
    context.state = 2008
    benchmark(PANDAS_IMPL.report_airports_for_state, context)


def test_rxpy_airports_for_state(benchmark):
    context = ReportContext()
    context.state = 2008
    benchmark(RXPY_IMPL.report_airports_for_state, context)


def test_pandas_airports_near_location(benchmark):
    context = ReportContext()
    context.location = HOUSTON
    context.distance = 50
    benchmark(PANDAS_IMPL.report_airports_near_location, context)


def test_rxpy_airports_near_location(benchmark):
    context = ReportContext()
    context.location = HOUSTON
    context.distance = 50
    benchmark(RXPY_IMPL.report_airports_near_location, context)


def test_pandas_airport_metrics(benchmark):
    context = ReportContext()
    context.year = 2008
    benchmark(PANDAS_IMPL.report_airport_metrics, context)


def test_rxpy_airport_metrics(benchmark):
    context = ReportContext()
    context.year = 2008
    benchmark(RXPY_IMPL.report_airport_metrics, context)


def test_pandas_airports_with_highest_cancellation_rate(benchmark):
    context = ReportContext()
    context.year = 2008
    context.limit = 10
    benchmark(PANDAS_IMPL.report_airports_with_highest_cancellation_rate, context)


def test_rxpy_airports_with_highest_cancellation_rate(benchmark):
    context = ReportContext()
    context.year = 2008
    context.limit = 10
    benchmark(RXPY_IMPL.report_airports_with_highest_cancellation_rate, context)
