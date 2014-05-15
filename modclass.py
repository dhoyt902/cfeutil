#!/usr/bin/python
from __future__ import print_function
import os
import re


class CFEclass:

    def __init__(self, classname=''):
        self.classname = classname

    def Getclasses(self):
        fclass = open('/tmp/classes.cf', 'r')
        clslist = []
        for x in fclass.readlines():
            if '=>' in x:
                re1 = '.*?'
                re2 = '((?:[a-z][a-z0-9_]*))'
                rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
                m = rg.search(x)
                if m:
                    clslist.append(m.group(1))
        fclass.close()
        return clslist

    def Getservers(self):
        header = self.classname
        clist = CFEclass().Getclasses()
        if header in clist:
            fclass = open('/tmp/classes.cf', 'r')
            temp = open('/tmp/temp.txt', 'w+')
            srvlist = []
            for x in re.findall('"%s"\ or\ =>(.*?);' % header, fclass.read(),
                re.S):
                temp.write(x)
            temp.close()
            with open('/tmp/temp.txt') as temp:
                for y in re.findall('{(.*?)}', temp.read(), re.S):
                    srvlist.append(y)
            fclass.close()
            os.remove('/tmp/temp.txt')
            return srvlist

    def Isdupe(self, srvname):
        self.srvname = srvname
        classname = self.classname
        srvlist = CFEclass(classname).Formtonorm()
        x = self.srvname in srvlist
        return x

    def Formtonorm(self):
        temp1 = open('/tmp/temp1.txt', 'w+')
        for i in CFEclass(classname=self.classname).Getservers():
            print(i, file=temp1)
        normlist = []
        temp1.close()
        with open('/tmp/temp1.txt') as srvlist:
            for x in srvlist.readlines():
                re1 = '.*?'
                re2 = '(?:[a-z][a-z0-9_]*)'
                re3 = '.*?'
                re4 = '((?:[a-z][a-z0-9_]*))'
                rg = re.compile(re1 + re2 + re3 + re4, re.IGNORECASE |
                    re.DOTALL)
                m = rg.search(x)
                if m:
                    res = m.group(1)
                    res = re.sub('_', '-', res)
                    normlist.append(res)
        srvlist.close()
        os.remove('/tmp/temp1.txt')
        return normlist

    def Normtoform(self, srvname):
        cfname = re.sub('-', '_', srvname)
        return cfname

    def Addtoclass(self, srvname):
        classname = self.classname
        template = ['\t"%s" or => {' % classname, '        };\n\n']
        dataset = CFEclass(classname).Getservers()[0].split('\n')
        for i in dataset:
            dataset[dataset.index(i)] = re.sub('\n', '', i)
        if CFEclass(classname).Isdupe(srvname) is False:
            srvname = CFEclass(classname).Normtoform(srvname)
            srvname = '\t\tclassify("%s")' % srvname
            if len(dataset) > 2:
                dataset[-2] += ','
            dataset.insert(-1, srvname)
            for i in dataset:
                if i.isspace():
                    dataset.remove(i)
            dataset.insert(0, template[0])
            for i in dataset:
                if i != '':
                    dataset[dataset.index(i)] += '\n'
            dataset.append(template[1])
            wholefile = open('/tmp/classes.cf', 'r')
            wholelist = []
            for line in wholefile:
                wholelist.append(line)
            clslist = CFEclass().Getclasses()
            if classname != clslist[-1]:
                cldelim = clslist[int(clslist.index(classname)) + 1]
                wholelist = wholelist[:wholelist.index('\t"%s" or => {\n' %
                    classname)] + wholelist[wholelist.index('\t"%s" or => {\n' %
                    cldelim):]
                for entry in dataset:
                    wholelist.insert(wholelist.index('\t"%s" or => {\n' %
                        cldelim), entry)
            else:
                wholelist = wholelist[:wholelist.index('\t"%s" or => {\n' %
                    classname)] + wholelist[-1:]
                for entry in dataset:
                    wholelist.insert(-1, entry)
            wholefile.close()
            with open('/tmp/classes.cf', 'w+') as \
            newfile:
                for line in wholelist:
                    newfile.write(line)

    def Delfromclass(self, srvname):
        classname = self.classname
        template = ['\t"%s" or => {' % classname, '        };\n\n']
        dataset = CFEclass(classname).Getservers()[0].split('\n')
        for i in dataset:
            dataset[dataset.index(i)] = re.sub('\n', '', i)
        if CFEclass(classname).Isdupe(srvname) is True:
            srvname = CFEclass(classname).Normtoform(srvname)
            for i in dataset:
                if i.isspace():
                    dataset.remove(i)
            srvnamesyn = '\t\tclassify("%s")' % srvname
            if srvnamesyn == dataset[-1]:
                    dataset[-2] = dataset[-2][:-1]
            for i in dataset:
                if srvname in i:
                    dataset.remove(i)
            dataset.insert(0, template[0])
            for i in dataset:
                if i != '':
                    dataset[dataset.index(i)] += '\n'
            dataset.append(template[1])
            wholefile = open('/tmp/classes.cf', 'r')
            wholelist = []
            for line in wholefile:
                wholelist.append(line)
            clslist = CFEclass().Getclasses()
            if classname != clslist[-1]:
                cldelim = clslist[int(clslist.index(classname)) + 1]
                wholelist = wholelist[:wholelist.index('\t"%s" or => {\n' %
                    classname)] + wholelist[wholelist.index('\t"%s" or => {\n' %
                    cldelim):]
                for entry in dataset:
                    wholelist.insert(wholelist.index('\t"%s" or => {\n' %
                        cldelim), entry)
            else:
                wholelist = wholelist[:wholelist.index('\t"%s" or => {\n' %
                    classname)] + wholelist[-1:]
                for entry in dataset:
                    wholelist.insert(-1, entry)
            wholefile.close()
            with open('/tmp/classes.cf', 'w+') as \
            newfile:
                for line in wholelist:
                    newfile.write(line)












