'''
Created on Jun 18, 2016

@author: ad
'''
import os
import csv
import pprint 
# import codecs
# from fileinput import filename
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authoringtool.settings')
 
import django
django.setup()

from django.utils import timezone
from sequencelistings.models import SequenceListing, Title, Sequence, Feature, Qualifier
from populate_db import add_title, copySequenceListing

from sequencelistings import util

def myCopyScript(aFileName):
    sl = SequenceListing.objects.filter(fileName=aFileName)[0] 
    copySequenceListing(sl)
    print 'Done with copying', aFileName

def setSequenceName(sequenceListing):
    sequences = sequenceListing.sequence_set.all()
    for seq in sequences:
        seq.sequenceName = 'seq_%i' % seq.sequenceIdNo
        seq.save()
        seq.inspectSequence()

# class Feature(object):
#     def __init__(self, name, mandatoryQualifiers, optionalQualifiers):
        
        
def setQualifierSets(aFilePath):
    with open(aFilePath, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        man = {}
        opt = {}
        n = reader.next()
        for k,v in n.iteritems():
            man[k] = []
            opt[k] = []
        del(man['Qualifier'])
        del(opt['Qualifier'])
        for row in reader:
            for k, v in row.iteritems():
                if v == 'M':
                    man[k].append(row['Qualifier'])
                elif v == 'O':
                    opt[k].append(row['Qualifier'])   
#         pprint.pprint(res)                 
        for k in sorted(man.keys()):
            print k 
            print '\tmandatory:', sorted(man[k])
            print '\toptional:', sorted(opt[k])
            
    
fp = os.path.join(util.PROJECT_DIRECTORY, 'sequencelistings', 'static', 'res', 'FeatureKeyQualifierCrossRef_wINSD_FT_10_6_14_Jul_2017.csv')

# setQualifierSets(fp)
        
# sls = SequenceListing.objects.all()
# for sl in sls:
#     setSequenceName(sl)

# myCopyScript('Invention_SEQL')

# print 'GGGX'*100
# print util.expandFormula('cg(agg)4..7')
# <?xml-stylesheet type="text/xsl" href="resources/st26_w3_4.xsl"?>
# <p><a href="{% static filePath %}">see generated sequence listing</a></p>
# {% for f in seq.feature_set.all %}