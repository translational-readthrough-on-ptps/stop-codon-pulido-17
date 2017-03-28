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
CODONS = [a+b+c for a in BASES for b in BASES for c in BASES]
AMINO_ACIDS = 'FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG'
CODON_TABLE = dict(zip(CODONS, AMINO_ACIDS))
CODON_CHANGE_TO_V = {
    "GCA" : "GTA",
    "GCC" : "GTC",
    "GCG" : "GTG",
    "GCT" : "GTT"
}
CODON_CHANGE_TO_A = { #GCA GCC GCG GCT
    "TTT":"GCT", "TTC":"GCC", "TTA":"GCA", "TTG":"GCG",
    "TCT":"GCT", "TCC":"GCC", "TCA":"GCA", "TCG":"GCG",
    "TAT":"GCT", "TAC":"GCC", "TAA":"GCA", "TAG":"GCG",
    "TGT":"GCT", "TGC":"GCC", "TGA":"GCA", "TGG":"GCG",
    "CTT":"GCT", "CTC":"GCC", "CTA":"GCA", "CTG":"GCG",
    "CCT":"GCT", "CCC":"GCC", "CCA":"GCA", "CCG":"GCG",
    "CAT":"GCT", "CAC":"GCC", "CAA":"GCA", "CAG":"GCG",
    "CGT":"GCT", "CGC":"GCC", "CGA":"GCA", "CGG":"GCG",
    "ATT":"GCT", "ATC":"GCC", "ATA":"GCA", "ATG":"GCG",
    "ACT":"GCT", "ACC":"GCC", "ACA":"GCA", "ACG":"GCG",
    "AAT":"GCT", "AAC":"GCC", "AAA":"GCA", "AAG":"GCG",
    "AGT":"GCT", "AGC":"GCC", "AGA":"GCA", "AGG":"GCG",
    "GTT":"GCT", "GTC":"GCC", "GTA":"GCA", "GTG":"GCG",
    "GAT":"GCT", "GAC":"GCC", "GAA":"GCA", "GAG":"GCG",
    "GGT":"GCT", "GGC":"GCC", "GGA":"GCA", "GGG":"GCG"
    }
COMPLEMENT = {'A':'T', 'C':'G', 'G':'C', 'T':'A', 'N':'N'}

def chain_rep(chain, start):
    """
    chain_rep
    """
    codon = chain[start:start+3]
    if CODON_TABLE[codon] == 'A': #substitute for V
        codon = CODON_CHANGE_TO_V[codon]
    else: #substitute for A
        codon = CODON_CHANGE_TO_A[codon]
    chain = chain[:start] + codon + chain[start+3:]
    return chain

def reverse_complement(chain):
    """
    reverse_complement
    """
    return "".join([COMPLEMENT.get(nt, '') for nt in chain[::-1]])


#Main start
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
        dlg = wx.MessageDialog( self, 'AlaChainRep: Developed and maintained by\
        Asier Erramuzpe \nSource code and contact info:\
        \nhttp://erramuzpe.github.io/LAB_TOOLS', 'About AlaChainRep', wx.OK)
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
        # the oligo num control
        self.lblname = wx.StaticText(self, \
        label='Output file name:', pos=(20, 170))
        self.editname = wx.TextCtrl(self, \
        value='output.txt', pos=(20, 190), size=(140, -1))
        

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
            self.seq = re.sub(r'\W', '', self.seq)
            #remove all non LETTER char
            self.seq = re.sub('[^a-zA-Z]', '', self.seq)
            self.seq = self.seq.upper()
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
                        side_num = (oligo_num-3) / 2
                except:
                    self.logger.AppendText('Insert a number, please \n')
    
                if oligo_assert == True:
    
                    line_num = int(self.editline.GetValue())
    
                    fname = self.editname.GetValue()
                    dum_file = open(fname, 'w')
    
    
                    self.logger.AppendText('\nProcessing...  \n')
                    for i in xrange(0, len(self.seq), 3):
    
                        chain = self.seq[i: i+oligo_num]
    
                        if len(chain) != oligo_num:
                            break
    
                        chain = chain_rep(chain, side_num)
                        chain_rev = reverse_complement(chain)
    
                        dum_file.write(str(line_num) + " " + chain + '\n')
                        dum_file.write(str(line_num+1) + " " + chain_rev + '\n \n')
    
                        line_num += 2
    
                    dum_file.close()
                    self.logger.AppendText('\nFinished! Results in '+fname+' \n')
    
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