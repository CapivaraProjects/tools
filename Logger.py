import json
import requests
import models.Logger

class Logger:
    """
    Logger class used to add logs
    """

    @staticmethod
    def create(url='', type='', message='', function='', obs='', config=''):
        """
        (str, str, str, str, str) -> (str)
        Method used to create a log and insert into elasticsearch
        """
        if config != 'TEST':
            logger = str(json.dumps(models.Logger.Logger(type, message, function, obs, config).__dict__))
            return requests.post(url, data=logger).text
