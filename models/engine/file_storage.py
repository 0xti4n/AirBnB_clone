#!/usr/bin/python3
import json
from models.base_model import BaseModel
import models
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
""" Class FileStorage """


class FileStorage():
    """ FileStorage """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Return all """
        return (FileStorage.__objects)

    def new(self, obj):
        """ Creat new """
        key = obj.__class__.__name__ + "." + obj.id
        FileStorage.__objects[key] = obj

    def save(self):
        """ Save all """
        dict_copy = {}
        for k, val in FileStorage.__objects.items():
            dict_copy[k] = val.to_dict()

        with open(FileStorage.__file_path, 'w') as f:
            f.write(json.dumps(dict_copy))

    def reload(self):
        """ Reload all """
        try:
            with open(self.__file_path, 'r') as f:
                data = json.loads(f.read())
                for k, v in data.items():
                    name = k.split('.')
                    obj = eval(name[0] + "(**v)")
                    self.__objects[k] = obj
        except:
            pass
