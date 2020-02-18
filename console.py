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
    intro = 'Welcome to HBNB console.   Type "help" or "?" to list commands.\n'
    prompt = '(hbnb) '
    doc_header = "Commands that can help you:\ntype \
\"help <command>\" to know more:"
    undoc_header = "HBNB Comands:"
    ruler = '='
    file = None

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
                if lis[0] not in classes:
                    print("** class doesn't exist **")
                else:
                    data = storage.all()
                    flag = 0
                    for k, v in data.items():
                        token = k.split('.')
                        if lis[1] == token[1]:
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
                        if lis[1] == token[1]:
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

    def do_update(self, arg):
        """Update instances"""
        data = storage.all()
        if len(arg) == 0:
            print("** class name missing **")
        else:
            lis_copy = arg
            lis = lis_copy.split(' ')
            if len(lis) == 1:
                if lis[0] not in classes:
                    print("** class doesn't exist **")
                else:
                    print("** instance id missing **")
            elif len(lis) == 2:
                concat = lis[0] + "." + lis[1]
                if not data.get(concat):
                    print("** no instance found **")
                else:
                    print("** attribute name missing **")

            elif len(lis) == 3:
                print("** value missing **")
            else:
                if lis[3][0] == '"':
                    com = arg.split('"')
                    lis[3] = com[1]
                else:
                    try:
                        lis[3] = int(lis[3])
                        if (lis[3].is_integer()):
                            pass
                        else:
                            try:
                                lis[3] = float(lis[3])
                            except:
                                pass
                    except:
                        pass
                concat = lis[0] + "." + lis[1]
                if data.get(concat):
                    obj = data[concat]
                    setattr(obj, lis[2], lis[3])
                    storage.save()
                else:
                    print("** no instance found **")

    """ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ """

    # Basic commands
    last_output = ''

    def do_shell(self, line):
        """ Run a shell command """
        # print("running shell command:", line)
        sub_cmd = subprocess.Popen(line, shell=True, stdout=subprocess.PIPE)
        output = sub_cmd.communicate()[0].decode('utf-8')
        print(output)
        self.last_output = output

    def do_Hello(self, arg):
        print("Hello, welcome to HBNB console")

    def do_prompt(self, line):
        """ Change the interactive prompt """
        self.prompt = line + ': '

    def do_EOF(self, arg):
        return True

    def do_quit(self, arg):
        sys.exit(1)

    def emptyline(self):
        pass

    do_q = do_quit

    """ +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ """
    # Docummented comands
    def help_quit(self):
        print("Quit command to exit the program\n")

    def help_EOF(self):
        print("Command to close the console")

    def help_q(self):
        print("Shortcut for \"quit\" command\n")

    def help_Hello(self):
        print("Print a welcome message\n")

    def help_emptyline(self):
        print("Do nothing\n")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
