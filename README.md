# AlaChainRep

## User Manual AlaChainRep

### Before using AlaChainRep:

- The program generates mutagenic oligonucleotide primers of pre-defined length for Ala-scanning mutagenesis (substitution to Ala of each residue of a given amino acid sequence; Ala residues are substituted to Val) of a known cDNA sequence.
- The forward and reverse mutagenic primers for each mutation are fully complementary, and all primers have the same length, which is defined by the user.
- The mutated Ala codon (3 nucleotides) is placed in the middle of the primer, with an equal number of nucleotides 5’ and 3’ to it. Therefore, the defined length of mutagenic primers has to be an odd number: n+3+n, where n is any number usually between 10 and 20 (the default n in the program is 13, which renders primers 29-mer). Take into consideration that if you want to mutate residues at the N-terminal or C-terminal parts of your protein, you will need portions of the nucleotide sequence from the vector where your cDNA is cloned.
- **Input**: the program accepts as input **.txt files** containing the cDNA sequence of interest, and ignores numbers, non-letter characters, spaces, or line breaks. The first letter in the .txt file is considered the first position from the chain (sequence to be mutagenized). Therefore, letter characters other than the nucleotides should be avoided in the file. The user defines where to start the design of primers by defining the position to start in the chain. 
- **Output**: the program provides a new .txt file with a list of consecutively numbered mutagenic primers, forward and reverse, written 5’ to 3’. The numbering of the first forward mutagenic primer and the name of the .txt file can be defined by the user.

### On-line Beta Versión of AlaChainRep:

Available for any OS and browser in https://erramuzpe.pythonanywhere.com/

###  Using AlaChainRep:

1. Click on "Download" (ZIP File of TAR Ball) to download the compressed file in your computer. Take into account that the output file with the mutagenic primers will be created in the folder where the AlaChainRep program is opened. Open "exec" folder. Open “gnulinux” or "windows" folder depending on your computer's Operative System. If you wish, save the program file (ala_chain_rep.exe) in the folder where you want to have the output file with the list of mutagenic primers.

or 

1. Select from "Downloads" your required version from https://github.com/erramuzpe/LAB_TOOLS/releases

 
2. Execute the program double clicking on the icon.
3. Click "Open" and browse for the .txt file containing the nucleotide sequence to be mutagenized.
4. Your nucleotide sequence (chain) is shown.  
5. Define the length of the mutagenic primers (29 by default).
6. Define the position from the chain at which you would like to start the designing of mutagenic primers (1 by
default). This position indicates the first nucleotide in the first mutagenic primer, and it will depend on the position on the chain of the first codon to be mutagenized and on the defined length of the mutagenic primers (n+3+n, where 3 indicates the three nucleotides of the codon to be mutated and n defines the primer length).
7. Define the number of the first primer (1 by default).
8. Define the name of the output file (output.txt by default).
9. Click "Run". 
10. The list of mutagenic primers is displayed in a new .txt file created in the folder where the AlaChainRep program was opened.   

### On-line Beta Versión of AlaChainRep:

Available for any OS and browser in https://erramuzpe.pythonanywhere.com/

---

# SAVER

Method to calculate an optimum experiment number
