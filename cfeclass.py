#!/usr/bin/python
#CGI BIN FOR CLASSES.CF
from __future__ import print_function

import cfebase
import cgi
import sys
import os
from subprocess import Popen, PIPE


sys.stderr = sys.stdout
form = cgi.FieldStorage()
os.popen('touch /tmp/latest')
print("Content-type: text/html")
HEADER = 'CFE Utility v1.0 for Prod'
command1 = 'scp fwappsadmin@138.208.1.90:/var/lib/cfengine3/masterfiles/classes.cf /tmp/classes.cf'
command2 = 'scp /tmp/classes.cf fwappsadmin@138.208.1.90:/var/lib/cfengine3/masterfiles/classes.cf'
command3 = "ssh fwappsadmin@138.208.1.90 'sudo chown root:cfebootstrap /var/lib/cfengine3/masterfiles/classes.cf;sudo \
/var/lib/cfengine3/masterfiles-commit.sh s'"
badlist = ['policy_server', 'commonapt_bundle', 'rogueremove', 'debian',
    'subnet253', 'subnet1', 'subnet63', 'subnet22', 'subnet21', 'subnet82',
    'subnet95', 'subnet201', 'subnet100', 'sshenable', 'ntpenable',
    'pacifictimezone', 'krb5enable', 'logrotate_bundle', 'snmp_bundle',
    'motd_bundle', 'rsyslogdev_bundle', 'rsyslogprod_bundle', 'hostnamefqdn',
    'masterkeyall', 'crontabdaily']
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
style="text-decoration: underline;">classes.cf</span>!</span><br>
<br>
Add/Delete Servers from Classes:<br>
<form method="post" action="cfeclass.py" name="classes">
<table style="text-align: left; width: 447px; height: 181px;"
border="1" cellpadding="2" cellspacing="2">
<tbody>
<tr>
<td style="vertical-align: top;">Please Select to add or remove
a server:<br>
</td>
<td style="vertical-align: top;">
<select name="method">
<option value="Addtoclass">Add Server</option>
<option value="Delfromclass">Remove Server</option>
</select>
<input name="tclass" value="classes" type="hidden"><br>
</td>
</tr>
<tr>
<td style="vertical-align: top;">Type the server name to add or
remove:<br>
</td>
<td style="vertical-align: top;"><input name="srvname"><br>
</td>
</tr>
<tr>
<td style="vertical-align: top;">Select which classes to modify:<br>
</td>
<td style="vertical-align: top;">%s
<br>
</td>
</tr>
</tbody>
</table>
<input value="Modify Classes" type="submit"><br>
<br>
</form>
<form method="post" action="cfeclass.py" name="Server Query">Query
what classes a server already belongs to: <input name="srvname">&nbsp;&nbsp;&nbsp;
<input type=hidden name=query value=query>
<input name="tclass" value="classes" type="hidden">
<input value="Go!" type="submit"><br>
</form>
<form method="post" action="cfeclass.py" name="Class Query">Query
what servers belong to a class: <select name="classname">%s</select>&nbsp;&nbsp;&nbsp;
<input type=hidden name=clsquery value=clsquery>
<input name="tclass" value="classes" type="hidden">
<input value="Go!" type="submit"><br>
</form>
%s
</body>
</html>
"""


def clslist():
    a = cfebase.caller(tclass='classes', method='Getclasses')
    with open('/tmp/latest', 'w+') as latest:
        for i in a:
            if i not in badlist:
                latest.write(i + '\n')

latest = open('/tmp/latest', 'r')
dyncls = ''
qr = ''
for i in latest:
    dyncls += '<input name="classname" value="%s" type="checkbox">%s<br>'\
         % (i, i)
latest.close()
dynclsdrop = ''
with open('/tmp/latest') as latest:
    for i in latest:
        dynclsdrop += '<option value="%s">%s</option>' % (i, i)
if 'page' in form:
    print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
    if os.path.isfile('/tmp/lock'):
        os.remove('/tmp/lock')
    exit()
if 'query' in form:
    data = {}
    for field in form:
        if not 'srvname' in form:
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
    latest = open('/tmp/latest')
    for i in latest:
        clsset.append(i)
    for i in clsset:
        clsset[clsset.index(i)] = clsset[clsset.index(i)].rstrip()
    query = []
    for i in clsset:
        a = cfebase.caller(tclass=data['tclass'], method='Formtonorm',
        classname=i)
        if data['srvname'] in a:
            query.append(i)
    qr = '<span style="font-weight: bold;">Results:</span><br>'
    for i in query:
        qr += '%s<br>' % i
    print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
    os.remove('/tmp/classes.cf')
    exit()
if 'clsquery' in form:
    data = {}
    for field in form:
        if not isinstance(form[field], list):
            data[field] = form[field].value
        else:
            values = [x.value for x in form[field]]
            data[field] = list(values)
    data['classname'] = data['classname'][:-2]
    os.popen(command1)
    clsquery = cfebase.caller(tclass=data['tclass'],
    classname=data['classname'], method='Formtonorm')
    qr = '<span style="font-weight: bold;">Results:</span><br>'
    for i in clsquery:
        qr += '%s<br>' % i
    print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
    clslist()
    os.remove('/tmp/classes.cf')
    exit()
if os.path.isfile('/tmp/lock'):
    HEADER = 'File LOCKED, try again in a few!'
    print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
    clslist()
    exit()
else:
    lock = open('/tmp/lock', 'w+')
os.popen(command1)
if not os.path.isfile('/tmp/classes.cf'):
    HEADER = 'SCP error'
    print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
    os.remove('/tmp/lock')
    exit()
data = {}
classlist = []
for field in ('tclass', 'classname', 'srvname', 'method'):
    if not field in form:
        HEADER = 'You need to fill out all the fields before you submit..'
        print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))
        os.remove('/tmp/lock')
        clslist()
        os.remove('/tmp/classes.cf')
        exit()
    else:
        if not isinstance(form[field], list):
            data[field] = form[field].value
        else:
            values = [x.value for x in form[field]]
            data[field] = list(values)
if isinstance(data['classname'], list):
    for x in data['classname']:
        classlist.append(x)
else:
    classlist.append(data['classname'])
for x in classlist:
    classlist[classlist.index(x)] = classlist[classlist.index(x)][:-2]
if isinstance(data['classname'], list):
    for i in classlist:
        cfebase.caller(tclass=data['tclass'], method=data['method'],
            srvname=data['srvname'], classname=classlist[classlist.index(i)])
else:
    cfebase.caller(tclass=data['tclass'], method=data['method'],
            srvname=data['srvname'], classname=classlist[0])
clslist()
p2 = Popen(command2, stderr=PIPE, stdout=PIPE, shell=True)
output, errors = p2.communicate()
p3 = Popen(command3, stderr=PIPE, stdout=PIPE, shell=True)
output, errors = p3.communicate()
lock.close()
os.remove('/tmp/lock')
os.remove('/tmp/classes.cf')
HEADER = '<span style="color: rgb(51, 204, 0); font-weight: bold;">OPERATION SUCCESSFUL</span><br>'
print(TEMPLATE % (HEADER, dyncls, dynclsdrop, qr))






