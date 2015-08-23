#TODO(jonathangsc): Add flight leg.

class FlightLeg:
  def __init__(self, flight_leg_dict):
    """Constructor of the class.

    Args:
      flight_leg_class: Dict with the content of qpxexpress#sliceInfo.
    """
    self.duration_ = flight_leg_dict["duration"]
    found = False
    for segment in flight_leg_dict["segment"]:
      if found:
        break
      self.flight_code_ = "%s/%s" % (
          segment["flight"]["carrier"], segment["flight"]["number"])
      for leg in segment["leg"]:
        if found:
          break
        self.origin_ = leg["origin"]
        self.destination_ = leg["destination"]
        self.arrival_time_ = leg["arrivalTime"]
        self.departure_time_ = leg["departureTime"]
        found = True

  def GetDuration(self):
    return self.duration_

  def GetFlightCode(self):
    return self.flight_code_

  def GetOrigin(self):
    return self.origin_

  def GetDestination(self):
    return self.destination_

  def GetArrivalTime(self):
    return self.arrival_time_

  def GetDepartureTime(self):
    return self.departure_time_

  def ToString(self):
    result = '  FLIGHT LEG:\n'
    result += '    %s-%s\n' % (self.GetOrigin(), self.GetDestination())
    result += '    Flight Code: %s\n' % self.GetFlightCode()
    result += '    Duration: %s\n' % self.GetDuration()
    result += '    Departure Time: %s\n' % self.GetDepartureTime()
    result += '    Arrival Time: %s\n' % self.GetArrivalTime()
    return result

  def Print(self):
    print self.ToString()

class Flight:
  """Simple class that models the data that should be contained by a flight."""
  def __init__(self, flight_dict):
    """Constructor of the class.

    Args:
      flight_dict: With the json dict from a qpxexpress#tripOption with no stops.
    """
    if len(flight_dict["saleTotal"]) > 3:
      self.price_ = float(flight_dict["saleTotal"][3:])
      self.currency_ = flight_dict["saleTotal"][0:3]
    else:
      self.price_ = -1
      self.currency_ = "EUR" 
    flight_legs = []
    for slice in flight_dict["slice"]:
      flight_leg = FlightLeg(slice)
      flight_legs.append(flight_leg)
    self.flight_legs_ = flight_legs
      
  def GetPrice(self):
    return self.price_
      
  def GetCurrency(self):
    return self.currency_

  def GetFlightLegs(self):
    return self.flight_legs_
