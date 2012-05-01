#!/usr/bin/python

from chirpme2 import ChirpData
import cgi
#import cgitb
#cgitb.enable(display=1, logdir="/home4/mcgover1/tmp/pythonlogs")

form = cgi.FieldStorage()    
#usr = ""
chirp = ""
query = ""


redirectURL = "login.py" 

def display(results):
        for line in results:
            line = cgi.escape(line)
            print '<div style="margin-left:auto;margin-right:auto;width:70%;"><p>',line,'</p></div>'
            
#if "username" in form:
#    usr = form["username"].value
if "chirp" in form:
    chirp = form["chirp"].value
if "query" in form:
    #prequery = query
    query = form.getfirst('query', 'empty')

prequery = query    
#    query = form["query"].value


if chirp:
    newChirp = ChirpData()                                            #create instance of class
    newChirp.chirp_add(chirp)
    print ("Status: 303 See Other")
    print ("Location: %s" % redirectURL)                        # takes care of refresh problem
    print ('')                                                  # blank line, end of headers
else:
    print ("Content-Type: text/html; charset=utf-8\n")                           # HTML is following
    print ('''<!DOCTYPE HTML>
<html>
<head>
<title>mcgoverns.com</title>
<meta charset="UTF-8">
<style type="text/css">
p.chirps
{
color:blue;
}
p.chirpMine
{
color:red;
}
.center
{
margin:auto;
width:70%
display:inline;
}
div.newChirp
{
display:inline;
}
</style>
</head>
<body onload="document.search.reset();">
<div class="center">
<fieldset style="width:50%;">
<legend>CreateChirp</legend>
<form action="http://www.mcgoverns.com/cgi-bin/login.py" method="post" name="chirpString">
<!--Username: <input type="text" name="username" size="24"><br>-->
Chirp: <input type="text" name="chirp" size="30"><br><br>
<input type="submit" value="chirp"><br>
</form>
</fieldset>
</div>
<div class="center">
<fieldset style="width:45%;">
<legend>Looking for something?</legend>
<form action="http://mcgoverns.com/cgi-bin/login.py" method="get" name="search" autocomplete="off">
<input type="text" name="query" size="40" autocomplete="off">
<input type="submit" value="search">
</form>
</fieldset>
</div><br><br>
''')

if not query:
    displayChirps = ChirpData()
    results = displayChirps.get_older_chirps(21)
    display(results)
    print '<p>from in not query</p>'
else:
    queryChirps = ChirpData()
    results = queryChirps.get_older_chirps(200,query)
    display(results)
    queryChirps.get_older_chirps(20,'%')    
    print '</body>'
    print '</html>'
