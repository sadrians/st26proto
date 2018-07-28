#!/usr/bin/python
# -*- coding: utf-8 -*-
import django
django.setup()
import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'authoringtool.settings'
from django.test import TestCase
from django.contrib.auth.models import User 
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import resolve, reverse
from models import SequenceListing, Title, Sequence, Feature, Qualifier
from forms import QualifierForm
import views

from django.utils import timezone
import util 

import inspect 
# import os
# import logging

# TODO: revive logging whenever necessary
# logger = logging.getLogger(__name__)
# logger.info('TEST start.')

def getName():
    return inspect.stack()[1][3]
 
class SequenceListingFixture(object):
    def create_sequencelisting_instance(self):
        sl = SequenceListing.objects.create(
            fileName = 'test_xmlsql',
            dtdVersion = '1',
            softwareName = 'prototype',
            softwareVersion = '0.1',
            productionDate = timezone.now().date(),
              
            applicantFileReference = '123',
       
            IPOfficeCode = 'EP',
            applicationNumberText = '2015123456',
            filingDate = timezone.now().date(),
           
            earliestPriorityIPOfficeCode = 'US',
            earliestPriorityApplicationNumberText = '998877',
            earliestPriorityFilingDate = timezone.now().date(),
           
            applicantName = 'John Smith',
            applicantNameLanguageCode = 'EN',
            applicantNameLatin = 'same',
           
            inventorName = 'Mary Dupont',
            inventorNameLanguageCode = 'FR',
            inventorNameLatin = 'Mary Dupont',        
            )
        
        self.create_title_instance(sl)
         
        return sl 
  
    def create_title_instance(self, sl):
        return Title.objects.create(
                    sequenceListing = sl,
                    inventionTitle = 'Invention 1',
                    inventionTitleLanguageCode = 'EN')
      
    def create_sequence_instance(self, sl):
        currentSeqIdNo = len(sl.sequence_set.all()) +1
        currentSequenceName = 'test_seq_%i' % currentSeqIdNo
        seq = Sequence.objects.create(
                    sequenceListing = sl,
                    sequenceName = currentSequenceName,
                    moltype = 'DNA',
                    residues = 'catcatcatcatcatcat')

        views.feature_source_helper(seq, 'Homo sapiens', 'genomic DNA')
        
        return seq 
    
    def create_custom_sequence_instance(self, sl, mt, res, org, mtq):
        currentSeqIdNo = len(sl.sequence_set.all()) +1
        currentSequenceName = 'test_seq_%i' % currentSeqIdNo
        
        seq = Sequence.objects.create(
                sequenceListing = sl,
                sequenceName = currentSequenceName,
                moltype = mt,
                residues = res)

        views.feature_source_helper(seq, org, mtq)
        
        return seq 
 
class OverviewViewNoSequenceListingTest(TestCase):
    def test_index_view_with_no_sequencelistings(self):
        """
        If no sequence listings exist, an appropriate message should be displayed 
        on overview page.
        """
        print 'Running %s ...' % getName()
        
        response = self.client.get(reverse('sequencelistings:overview'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No sequence listings are available.")
        self.assertContains(response, "sequencelistings/output/resources/style_colour.css")
        self.assertQuerysetEqual(response.context['sequencelistings'], [])
              
class ViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ViewsTests, cls).setUpClass()
        cls.sequenceListingFixture = SequenceListingFixture()
        seqls = SequenceListing.objects.all()
        for seql in seqls:
            seql.delete()
             
    def setUp(self):
#         self.sequenceListingFixture = SequenceListingFixture()
        self.sequenceListing = self.sequenceListingFixture.create_sequencelisting_instance()
         
    def tearDown(self):
        TestCase.tearDown(self)
        self.sequenceListing.delete()
     
#     TODO: add test after refactoring Index class into index function 
                               
    def test_overview_view_with_one_sequencelisting(self):
        """
        The overview page displays one sequence listing.
        """
        print 'Running %s ...' % getName()
        response = self.client.get(reverse('sequencelistings:overview'))
         
        self.assertEqual(response.status_code, 200)
#         test that the page returns expected html contents
        self.assertContains(response, "test_xmlsql")
        self.assertContains(response, "Invention 1")
        self.assertQuerysetEqual(response.context['sequencelistings'], 
                                 ['<SequenceListing: Sequence listing test_xmlsql>'])
     
     
#     def test_add_sequencelisting_page_can_save_a_post_request(self):
# #         TODO: add code similar to TDD online book? ...
 
#         response = self.client.get(reverse('sequencelistings:add_sequencelisting'))
# #         test that the page returns expected html contents
#         self.assertContains(response, "Invention title") 
#         self.assertContains(response, "Submit")      
#         TODO: continue adding test if necessary
             
    def test_detail_view(self):
        """
        The details of the sequence listing are correctly displayed.
        """
        print 'Running %s ...' % getName()
#         test that URL resolves to correct views function        
        found = resolve('/sequencelistings/sl%d/' % self.sequenceListing.id)
        self.assertEqual(found.func, views.detail)
         
        response = self.client.get(reverse('sequencelistings:detail', args=[self.sequenceListing.pk]))
        self.assertEqual(response.status_code, 200)
#         test that the page returns expected html contents        
        self.assertContains(response, "test_xmlsql")
        self.assertContains(response, "2015123456")
        self.assertEqual(response.context['sequencelisting'], self.sequenceListing)
#         there are no sequences created yet:
        self.assertFalse(response.context['sequencelisting'].sequence_set.all())
#         now a sequence is created
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        self.assertTrue(response.context['sequencelisting'].sequence_set.all())
        response = self.client.get(reverse('sequencelistings:detail', args=[self.sequenceListing.pk]))
#         print response
#         test that the page returns expected html contents
#         self.assertContains(response, "location")
        self.assertContains(response, "Sequence name")
        self.assertContains(response, "Location")
        self.assertContains(response, "Generate XML")
        self.assertContains(response, "source")
        self.assertContains(response, "organism")
        self.assertContains(response, "Homo sapiens")
          
#         if the user is logged in: TODO: see what is this?
#         self.assertContains(response, "Add new sequence")
# TODO: test if edit is allowed when user logged in
                
    def test_detail_view_after_add_sequence(self):
        """
        The sequence listing detail page, displays the generated sequences.
        """
        print 'Running %s ...' % getName()
               
        self.assertEqual(0, self.sequenceListing.sequenceTotalQuantity)
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
               
        self.assertEqual(1, self.sequenceListing.sequenceTotalQuantity)
#         check however that the sequence has been correctly created
        self.assertEqual(1, s1.sequenceIdNo)
        self.assertEqual('test_seq_1', s1.sequenceName)
        self.assertEqual('catcatcatcatcatcat', s1.residues)
          
        response = self.client.get(reverse('sequencelistings:detail', 
                                           args=[self.sequenceListing.id]))
        self.assertEqual(response.status_code, 200)
#         test that the page returns expected html contents
        self.assertContains(response, "18")
        self.assertContains(response, "catcatcatcatcatcat")
#         create another sequence      
        s2 = Sequence.objects.create(
            sequenceListing = self.sequenceListing,
            sequenceName = 'test_xyz',
            moltype = 'RNA',
            residues = 'caucaucaucaucaucaucc')
                 
        self.assertEqual(2, self.sequenceListing.sequenceTotalQuantity)
          
        response = self.client.get(reverse('sequencelistings:detail', 
                                           args=[self.sequenceListing.id]))
        self.assertEqual(response.status_code, 200)
#         test that the page returns expected html contents
        self.assertContains(response, 'test_xyz')
        self.assertContains(response, "18")
        self.assertContains(response, "catcatcatcatcatcat")
        self.assertContains(response, "20")
        self.assertContains(response, "RNA")
             
    def test_detail_view_after_add_feature(self):
        """
        The sequence listing detail page displays correctly the generated feature.
        """
        print 'Running %s ...' % getName()
               
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        f = s1.feature_set.all()
        self.assertEqual(1, len(f), 'Expected 1 feature.')
           
#         create feature
        f2 = Feature.objects.create(sequence=s1, 
                                    featureKey='allele', 
                                    location='4')
        self.assertEqual('allele', f2.featureKey)
        self.assertEqual('4', f2.location)
                
        f = s1.feature_set.all()
        self.assertEqual(2, len(f), 'Expected 2 features.')
        self.assertEqual('source', f[0].featureKey)
                
        response = self.client.get(reverse('sequencelistings:detail', args=[self.sequenceListing.id]))
        self.assertEqual(response.status_code, 200)
#         test that the page returns expected html contents
        self.assertContains(response, "source")
        self.assertContains(response, "1..18")
        self.assertContains(response, "allele")
        self.assertContains(response, "4")
       
    def test_detail_view_after_add_qualifier(self):
        """
        The sequence listing detail page displays correctly the generated qualifier.
        """
        print 'Running %s ...' % getName()
               
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
           
        f1 = Feature.objects.create(sequence=s1, 
                                    featureKey='modified_base', 
                                    location='7')
        q1 = Qualifier.objects.create(feature=f1, 
                                    qualifierName='note', 
                                    qualifierValue='test for note')
                
        self.assertEqual('note', q1.qualifierName)
        self.assertEqual('test for note', q1.qualifierValue)
          
        response = self.client.get(reverse('sequencelistings:detail', 
                                           args=[self.sequenceListing.id]))
#         test that the page returns expected html contents
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "note")
        self.assertContains(response, "test for note")
  
#     TODO: status code is 302 instead of 200. why???? bc of some redirection (2016 Jun 30)
    
    def test_add_sequencelisting_view(self):
        """
        The form add_sequencelisting is correctly displayed.
        """
        print 'Running %s ...' % getName()
        found = resolve('/sequencelistings/add_sequencelisting/')
        self.assertEqual(found.func, views.add_sequencelisting)
        
        response = self.client.get(reverse('sequencelistings:add_sequencelisting'))
        
#         #         first redirected because not logged in 
#         self.assertEqual(response.status_code, 302)
# #         create a user and log in
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.user.save()
#         login = self.client.login(username='testuser', password='12345')
#         
#         response = self.client.get(reverse('sequencelistings:add_sequencelisting'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create a sequence listing")
        self.assertContains(response, "File name:")
     
    def test_edit_seql_view(self):
        print 'Running %s ...' % getName()
         
        found = resolve('/sequencelistings/sl%d/edit_seql/' % self.sequenceListing.id)
        self.assertEqual(found.func, views.edit_seql)
         
        self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
         
        response = self.client.get(reverse('sequencelistings:edit_seql', 
                                           args=[self.sequenceListing.id]))
#         test that the page returns expected html contents
# #         first redirected because not logged in 
#         self.assertEqual(response.status_code, 302)
# #         create a user and log in
#         self.user = User.objects.create_user(username='testuser', password='12345')
#         self.user.save()
#         login = self.client.login(username='testuser', password='12345')
#         
#         response = self.client.get(reverse('sequencelistings:edit_seql', 
#                                            args=[self.sequenceListing.id]))
        self.assertEqual(response.status_code, 200)
        
        self.assertContains(response, "EDIT SEQUENCE LISTING")
        self.assertContains(response, "Add new title")
        self.assertContains(response, "Add new sequence") 
        self.assertContains(response, "Import sequence")        
        self.assertContains(response, "Add new feature")        
        self.assertContains(response, "Add new qualifier")        
 
    def test_sequence_view(self):
        print 'Running %s ...' % getName()
#         test that URL resolves to correct views function        
        seq = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
 
        found = resolve('/sequencelistings/sl%d/seq%d/' % (self.sequenceListing.id, seq.id))
        self.assertEqual(found.func, views.sequence)
         
        response = self.client.get(reverse('sequencelistings:sequence', 
                                           args=[self.sequenceListing.id, seq.id]))
#         test that the page returns expected html contents
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sequence name")
        self.assertContains(response, "Molecule type")
        self.assertContains(response, "Submit")
         
#         TODO: continue adding test if necessary
  
    def test_add_seq_view(self):
        """
        The form add_seq is correctly displayed.
        """
        print 'Running %s ...' % getName()
#         test that URL resolves to correct views function        
        found = resolve('/sequencelistings/sl%d/add_seq/' % self.sequenceListing.id)
        self.assertEqual(found.func, views.add_sequence)
         
        response = self.client.get(reverse('sequencelistings:add_seq', 
                                           args=[self.sequenceListing.id]))
#         test that the page returns expected html contents
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sequence name")
        self.assertContains(response, "Molecule type")
        self.assertContains(response, "Residues")
        
    def test_import_sequence_view(self):
        """
        The form import_seq is correctly displayed.
        """
        print 'Running %s ...' % getName()
#         test that URL resolves to correct views function        
        found = resolve('/sequencelistings/sl%d/import_seq/' % self.sequenceListing.id)
        self.assertEqual(found.func, views.import_sequence)
          
        response = self.client.get(reverse('sequencelistings:import_seq', 
                                           args=[self.sequenceListing.id]))
#         test that the page returns expected html contents
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sequence name")
        self.assertContains(response, "Molecule type")
        self.assertContains(response, "File")
        self.assertContains(response, "Upload file")
      
    def test_add_title_view(self):
         
        print 'Running %s ...' % getName()
#         test that URL resolves to correct views function        
        found = resolve('/sequencelistings/sl%d/add_title/' % self.sequenceListing.id)
        self.assertEqual(found.func, views.add_title)
 
        response = self.client.get(reverse('sequencelistings:add_title', 
                                           args=[self.sequenceListing.id]))
 
#         test that the page returns expected html contents
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invention title language code:")
        self.assertContains(response, "Submit")
#         TODO: continue if necessary
               
    def test_add_feature_view(self):
        """
        The form add_feature is correctly displayed.
        """
        print 'Running %s ...' % getName()
         
        seq = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
#         test that URL resolves to correct views function
        found = resolve('/sequencelistings/sl%d/seq%d/add_feature/' % (self.sequenceListing.id, seq.id))
        self.assertEqual(found.func, views.add_feature)
         
        response = self.client.get(reverse('sequencelistings:add_feature', 
                                           args=[self.sequenceListing.id, seq.id]))
        self.assertEqual(response.status_code, 200)
#         test that the page returns expected html contents
        self.assertContains(response, "Feature key")
        self.assertContains(response, "Submit")
        
    def test_add_multiple_feature_view(self):
        print 'Running %s ...' % getName()
         
        seq = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
#         test that URL resolves to correct views function
        found = resolve('/sequencelistings/sl%d/seq%d/add_multiple_feature/' % (self.sequenceListing.id, seq.id))
        self.assertEqual(found.func, views.add_multiple_feature)
         
        response = self.client.get(reverse('sequencelistings:add_multiple_feature', 
                                           args=[self.sequenceListing.id, seq.id]))
        self.assertEqual(response.status_code, 200)
#         test that the page returns expected html contents
        self.assertContains(response, "Add multiple feature")
        self.assertContains(response, "Qualifier value:")
        self.assertContains(response, "Submit")
         
    def test_edit_feature_view(self):
        """
        The form edit_feature is correctly displayed.
        """
        print 'Running %s ...' % getName()
        seq = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        f1 = seq.feature_set.all()[0]
#         test that URL resolves to correct views function        
        found = resolve('/sequencelistings/sl%d/seq%d/f%d/edit_feature/' % (self.sequenceListing.id, seq.id, f1.id))
        self.assertEqual(found.func, views.edit_feature)
         
        f = Feature.objects.create(sequence=seq, 
                                    featureKey='modified_base', 
                                    location='7')
         
        response = self.client.get(reverse('sequencelistings:edit_feature', args=[self.sequenceListing.id, seq.id, f.id]))
         
        self.assertEqual(response.status_code, 200)
#         test that the page returns expected html contents
        self.assertContains(response, "Feature key")
        self.assertContains(response, "7")
        self.assertContains(response, "Update")
         
    def test_add_qualifier_view(self):
        """
        The form add_qualifier is correctly displayed.
        """
        print 'Running %s ...' % getName()
         
        seq = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        f = seq.feature_set.all()[0]
#         test that URL resolves to correct views function        
        found = resolve('/sequencelistings/sl%d/seq%d/f%d/add_qualifier/' % (self.sequenceListing.id, seq.id, f.id))
        self.assertEqual(found.func, views.add_qualifier)
         
        response = self.client.get(reverse('sequencelistings:add_qualifier', 
                                           args=[self.sequenceListing.id, seq.id, f.id]))
        self.assertEqual(response.status_code, 200)
#         test that the page returns expected html contents
        self.assertContains(response, "Feature: source at location 1..")
        self.assertContains(response, "Qualifier name:")
        self.assertContains(response, "Qualifier value:")
          
    def test_xmloutput_view(self):
        """
        The generated xml file (xmloutput) is correctly displayed.
        """
        print 'Running %s ...' % getName()
              
        self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
 
        response = self.client.get(reverse('sequencelistings:xmloutput', args=[self.sequenceListing.pk, ]))
        self.assertEqual(response.status_code, 200)
#         test that the page returns expected html contents
#         self.assertContains(response, '%s.xml' % self.sequenceListing.fileName)
        self.assertContains(response, self.sequenceListing.fileName)
 
    def test_about_view(self):
        """
        The about_view page is correctly displayed.
        """
        print 'Running %s ...' % getName()
#         test that URL resolves to correct views function        
        found = resolve('/sequencelistings/about/')
        self.assertEqual(found.func, views.about)
         
        self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
 
        response = self.client.get(reverse('sequencelistings:about'))
        self.assertEqual(response.status_code, 200)
 
#         test that the page returns expected html contents
        self.assertContains(response, 'About')
        self.assertContains(response, 'only for information purposes')
     
# #     not sure how to implement this test ...
#     def test_download_view(self):
#         
#         print 'Running %s ...' % getName()
#         
#         found = resolve('/sequencelistings/download/test_xmlsql.xml')
#         self.assertEqual(found.func, views.download)
  
class ModelsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ModelsTests, cls).setUpClass()
        cls.sequenceListingFixture = SequenceListingFixture()
             
    def setUp(self):
        self.sequenceListing = self.sequenceListingFixture.create_sequencelisting_instance()
         
    def tearDown(self):
        TestCase.tearDown(self)
        self.sequenceListing.delete()
     
    def test_saving_and_retrieving_sequenceListings(self):
        print 'Running %s ...' % getName()
         
        second_seql = self.sequenceListingFixture.create_sequencelisting_instance()
        second_seql.fileName = 'abc'
        second_seql.save()
         
        saved_seqls = SequenceListing.objects.all()
        self.assertEqual(2, saved_seqls.count())
         
        first_saved_seql = saved_seqls[0]
        second_saved_seql = saved_seqls[1]
         
        self.assertEqual('test_xmlsql', first_saved_seql.fileName)
        self.assertEqual('abc', second_saved_seql.fileName)
         
        self.assertTrue(self.sequenceListing.isEditable, 'By default, a seql is editable.')
 
    def test_saving_and_retrieving_seql_no_inventor(self):
        sl = SequenceListing.objects.create(
            fileName = 'test_xmlsql_no_inventor',
            dtdVersion = '1',
            softwareName = 'prototype',
            softwareVersion = '0.1',
            productionDate = timezone.now().date(),
               
            applicantFileReference = '123',
        
            IPOfficeCode = 'EP',
            applicationNumberText = '2015123456',
            filingDate = timezone.now().date(),
            
            earliestPriorityIPOfficeCode = 'US',
            earliestPriorityApplicationNumberText = '998877',
            earliestPriorityFilingDate = timezone.now().date(),
            
            applicantName = 'John Smith',
            applicantNameLanguageCode = 'EN',
            applicantNameLatin = 'same',
                    
            )
         
        saved_seqls = SequenceListing.objects.all()
        self.assertEqual(2, saved_seqls.count())
         
        second_saved_seql = saved_seqls[1]
        self.assertEqual('test_xmlsql_no_inventor', second_saved_seql.fileName)
        self.assertEqual('', second_saved_seql.inventorName)
        self.assertEqual('', second_saved_seql.inventorNameLanguageCode)
        self.assertEqual('', second_saved_seql.inventorNameLatin)
     
    def test_saving_and_retrieving_seql_no_applicationIdentification(self):
        sl = SequenceListing.objects.create(
            fileName = 'test_xmlsql_no_applicationIdentification',
            dtdVersion = '1',
            softwareName = 'prototype',
            softwareVersion = '0.1',
            productionDate = timezone.now().date(),
               
            applicantFileReference = '123',
             
            earliestPriorityIPOfficeCode = 'US',
            earliestPriorityApplicationNumberText = '998877',
            earliestPriorityFilingDate = timezone.now().date(),
            
            applicantName = 'John Smith',
            applicantNameLanguageCode = 'EN',
            applicantNameLatin = 'same',
                    
            )
         
        saved_seqls = SequenceListing.objects.all()
        self.assertEqual(2, saved_seqls.count())
         
        second_saved_seql = saved_seqls[1]
        self.assertEqual('test_xmlsql_no_applicationIdentification', second_saved_seql.fileName)
        self.assertEqual('', second_saved_seql.IPOfficeCode)
        self.assertEqual('', second_saved_seql.applicationNumberText)
        self.assertEqual(None, second_saved_seql.filingDate)
         
    def test_saving_and_retrieving_sequences(self):
        print 'Running %s ...' % getName()
         
        self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        self.sequenceListingFixture.create_custom_sequence_instance(self.sequenceListing,
                    'AA', 'MRSVTF', 'Mus musculus', 'protein')
 
        saved_seqs = Sequence.objects.all()
        self.assertEqual(2, saved_seqs.count())
         
        first_saved_seq = saved_seqs[0]
        second_saved_seq = saved_seqs[1]
          
        self.assertEqual('DNA', first_saved_seq.moltype)
        self.assertEqual('AA', second_saved_seq.moltype)
        
#         test that the sequenceName is properly set
        self.assertEqual('test_seq_1', first_saved_seq.sequenceName)
        self.assertEqual('test_seq_2', second_saved_seq.sequenceName)

#         test that skipped is set to default, False        
        self.assertFalse(first_saved_seq.skipped)
        self.assertFalse(second_saved_seq.skipped)

    def test_create_sequence(self):
        print 'Running %s ...' % getName()
        
        s1 = self.sequenceListingFixture.create_custom_sequence_instance(self.sequenceListing, 'RNA', 'acgtaataatagcca', 
                                            'Mus musculus', 'genomic DNA')
        self.assertEqual(self.sequenceListing, s1.sequenceListing)
        self.assertEqual('test_seq_1', s1.sequenceName)
        self.assertEqual('RNA', s1.moltype)
        self.assertEqual('acgtaataatagcca', s1.residues)
        self.assertFalse(s1.skipped)
        
#         test that skipped is properly set for short sequence 
        s2 = self.sequenceListingFixture.create_custom_sequence_instance(self.sequenceListing, 
                'DNA', 'acgt', 'Mus musculus', 'genomic DNA')
        self.assertEqual('acgt', s2.residues)
        self.assertTrue(s2.skipped)
        
    def test_edit_sequence(self):
        print 'Running %s ...' % getName()
        
        s1 = self.sequenceListingFixture.create_custom_sequence_instance(self.sequenceListing, 
                'RNA', 'acgtaataatagcca', 'Mus musculus', 'genomic DNA')
        self.assertEqual(self.sequenceListing, s1.sequenceListing)
        self.assertEqual('test_seq_1', s1.sequenceName)
        self.assertEqual('RNA', s1.moltype)
        self.assertEqual('acgtaataatagcca', s1.residues)
        self.assertFalse(s1.skipped)
        
        s1.moltype = 'DNA'
        s1.save()
        self.assertEqual('DNA', s1.moltype)
        s1.skipped = True
        s1.save()
        self.assertTrue(s1.skipped)
        s1.residues = 'acgt'
        s1.save()
        self.assertTrue(s1.skipped)
        
        
    def test_deleting_sequence(self):
        print 'Running %s ...' % getName()
         
        seq1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        seq2 = self.sequenceListingFixture.create_custom_sequence_instance(self.sequenceListing,
                    'AA', 'MRSVTF', 'Mus musculus', 'protein')
        seq3 = self.sequenceListingFixture.create_custom_sequence_instance(self.sequenceListing,
                    'AA', 'MRAVTQVRT', 'Felis catus', 'protein')
        seq4 = self.sequenceListingFixture.create_custom_sequence_instance(self.sequenceListing,
                    'DNA', 'cgtatacggattaccatatatacagagatacca', 'Tomato', 'protein')
         
        saved_seqs = Sequence.objects.all()
        self.assertEqual(4, saved_seqs.count())
        self.assertEqual(4, self.sequenceListing.sequenceTotalQuantity)
         
        first_saved_seq = saved_seqs[0]
        second_saved_seq = saved_seqs[1]
        third_saved_seq = saved_seqs[2]
        fourth_saved_seq = saved_seqs[3]
         
        self.assertEqual('DNA', first_saved_seq.moltype)
        self.assertEqual('AA', second_saved_seq.moltype)
        self.assertEqual(9, third_saved_seq.length)
        self.assertEqual('cgtatacggattaccatatatacagagatacca', fourth_saved_seq.residues)
     
        seq2.delete()
         
        self.assertEqual(3, self.sequenceListing.sequenceTotalQuantity)
         
        self.assertEqual(3, saved_seqs.count())
         
        saved_seqs = Sequence.objects.all()
         
#         remaining_seq = saved_seqs[0]
        self.assertEqual(1, saved_seqs[0].sequenceIdNo)
        self.assertEqual('DNA', saved_seqs[0].moltype)
         
        print saved_seqs[1]
         
        self.assertEqual(2, saved_seqs[1].sequenceIdNo)
        self.assertEqual('AA', saved_seqs[1].moltype)
        self.assertEqual('MRAVTQVRT', saved_seqs[1].residues)
         
        self.assertEqual(3, saved_seqs[2].sequenceIdNo)
        self.assertEqual('DNA', saved_seqs[2].moltype)
        self.assertEqual('cgtatacggattaccatatatacagagatacca', saved_seqs[2].residues)
         
     
#     TODO: add tests for other models 
                       
    def test_getOrganism(self):
        """
        Test that the Sequence object returns correctly the organism value.
        """
        print 'Running %s ...' % getName()
               
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)             
        self.assertEqual('Homo sapiens', s1.getOrganism())
                 
        s2 = Sequence.objects.create(
                sequenceListing = self.sequenceListing,
                moltype = 'AA',
                residues = 'MRTAVTAD')
        self.assertEqual(None, s2.getOrganism())
          
        views.feature_source_helper(s2, 'Drosophila melanogaster', 'protein')
        self.assertEqual('Drosophila melanogaster', s2.getOrganism())
                        
        s3 = Sequence.objects.create(
            sequenceListing = self.sequenceListing,
            moltype = 'RNA',
            residues = 'caucaucaucaucaucau')
          
        views.feature_source_helper(s3, 'Mus musculus', 'genomic RNA')
        self.assertEqual('Mus musculus', s3.getOrganism())
 
    def test_getOrderedFeatures(self):
        """
        Test that the Sequence object returns correctly the ordered features.
        """
        print 'Running %s ...' % getName()
               
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)             
        
#         test that source feature is at index 0 when feature table has only 1 feature 
        source_feature = next((f for f in s1.feature_set.all() if f.featureKey == 'source'), None)
        ordered_features = s1.getOrderedFeatures()
        self.assertTrue(source_feature)
        self.assertEqual(0, ordered_features.index(source_feature))
        
#         add feature
        f1_1 = Feature.objects.create(sequence=s1, 
                                      featureKey='misc_feature', 
                                      location='4')
        
        ordered_features_after_f1_1 = s1.getOrderedFeatures()
        
        self.assertEqual(0, ordered_features_after_f1_1.index(source_feature))
        self.assertEqual(1, ordered_features_after_f1_1.index(f1_1))
        
        #         add feature
        f1_2 = Feature.objects.create(sequence=s1, 
                                      featureKey='misc_feature', 
                                      location='2')
        
        ordered_features_after_f1_2 = s1.getOrderedFeatures()
        
        self.assertEqual(0, ordered_features_after_f1_2.index(source_feature))
        self.assertEqual(1, ordered_features_after_f1_2.index(f1_2))
        self.assertEqual(2, ordered_features_after_f1_2.index(f1_1))
        
        #         add feature
        f1_3 = Feature.objects.create(sequence=s1, 
                                      featureKey='variation', 
                                      location='9')
        
        ordered_features_after_f1_3 = s1.getOrderedFeatures()
        
        self.assertEqual(0, ordered_features_after_f1_3.index(source_feature))
        self.assertEqual(1, ordered_features_after_f1_3.index(f1_2))
        self.assertEqual(2, ordered_features_after_f1_3.index(f1_1))
        self.assertEqual(3, ordered_features_after_f1_3.index(f1_3))
        
        #         add feature
        f1_4 = Feature.objects.create(sequence=s1, 
                                      featureKey='allele', 
                                      location='9')
        
        ordered_features_after_f1_4 = s1.getOrderedFeatures()
        
        self.assertEqual(0, ordered_features_after_f1_4.index(source_feature))
        self.assertEqual(1, ordered_features_after_f1_4.index(f1_2))
        self.assertEqual(2, ordered_features_after_f1_4.index(f1_1))
        self.assertEqual(3, ordered_features_after_f1_4.index(f1_4))
        self.assertEqual(4, ordered_features_after_f1_4.index(f1_3))
        
        #         add feature
        f1_5 = Feature.objects.create(sequence=s1, 
                                      featureKey='iDNA', 
                                      location='9')
        
        ordered_features_after_f1_5 = s1.getOrderedFeatures()
        
        self.assertEqual(0, ordered_features_after_f1_5.index(source_feature))
        self.assertEqual(1, ordered_features_after_f1_5.index(f1_2))
        self.assertEqual(2, ordered_features_after_f1_5.index(f1_1))
        self.assertEqual(3, ordered_features_after_f1_5.index(f1_4))
        self.assertEqual(4, ordered_features_after_f1_5.index(f1_5))
        self.assertEqual(5, ordered_features_after_f1_5.index(f1_3))
        
        #         add feature this will be ordered before 'allele', because 
#         capital letters are lower than lower case in ASCII
        f1_6 = Feature.objects.create(sequence=s1, 
                                      featureKey='CDS', 
                                      location='9..17')
        
        ordered_features_after_f1_6 = s1.getOrderedFeatures()
        
        self.assertEqual(0, ordered_features_after_f1_6.index(source_feature))
        self.assertEqual(1, ordered_features_after_f1_6.index(f1_2))
        self.assertEqual(2, ordered_features_after_f1_6.index(f1_1))
        self.assertEqual(3, ordered_features_after_f1_6.index(f1_6))
        self.assertEqual(4, ordered_features_after_f1_6.index(f1_4))
        self.assertEqual(5, ordered_features_after_f1_6.index(f1_5))
        self.assertEqual(6, ordered_features_after_f1_6.index(f1_3))
        
 
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
        self.assertEqual([1,3,5,7,9], util.rangeFromString(s1))
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
#         TODO: generate some fancy sequences to check xml validation?
        util.helper_generateXml(sequenceListing)
         
        f =  os.path.join(util.OUTPUT_DIR, '%s.xml' % sequenceListing.fileName)
 
        self.assertTrue(util.validateDocumentWithSchema(f, util.XML_SCHEMA_PATH))
        self.assertTrue(util.validateDocumentWithDtd(f, util.XML_DTD_PATH))
        sequenceListing.delete()
 
    def test_validateDocumentWithSchema(self):
        """
        Test that xml sequence listing files are correctly validated 
        against the schema.
        """
        print 'Running %s ...' % getName()
                    
#         valid seql contains the first 2 seqs from f2 - goes via if branch
        f3 = os.path.join(util.TEST_DATA_DIR_PATH, 'test3.xml')
        self.assertTrue(util.validateDocumentWithSchema(f3, util.XML_SCHEMA_PATH))
   
#         ApplicantNamex instead of ApplicantName - goes to except branch
        f4 = os.path.join(util.TEST_DATA_DIR_PATH, 'test4.xml')        
        self.assertFalse(util.validateDocumentWithSchema(f4, util.XML_SCHEMA_PATH))
   
#         SOURCxE instead of SOURCE - goes to else branch 
        f5 = os.path.join(util.TEST_DATA_DIR_PATH, 'test5.xml')        
        self.assertFalse(util.validateDocumentWithSchema(f5, util.XML_SCHEMA_PATH))
  
#         supplementary test with seql with more sequences
#         valid seql 20 sequences
        f2 = os.path.join(util.TEST_DATA_DIR_PATH, 'test2.xml')
        self.assertTrue(util.validateDocumentWithSchema(f2, util.XML_SCHEMA_PATH))
 
#         SequenceTotalQuantity element is missing
# TODO: the error msg says that EarliestPriorityApplicationIdentification is expected: /Users/ad/pyton/projects/st26proto/authoringtool/sequencelistings/testData/test8.xml:42:0:ERROR:SCHEMASV:SCHEMAV_ELEMENT_CONTENT: Element 'SequenceData': This element is not expected. Expected is ( EarliestPriorityApplicationIdentification ).
        f8 = os.path.join(util.TEST_DATA_DIR_PATH, 'test8.xml')
        self.assertFalse(util.validateDocumentWithSchema(f8, util.XML_SCHEMA_PATH))
       
#         skipped sequences
        f9 = os.path.join(util.TEST_DATA_DIR_PATH, 'test9.xml')
        self.assertTrue(util.validateDocumentWithSchema(f9, util.XML_SCHEMA_PATH))

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
            
class FormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(FormsTests, cls).setUpClass()
        cls.sequenceListingFixture = SequenceListingFixture()
              
    def setUp(self):
        self.sequenceListing = self.sequenceListingFixture.create_sequencelisting_instance()
              
    def tearDown(self):
        TestCase.tearDown(self)
        self.sequenceListing.delete()
          
    def test_qualifierForm(self):
        """
        Test the qualifier form.
        """
        print 'Running %s ...' % getName()
              
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
   
        f1 = Feature.objects.create(sequence=s1, 
                                    featureKey='modified_base', 
                                    location='7')
        qf1 = QualifierForm(feature=f1, 
                            data={'qualifierName': 'note',
                                  'qualifierValue':'test for value'})
               
        self.assertTrue(qf1.is_valid())
        self.assertEqual('note', qf1.cleaned_data['qualifierName'])  
              
        qf2 = QualifierForm(feature=f1, 
                            data={'qualifierName': 'xxx',
                                  'qualifierValue':'test for xxx value'})
               
        self.assertTrue(qf2.is_valid())


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                          os.path.join(util.PROJECT_DIRECTORY,
                                       'authoringtool', 'settings.py'))
    # unittest.main()