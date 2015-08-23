import json
import logging

class GpxRequest:
  """GpxRequest wrappe8r that generates the needed json data."""

  def __init__(self, source, destination, dates):
    """Constructor of the class.

    Args:
      source: 3 letter code for the source airport.
      destination: 3 letter code for the destination airport.
      dates: List with the pairs of start - end flight to be queried.
             The format should be yyyy-MM-dd.
    """
    self.source = source
    self.destination = destination
    self.dates = dates

  def GetSource(self):
    """Returns the source airport of the request."""
    return self.source

  def GetDestination(self):
    """Returns the destination airport of the request."""
    return self.destination

  def GetJsonRequests(self):
    """Returns a list with all the json requests to be sent again the GPX servers."""
    json_requests = []
    for date_pairs in self.dates:
      if len(date_pairs) != 2:
        logging.info('Date pairs format incorrect: %s' % date_pairs)
      start_date = date_pairs[0]
      end_date = date_pairs[1]
      request = {'request': {
                   'slice': [
                     {
                       'origin': self.source,
                       'destination': self.destination,
                       'date': start_date,
                       'maxStops': 0
                     },
                     {
		       'origin': self.destination,
                       'destination': self.source,
                       'date': end_date,
                       'maxStops': 0
                     }
                   ],
                   'passengers': {
                     'adultCount': 1,
                     'infantInLapCount': 0,
                     'infantInSeatCount': 0,
                     'childCount': 0,
                     'seniorCount': 0
                   },
                   'solutions': 5,
                 }
               }
      json_request = json.dumps(request, encoding='utf-8')
      json_requests.append(json_request)
    return json_requests
