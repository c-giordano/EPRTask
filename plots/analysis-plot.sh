#coarse simple
# python analysis-plot.py --version 2 --eta_cut coarse --simple_cut pt
# python analysis-plot.py --version 2 --eta_cut coarse --simple_cut mass
# python analysis-plot.py --version 2 --eta_cut coarse --simple_cut r
# python analysis-plot.py --version 2.1 --eta_cut coarse --simple_cut jetPt
python analysis-plot.py --version 2.2 --eta_cut coarse --simple_cut jetPt_high
python analysis-plot.py --version 2.2 --eta_cut coarse --simple_cut r_high
# Coarse composite
# python analysis-plot.py --version 2 --eta_cut coarse --simple_cut pt --composite_cut mass
# python analysis-plot.py --version 2 --eta_cut coarse --simple_cut pt --composite_cut r
# python analysis-plot.py --version 2 --eta_cut coarse --simple_cut mass --composite_cut r
# python analysis-plot.py --version 2.1 --eta_cut coarse --simple_cut pt --composite_cut jetPt
# python analysis-plot.py --version 2.1 --eta_cut coarse --simple_cut mass --composite_cut jetPt
# python analysis-plot.py --version 2.1 --eta_cut coarse --simple_cut r --composite_cut jetPt
python analysis-plot.py --version 2.2 --eta_cut coarse --simple_cut pt --composite_cut jetPt_high
python analysis-plot.py --version 2.2 --eta_cut coarse --simple_cut mass --composite_cut jetPt_high
python analysis-plot.py --version 2.2 --eta_cut coarse --simple_cut r_high --composite_cut jetPt_high

#Fine simple
# python analysis-plot.py --version 2 --eta_cut fine --simple_cut pt
# python analysis-plot.py --version 2 --eta_cut fine --simple_cut mass
# python analysis-plot.py --version 2 --eta_cut fine --simple_cut r
# python analysis-plot.py --version 2.1 --eta_cut fine --simple_cut jetPt
python analysis-plot.py --version 2.2 --eta_cut fine --simple_cut jetPt_high
python analysis-plot.py --version 2.2 --eta_cut fine --simple_cut r_high
#Fine composite
# python analysis-plot.py --version 2 --eta_cut fine --simple_cut pt --composite_cut mass
# python analysis-plot.py --version 2 --eta_cut fine --simple_cut pt --composite_cut r
# python analysis-plot.py --version 2 --eta_cut fine --simple_cut mass --composite_cut r
# python analysis-plot.py --version 2.1 --eta_cut fine --simple_cut pt --composite_cut jetPt
# python analysis-plot.py --version 2.1 --eta_cut fine --simple_cut mass --composite_cut jetPt
# python analysis-plot.py --version 2.1 --eta_cut fine --simple_cut r --composite_cut jetPt
python analysis-plot.py --version 2.2 --eta_cut fine --simple_cut pt --composite_cut jetPt_high
python analysis-plot.py --version 2.2 --eta_cut fine --simple_cut mass --composite_cut jetPt_high
python analysis-plot.py --version 2.2 --eta_cut fine --simple_cut r_high --composite_cut jetPt_high
#Scatter plot
# python analysis-plot.py --version 2 --plots Scatter
