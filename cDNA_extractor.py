#! /usr/bin/env python

# http://biostumblematic.wordpress.com

# Extraction of the cDNA
# for a given protein domain
# input CSV file should be one line per protein, in the format:
# [SwissProt ID],[Domain start residue],[Domain stop],[cDNA sequence]

import re, csv, sys
from Bio import ExPASy, SwissProt, SeqIO
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC

reader = csv.reader(open('test.csv'))
for row in reader:
    input_prot = row[0]
    get_prot = ExPASy.get_sprot_raw(input_prot)
#    prot_obj = SeqIO.read(get_prot, "swiss")
    prot_record = SwissProt.read(get_prot)
    get_prot.close()
    prot_seq = prot_record.sequence
#    prot_seq = prot_obj.seq
    prot_gene = prot_record.gene_name
    prot_domain = prot_seq[int(row[1])-1:int(row[2])]
    cdna = Seq(row[3], IUPAC.unambiguous_dna)

    outputfile = open('cDNA_extracted.csv', 'w')
    writer = csv.writer(outputfile)
    i=0
    # Steps through each possible frame of the input cDNA
    while i < 3:
        extracted = []
        frame = cdna[i::]
        trans = frame.translate()
        orf_find = re.search(str(prot_domain), str(trans))
        if orf_find:
            trans_split = re.split('('+str(prot_domain)+')', str(trans))
            # This seems like a sloppy way to get these positions
            cdna_start = len(trans_split[0])*3
            cdna_stop = cdna_start + len(trans_split[1])*3
            cdna_extracted = frame[cdna_start:cdna_stop]
            extracted.append(prot_gene)
            extracted.append(cdna_extracted)
            writer.writerow(extracted)
        else:
            pass
        i += 1
outputfile.close()
