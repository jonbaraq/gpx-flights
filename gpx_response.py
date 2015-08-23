import json
import logging

from model import Flight

class GpxResponse:
  """GpxRespone wrapper generated from a json data."""

  def __init__(self, json_response):
    """Constructor of the class.

    Args:
      json_response: response that contains the GPX flight options.
    """
    # Raw dictionary returned on the response.
    self.json_data_ = json.loads(json_response)
    self.flight_list_ = self._ParseFlights(self.json_data_)

  def _ParseFlights(self, json_data):
    """Parses the JSON data extracting the resulting flights from it.

    Args:
      json_data: Dictionary with the json_data.
    """
    flights = []
    for trip_option in json_data["trips"]["tripOption"]:
      flight = Flight(trip_option)
      flights.append(flight)
    return flights

  def Print(self):
    """Prints the dictionary containing the response."""
    print self.json_data_

  def GetFlights(self):
    """Returns the flights contained in the response."""
    return self.flight_list_
