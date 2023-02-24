import os
import logging
import ROOT
import itertools
from tWZ.Tools.helpers import deltaR2
#RootTools
from RootTools.core.standard import *



s = FWLiteSample.fromFiles("test", ["root://cms-xrd-global.cern.ch//store/data/Run2018D/DoubleMuon/AOD/15Feb2022_UL2018-v1/2430000/0154B378-D9C6-B84C-A2C2-2AE956E91590.root"])
