#!/usr/bin/python
#CGI BIN FOR userlist.CF
from __future__ import print_function

import cfebase
import cgi
import sys
import os
from subprocess import Popen, PIPE

sys.stderr = sys.stdout
form = cgi.FieldStorage()
os.popen('touch /tmp/latestuser')
print("Content-type: text/html")
HEADER = 'CFE Utility v1.0 for Dev'
command1 = 'scp fwappsadmin@138.208.253.26:/var/lib/cfengine3/masterfiles/userlist.cf /tmp/userlist.cf'
command2 = 'scp /tmp/userlist.cf fwappsadmin@138.208.253.26:/var/lib/cfengine3/masterfiles/userlist.cf'
command3 = "ssh fwappsadmin@138.208.253.26 'sudo chown root:cfebootstrap /var/lib/cfengine3/masterfiles/userlist.cf;sudo rm -rf /var/lib/cfengine3/inputs/*;sudo cp -rf /var/lib/cfengine3/masterfiles/* /var/lib/cfengine3/inputs/;cf-promises -v'"
badlist = []
TEMPLATE = """
<html>
<head>
<meta content="text/html; charset=ISO-8859-1"
http-equiv="content-type">
<title>CFEUtil</title>
</head>
<body>
<h1><small>%s</small></h1>
<span style="font-weight: bold; font-style: italic;">
Warning! This program modifies real CFEngine file: <span
style="text-decoration: underline;">userlist.cf</span>!</span><br>
<br>
Add/Delete Users from the security group user list:<br>
<form method="post" action="cfedevuserlist.py" name="userlist">
<table style="text-align: left; width: 447px; height: 181px;"
border="1" cellpadding="2" cellspacing="2">
<tbody>
<tr>
<td style="vertical-align: top;">Please Select to add or remove
a User:<br>
</td>
<td style="vertical-align: top;">
<select name="method">
<option value="Adduser">Add User</option>
<option value="Deluser">Delete User</option>
</select>
<input name="tclass" value="userlist" type="hidden"><br>
</td>
</tr>
<tr>
<td style="vertical-align: top;">Type the User ID to add or remove:<br>
</td>
<td style="vertical-align: top;"><input name="idnumber"><br>
</td>
</tr>
<tr>
<tr>
<td style="vertical-align: top;">Type the real First AND Last name
of the user:<br>
</td>
<td style="vertical-align: top;"><input name="name"><br>
</td>
</tr>
<tr>
<td style="vertical-align: top;">Select which security groups to modify:<br>
</td>
<td style="vertical-align: top;">%s
<br>
</td>
</tr>
</tbody>
</table>
<input value="Modify Security Groups" type="submit"><br>
<br>
</form>
<form method="post" action="cfedevuserlist.py" name="Server Query">Query
what security groups a User already belongs to: <input name="idnumber">&nbsp;&nbsp;&nbsp;
<input type=hidden name=query value=query>
<input name="tclass" value="userlist" type="hidden">
<input value="Go!" type="submit"><br>
</form>
<form method="post" action="cfedevuserlist.py" name="Class Query">Query
what Users belong to a security group: <select name="group">%s</select>&nbsp;&nbsp;&nbsp;
<input type=hidden name=clsquery value=clsquery>
<input name="tclass" value="userlist" type="hidden">
<input value="Go!" type="submit"><br>
</form>
%s
</body>
</html>
"""


def clslist():
    a = cfebase.caller(tclass='userlist', method='Getgroups')
    with open('/tmp/latestuser', 'w+') as latest:
        for i in a:
            if i not in badlist:
                latest.write(i + '\n')

latest = open('/tmp/latestuser', 'r')
dyncls = ''
qr = ''
for i in latest:
    dyncls += '<input name="group" value="%s" type="checkbox">%s<br>'\
         % (i, i)
latest.close()
dynclsdrop = ''
with open('/tmp/latestuser') as latest:
    for i in latest:
        dynclsdrop += '<option value="%s">%s</option>' % (i, i)
if 'page' in form:
    print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
    if os.path.isfile('/tmp/lockuser'):
	os.remove('/tmp/lockuser')
    exit()
if 'query' in form:
    data = {}
    for field in form:
        if not 'idnumber' in form:
            HEADER = 'You need to fill out all the fields before you submit..'
            print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
            exit()
        else:
            if not isinstance(form[field], list):
                data[field] = form[field].value
            else:
                values = [x.value for x in form[field]]
                data[field] = list(values)
    os.popen(command1)
    clslist()
    clsset = []
    latest = open('/tmp/latestuser')
    for i in latest:
        clsset.append(i)
    for i in clsset:
        clsset[clsset.index(i)] = clsset[clsset.index(i)].rstrip()
    query = []
    for i in clsset:
        a = cfebase.caller(tclass=data['tclass'], method='Getgroupdata',
            group=i)
        for x in a:
            if data['idnumber'] in x:
                query.append(i)
    qr = '<span style="font-weight: bold;">Results:</span><br>'
    for i in query:
        qr += '%s<br>' % i
    print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
    os.remove('/tmp/userlist.cf')
    exit()
if 'clsquery' in form:
    data = {}
    for field in form:
        if not isinstance(form[field], list):
            data[field] = form[field].value
        else:
            values = [x.value for x in form[field]]
            data[field] = list(values)
    data['group'] = data['group'][:-2]
    os.popen(command1)
    clslist()
    clsquery = cfebase.caller(tclass=data['tclass'], group=data['group'],
        method='Getgroupdata')
    qr = '<span style="font-weight: bold;">Results:</span><br>'
    idquery = cfebase.caller(tclass=data['tclass'], method='Getuserids')
    namequery = cfebase.caller(tclass=data['tclass'], method='Getnames')
    for i in clsquery:
        for x in idquery:
            if x in i:
                for z in namequery:
                    if z in i:
                        if not '%s\t%s<br>' % (x, z) in qr:
                            qr += '%s\t%s<br>' % (x, z)
    print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
    os.remove('/tmp/userlist.cf')
    exit()
if os.path.isfile('/tmp/lockuser'):
    HEADER = 'File LOCKED, try again in a few!'
    print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
    clslist()
    exit()
else:
    lock = open('/tmp/lockuser', 'w+')
os.popen(command1)
if not os.path.isfile('/tmp/userlist.cf'):
    HEADER = 'SCP error'
    print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
    os.remove('/tmp/lockuser')
    exit()
data = {}
classlist = []
for field in ('tclass', 'group', 'method', 'idnumber', 'name'):
    if not field in form:
        HEADER = 'You need to fill out all the fields before you submit..'
        print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
        os.remove('/tmp/lockuser')
        clslist()
        os.remove('/tmp/userlist.cf')
        exit()
    else:
        if not isinstance(form[field], list):
            data[field] = form[field].value
        else:
            values = [x.value for x in form[field]]
            data[field] = list(values)
if isinstance(data['group'], list):
    for x in data['group']:
        classlist.append(x)
else:
    classlist.append(data['group'])
for x in classlist:
    classlist[classlist.index(x)] = classlist[classlist.index(x)][:-2]
if isinstance(data['group'], list):
    for i in classlist:
        cfebase.caller(tclass=data['tclass'], method=data['method'],
        name=data['name'], idnumber=data['idnumber'],
        group=classlist[classlist.index(i)])
else:
    cfebase.caller(tclass=data['tclass'], method=data['method'],
            idnumber=data['idnumber'], group=classlist[0], name=data['name'])
clslist()
p2 = Popen(command2, stderr=PIPE, stdout=PIPE, shell=True)
output, errors1 = p2.communicate()
p3 = Popen(command3, stderr=PIPE, stdout=PIPE, shell=True)
output, errors2 = p3.communicate()
lock.close()
os.remove('/tmp/lockuser')
os.remove('/tmp/userlist.cf')
HEADER = '<span style="color: rgb(51, 204, 0); font-weight: bold;">OPERATION SUCCESSFUL</span><br>'
print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))







