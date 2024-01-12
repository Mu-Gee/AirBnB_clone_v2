#!/usr/bin/python3
"""create a unique FileStorage instance for your application"""
import os

import models
from . base_model import BaseModel
from . amenity import Amenity
from . city import City
from . place import Place
from . review import Review
from . state import State
from . user import User
from . engine import db_storage, file_storage

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    storage = db_storage.DBStorage()
else:
    storage = file_storage.FileStorage()

storage.reload()
