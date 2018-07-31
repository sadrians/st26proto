'''
Created on July 5, 2018

@author: ad
'''
import os
import re
import unittest
import util

class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test fixture.
            ::
                Test files:
                 annex_6_appendix_updated_2018_07_09.xml - reference valid seq list file
                 t1.xml - both ApplicationIdentification and ApplicantFileReference present
                 t2.xml - ApplicantFileReference missing
                 t3.xml - EarliestPriorityApplicationIdentification missing
                 t4.xml - ApplicantNameLatin missing
                 t5.xml - InventorName and InventorNameLatin missing
                 t6.xml - InventorNameLatin missing
                 t7.xml - both ApplicationIdentification and ApplicantFileReference missing
                 t8.xml - dtdVersion missing
                 t9.xml - fileName, softwareName, softwareVersion, productionDate missing
                 t10.xml - FilingDate of ApplicationIdentification missing
                 t11.xml - IPOfficeCode of ApplicationIdentification missing
                 t12.xml - ApplicationNumberText of ApplicationIdentification missing
                 t13.xml - languageCode of ApplicantName missing
                 t14.xml - InventionTitle missing
                 t15.xml - InventionTitle occurs twice
                 t16.xml - SequenceTotalQuantity missing
                 t17.xml - SequenceData missing
                 t18.xml - INSDSeq missing
                 t19.xml - INSDSeq_length missing
                 t20.xml - INSDSeq_moltype missing
                 t21.xml - INSDSeq_division missing
                 t22.xml - INSDSeq_feature-table missing
                 t23.xml - sequenceIDNumber missing
                 t24.xml - INSDSeq_other-seqids present
                 t25.xml - INSDSeq_other-seqids present twice
                 t26.xml - INSDSeqid missing
                 t27.xml - INSDFeature missing
                 t28.xml - INSDFeature_key missing
                 t29.xml - INSDFeature_location missing
                 t30.xml - INSDFeature_quals missing
                 t31.xml - INSDQualifier missing
                 t32.xml - INSDQualifier_name missing
                 t32a.xml - INSDQualifier_name is 'abc'
                 t33.xml - INSDQualifier_value missing
                 t34.xml - INSDSeq_sequence missing
                 t35.xml - IPOfficeCode of ApplicationIdentification empty
                 t36.xml - IPOfficeCode of ApplicationIdentification is sx
                 t37.xml - languageCode of ApplicantName empty
                 t38.xml - languageCode of ApplicantName xx
                 t39.xml - SequenceTotalQuantity empty
                 t40.xml - SequenceTotalQuantity 0
                 t41.xml - SequenceTotalQuantity is abc
                 t42.xml - sequenceIDNumber is empty
                 t43.xml - sequenceIDNumber is 0
                 t44.xml - sequenceIDNumber is abc
                 t45.xml - INSDSeq_length empty
                 t46.xml - INSDSeq_length is 0
                 t47.xml - INSDSeq_length is abc
                 t48.xml - INSDSeq_moltype empty
                 t49.xml - INSDSeq_moltype is PRT
                 t50.xml - INSDSeq_division empty
                 t51.xml - INSDSeq_division is xx
                 t51a.xml - INSDSeqid is 'pat|WO|2013999999|A1|123456'
                 t51b.xml - INSDSeqid is 'abc'
                 t52.xml - INSDFeature_key is empty
                 t53.xml - INSDFeature_key is xx
                 t54.xml - INSDFeature_key is misc_feature
                 t55.xml - INSDSeq_sequence is empty
                 t56.xml - INSDSeq_sequence is shorter than 10 nuc
                 t57.xml - INSDSeq_sequence contains u
                 t58.xml - INSDSeq_sequence contains G
                 t59.xml - INSDSeq_sequence is shorter than 4 aa
                 t60.xml - sequenceIDNumber is not unique
                 t61.xml - FilingDate of ApplicationIdentification empty
                 t62.xml - FilingDate of ApplicationIdentification is 2015-04-32
                 t63.xml - FilingDate of ApplicationIdentification is Not assigned yet
                 t64.xml - dtdVersion is 1.2
                 t65.xml - INSDQualifier_value is empty
                 t66.xml - INSDQualifier_value has more than 1000 chars
                 t66a.xml - INSDQualifier_value is ' !#$%&amp;()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~' (i.e., only chars from the char set defined in ST.26 par. 40(b))
                 t67.xml - INSDSeq_sequence is empty (nuc)
                 t68.xml - INSDSeq_sequence has less than 10 nuc
                 t69.xml - INSDSeq_sequence contains i
                 t69a.xml - INSDSeq_sequence contains all allowed nuc (seq 1), all allowed aa (seq 2), 000 (seq 3)
                 t70.xml - INSDSeq_sequence is empty (prt)
                 t71.xml - INSDSeq_sequence has less than 4 aa
                 t72.xml - INSDSeq_sequence contains *
                 t73.xml - seq 2 skip
                 t74.xml - INSDSeq_sequence is empty (skip)
                 t75.xml - extraneous element ExtraneousElementTest
                 t76.xml - missing closing tag ApplicantFileReference
                 t77.xml - typo in tag ApplicantNamex
                 t78.xml - no root (element ST26SequenceListing missing)
                 t79.xml - attribute softwareName not quoted
        """
        testFileNames = ['annex_6_appendix_updated_2018_07_09.xml', # reference valid seq list file
                         't1.xml', # both ApplicationIdentification and ApplicantFileReference present
                         't2.xml', # ApplicantFileReference missing
                         't3.xml', # EarliestPriorityApplicationIdentification missing
                         't4.xml', # ApplicantNameLatin missing
                         't5.xml', # InventorName and InventorNameLatin missing
                         't6.xml', # InventorNameLatin missing
                         't7.xml', # both ApplicationIdentification and ApplicantFileReference missing
                         't8.xml', # dtdVersion missing
                         't9.xml', # fileName, softwareName, softwareVersion, productionDate missing
                         't10.xml', # FilingDate of ApplicationIdentification missing
                         't11.xml', # IPOfficeCode of ApplicationIdentification missing
                         't12.xml', # ApplicationNumberText of ApplicationIdentification missing
                         't13.xml', # languageCode of ApplicantName missing
                         't14.xml', # InventionTitle missing
                         't15.xml', # InventionTitle occurs twice
                         't16.xml', # SequenceTotalQuantity missing
                         't17.xml', # SequenceData missing
                         't18.xml', # INSDSeq missing
                         't19.xml', # INSDSeq_length missing
                         't20.xml', # INSDSeq_moltype missing
                         't21.xml', # INSDSeq_division missing
                         't22.xml', # INSDSeq_feature-table missing
                         't23.xml', # sequenceIDNumber missing
                         't24.xml', # INSDSeq_other-seqids present
                         't25.xml', # INSDSeq_other-seqids present twice
                         't26.xml', # INSDSeqid missing
                         't27.xml', # INSDFeature missing
                         't28.xml', # INSDFeature_key missing
                         't29.xml', # INSDFeature_location missing
                         't30.xml', # INSDFeature_quals missing
                         't31.xml', # INSDQualifier missing
                         't32.xml', # INSDQualifier_name missing
                         't32a.xml', # INSDQualifier_name is 'abc'
                         't33.xml', # INSDQualifier_value missing
                         't34.xml', # INSDSeq_sequence missing
                         't35.xml', # IPOfficeCode of ApplicationIdentification empty
                         't36.xml', # IPOfficeCode of ApplicationIdentification is 'sx'
                         't37.xml', # languageCode of ApplicantName empty
                         't38.xml', # languageCode of ApplicantName 'xx'
                         't39.xml', # SequenceTotalQuantity empty
                         't40.xml', # SequenceTotalQuantity 0
                         't41.xml', # SequenceTotalQuantity is 'abc'
                         't42.xml', # sequenceIDNumber is empty
                         't43.xml', # sequenceIDNumber is '0'
                         't44.xml', # sequenceIDNumber is 'abc'
                         't45.xml', # INSDSeq_length empty
                         't46.xml', # INSDSeq_length is '0'
                         't47.xml', # INSDSeq_length is 'abc'
                         't48.xml', # INSDSeq_moltype empty
                         't49.xml', # INSDSeq_moltype is 'PRT'
                         't50.xml', # INSDSeq_division empty
                         't51.xml', # INSDSeq_division is 'xx'
                         't51a.xml', #INSDSeqid is 'pat|WO|2013999999|A1|123456'
                         't51b.xml', # INSDSeqid is 'abc'
                         't52.xml', # INSDFeature_key is empty
                         't53.xml', # INSDFeature_key is 'xx'
                         't54.xml', # INSDFeature_key is 'misc_feature'
                         't55.xml', # INSDSeq_sequence is empty
                         't56.xml', # INSDSeq_sequence is shorter than 10 nuc
                         't57.xml', # INSDSeq_sequence contains 'u'
                         't58.xml', # INSDSeq_sequence contains 'G'
                         't59.xml', # INSDSeq_sequence is shorter than 4 aa
                         't60.xml', # sequenceIDNumber is not unique
                         't61.xml', # FilingDate of ApplicationIdentification empty
                         't62.xml', # FilingDate of ApplicationIdentification is '2015-04-32'
                         't63.xml', # FilingDate of ApplicationIdentification is 'Not assigned yet'
                         't64.xml', # dtdVersion is '1.2'
                         't65.xml', # INSDQualifier_value is empty
                         't66.xml', # INSDQualifier_value has more than 1000 chars
                         't66a.xml', # INSDQualifier_value is ' !#$%&amp;()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~' (i.e., only chars from the char set defined in ST.26 par. 40(b))
                         't67.xml', # INSDSeq_sequence is empty (nuc)
                         't68.xml', # INSDSeq_sequence has less than 10 nuc
                         't69.xml', # INSDSeq_sequence contains i
                         't69a.xml', # INSDSeq_sequence contains all allowed nuc (seq 1), all allowed aa (seq 2), 000 (seq 3)
                         't70.xml', # INSDSeq_sequence is empty (prt)
                         't71.xml', # INSDSeq_sequence has less than 4 aa
                         't72.xml', # INSDSeq_sequence contains '*'
                         't73.xml', # seq 2 skip
                         't74.xml', # INSDSeq_sequence is empty (skip)
                         't75.xml', # extraneous element ExtraneousElementTest
                         't76.xml', # missing closing tag ApplicantFileReference
                         't77.xml', # typo in tag ApplicantNamex
                         't78.xml', # no root (element ST26SequenceListing missing)
                         't79.xml', # attribute softwareName not quoted

                         # 't72.xml', # INSDQualifier_value contains *

                         ]

        cls.testFiles = {fn: os.path.join(util.XTEST_DATA_DIR_PATH, fn) for fn in testFileNames}

# ==============================================
# 1 TEST STRUCTURE
# ==============================================
    def test_validateDocumentWithSchemax(self):

        """Validation ok for the reference sample file (ST.26 annex 6, appendix).

            - Test file: annex_6_appendix_updated_2018_07_09.xml
        """

        res = util.validateDocumentWithSchema(self.testFiles['annex_6_appendix_updated_2018_07_09.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema1(self):
        """Validation ok when both ApplicationIdentification and ApplicantFileReference are present.

            - Test file: t1.xml
        """
        f1 = self.testFiles['t1.xml']
        res = util.validateDocumentWithSchema(self.testFiles['t1.xml'], util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema2(self):
        """Validation ok when ApplicantFileReference missing.

            - Test file: t2.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t2.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema3(self):
        """Validation ok when EarliestPriorityApplicationIdentification missing.

            - Test file: t3.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t3.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema4(self):
        """Validation ok when ApplicantNameLatin missing.

            - Test file: t4.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t4.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema5(self):
        """Validation ok when InventorName and InventorNameLatin missing.

            - Test file: t5.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t5.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema6(self):
        """Validation ok when InventorNameLatin missing.

            - Test file: t6.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t6.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema7(self):
        """Validation fails when both ApplicationIdentification and ApplicantFileReference missing.

            - Test file: t7.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t7.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'EarliestPriorityApplicationIdentification': This element is not expected. Expected is one of ( ApplicationIdentification, ApplicantFileReference )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema8(self):
        """Validation fails when dtdVersion missing.

            - Test file: t8.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t8.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'ST26SequenceListing': The attribute 'dtdVersion' is required but missing."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema9(self):
        """Validation ok when fileName, softwareName, softwareVersion, productionDate missing.

            - Test file: t9.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t9.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema10(self):
        """Validation ok when FilingDate of ApplicationIdentification missing.

            - Test file: t10.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t10.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema11(self):
        """Validation fails when IPOfficeCode of ApplicationIdentification missing.

            - Test file: t11.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t11.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'ApplicationNumberText': This element is not expected. Expected is ( IPOfficeCode )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema12(self):
        """Validation fails when ApplicationNumberText of ApplicationIdentification missing.

            - Test file: t12.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t12.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'FilingDate': This element is not expected. Expected is ( ApplicationNumberText )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema13(self):
        """Validation fails when languageCode of ApplicantName missing.

            - Test file: t13.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t13.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'ApplicantName': The attribute 'languageCode' is required but missing."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema14(self):
        """Validation fails when InventionTitle missing.

            - Test file: t14.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t14.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'SequenceTotalQuantity': This element is not expected. Expected is ( InventionTitle )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema15(self):
        """Validation ok when InventionTitle occurs twice.

            - Test file: t15.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t15.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema16(self):
        """Validation fails when SequenceTotalQuantity missing.

            - Test file: t16.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t16.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'SequenceData': This element is not expected. Expected is one of ( InventionTitle, SequenceTotalQuantity )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema17(self):
        """Validation fails when SequenceData missing.

            - Test file: t17.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t17.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'ST26SequenceListing': Missing child element(s). Expected is ( SequenceData )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema18(self):
        """Validation fails when INSDSeq missing.

            - Test file: t18.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t18.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'SequenceData': Missing child element(s). Expected is ( INSDSeq )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema19(self):
        """Validation fails when INSDSeq_length missing.

            - Test file: t19.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t19.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'INSDSeq_moltype': This element is not expected. Expected is ( INSDSeq_length )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema20(self):
        """Validation fails when INSDSeq_moltype missing.

            - Test file: t20.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t20.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'INSDSeq_division': This element is not expected. Expected is ( INSDSeq_moltype )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema21(self):
        """Validation fails when INSDSeq_division missing.

            - Test file: t21.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t21.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'INSDSeq_feature-table': This element is not expected. Expected is ( INSDSeq_division )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema22(self):
        """Validation ok when INSDSeq_feature-table missing.

            - Test file: t22.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t22.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema23(self):
        """Validation fails when sequenceIDNumber missing.

            - Test file: t23.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t23.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'SequenceData': The attribute 'sequenceIDNumber' is required but missing."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema24(self):
        """Validation ok when INSDSeq_other-seqids present.

            - Test file: t24.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t24.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema25(self):
        """Validation fails when INSDSeq_other-seqids occurs twice.

            - Test file: t25.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t25.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'INSDSeq_other-seqids': This element is not expected. Expected is one of ( INSDSeq_feature-table, INSDSeq_sequence )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema26(self):
        """Validation fails when INSDSeqid missing.

            - Test file: t26.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t26.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'INSDSeq_other-seqids': Missing child element(s). Expected is ( INSDSeqid )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema27(self):
        """Validation fails when INSDFeature missing.

            - Test file: t27.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t27.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'INSDSeq_feature-table': Missing child element(s). Expected is ( INSDFeature )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema28(self):
        """Validation fails when INSDFeature_key missing.

            - Test file: t28.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t28.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'INSDFeature_location': This element is not expected. Expected is ( INSDFeature_key )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema29(self):
        """Validation fails when INSDFeature_location missing.

            - Test file: t29.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t29.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'INSDFeature_quals': This element is not expected. Expected is ( INSDFeature_location )."
        self.assertIn(msg, str(res['schemaError']))

    # TODO: This test may need to be rewritten after multiplicity of INSDFeature_quals is clarified
    def test_validateDocumentWithSchema30(self):
        """Validation fails when INSDFeature_quals missing.

            - Test file: t30.xml
        """
        #Currently it does not fail bc element is defined as optional.
        res = util.validateDocumentWithSchema(self.testFiles['t30.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        # msg = r"?????"
        # self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema31(self):
        """Validation fails when INSDQualifier missing.

            - Test file: t31.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t31.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'INSDFeature_quals': Missing child element(s). Expected is ( INSDQualifier )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema32(self):
        """Validation fails when INSDQualifier_name missing.

            - Test file: t32.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t32.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'INSDQualifier_value': This element is not expected. Expected is ( INSDQualifier_name )."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema32a(self):
        """Validation fails when INSDQualifier_name is 'abc'.

            - Test file: t32a.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t32a.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDQualifier_name': [facet 'enumeration'] The value 'abc' is not an element of the set {'allele', 'anticodon', 'bound_moiety', 'cell_line', 'cell_type', 'chromosome', 'clone', 'clone_lib', 'codon_start', 'collected_by', 'collection_date', 'compare', 'cultivar', 'dev_stage', 'direction', 'EC_number', 'ecotype', 'environmental_sample', 'exception', 'frequency', 'function', 'gene', 'gene_synonym', 'germline', 'haplogroup', 'haplotype', 'host', 'identified_by', 'isolate', 'isolation_source', 'lab_host', 'lat_lon', 'macronuclear', 'map', 'mating_type', 'mobile_element_type', 'mod_base', 'mol_type', 'ncRNA_class', 'note', 'number', 'operon', 'organelle', 'organism', 'PCR_primers', 'phenotype', 'plasmid', 'pop_variant', 'product', 'protein_id', 'proviral', 'pseudo', 'pseudogene', 'rearranged', 'recombination_class', 'regulatory_class', 'replace', 'ribosomal_slippage', 'rpt_family', 'rpt_type', 'rpt_unit_range', 'rpt_unit_seq', 'satellite', 'segment', 'serotype', 'serovar', 'sex', 'standard_name', 'strain', 'sub_clone', 'sub_species', 'sub_strain', 'tag_peptide', 'tissue_lib', 'tissue_type', 'transl_except', 'transl_table', 'translation', 'trans_splicing', 'variety', 'MOL_TYPE', 'NOTE', 'ORGANISM'}."
        self.assertIn(msg0, str(res['schemaError']))
        msg1 = r"Element 'INSDQualifier_name': 'abc' is not a valid value of the atomic type 'qualifierNameValues'."
        self.assertIn(msg1, str(res['schemaError']))

    def test_validateDocumentWithSchema33(self):
        """Validation ok when INSDQualifier_value missing.

            - Test file: t33.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t33.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema34(self):
        """Validation fails when INSDSeq_sequence missing.

            - Test file: t34.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t34.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'INSDSeq': Missing child element(s). Expected is ( INSDSeq_sequence )."
        self.assertIn(msg, str(res['schemaError']))

# ==============================================
# 2 TEST VALUES
# ==============================================
    def test_validateDocumentWithSchema35(self):
        """Validation fails when IPOfficeCode of ApplicationIdentification empty.

            - Test file: t35.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t35.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'IPOfficeCode': [facet 'enumeration'] The value '' is not an element of the set {'AF', 'OA', "
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'IPOfficeCode': '' is not a valid value of the atomic type 'IPOfficeCodeValues'."
        self.assertIn(msg1, str(res['schemaError'][1]))
        # print res['schemaError'][1]

    def test_validateDocumentWithSchema36(self):
        """Validation fails when IPOfficeCode of ApplicationIdentification is 'sx'.

            - Test file: t36.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t36.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'IPOfficeCode': [facet 'enumeration'] The value 'sx' is not an element of the set {'AF', 'OA', "
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'IPOfficeCode': 'sx' is not a valid value of the atomic type 'IPOfficeCodeValues'."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema37(self):
        """Validation fails when languageCode of ApplicantName is empty.

            - Test file: t37.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t37.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'ApplicantName', attribute 'languageCode': [facet 'enumeration'] The value '' is not an element of the set {'aa', 'ab', 'af', "
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'ApplicantName', attribute 'languageCode': '' is not a valid value of the atomic type 'languageCodeValues'."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema38(self):
        """Validation fails when languageCode of ApplicantName is empty.

            - Test file: t38.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t38.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'ApplicantName', attribute 'languageCode': [facet 'enumeration'] The value 'xx' is not an element of the set {'aa', 'ab', 'af', "
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'ApplicantName', attribute 'languageCode': 'xx' is not a valid value of the atomic type 'languageCodeValues'."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema39(self):
        """Validation fails when SequenceTotalQuantity is empty.

            - Test file: t39.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t39.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'SequenceTotalQuantity': '' is not a valid value of the atomic type 'xs:positiveInteger'."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema40(self):
        """Validation fails when SequenceTotalQuantity is 0.

            - Test file: t40.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t40.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'SequenceTotalQuantity': '0' is not a valid value of the atomic type 'xs:positiveInteger'."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema41(self):
        """Validation fails when SequenceTotalQuantity is empty.

            - Test file: t41.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t41.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg = r"Element 'SequenceTotalQuantity': 'abc' is not a valid value of the atomic type 'xs:positiveInteger'."
        self.assertIn(msg, str(res['schemaError']))

    def test_validateDocumentWithSchema42(self):
        """Validation fails when sequenceIDNumber is empty.

            - Test file: t42.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t42.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'SequenceData', attribute 'sequenceIDNumber': '' is not a valid value of the atomic type 'xs:positiveInteger'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'SequenceData', attribute 'sequenceIDNumber': Warning: No precomputed value available, the value was either invalid or something strange happend."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema43(self):
        """Validation fails when sequenceIDNumber is empty.

            - Test file: t43.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t43.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'SequenceData', attribute 'sequenceIDNumber': '0' is not a valid value of the atomic type 'xs:positiveInteger'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'SequenceData', attribute 'sequenceIDNumber': Warning: No precomputed value available, the value was either invalid or something strange happend."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema44(self):
        """Validation fails when sequenceIDNumber is 'abc'.

            - Test file: t44.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t44.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'SequenceData', attribute 'sequenceIDNumber': 'abc' is not a valid value of the atomic type 'xs:positiveInteger'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'SequenceData', attribute 'sequenceIDNumber': Warning: No precomputed value available, the value was either invalid or something strange happend."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema45(self):
        """Validation ok when INSDSeq_length is empty.

            - Test file: t45.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t45.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema46(self):
        """Validation fails when INSDSeq_length is 0.

            - Test file: t46.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t46.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_length': '0' is not a valid value of the local union type."
        self.assertIn(msg0, str(res['schemaError'][0]))

    def test_validateDocumentWithSchema47(self):
        """Validation fails when INSDSeq_length is 'abc'.

            - Test file: t47.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t47.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_length': 'abc' is not a valid value of the local union type."
        self.assertIn(msg0, str(res['schemaError'][0]))

    def test_validateDocumentWithSchema48(self):
        """Validation ok when INSDSeq_moltype is empty.

            - Test file: t48.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t48.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema49(self):
        """Validation fails when INSDSeq_moltype is 'PRT'.

            - Test file: t49.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t49.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_moltype': [facet 'pattern'] The value 'PRT' is not accepted by the pattern 'DNA|RNA|AA|.{0}'."
        self.assertIn(msg0, str(res['schemaError'][0]))

    def test_validateDocumentWithSchema50(self):
        """Validation ok when INSDSeq_division is empty.

            - Test file: t50.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t50.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema51(self):
        """Validation fails when INSDSeq_division is 'xx'.

            - Test file: t51.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t51.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_division': [facet 'pattern'] The value 'xx' is not accepted by the pattern 'PAT|.{0}'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_division': 'xx' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema51a(self):
        """Validation ok when INSDSeq_other-seqids is 'pat|WO|2013999999|A1|123456'.
        Pattern: "pat\|[A-Z]{2}\|[A-Z0-9]+\|[A-Z][0-9]\|[1-9][0-9]*".

            - Test file: t51a.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t51a.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema51b(self):
        """Validation fails when INSDSeq_other-seqids is 'abc'.

            - Test file: t51b.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t51b.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeqid': [facet 'pattern'] The value 'abc' is not accepted by the pattern 'pat\|[A-Z]{2}\|[A-Z0-9]+\|[A-Z][0-9]\|[1-9][0-9]*'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeqid': 'abc' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema52(self):
        """Validation fails when INSDFeature_key is empty.

            - Test file: t52.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t52.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDFeature_key': [facet 'enumeration'] The value '' is not an element of the set {'allele', 'attenuator', 'C_region', 'CAAT_signal', 'CDS', 'conflict', 'D-loop', 'D_segment', 'enhancer', 'exon', 'GC_signal', 'gene', 'iDNA', 'intron', 'J_segment', 'LTR', 'mat_peptide', 'misc_binding', 'misc_difference', 'misc_feature', 'misc_recomb', 'misc_RNA', 'misc_signal', 'misc_structure', 'modified_base', 'mRNA', 'mutation', 'N_region', 'old_sequence', 'polyA_signal', 'polyA_site', 'precursor_RNA', 'prim_transcript', 'primer_bind', 'promoter', 'protein_bind', 'RBS', 'repeat_region', 'repeat_unit', 'rep_origin', 'rRNA', 'S_region', 'satellite', 'scRNA', 'sig_peptide', 'snRNA', 'source', 'stem_loop', 'STS', 'TATA_signal', 'terminator', 'transit_peptide', 'tRNA', 'unsure', 'V_region', 'V_segment', 'variation', '3'clip', '3'UTR', '5'clip', '5'UTR', '-10_signal', '-35_signal', 'ACT_SITE', 'BINDING', 'CA_BIND', 'CARBOHYD', 'CHAIN', 'COILED', 'COMPBIAS', 'CONFLICT', 'CROSSLNK', 'DISULFID', 'DNA_BIND', 'DOMAIN', 'HELIX', 'INIT_MET', 'INTRAMEM', 'LIPID', 'METAL', 'MOD_RES', 'MOTIF', 'MUTAGEN', 'NON_STD', 'NON_TER', 'NP_BIND', 'PEPTIDE', 'PROPEP', 'REGION', 'REPEAT', 'SIGNAL', 'SITE', 'SOURCE', 'STRAND', 'TOPO_DOM', 'TRANSMEM', 'TRANSIT', 'TURN', 'UNSURE', 'VARIANT', 'VAR_SEQ', 'ZN_FING'}."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDFeature_key': '' is not a valid value of the atomic type 'featureKeyValues'."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema53(self):
        """Validation fails when INSDFeature_key is 'xx'.

            - Test file: t53.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t53.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDFeature_key': [facet 'enumeration'] The value 'xx' is not an element of the set {'allele', 'attenuator', 'C_region', 'CAAT_signal', 'CDS', 'conflict', 'D-loop', 'D_segment', 'enhancer', 'exon', 'GC_signal', 'gene', 'iDNA', 'intron', 'J_segment', 'LTR', 'mat_peptide', 'misc_binding', 'misc_difference', 'misc_feature', 'misc_recomb', 'misc_RNA', 'misc_signal', 'misc_structure', 'modified_base', 'mRNA', 'mutation', 'N_region', 'old_sequence', 'polyA_signal', 'polyA_site', 'precursor_RNA', 'prim_transcript', 'primer_bind', 'promoter', 'protein_bind', 'RBS', 'repeat_region', 'repeat_unit', 'rep_origin', 'rRNA', 'S_region', 'satellite', 'scRNA', 'sig_peptide', 'snRNA', 'source', 'stem_loop', 'STS', 'TATA_signal', 'terminator', 'transit_peptide', 'tRNA', 'unsure', 'V_region', 'V_segment', 'variation', '3'clip', '3'UTR', '5'clip', '5'UTR', '-10_signal', '-35_signal', 'ACT_SITE', 'BINDING', 'CA_BIND', 'CARBOHYD', 'CHAIN', 'COILED', 'COMPBIAS', 'CONFLICT', 'CROSSLNK', 'DISULFID', 'DNA_BIND', 'DOMAIN', 'HELIX', 'INIT_MET', 'INTRAMEM', 'LIPID', 'METAL', 'MOD_RES', 'MOTIF', 'MUTAGEN', 'NON_STD', 'NON_TER', 'NP_BIND', 'PEPTIDE', 'PROPEP', 'REGION', 'REPEAT', 'SIGNAL', 'SITE', 'SOURCE', 'STRAND', 'TOPO_DOM', 'TRANSMEM', 'TRANSIT', 'TURN', 'UNSURE', 'VARIANT', 'VAR_SEQ', 'ZN_FING'}."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDFeature_key': 'xx' is not a valid value of the atomic type 'featureKeyValues'."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema54(self):
        """Validation ok when INSDFeature_key is 'misc_feature' even though the seq is a prt.

            - Test file: t54.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t54.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema55(self):
        """Validation fails when INSDSeq_sequence is empty.

            - Test file: t55.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t55.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value '' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))

        msg1 = r"Element 'INSDSeq_sequence': '' is not a valid value of the local atomic type."
        # print msg1
        # print res['schemaError'][1]
        self.assertIn(msg1, str(res['schemaError'][1]))


    def test_validateDocumentWithSchema56(self):
        """Validation fails when INSDSeq_sequence is shorter than 10 nuc.

            - Test file: t56.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t56.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value 'atgact' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_sequence': 'atgact' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema57(self):
        """Validation fails when INSDSeq_sequence contains 'u'.

            - Test file: t57.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t57.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value 'atuacttgca' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_sequence': 'atuacttgca' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema58(self):
        """Validation fails when INSDSeq_sequence contains 'u'.

            - Test file: t58.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t58.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value 'atGacttgca' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_sequence': 'atGacttgca' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema59(self):
        """Validation fails when INSDSeq_sequence is shorter than 4 aa.

            - Test file: t59.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t59.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value 'MSR' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_sequence': 'MSR' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema60(self):
        """Validation fails when sequenceIDNumber is not unique.

            - Test file: t60.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t60.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'SequenceData': Duplicate key-sequence ['2'] in unique identity-constraint 'uniqueSequenceIDNumber'."
        self.assertIn(msg0, str(res['schemaError'][0]))

    def test_validateDocumentWithSchema61(self):
        """Validation fails when FilingDate of ApplicationIdentification empty.

            - Test file: t61.xml

        """
        res = util.validateDocumentWithSchema(self.testFiles['t61.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'FilingDate': '' is not a valid value of the atomic type 'xs:date'."
        self.assertIn(msg0, str(res['schemaError'][0]))

    def test_validateDocumentWithSchema62(self):
        """Validation fails when FilingDate of ApplicationIdentification is '2015-04-32.'

            - Test file: t62.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t62.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'FilingDate': '2015-04-32' is not a valid value of the atomic type 'xs:date'."
        self.assertIn(msg0, str(res['schemaError'][0]))

    def test_validateDocumentWithSchema63(self):
        """Validation fails when FilingDate of ApplicationIdentification is 'Not assigned yet'.

            - Test file: t63.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t63.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'FilingDate': 'Not assigned yet' is not a valid value of the atomic type 'xs:date'."
        self.assertIn(msg0, str(res['schemaError'][0]))

    def test_validateDocumentWithSchema64(self):
        """Validation fails when dtdVersion is '1.2'.

            - Test file: t64.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t64.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'ST26SequenceListing', attribute 'dtdVersion': [facet 'pattern'] The value '1.2' is not accepted by the pattern 'V[0-9]+_[0-9]+'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'ST26SequenceListing', attribute 'dtdVersion': '1.2' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema65(self):
        """Validation ok when INSDQualifier_value is empty.

            - Test file: t65.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t65.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema66(self):
        """Validation fails when INSDQualifier_value exceeds 1000 chars.

            - Test file: t66.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t66.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDQualifier_value': [facet 'maxLength'] The value has a length of '1011'; this exceeds the allowed maximum length of '1000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDQualifier_value': 'insert MTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRSMTRS' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema66a(self):
        """Validation ok when INSDQualifier_value is ' !#$%&amp;()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~' (e.g., only chars from the char set defined in ST.26 par. 40(b)).

            - Test file: t66a.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t66a.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema67(self):
        """Validation fails when INSDSeq_sequence is empty (nuc).

            - Test file: t67.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t67.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value '' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_sequence': '' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema68(self):
        """Validation fails when INSDSeq_sequence has less than 10 nuc.

            - Test file: t68.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t68.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value 'atgac' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_sequence': 'atgac' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema69(self):
        """Validation fails when INSDSeq_sequence contains i.

            - Test file: t69.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t69.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value 'aigacttgca' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_sequence': 'aigacttgca' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema69a(self):
        """Validation ok when INSDSeq_sequence contains all allowed nuc (seq 1), all allowed aa (seq 2), 000 (seq 3).

            - Test file: t69a.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t69a.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema70(self):
        """Validation fails when INSDSeq_sequence is empty (prt).

            - Test file: t70.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t70.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value '' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_sequence': '' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema71(self):
        """Validation fails when INSDSeq_sequence has less than 4 aa.

            - Test file: t71.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t71.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value 'MSR' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_sequence': 'MSR' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema72(self):
        """Validation fails when INSDSeq_sequence contains '*'.

            - Test file: t72.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t72.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value 'MSRK*' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_sequence': 'MSRK*' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema73(self):
        """Validation ok when seq 2 skip.

            - Test file: t73.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t73.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

    def test_validateDocumentWithSchema74(self):
        """Validation fails when INSDSeq_sequence is empty (skip).

            - Test file: t74.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t74.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'INSDSeq_sequence': [facet 'pattern'] The value '' is not accepted by the pattern '[a,c,g,t,m,r,w,s,y,k,v,h,d,b,n]{10,}|[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}|000'."
        self.assertIn(msg0, str(res['schemaError'][0]))
        msg1 = r"Element 'INSDSeq_sequence': '' is not a valid value of the local atomic type."
        self.assertIn(msg1, str(res['schemaError'][1]))

    def test_validateDocumentWithSchema75(self):
        """Validation fails when ExtraneousElementTest present.

            - Test file: t75.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t75.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        msg0 = r"Element 'ExtraneousElementTest': This element is not expected. Expected is ( SequenceData )."
        self.assertIn(msg0, str(res['schemaError'][0]))

# ==============================================
# 3 TEST SYNTAX (WELL FORMED)
# ==============================================
    def test_validateDocumentWithSchema76(self):
        """Parsing fails when missing closing tag ApplicantFileReference.

            - Test file: t76.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t76.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['schemaError'])
        msg0 = r"Opening and ending tag mismatch: ApplicantFileReference line 12 and ST26SequenceListing, line 85, column 23 (line 85)"
        self.assertEqual(msg0, str(res['parserError']))

    def test_validateDocumentWithSchema77(self):
        """Parsing fails when typo in tag ApplicantNamex.

            - Test file: t77.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t77.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['schemaError'])
        msg0 = r"Opening and ending tag mismatch: ApplicantNamex line 20 and ApplicantName, line 22, column 34 (line 22)"
        self.assertEqual(msg0, str(res['parserError']))

    def test_validateDocumentWithSchema78(self):
        """Parsing fails when no root (ST26SequenceListing missing).

            - Test file: t78.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t78.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['schemaError'])
        msg0 = r"Extra content at the end of the document, line 10, column 5 (line 10)"
        self.assertEqual(msg0, str(res['parserError']))

    def test_validateDocumentWithSchema79(self):
        """Parsing fails when attribute softwareName not quoted.

            - Test file: t79.xml
        """
        res = util.validateDocumentWithSchema(self.testFiles['t79.xml'],
                                              util.XML_SCHEMA_PATH)
        self.assertIsNone(res['schemaError'])
        msg0 = 'AttValue: " or \' expected, line 5, column 35 (line 5)'
        self.assertEqual(msg0, str(res['parserError']))

# ==============================================
# 4 TEST CHAR SET specified in ST.26 par.40(b) (e.g., subset of Basic Latin)
# ==============================================

    def test_charSet(self):
        """
        Test the char set currently defined in ST.26 par. 40(b) and Annex IV.
        ::
            Regex: ur'^[\u0020\u0021\u0023-\u0026\u0028-\u003B\u003D\u003F-\u007E]+$'
            Test strings:
                s1 = ' !#$%&()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
                s2 = 'abc'
                s3 = 'a & b'
                s4 = '<1..4'
                s5 = '1..>4'
                s6 = "To 5' end oxygene"
                s7 = 'Test for " - quotation mark char.'
                s8 = ur'abc\u00A9' #copyright sign &copy;
                s9 = ur'\u003C1..4'
                s10 = ur'1..\u003E4'
                s11 = ur"To 5\u0027 end oxygen"
                s12 = ur'Test for \u0022 - quotation mark char.'
                s13 = "3'UTR"
                s14 = ur'3\u0027UTR'
            Test result:
                s1 - s3 - match ok
                s4 - s14 mismatch
        """
        pattern_current = re.compile(ur'^[\u0020\u0021\u0023-\u0026\u0028-\u003B\u003D\u003F-\u007E]+$')

        s1 = ' !#$%&()*+,-./0123456789:;=?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
        s2 = 'abc'
        s3 = 'a & b'
        s4 = '<1..4'
        s5 = '1..>4'
        s6 = "The region at the 3' end of a mature transcript is not translated."
        s7 = 'Test for " - quotation mark char.'
        s8 = ur'abc\u00A9' #copyright sign &copy;
        s9 = ur'\u003C1..4'
        s10 = ur'1..\u003E4'
        s11 = ur"To 5\u0027 end oxygen"
        s12 = ur'Test for \u0022 - quotation mark char.'
        s13 = "3'UTR"
        s14 = ur'3\u0027UTR'

        self.assertEqual(s1, pattern_current.match(s1).group())
        self.assertEqual('abc', pattern_current.match(s2).group())
        self.assertEqual('a & b', pattern_current.match(s3).group())

        for s in [s4, s5, s6, s7, s8, s9, s10, s11, s12, s13, s14]:
            self.assertIsNone(pattern_current.match(s))


if __name__ == '__main__':
    unittest.main()