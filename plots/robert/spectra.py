import ROOT
from RootTools.core.standard import *
import RootTools.core.logger as logger_rt
import seaborn as sns

import Analysis.Tools.syncer as syncer
import os
import math

from JetTracking.Tools.user import plot_directory

# Arguments
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',           action='store',      default='INFO', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], help="Log level for logging")
argParser.add_argument('--plot_directory',     action='store',      default='')
argParser.add_argument('--data_version',     action='store',      default='v3')
argParser.add_argument('--sample',             action='store',      default='DYJetsToLL_M50_LO',)
argParser.add_argument('--small',                                   action='store_true',     help='Run only on a small subset of the data?')
argParser.add_argument('--twoD_logPt', action='store_true')
argParser.add_argument('--all',                                     action='store_true')
argParser.add_argument('--basic',                                   action='store_true')
argParser.add_argument('--preselection',                            action='store_true')
argParser.add_argument('--sliceEta',                                  action='store_true')
argParser.add_argument('--slicePt',                                  action='store_true')
argParser.add_argument('--twoD',                                   action='store_true')
argParser.add_argument('--twoD_selection',                                   action='store_true')
argParser.add_argument('--twoD_SC',                                   action='store_true')
argParser.add_argument('--SC',                                   action='store_true')
argParser.add_argument('--sliceR',                                   action='store_true')
argParser.add_argument('--cutR',                                   action='store_true')
argParser.add_argument('--cutPt',                                   action='store_true')
argParser.add_argument('--combo',                                   action='store_true')
argParser.add_argument('--slicePhi',                                   action='store_true')
argParser.add_argument('--twoD_maxminplots',                                               action='store_true')
argParser.add_argument('--occ',                                     action='store_true')

args = argParser.parse_args()

if args.all:
    args.basic = True
    args.twoD  = True
    args.SC    = True
    args.sliceR= True
    args.slicePhi=True

# choose a sample

if args.data_version == 'v3':
    args.plot_directory+="_new"
    import data_v3 as data
elif args.data_version == 'v4':
    args.plot_directory+="_new"
    import data_v3 as data
elif args.data_version == 'v6':
    import data_v3 as data
elif args.data_version == 'v7':
    import data_v7 as data
elif args.data_version == 'v8':
    import data_v8 as data
elif args.data_version == 'v9':
    import data_v9 as data

sample = getattr(data, args.sample)

if args.small:
    args.plot_directory+="_small"
    sample.reduceFiles(to=10)


sequence       = []

# preselection = 'Jet_pt>100&&Pair_pt<100&&abs(log(Pair_tp_pt/Pair_tm_pt))<2'
# preselection = 'Jet_pt>100&&Pair_pt<100'
preselection = 'Jet_pt>100'
preselection_dict = {
                     "Dense":   "Jet_pt>100",
                     # "Dense_r2to4":       "Jet_pt>100&&Pair_C_R>0.02&&Pair_C_R<=0.04",
                     # "Dense_r4to6":       "Jet_pt>100&&Pair_C_R>0.04&&Pair_C_R<=0.06",
                     # "Dense_r6to8":       "Jet_pt>100&&Pair_C_R>0.06&&Pair_C_R<=0.08",
                     #
                     # "Dense_isC_r2to4":   "Jet_pt>100&&Pair_isC&&Pair_C_R>0.02&&Pair_C_R<=0.04",
                     # "Dense_isS_r2to4":   "Jet_pt>100&&Pair_isS&&Pair_C_R>0.02&&Pair_C_R<=0.04",
                     # "Dense_isC_r4to6":   "Jet_pt>100&&Pair_isC&&Pair_C_R>0.04&&Pair_C_R<=0.06",
                     # "Dense_isS_r4to6":   "Jet_pt>100&&Pair_isS&&Pair_C_R>0.04&&Pair_C_R<=0.06",
                     # "Dense_isC_r6to8":   "Jet_pt>100&&Pair_isC&&Pair_C_R>0.06&&Pair_C_R<=0.08",
                     # "Dense_isS_r6to8":   "Jet_pt>100&&Pair_isS&&Pair_C_R>0.06&&Pair_C_R<=0.08",
                     }
eta_dictionary = {# "etaSlice_1_plus":     {"cut":"Pair_eta>0&&Pair_eta<0.5", "texX": "0 < #eta < 0.5"},
                  # "etaSlice_1_minus":    {"cut":"Pair_eta>-0.5&&Pair_eta<0", "texX": "-0.5 < #eta < 0"},
                  # "etaSlice_2_plus":     {"cut":"Pair_eta>=0.5&&Pair_eta<1", "texX": "0.5 < #eta < 1"},
                  # "etaSlice_2_minus":    {"cut":"Pair_eta>=-1&&Pair_eta<-0.5", "texX": "-1 < #eta < -0.5"},
                  # "etaSlice_3_plus":     {"cut":"Pair_eta>=1&&Pair_eta<1.5", "texX": "1 < #eta < 1.5"},
                  # "etaSlice_3_minus":    {"cut":"Pair_eta>=-1.5&&Pair_eta<-1", "texX": "-1.5 < #eta < -1"},
                  # "etaSlice_4_plus":     {"cut":"Pair_eta>=1.5&&Pair_eta<2", "texX": "1.5 < #eta < 2"},
                  # "etaSlice_4_minus":    {"cut":"Pair_eta>=-2&&Pair_eta<-1.5", "texX": "-2 < #eta < -1.5"},
                  # "etaSlice_5_plus":     {"cut":"Pair_eta>=2&&Pair_eta<2.5", "texX": "2 < #eta < 2.5"},
                  # "etaSlice_5_minus":    {"cut":"Pair_eta>=-2.5&&Pair_eta<-2", "texX": "-2.5 < #eta < -2"},
                  "etaSlice_6_plus":     {"cut":"Pair_eta>=2.5&&Pair_eta<3", "texX": "2.5 < #eta < 3"},
                  "etaSlice_6_minus":    {"cut":"Pair_eta>=-3&&Pair_eta<-2.5", "texX": "-3.5 < #eta < -2.5"},

}

r_cut_dict_cm = {
        "r2to4":   {"cut":         "Pair_C_R>=0.02&&Pair_C_R<0.04",     "texX":      "2<r<4 (cm)"},
        "r4to6":   {"cut":         "Pair_C_R>=0.04&&Pair_C_R<0.06",     "texX":      "4<r<6 (cm)"},
        "r6to8":   {"cut":         "Pair_C_R>=0.06&&Pair_C_R<0.08",     "texX":      "6<r<8 (cm)"},
        "r8to12":  {"cut":         "Pair_C_R>=0.08&&Pair_C_R<0.12",     "texX":      "8<r<12 (cm)"},
        "r12to18":  {"cut":         "Pair_C_R>=0.12&&Pair_C_R<0.18",     "texX":      "12<r<18 (cm)"},
        "r18plus":  {"cut":         "Pair_C_R>=0.18",     "texX":      "r>18 (cm)"},

        }

pt_dict = {
    "pt10":             {"cut":         "Pair_pt<=10",                  "texX":      "p_{T,Pair} #leq 10(GeV)"},
    "pt10to20":         {"cut":         "Pair_pt>10&&Pair_pt<=20",      "texX":      "p_{T,Pair} #leq 20(GeV)"},
    "pt20to40":         {"cut":         "Pair_pt>20&&Pair_pt<=40",      "texX":      "20 < p_{T,Pair} #leq 40(GeV)"},
    "pt40to60":         {"cut":         "Pair_pt>40&&Pair_pt<=60",      "texX":      "40 < p_{T,Pair} #leq 60(GeV)"},
    "pt60to80":         {"cut":         "Pair_pt>60&&Pair_pt<=80",      "texX":      "60 < p_{T,Pair} #leq 80(GeV)"},
    "pt80to100":        {"cut":         "Pair_pt>80&&Pair_pt<=100",     "texX":      "80 < p_{T,Pair} #leq 100(GeV)"},
    "pt100":            {"cut":         "Pair_pt>100",                  "texX":      "p_{T,Pair} > 100(GeV)"},
}

# 1D Jet & pair kinematics
if args.basic:
    # args.plot_directory+="basic"
    print "Make basic plots"
    plot_cfg = {
        # 'Jet_pt': {'var':'Jet_pt', 'binning':[30, 100, 1500], 'texX':"p_{T}(jet) (GeV)"},
        # 'Jet_eta':{'var':'Jet_eta', 'binning':[30, -3, 3], 'texX':"#eta(jet)"},
        # 'Jet_phi':{'var':'Jet_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(jet)"},
        #
        # 'Pair_pt':{'var':'Pair_pt', 'binning':[30, 0, 1500], 'texX':"p_{T}(pair) (GeV)"},
        # 'Pair_eta':{'var':'Pair_eta', 'binning':[30, -3, 3], 'texX':"#eta(pair)"},
        # 'Pair_phi':{'var':'Pair_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(pair)"},
        #
        'Pair_C_R':{'var':'Pair_C_R', 'binning':[50, 0, 0.04], 'texX':"R(C) (m)"},
        # 'Pair_C_phi':{'var':'Pair_C_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(C)"},
        'log_ratio': {'var':'log(Pair_tp_pt/Pair_tm_pt)', 'binning':[60, -10, 10], 'texX':"log(p^{+}_{Pair}/p^{-}_{Pair})"}
        # #
        # 'Pair_deltaPhi':{'var':'Pair_deltaPhi', 'binning':[30, -2, 2], 'texX':"#Delta#phi(pair)"},
        # 'Pair_deltaEta':{'var':'Pair_deltaEta', 'binning':[30, -2, 2], 'texX':"#Delta#eta(pair)"},

        # 'Track_pt':{'var':'Track_pt', 'binning':[30, 0, 1500], 'texX':"p_{T}(track)"},
        # 'Track_eta':{'var':'Track_eta', 'binning':[30, -3, 3], 'texX':"#eta(track)"},
        # 'Track_phi':{'var':'Track_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(track)"},
        }

    plots = []
    for name, p in plot_cfg.items():
        print "At " + name
        for pres in preselection_dict:
            print('At ' + pres)
            print('Cut ' + preselection_dict[pres])
            if args.preselection:
                h = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection_dict[pres])
                h.legendText = sample.name

                plots.append( Plot.fromHisto( name+"_"+pres, [[h]], texX = p['texX'] ) )
            elif args.sliceEta:
                for nameEta, dict in eta_dictionary.items():
                    print(dict['cut'])

                    h = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection_dict[pres]+"&&"+dict['cut'])
                    h.legendText = sample.name

                    plots.append( Plot.fromHisto( name+"_"+pres+"_"+nameEta, [[h]], texX = p['texX']+' for '+dict['texX'] ) )

    for logY in [False, True]:
        for p in plots:
            plotting.draw( p,
                plot_directory = os.path.join( plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logY else "lin")),
                yRange = "auto", extensions=["pdf", "png"], copyIndexPHP=True)
    syncer.sync()

# 2D pair pt eta vs phi
if args.twoD_SC:
    h2D = {}
    h2DR = {}
    h2DpT = {}
    h2DRpT = {}
    print "Make 2D plots"
    # for what in ["Pair"]:
    name = "Pair_eta_vs_Pair_phi"

    if args.preselection:
        for who in ['isC', 'isS']:
            h2D[who] = sample.get2DHistoFromDraw("Pair_eta:Pair_phi", [20,-math.pi,math.pi,20,-3,3], selectionString = preselection+"&&Pair_"+who)
            p = Plot2D.fromHisto( name+"_"+who, [[h2D[who]]], texX = "#phi(Pair) for {}".format( who), texY="#eta(Pair) for {}".format( who) )
            for logZ in [False, True]:
                plotting.draw2D( p, logZ = logZ,
                    plot_directory = os.path.join( plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                    extensions=["png", "pdf"], copyIndexPHP=True)

        ratio_name = "ratio_" + name
        ratios = h2D["isC"].Clone(ratio_name)
        ratios.Divide(h2D["isS"])
        # ratios.GetYaxis().SetNdivisions(40)
        for logZ in [False, True]:
            # Plot and save the ratio
            p = Plot2D.fromHisto(ratio_name, [[ratios]], texX="#phi(Pair)", texY="#eta(Pair)")
            # p.GetZaxis().SetNdivisions(10)
            plotting.draw2D(p, logZ=logZ,
                            plot_directory=os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                            extensions=["png", "pdf"], copyIndexPHP=True)

    if args.cutR:
        for who in ['isC', 'isS']:
            for r in r_cut_dict_cm:
                h2DR[who+"_"+r] = sample.get2DHistoFromDraw("Pair_eta:Pair_phi", [20,-math.pi,math.pi,20,-3,3], selectionString = preselection+"&&Pair_"+who+"&&"+r_cut_dict_cm[r]['cut'])
                p2 = Plot2D.fromHisto( name+"_"+who+"_"+r, [[h2DR[who+"_"+r]]], texX = "#phi(Pair) for {} and {}".format( who, r_cut_dict_cm[r]['texX']), texY="#eta(Pair) for {} and ".format( who, r_cut_dict_cm[r]['texX']) )
                for logZ in [False, True]:
                    plotting.draw2D( p2, logZ = logZ,
                        plot_directory = os.path.join( plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                        extensions=["png", "pdf"], copyIndexPHP=True)

        for r in r_cut_dict_cm:
            ratio_with_cuts = "ratio_" + name + "_" + r
            ratios2 = h2DR["isC_"+r].Clone(ratio_with_cuts)
            ratios2.Divide(h2DR["isS_"+r])
            for logZ in [False, True]:
                p = Plot2D.fromHisto(ratio_with_cuts, [[ratios2]], texX="#phi(Pair) for {}".format(r_cut_dict_cm[r]["texX"]), texY="#eta(Pair) for {}".format(r_cut_dict_cm[r]["texX"]))
                plotting.draw2D(p, zRange = (0.5, 1.5), logZ=logZ,
                                plot_directory=os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                                extensions=["png", "pdf"], copyIndexPHP=True)

    if args.cutPt:
        for who in ['isC', 'isS']:
            for pt in pt_dict:
                h2DpT[who+"_"+pt] = sample.get2DHistoFromDraw("Pair_eta:Pair_phi", [20,-math.pi,math.pi,20,-3,3], selectionString = preselection+"&&Pair_"+who+"&&"+pt_dict[pt]['cut'])
                p4 = Plot2D.fromHisto( name+"_"+who+"_"+pt, [[h2DpT[who+"_"+pt]]], texX = "#phi(Pair) for {} and {}".format( who, pt_dict[pt]['texX']), texY="#eta(Pair) for {} and ".format( who, pt_dict[pt]['texX']) )
                for logZ in [False, True]:
                    plotting.draw2D( p4, logZ = logZ,
                        plot_directory = os.path.join( plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                        extensions=["png", "pdf"], copyIndexPHP=True)

        for pt in pt_dict:
            ratio_with_cuts = "ratio_" + name + "_" + pt
            ratios2 = h2DpT["isC_"+pt].Clone(ratio_with_cuts)
            ratios2.Divide(h2DpT["isS_"+pt])
            for logZ in [False, True]:
                p = Plot2D.fromHisto(ratio_with_cuts, [[ratios2]], texX="#phi(Pair) for {}".format(pt_dict[pt]["texX"]), texY="#eta(Pair) for {}".format(pt_dict[pt]["texX"]))
                plotting.draw2D(p, zRange = (0.5, 1.5), logZ=logZ,
                                plot_directory=os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                                extensions=["png", "pdf"], copyIndexPHP=True)

    if args.combo:
        for who in ['isC', 'isS']:
            for r in r_cut_dict_cm:
                for pt in pt_dict:
                    h2DRpT[who+"_"+r+"_"+pt] = sample.get2DHistoFromDraw("Pair_eta:Pair_phi", [20,-math.pi,math.pi,20,-3,3], selectionString = preselection+"&&Pair_"+who+"&&"+r_cut_dict_cm[r]['cut']+"&&"+pt_dict[pt]['cut'])
                    p3 = Plot2D.fromHisto( name+"_"+who+"_"+r+"_"+pt, [[h2DRpT[who+"_"+r+"_"+pt]]], texX = "#phi(Pair) for {} and {} & {}".format( who, r_cut_dict_cm[r]['texX'], pt_dict[pt]['cut']), texY="#eta(Pair) for {} and {} & {}".format( who, r_cut_dict_cm[r]['texX'], pt_dict[pt]['cut']) )
                    for logZ in [False, True]:
                        plotting.draw2D( p3, logZ = logZ,
                            plot_directory = os.path.join( plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                            extensions=["png", "pdf"], copyIndexPHP=True)

        for r in r_cut_dict_cm:
            for pt in pt_dict:
                ratio_with_cuts = "ratio_" + name + "_" + r + "_" + pt
                ratios3 = h2DRpT["isC_"+r+ "_" +pt].Clone(ratio_with_cuts)
                ratios3.Divide(h2DRpT["isS_"+r+ "_" +pt])
                for logZ in [False, True]:
                    # Plot and save the ratio
                    p = Plot2D.fromHisto(ratio_with_cuts, [[ratios3]], texX="#phi(Pair) for {} and {}".format(r_cut_dict_cm[r]["texX"], pt_dict[pt]["texX"]), texY="#eta(Pair) for {} and {}".format(r_cut_dict_cm[r]["texX"], pt_dic[pt]["texX"]))
                    # p.GetZaxis().SetNdivisions(10)
                    plotting.draw2D(p, zRange = (0.5, 1.5), logZ=logZ,
                                    plot_directory=os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                                    extensions=["png", "pdf"], copyIndexPHP=True)
        # save h1 with Pair_isC
        # save h2 with Pair_isS
        # divide h1 by h2
        # plot

    syncer.sync()

################################################################################
# if args.occ:
#     args.plot_directory+="occupancy"
#     print "Make 2D plots"
#     h2D = {}
#     name = "occupancy_Pair_C_phi_vs_Pair_C_r"
#
#     for what in ["isC", "isS"]:
#         h2D[what] = sample.get2DHistoFromDraw("Pair_C_R:Pair_C_phi", [80, -math.pi, math.pi, 10, 0, 0.16], selectionString='Jet_pt>100')
#
#         # Plot and save individual histograms for isC and isS
#         p = Plot2D.fromHisto(name + "_" + what, [[h2D[what]]], texX="C_{#phi} for %s" % what, texY="C_{R} for %s" % what)
#         for logZ in [False, True]:
#             plotting.draw2D(p, logZ=logZ,
#                             plot_directory=os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
#                             extensions=["png"], copyIndexPHP=True)
#
#     for selection in selections.keys():
#         selection_criteria = selections[selection]["selection"]
#         cut_name = selections[selection]["name"]
#
#         for what in ["isC", "isS"]:
#             h2D[what] = sample.get2DHistoFromDraw("Pair_C_R:Pair_C_phi", [80, -math.pi, math.pi, 10, 0, 0.16], selectionString=preselection + "&&" + selection_criteria + "&&Pair_" + what)
#
#             # Plot and save individual histograms for isC and isS
#             p = Plot2D.fromHisto(name + "_" + what + "_" + cut_name, [[h2D[what]]], texX="C_{#phi} for %s" % what, texY="C_{R} for %s" % what)
#             for logZ in [False, True]:
#                 plotting.draw2D(p, logZ=logZ,
#                                 plot_directory=os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
#                                 extensions=["png"], copyIndexPHP=True)
#
#         # Calculate and save the ratio for the current cut
#         ratio_name = "ratio_" + name + "_" + cut_name
#         ratios = h2D["isC"].Clone(ratio_name)
#         ratios.Divide(h2D["isS"])
#         for logZ in [False, True]:
#             # Plot and save the ratio
#             p = Plot2D.fromHisto(ratio_name, [[ratios]], texX="C_{#phi}", texY="R_{#phi}")
#             plotting.draw2D(p, logZ=logZ,
#                             plot_directory=os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
#                             extensions=["png"], copyIndexPHP=False)
#
#     syncer.sync()
################################################################################

if args.twoD_selection:
    print "Make 2D plots with various cuts"
    for what in ["Pair"]:
        name = "{what}_deltaEta_vs_{what}_deltaPhi".format(what=what)
        for pres in preselection_dict:
            print(pres)
            print(preselection_dict[pres])
            for nameEta, dict in eta_dictionary.items():
                h2D = sample.get2DHistoFromDraw(name.replace("_vs_", ":"), [20,-1,1,20,-1,1], selectionString = preselection_dict[pres]+"&&"+dict['cut'])
                p = Plot2D.fromHisto( name+"_"+pres+"_"+nameEta, [[h2D]], texX = "#Delta#phi{0} for {1}".format(what,dict['texX']), texY="#Delta#eta{0} for {1}".format(what,dict['texX']) )
                for logZ in [False, True]:
                    plotting.draw2D( p, logZ = logZ,
                        plot_directory = os.path.join( plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                        extensions=["png", "pdf"], copyIndexPHP=True)
    syncer.sync()

if args.twoD_logPt:
    print "Make 2D plots"
    name = "log_Pair_tmvstp"
    h2D = sample.get2DHistoFromDraw("log10(Pair_tm_pt):log10(Pair_tp_pt)", [20,-0.5,2.5,20,-0.5,2.5])
    p = Plot2D.fromHisto( name, [[h2D]], texX = "p_{T}(-)", texY="p_{T}(+)" )
    for logZ in [False, True]:
        plotting.draw2D( p, logZ = logZ,
            plot_directory = os.path.join( plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
            extensions=["png", "pdf"], copyIndexPHP=True)
    syncer.sync()


if args.twoD_maxminplots:
    name = 'min_vs_max_Pair_pt'
    for pres in preselection_dict:
        if args.preselection:
            # [20,-0.5,3,20,-0.5,3]
            h2D = sample.get2DHistoFromDraw("log10(min(Pair_tm_pt, Pair_tp_pt)):log10(max(Pair_tm_pt, Pair_tp_pt))", [20,-1,2,20,-1,2], selectionString = preselection_dict[pres])
            p = Plot2D.fromHisto( name+"_"+pres, [[h2D]], texX = 'max(p_{T}(-), p_{T}(+))', texY='min(p_{T}(-), p_{T}(+))' )
            for logZ in [False, True]:
                plotting.draw2D( p, logZ = logZ,
                    plot_directory = os.path.join( plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                    extensions=["png", "pdf"], copyIndexPHP=True)
            syncer.sync()
        elif args.sliceEta:
            for nameEta, dict in eta_dictionary.items():
                h2D = sample.get2DHistoFromDraw("log10(min(Pair_tm_pt, Pair_tp_pt)):log10(max(Pair_tm_pt, Pair_tp_pt))", [20,0,2.5,20,-0.5,2], selectionString = preselection_dict[pres]+"&&"+dict['cut'])
                # p = Plot2D.fromHisto( name+"_"+pres+"_"+nameEta, [[h2D]], texX = 'max(p_{T}(-), p_{T}(+)) for {0}'.format(dict['texX']), texY='min(p_{T}(-), p_{T}(+))for {0}'.format(dict['texX']) )
                p = Plot2D.fromHisto( name+"_"+pres+"_"+nameEta, [[h2D]], texX = "max(pT(-), pT(+)) for {}".format(dict['texX']), texY="max(pT(-), pT(+)) for {}".format(dict['texX']) )
                for logZ in [False, True]:
                    plotting.draw2D( p, logZ = logZ,
                        plot_directory = os.path.join( plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                        extensions=["png", "pdf"], copyIndexPHP=True)
                syncer.sync()

# slices in Pair_phi
if args.slicePhi:
    print "Make sliced phi plots"
    slices = [ {'window':(math.pi*(-1+i/3.), math.pi*(-1+(i+1)/3.) ) } for i in range(6) ]
    colors = [ROOT.kBlue, ROOT.kRed, ROOT.kMagenta, ROOT.kGreen, ROOT.kPink, ROOT.kCyan]
    plot_cfg = {
        'Pair_pt':{'var':'Pair_pt', 'binning':[30, 0, 1500], 'texX':"p_{T}(pair) (GeV)"},
        'Pair_pt_low':{'var':'Pair_pt', 'binning':[30, 0, 100], 'texX':"p_{T}(pair) (GeV)"},
        'Pair_eta':{'var':'Pair_eta', 'binning':[30, -3, 3], 'texX':"#eta(pair)"},
        'Pair_phi':{'var':'Pair_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(pair)"},

        'Pair_C_R':{'var':'Pair_C_R', 'binning':[50, 0, 0.4], 'texX':"R(C) (m)"},
        'Pair_C_phi':{'var':'Pair_C_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(C)"},

        'Pair_tm_pt':{'var':'Pair_tm_pt', 'binning':[30, 0, 500], 'texX':"p_{T}(tm) (GeV)"},
        'Pair_tm_pt_low':{'var':'Pair_tm_pt', 'binning':[30, 0, 50], 'texX':"p_{T}(tm) (GeV)"},
        'Pair_tm_eta':{'var':'Pair_tm_eta', 'binning':[30, -3, 3], 'texX':"#eta(tm)"},
        'Pair_tm_phi':{'var':'Pair_tm_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(tm)"},

        'Pair_tp_pt':{'var':'Pair_tp_pt', 'binning':[30, 0, 500], 'texX':"p_{T}(tp) (GeV)"},
        'Pair_tp_pt_low':{'var':'Pair_tp_pt', 'binning':[30, 0, 50], 'texX':"p_{T}(tp) (GeV)"},
        'Pair_tp_eta':{'var':'Pair_tp_eta', 'binning':[30, -3, 3], 'texX':"#eta(tp)"},
        'Pair_tp_phi':{'var':'Pair_tp_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(tp)"},

        'Pair_deltaPhi':{'var':'Pair_deltaPhi', 'binning':[30, -3, 3], 'texX':"#Delta#eta(pair)"},
        'Pair_deltaEta':{'var':'Pair_deltaEta', 'binning':[30, -math.pi, math.pi], 'texX':"#Delta#phi(pair)"},
        }

    plots = []
    for name, p in plot_cfg.items():
        print "At " + name
        h_inc = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection)
        h_inc.SetMarkerStyle( 0 )
        h_inc.legendText = args.sample

        h_slice = {}
        for i_slice_, slice_ in enumerate( slices ):
            h_slice[slice_['window']] = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection+"&&Pair_phi>=%f&&Pair_phi<%f"%(slice_['window']))
            h_slice[slice_['window']].legendText = "%3.2f #leq #phi(Pair) < %3.2f" % slice_['window']
            h_slice[slice_['window']].SetLineColor( colors[i_slice_] )
            h_slice[slice_['window']].SetMarkerColor( colors[i_slice_] )
            h_slice[slice_['window']].SetMarkerStyle( 0 )

        plots.append( Plot.fromHisto( name+"_sliced", [[h_inc]] + [ [h_slice[slice_['window']]] for slice_ in slices], texX = p['texX'] ) )

    for logY in [False, True]:
        for p in plots:
            plotting.draw( p,
                plot_directory = os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logY else "lin")),
                yRange = "auto", extensions=["png"], copyIndexPHP=True)

    syncer.sync()

if args.slicePt:
    print "Make sliced phi plots"
    slices = [ {'window':(i*20, (i+1)*20) } for i in range(5) ]
    colors = [ROOT.kCyan, ROOT.kRed, ROOT.kMagenta, ROOT.kGreen, ROOT.kPink]
    plot_cfg = {
        # 'Pair_pt':{'var':'Pair_pt', 'binning':[30, 0, 1500], 'texX':"p_{T}(pair) (GeV)"},
        # 'Pair_pt_low':{'var':'Pair_pt', 'binning':[30, 0, 100], 'texX':"p_{T}(pair) (GeV)"},
        # 'Pair_eta':{'var':'Pair_eta', 'binning':[30, -3, 3], 'texX':"#eta(pair)"},
        # 'Pair_phi':{'var':'Pair_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(pair)"},

        'Pair_C_R':{'var':'Pair_C_R', 'binning':[50, 0, 0.4], 'texX':"R(C) (m)"},
        # 'Pair_C_phi':{'var':'Pair_C_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(C)"},

        # 'Pair_tm_pt':{'var':'Pair_tm_pt', 'binning':[30, 0, 500], 'texX':"p_{T}(tm) (GeV)"},
        # 'Pair_tm_pt_low':{'var':'Pair_tm_pt', 'binning':[30, 0, 50], 'texX':"p_{T}(tm) (GeV)"},
        # 'Pair_tm_eta':{'var':'Pair_tm_eta', 'binning':[30, -3, 3], 'texX':"#eta(tm)"},
        # 'Pair_tm_phi':{'var':'Pair_tm_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(tm)"},
        #
        # 'Pair_tp_pt':{'var':'Pair_tp_pt', 'binning':[30, 0, 500], 'texX':"p_{T}(tp) (GeV)"},
        # 'Pair_tp_pt_low':{'var':'Pair_tp_pt', 'binning':[30, 0, 50], 'texX':"p_{T}(tp) (GeV)"},
        # 'Pair_tp_eta':{'var':'Pair_tp_eta', 'binning':[30, -3, 3], 'texX':"#eta(tp)"},
        # 'Pair_tp_phi':{'var':'Pair_tp_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(tp)"},
        #
        # 'Pair_deltaPhi':{'var':'Pair_deltaPhi', 'binning':[30, -3, 3], 'texX':"#Delta#eta(pair)"},
        # 'Pair_deltaEta':{'var':'Pair_deltaEta', 'binning':[30, -math.pi, math.pi], 'texX':"#Delta#phi(pair)"},
        }

    plots = []
    for name, p in plot_cfg.items():
        print "At " + name
        h_inc = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection)
        h_inc.SetMarkerStyle( 0 )
        h_inc.legendText = args.sample

        h_slice = {}
        for i_slice_, slice_ in enumerate( slices ):
            h_slice[slice_['window']] = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection+"&&Pair_pt>=%f&&Pair_pt<%f"%(slice_['window']))
            h_slice[slice_['window']].legendText = "%3.2f #leq p_{T,Pair} < %3.2f" % slice_['window']
            h_slice[slice_['window']].SetLineColor( colors[i_slice_] )
            h_slice[slice_['window']].SetMarkerColor( colors[i_slice_] )
            h_slice[slice_['window']].SetMarkerStyle( 0 )

        for i_slice_, slice_ in enumerate( slices ):
            for who in ['isS', 'isC']:
                h_slice[slice_['window']] = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection+"&&Pair_pt>=%f&&Pair_pt<%f&&Pair_%s"%(slice_['window'])%who)
                h_slice[slice_['window']].legendText = "%3.2f #leq p_{T,Pair} < %3.2f for %isS" % (slice_['window'], who)
                h_slice[slice_['window']].SetLineColor( colors[i_slice_] )
                h_slice[slice_['window']].SetMarkerColor( colors[i_slice_] )
                h_slice[slice_['window']].SetMarkerStyle( 0 )

            plots.append( Plot.fromHisto( name+"_sliced_"+who, [[h_inc]] + [ [h_slice[slice_['window']]] for slice_ in slices], texX = p['texX'] ) )

    for logY in [False, True]:
        for p in plots:
            plotting.draw( p,
                plot_directory = os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logY else "lin")),
                yRange = "auto", extensions=["png", "pdf"], copyIndexPHP=True)

    syncer.sync()

# seagulls vs. cowboys (1D)
if args.SC:
    print "S vs. C comparison"
    slices = [ {'sel':'(1)', 'name':'all'}, {'sel':'Pair_isC', 'name':'isC'}, {'sel':'Pair_isS', 'name':'isS'} ]
    colors = [ROOT.kBlue, ROOT.kRed, ROOT.kMagenta, ROOT.kGreen, ROOT.kPink, ROOT.kCyan]
    plot_cfg = {
        'Pair_pt':{'var':'Pair_pt', 'binning':[30, 0, 1500], 'texX':"p_{T}(pair) (GeV)"},
        'Pair_pt_low':{'var':'Pair_pt', 'binning':[30, 0, 100], 'texX':"p_{T}(pair) (GeV)"},
        'Pair_eta':{'var':'Pair_eta', 'binning':[30, -3, 3], 'texX':"#eta(pair)"},
        'Pair_phi':{'var':'Pair_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(pair)"},

        'Pair_C_R':{'var':'Pair_C_R', 'binning':[50, 0, 0.4], 'texX':"R(C) (m)"},
        'Pair_C_phi':{'var':'Pair_C_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(C)"},

        'Pair_tm_pt':{'var':'Pair_tm_pt', 'binning':[30, 0, 500], 'texX':"p_{T}(tm) (GeV)"},
        'Pair_tm_pt_low':{'var':'Pair_tm_pt', 'binning':[30, 0, 50], 'texX':"p_{T}(tm) (GeV)"},
        'Pair_tm_eta':{'var':'Pair_tm_eta', 'binning':[30, -3, 3], 'texX':"#eta(tm)"},
        'Pair_tm_phi':{'var':'Pair_tm_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(tm)"},

        'Pair_tp_pt':{'var':'Pair_tp_pt', 'binning':[30, 0, 500], 'texX':"p_{T}(tp) (GeV)"},
        'Pair_tp_pt_low':{'var':'Pair_tp_pt', 'binning':[30, 0, 50], 'texX':"p_{T}(tp) (GeV)"},
        'Pair_tp_eta':{'var':'Pair_tp_eta', 'binning':[30, -3, 3], 'texX':"#eta(tp)"},
        'Pair_tp_phi':{'var':'Pair_tp_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(tp)"},
        }

    plots = []
    for name, p in plot_cfg.items():
        print "At " + name
        h_inc = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection)
        h_inc.SetMarkerStyle( 0 )
        h_inc.legendText = args.sample

        h_slice = {}
        for i_slice_, slice_ in enumerate( slices ):
            h_slice[slice_['name']] = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection+"&&"+slice_['sel'])
            h_slice[slice_['name']].legendText = slice_['name']
            h_slice[slice_['name']].SetLineColor( colors[i_slice_] )
            h_slice[slice_['name']].SetMarkerColor( colors[i_slice_] )
            h_slice[slice_['name']].SetMarkerStyle( 0 )

        plots.append( Plot.fromHisto( name+"_SvsC", [[h_inc]] + [ [h_slice[slice_['name']]] for slice_ in slices], texX = p['texX'] ) )

    for logY in [False, True]:
        for p in plots:
            plotting.draw( p,
                plot_directory = os.path.join( plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logY else "lin")),
                yRange = "auto", extensions=["png"], copyIndexPHP=True)

    syncer.sync()

# slices in C_R
if args.sliceR:

    print "Slices C_R"

    slices = [ {'window':( 0.16*i/6, 0.16*(i+1)/6. ) } for i in range(6) ]
    colors = [ROOT.kBlue, ROOT.kRed, ROOT.kMagenta, ROOT.kGreen, ROOT.kPink, ROOT.kCyan]
    plot_cfg = {
        'Pair_pt':{'var':'Pair_pt', 'binning':[30, 0, 1500], 'texX':"p_{T}(pair) (GeV)"},
        'Pair_pt_low':{'var':'Pair_pt', 'binning':[30, 0, 100], 'texX':"p_{T}(pair) (GeV)"},
        'Pair_eta':{'var':'Pair_eta', 'binning':[30, -3, 3], 'texX':"#eta(pair)"},
        'Pair_phi':{'var':'Pair_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(pair)"},

        'Pair_C_R':{'var':'Pair_C_R', 'binning':[50, 0, 0.4], 'texX':"R(C) (m)"},
        'Pair_C_phi':{'var':'Pair_C_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(C)"},

        'Pair_tm_pt':{'var':'Pair_tm_pt', 'binning':[30, 0, 500], 'texX':"p_{T}(tm) (GeV)"},
        'Pair_tm_pt_low':{'var':'Pair_tm_pt', 'binning':[30, 0, 50], 'texX':"p_{T}(tm) (GeV)"},
        'Pair_tm_eta':{'var':'Pair_tm_eta', 'binning':[30, -3, 3], 'texX':"#eta(tm)"},
        'Pair_tm_phi':{'var':'Pair_tm_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(tm)"},

        'Pair_tp_pt':{'var':'Pair_tp_pt', 'binning':[30, 0, 500], 'texX':"p_{T}(tp) (GeV)"},
        'Pair_tp_pt_low':{'var':'Pair_tp_pt', 'binning':[30, 0, 50], 'texX':"p_{T}(tp) (GeV)"},
        'Pair_tp_eta':{'var':'Pair_tp_eta', 'binning':[30, -3, 3], 'texX':"#eta(tp)"},
        'Pair_tp_phi':{'var':'Pair_tp_phi', 'binning':[30, -math.pi, math.pi], 'texX':"#phi(tp)"},
        }

    plots = []
    for name, p in plot_cfg.items():
        print "At " + name
        h_inc = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection)
        h_inc.SetMarkerStyle( 0 )
        h_inc.legendText = args.sample

        h_slice = {}
        for i_slice_, slice_ in enumerate( slices ):
            h_slice[slice_['window']] = sample.get1DHistoFromDraw(p['var'], p['binning'], selectionString = preselection+"&&Pair_C_R>=%f&&Pair_C_R<%f"%(slice_['window']))
            h_slice[slice_['window']].legendText = "%3.2f #leq R_{C}(Pair) < %3.2f" % slice_['window']
            h_slice[slice_['window']].SetLineColor( colors[i_slice_] )
            h_slice[slice_['window']].SetMarkerColor( colors[i_slice_] )
            h_slice[slice_['window']].SetMarkerStyle( 0 )

        plots.append( Plot.fromHisto( name+"_sliced_C_R", [[h_inc]] + [ [h_slice[slice_['window']]] for slice_ in slices], texX = p['texX'] ) )

    for logY in [False, True]:
        for p in plots:
            plotting.draw( p,
                plot_directory = os.path.join( plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logY else "lin")),
                yRange = "auto", extensions=["png"], copyIndexPHP=True)

    syncer.sync()

# 2D pair pt eta vs phi

selections = {"cut1":{"selection":"abs(log(Pair_tm_pt/Pair_tp_pt))<1 && Pair_tm_pt*Pair_tp_pt<3**2",    "name":"log_1_pt_3"},
              "cut2":{"selection":"abs(log(Pair_tm_pt/Pair_tp_pt))<1 && Pair_tm_pt*Pair_tp_pt<5**2",    "name":"log_1_pt_5"},
              "cut3":{"selection":"abs(log(Pair_tm_pt/Pair_tp_pt))<1 && Pair_tm_pt*Pair_tp_pt<10**2",   "name":"log_1_pt_10"},
              "cut4":{"selection":"abs(log(Pair_tm_pt/Pair_tp_pt))<2 && Pair_tm_pt*Pair_tp_pt<3**2",    "name":"log_2_pt_3"},
              "cut5":{"selection":"abs(log(Pair_tm_pt/Pair_tp_pt))<2 && Pair_tm_pt*Pair_tp_pt<5**2",    "name":"log_2_pt_5"},
              "cut6":{"selection":"abs(log(Pair_tm_pt/Pair_tp_pt))<2 && Pair_tm_pt*Pair_tp_pt<10**2",   "name":"log_2_pt_10"},
              "cut7":{"selection":"abs(log(Pair_tm_pt/Pair_tp_pt))<3 && Pair_tm_pt*Pair_tp_pt<3**2",    "name":"log_3_pt_3"},
              "cut8":{"selection":"abs(log(Pair_tm_pt/Pair_tp_pt))<3 && Pair_tm_pt*Pair_tp_pt<5**2",    "name":"log_3_pt_5"},
              "cut9":{"selection":"abs(log(Pair_tm_pt/Pair_tp_pt))<3 && Pair_tm_pt*Pair_tp_pt<10**2",   "name":"log_3_pt_10"},
            }

if args.occ:
    args.plot_directory+="occupancy"
    print "Make 2D plots"
    h2D = {}
    name = "occupancy_Pair_C_phi_vs_Pair_C_r"

    for what in ["isC", "isS"]:
        h2D[what] = sample.get2DHistoFromDraw("Pair_C_R:Pair_C_phi", [80, -math.pi, math.pi, 10, 0, 0.16], selectionString='Jet_pt>100')

        # Plot and save individual histograms for isC and isS
        p = Plot2D.fromHisto(name + "_" + what, [[h2D[what]]], texX="C_{#phi} for %s" % what, texY="C_{R} for %s" % what)
        for logZ in [False, True]:
            plotting.draw2D(p, logZ=logZ,
                            plot_directory=os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                            extensions=["png"], copyIndexPHP=True)

    for selection in selections.keys():
        selection_criteria = selections[selection]["selection"]
        cut_name = selections[selection]["name"]

        for what in ["isC", "isS"]:
            h2D[what] = sample.get2DHistoFromDraw("Pair_C_R:Pair_C_phi", [80, -math.pi, math.pi, 10, 0, 0.16], selectionString=preselection + "&&" + selection_criteria + "&&Pair_" + what)

            # Plot and save individual histograms for isC and isS
            p = Plot2D.fromHisto(name + "_" + what + "_" + cut_name, [[h2D[what]]], texX="C_{#phi} for %s" % what, texY="C_{R} for %s" % what)
            for logZ in [False, True]:
                plotting.draw2D(p, logZ=logZ,
                                plot_directory=os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                                extensions=["png"], copyIndexPHP=True)

        # Calculate and save the ratio for the current cut
        ratio_name = "ratio_" + name + "_" + cut_name
        ratios = h2D["isC"].Clone(ratio_name)
        ratios.Divide(h2D["isS"])
        for logZ in [False, True]:
            # Plot and save the ratio
            p = Plot2D.fromHisto(ratio_name, [[ratios]], texX="C_{#phi}", texY="R_{#phi}")
            plotting.draw2D(p, logZ=logZ,
                            plot_directory=os.path.join(plot_directory, "JetTracking", args.plot_directory, args.data_version, args.sample, ("log" if logZ else "lin")),
                            extensions=["png"], copyIndexPHP=False)

    syncer.sync()



# file:/eos/vbc/group/cms/robert.schoefbeck/tttt/miniAOD/Run2SIM_UL2016MiniAOD/TTTT_13TeV_madgraph_pythia8_Run2SIM_UL2016MiniAOD_231227_194239/try-2/MiniAOD_0001.root
# file:/eos/vbc/group/cms/robert.schoefbeck/tttt/miniAOD/Run2SIM_UL2016preVFPMiniAOD/TTTT_13TeV_madgraph_pythia8_Run2SIM_UL2016preVFPMiniAOD_231227_194504/try-2/MiniAOD_0001.root
# file:/eos/vbc/group/cms/robert.schoefbeck/tttt/miniAOD/Run2SIM_UL2017MiniAOD/TTTT_13TeV_madgraph_pythia8_Run2SIM_UL2017MiniAOD_231227_194331/try-2/MiniAOD_0001.root
# file:/eos/vbc/group/cms/robert.schoefbeck/tttt/miniAOD/Run2SIM_UL2018MiniAOD/TTTT_13TeV_madgraph_pythia8_Run2SIM_UL2018MiniAOD_231227_194417/try-2/MiniAOD_0001.root
#
# file:/eos/vbc/group/cms/robert.schoefbeck/tttt/miniAOD/Run2SIM_UL2016MiniAOD/TTbb_13TeV_madgraph_pythia8_Run2SIM_UL2016MiniAOD_240105_070820/try-2/MiniAOD_0001.root
# file:/eos/vbc/group/cms/robert.schoefbeck/tttt/miniAOD/Run2SIM_UL2016preVFPMiniAOD/TTbb_13TeV_madgraph_pythia8_Run2SIM_UL2016preVFPMiniAOD_240105_071106/try-2/MiniAOD_0001.root
# file:/eos/vbc/group/cms/robert.schoefbeck/tttt/miniAOD/Run2SIM_UL2017MiniAOD/TTbb_13TeV_madgraph_pythia8_Run2SIM_UL2017MiniAOD_240105_070919/try-2/
# file:/eos/vbc/group/cms/robert.schoefbeck/tttt/miniAOD/Run2SIM_UL2018MiniAOD/TTbb_13TeV_madgraph_pythia8_Run2SIM_UL2018MiniAOD_240105_071015/try-2/
