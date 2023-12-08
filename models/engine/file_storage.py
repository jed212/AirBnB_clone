#!/usr/bin/python3
"""
Defines the FileStorage class.
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    Represent an abstracted storage engine.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Return the dictionary __objects.
        """
        return self.__objects

    def new(self, obj):
        """
        Set in __objects obj with key <obj_class_name>.id
        """
        ocname = obj.__class__.__name__
        self.__objects["{}.{}".format(ocname, obj.id)] = obj

    def save(self):
        """
        Serialize __objects to the JSON file __file_path.
        """
        odict = self.__objects
        objdict = {obj: odict[obj].to_dict() for obj in odict.keys()}
        with open(self.__file_path, "w") as f:
            json.dump(objdict, f)

    def reload(self):
        """
        Deserialize the JSON file __file_path to __objects, if it exists.
        """
        try:
            with open(self.__file_path) as f:
                objdict = json.load(f)
                for v in objdict.values():
                    class_name = v["__class__"]
                    del v["__class__"]
                    self.new(eval(class_name)(**v))
        except FileNotFoundError:
            return
