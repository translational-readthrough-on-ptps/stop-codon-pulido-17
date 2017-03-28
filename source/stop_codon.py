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





def reverseComplement(seq):
    sequence = seq*1
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    return "".join([complement.get(nt, '') for nt in sequence[::-1]])


def format_chain(seq, start):
    seq = seq[0:start] + " " + \
          " ".join(seq[i:i+3] for i in range(start, len(seq) - start, 3)) \
          + " " + seq[len(seq) - start:]
    return seq


def create_seq():
    f = open('chain.txt', 'r')
    seq = f.read()
    f.close()
    return seq


def clean_seq(seq):
    # seq treatment
    seq = re.sub(r'\W', '', seq)  # remove all spaces/blanks/newlines
    seq = re.sub('[^a-zA-Z]', '', seq)  # remove all non LETTER char
    seq = seq.upper()
    return seq


def start_seq(seq):
    try:
        start_pos = int(input('Tell me the position you would like to \
                          start (1 by default): \n'))
    except:
        start_pos = 1

    start_pos -= 1
    print('You selected', seq[start_pos:start_pos+10],
          'as your starting point')

    seq = seq[start_pos:]  # delete the rest of the chain
    return seq


def get_info():
    oligo_assert = False
    while not oligo_assert:
        try:
            oligo_num = int(input('Tell me the length of oligos: \n'))
            side_num = 0

            if (oligo_num-3) % 2 != 0 or (oligo_num-3) <= 0:
                print('Incorrect number of oligos, insert a correct one')
            else:
                print('Number of oligos accepted')
                oligo_assert = True
                side_num = (oligo_num-3) // 2
        except:
            print('Insert a number, please')

    try:
        line_num = int(input('Tell me the line you would like to print as \
        the first one in your output file (1 by default): \n'))
    except:
        line_num = 1

    return oligo_num, side_num, line_num


if __name__ == "__main__":

    seq = create_seq()
    seq = clean_seq(seq)
    print('Your chains first 20:\n', seq[0:20], '\n')

    seq = start_seq(seq)
    print('Your chain now is', seq[:10], '...')

    oligo_num, side_num, line_num = get_info()

    global codon_table
    fname = "stop_codon_info.txt"
    sc_info = open(fname, 'w')

    fname = "stop_codon_replacement.txt"
    sc_replacement = open(fname, 'w')

    print('Processing...')
    for x_ in range(0, len(seq), 3):
        try:
            codon = seq[x_:x_+3]
        except:
            break

        if codon in codon_change_to_stop_codon.keys():

            sc_info.write(codon_table[codon] + str(x_ // 3) + " (" + codon + \
                          ")" + " -> " + \
                          str(codon_change_to_stop_codon[codon]) + '\n')

            chain = seq[x_: x_+oligo_num]
            if len(chain) != oligo_num:
                break

            for new_codon in codon_change_to_stop_codon[codon]:
                new_chain = chain[:side_num] + new_codon + chain[side_num+3:]
                chain_rev = reverseComplement(new_chain)

                sc_replacement.write(str(line_num) + "  " + codon_table[codon] + str(x_ // 3) + " " + new_chain + '\n')
                sc_replacement.write(str(line_num) + "  " + codon_table[codon] + str(x_ // 3) + " " + chain_rev + '\n \n')

                line_num += 2

    sc_info.close()
    sc_replacement.close()
    print('Results in stop_codon_info.txt')
    print('Results in stop_codon_replacement.txt')
