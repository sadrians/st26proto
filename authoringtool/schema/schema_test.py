'''
Created on May 27, 2018

@author: ad
'''
import django
from lib2to3.pygram import Symbols
django.setup()

from django.test import TestCase

import os 
from sequencelistings import util

SCHEMA_PATH = os.path.join(util.PROJECT_DIRECTORY, 'schema', 'xsd', 'st26_20180527.xsd')

class SchemaTests(TestCase):
    
    def getTestFilePath(self, aFileName):
        return os.path.join(util.TEST_DATA_DIR_PATH, aFileName)
    
    def test_validateDocumentWithSchema(self):
        """
        Test that xml sequence listing files are correctly validated 
        against the schema.
        """
#         print 'Running %s ...' % getName()
#         valid seql contains the first 2 seqs from f2 - goes via if branch
        f3 = os.path.join(util.TEST_DATA_DIR_PATH, 'test3.xml')
        self.assertTrue(util.validateDocumentWithSchema(f3, SCHEMA_PATH))
   
#         ApplicantNamex instead of ApplicantName - goes to except branch
        f4 = os.path.join(util.TEST_DATA_DIR_PATH, 'test4.xml')        
        self.assertFalse(util.validateDocumentWithSchema(f4, SCHEMA_PATH))
   
#         SOURCxE instead of SOURCE - goes to else branch 
        f5 = os.path.join(util.TEST_DATA_DIR_PATH, 'test5.xml')        
        self.assertFalse(util.validateDocumentWithSchema(f5, SCHEMA_PATH))
  
#         supplementary test with seql with more sequences
#         valid seql 20 sequences
# this test file will fail because seq 19 contains u symbols
        f2 = os.path.join(util.TEST_DATA_DIR_PATH, 'test2.xml')
        self.assertFalse(util.validateDocumentWithSchema(f2, SCHEMA_PATH))
 
#         SequenceTotalQuantity element is missing
# TODO: the error msg says that EarliestPriorityApplicationIdentification is expected: /Users/ad/pyton/projects/st26proto/authoringtool/sequencelistings/testData/test8.xml:42:0:ERROR:SCHEMASV:SCHEMAV_ELEMENT_CONTENT: Element 'SequenceData': This element is not expected. Expected is ( EarliestPriorityApplicationIdentification ).
        f8 = os.path.join(util.TEST_DATA_DIR_PATH, 'test8.xml')
        self.assertFalse(util.validateDocumentWithSchema(f8, SCHEMA_PATH))
       
#         seq 5 skipped sequence
        f10 = os.path.join(util.TEST_DATA_DIR_PATH, 'test10.xml')
        self.assertTrue(util.validateDocumentWithSchema(f10, SCHEMA_PATH))
        
# valid residues pattern: seq 1 - length 10 nuc
#                             seq 2 - length 4 aa
#                             seq 3 - all nuc symbols
#                             seq 4 - all aa symbols
#                             seq 5 - skip
        f10 = os.path.join(util.TEST_DATA_DIR_PATH, 'test10.xml')
        self.assertTrue(util.validateDocumentWithSchema(f10, SCHEMA_PATH))
        
# residues pattern: invalid length nuc seq 1 - length 4 nuc
        f11 = os.path.join(util.TEST_DATA_DIR_PATH, 'test11.xml')
        self.assertFalse(util.validateDocumentWithSchema(f11, SCHEMA_PATH))
        
# residues pattern: invalid length aa seq 2 - length 3 nuc
        f12 = os.path.join(util.TEST_DATA_DIR_PATH, 'test12.xml')
        self.assertFalse(util.validateDocumentWithSchema(f12, SCHEMA_PATH))
        
# residues pattern: invalid symbol nuc seq 3 - i
        f13 = os.path.join(util.TEST_DATA_DIR_PATH, 'test13.xml')
        self.assertFalse(util.validateDocumentWithSchema(f13, SCHEMA_PATH))
        
# residues pattern: invalid symbol aa seq 4 - i
        f14 = os.path.join(util.TEST_DATA_DIR_PATH, 'test14.xml')
        self.assertFalse(util.validateDocumentWithSchema(f14, SCHEMA_PATH))

# residues pattern: invalid symbol aa seq 5 - i
        f15 = os.path.join(util.TEST_DATA_DIR_PATH, 'test15.xml')
        self.assertFalse(util.validateDocumentWithSchema(f15, SCHEMA_PATH))
        
# invalid value SequenceTotalQuantity is 0
        f16 = os.path.join(util.TEST_DATA_DIR_PATH, 'test16.xml')
        self.assertFalse(util.validateDocumentWithSchema(f16, SCHEMA_PATH))
        
# invalid value SequenceTotalQuantity is xxx
        f17 = os.path.join(util.TEST_DATA_DIR_PATH, 'test17.xml')
        self.assertFalse(util.validateDocumentWithSchema(f17, SCHEMA_PATH))
