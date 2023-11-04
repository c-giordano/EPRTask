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


DoubleMuon_Run2017B = FWLiteSample.fromDAS("DoubleMuon_Run2017B", "/DoubleMuon/Run2017B-UL2017_MiniAODv2-v1/MINIAOD", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DoubleMuon_Run2017C = FWLiteSample.fromDAS("DoubleMuon_Run2017C", "/DoubleMuon/Run2017C-UL2017_MiniAODv2-v1/MINIAOD", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DoubleMuon_Run2017D = FWLiteSample.fromDAS("DoubleMuon_Run2017D", "/DoubleMuon/Run2017D-UL2017_MiniAODv2-v1/MINIAOD", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
# E is empty???
# DoubleMuon_Run2017E = FWLiteSample.fromDAS("DoubleMuon_Run2017E", "/DoubleMuon/Run2017E-UL2017_MiniAODv2-v1/MINIAOD", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
DoubleMuon_Run2017F = FWLiteSample.fromDAS("DoubleMuon_Run2017F", "/DoubleMuon/Run2017F-UL2017_MiniAODv2-v1/MINIAOD", dbFile=dbFile, overwrite=ov, prefix=redirector_global, skipCheck=True)
# DoubleMuon_Run2017 = [DoubleMuon_Run2017B, DoubleMuon_Run2017C, DoubleMuon_Run2017D, DoubleMuon_Run2017E, DoubleMuon_Run2017F]
DoubleMuon_Run2017 = [DoubleMuon_Run2017B, DoubleMuon_Run2017C, DoubleMuon_Run2017D, DoubleMuon_Run2017F]
