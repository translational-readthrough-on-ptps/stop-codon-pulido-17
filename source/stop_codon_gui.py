#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon March 27 12:55:04 2017

@author: asier
"""

# -*- coding: utf-8 -*-
import re
import wx
import os
import sys
import collections

BASES = ['T', 'C', 'A', 'G']
CODONS = [a+b+c for a in BASES for b in BASES for c in BASES]
AMINO_ACID = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
CODON_TABLE = dict(zip(CODONS, AMINO_ACID))

STOP_CODONS = ["TAG", "TAA", "TGA"]

CODON_CHANGE_TO_SC = {  # TAG TAA TGA
                      "TTA": ["TGA", "TAA"], "TCA": ["TGA", "TAA"],
                      "TAT": ["TAG", "TAA"], "TAC": ["TAG", "TAA"],
                      "TGT": ["TGA"], "TGC": ["TGA"],
                      "TGG": ["TAG", "TGA"], "TTG": ["TAG"],
                      "CAA": ["TAA"], "CAG": ["TAG"],
                      "CGA": ["TGA"], "AAA": ["TAA"],
                      "AAG": ["TAG"], "AGA": ["TGA"],
                      "GAA": ["TAA"], "GAG": ["TAG"],
                      "GGA": ["TGA"], "TCG": ["TAG"]
                      }
COMPLEMENT = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}


def reverseComplement(seq):
    sequence = seq*1
    return "".join([COMPLEMENT.get(nt, '') for nt in sequence[::-1]])


def format_chain(seq, start):
    seq = seq[0:start] + " " + \
          " ".join(seq[i:i+3] for i in range(start, len(seq) - start, 3)) \
          + " " + seq[len(seq) - start:]
    return seq


def clean_seq(seq):
    # seq treatment
    seq = re.sub(r'\W', '', seq)  # remove all spaces/blanks/newlines
    seq = re.sub('[^a-zA-Z]', '', seq)  # remove all non LETTER char
    seq = seq.upper()
    return seq


class MainWindow(wx.Frame):
    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent=parent, title=title, size=size)

        # Setting up the menu.
        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT, '&About', ' Information about this program')

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, '&File')  # Adding the "filemenu" to the Menu
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Show(True)

    def OnAbout(self, e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wx
        dlg = wx.MessageDialog(self, 'StopCodonRep: Developed and maintained by\
        Asier Erramuzpe \nSource code and contact info:\
        \nhttp://github.com/compneurobilbao/stop-codon', 'About StopCodonRep', wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.


class Panel(wx.Panel):
    """
    ExamplePanel
    """
    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent, size=size)
        self.dirname = ''
        self.seq = ''
        self.filename = ''
        # A multiline TextCtrl - This is here to show how the events work
        # in this program, don't pay too much attention to it
        self.logger = wx.TextCtrl(self, pos=(340, 20), size=(415, 260), \
        style=wx.TE_MULTILINE | wx.TE_READONLY)
        # Open button
        self.buttonopen = wx.Button(self, label='Open', pos=(20, 250))
        self.Bind(wx.EVT_BUTTON, self.on_click_open, self.buttonopen)
        # Run button
        self.buttonrun = wx.Button(self, label='Run', pos=(110, 250))
        self.Bind(wx.EVT_BUTTON, self.on_click_run, self.buttonrun)
        # Exit button
        self.buttonexit = wx.Button(self, label='Exit', pos=(200, 250))
        self.Bind(wx.EVT_BUTTON, self.on_click_exit, self.buttonexit)
        # the oligo num control
        self.lbloligo = wx.StaticText(self, label='Length of primers:', \
        pos=(20, 20))
        self.editoligo = wx.TextCtrl(self, value='29', \
        pos=(20, 40), size=(140, -1))
        # the position control
        self.lblpos = wx.StaticText(self, \
        label='Position you would like to start:', pos=(20, 70))
        self.editpos = wx.TextCtrl(self, value='1', \
        pos=(20, 90), size=(140, -1))
        # primer's first num
        self.lblline = wx.StaticText(self, \
        label='Number of first primer:', pos=(20, 120))
        self.editline = wx.TextCtrl(self, value='1', \
        pos=(20, 140), size=(140, -1))
        # gene name input
        self.lblline = wx.StaticText(self, \
        label='Gene name:', pos=(20, 170))
        self.editname = wx.TextCtrl(self, value='', \
        pos=(20, 190), size=(140, -1))

    def on_click_open(self, event):
        """ Open a file """
        try:
            dlg = wx.FileDialog(self, 'Choose a file', \
            self.dirname, '', '*.*', wx.OPEN)

            if dlg.ShowModal() == wx.ID_OK:
                self.filename = dlg.GetFilename()
                self.dirname = dlg.GetDirectory()
                dum_file = open(os.path.join(self.dirname, self.filename), 'r')
                self.seq = dum_file.read()
                dum_file.close()
            dlg.Destroy()
            self.logger.AppendText('File loaded! \n')

            # seq initial treatment
            # remove all spaces/blanks/newlines
            self.seq = clean_seq(self.seq)
            self.logger.AppendText('Your chain is:\n%s \n' \
            % self.seq)

        except:
            self.logger.AppendText('There was some problem \
        opening the file \n')

    def on_click_run(self, event):
        """ Main program """
        if not self.seq:
            self.logger.AppendText('Not file loaded? \n')
        else:
            try:
                start_pos = int(self.editpos.GetValue())

                start_pos -= 1
                self.logger.AppendText('\nYou selected %s as your starting point \n'\
                % self.seq[start_pos:start_pos+10])

                self.seq = self.seq[start_pos:] #delete the rest of the chain

                self.logger.AppendText('Your chain now is %s ... \n' \
                % self.seq[:10])

                oligo_assert = False
                try:
                    oligo_num = int(self.editoligo.GetValue())
                    side_num = 0

                    if (oligo_num-3) % 2 != 0 or (oligo_num-3) <= 0:
                        self.logger.AppendText('Incorrect number of oligos,\
                        insert a correct one \n')
                    else:
                        self.logger.AppendText('Length of primers accepted \n')

                        oligo_assert = True
                        side_num = (oligo_num-3) / 2
                except:
                    self.logger.AppendText('Insert a number, please \n')

                if oligo_assert:

                    line_num = line_num_info = int(self.editline.GetValue())
                    codon_list = []
                    stop_codon_list = []
                    stop_codon_c_list = []

                    gene_name = self.editname.GetValue()  
                    fname = "stop_codon_info.txt"
                    sc_info = open(fname, 'w')
                    sc_info.write( "Gene name:  " + gene_name + '\n \n \n')

                    fname = "stop_codon_replacement.txt"
                    sc_replacement = open(fname, 'w')
                    sc_replacement.write( "Gene name:  " + gene_name + '\n \n \n')

                    self.logger.AppendText('\nProcessing...  \n')
                    for x_ in range(0, len(self.seq), 3):
                        try:
                            pre_codon = self.seq[x_-3:x_]
                            codon = self.seq[x_:x_+3]
                            post_codon = self.seq[x_+3:x_+6]
                        except:
                            break

                        if codon in CODON_CHANGE_TO_SC.keys():
                            codon_list.append(codon)
                            for new_codon in CODON_CHANGE_TO_SC[codon]:
                                stop_codon_list.append(new_codon)

                            sc_info.write(str(line_num_info) + "  " + CODON_TABLE[codon] + str((x_ // 3) + 1) + " (" + codon + \
                                          ")" + " -> " + \
                                          str(pre_codon) + str(CODON_CHANGE_TO_SC[codon]) + str(post_codon) + '\n')
                            line_num_info += 1
                            
                            if str(post_codon)[0] == 'C':
                                stop_codon_c_list.append(new_codon + 'C')

                            chain = self.seq[x_ - side_num: x_ - side_num + oligo_num]
                            if (len(chain) != oligo_num) or (x_ - side_num < 0):
                                sc_replacement.write(str(line_num) + "  " + CODON_TABLE[codon] + str((x_ // 3) + 1) + " Not enough oligos to replace chain \n \n")
                                line_num += 1
                            else:
                                for new_codon in CODON_CHANGE_TO_SC[codon]:
                                    new_chain = chain[:side_num] + new_codon + chain[side_num+3:]
                                    chain_rev = reverseComplement(new_chain)

                                    sc_replacement.write(str(line_num) + "  " + CODON_TABLE[codon] + str((x_ // 3) + 1) + " " + new_chain + '\n')
                                    sc_replacement.write(str(line_num+1) + "  " + CODON_TABLE[codon] + str((x_ // 3) + 1) + " " + chain_rev + '\n \n')

                                    line_num += 2

                                    
                                 
                    codon_counter = collections.Counter(codon_list)
                    stop_codon_counter = collections.Counter(stop_codon_list)
                    stop_codon_c_counter = collections.Counter(stop_codon_c_list)
                    sc_info.write('\n'+ 'Gene name: ' + gene_name + '   Codon ' + str(codon_counter) + '  Total: ' + str(sum(codon_counter.values())) + '\n')  
                    sc_info.write('\n'+ 'Gene name: ' + gene_name + '   StopCodon ' + str(stop_codon_counter) + '  Total: ' + str(sum(stop_codon_counter.values())) + '\n') 
                    sc_info.write('\n'+ 'Gene name: ' + gene_name + '   StopCodonCounterC ' + str(stop_codon_c_counter) + '  Total: ' + str(sum(stop_codon_counter.values())) + '\n')  
                    
                    sc_replacement.write('\n'+ 'Gene name: ' + gene_name + '   Codon ' + str(codon_counter) + '  Total: ' + str(sum(codon_counter.values())) + '\n')  
                    sc_replacement.write('\n'+ 'Gene name: ' + gene_name + '   StopCodon ' + str(stop_codon_counter) + '  Total: ' + str(sum(stop_codon_counter.values())) + '\n') 
                    sc_replacement.write('\n'+ 'Gene name: ' + gene_name + '   StopCodonCounterC ' + str(stop_codon_c_counter) + '  Total: ' + str(sum(stop_codon_counter.values())) + '\n')
                    
                    sc_info.close()
                    sc_replacement.close()
                    
                    self.logger.AppendText('\nFinished! Results in \
                    stop_codon_info.txt and stop_codon_replacement.txt'+' \n')

            except:
                self.logger.AppendText('Not file loaded? \n')
                self.logger.AppendText('Unexpected error:'+ str(sys.exc_info()))


    def on_click_exit(self, event):
        """ Exit """
        APP.Destroy()
        sys.exit()



APP = wx.App(False)
FRAME = MainWindow(None, 'StopCodonRep', size=(775, 350))
PANEL = Panel(FRAME, size=(775, 350))
FRAME.Show()
APP.MainLoop()