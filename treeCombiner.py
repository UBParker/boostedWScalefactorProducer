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
                      dest='type',
                      default = '',
                      help='type of files to combine: data or ttjets currently implemented - soon - Wjets (all HT binned samples) , ST (all Single Top samples) and pseudodata (all MC combined)') 

    parser.add_option('--maxEvents', type='int', action='store',
                      dest='maxEvents',
                      default = None,
                      help='Max events')

    parser.add_option('--80X', action='store_true',
                      default=False,
                      dest='80X',
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

    fout = ROOT.TFile( './alphaMethod/'+ options.type +'_combinedttree_76x_v1p2_puppi.root', 'RECREATE')
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

    TTreeSemiLept.Branch('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt_   ,  'FatJetSDsubjetWpt/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWmass' , FatJetSDsubjetWmass_ ,  'FatJetSDsubjetWmass/F' )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau1'   , FatJetSDsubjetWtau1_   ,  'FatJetSDsubjetWtau1/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau2'   , FatJetSDsubjetWtau2_   ,  'FatJetSDsubjetWtau2/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau3'   , FatJetSDsubjetWtau3_   ,  'FatJetSDsubjetWtau3/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetWtau21'   , FatJetSDsubjetWtau21_   ,  'FatJetSDsubjetWtau21/F'   )

    if options.type == 'ttjets' :
        TTreeSemiLept.Branch('FatJetSDsubjet_isRealW'   , FatJetSDsubjet_isRealW_   ,  'FatJetSDsubjet_isRealW/F'   )
        TTreeSemiLept.Branch('FatJetSDsubjet_isFakeW'   , FatJetSDsubjet_isFakeW_   ,  'FatJetSDsubjet_isFakeW/F'   )

    TTreeSemiLept.Branch('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt_   ,  'FatJetSDsubjetBpt/F'   )
    TTreeSemiLept.Branch('FatJetSDsubjetBmass' , FatJetSDsubjetBmass_ ,  'FatJetSDsubjetBmass/F' )
    TTreeSemiLept.Branch('FatJetSDsubjetBbdisc' , FatJetSDsubjetBbdisc_ ,  'FatJetSDsubjetBbdisc/F' )

    TTreeSemiLept.Branch('LeptonType'          , LeptonType_          ,  'LeptonType/I'          )
    TTreeSemiLept.Branch('LeptonPt'            , LeptonPt_            ,  'LeptonPt/F'            )

    TTreeSemiLept.Branch('LeptonPtRel'         , LeptonPtRel_         ,  'LeptonPtRel/F'         )
    TTreeSemiLept.Branch('LeptonDRMin'         , LeptonDRMin_         ,  'LeptonDRMin/F'         ) 

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

    if options.type == 'data' :
        filesin = [ ROOT.TFile('./b2gttbar_ttrees/singleel_ttree_76x_v1p2_puppi.root'), 
                ROOT.TFile('./b2gttbar_ttrees/singlemu_ttree_76x_v1p2_puppi.root') ] 
    if options.type == 'ttjets' :
            filesin = [ROOT.TFile('./b2gttbar_ttrees/ttjets_ttree_76x_v1p2_puppi.root')]         


    # create list of trees to be combined
    alltrees = []

    for ji in filesin:
        alltrees.append(ji.Get("TreeSemiLept"))

    for ittree, ttree in enumerate(alltrees) :
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

            weightS = SemiLeptWeight[0]
            #if options.verbose : print "event weight is : " + str(weightS)

            fatmass_sd = FatJetMassSoftDrop[0]
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
            #print "W Jet tau 2 :" + str(tau2)
            W_tau3 = FatJetSDsubjetWtau3[0]
            #print "W Jet tau 3 :" + str(tau3)


            if W_tau1 > 0.001 :
                W_tau21 = W_tau2 / W_tau1
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


            fout.cd()
            SemiLeptWeight_      [0] = weightS

            FatJetRhoRatio_      [0] = Rhorat
            FatJetMass_          [0] = fatmass
            FatJetPt_            [0] = fatpt
            FatJetMassSoftDrop_  [0] = fatmass_sd
            FatJetPtSoftDrop_    [0] = fatpt_sd
            if (options.verbose and fatpt_sd > 350. ): 
                print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
                print "Fat Jet Pt SD : " + str(fatpt_sd)
                print "Fat Jet mass SD : " + str(fatmass_sd)
                print "Fat Jet Rho Ratio : " + str(Rhorat)
                print "-------------------------------------"

            FatJetTau1_          [0] = tau1
            FatJetTau2_          [0] = tau2
            FatJetTau3_          [0] = tau3
            FatJetTau32_         [0] = tau32
            FatJetTau21_         [0] = tau21

            FatJetSDsubjetWpt_   [0] = W_pt
            FatJetSDsubjetWmass_ [0] = W_m
            FatJetSDsubjetWtau1_ [0] = W_tau1
            FatJetSDsubjetWtau2_ [0] = W_tau2
            FatJetSDsubjetWtau3_ [0] = W_tau3
            FatJetSDsubjetWtau21_ [0] = W_tau21

            if options.type == 'ttjets' :
                FatJetSDsubjet_isRealW_ [0] = 0.0  # correct this once gen matching is implemented ???
                FatJetSDsubjet_isFakeW_ [0] = 0.0  # correct this once gen matching is implemented ???

            FatJetSDsubjetBpt_   [0] = B_pt 
            FatJetSDsubjetBmass_ [0] = B_m
            #FatJetSDsubjetBbdisc[0] = B_bdisc

            LeptonType_          [0] = lepton_Type
            LeptonPt_            [0] = lepton_pt
            LeptonPtRel_         [0] = lepton_ptRel
            LeptonDRMin_         [0] = lepton_DRmin

            SemiLepMETpt_        [0] = MET_pt

            SemiLeptRunNum_      [0] = runNum
            SemiLeptLumiBlock_   [0] = lumiBlock 
            SemiLeptEventNum_    [0] = eventNum

            TTreeSemiLept.Fill()


    fout.cd() 
    fout.Write()
    fout.Close()
    print "All Done. The "+ options.type +" TTrees were successfully combined!"
    print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
if __name__ == "__main__" :
    treeCombiner(sys.argv)
