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


def treeCombine(argv) : 
    parser = OptionParser()


    parser = OptionParser()

    parser.add_option('--type', type='string', action='store',
                      dest='type',
                      default = '',
                      help='type of files to combine: data or ttbar currently implemented - soon - Wjets (all HT binned samples) , ST (all Single Top samples) and pseudodata (all MC combined)') 

    parser.add_option('--maxEvents', type='int', action='store',
                      dest='maxEvents',
                      default = None,
                      help='Max events')

    parser.add_option('--isMC', action='store_true',
                      default=False,
                      dest='isMC',
                      help='is it MC?')

    parser.add_option('--80X', action='store_true',
                      default=False,
                      dest='80X',
                      help='Are the ttrees produced using CMSSW 80X?')

    parser.add_option('--verbose', action='store_true',
                      default=False,
                      dest='verbose',
                      help='Do you want to print values of key variables?')

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

    fout = ROOT.TFile( options.type +'_combinedttree_76x_v1p2_puppi.root', 'RECREATE')
    fout.cd()

    TTreeSemiLept = ROOT.TTree("TreeSemiLept", "TreeSemiLept")

    SemiLeptWeight      = array.array('f', [-1.])

    FatJetRhoRatio      = array.array('f', [-1.])
    FatJetMass          = array.array('f', [-1.])
    FatJetPt          = array.array('f', [-1.])
    FatJetMassSoftDrop  = array.array('f', [-1.])
    FatJetPtSoftDrop  = array.array('f', [-1.])
    FatJetTau1          = array.array('f', [-1.]) 
    FatJetTau2          = array.array('f', [-1.]) 
    FatJetTau3          = array.array('f', [-1.]) 
    FatJetTau32         = array.array('f', [-1.])
    FatJetTau21         = array.array('f', [-1.]) 

    FatJetSDsubjetWpt   = array.array('f', [-1.])
    FatJetSDsubjetWmass = array.array('f', [-1.])
    FatJetSDsubjetWtau1 = array.array('f', [-1.])
    FatJetSDsubjetWtau2 = array.array('f', [-1.])
    FatJetSDsubjetWtau3 = array.array('f', [-1.])
    FatJetSDsubjetWtau21 = array.array('f', [-1.])

    FatJetSDsubjet_isRealW = array.array('f', [-1.])
    FatJetSDsubjet_isFakeW = array.array('f', [-1.])

    FatJetSDsubjetBpt   = array.array('f', [-1.])
    FatJetSDsubjetBmass = array.array('f', [-1.])
    FatJetSDsubjetBbdisc = array.array('f', [-1.])

    LeptonType          = array.array('i', [-1])
    LeptonPt            = array.array('f', [-1.])

    LeptonPtRel         = array.array('f', [-1.])
    LeptonDRMin         = array.array('f', [-1.])

    SemiLepMETpt        = array.array('f', [-1.])

    SemiLeptRunNum        = array.array('f', [-1.])   
    SemiLeptLumiBlock     = array.array('f', [-1.])   
    SemiLeptEventNum      = array.array('f', [-1.])   

    TTreeSemiLept.Branch('SemiLeptWeight'      , SemiLeptWeight      ,  'SemiLeptWeight/F'      )
   
    TTreeSemiLept.Branch('FatJetRhoRatio'      , FatJetRhoRatio      ,  'FatJetRhoRatio/F'      )
    TTreeSemiLept.Branch('FatJetMass'          , FatJetMass          ,  'FatJetMass/F'          )
    TTreeSemiLept.Branch('FatJetPt'          , FatJetPt          ,  'FatJetPt/F'          )
    TTreeSemiLept.Branch('FatJetMassSoftDrop'  , FatJetMassSoftDrop  ,  'FatJetMassSoftDrop/F'  )
    TTreeSemiLept.Branch('FatJetPtSoftDrop'  , FatJetPtSoftDrop  ,  'FatJetPtSoftDrop/F'  )
    TTreeSemiLept.Branch('FatJetTau1'          , FatJetTau1          ,  'FatJetTau1/F'          )
    TTreeSemiLept.Branch('FatJetTau2'          , FatJetTau2          ,  'FatJetTau2/F'          )
    TTreeSemiLept.Branch('FatJetTau3'          , FatJetTau3          ,  'FatJetTau3/F'          )
    TTreeSemiLept.Branch('FatJetTau21'         , FatJetTau21         ,  'FatJetTau21/F'         )
    TTreeSemiLept.Branch('FatJetTau32'         , FatJetTau32         ,  'FatJetTau32/F'         )

    TTreeSemiLept.Branch('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt   ,  'FatJetSDsubjetWpt/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWmass' , FatJetSDsubjetWmass ,  'FatJetSDsubjetWmass/F' )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau1'   , FatJetSDsubjetWtau1   ,  'FatJetSDsubjetWtau1/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau2'   , FatJetSDsubjetWtau2   ,  'FatJetSDsubjetWtau2/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau3'   , FatJetSDsubjetWtau3   ,  'FatJetSDsubjetWtau3/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau21'   , FatJetSDsubjetWtau21   ,  'FatJetSDsubjetWtau21/F'   )

    if options.type == 'ttbar' :
        TTreeSemiLept.Branch('FatJetSDsubjet_isRealW'   , FatJetSDsubjet_isRealW   ,  'FatJetSDsubjet_isRealW/F'   )
        TTreeSemiLept.Branch('FatJetSDsubjet_isFakeW'   , FatJetSDsubjet_isFakeW   ,  'FatJetSDsubjet_isFakeW/F'   )

    TTreeSemiLept.Branch('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt   ,  'FatJetSDsubjetBpt/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetBmass' , FatJetSDsubjetBmass ,  'FatJetSDsubjetBmass/F' )
    TTreeSemiLept.Branch('FatJetSDsubjetBbdisc' , FatJetSDsubjetBbdisc ,  'FatJetSDsubjetBbdisc/F' )

    TTreeSemiLept.Branch('LeptonType'          , LeptonType          ,  'LeptonType/I'          )
    TTreeSemiLept.Branch('LeptonPt'            , LeptonPt            ,  'LeptonPt/F'            )

    TTreeSemiLept.Branch('LeptonPtRel'         , LeptonPtRel         ,  'LeptonPtRel/F'         )
    TTreeSemiLept.Branch('LeptonDRMin'         , LeptonDRMin         ,  'LeptonDRMin/F'         ) 

    TTreeSemiLept.Branch('SemiLepMETpt'        , SemiLepMETpt        ,  'SemiLepMETpt/F'        )

    TTreeSemiLept.Branch('SemiLeptRunNum'         ,  SemiLeptRunNum       ,  'SemiLeptRunNum/F'          )
    TTreeSemiLept.Branch('SemiLeptLumiBlock'      ,  SemiLeptLumiBlock    ,  'SemiLeptLumiBlock/F'       )
    TTreeSemiLept.Branch('SemiLeptEventNum'       ,  SemiLeptEventNum     ,  'SemiLeptEventNum/F'        )

    # _____ _   _ _____  _    _ _______   _____   ____   ____ _______ 
    #|_   _| \ | |  __ \| |  | |__   __| |  __ \ / __ \ / __ \__   __|
    #  | | |  \| | |__) | |  | |  | |    | |__) | |  | | |  | | | | 
    #  | | | . ` |  ___/| |  | |  | |    |  _  /| |  | | |  | | | |   
    # _| |_| |\  | |    | |__| |  | |    | | \ \| |__| | |__| | | | 
    #|_____|_| \_|_|     \____/   |_|    |_|  \_\\____/ \____/  |_|    

    # Input the existing trees to read them in and comine them into 1 tree

    if options.type == 'data' :
        filesin = [ ROOT.TFile('../b2gttbar_ttrees/singleel_ttree_76x_v1p2_puppi.root'), 
                ROOT.TFile('../b2gttbar_ttrees/singlemu_ttree_76x_v1p2_puppi.root') ] #  'b2gttbar_ttrees/ttjets_ttree_76x_v1p2_puppi.root',
    if options.type == 'ttbar' :
            filesin = [ROOT.TFile('../b2gttbar_ttrees/ttjets_ttree_76x_v1p2_puppi.root')]         

    filetitles =  ["ElData_PUPPI",
                   "MuData_PUPPI"] #"ttjets_PUPPI",

    alltrees = []

    for ji in filesin:
        alltrees.append(ji.Get("TreeSemiLept"))

    for ittree, ttree in enumerate(alltrees) :

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

        #FatJetSDbdiscW      = array.array('f', [-1.])
        FatJetSDsubjetWpt   = array.array('f', [-1.])
        FatJetSDsubjetWmass = array.array('f', [-1.])
        FatJetSDsubjetWtau1 = array.array('f', [-1.])
        FatJetSDsubjetWtau2 = array.array('f', [-1.])
        FatJetSDsubjetWtau3 = array.array('f', [-1.])

        #FatJetSDbdiscB      = array.array('f', [-1.])
        FatJetSDsubjetBpt   = array.array('f', [-1.])
        FatJetSDsubjetBmass = array.array('f', [-1.])
        FatJetSDsubjetBtau1 = array.array('f', [-1.])
        FatJetSDsubjetBtau2 = array.array('f', [-1.])
        FatJetSDsubjetBtau3 = array.array('f', [-1.])
   
        #BJetbDisc           = array.array('f', [-1.])

        LeptonType          = array.array('i', [-1])
        LeptonPt            = array.array('f', [-1.])

        LeptonPtRel         = array.array('f', [-1.])
        LeptonDRMin         = array.array('f', [-1.])

        SemiLepMETpt        = array.array('f', [-1.])

        #AK4bDisc            = array.array('f', [-1.])

        SemiLeptRunNum        = array.array('f', [-1.])   
        SemiLeptLumiBlock     = array.array('f', [-1.])   
        SemiLeptEventNum      = array.array('f', [-1.])

        ttree.SetBranchAddress('SemiLeptWeight'            , SemiLeptWeight     )

        ttree.SetBranchAddress('FatJetPt'            , FatJetPt            )
        ttree.SetBranchAddress('FatJetRhoRatio'      , FatJetRhoRatio      )
        ttree.SetBranchAddress('FatJetMass'          , FatJetMass          )
        ttree.SetBranchAddress('FatJetMassSoftDrop'  , FatJetMassSoftDrop  )
        ttree.SetBranchAddress('FatJetTau1'         , FatJetTau1         )
        ttree.SetBranchAddress('FatJetTau2'         , FatJetTau2         )
        ttree.SetBranchAddress('FatJetTau3'         , FatJetTau3         )
        ttree.SetBranchAddress('FatJetTau32'         , FatJetTau32         )
        ttree.SetBranchAddress('FatJetTau21'         , FatJetTau21         )

        #ttree.SetBranchAddress('FatJetSDbdiscW'      , FatJetSDbdiscW      )
        ttree.SetBranchAddress('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt   )
        ttree.SetBranchAddress('FatJetSDsubjetWmass' , FatJetSDsubjetWmass )
        ttree.SetBranchAddress('FatJetSDsubjetWtau1' , FatJetSDsubjetWtau1 )
        ttree.SetBranchAddress('FatJetSDsubjetWtau2' , FatJetSDsubjetWtau2 )
        ttree.SetBranchAddress('FatJetSDsubjetWtau3' , FatJetSDsubjetWtau3 )

        #ttree.SetBranchAddress('FatJetSDbdiscB'      , FatJetSDbdiscB      )
        ttree.SetBranchAddress('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt   )
        ttree.SetBranchAddress('FatJetSDsubjetBmass' , FatJetSDsubjetBmass )
        ttree.SetBranchAddress('FatJetSDsubjetBtau1' , FatJetSDsubjetBtau1 )
        ttree.SetBranchAddress('FatJetSDsubjetBtau2' , FatJetSDsubjetBtau2 )
        ttree.SetBranchAddress('FatJetSDsubjetBtau3' , FatJetSDsubjetBtau3 )

        #ttree.SetBranchAddress('BJetbDisc' , BJetbDisc )

        ttree.SetBranchAddress('LeptonType'          , LeptonType          )
        ttree.SetBranchAddress('LeptonPt'            , LeptonPt            )

        ttree.SetBranchAddress('LeptonPtRel'         , LeptonPtRel         )
        ttree.SetBranchAddress('LeptonDRMin'         , LeptonDRMin         )

        ttree.SetBranchAddress('SemiLepMETpt'        , SemiLepMETpt        )

        ttree.SetBranchAddress('SemiLeptRunNum'         ,  SemiLeptRunNum       )
        ttree.SetBranchAddress('SemiLeptLumiBlock'      ,  SemiLeptLumiBlock    )
        ttree.SetBranchAddress('SemiLeptEventNum'       ,  SemiLeptEventNum     )

        ttree.SetBranchStatus ('*', 0)

        ttree.SetBranchStatus ('SemiLeptWeight', 1)

        ttree.SetBranchStatus ('FatJetPt', 1)
        ttree.SetBranchStatus ('FatJetMass', 1)
        ttree.SetBranchStatus ('FatJetMassSoftDrop', 1)
        ttree.SetBranchStatus ('FatJetTau1', 1)
        ttree.SetBranchStatus ('FatJetTau2', 1)
        ttree.SetBranchStatus ('FatJetTau3', 1)
        ttree.SetBranchStatus ('FatJetTau32', 1)
        ttree.SetBranchStatus ('FatJetTau21', 1)
        ttree.SetBranchStatus ('FatJetRhoRatio', 1)

        #ttree.SetBranchStatus('BJetbDisc' , 1 )

        ttree.SetBranchStatus('FatJetSDsubjetWpt',1)
        ttree.SetBranchStatus('FatJetSDsubjetWmass',1)
        ttree.SetBranchStatus('FatJetSDsubjetWtau1',1)
        ttree.SetBranchStatus('FatJetSDsubjetWtau2',1)
        ttree.SetBranchStatus('FatJetSDsubjetWtau3',1)

        ttree.SetBranchStatus('FatJetSDsubjetBpt',1)
        ttree.SetBranchStatus('FatJetSDsubjetBmass',1)
        ttree.SetBranchStatus('FatJetSDsubjetBtau1',1)
        ttree.SetBranchStatus('FatJetSDsubjetBtau2',1)
        ttree.SetBranchStatus('FatJetSDsubjetBtau3',1)


        ttree.SetBranchStatus ('LeptonType'          , 1)
        ttree.SetBranchStatus ('LeptonPt'            , 1)

        ttree.SetBranchStatus ('LeptonPtRel'         , 1)
        ttree.SetBranchStatus ('LeptonDRMin'         , 1)

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

            
            #bJetCandP4puppi0 = ROOT.TLorentzVector()
            #bJetCandP4puppi0.SetPtEtaPhiM( BJetPt[0], BJetEta[0], BJetPhi[0], BJetMass[0])
            #bJetCandP4puppiEventnum = SemiLeptEventNum[0]
            #bJetCandP4puppi0Bdisc = -1.0
            #print "b jet PUPPI event number : " + str(bJetCandP4puppiEventnum)

            #bdisc = BJetbDisc2[0]

            #nuCandP4 = ROOT.TLorentzVector( )
            #nuCandP4.SetPtEtaPhiM( SemiLepMETpt[0], 0, SemiLepMETphi[0], SemiLepMETpt[0] )
            #theLepton = ROOT.TLorentzVector()
            #theLepton.SetPtEtaPhiE( LeptonPt[0], LeptonEta[0], LeptonPhi[0], LeptonEnergy[0] ) # Assume massless
            
            # FatJetSDpt = m / (R*sqrt(rhoRatio)) 
            weightS = SemiLeptWeight[0]
            if options.verbose : print "event weight is " + str(weightS)

            fatmass_sd = FatJetMassSoftDrop[0]
            fatmass = FatJetMass[0]
            fatpt = FatJetPt[0]
            Rhorat = FatJetRhoRatio[0]
            #print "Fat Jet Rho Ratio :" + str(Rhorat)
            if Rhorat > 0.001 :
                sqrtRhorat = math.sqrt(Rhorat)
                fatpt_sd = fatmass_sd / (0.8 * sqrtRhorat  )
            else :
                FatJetSD_pt = 0.
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
            #print "W Jet tau 2 :" + str(tau2)
            W_tau3 = FatJetSDsubjetWtau3[0]
            #print "W Jet tau 3 :" + str(tau3)


            if FatJetSDsubjetWtau1[0] > 0.001 :
                W_tau21 = FatJetSDsubjetWtau2[0] / FatJetSDsubjetWtau1[0]
            else :
                W_tau21 = 1.0
            B_pt = FatJetSDsubjetBpt[0]
            B_m = FatJetSDsubjetBmass[0]
            #print "B Jet Mass :" + str(B_m)

            #B_bdisc = 
            MET_pt = SemiLepMETpt[0]
            #print "MET_pt:" + str(MET_pt)
            W_pt2 = FatJetPt[0]
 
            #typE = BoosttypE[0]
            #evWeight = SemiLeptWeight[0]


            lepton_Type = LeptonType[0]
            lepton_pt = LeptonPt[0]
            #print "lepton_pt:" + str(lepton_pt)
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


            passKin = fatpt_sd > options.Ak8PtCut and W_pt > 0. and W_pt > 200.
            passKin2 =  fatpt_sd > 200. #and W_m < 1.
            
            passWPre =   W_m > 50. 
            passWPre2 = fatmass_sd > 50. 
            passTopTag = tau32 < options.tau32Cut and fatmass_sd > 110. and fatmass_sd < 250.
            pass2DCut = lepton_ptRel  > 20. or lepton_DRmin > 0.4 # B2G-15-002 uses  LeptonPtRel[0] > 20.or LeptonDRMin[0] > 0.4 (was 55.0 here)
            #passBtag = bdisc > 0.7

            passWPostM = (65. < W_m < 105.) #(55. < W_m < 105.)#50 to 130 before
            passWPosttau = W_tau21 < options.tau21Cut  #W_tau21 < 0.6 
            passWPost2M = (65.0 < W_m < 105.)  #(55. < FatJetSD_m < 105.)
            passWPost2tau = tau21 < options.tau21Cut
            passEleMETcut =  lepton_Type == 1 and MET_pt > 120. and lepton_pt > 55. #110.
            # B2G-15-002  uses ( theLepton.Perp() + MET_pt ) > 150. (was previously 250 here) 
            passMuHtLepcut = lepton_Type == 2 and ( lepton_pt + MET_pt ) > 150. and lepton_pt > 55.
            passLepcut = passEleMETcut or passMuHtLepcut 
  

            if  passTopTag and pass2DCut and passLepcut: # and passBtag :  
                if passKin :
                    #BoosttypE           [0] = typE
                    SemiLeptWeight      [0] = weightS

                    FatJetRhoRatio      [0] = Rhorat
                    FatJetMass          [0] = fatmass
                    FatJetPt            [0] = fatpt
                    FatJetMassSoftDrop  [0] = fatmass_sd
                    FatJetPtSoftDrop    [0] = fatpt_sd
                    FatJetTau1          [0] = tau1
                    FatJetTau2          [0] = tau2
                    FatJetTau3          [0] = tau3
                    FatJetTau32         [0] = tau32
                    FatJetTau21         [0] = tau21

                    FatJetSDsubjetWpt   [0] = W_pt
                    FatJetSDsubjetWmass [0] = W_m
                    FatJetSDsubjetWtau1 [0] = W_tau1
                    FatJetSDsubjetWtau2 [0] = W_tau2
                    FatJetSDsubjetWtau3 [0] = W_tau3
                    FatJetSDsubjetWtau21 [0] = W_tau21

                    if options.type == 'ttbar' :
                        FatJetSDsubjet_isRealW[0] = 0.0  # correct this once gen matching is implemented
                        FatJetSDsubjet_isFakeW[0] = 0.0  # correct this once gen matching is implemented

                    FatJetSDsubjetBpt   [0] = B_pt 
                    FatJetSDsubjetBmass [0] = B_m
                    #FatJetSDsubjetBbdisc[0] = B_bdisc

                    LeptonType          [0] = lepton_Type
                    LeptonPt            [0] = lepton_pt

                    LeptonPtRel         [0] = lepton_ptRel
                    LeptonDRMin         [0] = lepton_DRmin

                    SemiLepMETpt        [0] = MET_pt

                    SemiLeptRunNum      [0] = runNum
                    SemiLeptLumiBlock   [0] = lumiBlock 
                    SemiLeptEventNum    [0] = eventNum

                    TTreeSemiLept.Fill()


    fout.cd() 
    fout.Write()
    fout.Close()
    print "All Done. TTrees were successfully combined!"

if __name__ == "__main__" :
    treeCombine(sys.argv)
