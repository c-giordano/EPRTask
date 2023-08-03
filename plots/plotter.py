#Standard imports
import ROOT
import os, sys
from math import sqrt, cos, pi
from RootTools.core.Sample import Sample
from JetTracking.Tools.user import plot_directory

# argParser
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel', action='store', nargs='?', choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'], default='INFO', help="Log level for logging")
argParser.add_argument('--plot_directory', action='store', default='simplePlots')
argParser.add_argument('--version', action='store', default=2)
argParser.add_argument('--small', action='store_true')
args = argParser.parse_args()

import Analysis.Tools.syncer


# RootTools
from RootTools.core.standard import *
directory_ = "/scratch-cbe/users/robert.schoefbeck/JetTracking/nanoTuples/v2/miniAOD_Fall17/"
def make_dirs( dirs ):
    return [ os.path.join( directory_, dir_ ) for dir_ in dirs ]

file_directories = [f for f in os.listdir("/scratch-cbe/users/robert.schoefbeck/JetTracking/nanoTuples/v2/miniAOD_Fall17/")]


if args.small:
    s0 = Sample.fromDirectory(name="DY", treeName="Events", isData=False, texName="DY", directory=make_dirs(["DYJetsToLL_M50_HT100to200_LO"]))
else:
    s0 = Sample.fromDirectory(name="DY", treeName="Events", isData=False, texName="DY", directory=make_dirs(file_directories))

s0.style = styles.lineStyle( color = ROOT.kBlue )

if args.small: args.plot_directory += "_small"

plot_directory_ = os.path.join(plot_directory, 'v{}'.format(args.version), args.plot_directory)


logger = get_logger(args.logLevel, logFile = None)
selectionString = "Pair_pt>10"

stack = Stack( [ s0 ] )

plot_weight   = lambda event, sample : 1


# Variables to be read from the tree
pairVars = ["pt/F","eta/F","phi/F","mass/F",
            "deltaPhi/F","deltaEta/F","isC/I","isS/I",
            "tp_pt/F","tp_eta/F","tp_phi/F","tm_pt/F",
            "tm_eta/F","tm_phi/F","C_R/F",
            "C_x/F", "C_y/F"]
pairVarNames     = [x.split('/')[0] for x in pairVars]

jetVars     =   ['pt/F', 'eta/F', 'phi/F']
jetVarNames     = [x.split('/')[0] for x in jetVars]


read_variables = []
read_variables += [
     "Pair[%s]"%(",".join(pairVars)),
     "Jet[%s]"%(",".join(jetVars)),
     "Z_pt/F", "Z_eta/F", "Z_phi/F", "Z_mass/F",
     "Track_pt/F", "Track_eta/F", "Track_phi/F"
     #"evt/l", "run/I", "lumi/I",
    ]

#Sequence to be executed
sequence = []
plots = []

plots.append(Plot(
    name = "Pair_pt",
    stack = stack,
    attribute = TreeVariable.fromString( "Pair_pt/F" ),
    binning = [50,0,150],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = 'Pair_eta',
    stack = stack,
    attribute = TreeVariable.fromString( "Pair_eta/F" ),
    binning=[20,-3,3],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Pair_phi",
    stack = stack,
    attribute = TreeVariable.fromString( "Pair_phi/F" ),
    binning=[10,-pi,pi],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Pair_mass",
    stack = stack,
    attribute = TreeVariable.fromString( "Pair_mass/F" ),
    binning = [20,0,60],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Pair_deltaPhi",
    stack = stack,
    attribute = TreeVariable.fromString( "Pair_deltaPhi/F" ),
    binning = [10,-1,1],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Pair_deltaEta",
    stack = stack,
    attribute = TreeVariable.fromString( "Pair_deltaEta/F" ),
    binning = [10,-1,1],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Pair_C_R", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Pair_C_R/F" ),
    binning = [40,0,60],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Pair_C_x", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Pair_C_x/F" ),
    binning = [40,0,60],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Pair_C_y", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Pair_C_y/F" ),
    binning = [40,0,60],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Jet_pt", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Jet_pt/F" ),
    binning = [50,0,100],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Jet_eta", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Jet_eta/F" ),
    binning=[20,-3,3],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Jet_phi", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Jet_phi/F" ),
    binning=[20,-pi,pi],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Z_pt", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Z_pt/F" ),
    binning=[70,0,140],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Z_eta", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Z_eta/F" ),
    binning=[20,-3,3],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Z_phi", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Z_phi/F" ),
    binning=[20,-pi,pi],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Z_mass", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Z_mass/F" ),
    binning=[20,60,120],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Track_pt", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Track_pt/F" ),
    binning=[70,0,140],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Track_eta", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Track_eta/F" ),
    binning=[20,-3,3],
    selectionString = selectionString,
    weight = plot_weight
))

plots.append(Plot(
    name = "Track_phi", # Name is not needed. If not provided, variable.name is used as filename instead.
    stack = stack,
    attribute = TreeVariable.fromString( "Track_phi/F" ),
    binning=[20,-pi,pi],
    selectionString = selectionString,
    weight = plot_weight
))


plotting.fill(plots, read_variables = read_variables, sequence = sequence)

if not os.path.exists( plot_directory_ ): os.makedirs( plot_directory_ )
for plot in plots:
    plotting.draw(plot, plot_directory = plot_directory_,
        ratio =None, # Add a default ratio from the first two elements in the stack
        logX = False, logY = True,
        sorting = True,
        yRange = "auto",
        legend = "auto"
        )
# ratio = {'num':1, 'den':0, 'logY':False, 'style':None, 'texY': 'Data / MC', 'yRange': (0.5, 1.5)}
