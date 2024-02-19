from RootTools.core.standard import *
import RootTools.core.logger as logger_rt
import os

location = "/scratch-cbe/users/cristina.giordano/JetTracking/nanoTuples/v9/miniAOD_Fall17/"

DYJetsToLL_M50_LO  = Sample.fromDirectory( "DYJetsToLL_M50_LO", [ os.path.join( location, "DYJetsToLL_M50_LO")])
