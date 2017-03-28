#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 12:55:04 2015

@author: asier
"""

# -*- coding: utf-8 -*-
import re
import wx
import os
import sys

BASES = ['T', 'C', 'A', 'G']
CODONS = [a+b+c for a in bases for b in bases for c in bases]
AMINO_ACIDS = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
CODON_TABLE = dict(zip(codons, amino_acids))

STOP_CODONS = ["TAG", "TAA", "TGA"]

CODON_CHANGE_TO_SC = {  # TAG TAA TGA
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
        filemenu= wx.Menu() 
        menuAbout = filemenu.Append(wx.ID_ABOUT, '&About',' Information about this program')

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,'&File') # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Show(True)

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, 'StopCodonRep: Developed and maintained by\
        Asier Erramuzpe \nSource code and contact info:\
        \nhttp://github.com/compneurobilbao/stop-codon', 'About StopCodonRep', wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.



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
        label='Position you would like to start', pos=(20, 70))
        self.editpos = wx.TextCtrl(self, value='1', \
        pos=(20, 90), size=(140, -1))
        # the oligo num control
        self.lblline = wx.StaticText(self, \
        label='Number of first primer:', pos=(20, 120))
        self.editline = wx.TextCtrl(self, value='1', \
        pos=(20, 140), size=(140, -1))
        

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
            #remove all spaces/blanks/newlines
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
    
                    if (oligo_num-3)%2 != 0 or (oligo_num-3) <= 0:
                        self.logger.AppendText('Incorrect number of oligos,\
                        insert a correct one \n')
                    else:
                        self.logger.AppendText('Length of primers accepted \n')
    
                        oligo_assert = True
                        side_num = (oligo_num-3) // 2
                except:
                    self.logger.AppendText('Insert a number, please \n')
    
                if oligo_assert == True:
    
                    line_num = int(self.editline.GetValue())
    
                    fname = "stop_codon_info.txt"
                    sc_info = open(fname, 'w')
                
                    fname = "stop_codon_replacement.txt"
                    sc_replacement = open(fname, 'w')
                
                    self.logger.AppendText('\nProcessing...  \n')
                    for x_ in range(0, len(seq), 3):
                        try:
                            codon = self.seq[x_:x_+3]
                        except:
                            break
                
                        if codon in CODON_CHANGE_TO_SC.keys():
                
                            sc_info.write(CODON_TABLE[codon] + str(x_ // 3) + " (" + codon + \
                                          ")" + " -> " + \
                                          str(CODON_CHANGE_TO_SC[codon]) + '\n')
                
                            chain = self.seq[x_: x_+oligo_num]
                            if len(chain) != oligo_num:
                                break
                
                            for new_codon in CODON_CHANGE_TO_SC[codon]:
                                new_chain = chain[:side_num] + new_codon + chain[side_num+3:]
                                chain_rev = reverseComplement(new_chain)
                
                                sc_replacement.write(str(line_num) + "  " + CODON_TABLE[codon] + str(x_ // 3) + " " + new_chain + '\n')
                                sc_replacement.write(str(line_num) + "  " + CODON_TABLE[codon] + str(x_ // 3) + " " + chain_rev + '\n \n')
                
                                line_num += 2
                
                    sc_info.close()
                    sc_replacement.close()
                   
                    self.logger.AppendText('\nFinished! Results in \
                    stop_codon_info.txt and stop_codon_replacement.txt'+' \n')
    
            except:
                self.logger.AppendText('Not file loaded? \n')
                self.logger.AppendText('Unexpected error:'+ sys.exc_info()[0])


    def on_click_exit(self, event):
        """ Exit """
        APP.Destroy()
        sys.exit()
        
        

APP = wx.App(False)
FRAME = MainWindow(None, 'AlaChainRep', size=(775, 350))
PANEL = Panel(FRAME, size=(775, 350))
FRAME.Show()
APP.MainLoop()