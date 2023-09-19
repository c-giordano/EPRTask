import ROOT
from RootTools.core.standard import *
import Analysis.Tools.syncer as syncer
import os

c = ROOT.TChain("Events")
c.Add("/scratch-cbe/users/robert.schoefbeck/JetTracking/nanoTuples/v3/miniAOD_Fall17/DYJetsToLL_M50_HT600to800_LO/*.root")

import Analysis.Tools.user as user

c1 = ROOT.TCanvas()
c.Draw("log(Pair_tp_pt/Pair_tm_pt)>>h(100,-10,10)")
ROOT.h.Draw()

plot_directory = os.path.join( user.plot_directory, "JetTracking") 
try:
    os.makedirs( plot_directory)
except OSError:
    pass

c1.Print(os.path.join(plot_directory, "log_pair_pt_ratio.png"))
