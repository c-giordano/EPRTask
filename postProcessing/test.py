''' FWLiteReader example: Loop over a sample and write some data to a histogram.
'''

# Standard imports
import os, sys
import ROOT
import itertools
from   Analysis.Tools.helpers import deltaR2, deltaPhi, checkRootFile
from   math import sin, cos, sqrt, atan2

#RootTools
from RootTools.core.standard import *

# JetTracking
import JetTracking.Tools.user as user

# argParser
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',    action='store', nargs='?',  choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'],  default='INFO', help="Log level for logging")
argParser.add_argument('--sample',      action='store', default='DYJetsToLL_M50_HT1200to2500_LO', help="Name of the sample.")
argParser.add_argument('--sampleFile',  action='store', default='miniAOD_Fall17', help="Name of the sample.")
argParser.add_argument('--nJobs',              action='store',      nargs='?', type=int, default=1,  help="Maximum number of simultaneous jobs.")
argParser.add_argument('--job',                action='store',      nargs='?', type=int, default=0,  help="Run only job i")
argParser.add_argument('--targetDir',          action='store',      default='v2')
argParser.add_argument('--small',              action='store_true', help='Run only on a small subset of the data?')#, default = True)
argParser.add_argument('--maxNPairs',          action='store', type=int, default=100, help='Maximum number of pairs.')#, default = True)
argParser.add_argument('--copy_input',         action='store_true', help='xrdcp input file?')#, default = True)
args = argParser.parse_args()

## some hard-coded steering variables
#minPairPt = 2

import JetTracking.Tools.logger as _logger
logger    = _logger.get_logger( args.logLevel, logFile = None )
import RootTools.core.logger as _logger_rt
logger_rt = _logger_rt.get_logger(args.logLevel, logFile = None)

exec("import JetTracking.samples.%s as samples"%args.sampleFile)
sample = getattr( samples, args.sample )
logger.info( "Loaded sample %s from %s" %(args.sample, args.sampleFile) )

# Run only job number "args.job" from total of "args.nJobs"
if args.nJobs>1:
    n_files_before = len(sample.files)
    sample = sample.split(args.nJobs)[args.job]
    n_files_after  = len(sample.files)
    logger.info( "Running job %i/%i over %i files from a total of %i.", args.job, args.nJobs, n_files_after, n_files_before)

# small option
maxEvents = -1
if args.small:
    args.targetDir += "_small"
    maxEvents       = 100
    sample.files=sample.files[:1]

# relocate original
if args.copy_input:
    sample.copy_files( os.path.join(user.postprocessing_tmp_directory, "input") )

# define reader
products = {
    'jets':{'type':'vector<pat::Jet>', 'label':("slimmedJets")},
#      'genJets': {'type':'vector<reco::GenJet>', 'label':( "ak4GenJets" ) } ,
    #'gt':{'type':'vector<reco::Track>', 'label':("generalTracks", "", "RECO")},
#    'gt':{'type':'vector<reco::Track>', 'label':("generalTracks", "", "RECO")},
    #'gt':{'type':'vector<reco::Track>', 'label':("generalTracks", "", "RECO")},
    'pf':{'type':'vector<pat::PackedCandidate>', 'label': ( "packedPFCandidates" )},
    'pflost':{'type':'vector<pat::PackedCandidate>', 'label': ( "lostTracks" )},

    'muons':{'type':'vector<pat::Muon>', 'label':("slimmedMuons", "", "PAT")},
#    'electrons':{'type':'vector<reco::Electron>', 'label':("electrons", "", "RECO")},
#    'jets': {'type': 'vector<reco::PFJet>',  'label': ("ak4PFJets", "", "RECO")},
    }


# define tree maker
pairVars = "pt/F,eta/F,phi/F,mass/F,deltaPhi/F,deltaEta/F,isC/I,isS/I,tp_pt/F,tp_eta/F,tp_phi/F,tm_pt/F,tm_eta/F,tm_phi/F,tp_charge/I,tp_index/I,tm_charge/I,tm_index/I,C_x/F,C_y/F,C_R/F,C_phi/F"
variables = [
     "Pair[%s]"%pairVars,
     "evt/l", "run/I", "lumi/I",
     "Jet_pt/F", "Jet_eta/F", "Jet_phi/F", "Jet_nTrack/I",
     "Z_pt/F", "Z_eta/F", "Z_phi/F", "Z_mass/F", "Z_l_pdgId/I",
     "Track[pt/F,eta/F,phi/F,charge/I, pdgId/I, index/I]"
    ]
pairVarNames = list( map( lambda p:p.split('/')[0], pairVars.split(',') ))
fwliteReader = sample.fwliteReader( products = products )

fwliteReader.start()

while fwliteReader.run():
    if not fwliteReader.products['jets'].size()>0: continue
    jet = fwliteReader.products['jets'][0] 
    our_tracks = jet.getJetConstituents()
    if not our_tracks.size()>0: continue

    print [t.pt() for t in our_tracks]
