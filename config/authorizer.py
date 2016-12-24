import hashlib
import hmac
import base64
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Authorizer:

  KEY = os.environ.get('MOODSECRET') or '74cebe8a8ceefff4e89635fdd8a92777bb4fd0c541d25a1a10c12f7a126b5b3f243aea19d48c40c0f5b5a8898142a28a69094567c70a2f5e371cc6ac0af90eae'
  SPECIAL_TOKEN = bytes(KEY, "utf-8")

  def __init__(self, token, ts):
    self.token = token
    self.ts = bytes(str(ts), 'utf-8')

  def correct(self):
    return (self.token == self.digested())

  def correct_test(self):
    return True

  def digested(self):
    return hmac.new(self.SPECIAL_TOKEN, self.ts, digestmod=hashlib.sha256).hexdigest().upper()

