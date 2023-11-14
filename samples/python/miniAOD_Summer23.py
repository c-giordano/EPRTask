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

TTtoLNu2Q = FWLiteSample.fromDAS("TTtoLNu2Q", "/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer23BPixMiniAODv4-130X_mcRun3_2023_realistic_postBPix_v2-v3/MINIAODSIM", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
