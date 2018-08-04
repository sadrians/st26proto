from unittest import TestCase
import inspect
import os

from tests import SequenceListingFixture
import util

def getName():
    return inspect.stack()[1][3]

class UtilTests(TestCase):
    def setUp(self):
        self.sequenceListingFixture = SequenceListingFixture()

    def tearDown(self):
        TestCase.tearDown(self)

    def test_rangeFromString(self):
        """
        Test that range is correctly returned.
        """
        print 'Running %s ...' % getName()

        s1 = 'ra(1,11,2)'
        s2 = 'r(1,11,2)'
        #         print util.rangeFromString(s2)
        self.assertEqual([1 ,3 ,5 ,7 ,9], util.rangeFromString(s1))
        self.assertEqual(None, util.rangeFromString(s2))

    def test_expandFormula(self):
        """
        Test that a formula of type MARRST(ATWQ)2..9TFSRA is correctly expanded.
        """
        print 'Running %s ...' % getName()

        self.assertEqual('abc', util.expandFormula('abc'))
        self.assertEqual('abcddd', util.expandFormula('abc(d)3'))
        self.assertEqual('abcdededede', util.expandFormula('abc(de)4'))
        self.assertEqual('abcdedededefg', util.expandFormula('abc(de)4fg'))
        self.assertEqual('abcdededededede', util.expandFormula('abc(de)2..6'))
        self.assertEqual('abcdedededededefg', util.expandFormula('abc(de)2..6fg'))
        self.assertEqual('ab(c', util.expandFormula('ab(c'))
        self.assertEqual('a(b9c', util.expandFormula('a(b9c'))

    def test_helper_generateXml(self):
        print 'Running %s ...' % getName()

        sequenceListing = self.sequenceListingFixture.create_sequencelisting_instance()
        self.sequenceListingFixture.create_sequence_instance(sequenceListing)
        # TODO: generate some fancy sequences to check xml validation?
        util.helper_generateXml(sequenceListing)

        f = os.path.join(util.OUTPUT_DIR, '%s.xml' % sequenceListing.fileName)

        res = util.validateDocumentWithSchema(f, util.XML_SCHEMA_PATH)
        self.assertIsNone(res['parserError'])
        self.assertIsNone(res['schemaError'])

        self.assertTrue(util.validateDocumentWithDtd(f, util.XML_DTD_PATH))
        sequenceListing.delete() # TODO: shouldn't be in teardown?

    def test_validateDocumentWithDtd(self):
        """
        Test that xml sequence listing files are correctly validated
        against the dtd.
        """
        print 'Running %s ...' % getName()

#         valid seql contains the first 2 seqs from f2
        f3 = os.path.join(util.TEST_DATA_DIR_PATH, 'test3.xml')
        self.assertTrue(util.validateDocumentWithDtd(f3, util.XML_DTD_PATH))

#         SOURCxE instead of SOURCE. It passes the validation bc there is no
#         restriction defined in dtd on the value of an element
        f5 = os.path.join(util.TEST_DATA_DIR_PATH, 'test5.xml')
        self.assertTrue(util.validateDocumentWithDtd(f5, util.XML_DTD_PATH))

#         supplementary test with seql with more sequences
#         valid seql 20 sequences
        f2 = os.path.join(util.TEST_DATA_DIR_PATH, 'test2.xml')
        self.assertTrue(util.validateDocumentWithDtd(f2, util.XML_DTD_PATH))

#         ApplicantNamey instead of ApplicantName - except branch
        f6 = os.path.join(util.TEST_DATA_DIR_PATH, 'test6.xml')
        self.assertFalse(util.validateDocumentWithDtd(f6, util.XML_DTD_PATH))

#         ApplicantsName open and closing tags instead of ApplicantName - else branch
        f7 = os.path.join(util.TEST_DATA_DIR_PATH, 'test7.xml')
        self.assertFalse(util.validateDocumentWithDtd(f7, util.XML_DTD_PATH))

#         SequenceTotalQuantity element is missing
        f8 = os.path.join(util.TEST_DATA_DIR_PATH, 'test8.xml')
        self.assertFalse(util.validateDocumentWithDtd(f8, util.XML_DTD_PATH))

#         skipped sequences
        f9 = os.path.join(util.TEST_DATA_DIR_PATH, 'test9.xml')
        self.assertTrue(util.validateDocumentWithDtd(f9, util.XML_DTD_PATH))

    def test_getStartLocation(self):
        """
        Test that start location is correctly returned.
        """
        print 'Running %s ...' % getName()
        loc1 = '467'
        loc2 = '340..565'
        loc3 = '<345..500'
        loc4 = '<1..888'
        loc5 = '1..>888'
        loc6 = '102.110'
        loc7 = '123^124'
        loc8 = 'join(12..78,134..202)'
        loc9 = 'complement(34..126)'
        loc10 = 'complement(join(2691..4571,4918..5163))'
        #         for loc11 the start location returned will be 4918, i.e. the first
        #         number, which is not the lowest
        loc11 = 'join(complement(4918..5163),complement(2691..4571))'
        loc12 = ''
        loc13 = 'abc'
        loc14 = '<1..>888'

        loc = [loc1, loc2, loc3, loc4, loc5, loc6, loc7,
               loc8, loc9, loc10, loc11, loc12, loc13, loc14]

        expected = [467, 340, 345, 1, 1, 102, 123, 12, 34, 2691, 4918, 0, 0, 1]
        actual = [util.getStartLocation(lo) for lo in loc]

        self.assertEqual(expected, actual)

    def test_parseSequenceStringFromFile(self):
        """
        Test that a string is correctly parsed into components.
        """
        print 'Running %s ...' % getName()

        imp1 = """>P01013 GENE X PROTEIN (OVALBUMIN-RELATED)
QIKDLLVSSSTDLDTTLVLVNAIYFKGMWKTAFNAEDTREMPFHVTKQESKPVQMMCMNNSFNVATLPAE
KMKILELPFASGDLSMLVLLPDEVSDLERIEKTINFEKLTEWTNPNTMEKRRVKVYLPQMKIEEKYNLTS
VLMALGMTDLFIPSANLTGISSAESLKISQAVHGAFMELSEDGIEMAGSTGVIEDIKHSPESEQFRADHP
FLFLIKHNPTNTIVYFGRYWSP"""

        res1 = util.parseSequenceStringFromFile(imp1)

        expectedDescLine = 'P01013 GENE X PROTEIN (OVALBUMIN-RELATED)'

        expectedSeq = """QIKDLLVSSSTDLDTTLVLVNAIYFKGMWKTAFNAEDTREMPFHVTKQESKPVQMMCMNNSFNVATLPAEKMKILELPFASGDLSMLVLLPDEVSDLERIEKTINFEKLTEWTNPNTMEKRRVKVYLPQMKIEEKYNLTSVLMALGMTDLFIPSANLTGISSAESLKISQAVHGAFMELSEDGIEMAGSTGVIEDIKHSPESEQFRADHPFLFLIKHNPTNTIVYFGRYWSP"""
        self.assertEqual(expectedDescLine, res1.descriptionLine)
        self.assertEqual(expectedSeq, res1.sequenceLine)

        imp2 = """atgagcaagaacaaggaccagcggaccgccaagaccctggaacggacctgggacaccctg
aaccatctgctgttcatcagtagctgcctgtacaagctgaacctgaagtccgtggcccag
atcaccctgagcatcctggccatgatcatcagcaccagcctgatcattgccgccatcatc
tttatcgccagcgccaaccacaaagtgacccccaccacagccatcatccaggacgccacg
tcccagatcaagaacaccacccccacctacctgacccagaaccctcagctgggcatcagc"""

        res2 = util.parseSequenceStringFromFile(imp2)

        expectedDescLine = ''

        expectedSeq = """atgagcaagaacaaggaccagcggaccgccaagaccctggaacggacctgggacaccctgaaccatctgctgttcatcagtagctgcctgtacaagctgaacctgaagtccgtggcccagatcaccctgagcatcctggccatgatcatcagcaccagcctgatcattgccgccatcatctttatcgccagcgccaaccacaaagtgacccccaccacagccatcatccaggacgccacgtcccagatcaagaacaccacccccacctacctgacccagaaccctcagctgggcatcagc"""
        self.assertEqual(expectedDescLine, res2.descriptionLine)
        self.assertEqual(expectedSeq, res2.sequenceLine)

    def test_determineFormat_raw(self):
        """
        Test that the format of an input string is correctly determined.
        """
        print 'Running %s ...' % getName()

        #         returns raw because the space will be trimmed by splitlines func
        imp1 = """PROTEIN """
        self.assertEqual('raw', util.determineFormat(imp1))

        imp2 = """PROTEIN"""
        self.assertEqual('raw', util.determineFormat(imp2))

        imp3 = """QIKDLLVSSSTDLDTTLVLVNAIYFKGMWKTAFNAEDTREMPFHVTKQESKPVQMMCMNNSFNVATLPAE
KMKILELPFASGDLSMLVLLPDEVSDLERIEKTINFEKLTEWTNPNTMEKRRVKVYLPQMKIEEKYNLTS
VLMALGMTDLFIPSANLTGISSAESLKISQAVHGAFMELSEDGIEMAGSTGVIEDIKHSPESEQFRADHP
FLFLIKHNPTNTIVYFGRYWSP"""
        self.assertEqual('raw', util.determineFormat(imp3))

        imp4 = """QIKDLLVSSSTDLDTTLVLVNAIYFKGMWKTAFNAEDTREMPFHVTKQESKPV"""
        self.assertEqual('raw', util.determineFormat(imp4))

        imp5 = """qikdllvssstdldttlvlvnaiyfkgmwktafnaedtrempfhvtkqeskpv"""
        self.assertEqual('raw', util.determineFormat(imp5))

        imp6 = """uugaccaagc"""
        self.assertEqual('raw', util.determineFormat(imp6))

        #         returns raw because it matches the PRT pattern, even though it is less than 10 chars
        imp7 = """uugaccaag"""
        self.assertEqual('raw', util.determineFormat(imp7))

        imp8 = """atgatgatgcatgatgatgta"""
        self.assertEqual('raw', util.determineFormat(imp8))

        imp9 = """ATGATGATGATGATGCATGTA"""
        self.assertEqual('raw', util.determineFormat(imp9))

    def test_determineFormat_fasta(self):
        """
        Test that the format of an input string is correctly determined.
        """
        print 'Running %s ...' % getName()

        imp1 = """>P01013 GENE X PROTEIN (OVALBUMIN-RELATED)
QIKDLLVSSSTDLDTTLVLVNAIYFKGMWKTAFNAEDTREMPFHVTKQESKPVQMMCMNNSFNVATLPAE
KMKILELPFASGDLSMLVLLPDEVSDLERIEKTINFEKLTEWTNPNTMEKRRVKVYLPQMKIEEKYNLTS
VLMALGMTDLFIPSANLTGISSAESLKISQAVHGAFMELSEDGIEMAGSTGVIEDIKHSPESEQFRADHP
FLFLIKHNPTNTIVYFGRYWSP"""
        self.assertEqual('fasta', util.determineFormat(imp1))

    def test_determineFormat_unknown(self):
        """
        Test that the format unknown of an input string is correctly determined.
        """
        print 'Running %s ...' % getName()

        #         returns unknown because it contains spaces
        imp1 = """>P01013 GENE X PROTEIN (OVALBUMIN-RELATED)"""
        self.assertEqual('unknown', util.determineFormat(imp1))

        #         returns unknown because it contains spaces
        imp2 = """atgatgatga tgatgatgta cctgcagacc ccgtttccct ggtgccagtg gcagaggagt       60"""
        self.assertEqual('unknown', util.determineFormat(imp2))

        #         returns unknown because it contains spaces
        imp3 = """uugaccaagc uggggacccc ggucccuugg gaccaguggc agaggaguc                   49"""
        self.assertEqual('unknown', util.determineFormat(imp3))

        #         returns unknown because it contains spaces and end of line char
        imp4 = """atgatgatga tgatgatgta cctgcagacc ccgtttccct ggtgccagtg gcagaggagt       60

c                                                                       61
"""
        self.assertEqual('unknown', util.determineFormat(imp4))

        #         returns unknown because it is less than 3 chars
        imp5 = """act"""
        self.assertEqual('unknown', util.determineFormat(imp5))

    def test_isResiduesLine(self):
        """
        Test that an input string containing one letter symbols is correctly
        recognised as a residues line.
        """
        print 'Running %s ...' % getName()

        #         returns false because it contains spaces
        imp1 = """>P01013 GENE X PROTEIN (OVALBUMIN-RELATED)"""

        #         returns false because it contains spaces and end of line char
        imp2 = """>P01013 GENE X PROTEIN (OVALBUMIN-RELATED)
QIKDLLVSSSTDLDTTLVLVNAIYFKGMWKTAFNAEDTREMPFHVTKQESKPVQMMCMNNSFNVATLPAE
KMKILELPFASGDLSMLVLLPDEVSDLERIEKTINFEKLTEWTNPNTMEKRRVKVYLPQMKIEEKYNLTS
VLMALGMTDLFIPSANLTGISSAESLKISQAVHGAFMELSEDGIEMAGSTGVIEDIKHSPESEQFRADHP
FLFLIKHNPTNTIVYFGRYWSP"""

        #         returns false because it contains space
        imp3 = """PROTEIN """

        #         returns true
        imp4 = """PROTEIN"""

        #         returns false because it contains end of line chars
        imp5 = """QIKDLLVSSSTDLDTTLVLVNAIYFKGMWKTAFNAEDTREMPFHVTKQESKPVQMMCMNNSFNVATLPAE
KMKILELPFASGDLSMLVLLPDEVSDLERIEKTINFEKLTEWTNPNTMEKRRVKVYLPQMKIEEKYNLTS
VLMALGMTDLFIPSANLTGISSAESLKISQAVHGAFMELSEDGIEMAGSTGVIEDIKHSPESEQFRADHP
FLFLIKHNPTNTIVYFGRYWSP"""

        #         returns true
        imp6 = """QIKDLLVSSSTDLDTTLVLVNAIYFKGMWKTAFNAEDTREMPFHVTKQESKPV"""

        #         returns true
        imp7 = """qikdllvssstdldttlvlvnaiyfkgmwktafnaedtrempfhvtkqeskpv"""

        #         returns false because it contains spaces
        imp8 = """atgatgatga tgatgatgta cctgcagacc ccgtttccct ggtgccagtg gcagaggagt       60"""

        #         returns false because it contains spaces
        imp9 = """uugaccaagc uggggacccc ggucccuugg gaccaguggc agaggaguc                   49"""

        #         returns false because it contains spaces and end of line char
        imp10 = """atgatgatga tgatgatgta cctgcagacc ccgtttccct ggtgccagtg gcagaggagt       60

c                                                                       61
"""
        #         returns true
        imp11 = """uugaccaagc"""

        #         returns true because it matches the PRT pattern, even though it is less than 10 chars
        imp12 = """uugaccaag"""

        #         returns true
        imp13 = """atgatgatgcatgatgatgta"""

        #         returns true
        imp14 = """ATGATGATGATGATGCATGTA"""

        #         returns false because it is less than 3 chars
        imp15 = """act"""

        self.assertFalse(util.isResiduesLine(imp1))
        self.assertFalse(util.isResiduesLine(imp2))
        self.assertFalse(util.isResiduesLine(imp3))
        self.assertTrue(util.isResiduesLine(imp4))
        self.assertFalse(util.isResiduesLine(imp5))
        self.assertTrue(util.isResiduesLine(imp6))
        self.assertTrue(util.isResiduesLine(imp7))
        self.assertFalse(util.isResiduesLine(imp8))
        self.assertFalse(util.isResiduesLine(imp9))
        self.assertFalse(util.isResiduesLine(imp10))
        self.assertTrue(util.isResiduesLine(imp11))
        self.assertTrue(util.isResiduesLine(imp12))
        self.assertTrue(util.isResiduesLine(imp13))
        self.assertTrue(util.isResiduesLine(imp14))
        self.assertFalse(util.isResiduesLine(imp15))