'''
Created on May 27, 2018

@author: ad
'''

import os, logging 
from lxml import etree 

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
# handler = logging.handlers.RotatingFileHandler(maxBytes=1000000)
# logger.addHandler(handler)
# currentDirectory = os.path.abspath(os.path.dirname(__file__))
# PROJECT_DIRECTORY = os.path.abspath(os.path.join(currentDirectory, os.pardir))

# TEST_DATA_DIR_PATH = os.path.join(PROJECT_DIRECTORY, 
#                                        'sequencelistings', 'testData')

# TEST_DATA_DIR_PATH = os.path.join(PROJECT_DIRECTORY, 
#                                        'schema', 'test_data')

def validateDocumentWithSchema(aFilePath, aSchemaPath):
    result = False
    xmlschema_doc = etree.parse(aSchemaPath)
    xmlschema = etree.XMLSchema(xmlschema_doc)
    
    try:
        doc = etree.parse(aFilePath)
#         at this point the input file was successfully parsed
        
        if xmlschema.validate(doc):
            result = True
        else:
            logger.error('\nfile: %s' % aFilePath)
            logger.error('\n%s' % xmlschema.error_log)
    except etree.XMLSyntaxError as syntErr:
        logger.error('\n%s\n%s' % (aFilePath, syntErr))
    
    return result 

