import hashlib
import hmac
import os
from dotenv import load_dotenv
import json

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

KEY = os.environ.get('MOODSECRET') or '74cebe8a8ceefff4e89635fdd8a92777bb4fd0c541d25a1a10c12f7a126b5b3f243aea19d48c40c0f5b5a8898142a28a69094567c70a2f5e371cc6ac0af90eae'
SPECIAL_TOKEN = bytes(KEY, "utf-8")

def authorize(token, ts):
  salt = bytes(str(ts), 'utf-8')
  return (token == digested(salt))

def digested(salt):
  return hmac.new(SPECIAL_TOKEN, salt, digestmod=hashlib.sha256).hexdigest().upper()
