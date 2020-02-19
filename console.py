#!/usr/bin/python3
import cmd
import sys
import json
import subprocess
import models
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.base_model import BaseModel

classes = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]


class HBNBCommand(cmd.Cmd):
    doc_header = "\nDocumented commands (type help <topic>):"
    prompt = '(hbnb) '

    """ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ """
    # Commands to HBNB:
    def do_create(self, arg):
        """Create Instances"""
        if len(arg) == 0:
            print("** class name missing **")
        elif arg in classes:
            new_instance = eval(arg + "()")
            new_instance.save()
            print(new_instance.id)
        else:
            print("** class doesn't exist **")

    def do_show(self, arg):
        """Show Instances"""
        if len(arg) == 0:
            print("** class name missing **")

        else:
            lis = arg.split(' ')
            if len(lis) == 1:
                if lis[0] not in classes:
                    print("** class doesn't exist **")
                else:
                    print("** instance id missing **")
            else:
                flag = 0
                if lis[0] not in classes:
                    print("** class doesn't exist **")
                else:
                    data = storage.all()
                    flag = 0
                    for k, v in data.items():
                        token = k.split('.')
                        if lis[1] == token[1] and lis[0] == token[0]:
                            print(v)
                            flag = 1
                    if flag != 1:
                        print("** no instance found **")

    def do_destroy(self, arg):
        """Destroy instances"""
        if len(arg) == 0:
            print("** class name missing **")

        else:
            lis = arg.split(' ')
            if len(lis) == 1:
                if lis[0] not in classes:
                    print("** class doesn't exist **")
                else:
                    print("** instance id missing **")
            else:
                if lis[0] not in classes:
                    print("** class doesn't exist **")
                else:
                    data = storage.all()
                    flag = 0
                    for k, v in data.copy().items():
                        token = k.split('.')
                        if lis[1] == token[1] and lis[0] == token[0]:
                            flag = 1
                            data[k] = v.to_dict()
                            del data[k]
                    if flag != 1:
                        print("** no instance found **")
                    storage.save()

    def do_all(self, arg):
        """Print all instances"""
        args = arg.split()
        if len(args) == 0:
            data = storage.all()
            l = []
            for v in data.values():
                l.append(str(v))
            print(l)
        elif args[0] in classes:
            try:
                with open("file.json", "r") as f:
                    data = json.loads(f.read())
                l = []
                for k, v in data.items():
                    token = k.split('.')
                    if arg == token[0]:
                        obj = eval(arg + "(**v)")
                        l.append(str(obj))
                print(l)
            except:
                pass
        else:
            print("** class doesn't exist **")

    def validator(self, lis):
        """ Validator """
        if len(lis) == 0:
            print("** class name missing **")
            return
        elif lis[0] not in classes:
            print("** class doesn't exist **")
            return
        elif len(lis) < 2:
            print("** instance id missing **")
            return
        return (lis[0] + "." + lis[1])

    def do_update(self, arg):
        """Update instances"""
        copy = arg
        lis = copy.split()
        data = storage.all()
        obj = self.validator(lis)

        if obj:
            list_Int = ["number_rooms", "number_bathrooms",
                        "max_guest", "price_by_night"]
            list_float = ["latitude", "longitude"]
            if len(lis) < 3:
                if not data.get(obj):
                    print("** no instance found **")
                    return
                else:
                    print("** attribute name missing **")
                    return
            elif len(lis) < 4:
                if not data.get(obj):
                    print("** no instance found **")
                    return
                else:
                    print("** value missing **")
                    return
            if lis[3][0] == '"':
                com = arg.split('"')
                lis[3] = com[1]

            if (lis[2] in list_Int):
                num_int = lis[3]
                l = num_int.split('.')
                lis[3] = l[0]
                try:
                    lis[3] = int(lis[3])
                except:
                    pass
            elif (lis[2] in list_float):
                try:
                    data_float = float(lis[3])
                    lis[3] = data_float
                except:
                    pass

            if data.get(obj):
                ref = data[obj]
                setattr(ref, lis[2], lis[3])
                storage.save()
            else:
                print("** no instance found **")

    """ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ """
    """ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ """
    # ADVANCED TASKS
    def default(self, line):
        """ Advanced task 11 """
        token = line.split('.')
        if token[0] in classes:
            HBNBCommand.do_all(self, token[0].strip('('))

    """ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ """
    """ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ """

    # Basic commands
    def do_EOF(self, arg):
        print("")
        return True

    def do_quit(self, arg):
        sys.exit(1)

    def emptyline(self):
        pass

    """ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ """
    # Docummented comands
    def help_quit(self):
        print("Quit command to exit the program\n")

    def help_EOF(self):
        print("Command to close the console")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
