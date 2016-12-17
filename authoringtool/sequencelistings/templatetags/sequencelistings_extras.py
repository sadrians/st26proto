'''
Created on Feb 2, 2016

@author: ad
'''

from django import template
from sequencelistings.models import SequenceListing, Sequence 
from sequencelistings.util import getStartLocation

register = template.Library()

@register.inclusion_tag('sequencelistings/seqls.html')
def get_sequenceListing_list(sequenceListing=None):
    """used for populating the sidebar with links to sequence listings"""
    return {'seqls': SequenceListing.objects.all(), 'act_seql': sequenceListing}

# @register.filter(name='get_ordered_features')
# def get_ordered_features(aSequence):
#     """
#     Return a sorted list of the Feature instances of aSequence.
#     The ordering is: first the source feature, then the other features 
#     sorted ascending by the start location.
#     """
#     
#     unordered_features = aSequence.feature_set.all()
#     ordered_features = sorted(unordered_features, key = lambda feat: getStartLocation(feat.location))
#     
#     source_feature = next((f for f in ordered_features if f.key in ['source', 'SOURCE']), None)
#     
#     if source_feature:
#         index_of_source_feature = ordered_features.index(source_feature)
#         if index_of_source_feature != 0:
#             ordered_features.insert(0, ordered_features.pop(index_of_source_feature))
#     
#     return ordered_features 

#     it is expected that len(source_feature) is always 1, 
#     i.e. aSequence has exactly one source feature