"""
    Base metrics class for use in report modules.
"""


class FlightBasedMetrics(object):
    """Common metrics useful across various domain types"""
    def __init__(self, subject):
        self.totalFlights = 0
        self.totalCancelled = 0
        self.totalDiverted = 0
        self.subject = subject

    def cancellation_rate(self):
        return self.totalCancelled / self.totalFlights

    def diversion_rate(self):
        return self.totalDiverted / self.totalFlights
