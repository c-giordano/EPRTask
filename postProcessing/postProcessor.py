''' FWLiteReader example: Loop over a sample and write some data to a histogram.
'''

# Standard imports
import os
import ROOT
import itertools
from   Analysis.Tools.helpers import deltaR2

#RootTools
from RootTools.core.standard import *

# argParser
import argparse
argParser = argparse.ArgumentParser(description = "Argument parser")
argParser.add_argument('--logLevel',    action='store', nargs='?',  choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'],  default='INFO', help="Log level for logging")
argParser.add_argument('--sample',      action='store', default='doubleMuon2018', help="Name of the sample.")

args = argParser.parse_args()

import JetTracking.Tools.logger as _logger
logger    = _logger.get_logger( args.logLevel, logFile = None )

import JetTracking.samples.AOD as samples
sample = getattr( samples, args.sample )

sample.reduceFiles( to = 1 )

products = {
#    'slimmedJets':{'type':'vector<pat::Jet>', 'label':("slimmedJets", "", "reRECO")} 
    'gt':{'type':'vector<reco::Track>', 'label':("generalTracks", "", "RECO")}, 
    'muons':{'type':'vector<reco::Muon>', 'label':("muons", "", "RECO")}, 
#      'genJets': {'type':'vector<reco::GenJet>', 'label':( "ak4GenJets" ) } ,
    'jets': {'type': 'vector<reco::PFJet>',  'label': ("ak4PFJets", "", "RECO")}, 
    }

r = sample.fwliteReader( products = products )

r.start()

counter = 0
while r.run():
    print r.event.evt, r.event.lumi, r.event.run, "Number of genJets", r.event.gt.size()
    counter+=1
    muons = filter( lambda p:p.pt()>20., list(r.event.muons) )
    if len(muons)<2: continue

    Z_cand = None
    for m1, m2 in itertools.combinations(muons, 2):
        #print m1.charge(), m2.charge()
        #print (m1.p4()+m2.p4()).mass()
        #print 
        
        if m1.charge()+m2.charge()==0 and abs( (m1.p4()+m2.p4()).mass() - 91.2 )<15:
            Z_cand = (m1,m2)
            break

    if Z_cand is None: continue

    if r.event.jets.size()==0:continue
   
    jets = filter( lambda j:j.muonEnergyFraction()<0.2, list(r.event.jets) ) 
    if len(jets)<1: continue
    j = jets[0]

    #print j.pt()

    our_tracks = filter( lambda t: deltaR2({'phi':t.phi(), 'eta':t.eta()}, {'phi':j.phi(), 'eta':j.eta()})<0.4**2, list(r.event.gt) )

    for t in our_tracks:
        print t.pt(), t.charge()

    print 

    if counter>=500:
        break


