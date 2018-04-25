from django.db import models
import util 
from django.core.exceptions import ObjectDoesNotExist, ValidationError 
from django.core.validators import RegexValidator 
import re 
import datetime 

regex_nuc = '^[a,c,g,t,u,n,v,k,r,s,b,h,d]{10,}$' #TODO: add the full set of valid chars
regex_prt = '^[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J,B,Z]{4,}$'
pattern_nuc = re.compile(regex_nuc)
pattern_prt = re.compile(regex_prt)
        

class SequenceListing(models.Model):
#     xml attributes
    fileName = models.CharField('File name', max_length=100)
    dtdVersion = models.CharField('DTD version', max_length=10)
    softwareName = models.CharField('Software name', max_length=50)
    softwareVersion = models.CharField('Software version', max_length=100)
    productionDate = models.DateField('Production date')

#     xml children (except sequences which are represented as a separate Model)
    
    IPOfficeCode = models.CharField('IP office code', max_length=2, 
                                    blank=True,
                                    help_text='Valid format: WIPO ST.3 code')
    applicationNumberText = models.CharField('Application number text', 
                                    max_length=20,
                                    blank=True)
    filingDate = models.DateField('Filing date', 
                                  blank=True, null=True,
                                  help_text='Valid date format: WIPO ST.2 YYYY-MM-DD')

    applicantFileReference = models.CharField('Applicant file reference', max_length=30)
    
    earliestPriorityIPOfficeCode = models.CharField('Earliest priority IP office code', 
                                        max_length=2, 
                                        blank=True, 
                                        help_text='Valid format: WIPO ST.3 code')
    earliestPriorityApplicationNumberText = models.CharField('Earliest priority application number text', 
                                                             max_length=20, 
                                                             blank=True)
    earliestPriorityFilingDate = models.DateField('Earliest priority filing date', 
                                                  blank=True, null=True,
                                                  help_text='Valid date format: WIPO ST.2 YYYY-MM-DD')

    applicantName = models.CharField('Applicant name', max_length=200)
    applicantNameLanguageCode = models.CharField('Applicant name language code', 
                                    max_length=2, 
                                    help_text='Valid format: ISO 639-1')
    applicantNameLatin = models.CharField('Applicant name Latin', max_length=200, 
                                          blank=True)

    inventorName = models.CharField('Inventor name', max_length=200, blank=True)
    inventorNameLanguageCode = models.CharField('Inventor name language code', 
                                                max_length=2,
                                                blank=True, 
                                                help_text='Valid format: ISO 639-1')
    inventorNameLatin = models.CharField('Inventor name Latin', max_length=200, blank=True)
    
    sequenceTotalQuantity = models.IntegerField('Sequence total quantity', default=0)
    
    isEditable = models.BooleanField('Is editable', default=True) # not part of ST.26, just for prototyping
        
    def __unicode__(self):
        return 'Sequence listing %s' %self.fileName
    
    def getFirstTitle(self):
        return self.title_set.all()[0].inventionTitle
    
    def getFormattedProductionDate(self):
        return datetime.datetime.strftime(self.productionDate, '%Y-%m-%d')
    
    def getFormattedFilingDate(self):
        return datetime.datetime.strftime(self.filingDate, '%Y-%m-%d')
    
    def getFormattedEarliestPriorityFilingDate(self):
        return datetime.datetime.strftime(self.earliestPriorityFilingDate, '%Y-%m-%d')

    
class Title(models.Model):
    sequenceListing = models.ForeignKey(SequenceListing) 
    inventionTitle = models.CharField('Invention title', max_length=200)
    inventionTitleLanguageCode = models.CharField('Invention title language code', 
                                                  max_length=2, 
                                                  help_text='Valid format: ISO 639-1')

    def __unicode__(self):
        return '%s / title %s (%s)' % (self.sequenceListing, 
                                       self.inventionTitle, 
                                       self.inventionTitleLanguageCode)


class Sequence(models.Model): #good
    class Meta:
        ordering = ['sequenceIdNo']
    
    sequenceListing = models.ForeignKey(SequenceListing)
    
    sequenceIdNo = models.IntegerField('SEQ. ID. NO.', default=0)
    sequenceName = models.CharField('Sequence name', max_length=100)
    length = models.IntegerField('Length', default=0)
    moltype = models.CharField('Molecule type', max_length=3, choices=util.MOLTYPE_CHOICES)
    division = models.CharField('Division', max_length=3, default='PAT')
    otherSeqId = models.CharField('Other seq ID', max_length=100, default='-')
 
    residues = models.TextField()
    
    skipped = models.BooleanField('Skipped', default=False)
 
    def __unicode__(self):
        return str(self.sequenceListing) + ' / seq ' + str(self.sequenceIdNo)
         
    def save(self, *args, **kwargs):
        if not self.pk: # so it's an INSERT, not UPDATE
            self.sequenceIdNo = self.sequenceListing.sequenceTotalQuantity + 1
            self.sequenceListing.sequenceTotalQuantity += 1
            self.sequenceListing.save()
        self.residues = util.expandFormula(self.residues)
        self.length = len(self.residues)
        super(Sequence, self).save(*args, **kwargs)
        
#     def delete(self, *args, **kwargs):
#         currentSequenceIdNo = self.sequenceIdNo
# #         allSequences = self.sequenceListing.sequence_set.filter(sequenceIdNo > currentSequenceIdNo)
#         allSubsequentSequences = Sequence.objects.filter(sequenceListing = self.sequenceListing).filter(sequenceIdNo__gt=currentSequenceIdNo)
#         super(Sequence, self).delete(*args, **kwargs)
#         for seq in allSubsequentSequences:
#             seq.sequenceIdNo -= seq.sequenceIdNo
#             seq.save()
#              
#         self.sequenceListing.sequenceTotalQuantity -= 1
#         self.sequenceListing.save()
         
        
        
#     TODO: reinstate it as appropriate. Disabled so that ImportSequenceForm 
#     can be used in the new implementation as ext of ModelForm
    def clean(self):
        if self.moltype == 'AA':
            p = pattern_prt  
        else:
            p = pattern_nuc
        self.residues = util.expandFormula(self.residues)
        
#         if not p.match(self.residues):
#             raise ValidationError('Enter a valid residue symbol.')
    
#     this method is to be used only temporarily for Berthold; 20160710 TO REtain it!  
    def delete(self, *args, **kwargs):
        subsequentSequencesSet = self.sequenceListing.sequence_set.filter(sequenceIdNo__gt=self.sequenceIdNo)
        super(Sequence, self).delete(*args, **kwargs)
        self.sequenceListing.sequenceTotalQuantity = len(self.sequenceListing.sequence_set.all())
        self.sequenceListing.save()
        for s in subsequentSequencesSet:
            oldSequenceIdNo = int(s.sequenceIdNo)
            s.sequenceIdNo = oldSequenceIdNo - 1
            s.save()
#         print 'SEQ ID NO %i from sequence listing %s has been deleted.' %(self.sequenceIdNo, self.sequenceListing.pk)
    
        
    def inspectSequence(self):
        print 'sequenceListing', self.sequenceListing 
        print 'sequenceIdNo', self.sequenceIdNo
        print 'sequenceName', self.sequenceName
        print 'length', self.length
        print 'moltype', self.moltype
        print 'division', self.division
        print 'otherSeqId', self.otherSeqId
        print 'residues', self.residues
        
    def getOrganism(self):
        result = None
        
        sourceFeatureKey = 'source'
        organismQualifierName = 'organism'
        
        if self.moltype == 'AA':
            sourceFeatureKey = 'SOURCE'
            organismQualifierName = 'ORGANISM'
        try:
            sourceFeature = self.feature_set.get(featureKey=sourceFeatureKey)
            organismQualifier = sourceFeature.qualifier_set.get(qualifierName = organismQualifierName)
            
        except ObjectDoesNotExist:
            organismQualifier = None
        
        if organismQualifier:
            result = organismQualifier.qualifierValue
            
        return result
    
    def getOrderedFeatures(self):
        """
        Return a sorted list of the Feature instances of this sequence.
        The ordering is: first the source feature, then the other features 
        sorted ascending by the start location and alphabetically ascending 
        for the same start location.
        """
        
        unordered_features = self.feature_set.all()
        ordered_features = sorted(unordered_features, 
                                  key = lambda feat: (util.getStartLocation(feat.location), 
                                                      feat.featureKey))
        
        source_feature = next((f for f in ordered_features if f.featureKey in ['source', 'SOURCE']), None)
        
        if source_feature:
            index_of_source_feature = ordered_features.index(source_feature)
            if index_of_source_feature != 0:
                ordered_features.insert(0, ordered_features.pop(index_of_source_feature))
        
        return ordered_features  
 
class Feature(models.Model):
    sequence = models.ForeignKey(Sequence)
    featureKey = models.CharField('Feature key', max_length=100,
#                                                 choices=DNA_FEATURE_KEY_CHOICES,
                                                )
    location = models.CharField('Location', max_length=100)
    
    def __unicode__(self):
        return str(self.sequence) + ' / ' + self.featureKey  + ' / ' + self.location

class Qualifier(models.Model):
    feature = models.ForeignKey(Feature)
    qualifierName = models.CharField('Qualifier name', max_length=100)
    qualifierValue = models.CharField('Qualifier value', max_length=1000)

    def __unicode__(self):
        return str(self.feature) + ' / ' + self.qualifierName


