def fetch_configuration():

    eta_cut_dict_coarse = {
            "eta_cut01":    {"plus":     {"cut":    "Pair_eta>0&&Pair_eta<1",       "legend": " 0 < #eta < 1"},
                             "minus":    {"cut":    "Pair_eta>-1&&Pair_eta<0",      "legend": "-1 < #eta < 0"}},
            "eta_cut12":    {"plus":     {"cut":    "Pair_eta>1&&Pair_eta<2",       "legend": " 1 < #eta < 2"},
                             "minus":    {"cut":    "Pair_eta>-2&&Pair_eta<-1",     "legend": "-2 < #eta < -1"}},
            "eta_cut23":    {"plus":     {"cut":    "Pair_eta>2&&Pair_eta<3",       "legend": " 2 < #eta < 3"},
                             "minus":    {"cut":    "Pair_eta>-3&&Pair_eta<-2",     "legend": "-3 < #eta < -2"}},
            "eta_cut03":    {"plus":     {"cut":    "Pair_eta>0&&Pair_eta<3",       "legend": " 0 < #eta < 3"},
                             "minus":    {"cut":    "Pair_eta>-3&&Pair_eta<0",      "legend": "-3 < #eta < 0"}}}

    eta_cut_dict_fine = {
            "eta_cut0p5":    {"plus":     {"cut":    "Pair_eta>0&&Pair_eta<0.5",    "legend": " 0 < #eta < 0.5"},
                             "minus":    {"cut":    "Pair_eta>-0.5&&Pair_eta<0",    "legend": "-0.5 < #eta < 0"}},
            "eta_cut0p51":    {"plus":     {"cut":    "Pair_eta>=0.5&&Pair_eta<1",  "legend": " 0.5 < #eta < 1"},
                             "minus":    {"cut":    "Pair_eta>-1&&Pair_eta<=-0.5",  "legend": "-1 < #eta < -0.5"}},
            "eta_cut1p5":    {"plus":     {"cut":    "Pair_eta>=1&&Pair_eta<1.5",   "legend": " 1 < #eta < 1.5"},
                             "minus":    {"cut":    "Pair_eta>-1.5&&Pair_eta<=-1",  "legend": "-1.5 < #eta < -1"}},
            "eta_cut1p52":    {"plus":     {"cut":    "Pair_eta>=1.5&&Pair_eta<2",  "legend": " 1.5 < #eta < 2"},
                             "minus":    {"cut":    "Pair_eta>-2&&Pair_eta<=-1.5",  "legend": "-2 < #eta < -1.5"}},
            "eta_cut2p5":    {"plus":     {"cut":    "Pair_eta>=2&&Pair_eta<2.5",   "legend": " 2 < #eta < 2.5"},
                             "minus":    {"cut":    "Pair_eta>-2.5&&Pair_eta<=-2",  "legend": "-2.5 < #eta < -2"}}}

    Pair_pt_cut_dict = {
            "Pair_pt_20":       {"cut":     "Pair_pt<20",               "legend":  " p_{T, Pair} < 20"},
            "Pair_pt_20to40":    {"cut":     "Pair_pt>20&&Pair_pt<40",   "legend":  " 20 < p_{T, Pair} < 40"},
            "Pair_pt_40to60":    {"cut":     "Pair_pt>40&&Pair_pt<60",   "legend":  " 40 < p_{T, Pair} < 60"},
            "Pair_pt_60to80":    {"cut":     "Pair_pt>60&&Pair_pt<80",   "legend":  " 60 < p_{T, Pair} < 80"},
            "Pair_pt_80":        {"cut":     "Pair_pt>80",               "legend":  " p_{T, Pair} > 80"}}

    mass_dict = {
        "mass_01": {"cut":     "sqrt((2*Pair_tp_pt*Pair_tm_pt*(cosh(Pair_tp_eta-Pair_tm_eta) - cos(Pair_tp_phi-Pair_tm_phi))))>0&&sqrt((2*Pair_tp_pt*Pair_tm_pt*(cosh(Pair_tp_eta-Pair_tm_eta) - cos(Pair_tp_phi-Pair_tm_phi))))<(1)",
                         "legend":  "0 < #sqrt{M} < 1"},
        "mass_12": {"cut":     "sqrt((2*Pair_tp_pt*Pair_tm_pt*(cosh(Pair_tp_eta-Pair_tm_eta) - cos(Pair_tp_phi-Pair_tm_phi))))>=1&&sqrt((2*Pair_tp_pt*Pair_tm_pt*(cosh(Pair_tp_eta-Pair_tm_eta) - cos(Pair_tp_phi-Pair_tm_phi))))<(2)",
                         "legend":  "1 < #sqrt{M} < 2"},
        "mass_25": {"cut":     "sqrt((2*Pair_tp_pt*Pair_tm_pt*(cosh(Pair_tp_eta-Pair_tm_eta) - cos(Pair_tp_phi-Pair_tm_phi))))>(2)&&sqrt((2*Pair_tp_pt*Pair_tm_pt*(cosh(Pair_tp_eta-Pair_tm_eta) - cos(Pair_tp_phi-Pair_tm_phi))))<(5)",
                         "legend":  "2 < #sqrt{M} < 5"}}

    r_cut_dict = {
        "Pair_C_R_10":      {"cut":         "Pair_C_R<10",                  "legend":      "0 < r < 10"},
        "Pair_C_R_10to20":  {"cut":         "Pair_C_R>10&&Pair_C_R<20",     "legend":      "10 < r < 20"},
        "Pair_C_R_20to40":  {"cut":         "Pair_C_R>20&&Pair_C_R<40",     "legend":      " 20 < r < 40"},
        "Pair_C_R_40":      {"cut":         "Pair_C_R>40",                  "legend":      "r > 40"}}

    Jet_pt_dict = {
        "Jet_pt_20":        {"cut":         "Jet_pt<20",                    "legend":      "p_{T, Jet} < 20"},
        "Jet_pt_20to40":    {"cut":         "Jet_pt>=20&&Jet_pt<40",        "legend":      "20 < p_{T, Jet} <40"},
        "Jet_pt_40to60":    {"cut":         "Jet_pt>=40&&Jet_pt<60",        "legend":      "40 < p_{T, Jet} <60"},
        "Jet_pt_60":        {"cut":         "Jet_pt>=60",                   "legend":      "p_{T, Jet} > 60"}}


    return {"eta_cut_coarse":eta_cut_dict_coarse,"eta_cut_fine":eta_cut_dict_fine, "Pair_pt_cut_simple":Pair_pt_cut_dict, "mass_dict": mass_dict, "r_dict": r_cut_dict, "Jet_pt_dict": Jet_pt_dict}
