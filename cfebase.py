#!/usr/bin/python
from modclass import CFEclass
from modsecclass import CFEsecclass
from userlist import CFEuserlist


def caller(tclass, method, classname='N/A', srvname='N/A', group='N/A',
    idnumber='N/A', name='N/A'):
    if tclass == 'classes':
        if method == 'Addtoclass':
            CFEclass(classname=classname).Addtoclass(srvname=srvname)
        if method == 'Delfromclass':
            CFEclass(classname=classname).Delfromclass(srvname=srvname)
        if method == 'Getclasses':
            a = CFEclass(classname=classname).Getclasses()
            return a
        if method == 'Getservers':
            a = CFEclass(classname=classname).Getservers()
            return a
        if method == 'Formtonorm':
            a = CFEclass(classname=classname).Formtonorm()
            return a
    if tclass == 'secclasses':
        if method == 'Addtoclass':
            a = CFEsecclass(classname=classname).Addtoclass(srvname=srvname)
            return a
        if method == 'Delfromclass':
            a = CFEsecclass(classname=classname).Delfromclass(srvname=srvname)
            return a
        if method == 'Getclasses':
            a = CFEsecclass(classname=classname).Getclasses()
            return a
        if method == 'Getservers':
            a = CFEsecclass(classname=classname).Getservers()
            return a
        if method == 'Formtonorm':
            a = CFEsecclass(classname=classname).Formtonorm()
            return a
    if tclass == 'userlist':
        if method == 'Getdata':
            a = CFEuserlist(group=group, idnumber=idnumber, name=name).Getdata()
            return a
        if method == 'Deluser':
            a = CFEuserlist(group=group, idnumber=idnumber, name=name).Deluser()
            return a
        if method == 'Adduser':
            a = CFEuserlist(group=group, idnumber=idnumber, name=name).Adduser()
            return a
        if method == 'Getuserids':
            a = CFEuserlist(group=group, idnumber=idnumber, name=name).\
                Getuserids()
            return a
        if method == 'Getnames':
            a = CFEuserlist(group=group, idnumber=idnumber, name=name).\
            Getnames()
            return a
        if method == 'Getgroupdata':
            a = CFEuserlist(group=group, idnumber=idnumber, name=name).\
                Getgroupdata()
            return a
        if method == 'Getinfo':
            a = CFEuserlist(group=group, idnumber=idnumber, name=name).Getinfo()
            return a
        if method == 'Getgroups':
            a = CFEuserlist(group=group, idnumber=idnumber, name=name).\
            Getgroups()
            return a


#test
#a = caller(tclass='userlist', method='Getnames')
#print(a)
