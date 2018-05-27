'''
Created on May 27, 2018

@author: ad
'''
import django
django.setup()

from django.test import TestCase

import os 
# from unittest import TestCase
import client 
from sequencelistings import util

SCHEMA_PATH = os.path.join(util.PROJECT_DIRECTORY, 'schema', 'xsd', 'st26.xsd')

class SchemaTests(TestCase):
    
    def getTestFilePath(self, aFileName):
        return os.path.join(util.TEST_DATA_DIR_PATH, aFileName)
    
    def test_validateDocumentWithSchema(self):
        """
        Test that xml sequence listing files are correctly validated 
        against the schema.
        """
#         print 'Running %s ...' % getName()
        print util.PROJECT_DIRECTORY
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
        f2 = os.path.join(util.TEST_DATA_DIR_PATH, 'test2.xml')
        self.assertTrue(util.validateDocumentWithSchema(f2, SCHEMA_PATH))
 
#         SequenceTotalQuantity element is missing
# TODO: the error msg says that EarliestPriorityApplicationIdentification is expected: /Users/ad/pyton/projects/st26proto/authoringtool/sequencelistings/testData/test8.xml:42:0:ERROR:SCHEMASV:SCHEMAV_ELEMENT_CONTENT: Element 'SequenceData': This element is not expected. Expected is ( EarliestPriorityApplicationIdentification ).
        f8 = os.path.join(util.TEST_DATA_DIR_PATH, 'test8.xml')
        self.assertFalse(util.validateDocumentWithSchema(f8, SCHEMA_PATH))
       
#         skipped sequences
        f9 = os.path.join(util.TEST_DATA_DIR_PATH, 'test9.xml')
        self.assertTrue(util.validateDocumentWithSchema(f9, SCHEMA_PATH))
