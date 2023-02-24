import os

if os.environ["USER"] in ["cristina.giordano"]:
    postprocessing_output_directory = "/scratch-cbe/users/cristina.giordano/tttt/nanoTuples"
    postprocessing_tmp_directory    = "/scratch/hephy/cms/cristina.giordano/tttt/tmp/"
    plot_directory                  = "/groups/hephy/cms/cristina.giordano/www/tttt/plots"
    cache_dir                       = "/groups/hephy/cms/robert.schoefbeck/tttt/caches"
    cern_proxy_certificate          = "/users/cristina.giordano/.private/.proxy"
    gridpack_directory              = "/eos/vbc/user/robert.schoefbeck/gridpacks/4top/"
    variations_directory            = "/scratch-cbe/users/cristina.giordano/tttt/Variations"

elif os.environ["USER"] in ["robert.schoefbeck"]:
    postprocessing_output_directory = "/scratch-cbe/users/robert.schoefbeck/tttt/nanoTuples"
    postprocessing_tmp_directory    = "/scratch/hephy/cms/robert.schoefbeck/tttt/tmp/"
    plot_directory                  = "/groups/hephy/cms/robert.schoefbeck/www/tttt/plots"
    cache_dir                       = "/groups/hephy/cms/robert.schoefbeck/tttt/caches"
    gridpack_directory              = "/eos/vbc/user/robert.schoefbeck/gridpacks/4top/"
