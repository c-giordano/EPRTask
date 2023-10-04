
from RootTools.core.standard import *
import RootTools.core.logger as logger_rt
import os

location = "/scratch-cbe/users/robert.schoefbeck/JetTracking/nanoTuples/v3/miniAOD_Fall17/"

DYJetsToLL_M50_HT100to200_LO =      Sample.fromDirectory( "DYJetsToLL_M50_HT100to200_LO",      [ os.path.join( location, "DYJetsToLL_M50_HT100to200_LO")])
DYJetsToLL_M50_HT100to200_LO_ext1 = Sample.fromDirectory( "DYJetsToLL_M50_HT100to200_LO_ext1", [ os.path.join( location, "DYJetsToLL_M50_HT100to200_LO_ext1")])
DYJetsToLL_M50_HT1200to2500_LO =    Sample.fromDirectory( "DYJetsToLL_M50_HT1200to2500_LO",    [ os.path.join( location, "DYJetsToLL_M50_HT1200to2500_LO")])
DYJetsToLL_M50_HT200to400_LO =      Sample.fromDirectory( "DYJetsToLL_M50_HT200to400_LO",      [ os.path.join( location, "DYJetsToLL_M50_HT200to400_LO")])
DYJetsToLL_M50_HT200to400_LO_ext1 = Sample.fromDirectory( "DYJetsToLL_M50_HT200to400_LO_ext1", [ os.path.join( location, "DYJetsToLL_M50_HT200to400_LO_ext1")])
DYJetsToLL_M50_HT2500toInf_LO =     Sample.fromDirectory( "DYJetsToLL_M50_HT2500toInf_LO",     [ os.path.join( location, "DYJetsToLL_M50_HT2500toInf_LO")])
DYJetsToLL_M50_HT400to600_LO =      Sample.fromDirectory( "DYJetsToLL_M50_HT400to600_LO",      [ os.path.join( location, "DYJetsToLL_M50_HT400to600_LO")])
DYJetsToLL_M50_HT400to600_LO_ext1 = Sample.fromDirectory( "DYJetsToLL_M50_HT400to600_LO_ext1", [ os.path.join( location, "DYJetsToLL_M50_HT400to600_LO_ext1")])
DYJetsToLL_M50_HT600to800_LO =      Sample.fromDirectory( "DYJetsToLL_M50_HT600to800_LO",      [ os.path.join( location, "DYJetsToLL_M50_HT600to800_LO")])
DYJetsToLL_M50_HT70to100_LO =       Sample.fromDirectory( "DYJetsToLL_M50_HT70to100_LO",       [ os.path.join( location, "DYJetsToLL_M50_HT70to100_LO")])
DYJetsToLL_M50_HT800to1200_LO =     Sample.fromDirectory( "DYJetsToLL_M50_HT800to1200_LO",     [ os.path.join( location, "DYJetsToLL_M50_HT800to1200_LO")])
DYJetsToLL_M50_LO =                 Sample.fromDirectory( "DYJetsToLL_M50_LO",                 [ os.path.join( location, "DYJetsToLL_M50_LO")])
DYJetsToLL_M50_LO_ext1 =            Sample.fromDirectory( "DYJetsToLL_M50_LO_ext1",            [ os.path.join( location, "DYJetsToLL_M50_LO_ext1")])
DYJetsToLL_M50_NLO =                Sample.fromDirectory( "DYJetsToLL_M50_NLO",                [ os.path.join( location, "DYJetsToLL_M50_NLO")])
