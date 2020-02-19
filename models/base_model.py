#!/usr/bin/python3
import uuid
import datetime
import models
""" Class basemodel """


class BaseModel():
    """BaseModel"""

    def __init__(self, *args, **kwargs):
        """ init """
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k != "__class__":
                    if k == "created_at":
                        v = datetime.datetime.strptime(v, "\
%Y-%m-%dT%H:%M:%S.%f")
                    if k == "updated_at":
                        v = datetime.datetime.strptime(v, "\
%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, k, v)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def save(self):
        """Save"""
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """Convert to dict"""
        dic = self.__dict__.copy()
        dic['__class__'] = self.__class__.__name__
        dic['created_at'] = self.created_at.isoformat('T')
        dic['updated_at'] = self.updated_at.isoformat('T')
        return dic

    def __str__(self):
        """representation of str"""
        return ('[{}] ({}) \
{}'.format(self.__class__.__name__, self.id, self.__dict__))
