import datetime
import sys
import urllib2
from Queue import PriorityQueue

from email_sender import EmailSender
from gpx_configuration import GpxConfiguration
from gpx_request import GpxRequest
from gpx_response import GpxResponse


def GetCombinationsForDate(date):
  """Gets the next combinations of dates to be added.
     Thursday - Sunday
     Thursday - Monday
     Thursday - Tuesday
     Friday - Sunday
     Friday - Monday
     Friday - Tuesday

  Args:
    date: Initial date to be used.
  """
  dates = []
  # Thursday
  thursday = date
  # Friday
  friday = thursday + datetime.timedelta(days=1)
  # Sunday
  sunday = friday + datetime.timedelta(days=2)
  # Monday
  monday = sunday + datetime.timedelta(days=1)
  # Tuesday
  tuesday = monday + datetime.timedelta(days=1)
  dates.append([thursday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")])
  dates.append([friday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")])
  dates.append([thursday.strftime("%Y-%m-%d"), monday.strftime("%Y-%m-%d")])
  dates.append([friday.strftime("%Y-%m-%d"), monday.strftime("%Y-%m-%d")])
  dates.append([thursday.strftime("%Y-%m-%d"), tuesday.strftime("%Y-%m-%d")])
  dates.append([friday.strftime("%Y-%m-%d"), tuesday.strftime("%Y-%m-%d")])

  return dates


def GetDates():
  """Returns the dates to be queried."""
  # Start searching for days at least 30 days away from today.
  date = datetime.datetime.now() + datetime.timedelta(days=30)
  if date.date().weekday() > 3:
    date -= datetime.timedelta(days=date.date().weekday() + 4)
  else:
    date += datetime.timedelta(days=3 - date.date().weekday())

  dates = []
  # We just have 50 combinations.
  while len(dates) < 18:
    dates += GetCombinationsForDate(date)
    date += datetime.timedelta(days=7)
  
  return dates


if __name__ == '__main__':
  configuration = GpxConfiguration(sys.argv[1])
  url = '%s%s' % (configuration.GetApiUrl(), configuration.GetApiKey())
  dates = GetDates()
  for date in dates:
    print '%s %s' % (date[0], date[1])
  gpx_request = GpxRequest(
      configuration.GetSource(), configuration.GetDestination(), dates)

  acceptable_offers = PriorityQueue()
  index = 0
  for request in gpx_request.GetJsonRequests():
    url_req = urllib2.Request(url, request, {'Content-Type': 'application/json'})
    flight = urllib2.urlopen(url_req)
    response = GpxResponse(flight.read())
    flight.close()
    flights = response.GetFlights()
    for flight in flights:
      print 'Option #%s: Price %s %s' % (index, flight.GetPrice(), flight.GetCurrency())
      index += 1
      if flight.GetPrice() > configuration.GetThreshold():
        continue
      acceptable_offers.put([flight.GetPrice(), flight])

  if not acceptable_offers.empty():
    sender = EmailSender()
    sender.Send(configuration.GetEmail(), acceptable_offers)
