import os
import urllib
import json
import subprocess

perms = 0o777
name = raw_input("Please enter the name of the project:\n")

print "Checking if app already exists..."
if os.path.exists(name):
    print "App already exists, try again with a different name"
    exit(0)
print "OK!"

print "Checking if config file exists..."
if not os.path.isfile("config.json"):
    print "Error, no config file found..."
    print "Creating config file..."
    c = open("config.json", "w")
    c.write('{"scripts" : ["http://code.jquery.com/jquery-latest.min.js"]}')
    c.close()
    print "Config file created, please try again..."
    exit(0)
print "OK!"

print "Opening config file..."
settings = open("config.json")
print "OK!"
print "Reading JSON..."
config = json.loads(settings.read())
scripts = config["scripts"]
print "OK!"

print "Creating project structure..."
os.mkdir(name, perms)
os.chdir(name)
os.mkdir("scripts", perms)
os.mkdir("img", perms)
os.mkdir("styles", perms)
print "OK!"

print "Writing to files..."
indexContent = "<!-- Auto generated by https://github.com/charliedowler/WebAppTemplate -->" \
               "\n<!DOCTYPE html>" \
               "\n<html>" \
               "\n\t<head>" \
               "\n\t\t<title>" + name + "</title>"
for index, item in enumerate(scripts):
    ext = item.split("/")[-1]
    indexContent += "\n\t\t<script src='scripts/" + ext + "'></script>"

indexContent += "\n\t\t<script src='scripts/app.js'></script>" \
                "\n\t</head>" \
                "\n\t<body>" \
                "\n\t\t<h1>Hello World!</h1>" \
                "\n\t</body>" \
                "\n</html>"
index = "index.html"
file = open(index, 'w')
file.write(indexContent)
file.close()

appFilename = "app.js"
app = open('scripts/'+appFilename, 'w')
app.write("console.log('App Started');")
app.close()

print "OK!"

for index, item in enumerate(scripts):
    ext = item.split("/")[-1]
    print "Downloading " + item + "..."
    urllib.urlretrieve(item, "scripts/" + ext)
    print "OK!"

print "Running 'git init'..."
try:
    subprocess.call(["git", "init"])
    print "OK!"
except OSError:
    print "Git init failed, please make sure that you have git added to your PATH variable..."