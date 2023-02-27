import os

if os.environ["USER"] in ["cristina.giordano"]:
    postprocessing_output_directory = "/scratch-cbe/users/cristina.giordano/JetTracking/nanoTuples"
    postprocessing_tmp_directory    = "/scratch/hephy/cms/cristina.giordano/JetTracking/tmp/"
    plot_directory                  = "/groups/hephy/cms/cristina.giordano/www/JetTracking/plots"
    cache_dir                       = "/groups/hephy/cms/robert.schoefbeck/JetTracking/caches"
    cern_proxy_certificate          = "/users/cristina.giordano/.private/.proxy"
    variations_directory            = "/scratch-cbe/users/cristina.giordano/JetTracking/Variations"

elif os.environ["USER"] in ["robert.schoefbeck"]:
    postprocessing_output_directory = "/scratch-cbe/users/robert.schoefbeck/JetTracking/nanoTuples"
    postprocessing_tmp_directory    = "/scratch/hephy/cms/robert.schoefbeck/JetTracking/tmp/"
    plot_directory                  = "/groups/hephy/cms/robert.schoefbeck/www/JetTracking/plots"
    cache_dir                       = "/groups/hephy/cms/robert.schoefbeck/JetTracking/caches"
