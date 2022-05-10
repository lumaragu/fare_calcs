import csv
from datetime import datetime as dt
from math import asin, cos, radians, sin, sqrt
from typing import List


def calculate_fare() -> List:
    """
    Opens the file and calculate fares
    """   
    with open('paths.csv', 'r') as read_obj:
        csv_reader = csv.reader(read_obj)
        points = list(csv_reader)
        filtered_points = filter_data(points)
        results = calculate_total_fare(filtered_points)
    return results


def calculate_total_fare(points: List) -> List:
    """
    Calculates the fares for the different rides 
    """
    results = []
    fare = 1.30
    for i in range(len(points) - 1):
        point1 = points[i]
        point2 = points[i + 1]
        if point1[0] == point2[0]:
            segment_fare = calculate_segment_fare(point1, point2)
            fare += segment_fare
        else:
            fare = fare if fare > 3.47 else 3.47
            results.append(
                {
                    'id_ride': point1[0],
                    'fare_estimate': round(fare, 2)
                }
            )
            fare = 1.30
    write_result(results)
    return results


def calculate_segment_fare(point1: List, point2: List) -> float:
    """
    Calculate the fare for a segment
    """
    fare = 0.0
    distance = haversine(float(point1[1]), float(point1[2]), float(point2[1]), float(point2[2]))
    time = (float(point1[3]) - float(point2[3])) / 3600
    if time:
        velocity = abs(distance/time)
        if velocity <= 10:
            fare = 11.90 * abs(time)
        else:
            if timestamp_validation(int(point2[3])):
                fare = 0.74 * abs(distance)
            else:
                fare = 1.30 * abs(distance)
    return fare


def timestamp_validation(timestamp: int) -> bool:
    """
    Validates which fare applies depending on the timestamp
    """
    dt_object = dt.fromtimestamp(timestamp)
    if dt_object.hour > 0 and dt_object.hour <= 5:
        return False
    return True


def filter_data(points: List) -> List:
    """
    Filter the data removing points with velocity > 100km/h
    """
    filtered_points = []
    for i in range(len(points) - 1):
        if points[i][0] == points[i + 1][0]:
            distance = haversine(float(points[i][1]), float(points[i][2]), float(points[i + 1][1]), float(points[i + 1][2]))
            time = (float(points[i][3]) - float(points[i + 1][3])) / 3600
            if time:
                velocity = abs(distance/time)
                if velocity < 100:
                    filtered_points.append((points[i]))
    return filtered_points


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance in kilometers between two points
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371
    return c * r


def write_result(results: List) -> None:
    """
    Writes the results into a csv file
    """
    keys = results[0].keys()
    with open('results.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)


if __name__ == "__main__":
    calculate_fare()
