import json

from model.project import Project
import random
import string
import os.path
import json
import getopt
import sys


try:
    opts,args=getopt.getopt(sys.argv[1:], "n:f:",["number of projects","file"])
except getopt.GetoptError as err:
    getopt.usage()
    sys.exit(2)

n=3
f="data/projects.json"

for o,a in opts:
    if o =="-n":
        n=int(a)
    elif o=="-f":
        f=a



def random_string(prefix,maxlen):
    symbols=string.ascii_letters+string.digits
    return prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))])


testdata=[Project(name="", description="")]+ [
     Project(name=random_string("name",10),
             description=random_string("description",17)

             )
     for i in range(1)
    ]


#определение пути к  файлу
file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..",f)


with open(file,"w") as out:
    out.write(json.dumps(testdata, default=lambda x:x.__dict__, indent=2))
