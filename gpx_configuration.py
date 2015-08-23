import ConfigParser
import io

SECTION_ = "GPX-Alert"

class GpxConfiguration:
  """Object that holds the content of a GPX alert configuration."""

  def __init__(self, config_path):
    """Constructor of the class.

    Args:
      config_path: Path to the config file.
    """
    config = ConfigParser.ConfigParser()
    config.read(config_path)
    self.api_key_ = config.get(SECTION_, 'API_KEY')
    self.api_url_ = config.get(SECTION_, 'API_URL')
    self.source_ = config.get(SECTION_, 'SOURCE')
    self.destination_ = config.get(SECTION_, 'DESTINATION')
    self.threshold_ = float(config.get(SECTION_, 'THRESHOLD'))
    self.email_ = config.get(SECTION_, 'EMAIL')

  def GetApiKey(self):
    return self.api_key_

  def GetApiUrl(self):
    return self.api_url_

  def GetSource(self):
    return self.source_

  def GetDestination(self):
    return self.destination_

  def GetThreshold(self):
    return self.threshold_

  def GetEmail(self):
    return self.email_
