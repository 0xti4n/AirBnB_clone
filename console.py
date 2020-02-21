#!/usr/bin/python3
import cmd
import sys
import json
import subprocess
import models
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
                    data = models.storage.all()
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
                    data = models.storage.all()
                    flag = 0
                    for k, v in data.copy().items():
                        token = k.split('.')
                        if lis[1] == token[1] and lis[0] == token[0]:
                            flag = 1
                            data[k] = v.to_dict()
                            del data[k]
                    models.storage.save()
                    if flag != 1:
                        print("** no instance found **")

    def do_all(self, arg):
        """Print all instances"""
        args = arg.split()
        if len(args) == 0:
            data = models.storage.all()
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
        data = models.storage.all()
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
                models.storage.all()[obj].save()
            else:
                print("** no instance found **")

    """ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ """
    """ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ """
    # ADVANCED TASKS
    def default(self, line):
        """ Advanced task 11 """
        data = models.storage.all()
        token = line.split('.')
        if token[0] in classes:
            if token[1] == "all()":
                HBNBCommand.do_all(self, token[0].strip('('))

            elif token[1] == "count()":
                con = 0
                for k in data.keys():
                    key_tok = k.split('.')
                    if token[0] == key_tok[0]:
                        con += 1
                print(con)

            cpy1_tok = token[1].split('"')
            cpy2_tok = cpy1_tok[0].strip("(")
            if cpy2_tok == "show":
                concat = token[0] + "." + cpy1_tok[1]
                if data.get(concat):
                    print(data[concat])
                else:
                    print("** no instance found **")

            if cpy2_tok == "destroy":
                concat = token[0] + " " + cpy1_tok[1]
                HBNBCommand.do_destroy(self, concat)

            elif cpy2_tok == "update":
                if '{' not in line:
                    l = [token[0], cpy1_tok[1], cpy1_tok[3], cpy1_tok[5]]
                    concat = l[0] + " " + l[1] + " " + l[2] + " " + '\
"' + l[3] + '"'
                    HBNBCommand.do_update(self, concat)
                else:
                    cpy3_tok = token[1].split('(')
                    cpy4_tok = "{" + cpy3_tok[1].split(', {')[1].strip(')')
                    cpy5_tok = cpy4_tok.replace("'", '"')
                    dic = json.loads(cpy5_tok)
                    for k, v in dic.items():
                        concat = token[0] + " " + cpy1_tok[1] + " \
" + str(k) + " " + '"' + str(v) + '"'
                        HBNBCommand.do_update(self, concat)
        else:
            print("Command not found")

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
