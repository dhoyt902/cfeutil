#!/usr/bin/python
from __future__ import print_function
import re


class CFEuserlist:

    def __init__(self, group='No Group', idnumber='No Number',
        name='Real Name'):
        self.group = group
        self.idnumber = idnumber
        self.name = name

    def Getdata(self):
        flist = open('/tmp/userlist.cf', 'r')
        wlist = []
        for i in flist:
            wlist.append(i)
        dataset = []
        for val in wlist:
            if '=>' in val:
                dataset.append(val)
        return dataset

    def Getuserids(self):
        dataset = CFEuserlist().Getdata()
        ids = []
        for i in dataset:
            re1 = '.*?'
            re2 = '(\\d+)'
            rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
            m = rg.search(i)
            if m:
                idnum = m.group(1)
                ids.append(idnum)
        for t in dataset:
            re1 = '.*?'
            re2 = '(?:[a-z][a-z]+)'
            re3 = '.*?'
            re4 = '((?:[a-z][a-z]+))'
            rg = re.compile(re1 + re2 + re3 + re4, re.IGNORECASE | re.DOTALL)
            m = rg.search(t)
            if m:
                idnam = m.group(1)
                if idnam != 'string':
                    ids.append(idnam)
        return ids

    def Getnames(self):
        dataset = CFEuserlist().Getdata()
        names = []
        for i in dataset:
            re1 = '.*?'
            re2 = '(?:[a-z][a-z]+)'
            re3 = '.*?'
            re4 = '(?:[a-z][a-z]+)'
            re5 = '.*?'
            re6 = '((?:[a-z][a-z]+))'
            re7 = '(\\s+)'
            re8 = '((?:[a-z][a-z]+))'
            rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8,
                re.IGNORECASE | re.DOTALL)
            m = rg.search(i)
            if m:
                first = m.group(1)
                space = m.group(2)
                last = m.group(3)
                names.append(first + space + last)
        return names

    def Getgroups(self):
        dataset = CFEuserlist().Getdata()
        groups = []
        for i in dataset:
            re1 = '.*?'
            re2 = '((?:[a-z][a-z]+))'
            rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
            m = rg.search(i)
            if m:
                group = m.group(1)
                if group not in groups:
                    groups.append(group)
        return groups

    def Isdupe(self):
        idnumber = self.idnumber
        totalids = CFEuserlist().Getuserids()
        if totalids.count(idnumber) > 4:
            return True
        else:
            return False

    def Getinfo(self):
        idnumber = self.idnumber
        dataset = CFEuserlist().Getdata()
        info = []
        for i in dataset:
            if idnumber in i:
                info.append(i)
        retinfo = []
        for x in info:
            re1 = '.*?'
            re2 = '((?:[a-z][a-z]+))'
            rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
            m = rg.search(x)
            if m:
                group = m.group(1)
                retinfo.append(group)
        info += retinfo
        return info[-1]

    def Getgroupdata(self):
        group = self.group
        dataset = CFEuserlist().Getdata()
        groupdata = []
        for i in dataset:
            if i.startswith('\t\t"%s' % group):
                groupdata.append(i)
        return groupdata

    def Adduser(self):
        group = self.group
        idnumber = self.idnumber
        name = self.name
        template = '\t\t"%s[%s]" string => "%s";\t\t#%s\n' % \
            (group, idnumber, idnumber, name)
        modset = CFEuserlist(group=group, idnumber=idnumber, name=name).\
            Getgroupdata()
        modset.append(template)
        wholefile = open('/tmp/userlist.cf')
        wholelist = []
        for i in wholefile:
            wholelist.append(i)
        wholefile.close()
        if CFEuserlist(group=group, idnumber=idnumber, name=name).\
            Isdupe() is False:
            delim = modset[0]
            wholelist.insert(wholelist.index(delim), 'PLACEHOLDER')
            newlist = [x for x in wholelist if x not in modset]
            modset.reverse()
            for i in modset:
                newlist.insert(wholelist.index('PLACEHOLDER'), i)
            newlist.remove('PLACEHOLDER')
            with open('/tmp/userlist.cf', 'w+') as \
                userfile:
                for line in newlist:
                    userfile.write(line)

    def Deluser(self):
        idnumber = self.idnumber
        with open('/tmp/userlist.cf') as mfile:
            masterset = [i for i in mfile]
        masterset = [x for x in masterset if idnumber not in x]
        with open('/tmp/userlist.cf', 'w+') as \
            userfile:
            for line in masterset:
                userfile.write(line)


#test code
#CFEuserlist(group='serveradmin', name='Ryan Wood', idnumber='rwood').Adduser()
