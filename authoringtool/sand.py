'''
Created on Jun 18, 2016

@author: ad
'''
import os
# from fileinput import filename
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authoringtool.settings')
 
import django
django.setup()

from django.utils import timezone
from sequencelistings.models import SequenceListing, Title, Sequence, Feature, Qualifier
from populate_db import add_title, copySequenceListing

from sequencelistings.util import expandFormula 

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
        
# sls = SequenceListing.objects.all()
# for sl in sls:
#     setSequenceName(sl)

# myCopyScript('Invention_SEQL')

# print 'GGGX'*100
# print expandFormula('cg(agg)4..7')
# <?xml-stylesheet type="text/xsl" href="resources/st26_w3_4.xsl"?>
# <p><a href="{% static filePath %}">see generated sequence listing</a></p>
# {% for f in seq.feature_set.all %}