import ROOT, os
from array import array
from math import pi
# from tttt.Tools.user import plot_directory
from JetTracking.Tools.user import plot_directory
from plot_configuration import fetch_configuration
#eta_cut_dict_coarse

import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--plot_directory', action='store', default='profilePlots')
argParser.add_argument('--version', action='store', default=2)
argParser.add_argument('--eta_cut', action='store', default='coarse')
argParser.add_argument('--simple_cut', action='store', default='pt')
argParser.add_argument('--composite_cut', action='store', default=None)
argParser.add_argument('--small', action='store_true')
args = argParser.parse_args()

import Analysis.Tools.syncer

# Create chain
ev = ROOT.TChain("Events")
file_directories = [f for f in os.listdir("/scratch-cbe/users/robert.schoefbeck/JetTracking/nanoTuples/v2/miniAOD_Fall17/")]

if args.small:
    ev.Add("/scratch-cbe/users/robert.schoefbeck/JetTracking/nanoTuples/v2/miniAOD_Fall17/DYJetsToLL_M50_HT100to200_LO/*.root")
else:
    print(file_directories)
    for dir in file_directories:
        ev.Add("/scratch-cbe/users/robert.schoefbeck/JetTracking/nanoTuples/v2/miniAOD_Fall17/"+dir+"/*.root")

if args.small: args.plot_directory += "_small"

plot_directory_ = os.path.join(plot_directory, 'v{}'.format(args.version), args.plot_directory)

def merge_dict(dict1, dict2):
    dict3 = dict1.copy()
    dict3.update(dict2)
    return dict3

config = fetch_configuration()

if args.eta_cut == "coarse":
    eta_config_ = config["eta_cut_coarse"]
elif args.eta_cut == "fine":
    eta_config_ = config["eta_cut_fine"]

plot_directory_ = os.path.join(plot_directory_, args.eta_cut)

if args.simple_cut == "pt":         cut_config_ = config["Pair_pt_cut_simple"]
elif args.simple_cut == "mass":     cut_config_ = config["mass_dict"]
elif args.simple_cut == "r":        cut_config_ = config["r_dict"]
elif args.simple_cut == "jetPt":    cut_config_ = config["Jet_pt_dict"]

if args.composite_cut == "mass":    cut_config_2_ = config["mass_dict"]
elif args.composite_cut == "r":     cut_config_2_ = config["r_dict"]
elif args.composite_cut == "jetPt":    cut_config_2_ = config["Jet_pt_dict"]

if args.composite_cut == None:
    plot_directory_ = os.path.join(plot_directory_, args.simple_cut)
else:
    plot_directory_ = os.path.join(plot_directory_, args.simple_cut+"_"+args.composite_cut)


# Scatter plot (useless)
def scatter_plot(variable, cut):

    ratio = "(Sum$(Pair_isC)/Sum$(Pair_isS))"
    c = ROOT.TCanvas( 'c', 'c', 200, 10, 700, 500 )
    c.SetLogz()
    ev.Draw(ratio+":"+var+">>hist", cut, "colz")
    hist = ROOT.gPad.GetPrimitive("hist")
    hist.SetTitle("Scatter Plot")
    ROOT.gStyle.SetOptStat(0)
    hist.GetYaxis().SetTitle("Cowboys/Seagulls")
    if var == "Pair_phi":
        hist.GetXaxis().SetTitle("#varphi_{pair}")
        hist.GetXaxis().SetRangeUser(-3, 3)
        c.Draw()
        c.Print("RatioVs"+var+".pdf")

# Create profile plots
def profile_plot(eta_cut, cut1, cut2=None):

    ratio = "(Sum$(Pair_isC)/Sum$(Pair_isS))"
    c = ROOT.TCanvas( 'c', 'c', 200, 10, 700, 500 )
    p = ROOT.TProfile("p", "Profile plot", 30,  -pi, pi, 0, 5)
    p1 = ROOT.TProfile("p1", "", 30, -pi, pi, 0, 5)
    p.SetTitleSize(0.5)

    p.GetXaxis().SetTitle("#varphi_{pair}")
    p.GetYaxis().SetTitle("Cowboys/Seagulls")
    ROOT.gStyle.SetOptStat(0)

    if cut2 is None:
        ev.Draw(ratio+":Pair_phi>>p", eta_config_[eta_cut]["plus"]["cut"]+"&&"+cut_config_[cut1]["cut"])
    else:
        ev.Draw(ratio+":Pair_phi>>p", eta_config_[eta_cut]["plus"]["cut"]+"&&"+cut_config_[cut1]["cut"]+"&&"+cut_config_2_[cut2]["cut"])
    p.GetYaxis().SetRangeUser(0,2.5)

    h = ROOT.TH1D("h", "h", 10, 0, 100)
    h = p.ProjectionX()
    for i in range(1, h.GetNbinsX()+1):
        bEntries = h.GetBinContent(i)
        if bEntries >1:
            bError = h.GetBinError(i)/ ROOT.TMath.Sqrt(bEntries)
        else:
            bError = 0
        h.SetBinError(i, bError)
    h.Draw("E")

    h1 = ROOT.TH1D("h1", "h1", 10, 0, 100)
    if cut2 is None:
        ev.Draw(ratio+":Pair_phi>>p1", eta_config_[eta_cut]["minus"]["cut"]+"&&"+cut_config_[cut1]["cut"])
    else:
        ev.Draw(ratio+":Pair_phi>>p1", eta_config_[eta_cut]["minus"]["cut"]+"&&"+cut_config_[cut1]["cut"]+"&&"+cut_config_2_[cut2]["cut"])
    h1 = p1.ProjectionX()

    for i in range(1, h1.GetNbinsX()+1):
        bEntries = h1.GetBinContent(i)
        if bEntries >1:
            bError = h1.GetBinError(i)/ ROOT.TMath.Sqrt(bEntries)
        else:
            bError = 0
        h1.SetBinError(i, bError)
    h1.Draw("ESAME")
    h.SetLineColor(ROOT.kRed)
    h1.SetLineColor(ROOT.kBlue)

    ratio_pad = ROOT.TPad("rp", "rp", 0,0,1,0.3)
    ratio_pad.SetTopMargin(0.03)
    ratio_pad.SetBottomMargin(0.3)
    ratio_pad.Draw()

    r = ROOT.TRatioPlot(h, h1, "divsym")

    r.SetGraphDrawOpt("EP")
    r.Draw()
    r.GetUpperPad().SetTitle("Profile")


    l = ROOT.TLegend(0.4,0.4,0.6,0.6)
    l.SetFillColor(0)
    l.SetBorderSize(0)
    l.SetTextSize(0.03)

    tex = ROOT.TLatex(0, 0, eta_config_[eta_cut]["plus"]["legend"])
    tex1 = ROOT.TLatex(0, 0, eta_config_[eta_cut]["minus"]["legend"])
    if cut2 is None:
        cut_tex1 =  ROOT.TLatex(0, 0, cut_config_[cut1]["legend"])
    else:
        cut_tex1 =  ROOT.TLatex(0, 0, cut_config_[cut1]["legend"])
        cut_tex2 =  ROOT.TLatex(0, 0, cut_config_2_[cut2]["legend"])
    l.AddEntry("h", tex.GetTitle(), "l")
    l.AddEntry("h1", tex1.GetTitle(), "l")
    if cut2 is None:
        l.AddEntry(None, cut_tex1.GetTitle(), "")
    else:
        l.AddEntry(None, cut_tex1.GetTitle(), "")
        l.AddEntry(None, cut_tex2.GetTitle(), "")
    l.SetX1NDC(0.45)
    l.SetY1NDC(0.45)
    l.SetX2NDC(0.65)
    l.SetY2NDC(0.65)

    l.GetListOfPrimitives().At(0).SetLineColor(ROOT.kRed)
    l.GetListOfPrimitives().At(1).SetLineColor(ROOT.kBlue)

    l.Draw("SAME")

    c.Draw()

    format = ['pdf', 'png']
    for f in format:
        if cut2 is None:
            c.Print(plot_directory_+"/"+eta_cut+"_"+cut1+"."+f)
        else:
            c.Print(plot_directory_+"/"+eta_cut+"_"+cut1+"_"+cut2+"."+f)

if args.composite_cut == None:
    for i in eta_config_.keys():
        for j in cut_config_.keys():
            profile_plot(i,j, None)
else:
    for i in eta_config_.keys():
        for j in cut_config_.keys():
            for k in cut_config_2_.keys():
                profile_plot(i,j,k)
