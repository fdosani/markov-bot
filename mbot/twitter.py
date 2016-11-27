try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from mbot import logger
log = logger.getLogger(__name__)


class Twitter:
    def __init__(self, credentials_file="config.ini"):
        """
        """
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_secret = None
        try:
            (self.consumer_key, self.consumer_secret, self.access_token,
             self.access_secret) = self._read_ini(credentials_file)
        except KeyError:
            log.error('error reading config file: {0}'.format(credentials_file))
            raise KeyError


    def _read_ini(self, file_name):
        """
        """
        config = configparser.ConfigParser()
        log.info('reading config file: {0}'.format(file_name))
        config.read(file_name)
        return (config["twitter"]["consumer_key"],
                config["twitter"]["consumer_secret"],
                config["twitter"]["access_token"],
                config["twitter"]["access_secret"])
