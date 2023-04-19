import copy, os, sys
from RootTools.core.standard import *
import ROOT

def get_parser():
    import argparse
    argParser = argparse.ArgumentParser(description = "Argument parser for samples file")
    argParser.add_argument('--logLevel',    action='store', nargs='?',  choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'TRACE', 'NOTSET'],  default='INFO', help="Log level for logging")
    argParser.add_argument('--overwrite',   action='store_true',    help="Overwrite current entry in db?")
    argParser.add_argument('--update',      action='store_true',    help="Update current entry in db?")
    argParser.add_argument('--check_completeness', action='store_true',    help="Check competeness?")
    return argParser

# Logging
if __name__=="__main__":
    args = get_parser().parse_args()
    ov = args.overwrite
    if args.update:
        ov = 'update'
    import Samples.Tools.logger as logger
    logger = logger.get_logger(args.logLevel, logFile = None )
    import RootTools.core.logger as logger_rt
    logger_rt = logger_rt.get_logger(args.logLevel, logFile = None )
else:
    import logging
    logger = logging.getLogger(__name__)
    ov = False

from Samples.Tools.config import  redirector_global
redirector = redirector_global

## DB
from Samples.Tools.config import dbDir
dbFile = dbDir+'/JetTracking_AOD.sql'
logger.info("Using db file: %s", dbFile)

doubleMuon2018 = FWLiteSample.fromFiles("DoubleMu", ["root://cms-xrd-global.cern.ch//store/data/Run2018D/DoubleMuon/AOD/15Feb2022_UL2018-v1/2430000/0154B378-D9C6-B84C-A2C2-2AE956E91590.root"])

DYJetsToLL_M50     = FWLiteSample.fromDAS("DYJetsToLL_M50", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM", prefix=redirector, dbFile=dbFile, overwrite=ov, skipCheck=True)
DYJetsToLL_M50_ext = FWLiteSample.fromDAS("DYJetsToLL_M50_ext", "/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6_ext1-v1/AODSIM", prefix=redirector, dbFile=dbFile, overwrite=ov, skipCheck=True)

DYJetsToLL_M50_HT100to200  = FWLiteSample.fromDAS("DYJetsToLL_M50_HT100to200", "/DYJetsToLL_M-50_HT-100to200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM", prefix=redirector, dbFile=dbFile, overwrite=ov, skipCheck=True)
DYJetsToLL_M50_HT1200to2500= FWLiteSample.fromDAS("DYJetsToLL_M50_HT1200to2500", "/DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM",  prefix=redirector, dbFile=dbFile, overwrite=ov, skipCheck=True)
DYJetsToLL_M50_HT200to400  = FWLiteSample.fromDAS("DYJetsToLL_M50_HT200to400", "/DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM", prefix=redirector, dbFile=dbFile, overwrite=ov, skipCheck=True)
DYJetsToLL_M50_HT2500toInf = FWLiteSample.fromDAS("DYJetsToLL_M50_HT2500toInf", "/DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM", prefix=redirector, dbFile=dbFile, overwrite=ov, skipCheck=True)
DYJetsToLL_M50_HT400to600  = FWLiteSample.fromDAS("DYJetsToLL_M50_HT400to600", "/DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM",  prefix=redirector, dbFile=dbFile, overwrite=ov, skipCheck=True)
DYJetsToLL_M50_HT600to800  = FWLiteSample.fromDAS("DYJetsToLL_M50_HT600to800", "/DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM", prefix=redirector, dbFile=dbFile, overwrite=ov, skipCheck=True)
DYJetsToLL_M50_HT70to100   = FWLiteSample.fromDAS("DYJetsToLL_M50_HT70to100", "/DYJetsToLL_M-50_HT-70to100_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM", prefix=redirector, dbFile=dbFile, overwrite=ov, skipCheck=True)
DYJetsToLL_M50_HT800to1200 = FWLiteSample.fromDAS("DYJetsToLL_M50_HT800to1200", "/DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8/RunIISummer20UL17RECO-106X_mc2017_realistic_v6-v1/AODSIM", prefix=redirector, dbFile=dbFile, overwrite=ov, skipCheck=True)
