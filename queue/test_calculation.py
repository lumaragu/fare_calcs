import unittest
from unittest.mock import patch
from calculation import haversine, filter_data, timestamp_validation, calculate_segment_fare


class TestCalculation(unittest.TestCase):

    def test_haversine(self):
        lon1 = -103.548851
        lat1 = 32.0004311
        lon2 = -103.6041946
        lat2 = 33.374939
        distance = round(haversine(lat1, lon1, lat2, lon2), 2)
        assert distance == 152.93

    def test_filter(self):
        data = [
            [9,37.953066,23.735606,1405587697],
            [9,37.953009,23.735593,1405587707],
            [9,37.953195,23.736224,1405587717],
            [9,37.953433,23.736926,1405587727],
            [9,37.953450,23.737670,1405587738],
        ]
        data_filtered = filter_data(data)
        assert len(data_filtered) == 4

    def test_timestamp_validation(self):
        validation = timestamp_validation(1405587738)
        assert validation is False

    def test_segment_fare(self):
        segment_fare = calculate_segment_fare(
            [9,37.953433,23.736926,1405587727],
            [9,37.953450,23.737670,1405587738]
        )
        segment_fare = round(segment_fare, 3)
        assert segment_fare == 0.085
