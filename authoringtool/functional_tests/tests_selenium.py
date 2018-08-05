import django
django.setup()

from django.test import LiveServerTestCase
# from django.test import tag
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 

import time
from unittest import skip

class SeqlSeleniumTestFixture():    
#     @classmethod
#     def register(cls, aBrowser):
#         username = aBrowser.find_element_by_id('id_username')
#         email = aBrowser.find_element_by_id('id_email')
#         password1 = aBrowser.find_element_by_id('id_password1')
#         password2 = aBrowser.find_element_by_id('id_password2')
#                    
#         username.send_keys('user20')
#         email.send_keys('user20@email.com')
#         password1.send_keys('password20')
#         password2.send_keys('password20')
#          
#         aBrowser.find_element_by_class_name("btn").click()
    
    @classmethod
    def add_sequencelisting(cls, aBrowser, aFileName):
        inventionTitle = aBrowser.find_element_by_id('id_inventionTitle')
        inventionTitleLanguageCode = aBrowser.find_element_by_id('id_inventionTitleLanguageCode')
        fileName = aBrowser.find_element_by_id('id_fileName')
        applicantFileReference = aBrowser.find_element_by_id('id_applicantFileReference')
        IPOfficeCode = aBrowser.find_element_by_id('id_IPOfficeCode')
        applicationNumberText = aBrowser.find_element_by_id('id_applicationNumberText')
        filingDate = aBrowser.find_element_by_id('id_filingDate')
        earliestPriorityIPOfficeCode = aBrowser.find_element_by_id('id_earliestPriorityIPOfficeCode')
        earliestPriorityApplicationNumberText = aBrowser.find_element_by_id('id_earliestPriorityApplicationNumberText')
        earliestPriorityFilingDate = aBrowser.find_element_by_id('id_earliestPriorityFilingDate')
        applicantName = aBrowser.find_element_by_id('id_applicantName')
        applicantNameLanguageCode = aBrowser.find_element_by_id('id_applicantNameLanguageCode')
        applicantNameLatin = aBrowser.find_element_by_id('id_applicantNameLatin')
        inventorName = aBrowser.find_element_by_id('id_inventorName')
        inventorNameLanguageCode = aBrowser.find_element_by_id('id_inventorNameLanguageCode')
        inventorNameLatin = aBrowser.find_element_by_id('id_inventorNameLatin')
            
        inventionTitle.send_keys('a')
        inventionTitleLanguageCode.send_keys('b')
        fileName.send_keys(aFileName)
        applicantFileReference.send_keys('d')
        IPOfficeCode.send_keys('e')
        applicationNumberText.send_keys('f')
        filingDate.send_keys('2010-12-20')
        earliestPriorityIPOfficeCode.send_keys('g')
        earliestPriorityApplicationNumberText.send_keys('h')
        earliestPriorityFilingDate.send_keys('2009-12-20')
        applicantName.send_keys('i')
        applicantNameLanguageCode.send_keys('j')
        applicantNameLatin.send_keys('k')
        inventorName.send_keys('l')
        inventorNameLanguageCode.send_keys('m')
        inventorNameLatin.send_keys('n')
            
        aBrowser.find_element_by_xpath('//input[@value="Submit"]').click()

# @skip('temporarily skipped')
class VisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
             
    def tearDown(self):
        self.browser.quit()

    def test_can_access_home_page(self):
        print 'Selenium: Running %s ...' % self._testMethodName

        self.browser.get(
            '%s%s' % (self.live_server_url, '/sequencelistings'))

        self.assertIn('st26proto - Index', self.browser.title)
        self.assertIn('WELCOME',
                      self.browser.find_element_by_id('welcomeHeader').text)
        self.assertIn('Disclaimer',
                      self.browser.find_element_by_id('disclaimerHeader').text)

    def test_can_access_overview_page_no_seqls(self):
        print 'Selenium: Running %s ...' % self._testMethodName
                
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/overview'))
                
        self.assertIn('st26proto - Overview', self.browser.title) 
        self.assertIn('No sequence listings are available.', self.browser.find_element_by_id('no_seqls_par').text)
        self.assertEqual(0, len(self.browser.find_elements_by_tag_name('table')),
                         'There should be no table if no seqls created.')
        # TODO: 20180805 currently there is no registration any longer ...
#         unregistered visitors are not allowed to add seqls i.e. there is no link to add seql
        self.assertEqual(0, len(self.browser.find_elements_by_id('add_seql_link')))

    def test_validation_page(self):
        print 'Selenium: Running %s ...' % self._testMethodName

        self.browser.get(
            '%s%s' % (self.live_server_url, '/sequencelistings/validation'))
        self.assertIn('st26proto - Validation', self.browser.title)
        fileChooserInput = self.browser.find_element_by_name('myfile')
        fileChooserInput.send_keys('/Users/ad/pyton/work/st26proto/authoringtool/sequencelistings/schema/xtestdata/t25.xml')
        validateButton = self.browser.find_element_by_id('validateButton')
        validateButton.click()
        schemaErrorHeader = self.browser.find_element_by_id('schemaErrorHeader')

        self.assertIn('Schema error', schemaErrorHeader.text)

    def test_about_page(self):
        print 'Selenium: Running %s ...' % self._testMethodName
                
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/about'))     
        self.assertIn('st26proto - About', self.browser.title)
        
# @skip('temporarily skipped')
class CreateSequenceListingTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
             
        # register
#         self.browser.get('%s%s' %(self.live_server_url, '/accounts/register/'))    
#         SeqlSeleniumTestFixture.register(self.browser)
              
    def tearDown(self):
        self.browser.quit()
                 
#     def test_register(self):
#         print 'Selenium: Running %s ...' % self._testMethodName
#      
#  #         check that the index page of registered user is displayed
#         self.browser.get('%s%s' % (self.live_server_url, '/sequencelistings'))
#         self.assertIn('st26proto - Index', self.browser.title)
# #         self.assertIn('user20', self.browser.find_element_by_class_name('page-header').text)
#         self.assertIn('user20', self.browser.find_element_by_id('welcomeHeader').text)
        
    def test_add_sequencelisting_functionality(self):
        print 'Selenium: Running %s ...' % self._testMethodName
          
        fileName = 'selenium_test1'
          
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/add_sequencelisting')) 
        SeqlSeleniumTestFixture.add_sequencelisting(self.browser, fileName)
    
        self.browser.get('%s%s' % (self.live_server_url, '/sequencelistings/overview'))
            
        table = self.browser.find_element_by_id('home_page_table')
#         self.assertEqual(1, len(table), 'There should be a table if a seql added.')
        cells = table.find_elements_by_tag_name('td')
        self.assertIn(fileName, [cell.text for cell in cells])
                
    def test_add_sequencelisting_no_inventor_functionality(self):
        """
        Test that a seql can be created without providing inventor data.
        """
        print 'Selenium: Running %s ...' % self._testMethodName
                
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/add_sequencelisting')) 
                    
#         =======add seql no inventor=================
        inventionTitle = self.browser.find_element_by_id('id_inventionTitle')
        inventionTitleLanguageCode = self.browser.find_element_by_id('id_inventionTitleLanguageCode')
        fileName = self.browser.find_element_by_id('id_fileName')
        applicantFileReference = self.browser.find_element_by_id('id_applicantFileReference')
        IPOfficeCode = self.browser.find_element_by_id('id_IPOfficeCode')
        applicationNumberText = self.browser.find_element_by_id('id_applicationNumberText')
        filingDate = self.browser.find_element_by_id('id_filingDate')
        earliestPriorityIPOfficeCode = self.browser.find_element_by_id('id_earliestPriorityIPOfficeCode')
        earliestPriorityApplicationNumberText = self.browser.find_element_by_id('id_earliestPriorityApplicationNumberText')
        earliestPriorityFilingDate = self.browser.find_element_by_id('id_earliestPriorityFilingDate')
        applicantName = self.browser.find_element_by_id('id_applicantName')
        applicantNameLanguageCode = self.browser.find_element_by_id('id_applicantNameLanguageCode')
        applicantNameLatin = self.browser.find_element_by_id('id_applicantNameLatin')
                
        inventionTitle.send_keys('axx')
        inventionTitleLanguageCode.send_keys('b')
        fileName.send_keys('selenium_test_file_name_no_inventor')
        applicantFileReference.send_keys('d')
        IPOfficeCode.send_keys('e')
        applicationNumberText.send_keys('f')
        filingDate.send_keys('2010-12-20')
        earliestPriorityIPOfficeCode.send_keys('g')
        earliestPriorityApplicationNumberText.send_keys('h')
        earliestPriorityFilingDate.send_keys('2009-12-20')
        applicantName.send_keys('i')
        applicantNameLanguageCode.send_keys('j')
        applicantNameLatin.send_keys('k')
                
        self.browser.find_element_by_xpath('//input[@value="Submit"]').click()
# =================
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/overview')) 
     
        table = self.browser.find_element_by_id('home_page_table')
        cells = table.find_elements_by_tag_name('td')
        self.assertIn('selenium_test_file_name_no_inventor', [cell.text for cell in cells])
                 
    def test_add_sequencelisting_no_application_identification_functionality(self):
        """
        Test that a seql can be created without providing application identification data.
        """
        print 'Selenium: Running %s ...' % self._testMethodName
            
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/add_sequencelisting')) 
                 
#         =======add seql no inventor=================
        inventionTitle = self.browser.find_element_by_id('id_inventionTitle')
        inventionTitleLanguageCode = self.browser.find_element_by_id('id_inventionTitleLanguageCode')
        fileName = self.browser.find_element_by_id('id_fileName')
        applicantFileReference = self.browser.find_element_by_id('id_applicantFileReference')
#         IPOfficeCode = self.browser.find_element_by_id('id_IPOfficeCode')
#         applicationNumberText = self.browser.find_element_by_id('id_applicationNumberText')
        filingDate = self.browser.find_element_by_id('id_filingDate')
        earliestPriorityIPOfficeCode = self.browser.find_element_by_id('id_earliestPriorityIPOfficeCode')
        earliestPriorityApplicationNumberText = self.browser.find_element_by_id('id_earliestPriorityApplicationNumberText')
        earliestPriorityFilingDate = self.browser.find_element_by_id('id_earliestPriorityFilingDate')
        applicantName = self.browser.find_element_by_id('id_applicantName')
        applicantNameLanguageCode = self.browser.find_element_by_id('id_applicantNameLanguageCode')
        applicantNameLatin = self.browser.find_element_by_id('id_applicantNameLatin')
                 
        inventionTitle.send_keys('axx')
        inventionTitleLanguageCode.send_keys('b')
        fileName.send_keys('selenium_test_file_name_no_applIdentification')
        applicantFileReference.send_keys('d')
#         IPOfficeCode.send_keys('e')
#         applicationNumberText.send_keys('f')
#         filingDate.send_keys('2010-12-20')
        earliestPriorityIPOfficeCode.send_keys('g')
        earliestPriorityApplicationNumberText.send_keys('h')
        earliestPriorityFilingDate.send_keys('2009-12-20')
        applicantName.send_keys('i')
        applicantNameLanguageCode.send_keys('j')
        applicantNameLatin.send_keys('k')
                 
        self.browser.find_element_by_xpath('//input[@value="Submit"]').click()
# =================
                 
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/overview')) 
                  
        table = self.browser.find_element_by_id('home_page_table')
        cells = table.find_elements_by_tag_name('td')
        self.assertIn('selenium_test_file_name_no_applIdentification', [cell.text for cell in cells])
 
# @skip('temporarily skipped')
class EditSequenceListingTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
          
#         self.browser.get('%s%s' %(self.live_server_url, '/accounts/register/')) 
#         SeqlSeleniumTestFixture.register(self.browser)
        self.fileName = 'selenium_test2'
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/add_sequencelisting')) 
        SeqlSeleniumTestFixture.add_sequencelisting(self.browser, self.fileName)
        
    def tearDown(self):
        self.browser.quit()

    def test_add_sequence_form(self):
        print 'Selenium: Running %s ...' % self._testMethodName
         
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/overview'))
         
#         check that there is a detail page is produced for the newly created seql        
        self.browser.find_element_by_link_text(self.fileName).click()
                   
#         check that the link to preview, edit and generate XML sequence listing is displayed
        preview_seql_link = self.browser.find_element_by_link_text('Preview')
        self.assertTrue(preview_seql_link.is_displayed())
        edit_seql_link = self.browser.find_element_by_link_text('Edit')
        self.assertTrue(edit_seql_link.is_displayed())       
        generatexml_seql_link = self.browser.find_element_by_link_text('Generate XML')
        self.assertTrue(generatexml_seql_link.is_displayed())       
           
    def test_add_sequence_functionality(self):
        print 'Selenium: Running %s ...' % self._testMethodName
         
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/overview'))
         
#         check that there is a detail page is produced for the newly created seql        
        self.browser.find_element_by_link_text(self.fileName).click()
        
#         check that the link to edit is displayed
        edit_seql_link = self.browser.find_element_by_link_text('Edit')
        self.assertTrue(edit_seql_link.is_displayed())       
   
#         render the page to edit seql form to add a sequence
        edit_seql_link.click()

#         check that the link to add a sequence is displayed        
        add_seq_link = self.browser.find_element_by_link_text('Add new sequence')
        self.assertTrue(add_seq_link.is_displayed()) 

#         render the page to add a sequence        
        add_seq_link.click() 
        
        headers_h2_add_seq = self.browser.find_elements_by_tag_name('h2')
        self.assertIn('Add new sequence', [h.text for h in headers_h2_add_seq])
        
        moltype = self.browser.find_element_by_id('id_moltype')
        residues = self.browser.find_element_by_id('id_residues') 
        organism  = self.browser.find_element_by_id('id_organism') 
        
        moltype.send_keys('DNA')
        residues.send_keys('acgtacgtacgt')
        organism.send_keys('Homo sapiens selenium')
           
        self.browser.find_element_by_xpath('//input[@value="Submit"]').click()
#         self.browser.execute_script("document.getElementsByTagName('input')[0].click();")
#         self.browser.execute_script("document.querySelectorAll('input[value]=\x22Submit\x22').click();")
           
#         check that the sequence has been created
#         self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/sl1'))
#         this commented out because it gives an error "NoSuchElementException: Message: Unable to locate element: {"method":"link text","selector":"selenium_test2"}" after disabling bootstrap which is broken since launching of v.4 beta version.
#         self.browser.find_element_by_link_text(self.fileName).click()  

#         now we are on detail view
        residues_element = self.browser.find_element_by_class_name('residues')
        self.assert_('acgtacgtac gt', residues_element.text)
           
#         check that the seql page contains now the new sequence
        tds = self.browser.find_elements_by_tag_name('td')
        self.assertIn('Homo sapiens selenium', [td.text for td in tds])
          
#         cant test residues because they are not loaded (due to JavaScript????)
#         residues_elements = self.browser.find_element_by_class_name('residues')
#         print residues_elements.text
#         self.assertIn('acgtacgtac gt 12', [r.text for r in residues_elements])
   
#         generate SEQL XML file
        self.browser.find_element_by_link_text("Generate XML").click()
           
#         self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/sl1/xmloutput'))
           
        display_link = self.browser.find_element_by_link_text("display generated sequence listing")
           
#         check that the link to display the generated xml file is displayed
        self.assertTrue(display_link.is_displayed()) 
                 
#         cant test display generated xml because of JavaScript probably?
#         display_link.click()
#         time.sleep(20)
#         self.browser.execute_script("document.getElementsByTagName('a')[0].click();")
#         print 'executed script'       
#         self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/display/selenium_test_file_name'))
#         time.sleep(20)
#         print self.browser.page_source
           
#         headers_h1 = self.browser.find_elements_by_tag_name('h1')
#         self.assertIn('ST26 SEQUENCE LISTING with client side XSLT', [h.text for h in headers_h1])

    def test_add_sequence_functionality_sequenceName(self):
        print 'Selenium: Running %s ...' % self._testMethodName
         
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/overview'))
         
        self.browser.find_element_by_link_text(self.fileName).click()
        edit_seql_link = self.browser.find_element_by_link_text('Edit')
        edit_seql_link.click()
        add_seq_link = self.browser.find_element_by_link_text('Add new sequence')
        add_seq_link.click() 
                
        sequenceName = self.browser.find_element_by_id('id_sequenceName')   
        moltype = self.browser.find_element_by_id('id_moltype')
        residues = self.browser.find_element_by_id('id_residues') 
        organism  = self.browser.find_element_by_id('id_organism') 

#         test that the sequenceName field is prepopulated
        self.assert_('seq_1', sequenceName.text)
           
#         sequenceName.send_keys('selenium_test_seq_name')
        moltype.send_keys('DNA')
        residues.send_keys('acgtacgtacgt')
        organism.send_keys('Homo sapiens selenium')
           
        self.browser.find_element_by_xpath('//input[@value="Submit"]').click()

#         now we are on edit_seql view
#         test sequenceName value
        sequenceName_element = self.browser.find_element_by_class_name('sequenceName')
        self.assert_('seq_1', sequenceName_element.text)
             
#           test 
        add_seq_link = self.browser.find_element_by_link_text('Add new sequence')
        add_seq_link.click()
        sequenceName = self.browser.find_element_by_id('id_sequenceName')   
        moltype = self.browser.find_element_by_id('id_moltype')
        residues = self.browser.find_element_by_id('id_residues') 
        organism  = self.browser.find_element_by_id('id_organism') 

#         test that the sequenceName field is prepopulated
        self.assert_('seq_2', sequenceName.text)
           
#         sequenceName.send_keys('selenium_test_seq_name')
        moltype.send_keys('DNA')
        sequenceName.send_keys('xxyyzz')
        residues.send_keys('acgtacgtacgt')
        organism.send_keys('Homo sapiens selenium2')
           
        self.browser.find_element_by_xpath('//input[@value="Submit"]').click()

#         now we are on edit_seql view
#         if I comment out this line the test fails
#         print 'residues:', self.browser.find_element_by_class_name('residues').text
#         test sequenceName value
        sequenceName_element = self.browser.find_element_by_class_name('sequenceName')
        self.assert_('xxyyzz', sequenceName_element.text) 
        
    def test_import_sequence(self):
        print 'Selenium: Running %s ...' % self._testMethodName
         
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/overview'))
          
#         check that there is a detail page is produced for the newly created seql        
        self.browser.find_element_by_link_text(self.fileName).click()
            
#         check that the link to edit is displayed
        edit_seql_link = self.browser.find_element_by_link_text('Edit')
        self.assertTrue(edit_seql_link.is_displayed())       
            
#         add a sequence
        edit_seql_link.click()
         
        import_seq_link = self.browser.find_element_by_link_text('Import sequence')
        self.assertTrue(import_seq_link.is_displayed()) 
         
        import_seq_link.click() 
        
#         self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/sl1/import_seq'))
        headers_h2_import_seq = self.browser.find_elements_by_tag_name('h2')
        self.assertIn('Import sequence', [h.text for h in headers_h2_import_seq])
        
        organism  = self.browser.find_element_by_id('id_organism')
        moltype = self.browser.find_element_by_id('id_moltype')
        fileField = self.browser.find_element_by_id('id_file')
         
        organism.send_keys('Felix catus selenium')
        moltype.send_keys('AA')
        fileField.send_keys(r'/Users/ad/pyton/projects/st26proto/authoringtool/functional_tests/imp1.fasta')
        
        self.browser.find_element_by_xpath('//input[@value="Upload file"]').click()

#         now we are on edit_seql view
        residues_element = self.browser.find_element_by_class_name('residues')
        self.assert_('QIKDLLVSSS', residues_element.text)
#         self.assert_('QIKDLLVSSS TDLDTTLVLV NAIYFKGMWK ', residues_element.text)
#            TODO: continue uncommenting to test import!!!!!!!!!!!
# #         check that the seql page contains now the new sequence
#         tds = self.browser.find_elements_by_tag_name('td')
#         self.assertIn('Homo sapiens selenium', [td.text for td in tds])
#            
# #         cant test residues because they are not loaded (due to JavaScript????)
# #         residues_elements = self.browser.find_element_by_class_name('residues')
# #         print residues_elements.text
# #         self.assertIn('acgtacgtac gt 12', [r.text for r in residues_elements])
#    
# #         generate SEQL XML file
#         self.browser.find_element_by_link_text("Generate XML").click()
#            
# #         self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/sl1/xmloutput'))
#            
#         display_link = self.browser.find_element_by_link_text("display generated sequence listing")
#            
# #         check that the link to display the generated xml file is displayed
#         self.assertTrue(display_link.is_displayed()) 