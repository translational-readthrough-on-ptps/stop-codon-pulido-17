# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 12:55:04 2015

@author: asier
"""

# -*- coding: utf-8 -*-
import re

# mystr = "I want to Remove all white \t spaces, new lines \n and tabs \t"
# print re.sub(r"\W", "", mystr)

bases = ['T', 'C', 'A', 'G']
codons = [a+b+c for a in bases for b in bases for c in bases]
amino_acids = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
codon_table = dict(zip(codons, amino_acids))

stop_codons = ["TAG", "TAA", "TGA"]

codon_change_to_stop_codon = {  # TAG TAA TGA
                              "TTA": ["TGA", "TAA"], "TCA": ["TGA", "TAA"],
                              "TAT": ["TAG", "TAA"], "TAC": ["TAG", "TAA"],
                              "TGT": ["TGA"], "TGC": ["TGA"],
                              "TGG": ["TAG"], "TTG": ["TAG"],
                              "CAA": ["TAA"], "CAG": ["TAG"],
                              "CGA": ["TGA"], "AAA": ["TAA"],
                              "AAG": ["TAG"], "AGA": ["TGA"],
                              "GAA": ["TAA"], "GAG": ["TAG"],
                              "GGA": ["TGA"], "TCG": ["TAG"]
                              }


def chain_rep(chain, start):
    global codon_table

    codon = chain[start:start+3]
    if codon_table[codon] == '*':  # warning
        print('Warning: Stop codon found in your chain. Revise your chain\n',
              seq[0:20], '\n')
    else:  # substitute for stop-codon
        codon = codon_change_to_stop_codon[codon]
    chain = chain[:start] + codon + chain[start+3:]
    return chain


def reverseComplement(seq):
    sequence = seq*1
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    return "".join([complement.get(nt, '') for nt in sequence[::-1]])


def format_chain(seq, start):
    seq = seq[0:start] + " " + \
          " ".join(seq[i:i+3] for i in range(start, len(seq) - start, 3)) \
          + " " + seq[len(seq) - start:]
    return seq


if __name__ == "__main__":

    f = open('chain.txt', 'r')
    seq = f.read()
    f.close()

    # seq treatment
    seq = re.sub(r'\W', '', seq)  # remove all spaces/blanks/newlines
    seq = re.sub('[^a-zA-Z]', '', seq)  # remove all non LETTER char
    seq = seq.upper()

    print('Your chains first 20:\n', seq[0:20], '\n')

    try:
        start_pos = input('Tell me the position you would like to \
                          start (1 by default): \n')
    except:
        start_pos = 1

    start_pos -= 1
    print('You selected', seq[start_pos:start_pos+10],
          'as your starting point')

    seq = seq[start_pos:]  # delete the rest of the chain

    print('Your chain now is', seq[:10], '...')

    oligo_assert = False
    while not oligo_assert:
        try:
            oligo_num = input('Tell me the length of oligos: \n')
            side_num = 0

            if (oligo_num-3) % 2 != 0 or (oligo_num-3) <= 0:
                print('Incorrect number of oligos, insert a correct one')
            else:
                print('Number of oligos accepted')
                oligo_assert = True
                side_num = (oligo_num-3) / 2
        except:
            print('Insert a number, please')

    try:
        line_num = input('Tell me the line you would like to print as \
        the first one in your output file (1 by default): \n')
    except:
        line_num = 1

    fname = "new_chain.txt"
    file = open(fname, 'w')

    print('Processing...')
    for x_ in range(0, len(seq), 3):

        chain = seq[x_: x_+oligo_num]

        if len(chain) != oligo_num:
            break

        chain = chain_rep(chain, side_num)
        chain_rev = reverseComplement(chain)

        file.write(str(line_num) + " " + chain + '\n')
        file.write(str(line_num+1) + " " + chain_rev + '\n \n')

        line_num += 2

    file.close()
    print('Results in new_chain.txt')
