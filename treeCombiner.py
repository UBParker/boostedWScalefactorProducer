#! /usr/bin/env python


## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 


# This script reads multiples TTrees and does a semileptonic T Tbar selection then writes all results to a single TTree


import sys
import math
import array
from optparse import OptionParser


def treeCombiner(argv) : 
    parser = OptionParser()


    parser = OptionParser()

    parser.add_option('--type', type='string', action='store',
                      dest='dtype',
                      default = '',
                      help='type of files to combine: data , ttjets, wjets , st and pseudodata (all MC combined)') 

    parser.add_option('--maxEvents', type='int', action='store',
                      dest='maxEvents',
                      default = None,
                      help='Max events')

    parser.add_option('--is80x', action='store_true',
                      default=True,
                      dest='is80x',
                      help='Are the ttrees produced using CMSSW 80X?')

    parser.add_option('--verbose', action='store_true',
                      default=False,
                      dest='verbose',
                      help='Do you want to print values of key variables?')

        
    (options, args) = parser.parse_args(argv)
    argv = []


    #   ____  _    _ _______ _____  _    _ _______   _____   ____   ____ _______ 
    #  / __ \| |  | |__   __|  __ \| |  | |__   __| |  __ \ / __ \ / __ \__   __|
    # | |  | | |  | |  | |  | |__) | |  | |  | |    | |__) | |  | | |  | | | |   
    # | |  | | |  | |  | |  |  ___/| |  | |  | |    |  _  /| |  | | |  | | | |   
    # | |__| | |__| |  | |  | |    | |__| |  | |    | | \ \| |__| | |__| | | |   
    #  \____/ \____/   |_|  |_|     \____/   |_|    |_|  \_\\____/ \____/  |_|   
                                                                                

    # @@@ Create output root file
    import ROOT
    if options.is80x :     
        fout = ROOT.TFile( './output80x/'+ options.dtype +'_combinedttree_80x_v1p2_puppi.root', 'RECREATE')
        print "Using 80X ttrees!"
    else : 
        fout = ROOT.TFile( './output76x/'+ options.dtype +'_combinedttree_76x_v1p2_puppi.root', 'RECREATE')
        print "Using 76X ttrees!"
    fout.cd()

    TTreeSemiLept = ROOT.TTree("TreeSemiLept", "TreeSemiLept")

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

    FatJetSDbdiscW_      = array.array('f', [-1.])
    FatJetSDsubjetWpt_   = array.array('f', [-1.])
    FatJetSDsubjetWmass_ = array.array('f', [-1.])
    FatJetSDsubjetWtau1_ = array.array('f', [-1.])
    FatJetSDsubjetWtau2_ = array.array('f', [-1.])
    FatJetSDsubjetWtau3_ = array.array('f', [-1.])
    FatJetSDsubjetWtau21_ = array.array('f', [-1.])

    #FatJetSDsubjet_isRealW_ = array.array('f', [-1.])
    #FatJetSDsubjet_isFakeW_ = array.array('f', [-1.])

    FatJetSDsubjetBpt_   = array.array('f', [-1.])
    FatJetSDsubjetBmass_ = array.array('f', [-1.])
    FatJetSDbdiscB_      = array.array('f', [-1.])

    LeptonType_          = array.array('i', [-1])
    LeptonPt_            = array.array('f', [-1.])

    LeptonPtRel_         = array.array('f', [-1.])
    LeptonDRMin_         = array.array('f', [-1.])
    DeltaPhiLepFat_       = array.array('f', [-1.])

    SemiLepMETpt_        = array.array('f', [-1.])

    SemiLeptRunNum_        = array.array('f', [-1.])   
    SemiLeptLumiBlock_     = array.array('f', [-1.])   
    SemiLeptEventNum_      = array.array('f', [-1.])   

    TTreeSemiLept.Branch('SemiLeptWeight'      , SemiLeptWeight_      ,  'SemiLeptWeight/F'      )
   
    TTreeSemiLept.Branch('FatJetRhoRatio'      , FatJetRhoRatio_      ,  'FatJetRhoRatio/F'      )
    TTreeSemiLept.Branch('FatJetMass'          , FatJetMass_          ,  'FatJetMass/F'          )
    TTreeSemiLept.Branch('FatJetPt'          , FatJetPt_          ,  'FatJetPt/F'          )
    TTreeSemiLept.Branch('FatJetMassSoftDrop'  , FatJetMassSoftDrop_  ,  'FatJetMassSoftDrop/F'  )
    TTreeSemiLept.Branch('FatJetPtSoftDrop'  , FatJetPtSoftDrop_  ,  'FatJetPtSoftDrop/F'  )
    TTreeSemiLept.Branch('FatJetTau1'          , FatJetTau1_          ,  'FatJetTau1/F'          )
    TTreeSemiLept.Branch('FatJetTau2'          , FatJetTau2_          ,  'FatJetTau2/F'          )
    TTreeSemiLept.Branch('FatJetTau3'          , FatJetTau3_          ,  'FatJetTau3/F'          )
    TTreeSemiLept.Branch('FatJetTau21'         , FatJetTau21_         ,  'FatJetTau21/F'         )
    TTreeSemiLept.Branch('FatJetTau32'         , FatJetTau32_         ,  'FatJetTau32/F'         )

    TTreeSemiLept.Branch('FatJetSDbdiscW'   , FatJetSDbdiscW_   ,  'FatJetSDbdiscW/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt_   ,  'FatJetSDsubjetWpt/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWmass' , FatJetSDsubjetWmass_ ,  'FatJetSDsubjetWmass/F' )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau1'   , FatJetSDsubjetWtau1_   ,  'FatJetSDsubjetWtau1/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau2'   , FatJetSDsubjetWtau2_   ,  'FatJetSDsubjetWtau2/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau3'   , FatJetSDsubjetWtau3_   ,  'FatJetSDsubjetWtau3/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau21'   , FatJetSDsubjetWtau21_   ,  'FatJetSDsubjetWtau21/F'   )

    
    #TTreeSemiLept.Branch('FatJetSDsubjet_isRealW'   , FatJetSDsubjet_isRealW_   ,  'FatJetSDsubjet_isRealW/F'   )
    #TTreeSemiLept.Branch('FatJetSDsubjet_isFakeW'   , FatJetSDsubjet_isFakeW_   ,  'FatJetSDsubjet_isFakeW/F'   )

    TTreeSemiLept.Branch('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt_   ,  'FatJetSDsubjetBpt/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetBmass' , FatJetSDsubjetBmass_ ,  'FatJetSDsubjetBmass/F' )
    TTreeSemiLept.Branch('FatJetSDbdiscB' , FatJetSDbdiscB_ ,  'FatJetSDbdiscB/F' )

    TTreeSemiLept.Branch('LeptonType'          , LeptonType_          ,  'LeptonType/I'          )
    TTreeSemiLept.Branch('LeptonPt'            , LeptonPt_            ,  'LeptonPt/F'            )

    TTreeSemiLept.Branch('LeptonPtRel'         , LeptonPtRel_         ,  'LeptonPtRel/F'         )
    TTreeSemiLept.Branch('LeptonDRMin'         , LeptonDRMin_         ,  'LeptonDRMin/F'         ) 

    TTreeSemiLept.Branch('DeltaPhiLepFat'      , DeltaPhiLepFat_      ,  'DeltaPhiLepFat/F'      ) 

    TTreeSemiLept.Branch('SemiLepMETpt'        , SemiLepMETpt_        ,  'SemiLepMETpt/F'        )

    TTreeSemiLept.Branch('SemiLeptRunNum'         ,  SemiLeptRunNum_       ,  'SemiLeptRunNum/F'          )
    TTreeSemiLept.Branch('SemiLeptLumiBlock'      ,  SemiLeptLumiBlock_    ,  'SemiLeptLumiBlock/F'       )
    TTreeSemiLept.Branch('SemiLeptEventNum'       ,  SemiLeptEventNum_     ,  'SemiLeptEventNum/F'        )

    # _____ _   _ _____  _    _ _______   _____   ____   ____ _______ 
    #|_   _| \ | |  __ \| |  | |__   __| |  __ \ / __ \ / __ \__   __|
    #  | | |  \| | |__) | |  | |  | |    | |__) | |  | | |  | | | | 
    #  | | | . ` |  ___/| |  | |  | |    |  _  /| |  | | |  | | | |   
    # _| |_| |\  | |    | |__| |  | |    | | \ \| |__| | |__| | | | 
    #|_____|_| \_|_|     \____/   |_|    |_|  \_\\____/ \____/  |_|    

    # Input the existing trees to read them in and comine them into 1 tree

       
    if options.is80x: 
        if options.dtype == 'data' :
            filesin = [ ROOT.TFile('./newdata/Puppi_Eldata_lumi12p295_13TeV_80Xv2p0Ntuple_98p_1of7.root
                        ROOT.TFile('./newdata/Puppi_Eldata_lumi12p295_13TeV_80Xv2p0Ntuple_98p_2of7.root'),
                        ROOT.TFile('./newdata/Puppi_Eldata_lumi12p295_13TeV_80Xv2p0Ntuple_98p_3of7.root'),
                        ROOT.TFile('./newdata/Puppi_Eldata_lumi12p295_13TeV_80Xv2p0Ntuple_98p_4of7.root'),
                        ROOT.TFile('./newdata/Puppi_Eldata_lumi12p295_13TeV_80Xv2p0Ntuple_98p_5of7.root'),
                        ROOT.TFile('./newdata/Puppi_Eldata_lumi12p295_13TeV_80Xv2p0Ntuple_98p_6of7.root'),
                        ROOT.TFile('./newdata/Puppi_Eldata_lumi12p295_13TeV_80Xv2p0Ntuple_98p_7of7.root'),
                        ROOT.TFile('./newdata/Puppi_Mudata_lumi12p358_13TeV_80Xv2p0Ntuple_98p_1of7.root'),
                        ROOT.TFile('./newdata/Puppi_Mudata_lumi12p358_13TeV_80Xv2p0Ntuple_98p_2of7.root'),
                        ROOT.TFile('./newdata/Puppi_Mudata_lumi12p358_13TeV_80Xv2p0Ntuple_98p_3of7.root'),
                        ROOT.TFile('./newdata/Puppi_Mudata_lumi12p358_13TeV_80Xv2p0Ntuple_98p_4of7.root'),
                        ROOT.TFile('./newdata/Puppi_Mudata_lumi12p358_13TeV_80Xv2p0Ntuple_98p_5of7.root'),
                        ROOT.TFile('./newdata/Puppi_Mudata_lumi12p358_13TeV_80Xv2p0Ntuple_98p_6of7.root'),
                        ROOT.TFile('./newdata/Puppi_Mudata_lumi12p358_13TeV_80Xv2p0Ntuple_98p_7of7.root')]

            '''
            filesin = [ ROOT.TFile('./data/Puppi_MuData_12p35875invfb_13TeV_80Xv2p0Ntuple_incomplete_2of2.root'), 
                        ROOT.TFile('./data/Puppi_ElData_12p29565invfb_13TeV_80Xv2p0Ntuple_2of2.root'),
                        ROOT.TFile('./data/Puppi_ElData_12p29565invfb_13TeV_80Xv2p0Ntuple_1of2.root'),
                        ROOT.TFile('./data/Puppi_MuData_12p35875invfb_13TeV_80Xv2p0Ntuple_incomplete_1of2.root')]

        if options.dtype == 'mudata' :
            filesin = [ ROOT.TFile('./data/Puppi_MuData_12p35875invfb_13TeV_80Xv2p0Ntuple_incomplete_2of2.root'), 
                        ROOT.TFile('./data/Puppi_MuData_12p35875invfb_13TeV_80Xv2p0Ntuple_incomplete_1of2.root')]

        if options.dtype == 'eldata' :
            filesin = [ ROOT.TFile('./data/Puppi_ElData_12p29565invfb_13TeV_80Xv2p0Ntuple_2of2.root'),
                        ROOT.TFile('./data/Puppi_ElData_12p29565invfb_13TeV_80x_80Xv2p0Ntuple_1of2.root')]
            '''

        if options.dtype == 'ttjets' :

            filesin = [ ROOT.TFile('./newttjets/Puppi_TT_TuneCUETP8M1_13TeV_80Xv2p0Ntuple_96p_1of1.root')]   
            #filesin = [ ROOT.TFile('./ttjets/Puppi_TT_TuneCUETP8M1_13TeV_80Xv2p0Ntuple_incomplete_1of1.root')]   

        '''
        if options.dtype == 'wjets' :
                filesin = [ ROOT.TFile('./wjets/Puppi_Wjets100to200_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets200to400_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets400to600_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets600to800_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets800to1200_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets1200to2500_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets2500toInf_13TeV_80Xv2p0Ntuple.root')]
        '''

        if options.dtype == 'wjets1' :
                filesin = [ ROOT.TFile('./newwjets/Puppi_WJets_100to200_13TeV_80Xv2p0Ntuple_1of1.root')]
        if options.dtype == 'wjets2' :
                filesin = [ ROOT.TFile('./newwjets/Puppi_WJets_200to400_13TeV_80Xv2p0Ntuple_1of1.root')]
        if options.dtype == 'wjets3' :
                filesin = [ ROOT.TFile('./newwjets/Puppi_WJets_400to600_13TeV_80Xv2p0Ntuple_1of1.root')]
        if options.dtype == 'wjets4' :
                filesin = [ ROOT.TFile('./newwjets/Puppi_WJets_600to800_13TeV_80Xv2p0Ntuple_1of1.root')]
        if options.dtype == 'wjets5' :
                filesin = [ ROOT.TFile('./newwjets/Puppi_WJets_800to1200_13TeV_80Xv2p0Ntuple_1of1.root')]
        if options.dtype == 'wjets6' :
                filesin = [ ROOT.TFile('./newwjets/Puppi_WJets_1200to2500_13TeV_80Xv2p0Ntuple_1of1.root')]
        if options.dtype == 'wjets7' :
                filesin = [ ROOT.TFile('./newwjets/Puppi_WJets_2500toInf_13TeV_80Xv2p0Ntuple_1of1.root')]
        '''
        if options.dtype == 'wjets' :
                filesin = [ ROOT.TFile('./wjets/Puppi_Wjets100to200_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets200to400_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets400to600_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets600to800_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets800to1200_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets1200to2500_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./wjets/Puppi_Wjets2500toInf_13TeV_80Xv2p0Ntuple.root')]


        if options.dtype == 'st' :

                filesin = [ ROOT.TFile('./st/Puppi_STtchannelTop_13TeV_80Xv2p0Ntuple.root'),
                            ROOT.TFile('./st/Puppi_STtchannelAntitop_13TeV_80Xv2p0Ntuple.root')]
        '''

        if options.dtype == 'st1' :
                filesin = [ ROOT.TFile('./newst/Puppi_ST_top_13TeV_80Xv2p0Ntuple_1of1.root')]

        if options.dtype == 'st2' :
                filesin = [ ROOT.TFile('./newst/Puppi_ST_antitop_13TeV_80Xv2p0Ntuple_1of1.root')]



        if options.dtype == 'pseudodata' :
                filesin = [ ROOT.TFile('./newst/Puppi_ST_top_13TeV_80Xv2p0Ntuple_1of1.root'),
                            ROOT.TFile('./newst/Puppi_ST_antitop_13TeV_80Xv2p0Ntuple_1of1.root'),
                            ROOT.TFile('./newwjets/Puppi_WJets_100to200_13TeV_80Xv2p0Ntuple_1of1.root'),
                            ROOT.TFile('./newwjets/Puppi_WJets_200to400_13TeV_80Xv2p0Ntuple_1of1.root'),
                            ROOT.TFile('./newwjets/Puppi_WJets_400to600_13TeV_80Xv2p0Ntuple_1of1.root'),
                            ROOT.TFile('./newwjets/Puppi_WJets_600to800_13TeV_80Xv2p0Ntuple_1of1.root'),
                            ROOT.TFile('./newwjets/Puppi_WJets_800to1200_13TeV_80Xv2p0Ntuple_1of1.root'),
                            ROOT.TFile('./newwjets/Puppi_WJets_1200to2500_13TeV_80Xv2p0Ntuple_1of1.root'),
                            ROOT.TFile('./newwjets/Puppi_WJets_2500toInf_13TeV_80Xv2p0Ntuple_1of1.root'),
                            ROOT.TFile('./newttjets/Puppi_TT_TuneCUETP8M1_13TeV_80Xv2p0Ntuple_96p_1of1.root')]
    else :
        if options.dtype == 'data' :
            filesin = [ ROOT.TFile('./b2gttbar_ttrees/singleel_ttree_76x_v1p2_puppi.root'), 
                    ROOT.TFile('./b2gttbar_ttrees/singlemu_ttree_76x_v1p2_puppi.root') ] 
        if options.dtype == 'ttjets' :
                filesin = [ROOT.TFile('./b2gttbar_ttrees/ttjets_ttree_76x_v1p2_puppi.root')] 
        if options.dtype != 'ttjets' and options.dtype != 'data' :
                print "No input files for 76x in types other than ttjets and data!"

    # create list of trees to be combined
    alltrees = []

    for ji in filesin:
        if options.verbose: print "File is " + str(ji)
        alltrees.append(ji.Get("TreeSemiLept"))

    for ittree, ttree in enumerate(alltrees) :
        tempevnum = 0.
    # create arrays to store the data
        SemiLeptWeight      = array.array('f', [-1.])

        FatJetPt            = array.array('f', [-1.])
        FatJetRhoRatio      = array.array('f', [-1.])
        FatJetMass          = array.array('f', [-1.])
        FatJetMassSoftDrop  = array.array('f', [-1.])
        FatJetTau1          = array.array('f', [-1.]) 
        FatJetTau2          = array.array('f', [-1.]) 
        FatJetTau3          = array.array('f', [-1.]) 
        FatJetTau32         = array.array('f', [-1.])
        FatJetTau21         = array.array('f', [-1.]) 

        FatJetSDbdiscW      = array.array('f', [-1.])
        FatJetSDsubjetWpt   = array.array('f', [-1.])
        FatJetSDsubjetWptRaw   = array.array('f', [-1.])
        FatJetSDsubjetWmass = array.array('f', [-1.])
        FatJetSDsubjetWmassRaw = array.array('f', [-1.])
        FatJetSDsubjetWtau1 = array.array('f', [-1.])
        FatJetSDsubjetWtau2 = array.array('f', [-1.])
        FatJetSDsubjetWtau3 = array.array('f', [-1.])
        FatJetSDsubjetWtau21 = array.array('f', [-1.])

        FatJetSDbdiscB      = array.array('f', [-1.])
        FatJetSDsubjetBpt   = array.array('f', [-1.])
        FatJetSDsubjetBmass = array.array('f', [-1.])
        FatJetSDsubjetBtau1 = array.array('f', [-1.])
        FatJetSDsubjetBtau2 = array.array('f', [-1.])
        FatJetSDsubjetBtau3 = array.array('f', [-1.])

        #FatJetSDsubjet_isRealW = array.array('f', [-1.])
        #FatJetSDsubjet_isFakeW = array.array('f', [-1.])

        LeptonType          = array.array('i', [-1])
        LeptonPt            = array.array('f', [-1.])

        LeptonPtRel         = array.array('f', [-1.])
        LeptonDRMin         = array.array('f', [-1.])

        DeltaPhiLepFat        = array.array('f', [-1.])

        SemiLepMETpt        = array.array('f', [-1.])

        #AK4bDisc            = array.array('f', [-1.])

        SemiLeptRunNum        = array.array('f', [-1.])   
        SemiLeptLumiBlock     = array.array('f', [-1.])   
        SemiLeptEventNum      = array.array('f', [-1.])

        ttree.SetBranchAddress('SemiLeptWeight'      , SemiLeptWeight      )

        ttree.SetBranchAddress('FatJetPt'            , FatJetPt            )
        ttree.SetBranchAddress('FatJetRhoRatio'      , FatJetRhoRatio      )
        ttree.SetBranchAddress('FatJetMass'          , FatJetMass          )
        ttree.SetBranchAddress('FatJetMassSoftDrop'  , FatJetMassSoftDrop  )
        ttree.SetBranchAddress('FatJetTau1'         , FatJetTau1           )
        ttree.SetBranchAddress('FatJetTau2'         , FatJetTau2           )
        ttree.SetBranchAddress('FatJetTau3'         , FatJetTau3           )
        ttree.SetBranchAddress('FatJetTau32'         , FatJetTau32         )
        ttree.SetBranchAddress('FatJetTau21'         , FatJetTau21         )

        ttree.SetBranchAddress('FatJetSDbdiscW'      , FatJetSDbdiscW      )
        ttree.SetBranchAddress('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt   )
        ttree.SetBranchAddress('FatJetSDsubjetWptRaw'   , FatJetSDsubjetWptRaw   )
        ttree.SetBranchAddress('FatJetSDsubjetWmass' , FatJetSDsubjetWmass )
        ttree.SetBranchAddress('FatJetSDsubjetWmassRaw' , FatJetSDsubjetWmassRaw )
        ttree.SetBranchAddress('FatJetSDsubjetWtau1' , FatJetSDsubjetWtau1 )
        ttree.SetBranchAddress('FatJetSDsubjetWtau2' , FatJetSDsubjetWtau2 )
        ttree.SetBranchAddress('FatJetSDsubjetWtau3' , FatJetSDsubjetWtau3 )
        ttree.SetBranchAddress('FatJetSDsubjetWtau21' , FatJetSDsubjetWtau21 )

        ttree.SetBranchAddress('FatJetSDbdiscB'      , FatJetSDbdiscB      )
        ttree.SetBranchAddress('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt   )
        ttree.SetBranchAddress('FatJetSDsubjetBmass' , FatJetSDsubjetBmass )
        ttree.SetBranchAddress('FatJetSDsubjetBtau1' , FatJetSDsubjetBtau1 )
        ttree.SetBranchAddress('FatJetSDsubjetBtau2' , FatJetSDsubjetBtau2 )
        ttree.SetBranchAddress('FatJetSDsubjetBtau3' , FatJetSDsubjetBtau3 )

        #ttree.SetBranchAddress('FatJetSDsubjet_isRealW'   , FatJetSDsubjet_isRealW ) 
        #ttree.SetBranchAddress('FatJetSDsubjet_isFakeW'   , FatJetSDsubjet_isFakeW )

        ttree.SetBranchAddress('LeptonType'          , LeptonType          )
        ttree.SetBranchAddress('LeptonPt'            , LeptonPt            )

        ttree.SetBranchAddress('LeptonPtRel'         , LeptonPtRel         )
        ttree.SetBranchAddress('LeptonDRMin'         , LeptonDRMin         )
        ttree.SetBranchAddress('DeltaPhiLepFat'         , DeltaPhiLepFat   )

        ttree.SetBranchAddress('SemiLepMETpt'        , SemiLepMETpt        )

        ttree.SetBranchAddress('SemiLeptRunNum'         ,  SemiLeptRunNum       )
        ttree.SetBranchAddress('SemiLeptLumiBlock'      ,  SemiLeptLumiBlock    )
        ttree.SetBranchAddress('SemiLeptEventNum'       ,  SemiLeptEventNum     )

        ttree.SetBranchStatus ('*', 0)

        ttree.SetBranchStatus ('SemiLeptWeight', 1)


        ttree.SetBranchStatus ('FatJetPt', 1)
        ttree.SetBranchStatus ('FatJetRhoRatio', 1)
        ttree.SetBranchStatus ('FatJetMass', 1)
        ttree.SetBranchStatus ('FatJetMassSoftDrop', 1)
        ttree.SetBranchStatus ('FatJetTau1', 1)
        ttree.SetBranchStatus ('FatJetTau2', 1)
        ttree.SetBranchStatus ('FatJetTau3', 1)
        ttree.SetBranchStatus ('FatJetTau32', 1)
        ttree.SetBranchStatus ('FatJetTau21', 1)

        ttree.SetBranchStatus('FatJetSDbdiscW',1)
        ttree.SetBranchStatus('FatJetSDsubjetWpt',1)
        ttree.SetBranchStatus('FatJetSDsubjetWptRaw',1)
        ttree.SetBranchStatus('FatJetSDsubjetWmass',1)
        ttree.SetBranchStatus('FatJetSDsubjetWmassRaw',1)
        ttree.SetBranchStatus('FatJetSDsubjetWtau1',1)
        ttree.SetBranchStatus('FatJetSDsubjetWtau2',1)
        ttree.SetBranchStatus('FatJetSDsubjetWtau3',1)
        ttree.SetBranchStatus('FatJetSDsubjetWtau21',1)

        ttree.SetBranchStatus('FatJetSDbdiscB',1)
        ttree.SetBranchStatus('FatJetSDsubjetBpt',1)
        ttree.SetBranchStatus('FatJetSDsubjetBmass',1)
        ttree.SetBranchStatus('FatJetSDsubjetBtau1',1)
        ttree.SetBranchStatus('FatJetSDsubjetBtau2',1)
        ttree.SetBranchStatus('FatJetSDsubjetBtau3',1)

        #ttree.SetBranchStatus('FatJetSDsubjet_isRealW',1)
        #ttree.SetBranchStatus('FatJetSDsubjet_isFakeW',1)

        ttree.SetBranchStatus ('LeptonType'          , 1)
        ttree.SetBranchStatus ('LeptonPt'            , 1)

        ttree.SetBranchStatus ('LeptonPtRel'         , 1)
        ttree.SetBranchStatus ('LeptonDRMin'         , 1)
        ttree.SetBranchStatus ('DeltaPhiLepFat'      , 1)
        ttree.SetBranchStatus ('SemiLepMETpt'        , 1)

        ttree.SetBranchStatus ('SemiLeptRunNum'      , 1)
        ttree.SetBranchStatus ('SemiLeptLumiBlock'   , 1)
        ttree.SetBranchStatus ('SemiLeptEventNum'    , 1)

        entries = ttree.GetEntriesFast()
        if options.maxEvents != None :
            eventsToRun = options.maxEvents
        else :
            eventsToRun = entries


        for jentry in xrange( eventsToRun ):
            if jentry % 100000 == 0 :
                print 'processing ' + str(jentry)
        # get the next tree in the chain and verify
            ientry = ttree.GetEntry( jentry )
            if ientry < 0:
                break

            fatmass_sd = FatJetMassSoftDrop[0]
            if ( fatmass_sd == -1. ) :
                continue
                print "skipping event, Fatmass is -1"

            weightS = SemiLeptWeight[0]
            #if fatmass_sd > 110. : print "Fat Jet mass SD  {0:6.3} in ttree number {1}".format(fatmass_sd, ittree)
            fatmass = FatJetMass[0]
            fatpt = FatJetPt[0]
            Rhorat = FatJetRhoRatio[0]
            if Rhorat > 0.001 :
                sqrtRhorat = math.sqrt(Rhorat)
                fatpt_sd = fatmass_sd / (0.8 * sqrtRhorat  )
            else :
                fatpt_sd = 0.
            tau32 = FatJetTau32[0]
            #print "Fat Jet tau 32 :" + str(tau32)
            tau21 = FatJetTau21[0]
            #print "Fat Jet tau 21 :" + str(tau21)


            tau1 = FatJetTau1[0]
            #print "Fat Jet tau 1 :" + str(tau1)
            tau2 = FatJetTau2[0]
            #print "Fat Jet tau 2 :" + str(tau2)
            tau3 = FatJetTau3[0]


            W_m = FatJetSDsubjetWmass[0]
            W_pt = FatJetSDsubjetWpt[0]
            W_tau1 = FatJetSDsubjetWtau1[0]
            W_tau2 = FatJetSDsubjetWtau2[0]
            W_tau3 = FatJetSDsubjetWtau3[0]
            W_bdisc = FatJetSDbdiscW[0]

            if not options.is80x :
                if abs(W_tau1) > 0.000001 :
                    W_tau21 = W_tau2 / W_tau1
                else :
                    W_tau21 = 1.
            else :
                W_tau21 = FatJetSDsubjetWtau21[0]

            if options.dtype == 'ttjets':
                realw = 0
                fakew = 0
                #realw = FatJetSDsubjet_isRealW[0]
                #fakew = FatJetSDsubjet_isFakeW[0]
            else:
                realw = 0
                fakew = 0
            B_pt = FatJetSDsubjetBpt[0]
            B_m = FatJetSDsubjetBmass[0]
            B_bdisc = FatJetSDbdiscB[0]


            MET_pt = SemiLepMETpt[0]

            W_pt2 = FatJetPt[0]
 
            #typE = BoosttypE[0]


            lepton_Type = LeptonType[0]
            lepton_pt = LeptonPt[0]
            lepton_ptRel = LeptonPtRel[0]
            lepton_DRmin = LeptonDRMin[0] 

            dphi =  DeltaPhiLepFat[0]

            runNum = SemiLeptRunNum[0]
            lumiBlock = SemiLeptLumiBlock[0]
            eventNum = SemiLeptEventNum[0]
            
            if (options.verbose): # and fatpt_sd > 350. 
                print ">>>>>>>>>>>>>>treeCombiner>>>>>>>>>>"
                print "Event Number : " + str(eventNum)
                print "Fat Jet Pt SD : " + str(fatpt_sd)
                print "Fat Jet mass SD : " + str(fatmass_sd)
                print "Fat Jet Rho Ratio : " + str(Rhorat)
                if eventNum == tempevnum :
                    print "Repeated event: tree index in list "+str(ittree) 
                print "-------------------------------------"
            tempevnum = eventNum

            SemiLeptWeight_      [0] = weightS

            FatJetRhoRatio_      [0] = Rhorat
            FatJetMass_          [0] = fatmass
            FatJetPt_            [0] = fatpt
            FatJetMassSoftDrop_  [0] = fatmass_sd
            FatJetPtSoftDrop_    [0] = fatpt_sd

            FatJetTau1_          [0] = tau1
            FatJetTau2_          [0] = tau2
            FatJetTau3_          [0] = tau3
            FatJetTau32_         [0] = tau32
            FatJetTau21_         [0] = tau21

            FatJetSDbdiscW_       [0] = W_bdisc
            FatJetSDsubjetWpt_    [0] = W_pt
            FatJetSDsubjetWmass_  [0] = W_m
            FatJetSDsubjetWtau1_  [0] = W_tau1
            FatJetSDsubjetWtau2_  [0] = W_tau2
            FatJetSDsubjetWtau3_  [0] = W_tau3
            FatJetSDsubjetWtau21_ [0] = W_tau21

            #FatJetSDsubjet_isRealW_ [0] = realw 
            #FatJetSDsubjet_isFakeW_ [0] = fakew 

            FatJetSDsubjetBpt_   [0] = B_pt 
            FatJetSDsubjetBmass_ [0] = B_m
            FatJetSDbdiscB_      [0] = B_bdisc

            LeptonType_          [0] = lepton_Type
            LeptonPt_            [0] = lepton_pt
            LeptonPtRel_         [0] = lepton_ptRel
            LeptonDRMin_         [0] = lepton_DRmin
            DeltaPhiLepFat_      [0] = dphi

            SemiLepMETpt_        [0] = MET_pt

            SemiLeptRunNum_      [0] = runNum
            SemiLeptLumiBlock_   [0] = lumiBlock 
            SemiLeptEventNum_    [0] = eventNum

            TTreeSemiLept.Fill()

    fout.cd() 
    fout.Write()
    fout.Close()
    print "All Done. The "+ options.dtype +" TTrees were successfully combined!"
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
if __name__ == "__main__" :
    treeCombiner(sys.argv)
