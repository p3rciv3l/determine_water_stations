import gpxpy
import geopy.distance

class GPXRoute:
    def __init__(self, gpx_data):
        self.gpx_data = gpx_data
        self.coordinates = self.get_coordinates()
        self.total_distance = self.calculate_total_distance()

    def get_coordinates(self):
        points = []
        for track in self.gpx_data.tracks:
            for segment in track.segments:
                for point in segment.points:
                    points.append((point.latitude, point.longitude))
        return points
    
    def calculate_total_distance(self):
        total_distance = 0.0
        for i in range(1, len(self.coordinates)):
            total_distance += geopy.distance.geodesic(self.coordinates[i-1], self.coordinates[i]).miles
        return total_distance

    def get_coordinate_at_mile(self, mile):
        if mile < 0 or mile > self.total_distance:
            return "Error: Mile point out of bounds."
        
        accumulated_distance = 0.0
        for i in range(1, len(self.coordinates)):
            segment_distance = geopy.distance.geodesic(self.coordinates[i-1], self.coordinates[i]).miles
            if accumulated_distance + segment_distance >= mile:
                ratio = (mile - accumulated_distance) / segment_distance
                lat = self.coordinates[i-1][0] + ratio * (self.coordinates[i][0] - self.coordinates[i-1][0])
                lon = self.coordinates[i-1][1] + ratio * (self.coordinates[i][1] - self.coordinates[i-1][1])
                return (lat, lon)
            accumulated_distance += segment_distance
        return "Error: Mile point exceeds route distance."
