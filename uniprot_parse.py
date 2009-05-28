#! /usr/bin/env python
###################
# Read data from a Uniprot XML dump
###################

import sys, re, textwrap
import xml.etree.ElementTree as ET

# XML work
ns = '{http://uniprot.org/uniprot}'

tree = ET.parse('infile.xml')

def GetName(self):
    '''Get the name of the protein'''
    try:
        name = protein.find(ns+'protein').find(ns+'recommendedName').findtext(ns+'fullName')
    except:
        name = protein.find(ns+'protein').find(ns+'submittedName').findtext(ns+'fullName')
    return name

def GetGeneName(self):
    '''Get the gene name'''
    try:
        gene_name = protein.find(ns+'gene').findtext(ns+'name')
    except:
        # Have to invent short names for proteins that don't have one
        try:
            fullname = protein.find(ns+'protein').find(ns+'recommendedName').findtext(ns+'fullName')
        except:
            fullname = protein.find(ns+'protein').find(ns+'submittedName').findtext(ns+'fullName')
        gene_name = fullname[0:13]
    return gene_name
    
def GetAccessions(self):
    '''Get all accession codes for this protein'''
    accession_list = []
    accessions = protein.findall(ns+'accession')
    for accession in accessions:
        accession_list.append(accession.text)
    return accession_list

def GetSequence(self):
    '''Retrieve the protein sequence'''
    sequence = protein.findtext(ns+'sequence')
    seq_clean = re.sub("\s+", "", sequence)
    seq_wrapped = textwrap.fill(seq_clean, 60)
    return seq_wrapped
  
def GetDomain(self):
    '''Return domains with start and stop positions'''
    domain_dict = {}
    domain_list = []
    domains = protein.findall(ns+'feature')
    # This loop seems cumbersome
    for feature in domains:
        if feature.get('type') == 'domain':
            domain_list.append(feature)
            for domain in domain_list:
                domain_start = feature.find(ns+'location').find(ns+'begin').get('position')
                domain_stop = feature.find(ns+'location').find(ns+'end').get('position')
                domain_span = domain_start+'-'+domain_stop
                domain_dict[feature.get('description')]= domain_span
    return domain_dict

# Let's do it
for item in tree.getiterator(ns+'uniprot'):
    proteins = item.findall(ns+'entry')
    for protein in proteins:
        print GetName(item)
        print GetGeneName(item)
        print GetAccessions(item)
        print GetSequence(item)
        print GetDomain(item)
        print '------------\n'
