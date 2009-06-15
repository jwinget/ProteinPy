#!/usr/bin/env python
# http://biostumblematic.wordpress.com

import string
from Bio import AlignIO

# change input.fasta to match your alignment
input_handle = open("input.fasta", "rU")
alignment = AlignIO.read(input_handle, "fasta")

j=0 # counts positions in first sequence
i=0 # counts identity hits 
for record in alignment:
    for amino_acid in record.seq:
        if amino_acid == '-':
            pass
        else:
            if amino_acid == alignment[0].seq[j]:
                i += 1
        j += 1
    j = 0
    seq = str(record.seq)
    gap_strip = seq.replace('-', '')
    percent = 100*i/len(gap_strip)
    print record.id+' '+str(percent)
    i=0
