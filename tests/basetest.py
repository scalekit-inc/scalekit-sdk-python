import os
import unittest
from scalekit import ScalekitClient

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """ Before Class Method to initialize ScalekitClient """
        cls.scalekit_client = ScalekitClient(
            os.environ['SCALEKIT_ENV_URL'],
            os.environ['SCALEKIT_CLIENT_ID'],
            os.environ['SCALEKIT_CLIENT_SECRET'])
