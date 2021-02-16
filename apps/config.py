import os
from uuid import uuid4


class Config:
    SECRET_KEY = str(uuid4())
    DEBUG = True