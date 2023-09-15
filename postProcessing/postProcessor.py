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
argParser.add_argument('--overwrite',          action='store_true', help='Overwrite?')#, default = True)
argParser.add_argument('--copy_input',         action='store_true', help='xrdcp input file?')#, default = True)
args = argParser.parse_args()

# some hard-coded steering variables
minPairPt = 2

import JetTracking.Tools.logger as _logger
logger    = _logger.get_logger( args.logLevel, logFile = None )
import RootTools.core.logger as _logger_rt
logger_rt = _logger_rt.get_logger(args.logLevel, logFile = None)

exec("import JetTracking.samples.%s as samples"%args.sampleFile)
sample = getattr( samples, args.sample )

# Define & create output directory
output_directory = os.path.join(user.postprocessing_output_directory, args.targetDir, args.sampleFile, sample.name)
if not os.path.exists( output_directory ):
    try:
        os.makedirs( output_directory )
    except OSError:
        pass
    logger.info( "Created output directory %s", output_directory )

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

# output file & log files
output_filename =  os.path.join(output_directory, sample.name+ '.root')

# Check whether we have to do anything
if os.path.exists( output_filename ) and checkRootFile( output_filename, checkForObjects=["Events"]) and not args.overwrite:
    logger.info( "File %s found. Quit.", output_filename )
    sys.exit(0)

# relocate original
if args.copy_input:
    sample.copy_files( os.path.join(user.postprocessing_tmp_directory, "input") )

_logger.   add_fileHandler( output_filename.replace('.root', '.log'), args.logLevel )
_logger_rt.add_fileHandler( output_filename.replace('.root', '_rt.log'), args.logLevel )

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
pairVars = "pt/F,eta/F,phi/F,mass/F,deltaPhi/F,deltaEta/F,isC/I,isS/I,tp_pt/F,tp_eta/F,tp_phi/F,tm_pt/F,tm_eta/F,tm_phi/F,C_x/F,C_y/F,C_R/F,C_phi/F"
variables = [
     "Pair[%s]"%pairVars,
     "evt/l", "run/I", "lumi/I",
     "Jet_pt/F", "Jet_eta/F", "Jet_phi/F", "Jet_nTrack/I",
     "Z_pt/F", "Z_eta/F", "Z_phi/F", "Z_mass/F", "Z_l_pdgId/I",
     "Track[pt/F,eta/F,phi/F,charge/I, pdgId/I]"
    ]
pairVarNames = list( map( lambda p:p.split('/')[0], pairVars.split(',') ))
fwliteReader = sample.fwliteReader( products = products )

def fill_vector_collection( event, collection_name, collection_varnames, objects, maxN = 100):
    setattr( event, "n"+collection_name, len(objects) )
    for i_obj, obj in enumerate(objects[:maxN]):
        for var in collection_varnames:
            if var in obj.keys():
                if type(obj[var]) == type("string"):
                    obj[var] = int(ord(obj[var]))
                if type(obj[var]) == type(True):
                    obj[var] = int(obj[var])
                getattr(event, collection_name+"_"+var)[i_obj] = obj[var]

def filler( event ):

    event.run, event.lumi, event.evt = fwliteReader.evt
    if fwliteReader.position % 100==0: logger.info("At event %i/%i", fwliteReader.position, min(fwliteReader.nEvents, maxEvents) if maxEvents>0 else fwliteReader.nEvents)

    Z_cand = None

    muons = filter( lambda p:p.pt()>20., list(fwliteReader.event.muons) )
    if len(muons)>2:
        for m1, m2 in itertools.combinations(muons, 2):

            if m1.charge()+m2.charge()==0 and abs( (m1.p4()+m2.p4()).mass() - 91.2 )<15:
                Z_cand = (m1,m2)
                Z_p4 = Z_cand[0].p4()+Z_cand[1].p4()
                event.Z_pt, event.Z_eta, event.Z_phi, event.Z_mass = Z_p4.Pt(), Z_p4.Eta(), Z_p4.Phi(), Z_p4.M()
#                event.Z_l_pdgId = 13
                break

    jet = None
    if fwliteReader.event.jets.size()>0:
        jets = filter( lambda j:j.muonEnergyFraction()<0.2, list(fwliteReader.event.jets) )
        # print(len(jets))
        if len(jets)>0:
            jet = jets[0]
            event.Jet_pt, event.Jet_eta, event.Jet_phi, event.Jet_mass = jet.p4().Pt(), jet.p4().Eta(), jet.p4().Phi(), jet.p4().M()

    if jet is None or Z_cand is None: return

    # select tracks within a high-pt jet
    if jet and Z_cand:
        our_tracks = sorted( filter( lambda t: deltaR2({'phi':t.phi(), 'eta':t.eta()}, {'phi':jet.phi(), 'eta':jet.eta()})<0.4**2 and abs(t.pdgId())==211, list(fwliteReader.event.pf)+list(fwliteReader.event.pflost) ), key = lambda t:-t.pt() )
        logger.debug( "Our tracks %i, pts: %r" %( len(our_tracks), [t.pt() for t in our_tracks]) )
        event.Jet_nTrack = len(our_tracks)
        #if len(our_tracks)>0:
        #    track = our_tracks[0]
        #    event.Track_pt, event.Track_eta, event.Track_phi, event.Track_charge = track.pt(), track.eta(), track.phi(), track.charge()

        #our_tracks.sort( key = lambda p:-p.pt() )
        fill_vector_collection( event, "Track", ['pt', 'eta', 'phi', 'charge', 'pdgId'], [ {'pt':t.pt(), 'phi':t.phi(), 'eta':t.eta(), 'charge':t.charge(), 'pdgId':t.pdgId()} for t in our_tracks])
        # print(event.Track_charge[0], event.Track_pdgId[0])

        pairs = []
        for i_pair, pair in enumerate(itertools.combinations( list(our_tracks), 2)):
            if pair[0].charge()+pair[1].charge()>=5: continue
            if pair[0].charge()>pair[1].charge():
                tp, tm = pair
            else:
                tm, tp = pair
            tp_p4 = ROOT.Math.PtEtaPhiMVector(tp.pt(), tp.eta(), tp.phi(), 0)
            tm_p4 = ROOT.Math.PtEtaPhiMVector(tm.pt(), tm.eta(), tm.phi(), 0)
            pair_p4 = tp_p4 + tm_p4
            # require minimum pt & OS pairs
            if not pair_p4.pt()>minPairPt: continue

            pair_dict = { 'tp_pt':tp.pt(), 'tp_eta':tp.eta(), 'tp_phi':tp.phi() }
            pair_dict.update( { 'tm_pt':tm.pt(), 'tm_eta':tm.eta(), 'tm_phi':tm.phi()})
            pair_dict.update( { 'pt':pair_p4.Pt(), 'eta':pair_p4.Eta(), 'phi':pair_p4.Phi(), 'mass':pair_p4.M()})
            pair_dict['deltaPhi'] = deltaPhi( pair_dict['tp_phi'], pair_dict['tm_phi'], returnAbs=False)
            pair_dict['deltaEta'] = tp.eta()-tm.eta()
            pair_dict['isC']      = pair_dict['deltaPhi']>0
            pair_dict['isS']      = not pair_dict['isC']

            rp = tp.pt()/(0.3*3.8)
            rm = tm.pt()/(0.3*3.8)

            pair_dict['C_x'] = -2*rp*rm*(rp*cos(tp.phi())-rm*cos(tm.phi()))*sin(tp.phi()-tm.phi())/(rp**2+rm**2-2*rp*rm*cos(tp.phi()-tm.phi()))
            pair_dict['C_y'] = -2*rp*rm*(rp*sin(tp.phi())-rm*sin(tm.phi()))*sin(tp.phi()-tm.phi())/(rp**2+rm**2-2*rp*rm*cos(tp.phi()-tm.phi()))

            pair_dict['C_R']   = sqrt( pair_dict['C_x']**2 + pair_dict['C_y']**2 )
            pair_dict['C_phi'] = atan2( pair_dict['C_y'], pair_dict['C_x'] )

            pairs.append( pair_dict )

            if i_pair>=100: break

        #if len(pairs)>0:
        #    print(pairs)

        fill_vector_collection( event, "Pair", pairVarNames, pairs)

    # We need to report success, because we fill only if we have found pairs
    return len(pairs)>0

# TreeMaker initialisation
tmp_dir     = ROOT.gDirectory
output_file = ROOT.TFile( output_filename, 'recreate')
output_file.cd()
maker = TreeMaker(
    #sequence  = [ filler ],
    variables = [ (TreeVariable.fromString(x) if type(x)==str else x) for x in variables ],
    treeName = "Events"
    )
tmp_dir.cd()

maker.start()
fwliteReader.start()

counter = 0
while fwliteReader.run():
    logger.debug( "Evt: %i %i %i Number of Tracks: %i", fwliteReader.event.evt, fwliteReader.event.lumi, fwliteReader.event.run, fwliteReader.event.pf.size()+fwliteReader.event.pflost.size() )

    #maker.fill()
    success = filler( maker.event )
    if success:
        maker.run()
    counter+=1

    if counter>=maxEvents and maxEvents>0:
        break

output_file.cd()
maker.tree.Write()
output_file.Close()

logger.info( "Done. Output: %s", output_filename )
