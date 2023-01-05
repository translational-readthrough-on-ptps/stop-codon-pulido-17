# PTCMAKER

## User Manual PTCMAKER

### Before using PTCMAKER:

- The program provides information on the premature termination codons (PTC) which can be generated from a cDNA sequence by single-nucleotide substitutions targeting the 18 potential PTC-generating eukaryotic codons. The program provides a full list of PTC (potential PTCome) with information on the targeted and the adjacent codons. The number and identity of the targeted codons, PTC, and PTC containing a cytosine (C) at position +4 (position +1 being the first nucleotide from the PTC) is also provided.
- The program also generates mutagenic oligonucleotide
primers of pre-defined length to obtain the desired PTC
variants by PCR oligonucleotide site-directed mutagenesis,
as described (Mingo et al., PLoS One, 11(8):e0160972,
2016). The forward and reverse mutagenic primers for each
mutation are fully complementary, and all primers have the
same length, which is defined by the user. The mutated PTC
(3 nucleotides) is placed in the middle of the primer, with
an equal number of nucleotides 5’ and 3’ to it. Therefore,
the defined length of mutagenic primers has to be an odd
number: n+3+n, where n is any number usually between 10 and
20 (the default n in the program is 13, which renders
primers 29-mer). Take into consideration that to generate
PTC at the N-terminal or C-terminal parts of your protein,
you will need portions of the nucleotide sequence from the
vector where your cDNA is cloned.
- **Input**: the program accepts as input **.txt files**
containing the cDNA sequence of interest, and ignores
numbers, non-letter characters, spaces, or line breaks. The
first letter in the .txt file is considered the first
position from the chain (sequence to be mutagenized).
Therefore, letter characters other than the nucleotides
should be avoided in the file. The user defines where to
start the design of primers by defining the position to
start in the chain.
- **Output**: the program provides two new .txt files:
stop_codon_info, providing information on the potential
PTCome, as indicated above; and stop_codon_replacement,
providing a list of consecutively numbered PTC mutagenic
primers, forward and reverse, written 5’ to 3’. The
numbering of the first forward mutagenic primer and the
name of the .txt file can be defined by the user.

### Using PTCMAKER:

Take into account that the output txt.files with the potential PTCome
information and the mutagenic primers will be created in
the folder where the PTCMAKER program is opened. 

1. Download de .exe from https://github.com/translational-readthrough-on-ptps/ptc-maker 
3. Execute the program double clicking on the icon.
4. Click "Open" and browse for the .txt file containing the
nucleotide sequence to be analyzed.
4. Your nucleotide sequence (chain) is shown.
5. Define the length of the mutagenic primers (29 by
default).
6. Define the position from the chain at which you would
like to start the designing of mutagenic primers (1 by
default). This position indicates the first nucleotide in
the first mutagenic primer, and it will depend on the
position on the chain of the first codon to be mutagenized
and on the defined length of the mutagenic primers (n+3+n,
where 3 indicates the three nucleotides of the codon to be
mutated and n defines the primer length).
7. Define the number of the first primer (1 by default).
8. Define the name of the output file (output.txt by
default).
9. Click "Run".
10. The information on the potential PTCome and the list of
PTC mutagenic primers is displayed in new .txt files as
indicated above, created in the folder where the PTCMAKER
program was opened.
