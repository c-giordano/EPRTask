''' FWLiteReader example: Loop over a sample and write some data to a histogram.
'''

# Standard imports
import os
import ROOT
import itertools
from   Analysis.Tools.helpers import deltaR2

#RootTools
from RootTools.core.standard import *

# JetTracking
import JetTracking.Tools.user as user

# argParser
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',    action='store', nargs='?',  choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'],  default='INFO', help="Log level for logging")
argParser.add_argument('--sample',      action='store', default='doubleMuon2018', help="Name of the sample.")
argParser.add_argument('--nJobs',              action='store',      nargs='?', type=int, default=1,  help="Maximum number of simultaneous jobs.")
argParser.add_argument('--job',                action='store',      nargs='?', type=int, default=0,  help="Run only job i")
argParser.add_argument('--targetDir',          action='store',      default='v1')
argParser.add_argument('--small',              action='store_true', help='Run only on a small subset of the data?')#, default = True)
args = argParser.parse_args()

import JetTracking.Tools.logger as _logger
logger    = _logger.get_logger( args.logLevel, logFile = None )
import RootTools.core.logger as _logger_rt
logger_rt = _logger_rt.get_logger(args.logLevel, logFile = None)

import JetTracking.samples.AOD as samples
sample = getattr( samples, args.sample )

# Run only job number "args.job" from total of "args.nJobs"
if args.nJobs>1:
    n_files_before = len(sample.files)
    sample = sample.split(args.nJobs)[args.job]
    n_files_after  = len(sample.files)
    logger.info( "Running job %i/%i over %i files from a total of %i.", args.job, args.nJobs, n_files_after, n_files_before)

# small option
maxEvents = -1
if args.small:
    args.targetDir += "_mall"
    maxEvents       = 100
    sample.files=sample.files[:1]

# Define & create output directory
output_directory = os.path.join(user.postprocessing_output_directory, args.targetDir, sample.name) 
if not os.path.exists( output_directory ):
    try:
        os.makedirs( output_directory )
    except OSError:
        pass
    logger.info( "Created output directory %s", output_directory )

# output file & log files
output_filename =  os.path.join(output_directory, sample.name+ '.root')
_logger.   add_fileHandler( output_filename.replace('.root', '.log'), args.logLevel )
_logger_rt.add_fileHandler( output_filename.replace('.root', '_rt.log'), args.logLevel )

# define reader
products = {
#    'slimmedJets':{'type':'vector<pat::Jet>', 'label':("slimmedJets", "", "reRECO")} 
#      'genJets': {'type':'vector<reco::GenJet>', 'label':( "ak4GenJets" ) } ,
    'gt':{'type':'vector<reco::Track>', 'label':("generalTracks", "", "RECO")}, 
    'muons':{'type':'vector<reco::Muon>', 'label':("muons", "", "RECO")}, 
    'jets': {'type': 'vector<reco::PFJet>',  'label': ("ak4PFJets", "", "RECO")}, 
    }

# define tree maker
variables = ["event/l", "run/I", "lumi/I"]

fwliteReader = sample.fwliteReader( products = products )
fwliteReader.start()

def filler( event ):

    event.run, event.lumi, event.evt = fwliteReader.evt
    if fwliteReader.position % 100==0: logger.info("At event %i/%i", fwliteReader.position, fwliteReader.nEvents)

    muons = filter( lambda p:p.pt()>20., list(fwliteReader.event.muons) )
    if len(muons)<2: return

    Z_cand = None
    for m1, m2 in itertools.combinations(muons, 2):
        
        if m1.charge()+m2.charge()==0 and abs( (m1.p4()+m2.p4()).mass() - 91.2 )<15:
            Z_cand = (m1,m2)
            break

    if Z_cand is None: return

    if fwliteReader.event.jets.size()==0:return
   
    jets = filter( lambda j:j.muonEnergyFraction()<0.2, list(fwliteReader.event.jets) ) 
    if len(jets)<1: return
    j = jets[0]

    our_tracks = filter( lambda t: deltaR2({'phi':t.phi(), 'eta':t.eta()}, {'phi':j.phi(), 'eta':j.eta()})<0.4**2, list(fwliteReader.event.gt) )

# TreeMaker initialisation
tmp_dir     = ROOT.gDirectory
output_file = ROOT.TFile( output_filename, 'recreate')
output_file.cd()
maker = TreeMaker(
    sequence  = [ filler ],
    variables = [ (TreeVariable.fromString(x) if type(x)==str else x) for x in variables ],
    treeName = "Events"
    )
tmp_dir.cd()

maker.start()

counter = 0
while fwliteReader.run():
    logger.debug( "Evt: %i %i %i Number of genJets: %i", fwliteReader.event.evt, fwliteReader.event.lumi, fwliteReader.event.run, fwliteReader.event.gt.size() )
    maker.run()
    counter+=1

    if counter>=maxEvents and maxEvents>0:
        break

logger.info( "Done. Output: %s", output_filename )
