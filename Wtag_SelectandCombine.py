#! /usr/bin/env python


## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 
import sys
import math
import array as array
from optparse import OptionParser

# This script reads serveral TTrees and writes combined trees into root files and well as a seperate output root file with the histograms of W candidate (SD subjet 0 from Semi-Leptonic TTbar selection) mass binned by the pt of the w candidate 

def Wtag_SelectandCombine(argv) : 
    parser = OptionParser()

    parser.add_option('--maxEvents', type='int', action='store',
                  default=-1,
                  dest='maxEvents',
                  help='Number of events to run. -1 is all events')

    parser.add_option('--filestr', type='string', action='store',
                      dest='filestr',
                      default = '',
                      help='File string') 

    parser.add_option('--tau32Cut', type='float', action='store',
                      dest='tau32Cut',
                      default = 0.7,
                      help='Tau32 < tau32Cut')

    parser.add_option('--Ak8PtCut', type='float', action='store',
                      dest='Ak8PtCut',
                      default = 350.,
                      help='Ak8Pt < Ak8PtCut')

    parser.add_option('--tau21Cut', type='float', action='store',
                      dest='tau21Cut',
                      default = 1.1,
                      help='Tau21 < tau21Cut')

    parser.add_option('--combineTrees', action='store_true',
                      default=False,
                      dest='combineTrees',
                      help='Do you want to create combined ttrees???')

    parser.add_option('--verbose', action='store_true',
                      default=False,
                      dest='verbose',
                      help='Do you want to print values of key variables?')

    (options, args) = parser.parse_args(argv)
    argv = []

 #   print '===== Command line options ====='
 #   print options
 #   print '================================'

    import ROOT
    ROOT.gStyle.SetOptStat(0000000000)


    if options.combineTrees and options.filestr == 'LooseWP':

        sys.argv.remove('--combineTrees')
        sys.argv.remove('--filestr')
        sys.argv.remove('LooseWP')
        sys.argv.remove('--tau21Cut')
        sys.argv.remove('0.6')

    if options.combineTrees and options.filestr == 'TightWP':

        sys.argv.remove('--combineTrees')
        sys.argv.remove('--filestr')
        sys.argv.remove('TightWP')
        sys.argv.remove('--tau21Cut')
        sys.argv.remove('0.45')


    if options.combineTrees :
        sys.argv.append('--type')
        sys.argv.append('data')
 
        print sys.argv

        from treeCombiner import *
        treeCombiner(sys.argv)

        sys.argv.remove('--type')
        sys.argv.remove('data')

        sys.argv.append('--type')
        sys.argv.append('ttjets')
 
        print sys.argv

        treeCombiner(sys.argv)


        filesout = ['./alphaMethod/ttjets_combinedttree_afterSelection_76x_v1p2_puppi.root',
                './alphaMethod/data_combinedttree_afterSelection_76x_v1p2_puppi.root']

        foutlist = []
        treelist = []

        if options.combineTrees:
            for ifile, filee in enumerate(filesout) :
                
                foutlist.append( ROOT.TFile( filee, "RECREATE") )

                foutlist[ifile].cd()

                treelist.append(ROOT.TTree("TreeSemiLept", "TreeSemiLept") )

                SemiLeptWeight_      = array.array('f', [-1.])

                FatJetRhoRatio_      = array.array('f', [-1.])
                FatJetMass_          = array.array('f', [-1.])
                FatJetPt_          = array.array('f', [-1.])
                FatJetMassSoftDrop_  = array.array('f', [-1.])
                FatJetPtSoftDrop_  = array.array('f', [-1.])
                FatJetTau1_          = array.array('f', [-1.]) 
                FatJetTau2_          = array.array('f', [-1.]) 
                FatJetTau3_          = array.array('f', [-1.]) 
                FatJetTau32_         = array.array('f', [-1.])
                FatJetTau21_         = array.array('f', [-1.]) 

                FatJetSDsubjetWpt_   = array.array('f', [-1.])
                FatJetSDsubjetWmass_ = array.array('f', [-1.])
                FatJetSDsubjetWtau1_ = array.array('f', [-1.])
                FatJetSDsubjetWtau2_ = array.array('f', [-1.])
                FatJetSDsubjetWtau3_ = array.array('f', [-1.])
                FatJetSDsubjetWtau21_ = array.array('f', [-1.])

                FatJetSDsubjet_isRealW_ = array.array('f', [-1.])
                FatJetSDsubjet_isFakeW_ = array.array('f', [-1.])

                FatJetSDsubjetBpt_   = array.array('f', [-1.])
                FatJetSDsubjetBmass_ = array.array('f', [-1.])
                FatJetSDsubjetBbdisc_ = array.array('f', [-1.])

                LeptonType_          = array.array('i', [-1])
                LeptonPt_            = array.array('f', [-1.])

                LeptonPtRel_         = array.array('f', [-1.])
                LeptonDRMin_         = array.array('f', [-1.])

                SemiLepMETpt_        = array.array('f', [-1.])

                SemiLeptRunNum_        = array.array('f', [-1.])   
                SemiLeptLumiBlock_     = array.array('f', [-1.])   
                SemiLeptEventNum_      = array.array('f', [-1.])   

                treelist[ifile].Branch('SemiLeptWeight'      , SemiLeptWeight_      ,  'SemiLeptWeight/F'      )
               
                treelist[ifile].Branch('FatJetRhoRatio'      , FatJetRhoRatio_      ,  'FatJetRhoRatio/F'      )
                treelist[ifile].Branch('FatJetMass'          , FatJetMass_          ,  'FatJetMass/F'          )
                treelist[ifile].Branch('FatJetPt'          , FatJetPt_          ,  'FatJetPt/F'          )
                treelist[ifile].Branch('FatJetMassSoftDrop'  , FatJetMassSoftDrop_  ,  'FatJetMassSoftDrop/F'  )
                treelist[ifile].Branch('FatJetPtSoftDrop'  , FatJetPtSoftDrop_  ,  'FatJetPtSoftDrop/F'  )
                treelist[ifile].Branch('FatJetTau1'          , FatJetTau1_          ,  'FatJetTau1/F'          )
                treelist[ifile].Branch('FatJetTau2'          , FatJetTau2_          ,  'FatJetTau2/F'          )
                treelist[ifile].Branch('FatJetTau3'          , FatJetTau3_          ,  'FatJetTau3/F'          )
                treelist[ifile].Branch('FatJetTau21'         , FatJetTau21_         ,  'FatJetTau21/F'         )
                treelist[ifile].Branch('FatJetTau32'         , FatJetTau32_         ,  'FatJetTau32/F'         )

                treelist[ifile].Branch('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt_   ,  'FatJetSDsubjetWpt/F'   )
                treelist[ifile].Branch('FatJetSDsubjetWmass' , FatJetSDsubjetWmass_ ,  'FatJetSDsubjetWmass/F' )
                treelist[ifile].Branch('FatJetSDsubjetWtau1'   , FatJetSDsubjetWtau1_   ,  'FatJetSDsubjetWtau1/F'   )
                treelist[ifile].Branch('FatJetSDsubjetWtau2'   , FatJetSDsubjetWtau2_   ,  'FatJetSDsubjetWtau2/F'   )
                treelist[ifile].Branch('FatJetSDsubjetWtau3'   , FatJetSDsubjetWtau3_   ,  'FatJetSDsubjetWtau3/F'   )
                treelist[ifile].Branch('FatJetSDsubjetWtau21'   , FatJetSDsubjetWtau21_   ,  'FatJetSDsubjetWtau21/F'   )

                if filee == './alphaMethod/ttjets_combinedttree_afterSelection_76x_v1p2_puppi.root' :
                    treelist[ifile].Branch('FatJetSDsubjet_isRealW'   , FatJetSDsubjet_isRealW_   ,  'FatJetSDsubjet_isRealW/F'   )
                    treelist[ifile].Branch('FatJetSDsubjet_isFakeW'   , FatJetSDsubjet_isFakeW_   ,  'FatJetSDsubjet_isFakeW/F'   )

                treelist[ifile].Branch('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt_   ,  'FatJetSDsubjetBpt/F'   )
                treelist[ifile].Branch('FatJetSDsubjetBmass' , FatJetSDsubjetBmass_ ,  'FatJetSDsubjetBmass/F' )
                treelist[ifile].Branch('FatJetSDsubjetBbdisc' , FatJetSDsubjetBbdisc_ ,  'FatJetSDsubjetBbdisc/F' )

                treelist[ifile].Branch('LeptonType'          , LeptonType_          ,  'LeptonType/I'          )
                treelist[ifile].Branch('LeptonPt'            , LeptonPt_            ,  'LeptonPt/F'            )

                treelist[ifile].Branch('LeptonPtRel'         , LeptonPtRel_         ,  'LeptonPtRel/F'         )
                treelist[ifile].Branch('LeptonDRMin'         , LeptonDRMin_         ,  'LeptonDRMin/F'         ) 

                treelist[ifile].Branch('SemiLepMETpt'        , SemiLepMETpt_        ,  'SemiLepMETpt/F'        )

                treelist[ifile].Branch('SemiLeptRunNum'         ,  SemiLeptRunNum_       ,  'SemiLeptRunNum/F'          )
                treelist[ifile].Branch('SemiLeptLumiBlock'      ,  SemiLeptLumiBlock_    ,  'SemiLeptLumiBlock/F'       )
                treelist[ifile].Branch('SemiLeptEventNum'       ,  SemiLeptEventNum_     ,  'SemiLeptEventNum/F'        )


    if options.combineTrees :
        fout= ROOT.TFile('Wmass_pt_binned_CombinedTrees_' + options.filestr + '.root', "RECREATE")
    else:
        fout= ROOT.TFile('Wmass_pt_binned_' + options.filestr + '.root', "RECREATE")


    if options.combineTrees :
        filesin = [ './alphaMethod/ttjets_combinedttree_76x_v1p2_puppi.root',
                './alphaMethod/data_combinedttree_76x_v1p2_puppi.root']
    else :
        filesin = [ 'b2gttbar_ttrees/ttjets_ttree_76x_v1p2_puppi.root',
                    'b2gttbar_ttrees/singleel_ttree_76x_v1p2_puppi.root', 
                    'b2gttbar_ttrees/singlemu_ttree_76x_v1p2_puppi.root' ]

    binlimit = 200.
    numbins = 200

    h_mWsubjet_ttjets = ROOT.TH1F("h_mWsubjet_ttjets", "; ; ", numbins, 0, binlimit)
    h_ptWsubjet_ttjets = ROOT.TH1F("h_ptWsubjet_ttjets", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)

    h_mWjet_ttjets = ROOT.TH1F("h_mWjet_ttjets", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_ptWjet_ttjets = ROOT.TH1F("h_ptWjet_ttjets", ";P_{T} SD jet0 (GeV);  ", 1300, 0, 1300)

    Wsj_tt = []

    for num in range(1,5):
        if options.verbose : print "h_mWsubjet_b"+str(num)+"_ttjets"
        Wsj_tt.append(ROOT.TH1F("h_mWsubjet_b"+str(num)+"_ttjets", "; ;  ", numbins, 0, binlimit)   )


    #h_mWsubjet_b1_ttjets  = ROOT.TH1F("h_mWsubjet_b1_ttjets", "; ;  ", numbins, 0, binlimit)
    #h_mWsubjet_b2_ttjets  = ROOT.TH1F("h_mWsubjet_b2_ttjets", "; ;  ", numbins, 0, binlimit)
    #h_mWsubjet_b3_ttjets  = ROOT.TH1F("h_mWsubjet_b3_ttjets", "; ;  ", numbins, 0, binlimit)
    #h_mWsubjet_b4_ttjets  = ROOT.TH1F("h_mWsubjet_b4_ttjets", "; ;  ", numbins, 0, binlimit)

    h_mWjet_b1_ttjets  = ROOT.TH1F("h_mWjet_b1_ttjets", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b2_ttjets  = ROOT.TH1F("h_mWjet_b2_ttjets", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b3_ttjets  = ROOT.TH1F("h_mWjet_b3_ttjets", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b4_ttjets  = ROOT.TH1F("h_mWjet_b4_ttjets", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)

    h_mWsubjet_EleData = ROOT.TH1F("h_mWsubjet_EleData", "; ;  ", numbins, 0, binlimit)
    h_ptWsubjet_EleData = ROOT.TH1F("h_ptWsubjet_EleData", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)

    h_mWsubjet_b1_EleData  = ROOT.TH1F("h_mWsubjet_b1_EleData", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b2_EleData  = ROOT.TH1F("h_mWsubjet_b2_EleData", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b3_EleData  = ROOT.TH1F("h_mWsubjet_b3_EleData", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b4_EleData  = ROOT.TH1F("h_mWsubjet_b4_EleData", "; ;  ", numbins, 0, binlimit)

    h_mWsubjet_MuData = ROOT.TH1F("h_mWsubjet_MuData", "; ;  ", numbins, 0, binlimit)
    h_ptWsubjet_MuData = ROOT.TH1F("h_ptWsubjet_MuData", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)

    h_mWsubjet_b1_MuData  = ROOT.TH1F("h_mWsubjet_b1_MuData", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b2_MuData  = ROOT.TH1F("h_mWsubjet_b2_MuData", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b3_MuData  = ROOT.TH1F("h_mWsubjet_b3_MuData", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b4_MuData  = ROOT.TH1F("h_mWsubjet_b4_MuData", "; ;  ", numbins, 0, binlimit)

    h_mWsubjet_Data = ROOT.TH1F("h_mWsubjet_Data", "; ;  ", numbins, 0, binlimit)
    h_ptWsubjet_Data = ROOT.TH1F("h_ptWsubjet_Data", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)

    h_mWsubjet_b1_Data  = ROOT.TH1F("h_mWsubjet_b1_Data", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b2_Data  = ROOT.TH1F("h_mWsubjet_b2_Data", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b3_Data  = ROOT.TH1F("h_mWsubjet_b3_Data", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b4_Data  = ROOT.TH1F("h_mWsubjet_b4_Data", "; ;  ", numbins, 0, binlimit)
    
    h_mWsubjet_ttjetsp = ROOT.TH1F("h_mWsubjet_ttjetsp", "; ;  ", numbins, 0, binlimit)
    h_ptWsubjet_ttjetsp = ROOT.TH1F("h_ptWsubjet_ttjetsp", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)

    h_mWsubjet_b1_ttjetsp  = ROOT.TH1F("h_mWsubjet_b1_ttjetsp", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b2_ttjetsp  = ROOT.TH1F("h_mWsubjet_b2_ttjetsp", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b3_ttjetsp  = ROOT.TH1F("h_mWsubjet_b3_ttjetsp", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b4_ttjetsp  = ROOT.TH1F("h_mWsubjet_b4_ttjetsp", "; ;  ", numbins, 0, binlimit)

    h_mWsubjet_Datap = ROOT.TH1F("h_mWsubjet_Datap", "; ;  ", numbins, 0, binlimit)
    h_ptWsubjet_Datap = ROOT.TH1F("h_ptWsubjet_Datap", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)

    h_mWsubjet_b1_Datap  = ROOT.TH1F("h_mWsubjet_b1_Datap", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b2_Datap  = ROOT.TH1F("h_mWsubjet_b2_Datap", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b3_Datap  = ROOT.TH1F("h_mWsubjet_b3_Datap", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b4_Datap  = ROOT.TH1F("h_mWsubjet_b4_Datap", "; ;  ", numbins, 0, binlimit)

    h_mWjet_Data = ROOT.TH1F("h_mWjet_Data", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_ptWjet_Data = ROOT.TH1F("h_ptWjet_Data", ";P_{T} SD jet0 (GeV);  ", 1300, 0, 1300)

    h_mWjet_b1_Data  = ROOT.TH1F("h_mWjet_b1_Data", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b2_Data  = ROOT.TH1F("h_mWjet_b2_Data", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b3_Data  = ROOT.TH1F("h_mWjet_b3_Data", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b4_Data  = ROOT.TH1F("h_mWjet_b4_Data", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    
    h_mWjet_ttjetsp = ROOT.TH1F("h_mWjet_ttjetsp", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_ptWjet_ttjetsp = ROOT.TH1F("h_ptWjet_ttjetsp", ";P_{T} SD jet0 (GeV);  ", 1300, 0, 1300)

    h_mWjet_b1_ttjetsp  = ROOT.TH1F("h_mWjet_b1_ttjetsp", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b2_ttjetsp  = ROOT.TH1F("h_mWjet_b2_ttjetsp", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b3_ttjetsp  = ROOT.TH1F("h_mWjet_b3_ttjetsp", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b4_ttjetsp  = ROOT.TH1F("h_mWjet_b4_ttjetsp", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)

    h_mWjet_Datap = ROOT.TH1F("h_mWjet_Datap", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_ptWjet_Datap = ROOT.TH1F("h_ptWjet_Datap", ";P_{T} SD jet0 (GeV);  ", 1300, 0, 1300)

    h_mWjet_b1_Datap  = ROOT.TH1F("h_mWjet_b1_Datap", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b2_Datap  = ROOT.TH1F("h_mWjet_b2_Datap", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b3_Datap  = ROOT.TH1F("h_mWjet_b3_Datap", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b4_Datap  = ROOT.TH1F("h_mWjet_b4_Datap", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)

    h_ptWsubjet_Data_Type1 = ROOT.TH1F("h_ptWsubjet_Data_Type1", ";Jet P_{T} (GeV); ", 80, 0, 1500) # SD subjet0 
    h_ptWsubjet_Data_Type2 = ROOT.TH1F("h_ptWsubjet_Data_Type2", ";Jet P_{T} (GeV); ", 80, 0, 1500)#of leading AK8 jet

    h_ptWsubjet_MC_Type1 = ROOT.TH1F("h_ptWsubjet_MC_Type1", ";Jet P_{T} (GeV); ", 80, 0, 1500) # SD subjet0 
    h_ptWsubjet_MC_Type2 = ROOT.TH1F("h_ptWsubjet_MC_Type2", ";Jet P_{T} (GeV); ", 80, 0, 1500)#of leading AK8 jet

    h_mWjet_EleData = ROOT.TH1F("h_mWjet_EleData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_ptWjet_EleData = ROOT.TH1F("h_ptWjet_EleData", ";P_{T} SD jet0 (GeV);  ", 1300, 0, 1300)

    h_mWjet_b1_EleData  = ROOT.TH1F("h_mWjet_b1_EleData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b2_EleData  = ROOT.TH1F("h_mWjet_b2_EleData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b3_EleData  = ROOT.TH1F("h_mWjet_b3_EleData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b4_EleData  = ROOT.TH1F("h_mWjet_b4_EleData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)

    h_mWjet_MuData = ROOT.TH1F("h_mWjet_MuData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_ptWjet_MuData = ROOT.TH1F("h_ptWjet_MuData", ";P_{T} SD jet0 (GeV);  ", 1300, 0, 1300)

    h_mWjet_b1_MuData  = ROOT.TH1F("h_mWjet_b1_MuData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b2_MuData  = ROOT.TH1F("h_mWjet_b2_MuData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b3_MuData  = ROOT.TH1F("h_mWjet_b3_MuData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    h_mWjet_b4_MuData  = ROOT.TH1F("h_mWjet_b4_MuData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    

    passkin = 0 
    passkin2 = 0
    pass2D  = 0
    passB   = 0
    passT   = 0 
    passLep = 0
    passOp  = 0
    passEle   = 0
    passMu   = 0
    pass3   = 0

    #passcounts = [] 

    for ifile, filee in enumerate(filesin) :
        fin = ROOT.TFile.Open( filee )
        if options.verbose : 
            print "Opened the File!  " + filee
            print "This is file number : " + str(ifile)
        t =  fin.Get("TreeSemiLept") 
        if options.combineTrees :

            FatJetRhoRatio      = array.array('f', [-1.])
            FatJetMass          = array.array('f', [-1.])
            FatJetPt          = array.array('f', [-1.])
            FatJetMassSoftDrop  = array.array('f', [-1.])
            FatJetPtSoftDrop  = array.array('f', [-1.])
            FatJetTau32         = array.array('f', [-1.])
            FatJetTau21         = array.array('f', [-1.]) 

            FatJetSDsubjetWpt   = array.array('f', [-1.])
            FatJetSDsubjetWmass = array.array('f', [-1.])
            FatJetSDsubjetWtau1 = array.array('f', [-1.])
            FatJetSDsubjetWtau2 = array.array('f', [-1.])
            FatJetSDsubjetWtau3 = array.array('f', [-1.])
            FatJetSDsubjetWtau21 = array.array('f', [-1.])

            FatJetSDsubjetBpt   = array.array('f', [-1.])
            FatJetSDsubjetBmass = array.array('f', [-1.])
            FatJetSDsubjetBbdisc = array.array('f', [-1.])

            SemiLepMETpt        = array.array('f', [-1.])

            LeptonType          = array.array('i', [-1])
            LeptonPt            = array.array('f', [-1.])

            LeptonPtRel         = array.array('f', [-1.])
            LeptonDRMin         = array.array('f', [-1.])

            SemiLepMETpt        = array.array('f', [-1.])

            SemiLeptRunNum        = array.array('f', [-1.])   
            SemiLeptLumiBlock     = array.array('f', [-1.])   
            SemiLeptEventNum      = array.array('f', [-1.])   

            t.SetBranchAddress('FatJetPt'            , FatJetPt            )
            t.SetBranchAddress('FatJetMass'          , FatJetMass          )
            t.SetBranchAddress('FatJetMassSoftDrop'  , FatJetMassSoftDrop  )
            t.SetBranchAddress('FatJetPtSoftDrop'  , FatJetPtSoftDrop  )
            t.SetBranchAddress('FatJetTau32'         , FatJetTau32         )
            t.SetBranchAddress('FatJetTau21'         , FatJetTau21         )
            t.SetBranchAddress('FatJetRhoRatio'      , FatJetRhoRatio      )

            t.SetBranchAddress('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt   )
            t.SetBranchAddress('FatJetSDsubjetWmass' , FatJetSDsubjetWmass )
            t.SetBranchAddress('FatJetSDsubjetWtau1' , FatJetSDsubjetWtau1 )
            t.SetBranchAddress('FatJetSDsubjetWtau2' , FatJetSDsubjetWtau2 )
            t.SetBranchAddress('FatJetSDsubjetWtau3' , FatJetSDsubjetWtau3 )
            t.SetBranchAddress('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt   )
            t.SetBranchAddress('FatJetSDsubjetBmass' , FatJetSDsubjetBmass )

            t.SetBranchAddress('SemiLepMETpt'        , SemiLepMETpt        )

            t.SetBranchAddress('LeptonType'          , LeptonType          )
            t.SetBranchAddress('LeptonPt'            , LeptonPt            )

            t.SetBranchAddress('LeptonPtRel'         , LeptonPtRel         )
            t.SetBranchAddress('LeptonDRMin'         , LeptonDRMin         )

            t.SetBranchStatus ('*', 0)
            t.SetBranchStatus ('FatJetPt', 1)
            t.SetBranchStatus ('FatJetMass', 1)
            t.SetBranchStatus ('FatJetMassSoftDrop', 1)
            t.SetBranchStatus ('FatJetPtSoftDrop', 1)
            t.SetBranchStatus ('FatJetTau32', 1)
            t.SetBranchStatus ('FatJetTau21', 1)
            t.SetBranchStatus ('FatJetRhoRatio', 1)

            t.SetBranchStatus('FatJetSDsubjetWpt',1)
            t.SetBranchStatus('FatJetSDsubjetWtau1',1)
            t.SetBranchStatus('FatJetSDsubjetWtau2',1)
            t.SetBranchStatus('FatJetSDsubjetWtau3',1)
            t.SetBranchStatus('FatJetSDsubjetWmass',1)
            t.SetBranchStatus ('SemiLepMETpt' , 1 )

            t.SetBranchStatus ('LeptonType'          , 1 )
            t.SetBranchStatus ('LeptonPt'            , 1)

            t.SetBranchStatus ('LeptonPtRel'         , 1)
            t.SetBranchStatus ('LeptonDRMin'         , 1)
        else:     
            if (ifile  > 0 ): 
                SemiLeptTrig        = array.array('i', [0]  )
            SemiLeptWeight      = array.array('f', [0.] )
            BoosttypE           = array.array('i', [0] )
            FatJetCorr          = array.array('f', [0.] )
            FatJetCorrUp        = array.array('f', [0.] )
            FatJetCorrDn        = array.array('f', [0.] )
            FatJetMassCorr      = array.array('f', [0.] )
            FatJetMassCorrUp    = array.array('f', [0.] )
            FatJetMassCorrDn    = array.array('f', [0.] )
            JetPtSmearFactor    = array.array('f', [0.] )
            JetPtSmearFactorUp  = array.array('f', [0.] )
            JetPtSmearFactorDn  = array.array('f', [0.] )
            JetEtaScaleFactor   = array.array('f', [0.] )
            JetPhiScaleFactor   = array.array('f', [0.] )
            JetMatchedGenJetPt  = array.array('f', [0.] )
            FatJetPtRaw         = array.array('f', [0.] )
            FatJetEtaRaw        = array.array('f', [0.] )  
            FatJetPhiRaw        = array.array('f', [0.] )
            FatJetRapRaw        = array.array('f', [0.] )
            FatJetMassRaw       = array.array('f', [0.] )
            FatJetP             = array.array('f', [0.] )
            FatJetPt            = array.array('f', [-1.])
            FatJetEta           = array.array('f', [-1.])
            FatJetPhi           = array.array('f', [-1.])
            FatJetRap           = array.array('f', [-1.])
            FatJetEnergy        = array.array('f', [-1.])
            FatJetBDisc         = array.array('f', [-1.])
            FatJetRhoRatio      = array.array('f', [-1.])
            FatJetMass          = array.array('f', [-1.])
            FatJetMassSoftDrop  = array.array('f', [-1.])
            FatJetMassSDsumSubjetCorr        = array.array('f', [-1.])
            FatJetMassSDsumSubjetRaw         = array.array('f', [-1.])
            FatJetMassSDsumSubjetCorrUp      = array.array('f', [-1.])
            FatJetMassSDsumSubjetCorrDn      = array.array('f', [-1.])
            FatJetMassSDsumSubjetCorrSmear   = array.array('f', [-1.])
            FatJetMassSDsumSubjetCorrSmearUp = array.array('f', [-1.])
            FatJetMassSDsumSubjetCorrSmearDn = array.array('f', [-1.])
            FatJetMassPruned    = array.array('f', [-1.])
            FatJetMassFiltered  = array.array('f', [-1.])       
            FatJetMassTrimmed   = array.array('f', [-1.])
            FatJetTau1          = array.array('f', [-1.])
            FatJetTau2          = array.array('f', [-1.])
            FatJetTau3          = array.array('f', [-1.])
            FatJetTau32         = array.array('f', [-1.])
            FatJetTau21         = array.array('f', [-1.]) 
            FatJetSDnsubjets    = array.array('f', [-1.])
            FatJetSDbdiscW      = array.array('f', [-1.])
            FatJetSDbdiscB      = array.array('f', [-1.])
            FatJetSDmaxbdisc    = array.array('f', [-1.])
            FatJetSDsubjetWpt   = array.array('f', [-1.])
            FatJetSDsubjetWmass = array.array('f', [-1.])
            FatJetSDsubjetWp4   = array.array('f', [-1.])
            FatJetSDsubjetWtau1   = array.array('f', [-1.])
            FatJetSDsubjetWtau2   = array.array('f', [-1.])
            FatJetSDsubjetWtau3   = array.array('f', [-1.])
            FatJetSDsubjetBpt   = array.array('f', [-1.])
            FatJetSDsubjetBmass = array.array('f', [-1.])
            FatJetSDsubjetBp4   = array.array('f', [-1.])
            FatJetSDsubjetBtau1   = array.array('f', [-1.])
            FatJetSDsubjetBtau2   = array.array('f', [-1.])
            FatJetSDsubjetBtau3   = array.array('f', [-1.])
            FatJetSDsubjet0pt   = array.array('f', [-1.])
            FatJetSDsubjet0mass = array.array('f', [-1.])
            FatJetSDsubjet0area = array.array('f', [-1.])
            FatJetSDsubjet0flav = array.array('f', [-1.])
            FatJetSDsubjet0tau1 = array.array('f', [-1.])
            FatJetSDsubjet0tau2 = array.array('f', [-1.])
            FatJetSDsubjet0tau3 = array.array('f', [-1.])
            FatJetSDsubjet1pt   = array.array('f', [-1.])
            FatJetSDsubjet1mass = array.array('f', [-1.])
            FatJetSDsubjet1area = array.array('f', [-1.])
            FatJetSDsubjet1flav = array.array('f', [-1.])
            FatJetSDsubjet1tau1 = array.array('f', [-1.])
            FatJetSDsubjet1tau2 = array.array('f', [-1.])
            FatJetSDsubjet1tau3 = array.array('f', [-1.])
            FatJetCMSmaxbdisc   = array.array('f', [-1.])
            FatJetCMSnsubjets   = array.array('f', [-1.])
            FatJetCMSminMass    = array.array('f', [-1.])
            FatJetCMSm01        = array.array('f', [-1.])
            FatJetCMSm02        = array.array('f', [-1.])
            FatJetCMSm12        = array.array('f', [-1.])
            FatJetNHF           = array.array('f', [-1.])
            FatJetCHF           = array.array('f', [-1.])
            FatJetNEF           = array.array('f', [-1.])
            FatJetCEF           = array.array('f', [-1.])
            FatJetNC            = array.array('f', [-1.])
            FatJetNCH           = array.array('f', [-1.])
            BJetbDisc           = array.array('f', [-1.])
            BJetPt              = array.array('f', [-1.])
            BJetEta             = array.array('f', [-1.])
            BJetPhi             = array.array('f', [-1.])
            BJetMass            = array.array('f', [-1.])
            BJetbDisc2           = array.array('f', [-1.])
            BJetPt2              = array.array('f', [-1.])
            BJetEta2             = array.array('f', [-1.])
            BJetPhi2             = array.array('f', [-1.])
            BJetMass2            = array.array('f', [-1.])
            Type2PairMass       = array.array('f', [-1.])
            Type2PairPt         = array.array('f', [-1.])
            LeptonType          = array.array('i', [-1])
            LeptonPt            = array.array('f', [-1.])
            LeptonEta           = array.array('f', [-1.])
            LeptonPhi           = array.array('f', [-1.])
            LeptonPx            = array.array('f', [-1.])
            LeptonPy            = array.array('f', [-1.])
            LeptonPz            = array.array('f', [-1.])
            LeptonEnergy        = array.array('f', [-1.])
            LeptonIso           = array.array('f', [-1.])
            LeptonPtRel         = array.array('f', [-1.])
            LeptonDRMin         = array.array('f', [-1.])
            SemiLepMETpx        = array.array('f', [-1.])
            SemiLepMETpy        = array.array('f', [-1.])
            SemiLepMETpt        = array.array('f', [-1.])
            SemiLepMETphi       = array.array('f', [-1.])
            SemiLepNvtx         = array.array('f', [-1.])
            SemiLepEventWeight  = array.array('f', [-1.])
            SemilLepTTmass      = array.array('f', [-1.])  
            DeltaPhiLepFat      = array.array('f', [-1.]) 
            AK4bDisc            = array.array('f', [-1.])
            NearestAK4JetPt     = array.array('f', [-1.])
            NearestAK4JetEta    = array.array('f', [-1.])
            NearestAK4JetPhi    = array.array('f', [-1.])
            NearestAK4JetMass   = array.array('f', [-1.])
            NearestAK4JetPt2     = array.array('f', [-1.])
            NearestAK4JetEta2    = array.array('f', [-1.])
            NearestAK4JetPhi2    = array.array('f', [-1.])
            NearestAK4JetMass2   = array.array('f', [-1.])
            SemiLeptRunNum      = array.array('f', [-1.])  
            SemiLeptLumiBlock   = array.array('f', [-1.])  
            SemiLeptEventNum    = array.array('f', [-1.])
            SemiLeptEventNum2    = array.array('f', [-1.])  
            PU_CorrDn           = array.array('f', [-1.])
            PU_CorrUp           = array.array('f', [-1.])

            if (ifile  > 0 ):  
                t.SetBranchAddress('SemiLeptTrig'        , SemiLeptTrig        )
            t.SetBranchAddress('SemiLeptWeight'      , SemiLeptWeight      )
            t.SetBranchAddress('FatJetPt'            , FatJetPt            )
            t.SetBranchAddress('FatJetEta'           , FatJetEta           )
            t.SetBranchAddress('FatJetPhi'           , FatJetPhi           )
            t.SetBranchAddress('FatJetRap'           , FatJetRap           )
            t.SetBranchAddress('FatJetEnergy'        , FatJetEnergy        )
            t.SetBranchAddress('FatJetBDisc'         , FatJetBDisc         )
            t.SetBranchAddress('FatJetMass'          , FatJetMass          )
            t.SetBranchAddress('FatJetMassSoftDrop'  , FatJetMassSoftDrop  )
            t.SetBranchAddress('FatJetTau32'         , FatJetTau32         )
            t.SetBranchAddress('FatJetTau21'         , FatJetTau21         )
            t.SetBranchAddress('FatJetRhoRatio'      , FatJetRhoRatio      )
            t.SetBranchAddress('FatJetSDbdiscW'      , FatJetSDbdiscW      )
            t.SetBranchAddress('FatJetSDbdiscB'      , FatJetSDbdiscB      )
            t.SetBranchAddress('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt   )
            t.SetBranchAddress('FatJetSDsubjetWmass' , FatJetSDsubjetWmass )
            t.SetBranchAddress('FatJetSDsubjetWtau1' , FatJetSDsubjetWtau1 )
            t.SetBranchAddress('FatJetSDsubjetWtau2' , FatJetSDsubjetWtau2 )
            t.SetBranchAddress('FatJetSDsubjetWtau3' , FatJetSDsubjetWtau3 )
            t.SetBranchAddress('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt   )
            t.SetBranchAddress('FatJetSDsubjetBmass' , FatJetSDsubjetBmass )
            t.SetBranchAddress('FatJetSDsubjetBtau1' , FatJetSDsubjetBtau1 )
            t.SetBranchAddress('FatJetSDsubjetBtau2' , FatJetSDsubjetBtau2 )
            t.SetBranchAddress('FatJetSDsubjetBtau3' , FatJetSDsubjetBtau3 )
            t.SetBranchAddress('FatJetSDsubjet0tau1' , FatJetSDsubjetWtau1 )
            t.SetBranchAddress('FatJetSDsubjet0tau2' , FatJetSDsubjetWtau2 )
            t.SetBranchAddress('FatJetSDsubjet0tau3' , FatJetSDsubjetWtau3 )
            t.SetBranchAddress('FatJetSDsubjet1tau1' , FatJetSDsubjetWtau1 )
            t.SetBranchAddress('FatJetSDsubjet1tau2' , FatJetSDsubjetWtau2 )
            t.SetBranchAddress('FatJetSDsubjet1tau3' , FatJetSDsubjetWtau3 )
            t.SetBranchAddress('BJetbDisc' , BJetbDisc )
            t.SetBranchAddress('BJetPt' , BJetPt )
            t.SetBranchAddress('BJetEta' , BJetEta )
            t.SetBranchAddress('BJetPhi' , BJetPhi )
            t.SetBranchAddress('BJetMass' , BJetMass )
            t.SetBranchAddress('LeptonType'          , LeptonType          )
            t.SetBranchAddress('LeptonPt'            , LeptonPt            )
            t.SetBranchAddress('LeptonEta'           , LeptonEta           )
            t.SetBranchAddress('LeptonPhi'           , LeptonPhi           )
            t.SetBranchAddress('LeptonEnergy'        , LeptonEnergy        )
            t.SetBranchAddress('LeptonIso'           , LeptonIso           )
            t.SetBranchAddress('LeptonPtRel'         , LeptonPtRel         )
            t.SetBranchAddress('LeptonDRMin'         , LeptonDRMin         )
            t.SetBranchAddress('SemiLepMETpt'        , SemiLepMETpt        )
            t.SetBranchAddress('SemiLepMETphi'       , SemiLepMETphi       )
            t.SetBranchAddress('SemiLepNvtx'         , SemiLepNvtx         )
            t.SetBranchAddress('DeltaPhiLepFat'      , DeltaPhiLepFat      )
            t.SetBranchAddress('NearestAK4JetPt'     , NearestAK4JetPt     )
            t.SetBranchAddress('NearestAK4JetEta'    , NearestAK4JetEta    )
            t.SetBranchAddress('NearestAK4JetPhi'    , NearestAK4JetPhi    )
            t.SetBranchAddress('NearestAK4JetMass'   , NearestAK4JetMass   )
            t.SetBranchAddress('SemiLepEventWeight'     ,  SemiLepEventWeight   )
            t.SetBranchAddress('SemiLeptRunNum'         ,  SemiLeptRunNum       )
            t.SetBranchAddress('SemiLeptLumiBlock'      ,  SemiLeptLumiBlock    )
            t.SetBranchAddress('SemiLeptEventNum'       ,  SemiLeptEventNum     )
            t.SetBranchAddress('PU_CorrDn'       ,  PU_CorrDn     )
            t.SetBranchAddress('PU_CorrUp'       ,  PU_CorrUp     )
     
            t.SetBranchStatus ('*', 0)
            t.SetBranchStatus ('FatJetPt', 1)
            t.SetBranchStatus ('FatJetEta', 1)
            t.SetBranchStatus ('FatJetPhi', 1)
            t.SetBranchStatus ('FatJetMass', 1)
            t.SetBranchStatus ('FatJetMassSoftDrop', 1)
            t.SetBranchStatus ('FatJetTau32', 1)
            t.SetBranchStatus ('FatJetTau21', 1)
            t.SetBranchStatus ('FatJetRhoRatio', 1)
            t.SetBranchStatus('BJetPt' , 1)
            t.SetBranchStatus('BJetEta' , 1)
            t.SetBranchStatus('BJetPhi' , 1 )
            t.SetBranchStatus('BJetMass' , 1)
            t.SetBranchStatus('FatJetSDsubjetWpt',1)
            t.SetBranchStatus('FatJetSDsubjetWtau1',1)
            t.SetBranchStatus('FatJetSDsubjetWtau2',1)
            t.SetBranchStatus('FatJetSDsubjetWtau3',1)
            t.SetBranchStatus('FatJetSDsubjetBtau1',1)
            t.SetBranchStatus('FatJetSDsubjetBtau2',1)
            t.SetBranchStatus('FatJetSDsubjetBtau3',1)
            t.SetBranchStatus('FatJetSDsubjet0tau1',1)
            t.SetBranchStatus('FatJetSDsubjet0tau2',1)
            t.SetBranchStatus('FatJetSDsubjet0tau3',1)
            t.SetBranchStatus('FatJetSDsubjet1tau1',1)
            t.SetBranchStatus('FatJetSDsubjet1tau2',1)
            t.SetBranchStatus('FatJetSDsubjet1tau3',1)
            t.SetBranchStatus('FatJetSDsubjetBpt',1)
            t.SetBranchStatus('FatJetSDsubjetWmass',1)
            t.SetBranchStatus ('SemiLeptTrig', 1)
            t.SetBranchStatus ('NearestAK4JetPt'   ,1 )
            t.SetBranchStatus ('NearestAK4JetEta'  ,1 )
            t.SetBranchStatus ('NearestAK4JetPhi'  ,1 )
            t.SetBranchStatus ('NearestAK4JetMass' ,1 )
            t.SetBranchStatus ('SemiLepMETpt' , 1 )
            t.SetBranchStatus ('SemiLepMETphi' , 1 )
            t.SetBranchStatus ('LeptonType'          , 1 )
            t.SetBranchStatus ('LeptonPt'            , 1)
            t.SetBranchStatus ('LeptonEta'           , 1)
            t.SetBranchStatus ('LeptonPhi'           , 1)
            t.SetBranchStatus ('LeptonEnergy'        , 1)
            t.SetBranchStatus ('LeptonIso'           , 1)
            t.SetBranchStatus ('LeptonPtRel'         , 1)
            t.SetBranchStatus ('LeptonDRMin'         , 1)
            t.SetBranchStatus ('SemiLepEventWeight'  , 1) 
            t.SetBranchStatus ('SemiLeptRunNum'      , 1)
            t.SetBranchStatus ('SemiLeptLumiBlock'   , 1)
            t.SetBranchStatus ('SemiLeptEventNum'    , 1)
            t.SetBranchStatus ('PU_CorrDn'           , 1)
            t.SetBranchStatus ('PU_CorrUp'           , 1)


        entries = t.GetEntriesFast()
        if options.maxEvents < 0. :
            eventsToRun = entries
        else :
            eventsToRun = options.maxEvents
        #eventsToRun = 10000
#        print entries


        for jentry in xrange( eventsToRun ):
            if jentry % 100000 == 0 :
                print 'processing ' + str(jentry)
            # get the next tree in the chain and verify
            ientry = t.GetEntry( jentry )
            if ientry < 0:
                break

            
            #bJetCandP4puppi0 = ROOT.TLorentzVector()
            #bJetCandP4puppi0.SetPtEtaPhiM( BJetPt[0], BJetEta[0], BJetPhi[0], BJetMass[0])
            #bJetCandP4puppiEventnum = SemiLeptEventNum[0]
            #bJetCandP4puppi0Bdisc = -1.0
            #print "b jet PUPPI event number : " + str(bJetCandP4puppiEventnum)

            '''
            bJetCandP4chs0 = ROOT.TLorentzVector()
            bJetCandP4chs0.SetPtEtaPhiM( BJetPt2[0], BJetEta2[0], BJetPhi2[0], BJetMass2[0])
            bJetCandP4chsBdisc = [ BJetbDisc2[0] ]
            bJetCandP4chs0Eventnum = SemiLeptEventNum2[0]

            if len(BJetPt2) == 2:
                bJetCandP4chs1 = ROOT.TLorentzVector()
                bJetCandP4chs1.SetPtEtaPhiM( BJetPt2[1], BJetEta2[1], BJetPhi2[1], BJetMass2[1])
                bJetCandP4chsBdisc = [  BJetbDisc2[0], BJetbDisc2[1] ]
                bJetCandP4chs1Eventnum = SemiLeptEventNum2[1]

            if len(BJetPt2) > 2:
                bJetCandP4chs2 = ROOT.TLorentzVector()
                bJetCandP4chs2.SetPtEtaPhiM( BJetPt2[2], BJetEta2[2], BJetPhi2[2], BJetMass2[2])
                bJetCandP4chsBdisc = [  BJetbDisc2[0], BJetbDisc2[1], BJetbDisc2[2]  ]
                bJetCandP4chs2Eventnum = SemiLeptEventNum2[2]

            #print "b jet CHS event number : " + str(bJetCandP4chs0Eventnum)

            
            DrMin = 9999.0
            dr = [bJetCandP4puppi0.DeltaR(bJetCandP4chs0), bJetCandP4puppi0.DeltaR(bJetCandP4chs1), bJetCandP4puppi0.DeltaR(bJetCandP4chs2) ]
            #fill the dr array 
            for i, s in dr :
                if s < DrMin:
                    DrMin = s
                    bJetCandP4puppi0Bdisc = 
                    bdisc = AK4bDisc[i]
            '''
            #bdisc = BJetbDisc2[0]

            #nuCandP4 = ROOT.TLorentzVector( )
            #nuCandP4.SetPtEtaPhiM( SemiLepMETpt[0], 0, SemiLepMETphi[0], SemiLepMETpt[0] )
            #theLepton = ROOT.TLorentzVector()
            #theLepton.SetPtEtaPhiE( LeptonPt[0], LeptonEta[0], LeptonPhi[0], LeptonEnergy[0] ) # Assume massless
            
            # FatJetSDpt = m / (R*sqrt(rhoRatio)) 
            # using SD pts for both types

            #weightS = SemiLeptWeight[0]

            LepPt = LeptonPt[0]    
            lepton_Type =  LeptonType[0]
   
            fatpt = FatJetPt[0]
            fatmass = FatJetMass[0]

            FatJetSD_m = FatJetMassSoftDrop[0]
            if options.verbose : print "Fat Jet mass SD is  : " + str(FatJetSD_m)
            Rhorat = FatJetRhoRatio[0]
            if options.verbose : 
                print "Fat Jet Rho Ratio : " + str(Rhorat)
                print "..............................."
            if (Rhorat > 0.001):
                sqrtRhorat = math.sqrt(Rhorat)
                FatJetSD_pt = FatJetSD_m / (0.8 * sqrtRhorat  )
            else:
                FatJetSD_pt = 0.

            #tau3 = FatJetTau3[0]
            #tau2 = FatJetTau2[0]
            #tau1 = FatJetTau1[0]
            tau32 = FatJetTau32[0]
            #tau21 = FatJetTau21[0]
           #mass_sd = FatJetMassSoftDrop[0]


            W_m = FatJetSDsubjetWmass[0]
            W_pt = FatJetSDsubjetWpt[0]
            W_tau1 = FatJetSDsubjetWtau1[0]
            W_tau2 = FatJetSDsubjetWtau2[0]
            W_tau3 = FatJetSDsubjetWtau3[0]
            if  W_tau1 > 0.001 :
                W_tau21 = W_tau2 / W_tau1
            else :
                W_tau21 = 1.0
            B_pt = FatJetSDsubjetBpt[0]
            B_m = FatJetSDsubjetBmass[0]
            MET_pt = SemiLepMETpt[0]
            W_pt2 = FatJetPt[0]

            lepton_ptRel = LeptonPtRel[0]
            lepton_DRmin = LeptonDRMin[0] 

            runNum = SemiLeptRunNum[0]
            lumiBlock = SemiLeptLumiBlock[0]
            eventNum = SemiLeptEventNum[0]



            ##  ____  __.__                              __  .__         __________                     
            ## |    |/ _|__| ____   ____   _____ _____ _/  |_|__| ____   \______   \ ____   ____  ____  
            ## |      < |  |/    \_/ __ \ /     \\__  \\   __\  |/ ___\   |       _// __ \_/ ___\/  _ \ 
            ## |    |  \|  |   |  \  ___/|  Y Y  \/ __ \|  | |  \  \___   |    |   \  ___/\  \__(  <_> )
            ## |____|__ \__|___|  /\___  >__|_|  (____  /__| |__|\___  >  |____|_  /\___  >\___  >____/ 
            ##         \/       \/     \/      \/     \/             \/          \/     \/     \/       

            # Now we do our kinematic calculation based on the semi-leptonic Z' selection detailed in  B2G-15-002 


            passKin = FatJetSD_pt > options.Ak8PtCut  and W_pt > 200.
            if (options.verbose and FatJetSD_pt > 300.): print "The Fat jet SD_pt is" + str(FatJetSD_pt)

            passKin2 =  FatJetSD_pt > 200. #and W_m < 1.
            
            passWPre =   W_m > 50. 
            passWPre2 = FatJetSD_m > 50. 
            passTopTag = tau32 < options.tau32Cut and FatJetSD_m > 110. and FatJetSD_m < 250.
            pass2DCut = LeptonPtRel[0] > 20. or LeptonDRMin[0] > 0.4 # B2G-15-002 uses  LeptonPtRel[0] > 20.or LeptonDRMin[0] > 0.4 (was 55.0 here)
            #passBtag = bdisc > 0.7

            passWPostM = (55. < W_m < 115.) #(50. < W_m < 150.) #(55. < W_m < 105.)#50 to 130 before
            passWPosttag = W_tau21 < options.tau21Cut  #W_tau21 < 0.6 
            passWPost2M = (50.0 < W_m < 150.)  #(55. < FatJetSD_m < 105.)
            #passWPost2tau = tau21 < options.tau21Cut
            passEleMETcut =  LeptonType[0] == 1 and MET_pt > 120. and LepPt > 55. #110.
            # B2G-15-002  uses ( theLepton.Perp() + MET_pt ) > 150. (was previously 250 here) 
            passMuHtLepcut = LeptonType[0] == 2 and ( LepPt + MET_pt ) > 150. and LepPt > 55.
            passLepcut = passEleMETcut or passMuHtLepcut 

            if pass2DCut : 
                pass2D += 1

            #if passBtag :
            #    passB += 1
           
            if passTopTag :
                passT += 1

            if passLepcut :
                passLep += 1
            if passEleMETcut :
                passEle +=1
            if passMuHtLepcut :
                passMu +=1

            #if (ifile > 0 and passKin) :
                #h_ptWsubjet_Data_Type1.Fill(W_pt, 1)
                #print "Pt of W tagged subjet of the AK8 jet for events 5 and 500 : " + str( W_pt)
            #if (ifile > 0 and passKin2 ) :
                #h_ptWsubjet_Data_Type2.Fill( FatJetSD_pt , 1)   
                #print "Pt of W tagged AK8 jet for events 5 and 500 : " + str( W_pt)      
            if  (passTopTag and pass2DCut and passLepcut) : # and passBtag :  
                if passKin :
                    #if ( ifile == 1 or ifile == 2 ):
                    #    h_ptWsubjet_Data_Type1.Fill(W_pt, 1)
                    passkin += 1

                    # Fill the Combined Trees after selection
                    if options.combineTrees :
                        #SemiLeptWeight_      [0] = weightS

                        FatJetRhoRatio_      [0] = Rhorat
                        FatJetMass_          [0] = fatmass
                        FatJetPt_            [0] = fatpt
                        FatJetMassSoftDrop_  [0] = FatJetSD_m
                        FatJetPtSoftDrop_    [0] = FatJetSD_pt
                        #FatJetTau1_          [0] = tau1
                        #FatJetTau2_          [0] = tau2
                        #FatJetTau3_          [0] = tau3
                        FatJetTau32_         [0] = tau32
                        #FatJetTau21_         [0] = tau21

                        FatJetSDsubjetWpt_   [0] = W_pt
                        FatJetSDsubjetWmass_ [0] = W_m
                        FatJetSDsubjetWtau1_ [0] = W_tau1
                        FatJetSDsubjetWtau2_ [0] = W_tau2
                        FatJetSDsubjetWtau3_ [0] = W_tau3
                        FatJetSDsubjetWtau21_ [0] = W_tau21

                        if filee == './alphaMethod/ttbar_combinedttree_76x_v1p2_puppi.root' :
                            FatJetSDsubjet_isRealW_[0] = 0.0  # correct this once gen matching is implemented ???
                            FatJetSDsubjet_isFake_W[0] = 0.0  # correct this once gen matching is implemented ???

                        FatJetSDsubjetBpt_   [0] = B_pt 
                        FatJetSDsubjetBmass_ [0] = B_m
                        #FatJetSDsubjetBbdisc_[0] = B_bdisc

                        LeptonType_          [0] = lepton_Type
                        LeptonPt_            [0] = LepPt

                        LeptonPtRel_         [0] = lepton_ptRel
                        LeptonDRMin_         [0] = lepton_DRmin

                        SemiLepMETpt_        [0] = MET_pt

                        SemiLeptRunNum_      [0] = runNum
                        SemiLeptLumiBlock_   [0] = lumiBlock 
                        SemiLeptEventNum_    [0] = eventNum

                        foutlist[ifile].cd()
                        treelist[ifile].Fill()
                        

                    fout.cd() 
                    if (ifile == 0 ): #ttjets
                        h_mWsubjet_ttjetsp.Fill(W_m , 1 )
                        h_ptWsubjet_ttjetsp.Fill(W_pt , 1 )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #if passWPre and ( float(options.mc_mean0 -options.mc_sigma0 )  < W_m < float(options.mc_mean0 +options.mc_sigma0 ) ): nMCpre[0] += 1
                            h_mWsubjet_b1_ttjetsp.Fill(W_m , 1 )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) :
                            #if ( float(options.mc_mean1 -options.mc_sigma1)  < W_m < float(options.mc_mean1 +options.mc_sigma1)) :
                            #    print "This jet passed the 300-400 pt requirement for PRE MC and has a mass of " + str(W_m)
                            #    print "where the acceptable range is " + str(float(options.mc_mean1 -options.mc_sigma1)) + " to " + str(float(options.mc_mean1 +options.mc_sigma1))
                            #if passWPre and ( float(options.mc_mean1 -options.mc_sigma1)  < W_m < float(options.mc_mean1 +options.mc_sigma1)) : nMCpre[1] +=1 
                            h_mWsubjet_b2_ttjetsp.Fill(W_m , 1 )                           

                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #if passWPre and ( float(options.mc_mean2 -options.mc_sigma2 )  < W_m < float(options.mc_mean2 +options.mc_sigma2 )) : nMCpre[2] +=1
                            h_mWsubjet_b3_ttjetsp.Fill(W_m , 1 )

                        if ( W_pt > 500.0 ) : 
                            #if passWPre  and ( float(options.mc_mean3 -options.mc_sigma3 )  < W_m < float(options.mc_mean3 +options.mc_sigma3 )): nMCpre[3]  +=1
                            h_mWsubjet_b4_ttjetsp.Fill(W_m , 1 )
                    if (ifile != 0 ):
                        h_mWsubjet_Datap.Fill(W_m , 1 )
                        h_ptWsubjet_Datap.Fill(W_pt , 1 )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #print "This jet passed the 200-300 pt requirement for PRE DATA and has a mass of " + str(W_m)
                            #if passWPre  and ( float(options.data_mean0 - options.data_sigma0 ) < W_m < float(options.data_mean0 + options.data_sigma0 )) : nDatapre[0]  +=1
                            h_mWsubjet_b1_Datap.Fill(W_m , 1 )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) : 
                            #if passWPre and (float(options.data_mean1 - options.data_sigma1 ) < W_m < float(options.data_mean1 + options.data_sigma1 )) : nDatapre[1]  +=1
                            h_mWsubjet_b2_Datap.Fill(W_m , 1 )

                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #if passWPre  and (float(options.data_mean2 - options.data_sigma2 ) < W_m < float(options.data_mean2 + options.data_sigma2 )): nDatapre[2]  +=1
                            h_mWsubjet_b3_Datap.Fill(W_m , 1 )

                        if ( W_pt > 500.0 ) : 
                            #if passWPre and (float(options.data_mean3 - options.data_sigma3 ) < W_m < float(options.data_mean3 + options.data_sigma3 )) : nDatapre[3] +=1
                            h_mWsubjet_b4_Datap.Fill(W_m , 1 )
                    if passWPosttag :
                        passOp += 1 
                        if (ifile == 0 ): #ttjets.root
                            if passWPostM  : 
                                h_ptWsubjet_MC_Type1.Fill(W_pt, 1)
                            h_mWsubjet_ttjets.Fill(W_m , 1 )
                            h_ptWsubjet_ttjets.Fill(W_pt , 1 )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) :
                                #if passWPostM  and ( float(options.mc_mean0 -options.mc_sigma0 )  < W_m < float(options.mc_mean0 +options.mc_sigma0 )) : nMCpost[0] +=1
                                Wsj_tt[0].Fill(W_m , 1 )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) : 
                                #print "This jet passed the 300-400 pt requirement for POST MC and has a mass of " + str(W_m)
                                #if passWPostM  and (float(options.mc_mean1 -options.mc_sigma1 )  < W_m < float(options.mc_mean1 +options.mc_sigma1 )): nMCpost[1]  +=1
                                Wsj_tt[1].Fill(W_m , 1 )

                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #if passWPostM  and (float(options.mc_mean2 -options.mc_sigma2 )  < W_m < float(options.mc_mean2 +options.mc_sigma2 )): nMCpost[2]  +=1
                                Wsj_tt[2].Fill(W_m , 1 )

                            if ( W_pt > 500.0 ) : 
                                #if passWPostM  and (float(options.mc_mean3 -options.mc_sigma3 )  < W_m < float(options.mc_mean3 +options.mc_sigma3 )): nMCpost[3]  +=1
                                Wsj_tt[3].Fill(W_m , 1 )
                        if (ifile == 1  ):
                            h_mWsubjet_EleData.Fill(W_m , 1 )
                            h_ptWsubjet_EleData.Fill(W_pt , 1 )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) : 
                                h_mWsubjet_b1_EleData.Fill(W_m , 1 )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) : 
                                h_mWsubjet_b2_EleData.Fill(W_m , 1 )

                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                h_mWsubjet_b3_EleData.Fill(W_m , 1 )

                            if ( W_pt > 500.0 ) : 
                                h_mWsubjet_b4_EleData.Fill(W_m , 1 )

                        if (ifile == 2 ):
                            h_mWsubjet_MuData.Fill(W_m , 1 )
                            h_ptWsubjet_MuData.Fill(W_pt , 1 )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) : 
                                h_mWsubjet_b1_MuData.Fill(W_m , 1 )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) : 
                                h_mWsubjet_b2_MuData.Fill(W_m , 1 )

                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                h_mWsubjet_b3_MuData.Fill(W_m , 1 )

                            if ( W_pt > 500.0 ) : 
                                h_mWsubjet_b4_MuData.Fill(W_m , 1 )
                        if (ifile != 0 ):
                            if passWPostM : 
                                h_ptWsubjet_Data_Type1.Fill(W_pt, 1)
                            h_mWsubjet_Data.Fill(W_m , 1 )
                            h_ptWsubjet_Data.Fill(W_pt , 1 )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) : 
                                #print "This jet passed the 200-300 pt requirement for POST DATA and has a mass of " + str(W_m)
                                #if passWPostM and (float(options.data_mean0 - options.data_sigma0 ) < W_m < float(options.data_mean0 + options.data_sigma0 )): nDatapost[0]  +=1
                                h_mWsubjet_b1_Data.Fill(W_m , 1 )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) : 
                                #if passWPostM and (float(options.data_mean1 - options.data_sigma1 ) < W_m < float(options.data_mean1 + options.data_sigma1 )): nDatapost[1] +=1
                                h_mWsubjet_b2_Data.Fill(W_m , 1 )

                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #if passWPostM and (float(options.data_mean2 - options.data_sigma2 ) < W_m < float(options.data_mean2 + options.data_sigma2 )): nDatapost[2] +=1
                                h_mWsubjet_b3_Data.Fill(W_m , 1 )

                            if ( W_pt > 500.0 ) : 
                                #if passWPostM and (float(options.data_mean3 - options.data_sigma3 ) < W_m < float(options.data_mean3 + options.data_sigma3 )): nDatapost[3] +=1
                                h_mWsubjet_b4_Data.Fill(W_m , 1 )


    print "Number of events passing basic cuts:"
    print "total passing pre-selection : " + str(passkin)

    print "total passing final selection : " + str(passOp)


    fout.cd() 
    fout.Write()
    fout.Close()

if __name__ == "__main__" :
    Wtag_SelectandCombine(sys.argv)
