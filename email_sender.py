import datetime
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender:
  """Class to send email notifications about flights offers."""

  def __init__(self):
    self.from_ = 'flights@jonbaraq.eu'
    date = datetime.datetime.now()
    self.subject_ = 'Flight offers on %s' % (date.strftime("%d-%m-%y"))

  def _GetFlightContent(self, flights):
    result = ''
    index = 1
    while not flights.empty():
      flight = flights.get()[1]
      result += 'Option #%s:\n' % index
      result += '  Price: %s %s\n' % (flight.GetPrice(), flight.GetCurrency())
      for leg in flight.GetFlightLegs():
        result += leg.ToString()
      index += 1
    return result 

  def Send(self, to, flights):
    """Sends an email to the provided recipient with all the flight offers.

    Args:
      to: Recipient email address.
      flights: Priority queue of flights offered ordered by price.
    """
    if not flights:
      return
    msg = MIMEMultipart('alternative')
    msg['Subject'] = self.subject_
    msg['From'] = self.from_
    msg['To'] = to

    text = 'List of all the flights found for the provided price:\n'
    text += self._GetFlightContent(flights)
    content = MIMEText(text, 'plain')
    msg.attach(content)
    s = smtplib.SMTP('localhost')
    s.sendmail(to, self.from_, msg.as_string())
    s.quit()
