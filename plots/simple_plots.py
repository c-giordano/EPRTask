import ROOT
import os
from JetTracking.Tools.user import plot_directory
import Analysis.Tools.syncer
from array import array
from math import pi


ev = ROOT.TChain("Events")
file_directories = [f for f in os.listdir("/scratch-cbe/users/robert.schoefbeck/JetTracking/nanoTuples/v2/miniAOD_Fall17/")]
for dir in file_directories:
    ev.Add("/scratch-cbe/users/robert.schoefbeck/JetTracking/nanoTuples/v2/miniAOD_Fall17/"+dir+"/*.root")

#Later
# selectionDictionary ={"Dense":"Jet_pt>100",
#                     "Dense_t2_S":"Jet_pt>100&&Pair_tp_pt>2&&Pair_tm_pt>2&&Pair_isS",
#                     "Dense_t2_C":"Jet_pt>100&&Pair_tp_pt>2&&Pair_tm_pt>2&&Pair_isC",
#                     "Dense_t5_S":"Jet_pt>100&&Pair_tp_pt>5&&Pair_tm_pt>5&&Pair_isS",
#                     "Dense_t5_C":"Jet_pt>100&&Pair_tp_pt>5&&Pair_tm_pt>5&&Pair_isC",
#                     "Dense_t10_S":"Jet_pt>100&&Pair_tp_pt>10&&Pair_tm_pt>10&&Pair_isS",
#                     "Dense_t10_C":"Jet_pt>100&&Pair_tp_pt>10&&Pair_tm_pt>10&&Pair_isC"}


def simple_plot(variable, cut):
    c = ROOT.TCanvas( 'c', 'c', 200, 10, 700, 500 )
    ROOT.gStyle.SetOptStat(0)

    ev.Draw(variable+">>h(200,0,2)", cut)#&&Pair_tp_pt>5&&Pair_tm_pt>5&&Pair_isS")
    c.Draw()
    c.Print("./"+variable+".pdf")


simple_plot("Pair_C_R", "Jet_pt>100&&Pair_tp_pt>2&&Pair_tm_pt>2&&Pair_isS")
