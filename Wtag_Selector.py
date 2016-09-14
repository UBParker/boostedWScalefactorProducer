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

# This script reads several TTrees and writes combined trees into root files and well as a seperate output root file with the histograms of W candidate (SD subjet 0 from Semi-Leptonic TTbar selection) mass binned by the pt of the w candidate 

def Wtag_Selector(argv) : 
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

    parser.add_option('--80x', action='store_true',
                      default=True,
                      dest='is80x',
                      help='Are the ttrees produced using CMSSW 80X?')

    parser.add_option('--type', type='string', action='store',
                      dest='dtype',
                      default = '',
                      help='type of files to combine: data , ttjets, wjets (1-7) , st (1-2) and pseudodata (all MC combined)') 

    parser.add_option('--maxEvents', type='int', action='store',
                      dest='maxEvents',
                      default = None,
                      help='Max events')

    parser.add_option('--tau21Cut', type='float', action='store',
                      dest='tau21Cut',
                      default = 0.6,
                      help='Tau21 < tau21Cut')

    parser.add_option('--verbose', action='store_true',
                      default=False,
                      dest='verbose',
                      help='Do you want to print values of key variables?')

    parser.add_option('--match', action='store_true',
                      default=False,
                      dest='match',
                      help='Do you want to get the gen match info for the ttjets MC?')

    parser.add_option('--applyTheaCorr', action='store_true',
                      default=False,
                      dest='applyTheaCorr',
                      help='Do you want to apply SD mass corrections from Thea ???')

    parser.add_option('--Type2', action='store_true',
                      default=False,
                      dest='Type2',
                      help='Do you want to apply selection for type 2 tops as described in AN-16-215 ???')

    parser.add_option('--applyHIPCorr', action='store_true',
                      default=False,
                      dest='applyHIPCorr',
                      help='Do you want apply the HIP corrections to the muons ???')

    parser.add_option('--isMC', action='store_true',
                      default=False,
                      dest='isMC',
                      help='is it MC?')

    (options, args) = parser.parse_args(argv)
    argv = []

 #   print '===== Command line options ====='
 #   print options
 #   print '================================'

    import ROOT
    ROOT.gStyle.SetOptStat(0000000000)

    if options.isMC :
        c=ROOT.KalmanMuonCalibrator("MC_80X_13TeV")
    else :
        c=ROOT.KalmanMuonCalibrator("DATA_80X_13TeV")

    def getPUPPIweight(puppipt, puppieta) : #{

        finCor1 = ROOT.TFile.Open( "/home/amp/WJets/80xTrees/SimpleSelect/PuppiCorr/PuppiSoftdropMassCorr/weights/puppiCorr.root","READ")
        puppisd_corrGEN      = finCor1.Get("puppiJECcorr_gen")
        puppisd_corrRECO_cen = finCor1.Get("puppiJECcorr_reco_0eta1v3")
        puppisd_corrRECO_for = finCor1.Get("puppiJECcorr_reco_1v3eta2v5")
      
        genCorr  = 1.
        recoCorr = 1.
        totalWeight = 1.

        genCorr =  puppisd_corrGEN.Eval( puppipt )
        
        if (abs(puppieta) <=1.3 ): recoCorr = puppisd_corrRECO_cen.Eval(puppipt)
        if (abs(puppieta) > 1.3 ): recoCorr = puppisd_corrRECO_for.Eval(puppipt)
        totalWeight = genCorr * recoCorr
        return totalWeight
        #} 

    def getgsfTrackEffScaleFactor(eleta) : #{
        finSF = ROOT.TFile.Open( "/home/amp/WJets/80xTrees/SimpleSelect/egammaEffitxt_SF2D.root","READ")
        th2_EGamma_SF2D     = finSF.Get("EGamma_SF2D")
        gsfSF = EGamma_SF2D.Eval( eleta)
        return gsfSF
        #}  

    def getHIPMuonCorr(pt, eta phi, charge) : #{
        # apply HIP muon corrections as described here https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonScaleResolKalman
        if muCharge[i] < 0. :
            chargeSign = -1 
        if muCharge[i] > 0. :
            chargeSign = 1    
        corrMuPt = c.getCorrectedPt(pt, eta phi, charge)
        dpt = abs( pt- CorrMuPt )
        dptopt = dpt/ pt
        c.getCorrectedError(pt, eta, dptopt)#'Recall! This correction is only valid after smearing'
        c.smear(pt, eta)
        #print 'propagate the statistical error of the calibration
        #print 'first get number of parameters'
        N=c.getN()
        print N,'parameters'
        for i in range(0,N):
            c.vary(i,+1)
            print 'variation',i,'ptUp', c.getCorrectedPt(pt, eta phi, charge)
            c.vary(i,-1)
            print 'variation',i,'ptDwn', c.getCorrectedPt(pt, eta phi, charge)
        c.reset()
        #print 'propagate the closure error 
        c.varyClosure(chargeSign)
        newpt = c.getCorrectedPt(pt, eta phi, charge)
        print 'After closure shift pt={0:4.3f}'.format{newpt}
        return newpt
        #} 


        # Create output ROOT file to store ttree after selection-When selection is good, produce final ttrees with No wtag cuts for Roofit input
        if options.writetree :
            if options.is80x:
                fileout = './output80xselector/%s_afterSelection_80x_v1p2_puppi.root'%options.dtype
            else:
                print "Must add 76x functionality to use this option"
                
            fout = ROOT.TFile( fileout, "RECREATE") 

            fout.cd()

            TreeSemiLept = ROOT.TTree("TreeSemiLept", "TreeSemiLept")

            SemiLeptTrig        = array('i', [0]  )
            BoosttypE           = array('i', [0] )
            SemiLeptWeight      = array('f', [0.] )
            
            FatJetCorr          = array('f', [-1.])
            FatJetCorrUp        = array('f', [-1.])
            FatJetCorrDn        = array('f', [-1.])
            FatJetMassCorr      = array('f', [-1.])
            FatJetMassCorrUp    = array('f', [-1.])
            FatJetMassCorrDn    = array('f', [-1.])
            JetPtSmearFactor    = array('f', [-1.])
            JetPtSmearFactorUp  = array('f', [-1.])
            JetPtSmearFactorDn  = array('f', [-1.])
            JetEtaScaleFactor   = array('f', [-1.])
            JetPhiScaleFactor   = array('f', [-1.])
            JetMatchedGenJetPt  = array('f', [-1.])
            FatJetPtRaw         = array('f', [-1.])
            FatJetEtaRaw        = array('f', [-1.])
            FatJetPhiRaw        = array('f', [-1.])
            FatJetRapRaw        = array('f', [-1.])
            FatJetMassRaw       = array('f', [-1.])
            FatJetP             = array('f', [-1.])
            FatJetPt            = array('f', [-1.])
            FatJetEta           = array('f', [-1.])
            FatJetPhi           = array('f', [-1.])
            FatJetRap           = array('f', [-1.])
            FatJetEnergy        = array('f', [-1.])
            FatJetBDisc         = array('f', [-1.])
            FatJetttio      = array('f', [-1.])
            FatJetMass          = array('f', [-1.])
            FatJetMassSoftDrop  = array('f', [-1.])
            FatJetMassSDsumSubjetCorr        = array('f', [-1.] )
            FatJetMassSDsumSubjetRaw         = array('f', [-1.] )
            FatJetMassSDsumSubjetCorrUp      = array('f', [-1.] )
            FatJetMassSDsumSubjetCorrDn      = array('f', [-1.] )
            FatJetMassSDsumSubjetCorrSmear   = array('f', [-1.] )
            FatJetMassSDsumSubjetCorrSmearUp = array('f', [-1.] )
            FatJetMassSDsumSubjetCorrSmearDn = array('f', [-1.] )
            FatJetMassPruned    = array('f', [-1.])
            FatJetMassFiltered  = array('f', [-1.])
            FatJetMassTrimmed   = array('f', [-1.])
            FatJetTau1          = array('f', [-1.]) 
            FatJetTau2          = array('f', [-1.]) 
            FatJetTau3          = array('f', [-1.]) 
            FatJetTau32         = array('f', [-1.])
            FatJetTau21         = array('f', [-1.]) 
            FatJetSDnsubjets    = array('f', [-1.])
            FatJetSDbdiscW      = array('f', [-1.])
            FatJetSDbdiscB      = array('f', [-1.])
            FatJetSDmaxbdisc    = array('f', [-1.])
            FatJetSDsubjetWpt   = array('f', [-1.])
            FatJetSDsubjetWEta   = array('f', [-1.])
            FatJetSDsubjetWPhi   = array('f', [-1.])
            FatJetSDsubjetWptRaw   = array('f', [-1.])
            FatJetSDsubjetWmass = array('f', [-1.])
            FatJetSDsubjetWmassRaw = array('f', [-1.])
            FatJetSDsubjetWtau1 = array('f', [-1.])
            FatJetSDsubjetWtau2 = array('f', [-1.])
            FatJetSDsubjetWtau3 = array('f', [-1.])
            FatJetSDsubjetWtau21 = array('f', [-1.])
            FatJetSDsubjetWtau32 = array('f', [-1.])

            FatJetSDsubjetBpt   = array('f', [-1.])
            FatJetSDsubjetBmass = array('f', [-1.])
            FatJetSDsubjetBtau1 = array('f', [-1.])
            FatJetSDsubjetBtau2 = array('f', [-1.])
            FatJetSDsubjetBtau3 = array('f', [-1.])
            FatJetSDsubjetBtau21 = array('f', [-1.])
            FatJetSDsubjetBtau32 = array('f', [-1.])

            FatJetCMSmaxbdisc   = array('f', [-1.])
            FatJetCMSnsubjets   = array('f', [-1.])
            #FatJetCMSminMass    = array('f', [-1.])
            FatJetCMSm01        = array('f', [-1.])
            FatJetCMSm02        = array('f', [-1.])
            FatJetCMSm12        = array('f', [-1.])
            FatJetNHF           = array('f', [-1.])   
            FatJetCHF           = array('f', [-1.])   
            FatJetNEF           = array('f', [-1.])   
            FatJetCEF           = array('f', [-1.])   
            FatJetNC            = array('f', [-1.])   
            FatJetNCH           = array('f', [-1.])   
            FatJetSDsubjet0pt   = array('f', [-1.])   
            FatJetSDsubjet0mass = array('f', [-1.])   
            FatJetSDsubjet0area = array('f', [-1.])   
            FatJetSDsubjet0flav = array('f', [-1.])   
            FatJetSDsubjet1pt   = array('f', [-1.])   
            FatJetSDsubjet1mass = array('f', [-1.])   
            FatJetSDsubjet1area = array('f', [-1.])   
            FatJetSDsubjet1flav = array('f', [-1.])   
            BJet2bDisc           = array('f', [-1.])
            BJet2Pt              = array('f', [-1.])
            BJet2Eta             = array('f', [-1.])
            BJet2Phi             = array('f', [-1.])
            BJet2Mass            = array('f', [-1.])
            Type2PairMass       = array('f', [-1.])
            Type2PairPt         = array('f', [-1.])
            DeltaRLepFat        = array('f', [-1.])
            DeltaRAK4AK8        = array('f', [-1.])

            LeptonType          = array('i', [-1])
            LeptonPt            = array('f', [-1.])
            LeptonEta           = array('f', [-1.])
            LeptonPhi           = array('f', [-1.])
            LeptonPx            = array('f', [-1.])
            LeptonPy            = array('f', [-1.])
            LeptonPz            = array('f', [-1.])
            LeptonEnergy        = array('f', [-1.])
            LeptonIso           = array('f', [-1.])
            LeptonPtRel         = array('f', [-1.])
            LeptonDRMin         = array('f', [-1.])

            SemiLepMETpx        = array('f', [-1.])
            SemiLepMETpy        = array('f', [-1.])
            SemiLepMETpt        = array('f', [-1.])
            SemiLepMETphi       = array('f', [-1.])
            SemiLepNvtx         = array('f', [-1.])
            SemiLepEventWeight  = array('f', [-1.])

            SemilLepTTmass      = array('f', [-1.])
            DeltaPhiLepFat      = array('f', [-1.]) 
            DeltaRLepFat        = array('f', [-1.]) 
            DeltaRAK4AK8        = array('f', [-1.]) 
     
            AK4bDisc            = array('f', [-1.])
            NearestAK4JetPt     = array('f', [-1.])
            NearestAK4JetEta    = array('f', [-1.])
            NearestAK4JetPhi    = array('f', [-1.])
            NearestAK4JetMass   = array('f', [-1.])
            PU_CorrDn           = array('f', [-1.])
            PU_CorrUp           = array('f', [-1.])

            SemiLeptRunNum        = array('f', [-1.])   
            SemiLeptLumiBlock     = array('f', [-1.])   
            SemiLeptEventNum      = array('f', [-1.]) 

            NearestAK4JetMass   = array('f', [-1.])
            PU_CorrDn           = array('f', [-1.])
            PU_CorrUp           = array('f', [-1.])
            
            TreeSemiLept.Branch('SemiLeptTrig'        , SemiLeptTrig        ,  'SemiLeptTrig/I'        )
            TreeSemiLept.Branch('SemiLeptWeight'      , SemiLeptWeight      ,  'SemiLeptWeight/F'      )    
            TreeSemiLept.Branch('BoosttypE'           , BoosttypE           ,  'BoosttypE/I'           )
            TreeSemiLept.Branch('FatJetCorr'          , FatJetCorr          ,  'FatJetCorr/F'          )
            TreeSemiLept.Branch('FatJetCorrUp'        , FatJetCorrUp        ,  'FatJetCorrUp/F'        )
            TreeSemiLept.Branch('FatJetCorrDn'        , FatJetCorrDn        ,  'FatJetCorrDn/F'        )
            TreeSemiLept.Branch('FatJetMassCorr'          , FatJetMassCorr          ,  'FatJetMassCorr/F'          )
            TreeSemiLept.Branch('FatJetMassCorrUp'        , FatJetMassCorrUp        ,  'FatJetMassCorrUp/F'        )
            TreeSemiLept.Branch('FatJetMassCorrDn'        , FatJetMassCorrDn        ,  'FatJetMassCorrDn/F'        )
            TreeSemiLept.Branch('JetPtSmearFactor'  , JetPtSmearFactor   , 'JetPtSmearFactor/F'   ) 
            TreeSemiLept.Branch('JetPtSmearFactorUp', JetPtSmearFactorUp , 'JetPtSmearFactorUp/F' ) 
            TreeSemiLept.Branch('JetPtSmearFactorDn', JetPtSmearFactorDn , 'JetPtSmearFactorDn/F' ) 
            TreeSemiLept.Branch('JetEtaScaleFactor' , JetEtaScaleFactor  , 'JetEtaScaleFactor/F'  ) 
            TreeSemiLept.Branch('JetPhiScaleFactor' , JetPhiScaleFactor  , 'JetPhiScaleFactor/F'  ) 
            TreeSemiLept.Branch('JetMatchedGenJetPt', JetMatchedGenJetPt , 'JetMatchedGenJetPt/F' ) 
            TreeSemiLept.Branch('FatJetPtRaw'          , FatJetPtRaw           , 'FatJetPtRaw/F'           )
            TreeSemiLept.Branch('FatJetEtaRaw'         , FatJetEtaRaw          , 'FatJetEtaRaw/F'          ) 
            TreeSemiLept.Branch('FatJetPhiRaw'         , FatJetPhiRaw          , 'FatJetPhiRaw/F'          ) 
            TreeSemiLept.Branch('FatJetRapRaw'         , FatJetRapRaw          , 'FatJetRapRaw/F'          ) 
            TreeSemiLept.Branch('FatJetMassRaw'        , FatJetMassRaw         , 'FatJetMassRaw/F'         ) 
            TreeSemiLept.Branch('FatJetP'             , FatJetP             ,  'FatJetP/F'             )
            TreeSemiLept.Branch('FatJetPt'            , FatJetPt            ,  'FatJetPt/F'            )
            TreeSemiLept.Branch('FatJetEta'           , FatJetEta           ,  'FatJetEta/F'           )
            TreeSemiLept.Branch('FatJetPhi'           , FatJetPhi           ,  'FatJetPhi/F'           )
            TreeSemiLept.Branch('FatJetRap'           , FatJetRap           ,  'FatJetRap/F'           )
            TreeSemiLept.Branch('FatJetEnergy'        , FatJetEnergy        ,  'FatJetEnergy/F'        )
            TreeSemiLept.Branch('FatJetBDisc'         , FatJetBDisc         ,  'FatJetBDisc/F'         )
            TreeSemiLept.Branch('FatJetRhoRatio'      , FatJetRhoRatio      ,  'FatJetRhoRatio/F'      )
            TreeSemiLept.Branch('FatJetMass'          , FatJetMass          ,  'FatJetMass/F'          )
            TreeSemiLept.Branch('FatJetMassSoftDrop'  , FatJetMassSoftDrop  ,  'FatJetMassSoftDrop/F'  )
            TreeSemiLept.Branch('FatJetMassSDsumSubjetCorr'        , FatJetMassSDsumSubjetCorr         , 'FatJetMassSDsumSubjetCorr/F'        )   
            TreeSemiLept.Branch('FatJetMassSDsumSubjetRaw'         , FatJetMassSDsumSubjetRaw          , 'FatJetMassSDsumSubjetRaw/F'         )   
            TreeSemiLept.Branch('FatJetMassSDsumSubjetCorrUp'      , FatJetMassSDsumSubjetCorrUp       , 'FatJetMassSDsumSubjetCorrUp/F'      )   
            TreeSemiLept.Branch('FatJetMassSDsumSubjetCorrDn'      , FatJetMassSDsumSubjetCorrDn       , 'FatJetMassSDsumSubjetCorrDn/F'      )   
            TreeSemiLept.Branch('FatJetMassSDsumSubjetCorrSmear'   , FatJetMassSDsumSubjetCorrSmear    , 'FatJetMassSDsumSubjetCorrSmear/F'   )   
            TreeSemiLept.Branch('FatJetMassSDsumSubjetCorrSmearUp' , FatJetMassSDsumSubjetCorrSmearUp  , 'FatJetMassSDsumSubjetCorrSmearUp/F' )   
            TreeSemiLept.Branch('FatJetMassSDsumSubjetCorrSmearDn' , FatJetMassSDsumSubjetCorrSmearDn  , 'FatJetMassSDsumSubjetCorrSmearDn/F' )   
            TreeSemiLept.Branch('FatJetMassPruned'    , FatJetMassPruned    ,  'FatJetMassPruned/F'    )
            TreeSemiLept.Branch('FatJetMassFiltered'  , FatJetMassFiltered  ,  'FatJetMassFiltered/F'  )
            TreeSemiLept.Branch('FatJetMassTrimmed'   , FatJetMassTrimmed   ,  'FatJetMassTrimmed/F'   )
            TreeSemiLept.Branch('FatJetTau1'          , FatJetTau1          ,  'FatJetTau1/F'          )
            TreeSemiLept.Branch('FatJetTau2'          , FatJetTau2          ,  'FatJetTau2/F'          )
            TreeSemiLept.Branch('FatJetTau3'          , FatJetTau3          ,  'FatJetTau3/F'          )
            TreeSemiLept.Branch('FatJetTau32'         , FatJetTau32         ,  'FatJetTau32/F'         )
            TreeSemiLept.Branch('FatJetTau21'         , FatJetTau21         ,  'FatJetTau21/F'         )
            TreeSemiLept.Branch('FatJetSDnsubjets'    , FatJetSDnsubjets    ,  'FatJetSDnsubjets/F'    )
            TreeSemiLept.Branch('FatJetSDbdiscW'      , FatJetSDbdiscW      ,  'FatJetSDbdiscW/F'      )
            TreeSemiLept.Branch('FatJetSDbdiscB'      , FatJetSDbdiscB      ,  'FatJetSDbdiscB/F'      )
            TreeSemiLept.Branch('FatJetSDmaxbdisc'    , FatJetSDmaxbdisc    ,  'FatJetSDmaxbdisc/F'    )
            TreeSemiLept.Branch('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt   ,  'FatJetSDsubjetWpt/F'   )
            TreeSemiLept.Branch('FatJetSDsubjetWPhi'   , FatJetSDsubjetWPhi   ,  'FatJetSDsubjetWPhi/F'   )
            TreeSemiLept.Branch('FatJetSDsubjetWEta'   , FatJetSDsubjetWEta   ,  'FatJetSDsubjetWEta/F'   )
            TreeSemiLept.Branch('FatJetSDsubjetWptRaw'   , FatJetSDsubjetWptRaw   ,  'FatJetSDsubjetWptRaw/F'   )
            TreeSemiLept.Branch('FatJetSDsubjetWmass' , FatJetSDsubjetWmass ,  'FatJetSDsubjetWmass/F' )
            TreeSemiLept.Branch('FatJetSDsubjetWmassRaw' , FatJetSDsubjetWmassRaw ,  'FatJetSDsubjetWmassRaw/F' )
            TreeSemiLept.Branch('FatJetSDsubjetWtau1' , FatJetSDsubjetWtau1 ,  'FatJetSDsubjetWtau1/F' )
            TreeSemiLept.Branch('FatJetSDsubjetWtau2' , FatJetSDsubjetWtau2 ,  'FatJetSDsubjetWtau2/F' )
            TreeSemiLept.Branch('FatJetSDsubjetWtau3' , FatJetSDsubjetWtau3 ,  'FatJetSDsubjetWtau3/F' )
            TreeSemiLept.Branch('FatJetSDsubjetWtau21' , FatJetSDsubjetWtau21 ,  'FatJetSDsubjetWtau21/F' )
            TreeSemiLept.Branch('FatJetSDsubjetWtau32' , FatJetSDsubjetWtau32 ,  'FatJetSDsubjetWtau32/F' )
            TreeSemiLept.Branch('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt   ,  'FatJetSDsubjetBpt/F'   )
            TreeSemiLept.Branch('FatJetSDsubjetBmass' , FatJetSDsubjetBmass ,  'FatJetSDsubjetBmass/F' )
            TreeSemiLept.Branch('FatJetSDsubjetBtau1' , FatJetSDsubjetBtau1 ,  'FatJetSDsubjetBtau1/F' )
            TreeSemiLept.Branch('FatJetSDsubjetBtau2' , FatJetSDsubjetBtau2 ,  'FatJetSDsubjetBtau2/F' )
            TreeSemiLept.Branch('FatJetSDsubjetBtau3' , FatJetSDsubjetBtau3 ,  'FatJetSDsubjetBtau3/F' )
            TreeSemiLept.Branch('FatJetSDsubjetBtau21' , FatJetSDsubjetBtau21 ,  'FatJetSDsubjetBtau21/F' )
            TreeSemiLept.Branch('FatJetSDsubjetBtau32' , FatJetSDsubjetBtau32 ,  'FatJetSDsubjetBtau32/F' )
            TreeSemiLept.Branch('FatJetSDsubjet0pt'   , FatJetSDsubjet0pt   ,  'FatJetSDsubjet0pt/F'   ) 
            TreeSemiLept.Branch('FatJetSDsubjet0mass' , FatJetSDsubjet0mass ,  'FatJetSDsubjet0mass/F' ) 
            TreeSemiLept.Branch('FatJetSDsubjet0area' , FatJetSDsubjet0area ,  'FatJetSDsubjet0area/F' ) 
            TreeSemiLept.Branch('FatJetSDsubjet0flav' , FatJetSDsubjet0flav ,  'FatJetSDsubjet0flav/F' ) 
            TreeSemiLept.Branch('FatJetSDsubjet1pt'   , FatJetSDsubjet1pt   ,  'FatJetSDsubjet1pt/F'   ) 
            TreeSemiLept.Branch('FatJetSDsubjet1mass' , FatJetSDsubjet1mass ,  'FatJetSDsubjet1mass/F' ) 
            TreeSemiLept.Branch('FatJetSDsubjet1area' , FatJetSDsubjet1area ,  'FatJetSDsubjet1area/F' ) 
            TreeSemiLept.Branch('FatJetSDsubjet1flav' , FatJetSDsubjet1flav ,  'FatJetSDsubjet1flav/F' ) 
            TreeSemiLept.Branch('FatJetCMSmaxbdisc'   , FatJetCMSmaxbdisc   ,  'FatJetCMSmaxbdisc/F'   )
            TreeSemiLept.Branch('FatJetCMSnsubjets'   , FatJetCMSnsubjets   ,  'FatJetCMSnsubjets/F'   )
            #TreeSemiLept.Branch('FatJetCMSminMass'    , FatJetCMSminMass    ,  'FatJetCMSminMass/F'    )
            TreeSemiLept.Branch('FatJetCMSm01'        , FatJetCMSm01        ,  'FatJetCMSm01/F'        )
            TreeSemiLept.Branch('FatJetCMSm02'        , FatJetCMSm02        ,  'FatJetCMSm02/F'        )
            TreeSemiLept.Branch('FatJetCMSm12'        , FatJetCMSm12        ,  'FatJetCMSm12/F'        )
            TreeSemiLept.Branch('FatJetNHF'           , FatJetNHF           ,  'FatJetNHF/F'           )  
            TreeSemiLept.Branch('FatJetCHF'           , FatJetCHF           ,  'FatJetCHF/F'           )  
            TreeSemiLept.Branch('FatJetNEF'           , FatJetNEF           ,  'FatJetNEF/F'           )  
            TreeSemiLept.Branch('FatJetCEF'           , FatJetCEF           ,  'FatJetCEF/F'           )  
            TreeSemiLept.Branch('FatJetNC'            , FatJetNC            ,  'FatJetNC/F'            ) 
            TreeSemiLept.Branch('FatJetNCH'           , FatJetNCH           ,  'FatJetNCH/F'           )    
            TreeSemiLept.Branch('BJet2bDisc'           , BJet2bDisc           ,  'BJet2bDisc/F'           )
            TreeSemiLept.Branch('BJet2Pt'              , BJet2Pt              ,  'BJet2Pt/F'              )
            TreeSemiLept.Branch('BJet2Eta'             , BJet2Eta             ,  'BJet2Eta/F'             )
            TreeSemiLept.Branch('BJet2Phi'             , BJet2Phi             ,  'BJet2Phi/F'             )
            TreeSemiLept.Branch('BJet2Mass'            , BJet2Mass            ,  'BJet2Mass/F'            )
            TreeSemiLept.Branch('Type2PairMass'       , Type2PairMass       ,  'Type2PairMass/F'       )
            TreeSemiLept.Branch('Type2PairPt'         , Type2PairPt         ,  'Type2PairPt/F'         )
            TreeSemiLept.Branch('LeptonType'          , LeptonType          ,  'LeptonType/I'          )
            TreeSemiLept.Branch('LeptonPt'            , LeptonPt            ,  'LeptonPt/F'            )
            TreeSemiLept.Branch('LeptonEta'           , LeptonEta           ,  'LeptonEta/F'           )
            TreeSemiLept.Branch('LeptonPhi'           , LeptonPhi           ,  'LeptonPhi/F'           )
            TreeSemiLept.Branch('LeptonPx'            , LeptonPx            ,  'LeptonPx/F'            )
            TreeSemiLept.Branch('LeptonPy'            , LeptonPy            ,  'LeptonPy/F'            )
            TreeSemiLept.Branch('LeptonPz'            , LeptonPz            ,  'LeptonPz/F'            )
            TreeSemiLept.Branch('LeptonEnergy'        , LeptonEnergy        ,  'LeptonEnergy/F'        )
            TreeSemiLept.Branch('LeptonIso'           , LeptonIso           ,  'LeptonIso/F'           )
            TreeSemiLept.Branch('LeptonPtRel'         , LeptonPtRel         ,  'LeptonPtRel/F'         )
            TreeSemiLept.Branch('LeptonDRMin'         , LeptonDRMin         ,  'LeptonDRMin/F'         )        
            TreeSemiLept.Branch('SemiLepMETpx'        , SemiLepMETpx        ,  'SemiLepMETpx/F'        )
            TreeSemiLept.Branch('SemiLepMETpy'        , SemiLepMETpy        ,  'SemiLepMETpy/F'        )
            TreeSemiLept.Branch('SemiLepMETpt'        , SemiLepMETpt        ,  'SemiLepMETpt/F'        )
            TreeSemiLept.Branch('SemiLepMETphi'       , SemiLepMETphi       ,  'SemiLepMETphi/F'       )
            TreeSemiLept.Branch('SemiLepNvtx'         , SemiLepNvtx         ,  'SemiLepNvtx/F'         )
            TreeSemiLept.Branch('SemiLepEventWeight'  , SemiLepEventWeight  ,  'SemiLepEventWeight/F'  )
            TreeSemiLept.Branch('SemilLepTTmass'      , SemilLepTTmass      ,  'SemilLepTTmass/F'      )
            TreeSemiLept.Branch('DeltaPhiLepFat'      , DeltaPhiLepFat      ,  'DeltaPhiLepFat/F'      )
            TreeSemiLept.Branch('DeltaRLepFat'        , DeltaRLepFat        ,  'DeltaRLepFat/F'        )
            TreeSemiLept.Branch('DeltaRAK4AK8'        , DeltaRAK4AK8        ,  'DeltaRAK4AK8/F'        )
            TreeSemiLept.Branch('AK4bDisc'            ,AK4bDisc             ,  'AK4bDisc/F'            )
            TreeSemiLept.Branch('NearestAK4JetPt'     ,NearestAK4JetPt      ,  'NearestAK4JetPt/F'     )
            TreeSemiLept.Branch('NearestAK4JetEta'    ,NearestAK4JetEta     ,  'NearestAK4JetEta/F'    )
            TreeSemiLept.Branch('NearestAK4JetPhi'    ,NearestAK4JetPhi     ,  'NearestAK4JetPhi/F'    )

            TreeSemiLept.Branch('NearestAK4JetMass' ,  NearestAK4JetMass    ,  'NearestAK4JetMass/F'   )
            TreeSemiLept.Branch('PU_CorrDn'         ,  PU_CorrDn            ,  'PU_CorrDn/F'           )
            TreeSemiLept.Branch('PU_CorrUp'         ,  PU_CorrUp            ,  'PU_CorrUp/F'           )
       
            TreeSemiLept.Branch('SemiLeptRunNum'         ,  SemiLeptRunNum       ,  'SemiLeptRunNum/F'          )
            TreeSemiLept.Branch('SemiLeptLumiBlock'      ,  SemiLeptLumiBlock    ,  'SemiLeptLumiBlock/F'       ) 
            TreeSemiLept.Branch('SemiLeptEventNum'       ,  SemiLeptEventNum     ,  'SemiLeptEventNum/F'        )


        if options.is80x :  
            fout= ROOT.TFile('./output80xselector/histos_80x_' + options.filestr + '.root', "RECREATE")
            filein =  './output80xselector/%s_combinedttree_80x_v1p2_puppi.root'%options.dtype


    binlimit = 200.
    numbins = 300

    if options.dtype == 'data':#FIX THIS see wjets1 and wjets2
        h_mWsubjet_ElData = ROOT.TH1F("h_mWsubjet_ElData", "; ;  ", numbins, 0, binlimit)
        h_ptWsubjet_ElData = ROOT.TH1F("h_ptWsubjet_ElData", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)
        h_mWsubjet_b1_ElData  = ROOT.TH1F("h_mWsubjet_b1_ElData", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_ElData  = ROOT.TH1F("h_mWsubjet_b2_ElData", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_ElData  = ROOT.TH1F("h_mWsubjet_b3_ElData", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_ElData  = ROOT.TH1F("h_mWsubjet_b4_ElData", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_ElDatap = ROOT.TH1F("h_mWsubjet_ElDatap", "; ;  ", numbins, 0, binlimit)
        h_ptWsubjet_ElDatap = ROOT.TH1F("h_ptWsubjet_ElDatap", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)
        h_mWsubjet_b1_ElDatap  = ROOT.TH1F("h_mWsubjet_b1_ElDatap", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_ElDatap  = ROOT.TH1F("h_mWsubjet_b2_ElDatap", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_ElDatap  = ROOT.TH1F("h_mWsubjet_b3_ElDatap", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_ElDatap  = ROOT.TH1F("h_mWsubjet_b4_ElDatap", "; ;  ", numbins, 0, binlimit)

        h_mWsubjet_MuData = ROOT.TH1F("h_mWsubjet_MuData", "; ;  ", numbins, 0, binlimit)
        h_ptWsubjet_MuData = ROOT.TH1F("h_ptWsubjet_MuData", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)
        h_mWsubjet_b1_MuData  = ROOT.TH1F("h_mWsubjet_b1_MuData", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_MuData  = ROOT.TH1F("h_mWsubjet_b2_MuData", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_MuData  = ROOT.TH1F("h_mWsubjet_b3_MuData", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_MuData  = ROOT.TH1F("h_mWsubjet_b4_MuData", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_MuDatap = ROOT.TH1F("h_mWsubjet_MuDatap", "; ;  ", numbins, 0, binlimit)
        h_ptWsubjet_MuDatap = ROOT.TH1F("h_ptWsubjet_MuDatap", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)
        h_mWsubjet_b1_MuDatap  = ROOT.TH1F("h_mWsubjet_b1_MuDatap", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_MuDatap  = ROOT.TH1F("h_mWsubjet_b2_MuDatap", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_MuDatap  = ROOT.TH1F("h_mWsubjet_b3_MuDatap", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_MuDatap  = ROOT.TH1F("h_mWsubjet_b4_MuDatap", "; ;  ", numbins, 0, binlimit)

        h_mWsubjet_Data = ROOT.TH1F("h_mWsubjet_Data", "; ;  ", numbins, 0, binlimit)
        h_ptWsubjet_Data = ROOT.TH1F("h_ptWsubjet_Data", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)
        h_mWsubjet_b1_Data  = ROOT.TH1F("h_mWsubjet_b1_Data", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_Data  = ROOT.TH1F("h_mWsubjet_b2_Data", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_Data  = ROOT.TH1F("h_mWsubjet_b3_Data", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_Data  = ROOT.TH1F("h_mWsubjet_b4_Data", "; ;  ", numbins, 0, binlimit)
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
        h_mWjet_Datap = ROOT.TH1F("h_mWjet_Datap", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_ptWjet_Datap = ROOT.TH1F("h_ptWjet_Datap", ";P_{T} SD jet0 (GeV);  ", 1300, 0, 1300)
        h_mWjet_b1_Datap  = ROOT.TH1F("h_mWjet_b1_Datap", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b2_Datap  = ROOT.TH1F("h_mWjet_b2_Datap", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b3_Datap  = ROOT.TH1F("h_mWjet_b3_Datap", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b4_Datap  = ROOT.TH1F("h_mWjet_b4_Datap", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)


        h_mWjet_ElData = ROOT.TH1F("h_mWjet_ElData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_ptWjet_ElData = ROOT.TH1F("h_ptWjet_ElData", ";P_{T} SD jet0 (GeV);  ", 1300, 0, 1300)
        h_mWjet_b1_ElData  = ROOT.TH1F("h_mWjet_b1_ElData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b2_ElData  = ROOT.TH1F("h_mWjet_b2_ElData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b3_ElData  = ROOT.TH1F("h_mWjet_b3_ElData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b4_ElData  = ROOT.TH1F("h_mWjet_b4_ElData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)

        h_mWjet_MuData = ROOT.TH1F("h_mWjet_MuData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_ptWjet_MuData = ROOT.TH1F("h_ptWjet_MuData", ";P_{T} SD jet0 (GeV);  ", 1300, 0, 1300)
        h_mWjet_b1_MuData  = ROOT.TH1F("h_mWjet_b1_MuData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b2_MuData  = ROOT.TH1F("h_mWjet_b2_MuData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b3_MuData  = ROOT.TH1F("h_mWjet_b3_MuData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b4_MuData  = ROOT.TH1F("h_mWjet_b4_MuData", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
    if options.dtype == 'ttjets': #FIX THIS see wjets1 and wjets2
        h_mWsubjet_ttjets = ROOT.TH1F("h_mWsubjet_ttjets", "; ; ", numbins, 0, binlimit)
        h_ptWsubjet_ttjets = ROOT.TH1F("h_ptWsubjet_ttjets", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)
        h_mWsubjet_b1_ttjets  = ROOT.TH1F("h_mWsubjet_b1_ttjets", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_ttjets  = ROOT.TH1F("h_mWsubjet_b2_ttjets", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_ttjets  = ROOT.TH1F("h_mWsubjet_b3_ttjets", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_ttjets  = ROOT.TH1F("h_mWsubjet_b4_ttjets", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_ttjetsp = ROOT.TH1F("h_mWsubjet_ttjetsp", "; ;  ", numbins, 0, binlimit)
        h_ptWsubjet_ttjetsp = ROOT.TH1F("h_ptWsubjet_ttjetsp", ";P_{T} SD subjet0 (GeV);  ", 1300, 0, 1300)
        h_mWsubjet_b1_ttjetsp  = ROOT.TH1F("h_mWsubjet_b1_ttjetsp", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_ttjetsp  = ROOT.TH1F("h_mWsubjet_b2_ttjetsp", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_ttjetsp  = ROOT.TH1F("h_mWsubjet_b3_ttjetsp", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_ttjetsp  = ROOT.TH1F("h_mWsubjet_b4_ttjetsp", "; ;  ", numbins, 0, binlimit)
        h_mWjet_ttjets = ROOT.TH1F("h_mWjet_ttjets", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)

        h_ptWjet_ttjets = ROOT.TH1F("h_ptWjet_ttjets", ";P_{T} SD jet0 (GeV);  ", 1300, 0, 1300)
        h_mWjet_b1_ttjets  = ROOT.TH1F("h_mWjet_b1_ttjets", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b2_ttjets  = ROOT.TH1F("h_mWjet_b2_ttjets", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b3_ttjets  = ROOT.TH1F("h_mWjet_b3_ttjets", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b4_ttjets  = ROOT.TH1F("h_mWjet_b4_ttjets", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_ttjetsp = ROOT.TH1F("h_mWjet_ttjetsp", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_ptWjet_ttjetsp = ROOT.TH1F("h_ptWjet_ttjetsp", ";P_{T} SD jet0 (GeV);  ", 1300, 0, 1300)
        h_mWjet_b1_ttjetsp  = ROOT.TH1F("h_mWjet_b1_ttjetsp", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b2_ttjetsp  = ROOT.TH1F("h_mWjet_b2_ttjetsp", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b3_ttjetsp  = ROOT.TH1F("h_mWjet_b3_ttjetsp", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)
        h_mWjet_b4_ttjetsp  = ROOT.TH1F("h_mWjet_b4_ttjetsp", ";m_{SD jet0} (GeV);  ", numbins, 0, binlimit)    


    if options.dtype == 'wjets1':
        if options.Type2:
            h_mWsubjet_b1_wjets1  = ROOT.TH1F("h_mWjet_b1_wjets1", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b2_wjets1  = ROOT.TH1F("h_mWjet_b2_wjets1", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b3_wjets1  = ROOT.TH1F("h_mWjet_b3_wjets1", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b4_wjets1  = ROOT.TH1F("h_mWjet_b4_wjets1", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b1_wjetsp1  = ROOT.TH1F("h_mWjet_b1_wjetsp1", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b2_wjetsp1  = ROOT.TH1F("h_mWjet_b2_wjetsp1", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b3_wjetsp1  = ROOT.TH1F("h_mWjet_b3_wjetsp1", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b4_wjetsp1  = ROOT.TH1F("h_mWsubjet_b4_wjetsp1", "; ;  ", numbins, 0, binlimit)
        else :
            h_mWsubjet_b1_wjets1  = ROOT.TH1F("h_mWsubjet_b1_wjets1", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b2_wjets1  = ROOT.TH1F("h_mWsubjet_b2_wjets1", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b3_wjets1  = ROOT.TH1F("h_mWsubjet_b3_wjets1", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b4_wjets1  = ROOT.TH1F("h_mWsubjet_b4_wjets1", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b1_wjetsp1  = ROOT.TH1F("h_mWsubjet_b1_wjetsp1", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b2_wjetsp1  = ROOT.TH1F("h_mWsubjet_b2_wjetsp1", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b3_wjetsp1  = ROOT.TH1F("h_mWsubjet_b3_wjetsp1", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b4_wjetsp1  = ROOT.TH1F("h_mWsubjet_b4_wjetsp1", "; ;  ", numbins, 0, binlimit)

    if options.dtype == 'wjets2':
        if options.Type2:
            h_mWsubjet_b1_wjets2  = ROOT.TH1F("h_mWjet_b1_wjets2", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b2_wjets2  = ROOT.TH1F("h_mWjet_b2_wjets2", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b3_wjets2  = ROOT.TH1F("h_mWjet_b3_wjets2", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b4_wjets2  = ROOT.TH1F("h_mWjet_b4_wjets2", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b1_wjetsp2  = ROOT.TH1F("h_mWjet_b1_wjetsp2", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b2_wjetsp2  = ROOT.TH1F("h_mWjet_b2_wjetsp2", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b3_wjetsp2  = ROOT.TH1F("h_mWjet_b3_wjetsp2", "; ;  ", numbins, 0, binlimit)
            h_mWjet_b4_wjetsp2  = ROOT.TH1F("h_mWsubjet_b4_wjetsp2", "; ;  ", numbins, 0, binlimit)
        else :
            h_mWsubjet_b1_wjets2  = ROOT.TH1F("h_mWsubjet_b1_wjets2", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b2_wjets2  = ROOT.TH1F("h_mWsubjet_b2_wjets2", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b3_wjets2  = ROOT.TH1F("h_mWsubjet_b3_wjets2", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b4_wjets2  = ROOT.TH1F("h_mWsubjet_b4_wjets2", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b1_wjetsp2  = ROOT.TH1F("h_mWsubjet_b1_wjetsp2", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b2_wjetsp2  = ROOT.TH1F("h_mWsubjet_b2_wjetsp2", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b3_wjetsp2  = ROOT.TH1F("h_mWsubjet_b3_wjetsp2", "; ;  ", numbins, 0, binlimit)
            h_mWsubjet_b4_wjetsp2  = ROOT.TH1F("h_mWsubjet_b4_wjetsp2", "; ;  ", numbins, 0, binlimit)
    if options.dtype == 'wjets3': #FIX THIS see wjets1 and wjets2
        h_mWsubjet_b1_wjets3  = ROOT.TH1F("h_mWsubjet_b1_wjets3", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_wjets3  = ROOT.TH1F("h_mWsubjet_b2_wjets3", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_wjets3  = ROOT.TH1F("h_mWsubjet_b3_wjets3", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_wjets3  = ROOT.TH1F("h_mWsubjet_b4_wjets3", "; ;  ", numbins, 0, binlimit)

        h_mWsubjet_b1_wjetsp3  = ROOT.TH1F("h_mWsubjet_b1_wjetsp3", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_wjetsp3  = ROOT.TH1F("h_mWsubjet_b2_wjetsp3", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_wjetsp3  = ROOT.TH1F("h_mWsubjet_b3_wjetsp3", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_wjetsp3  = ROOT.TH1F("h_mWsubjet_b4_wjetsp3", "; ;  ", numbins, 0, binlimit)
    if options.dtype == 'wjets4':#FIX THIS see wjets1 and wjets2
        h_mWsubjet_b1_wjets4  = ROOT.TH1F("h_mWsubjet_b1_wjets4", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_wjets4  = ROOT.TH1F("h_mWsubjet_b2_wjets4", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_wjets4  = ROOT.TH1F("h_mWsubjet_b3_wjets4", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_wjets4  = ROOT.TH1F("h_mWsubjet_b4_wjets4", "; ;  ", numbins, 0, binlimit)

        h_mWsubjet_b1_wjetsp4  = ROOT.TH1F("h_mWsubjet_b1_wjetsp4", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_wjetsp4  = ROOT.TH1F("h_mWsubjet_b2_wjetsp4", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_wjetsp4  = ROOT.TH1F("h_mWsubjet_b3_wjetsp4", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_wjetsp4  = ROOT.TH1F("h_mWsubjet_b4_wjetsp4", "; ;  ", numbins, 0, binlimit)
    if options.dtype == 'wjets5':#FIX THIS see wjets1 and wjets2
        h_mWsubjet_b1_wjets5  = ROOT.TH1F("h_mWsubjet_b1_wjets5", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_wjets5  = ROOT.TH1F("h_mWsubjet_b2_wjets5", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_wjets5  = ROOT.TH1F("h_mWsubjet_b3_wjets5", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_wjets5  = ROOT.TH1F("h_mWsubjet_b4_wjets5", "; ;  ", numbins, 0, binlimit)

        h_mWsubjet_b1_wjetsp5  = ROOT.TH1F("h_mWsubjet_b1_wjetsp5", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_wjetsp5  = ROOT.TH1F("h_mWsubjet_b2_wjetsp5", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_wjetsp5  = ROOT.TH1F("h_mWsubjet_b3_wjetsp5", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_wjetsp5  = ROOT.TH1F("h_mWsubjet_b4_wjetsp5", "; ;  ", numbins, 0, binlimit)
    if options.dtype == 'wjets6':#FIX THIS see wjets1 and wjets2
        h_mWsubjet_b1_wjets6  = ROOT.TH1F("h_mWsubjet_b1_wjets6", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_wjets6  = ROOT.TH1F("h_mWsubjet_b2_wjets6", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_wjets6  = ROOT.TH1F("h_mWsubjet_b3_wjets6", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_wjets6  = ROOT.TH1F("h_mWsubjet_b4_wjets6", "; ;  ", numbins, 0, binlimit)

        h_mWsubjet_b1_wjetsp6  = ROOT.TH1F("h_mWsubjet_b1_wjetsp6", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_wjetsp6  = ROOT.TH1F("h_mWsubjet_b2_wjetsp6", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_wjetsp6  = ROOT.TH1F("h_mWsubjet_b3_wjetsp6", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_wjetsp6  = ROOT.TH1F("h_mWsubjet_b4_wjetsp6", "; ;  ", numbins, 0, binlimit)
    if options.dtype == 'wjets7':#FIX THIS see wjets1 and wjets2
        h_mWsubjet_b1_wjets7  = ROOT.TH1F("h_mWsubjet_b1_wjets7", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_wjets7  = ROOT.TH1F("h_mWsubjet_b2_wjets7", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_wjets7  = ROOT.TH1F("h_mWsubjet_b3_wjets7", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_wjets7  = ROOT.TH1F("h_mWsubjet_b4_wjets7", "; ;  ", numbins, 0, binlimit)

        h_mWsubjet_b1_wjetsp7  = ROOT.TH1F("h_mWsubjet_b1_wjetsp7", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_wjetsp7  = ROOT.TH1F("h_mWsubjet_b2_wjetsp7", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_wjetsp7  = ROOT.TH1F("h_mWsubjet_b3_wjetsp7", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_wjetsp7  = ROOT.TH1F("h_mWsubjet_b4_wjetsp7", "; ;  ", numbins, 0, binlimit)

    if options.dtype == 'st1':#FIX THIS see wjets1 and wjets2
        h_mWsubjet_b1_st1  = ROOT.TH1F("h_mWsubjet_b1_st1", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_st1  = ROOT.TH1F("h_mWsubjet_b2_st1", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_st1  = ROOT.TH1F("h_mWsubjet_b3_st1", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_st1  = ROOT.TH1F("h_mWsubjet_b4_st1", "; ;  ", numbins, 0, binlimit)

        h_mWsubjet_b1_stp1  = ROOT.TH1F("h_mWsubjet_b1_stp1", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_stp1  = ROOT.TH1F("h_mWsubjet_b2_stp1", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_stp1  = ROOT.TH1F("h_mWsubjet_b3_stp1", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_stp1  = ROOT.TH1F("h_mWsubjet_b4_stp1", "; ;  ", numbins, 0, binlimit)

    if options.dtype == 'st2':#FIX THIS see wjets1 and wjets2
        h_mWsubjet_b1_st2  = ROOT.TH1F("h_mWsubjet_b1_st2", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_st2  = ROOT.TH1F("h_mWsubjet_b2_st2", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_st2  = ROOT.TH1F("h_mWsubjet_b3_st2", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_st2  = ROOT.TH1F("h_mWsubjet_b4_st2", "; ;  ", numbins, 0, binlimit)

        h_mWsubjet_b1_stp2  = ROOT.TH1F("h_mWsubjet_b1_stp2", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b2_stp2  = ROOT.TH1F("h_mWsubjet_b2_stp2", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b3_stp2  = ROOT.TH1F("h_mWsubjet_b3_stp2", "; ;  ", numbins, 0, binlimit)
        h_mWsubjet_b4_stp2  = ROOT.TH1F("h_mWsubjet_b4_stp2", "; ;  ", numbins, 0, binlimit)
    #if options.dtype == 'st3':
    #if options.dtype == 'st4':

    # Counters for cut flow table
    passcuts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    # Open Input file and read tree
    fin = ROOT.TFile.Open( filein )
    if options.verbose :  print "Opened the File!  {}".format(filein)

    t =  fin.Get("TreeSemiLept") 
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
    FatJetSDmaxbdisc    = array.array('f', [-1.])
    FatJetSDsubjetWpt   = array.array('f', [-1.])
    FatJetSDsubjetWEta   = array.array('f', [-1.])
    FatJetSDsubjetWPhi   = array.array('f', [-1.])
    FatJetSDsubjetWmass = array.array('f', [-1.])
    FatJetSDsubjetWtau1   = array.array('f', [-1.])
    FatJetSDsubjetWtau2   = array.array('f', [-1.])
    FatJetSDsubjetWtau3   = array.array('f', [-1.])
    FatJetSDsubjetWtau21   = array.array('f', [-1.])
    FatJetSDsubjetWtau32   = array.array('f', [-1.])
    FatJetSDbdiscW      = array.array('f', [-1.])
    FatJetSDsubjetBpt   = array.array('f', [-1.])
    FatJetSDsubjetBmass = array.array('f', [-1.])
    FatJetSDsubjetBtau1   = array.array('f', [-1.])
    FatJetSDsubjetBtau2   = array.array('f', [-1.])
    FatJetSDsubjetBtau3   = array.array('f', [-1.])
    FatJetSDsubjetBtau21   = array.array('f', [-1.])
    FatJetSDsubjetBtau32   = array.array('f', [-1.])
    FatJetSDbdiscB      = array.array('f', [-1.])
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
    DeltaRLepFat        = array.array('f', [-1.])
    DeltaRAK4AK8        = array.array('f', [-1.])
    NearestAK4JetPt     = array.array('f', [-1.])
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
    t.SetBranchAddress('FatJetSDsubjetWEta'   , FatJetSDsubjetWEta )
    t.SetBranchAddress('FatJetSDsubjetWPhi'   , FatJetSDsubjetWPhi )
    t.SetBranchAddress('FatJetSDsubjetWmass' , FatJetSDsubjetWmass )
    t.SetBranchAddress('FatJetSDsubjetWtau1' , FatJetSDsubjetWtau1 )
    t.SetBranchAddress('FatJetSDsubjetWtau2' , FatJetSDsubjetWtau2 )
    t.SetBranchAddress('FatJetSDsubjetWtau3' , FatJetSDsubjetWtau3 )
    t.SetBranchAddress('FatJetSDsubjetWtau21' , FatJetSDsubjetWtau21 )
    t.SetBranchAddress('FatJetSDsubjetWtau32' , FatJetSDsubjetWtau32 )
    t.SetBranchAddress('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt   )
    t.SetBranchAddress('FatJetSDsubjetBmass' , FatJetSDsubjetBmass )
    t.SetBranchAddress('FatJetSDsubjetBtau1' , FatJetSDsubjetBtau1 )
    t.SetBranchAddress('FatJetSDsubjetBtau2' , FatJetSDsubjetBtau2 )
    t.SetBranchAddress('FatJetSDsubjetBtau32' , FatJetSDsubjetBtau32 )
    t.SetBranchAddress('FatJetSDsubjetBtau21' , FatJetSDsubjetBtau21 )
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
    t.SetBranchAddress('AK4bDisc'            , AK4bDisc            )
    t.SetBranchAddress('SemiLepMETphi'       , SemiLepMETphi       )
    t.SetBranchAddress('SemiLepNvtx'         , SemiLepNvtx         )
    t.SetBranchAddress('DeltaPhiLepFat'      , DeltaPhiLepFat      )
    t.SetBranchAddress('DeltaRLepFat'        , DeltaRLepFat        )
    t.SetBranchAddress('DeltaRAK4AK8'        , DeltaRAK4AK8        )
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
    t.SetBranchStatus('BJetbDisc' , 1)
    t.SetBranchStatus('FatJetSDsubjetWpt',1)
    t.SetBranchStatus('FatJetSDsubjetWtau1',1)
    t.SetBranchStatus('FatJetSDsubjetWtau2',1)
    t.SetBranchStatus('FatJetSDsubjetWtau3',1)
    t.SetBranchStatus('FatJetSDsubjetWtau21',1)
    t.SetBranchStatus('FatJetSDsubjetWtau32',1)
    t.SetBranchStatus('FatJetSDbdiscW',1)
    t.SetBranchStatus('FatJetSDsubjetWEta',1)
    t.SetBranchStatus('FatJetSDsubjetWPhi',1)
    t.SetBranchStatus('FatJetSDsubjetBtau1',1)
    t.SetBranchStatus('FatJetSDsubjetBtau2',1)
    t.SetBranchStatus('FatJetSDsubjetBtau3',1)
    t.SetBranchStatus('FatJetSDsubjetBtau21',1)
    t.SetBranchStatus('FatJetSDsubjetBtau32',1)
    t.SetBranchStatus('FatJetSDbdiscB',1)
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
    t.SetBranchStatus ('SemiLepMETpt'  , 1  )
    t.SetBranchStatus ('AK4bDisc'      , 1  )
    t.SetBranchStatus ('SemiLepMETphi' , 1  )
    t.SetBranchStatus ('LeptonType'          , 1)
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

    # Begin Event Loop
    for jentry in xrange( eventsToRun ):
        if jentry % 100000 == 0 :
            print 'processing ' + str(jentry)
        ientry = t.GetEntry( jentry )
        if ientry < 0:
            break
        # Event Info
        weightS = SemiLeptWeight[0]
        eventNum = SemiLeptEventNum[0]
        type1or2 = BoosttypE[0]
        runNum = SemiLeptRunNum[0]
        lumiBlock = SemiLeptLumiBlock[0]

        # Lepton Observables
        theLepton = ROOT.TLorentzVector()
        theLepton.SetPtEtaPhiE( LeptonPt[0], LeptonEta[0], LeptonPhi[0], LeptonEnergy[0] ) # Assume massless
        LepPt = theLepton.Perp()
        LepEta = theLepton.Eta()
        LepType =  LeptonType[0]
        lepton_ptRel = LeptonPtRel[0]
        lepton_DRmin = LeptonDRMin[0] 

        # MET Observables
        nuCandP4 = ROOT.TLorentzVector( )
        nuCandP4.SetPtEtaPhiM( SemiLepMETpt[0], 0, SemiLepMETphi[0], SemiLepMETpt[0] )
        MET_pt = nuCandP4.Perp()


        # ak4 Observables            
        bJetCandP4puppi0 = ROOT.TLorentzVector()
        if options.Type2 :
            bJetCandP4puppi0.SetPtEtaPhiM( BJetPt[0], BJetEta[0], BJetPhi[0], BJetMass[0])
            ak4_bdisc = BJetbDisc[0]
        else :
            bJetCandP4puppi0.SetPtEtaPhiM( NearestAK4JetPt[0], NearestAK4JetEta[0], NearestAK4JetPhi[0], NearestAK4JetMass[0])
            ak4_bdisc = AK4bDisc[0]


        # ak8 Observables 

        FatJetP4 = ROOT.TLorentzVector()    
        FatJetP4.SetPtEtaPhiM( FatJetPt[0], FatJetEta[0], FatJetPhi[0], FatJetMass[0])     
        fatpt = FatJetP4.Perp()
        fateta = FatJetP4.Eta()
        fatmass = FatJetP4.M()

        FatJetSD_m = FatJetMassSoftDrop[0]
        Rhorat = FatJetRhoRatio[0]
        if (Rhorat > 0.001): # FatJetSDpt = m / (R*sqrt(rhoRatio))
            sqrtRhorat = math.sqrt(Rhorat)
            FatJetSD_pt = FatJetSD_m / (0.8 * sqrtRhorat  )
        else:
            FatJetSD_pt = 0.
        tau32 = FatJetTau32[0]
        tau21 = FatJetTau21[0]
        tau3 = FatJetTau3[0]
        tau2 = FatJetTau2[0]
        tau1 = FatJetTau1[0]


        # ak8 subjet Observables             

        W_m = FatJetSDsubjetWmass[0]
        W_pt = FatJetSDsubjetWpt[0]
        W_tau1 = FatJetSDsubjetWtau1[0]
        W_tau2 = FatJetSDsubjetWtau2[0]
        W_tau3 = FatJetSDsubjetWtau3[0]
        W_bdisc = FatJetSDbdiscW[0]
        W_eta = FatJetSDsubjetWEta[0]
        W_phi = FatJetSDsubjetWPhi[0]
        W_tau21 = FatJetSDsubjetWtau21[0]

        B_pt = FatJetSDsubjetBpt[0]
        B_m = FatJetSDsubjetBmass[0]
        B_bdisc = FatJetSDbdiscB[0]


        #applying Thea's corrections for Type 2   FIX THIS SHOULD BE SD MASS AND PT RAW
        if options.applyTheaCorr and  options.Type2  and FatJetSD_pt >  170. and type1or2 == 2 :
            W_mRaw = FatJetSD_m # SD mass is raw
            W_ptRaw = FatJetSD_pt
            puppiCorr = getPUPPIweight( W_ptRaw , W_eta )
            FatJetSD_m = W_mRaw * puppiCorr

        #applying Thea's corrections for Type 1
        if options.applyTheaCorr and ( not options.Type2 ) and FatJetSD_pt > (options.Ak8PtCut - 20. ) and W_pt > 170. and type1or2 == 1  :
            W_mRaw = FatJetSDsubjetWmassRaw[0]
            W_ptRaw = FatJetSDsubjetWptRaw[0]
            puppiCorr = getPUPPIweight( W_ptRaw , W_eta )
            W_m =  W_mRaw  * puppiCorr


        realw = -1
        fakew = -1
        # Get Generator level matching Info
        if options.match and options.dtype == 'ttjets':
            # FIX THIS read the Matched tree and get info
            realw = FatJetSDsubjet_isRealW[0]
            fakew = FatJetSDsubjet_isRealW[0]

        ##  ____  __.__                              __  .__         __________                     
        ## |    |/ _|__| ____   ____   _____ _____ _/  |_|__| ____   \______   \ ____   ____  ____  
        ## |      < |  |/    \_/ __ \ /     \\__  \\   __\  |/ ___\   |       _// __ \_/ ___\/  _ \ 
        ## |    |  \|  |   |  \  ___/|  Y Y  \/ __ \|  | |  \  \___   |    |   \  ___/\  \__(  <_> )
        ## |____|__ \__|___|  /\___  >__|_|  (____  /__| |__|\___  >  |____|_  /\___  >\___  >____/ 
        ##         \/       \/     \/      \/     \/             \/          \/     \/     \/       

        # Now we do our kinematic calculation based on the semi-leptonic selection detailed in AN-16-215 (previous selection was B2G-15-002)

        #Electron Selection
        passEleMETcut  = LepType == 1 and MET_pt > 80. 
        passEleEtacut  = LepType == 1 and  0. < abs(LepEta) < 1.442 or 1.56 < abs(LepEta) < 2.5 
        passElePtcut   = LepType == 1  and  LepPt > 120. 
        passEl         = (passEleMETcut and passElePtcut and passEleEtacut)

        if passElePtcut :
            passcuts[0] +=1

        if passEleEtacut :
            passcuts[1] +=1

        if passEleMETcut :
            passcuts[2] +=1

        if passEl :
            passcuts[18] +=1

        #Muon Selection
        passMuPtcut     = LepType == 2 and LepPt > 53. 
        passMuEtacut    = LepType == 2 and abs(LepEta) < 2.1 
        passMuMETcut    = LepType == 2 and MET_pt > 40. and LepPt > 53. and abs(LepEta) < 2.1 
        passMuIsocut    = LepType == 2 and LeptonIso[0] < 0.1
        passMu          = (passMuPtcut and passMuMETcut and passMuEtacut and passMuIsocut )

        if passMuPtcut :
            passcuts[3]   +=1
        if passMuEtacut :
            passcuts[19]  +=1
        if passMuMETcut :
            passcuts[20]  +=1
        if passMuIsocut :
            passcuts[4]   +=1  
        if passMu :
            passcuts[21]  +=1

        #Lepton Selection
        passLepDrmin    = LeptonDRMin[0] > 0.3
        passHemidR = DeltaRLepFat[0] > 1. 
        passLepcut = passHemidR and passLepDrmin and (  passEl or passMu  ) 

        if passLepDrmin :
            passcuts[22] += 1
        if passHemidR:
            passcuts[7] +=1
        if passLepcut :
            passcuts[5] += 1

        if options.verbose and passLepcut and passEl: 
            print "Electron:  pt {0:3.2f}, eta {1:3.2f}, MET_pt {2:3.2f}".format(LepPt, abs(LepEta),  MET_pt) 
        if options.verbose and passLepcut and passMu: 
            print "Muon:  pt {0:3.2f}, eta {1:3.2f}, MET_pt {2:3.2f}".format(LepPt, abs(LepEta),  MET_pt) 

        # Lepton cuts applied
        if not passLepcut : continue

        #AK4 Selection
        passBtagBdisc = ak4_bdisc > 0.8 
        passBtagPt = NearestAK4JetPt[0] > 30.
        passBDrAK8 = drAK4AK8 > 0.8 
        passAK4 = (passBtagBdisc and passBtagPt and passBDrAK8)
        if passBtagBdisc :
            passcuts[12] += 1
        if passBtagPt :
            passcuts[13] += 1  
        if passBDrAK8 :
            passcuts[23] += 1  
        if passAK4 :
            passcuts[24] += 1

        # AK4 cuts applied
        if not passAK4 : continue
        if not passAK4 : print "THIS DOESNT DO WHAT YOU THINK IT DOES"

        #AK8 Selection

        if options.Type2 :                                                                    # Type 2 AK8 selection
            #passWPre2 = FatJetSD_m > 50.
            passKin2 =  FatJetSD_pt > 200. and abs(fateta) < 2.4 and W_m < 0.
            passWTagmass = 0.2 < FatJetSD_m < 160.
            passWPosttau2 = tau21 < options.tau21Cut  and tau21 > 0.1
            passWPostM2 = 55. < FatJetSD_m < 115.

            if passKin2 :
                passcuts[14] += 1
            if passWTagmass :
                passcuts[10] += 1
            if passWPosttau2:
                passcuts[15] +=1
            if passWPostM2:
                passcuts[16] +=1

            # AK8 cuts applied
            if not (passKin2 and ):

        else :                                                                                # Type 1 AK8 selection
            passWPre =   W_m > 50.  # WORKING HERE ????

            passWPostM = 55. < W_m < 115.
            passWPosttag = 0.1 < W_tau21 < options.tau21Cut 

            passKin = FatJetSD_pt > options.Ak8PtCut  
            passWKin = W_pt > 200.  and abs(W_eta) < 2.4 

            passTopTagtau = tau32 < options.tau32Cut 
            passTopTagmass =  110. < FatJetSD_m < 250.

            pass2DCut = LeptonPtRel[0] > 20. or LeptonDRMin[0] > 0.4

            if passKin :
            passcuts[17] += 1
            if passWKin :
            passcuts[14] += 1
            if pass2DCut : 
            passcuts[11] += 1
            if passTopTagtau :
            passcuts[9] += 1
            if passTopTagmass :
            passcuts[10] += 1
            if passWPosttag:
            passcuts[15] +=1
            if passWPostM:
            passcuts[16] +=1
        
        # Type 2 cuts applied
        if options.Type2 : 
            if (passKin2 and passWTagmass  and passHemidR)                                                            

            if passKin2 :
                passcuts[14] += 1
            if passWTagmass :
                passcuts[10] += 1
            if passWPosttau2:
                passcuts[15] +=1
            if passWPostM2:
                passcuts[16] +=1

        # Type 1 cuts applied
        if not options.Type2 :
            if  (passTopTagtau and passTopTagmass and pass2DCut and passLepcut and passBtagBdisc and passBtagPt and passHemidR ): #
                if options.verbose and (15. < W_m < 40.): print "Fat Jet: SD Mass {0:6.3}, Pt {1:6.3}, tau32 {2:0.4} - W Subjet: SD Mass {3:6.3}, Pt {4:6.3}, tau21 {5:0.4} - dphiLepFat {6:6.3} ".format(FatJetSD_m, FatJetSD_pt, tau32, W_m, W_pt, W_tau21, DeltaPhiLepFat[0] )
                #print "SD pt of W subjet {0:6.3} and Pt is {1:6.3}".format()

                if passKin and passWKin :




                    # FIX THIS -Fill the Combined Trees after selection here 
                    if options.combineTrees :
                        print "Tree writing is not yet enabled"
                        fout.cd()
                        tree.Fill()
                        

                    fout.cd() 
                    TheWeight = weightS

                    if LepType ==1 :
                        ElgsfSF = getgsfTrackEffScaleFactor(LepEta)
                        TheWeight = weightS * ElgsfSF

                    if (ifile != 11 and ifile != 0):
                        h_mWsubjet_MC.Fill(W_m , TheWeight )
                    if (ifile == 11 ):
                        h_mWsubjet_Data.Fill(W_m , TheWeight )
                    if (ifile == 10 ): #ttjets
                        h_mWsubjet_ttjets.Fill(W_m , TheWeight )

                    if (ifile == 1 ): #st top
                        #h_mWsubjet_stp.Fill(W_m ,TheWeight )
                        #h_ptWsubjet_stp.Fill(W_pt , TheWeight )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #Wsj_ttp[0].Fill(W_m , 1 )
                            h_mWsubjet_b1_stp1.Fill(W_m , TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) :
                            #Wsj_ttp[1].Fill(W_m , 1 )                           
                            h_mWsubjet_b2_stp1.Fill(W_m ,TheWeight )
                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #Wsj_ttp[2].Fill(W_m , 1 )
                            h_mWsubjet_b3_stp1.Fill(W_m ,TheWeight )
                        if ( W_pt > 500.0 ) : 
                            #Wsj_ttp[3].Fill(W_m , 1 )
                            h_mWsubjet_b4_stp1.Fill(W_m , TheWeight )
                    if (ifile == 2 ): #st antitop
                        #h_mWsubjet_stp.Fill(W_m ,TheWeight )
                        #h_ptWsubjet_stp.Fill(W_pt , TheWeight )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #Wsj_ttp[0].Fill(W_m , 1 )
                            h_mWsubjet_b1_stp2.Fill(W_m , TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) :
                            #Wsj_ttp[1].Fill(W_m , 1 )                           
                            h_mWsubjet_b2_stp2.Fill(W_m ,TheWeight )
                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #Wsj_ttp[2].Fill(W_m , 1 )
                            h_mWsubjet_b3_stp2.Fill(W_m ,TheWeight )
                        if ( W_pt > 500.0 ) : 
                            #Wsj_ttp[3].Fill(W_m , 1 )
                            h_mWsubjet_b4_stp2.Fill(W_m , TheWeight )
                    if (ifile == 3 ): #wjets1 - 100to200  
                        #h_mWsubjet_wjetsp.Fill(W_m ,TheWeight)
                        #h_ptWsubjet_wjetsp.Fill(W_pt ,TheWeight )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #Wsj_ttp[0].Fill(W_m , 1 )
                            h_mWsubjet_b1_wjetsp1.Fill(W_m , TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) :
                            #Wsj_ttp[1].Fill(W_m , 1 )                           
                            h_mWsubjet_b2_wjetsp1.Fill(W_m , TheWeight )
                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #Wsj_ttp[2].Fill(W_m , 1 )
                            h_mWsubjet_b3_wjetsp1.Fill(W_m , TheWeight )
                        if ( W_pt > 500.0 ) : 
                            #Wsj_ttp[3].Fill(W_m , 1 )
                            h_mWsubjet_b4_wjetsp1.Fill(W_m , TheWeight )
                    if (ifile == 4 ): #wjets2 - 200to400  
                        #h_mWsubjet_wjetsp.Fill(W_m ,TheWeight)
                        #h_ptWsubjet_wjetsp.Fill(W_pt ,TheWeight )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #Wsj_ttp[0].Fill(W_m , 1 )
                            h_mWsubjet_b1_wjetsp2.Fill(W_m , TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) :
                            #Wsj_ttp[1].Fill(W_m , 1 )                           
                            h_mWsubjet_b2_wjetsp2.Fill(W_m , TheWeight )
                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #Wsj_ttp[2].Fill(W_m , 1 )
                            h_mWsubjet_b3_wjetsp2.Fill(W_m , TheWeight )
                        if ( W_pt > 500.0 ) : 
                            #Wsj_ttp[3].Fill(W_m , 1 )
                            h_mWsubjet_b4_wjetsp2.Fill(W_m , TheWeight )
                    if (ifile == 5 ): #wjets3 - 400to600  
                        #h_mWsubjet_wjetsp.Fill(W_m ,TheWeight)
                        #h_ptWsubjet_wjetsp.Fill(W_pt ,TheWeight )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #Wsj_ttp[0].Fill(W_m , 1 )
                            h_mWsubjet_b1_wjetsp3.Fill(W_m , TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) :
                            #Wsj_ttp[1].Fill(W_m , 1 )                           
                            h_mWsubjet_b2_wjetsp3.Fill(W_m , TheWeight )
                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #Wsj_ttp[2].Fill(W_m , 1 )
                            h_mWsubjet_b3_wjetsp3.Fill(W_m , TheWeight )
                        if ( W_pt > 500.0 ) : 
                            #Wsj_ttp[3].Fill(W_m , 1 )
                            h_mWsubjet_b4_wjetsp3.Fill(W_m , TheWeight )
                    if (ifile == 6 ): #wjets4 - 600to800  
                        #h_mWsubjet_wjetsp.Fill(W_m ,TheWeight)
                        #h_ptWsubjet_wjetsp.Fill(W_pt ,TheWeight )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #Wsj_ttp[0].Fill(W_m , 1 )
                            h_mWsubjet_b1_wjetsp4.Fill(W_m , TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) :
                            #Wsj_ttp[1].Fill(W_m , 1 )                           
                            h_mWsubjet_b2_wjetsp4.Fill(W_m , TheWeight )
                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #Wsj_ttp[2].Fill(W_m , 1 )
                            h_mWsubjet_b3_wjetsp4.Fill(W_m , TheWeight )
                        if ( W_pt > 500.0 ) : 
                            #Wsj_ttp[3].Fill(W_m , 1 )
                            h_mWsubjet_b4_wjetsp4.Fill(W_m , TheWeight )
                    if (ifile == 7 ): #wjets5 - 800to1200  
                        #h_mWsubjet_wjetsp.Fill(W_m ,TheWeight)
                        #h_ptWsubjet_wjetsp.Fill(W_pt ,TheWeight )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #Wsj_ttp[0].Fill(W_m , 1 )
                            h_mWsubjet_b1_wjetsp5.Fill(W_m , TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) :
                            #Wsj_ttp[1].Fill(W_m , 1 )                           
                            h_mWsubjet_b2_wjetsp5.Fill(W_m , TheWeight )
                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #Wsj_ttp[2].Fill(W_m , 1 )
                            h_mWsubjet_b3_wjetsp5.Fill(W_m , TheWeight )
                        if ( W_pt > 500.0 ) : 
                            #Wsj_ttp[3].Fill(W_m , 1 )
                            h_mWsubjet_b4_wjetsp5.Fill(W_m , TheWeight )
                    if (ifile == 8 ): #wjets6 - 1200to2500  
                        #h_mWsubjet_wjetsp.Fill(W_m ,TheWeight)
                        #h_ptWsubjet_wjetsp.Fill(W_pt ,TheWeight )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #Wsj_ttp[0].Fill(W_m , 1 )
                            h_mWsubjet_b1_wjetsp6.Fill(W_m , TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) :
                            #Wsj_ttp[1].Fill(W_m , 1 )                           
                            h_mWsubjet_b2_wjetsp6.Fill(W_m , TheWeight )
                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #Wsj_ttp[2].Fill(W_m , 1 )
                            h_mWsubjet_b3_wjetsp6.Fill(W_m , TheWeight )
                        if ( W_pt > 500.0 ) : 
                            #Wsj_ttp[3].Fill(W_m , 1 )
                            h_mWsubjet_b4_wjetsp6.Fill(W_m , TheWeight )
                    if (ifile == 9 ): #wjets7 - 2500toInf  
                        #h_mWsubjet_wjetsp.Fill(W_m ,TheWeight)
                        #h_ptWsubjet_wjetsp.Fill(W_pt ,TheWeight )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #Wsj_ttp[0].Fill(W_m , 1 )
                            h_mWsubjet_b1_wjetsp7.Fill(W_m , TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) :
                            #Wsj_ttp[1].Fill(W_m , 1 )                           
                            h_mWsubjet_b2_wjetsp7.Fill(W_m , TheWeight )
                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #Wsj_ttp[2].Fill(W_m , 1 )
                            h_mWsubjet_b3_wjetsp7.Fill(W_m , TheWeight )
                        if ( W_pt > 500.0 ) : 
                            #Wsj_ttp[3].Fill(W_m , 1 )
                            h_mWsubjet_b4_wjetsp7.Fill(W_m , TheWeight )

                    if (ifile == 10 ): #ttjets
                        h_mWsubjet_wjetsp.Fill(W_m , TheWeight )
                        h_ptWsubjet_wjetsp.Fill(W_pt , TheWeight )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #Wsj_ttp[0].Fill(W_m , 1 )
                            h_mWsubjet_b1_ttjetsp.Fill(W_m , TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) :
                            #Wsj_ttp[1].Fill(W_m , 1 )                           
                            h_mWsubjet_b2_ttjetsp.Fill(W_m ,TheWeight )
                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #Wsj_ttp[2].Fill(W_m , 1 )
                            h_mWsubjet_b3_ttjetsp.Fill(W_m , TheWeight )
                        if ( W_pt > 500.0 ) : 
                            #Wsj_ttp[3].Fill(W_m , 1 )
                            h_mWsubjet_b4_ttjetsp.Fill(W_m , TheWeight )
                    if (ifile == 11) and LeptonType[0] == 1 and W_m > 0.1 : 
                        h_mWsubjet_ElDatap.Fill(W_m , TheWeight )
                        h_ptWsubjet_ElDatap.Fill(W_pt , TheWeight  )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) : 
                            h_mWsubjet_b1_ElDatap.Fill(W_m ,TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) : 
                            h_mWsubjet_b2_ElDatap.Fill(W_m , TheWeight )

                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            h_mWsubjet_b3_ElDatap.Fill(W_m , TheWeight)

                        if ( W_pt > 500.0 ) : 
                            h_mWsubjet_b4_ElDatap.Fill(W_m , TheWeight )
                        
                    if (ifile == 11 ) and LeptonType[0] == 2 and W_m > 0.1 :
                        h_mWsubjet_MuDatap.Fill(W_m , TheWeight )
                        h_ptWsubjet_MuDatap.Fill(W_pt , TheWeight)

                        if ( W_pt > 200.0 and W_pt < 300.0 ) : 
                            h_mWsubjet_b1_MuDatap.Fill(W_m , TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) : 
                            h_mWsubjet_b2_MuDatap.Fill(W_m , TheWeight )

                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            h_mWsubjet_b3_MuDatap.Fill(W_m , TheWeight )

                        if ( W_pt > 500.0 ) : 
                            h_mWsubjet_b4_MuDatap.Fill(W_m , TheWeight ) 
                    if (ifile == 11 ):
                        h_mWsubjet_Datap.Fill(W_m , TheWeight )
                        h_ptWsubjet_Datap.Fill(W_pt , TheWeight )

                        if ( W_pt > 200.0 and W_pt < 300.0 ) :
                            #Wsj_datap[0].Fill(W_m , 1 )
                            h_mWsubjet_b1_Datap.Fill(W_m ,TheWeight )

                        if ( W_pt > 300.0 and W_pt < 400.0 ) : 
                            #Wsj_datap[1].Fill(W_m , 1 )
                            h_mWsubjet_b2_Datap.Fill(W_m , TheWeight )

                        if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                            #Wsj_datap[2].Fill(W_m , 1 )
                            h_mWsubjet_b3_Datap.Fill(W_m , TheWeight )

                        if ( W_pt > 500.0 ) : 
                            #Wsj_datap[3].Fill(W_m , 1 )
                            h_mWsubjet_b4_Datap.Fill(W_m , TheWeight )
                    if passWPosttag :
                        passOp += 1 
                        if (ifile == 1 ): #st top
                            #h_mWsubjet_st.Fill(W_m , TheWeight )
                            #h_ptWsubjet_st.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) :
                                #Wsj_ttp[0].Fill(W_m , 1 )
                                h_mWsubjet_b1_st1.Fill(W_m , TheWeight )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) :
                                #Wsj_ttp[1].Fill(W_m , 1 )                           
                                h_mWsubjet_b2_st1.Fill(W_m , TheWeight )
                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #Wsj_ttp[2].Fill(W_m , 1 )
                                h_mWsubjet_b3_st1.Fill(W_m ,TheWeight )
                            if ( W_pt > 500.0 ) : 
                                #Wsj_ttp[3].Fill(W_m , 1 )
                                h_mWsubjet_b4_st1.Fill(W_m , TheWeight )
                        if (ifile == 2 ): #st antitop
                            #h_mWsubjet_st.Fill(W_m , TheWeight )
                            #h_ptWsubjet_st.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) :
                                #Wsj_ttp[0].Fill(W_m , 1 )
                                h_mWsubjet_b1_st2.Fill(W_m , TheWeight )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) :
                                #Wsj_ttp[1].Fill(W_m , 1 )                           
                                h_mWsubjet_b2_st2.Fill(W_m , TheWeight )
                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #Wsj_ttp[2].Fill(W_m , 1 )
                                h_mWsubjet_b3_st2.Fill(W_m ,TheWeight )
                            if ( W_pt > 500.0 ) : 
                                #Wsj_ttp[3].Fill(W_m , 1 )
                                h_mWsubjet_b4_st2.Fill(W_m , TheWeight )
                        if (ifile == 3): #wjets1 - 100to200  
                            # h_mWsubjet_wjets.Fill(W_m , TheWeight)
                            #h_ptWsubjet_wjets.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) :
                                #Wsj_ttp[0].Fill(W_m , 1 )
                                h_mWsubjet_b1_wjets1.Fill(W_m ,TheWeight )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) :
                                #Wsj_ttp[1].Fill(W_m , 1 )                           
                                h_mWsubjet_b2_wjets1.Fill(W_m , TheWeight)
                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #Wsj_ttp[2].Fill(W_m , 1 )
                                h_mWsubjet_b3_wjets1.Fill(W_m , TheWeight )
                            if ( W_pt > 500.0 ) : 
                                #Wsj_ttp[3].Fill(W_m , 1 )
                                h_mWsubjet_b4_wjets1.Fill(W_m , TheWeight )
                        if (ifile == 4): #wjets2 - 200to400  
                            # h_mWsubjet_wjets.Fill(W_m , TheWeight)
                            #h_ptWsubjet_wjets.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) :
                                #Wsj_ttp[0].Fill(W_m , 1 )
                                h_mWsubjet_b1_wjets2.Fill(W_m ,TheWeight )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) :
                                #Wsj_ttp[1].Fill(W_m , 1 )                           
                                h_mWsubjet_b2_wjets2.Fill(W_m , TheWeight)
                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #Wsj_ttp[2].Fill(W_m , 1 )
                                h_mWsubjet_b3_wjets2.Fill(W_m , TheWeight )
                            if ( W_pt > 500.0 ) : 
                                #Wsj_ttp[3].Fill(W_m , 1 )
                                h_mWsubjet_b4_wjets2.Fill(W_m , TheWeight )
                        if (ifile == 5): #wjets3 - 400to600  
                            # h_mWsubjet_wjets.Fill(W_m , TheWeight)
                            #h_ptWsubjet_wjets.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) :
                                #Wsj_ttp[0].Fill(W_m , 1 )
                                h_mWsubjet_b1_wjets3.Fill(W_m ,TheWeight )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) :
                                #Wsj_ttp[1].Fill(W_m , 1 )                           
                                h_mWsubjet_b2_wjets3.Fill(W_m , TheWeight)
                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #Wsj_ttp[2].Fill(W_m , 1 )
                                h_mWsubjet_b3_wjets3.Fill(W_m , TheWeight )
                            if ( W_pt > 500.0 ) : 
                                #Wsj_ttp[3].Fill(W_m , 1 )
                                h_mWsubjet_b4_wjets3.Fill(W_m , TheWeight )
                        if (ifile == 6): #wjets4 - 600to800  
                            # h_mWsubjet_wjets.Fill(W_m , TheWeight)
                            #h_ptWsubjet_wjets.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) :
                                #Wsj_ttp[0].Fill(W_m , 1 )
                                h_mWsubjet_b1_wjets4.Fill(W_m ,TheWeight )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) :
                                #Wsj_ttp[1].Fill(W_m , 1 )                           
                                h_mWsubjet_b2_wjets4.Fill(W_m , TheWeight)
                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #Wsj_ttp[2].Fill(W_m , 1 )
                                h_mWsubjet_b3_wjets4.Fill(W_m , TheWeight )
                            if ( W_pt > 500.0 ) : 
                                #Wsj_ttp[3].Fill(W_m , 1 )
                                h_mWsubjet_b4_wjets4.Fill(W_m , TheWeight )
                        if (ifile == 7): #wjets5 - 800to1200  
                            # h_mWsubjet_wjets.Fill(W_m , TheWeight)
                            #h_ptWsubjet_wjets.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) :
                                #Wsj_ttp[0].Fill(W_m , 1 )
                                h_mWsubjet_b1_wjets5.Fill(W_m ,TheWeight )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) :
                                #Wsj_ttp[1].Fill(W_m , 1 )                           
                                h_mWsubjet_b2_wjets5.Fill(W_m , TheWeight)
                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #Wsj_ttp[2].Fill(W_m , 1 )
                                h_mWsubjet_b3_wjets5.Fill(W_m , TheWeight )
                            if ( W_pt > 500.0 ) : 
                                #Wsj_ttp[3].Fill(W_m , 1 )
                                h_mWsubjet_b4_wjets5.Fill(W_m , TheWeight )
                        if (ifile == 8): #wjets6 - 1200to2500  
                            # h_mWsubjet_wjets.Fill(W_m , TheWeight)
                            #h_ptWsubjet_wjets.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) :
                                #Wsj_ttp[0].Fill(W_m , 1 )
                                h_mWsubjet_b1_wjets6.Fill(W_m ,TheWeight )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) :
                                #Wsj_ttp[1].Fill(W_m , 1 )                           
                                h_mWsubjet_b2_wjets6.Fill(W_m , TheWeight)
                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #Wsj_ttp[2].Fill(W_m , 1 )
                                h_mWsubjet_b3_wjets6.Fill(W_m , TheWeight )
                            if ( W_pt > 500.0 ) : 
                                #Wsj_ttp[3].Fill(W_m , 1 )
                                h_mWsubjet_b4_wjets6.Fill(W_m , TheWeight )
                        if (ifile == 9): #wjets7 - 2500toInf  
                            # h_mWsubjet_wjets.Fill(W_m , TheWeight)
                            #h_ptWsubjet_wjets.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) :
                                #Wsj_ttp[0].Fill(W_m , 1 )
                                h_mWsubjet_b1_wjets7.Fill(W_m ,TheWeight )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) :
                                #Wsj_ttp[1].Fill(W_m , 1 )                           
                                h_mWsubjet_b2_wjets7.Fill(W_m , TheWeight)
                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #Wsj_ttp[2].Fill(W_m , 1 )
                                h_mWsubjet_b3_wjets7.Fill(W_m , TheWeight )
                            if ( W_pt > 500.0 ) : 
                                #Wsj_ttp[3].Fill(W_m , 1 )
                                h_mWsubjet_b4_wjets7.Fill(W_m , TheWeight )

                        if (ifile == 10 ): #ttjets
                            if passWPostM  : 
                                h_ptWsubjet_MC_Type1.Fill(W_pt,TheWeight )
                            #h_mWsubjet_ttjets.Fill(W_m , TheWeight )
                            h_ptWsubjet_ttjets.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) :
                                #Wsj_tt[0].Fill(W_m , 1 )
                                h_mWsubjet_b1_ttjets.Fill(W_m , TheWeight )
                            if ( W_pt > 300.0 and W_pt < 400.0 ) :
                                #Wsj_tt[1].Fill(W_m , 1 )                           
                                h_mWsubjet_b2_ttjets.Fill(W_m , TheWeight )
                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #Wsj_tt[2].Fill(W_m , 1 )
                                h_mWsubjet_b3_ttjets.Fill(W_m , TheWeight )
                            if ( W_pt > 500.0 ) : 
                                #Wsj_tt[3].Fill(W_m , 1 )
                                h_mWsubjet_b4_ttjets.Fill(W_m , TheWeight )
                        if (ifile == 11) and LeptonType[0] == 1 and W_m > 0.1 : 
                            h_mWsubjet_ElData.Fill(W_m , TheWeight )
                            h_ptWsubjet_ElData.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) : 
                                h_mWsubjet_b1_ElData.Fill(W_m , TheWeight )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) : 
                                h_mWsubjet_b2_ElData.Fill(W_m , TheWeight )

                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                h_mWsubjet_b3_ElData.Fill(W_m , TheWeight )

                            if ( W_pt > 500.0 ) : 
                                h_mWsubjet_b4_ElData.Fill(W_m , TheWeight )
                            
                        if (ifile == 11) and LeptonType[0] == 2 and W_m > 0.1 :
                            h_mWsubjet_MuData.Fill(W_m , TheWeight )
                            h_ptWsubjet_MuData.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) : 
                                h_mWsubjet_b1_MuData.Fill(W_m , TheWeight )

                            if ( W_pt > 300.0 and W_pt < 400.0 ) : 
                                h_mWsubjet_b2_MuData.Fill(W_m , TheWeight )

                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                h_mWsubjet_b3_MuData.Fill(W_m , TheWeight )

                            if ( W_pt > 500.0 ) : 
                                h_mWsubjet_b4_MuData.Fill(W_m , TheWeight ) 
                            
                        if (ifile == 11 ):
                            if passWPostM : 
                                h_ptWsubjet_Data_Type1.Fill(W_pt,TheWeight)
                            #h_mWsubjet_Data.Fill(W_m , TheWeight )
                            h_ptWsubjet_Data.Fill(W_pt , TheWeight )

                            if ( W_pt > 200.0 and W_pt < 300.0 ) : 
                                 #Wsj_data[0].Fill(W_m , 1 )
                                h_mWsubjet_b1_Data.Fill(W_m , TheWeight) 

                            if ( W_pt > 300.0 and W_pt < 400.0 ) : 
                                #Wsj_data[1].Fill(W_m , 1 )
                                h_mWsubjet_b2_Data.Fill(W_m , TheWeight )

                            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                                #Wsj_data[2].Fill(W_m , 1 )
                                h_mWsubjet_b3_Data.Fill(W_m , TheWeight )

                            if ( W_pt > 500.0 ) : 
                                #Wsj_data[3].Fill(W_m , 1 )
                                h_mWsubjet_b4_Data.Fill(W_m , TheWeight )

    sf = 0.
    if (h_mWsubjet_Data.Integral() > 0) and (h_mWsubjet_MC.Integral() > 0): 
        diff = h_mWsubjet_Data.Integral()-h_mWsubjet_MC.Integral()
        sf = diff/ (h_mWsubjet_ttjets.Integral())+1
    lumi = 12300.
    kfactorw = 1.21
    scalefactor = 1.
    scalefactortt = 1.
    if sf > 0. :
        scalefactortt = sf
        print "TT SCALE FACTOR APPLIED WAS : " + str(sf)
    # W + jets cross sections from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#W_jets


    if h_mWsubjet_b1_ttjets.Integral() > 0 : 
        h_mWsubjet_b1_ttjets.Scale(lumi* scalefactortt * 831.76 / 91061600. )#97994456. )#182123200.) #hdataT.GetEntries()/ httbarT.Integral()) #
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt b1 empty"
        h_mWsubjet_b1_ttjets.Scale( 0.)


    if h_mWsubjet_b1_ttjetsp.Integral() > 0 : 
        h_mWsubjet_b1_ttjetsp.Scale(lumi* scalefactortt * 831.76 / 97994456. )#182123200. )  # hdataTp.GetEntries()/ httbarTp.Integral()) #
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt b1 p empty"
        h_mWsubjet_b1_ttjetsp.Scale( 0.)

    if h_mWsubjet_b2_ttjets.Integral() > 0 : 
        h_mWsubjet_b2_ttjets.Scale(lumi* scalefactortt * 831.76 / 91061600. )#97994456. )#182123200.) #hdataT.GetEntries()/ httbarT.Integral()) #
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt b2 empty"
        h_mWsubjet_b2_ttjets.Scale( 0.)


    if h_mWsubjet_b2_ttjetsp.Integral() > 0 : 
        h_mWsubjet_b2_ttjetsp.Scale(lumi* scalefactortt * 831.76 / 97994456. )#182123200. )  # hdataTp.GetEntries()/ httbarTp.Integral()) #
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt b2 p empty"
        h_mWsubjet_b2_ttjetsp.Scale( 0.)

    if h_mWsubjet_b3_ttjets.Integral() > 0 : 
        h_mWsubjet_b3_ttjets.Scale(lumi* scalefactortt * 831.76 / 91061600. )#97994456. )#182123200.) #hdataT.GetEntries()/ httbarT.Integral()) #
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt b3 empty"
        h_mWsubjet_b3_ttjets.Scale( 0.)


    if h_mWsubjet_b3_ttjetsp.Integral() > 0 : 
        h_mWsubjet_b3_ttjetsp.Scale(lumi* scalefactortt * 831.76 / 97994456. )#182123200. )  # hdataTp.GetEntries()/ httbarTp.Integral()) #
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt b3 p empty"
        h_mWsubjet_b3_ttjetsp.Scale( 0.)

    if h_mWsubjet_b4_ttjets.Integral() > 0 : 
        h_mWsubjet_b4_ttjets.Scale(lumi* scalefactortt * 831.76 / 91061600. )#97994456. )#182123200.) #hdataT.GetEntries()/ httbarT.Integral()) #
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt b4 empty"
        h_mWsubjet_b4_ttjets.Scale( 0.)


    if h_mWsubjet_b4_ttjetsp.Integral() > 0 : 
        h_mWsubjet_b4_ttjetsp.Scale(lumi* scalefactortt * 831.76 / 97994456. )#182123200. )  # hdataTp.GetEntries()/ httbarTp.Integral()) #
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt b4 p empty"
        h_mWsubjet_b4_ttjetsp.Scale( 0.)

    if h_mWsubjet_b1_wjets1.Integral() > 0 : 
        h_mWsubjet_b1_wjets1.Scale(lumi * kfactorw * scalefactor *1345. / 10152718.)#27529599. ) 
    else :
        print "w+jets 100to200 b1 empty"
        h_mWsubjet_b1_wjets1.Scale( 0.)
    if h_mWsubjet_b1_wjetsp1.Integral() > 0 : 
        h_mWsubjet_b1_wjetsp1.Scale(lumi * kfactorw * scalefactor *1345. /10152718. )# 27529599. ) 
    else :
        print "w+jets p 100to200 b1 empty"
        h_mWsubjet_b1_wjetsp1.Scale( 0.)

    if h_mWsubjet_b1_wjets2.Integral() > 0 : 
        h_mWsubjet_b1_wjets2.Scale(lumi * kfactorw * scalefactor *359.7 / 4963240.) 
    else :
        print "w+jets 200to400 b1 empty"
        h_mWsubjet_b1_wjets2.Scale( 0.)

    if h_mWsubjet_b1_wjetsp2.Integral() > 0 : 
        h_mWsubjet_b1_wjetsp2.Scale(lumi * kfactorw * scalefactor *359.7 / 4963240.) 
    else :
        print "w+jets p 200to400 b1 empty"
        h_mWsubjet_b1_wjetsp2.Scale( 0.)

    if h_mWsubjet_b1_wjets3.Integral() > 0 : 
        h_mWsubjet_b1_wjets3.Scale(lumi *kfactorw * scalefactor * 48.91/ 1963464. ) 
    else :
        print "w+jets 400to600 b1 empty"
        h_mWsubjet_b1_wjets3.Scale( 0.)
    if h_mWsubjet_b1_wjetsp3.Integral() > 0 : 
        h_mWsubjet_b1_wjetsp3.Scale(lumi *kfactorw * scalefactor * 48.91/ 1963464.) 
    else :
        print "w+jets p 400to600 b1 empty"
        h_mWsubjet_b1_wjetsp3.Scale( 0.)    

    if h_mWsubjet_b1_wjets4.Integral() > 0 : 
        h_mWsubjet_b1_wjets4.Scale(lumi * kfactorw * scalefactor * 12.05/  3722395.) 
    else :
        print "w+jets 600to800 b1 empty"
        h_mWsubjet_b1_wjets4.Scale( 0.)
    if h_mWsubjet_b1_wjetsp4.Integral() > 0 : 
        h_mWsubjet_b1_wjetsp4.Scale(lumi * kfactorw * scalefactor *12.05 / 3722395. ) 
    else :
        print "w+jets p 600to800 b1 empty"
        h_mWsubjet_b1_wjetsp4.Scale( 0.)

    if h_mWsubjet_b1_wjets5.Integral() > 0 : 
        h_mWsubjet_b1_wjets5.Scale(lumi *kfactorw * scalefactor * 5.501 / 6314257.) 
    else :
        print "w+jets 800to1200 b1 empty"
        h_mWsubjet_b1_wjets5.Scale( 0.)
    if h_mWsubjet_b1_wjetsp5.Integral() > 0 : 
        h_mWsubjet_b1_wjetsp5.Scale(lumi * kfactorw * scalefactor *5.501 / 6314257.) 
    else :
        print "w+jets p 800to1200 b1 empty"
        h_mWsubjet_b1_wjetsp5.Scale( 0.)

    if h_mWsubjet_b1_wjets6.Integral() > 0 : 
        h_mWsubjet_b1_wjets6.Scale(lumi  * kfactorw * scalefactor *1.329 / 6768156.) 
    else :
        print "w+jets 1200to2500 b1 empty"
        h_mWsubjet_b1_wjets6.Scale( 0.)
    if h_mWsubjet_b1_wjetsp6.Integral() > 0 : 
        h_mWsubjet_b1_wjetsp6.Scale(lumi * kfactorw * scalefactor *1.329 / 6768156.) 
    else :
        print "w+jets p 1200to2500 b1 empty"
        h_mWsubjet_b1_wjetsp6.Scale( 0.)

    if h_mWsubjet_b1_wjets7.Integral() > 0 : 
        h_mWsubjet_b1_wjets7.Scale(lumi *kfactorw * scalefactor * 0.03216 / 253561.) 
    else :
        print "w+jets 2500toInf b1 empty"
        h_mWsubjet_b1_wjets7.Scale( 0.)
    if h_mWsubjet_b1_wjetsp7.Integral() > 0 : 
        h_mWsubjet_b1_wjetsp7.Scale(lumi * kfactorw * scalefactor *0.03216 / 253561. ) 
    else :
        print "w+jets p 2500toInf empty"
        h_mWsubjet_b1_wjetsp7.Scale( 0.)
    # bin2
    if h_mWsubjet_b2_wjets1.Integral() > 0 : 
        h_mWsubjet_b2_wjets1.Scale(lumi * kfactorw * scalefactor *1345. / 27529599. ) 
    else :
        print "w+jets 100to200 b2 empty"
        h_mWsubjet_b2_wjets1.Scale( 0.)
    if h_mWsubjet_b2_wjetsp1.Integral() > 0 : 
        h_mWsubjet_b2_wjetsp1.Scale(lumi *kfactorw * scalefactor * 1345. / 27529599. ) 
    else :
        print "w+jets p 100to200 b2 empty"
        h_mWsubjet_b2_wjetsp1.Scale( 0.)

    if h_mWsubjet_b2_wjets2.Integral() > 0 : 
        h_mWsubjet_b2_wjets2.Scale(lumi * kfactorw * scalefactor *359.7 / 4963240.) 
    else :
        print "w+jets 200to400 b2 empty"
        h_mWsubjet_b2_wjets2.Scale( 0.)
    if h_mWsubjet_b2_wjetsp2.Integral() > 0 : 
        h_mWsubjet_b2_wjetsp2.Scale(lumi *kfactorw * scalefactor * 359.7 / 4963240.) 
    else :
        print "w+jets p 200to400 b2 empty"
        h_mWsubjet_b2_wjetsp2.Scale( 0.)

    if h_mWsubjet_b2_wjets3.Integral() > 0 : 
        h_mWsubjet_b2_wjets3.Scale(lumi * kfactorw * scalefactor *48.91/ 1963464. ) 
    else :
        print "w+jets 400to600 b2 empty"
        h_mWsubjet_b2_wjets3.Scale( 0.)
    if h_mWsubjet_b2_wjetsp3.Integral() > 0 : 
        h_mWsubjet_b2_wjetsp3.Scale(lumi * kfactorw * scalefactor *48.91/ 1963464.) 
    else :
        print "w+jets p 400to600 b2 empty"
        h_mWsubjet_b2_wjetsp3.Scale( 0.)    

    if h_mWsubjet_b2_wjets4.Integral() > 0 : 
        h_mWsubjet_b2_wjets4.Scale(lumi *  kfactorw * scalefactor *12.05/  3722395.) 
    else :
        print "w+jets 600to800 b2 empty"
        h_mWsubjet_b2_wjets4.Scale( 0.)
    if h_mWsubjet_b2_wjetsp4.Integral() > 0 : 
        h_mWsubjet_b2_wjetsp4.Scale(lumi * kfactorw * scalefactor *12.05 / 3722395. ) 
    else :
        print "w+jets p 600to800 b2 empty"
        h_mWsubjet_b2_wjetsp4.Scale( 0.)

    if h_mWsubjet_b2_wjets5.Integral() > 0 : 
        h_mWsubjet_b2_wjets5.Scale(lumi *kfactorw * scalefactor * 5.501 / 6314257.) 
    else :
        print "w+jets 800to1200 b2 empty"
        h_mWsubjet_b2_wjets5.Scale( 0.)
    if h_mWsubjet_b2_wjetsp5.Integral() > 0 : 
        h_mWsubjet_b2_wjetsp5.Scale(lumi * kfactorw * scalefactor *5.501 / 6314257.) 
    else :
        print "w+jets p 800to1200 b2 empty"
        h_mWsubjet_b2_wjetsp5.Scale( 0.)

    if h_mWsubjet_b2_wjets6.Integral() > 0 : 
        h_mWsubjet_b2_wjets6.Scale(lumi  *kfactorw * scalefactor * 1.329 / 6768156.) 
    else :
        print "w+jets 1200to2500 b2 empty"
        h_mWsubjet_b2_wjets6.Scale( 0.)
    if h_mWsubjet_b2_wjetsp6.Integral() > 0 : 
        h_mWsubjet_b2_wjetsp6.Scale(lumi * kfactorw * scalefactor *1.329 / 6768156.) 
    else :
        print "w+jets p 1200to2500 b2 empty"
        h_mWsubjet_b2_wjetsp6.Scale( 0.)

    if h_mWsubjet_b2_wjets7.Integral() > 0 : 
        h_mWsubjet_b2_wjets7.Scale(lumi * kfactorw * scalefactor *0.03216 / 253561.) 
    else :
        print "w+jets 2500toInf b2 empty"
        h_mWsubjet_b2_wjets7.Scale( 0.)
    if h_mWsubjet_b2_wjetsp7.Integral() > 0 : 
        h_mWsubjet_b2_wjetsp7.Scale(lumi *kfactorw * scalefactor * 0.03216 / 253561. ) 
    else :
        print "w+jets p 2500toInf b2 empty"
        h_mWsubjet_b2_wjetsp7.Scale( 0.)
    #bin3
    if h_mWsubjet_b3_wjets1.Integral() > 0 : 
        h_mWsubjet_b3_wjets1.Scale(lumi * kfactorw * scalefactor *1345. / 27529599. ) 
    else :
        print "w+jets 100to200 b3 empty"
        h_mWsubjet_b3_wjets1.Scale( 0.)
    if h_mWsubjet_b3_wjetsp1.Integral() > 0 : 
        h_mWsubjet_b3_wjetsp1.Scale(lumi * kfactorw * scalefactor *1345. / 27529599. ) 
    else :
        print "w+jets p 100to200 b3 empty"
        h_mWsubjet_b3_wjetsp1.Scale( 0.)

    if h_mWsubjet_b3_wjets2.Integral() > 0 : 
        h_mWsubjet_b3_wjets2.Scale(lumi *kfactorw * scalefactor * 359.7 / 4963240.) 
    else :
        print "w+jets 200to400 b3 empty"
        h_mWsubjet_b3_wjets2.Scale( 0.)
    if h_mWsubjet_b3_wjetsp2.Integral() > 0 : 
        h_mWsubjet_b3_wjetsp2.Scale(lumi *kfactorw * scalefactor * 359.7 / 4963240.) 
    else :
        print "w+jets p 200to400 b3 empty"
        h_mWsubjet_b3_wjetsp2.Scale( 0.)

    if h_mWsubjet_b3_wjets3.Integral() > 0 : 
        h_mWsubjet_b3_wjets3.Scale(lumi * kfactorw * scalefactor *48.91/ 1963464. ) 
    else :
        print "w+jets 400to600 b3 empty"
        h_mWsubjet_b3_wjets3.Scale( 0.)
    if h_mWsubjet_b3_wjetsp3.Integral() > 0 : 
        h_mWsubjet_b3_wjetsp3.Scale(lumi *kfactorw * scalefactor * 48.91/ 1963464.) 
    else :
        print "w+jets p 400to600 b3 empty"
        h_mWsubjet_b3_wjetsp3.Scale( 0.)    

    if h_mWsubjet_b3_wjets4.Integral() > 0 : 
        h_mWsubjet_b3_wjets4.Scale(lumi * kfactorw * scalefactor * 12.05/  3722395.) 
    else :
        print "w+jets 600to800 b3 empty"
        h_mWsubjet_b3_wjets4.Scale( 0.)
    if h_mWsubjet_b3_wjetsp4.Integral() > 0 : 
        h_mWsubjet_b3_wjetsp4.Scale(lumi *kfactorw * scalefactor * 12.05 / 3722395. ) 
    else :
        print "w+jets p 600to800 b3 empty"
        h_mWsubjet_b3_wjetsp4.Scale( 0.)

    if h_mWsubjet_b3_wjets5.Integral() > 0 : 
        h_mWsubjet_b3_wjets5.Scale(lumi * kfactorw * scalefactor *5.501 / 6314257.) 
    else :
        print "w+jets 800to1200 b3 empty"
        h_mWsubjet_b3_wjets5.Scale( 0.)
    if h_mWsubjet_b3_wjetsp5.Integral() > 0 : 
        h_mWsubjet_b3_wjetsp5.Scale(lumi *kfactorw * scalefactor * 5.501 / 6314257.) 
    else :
        print "w+jets p 800to1200 b3 empty"
        h_mWsubjet_b3_wjetsp5.Scale( 0.)

    if h_mWsubjet_b3_wjets6.Integral() > 0 : 
        h_mWsubjet_b3_wjets6.Scale(lumi  *kfactorw * scalefactor * 1.329 / 6768156.) 
    else :
        print "w+jets 1200to2500 b3 empty"
        h_mWsubjet_b3_wjets6.Scale( 0.)
    if h_mWsubjet_b3_wjetsp6.Integral() > 0 : 
        h_mWsubjet_b3_wjetsp6.Scale(lumi * kfactorw * scalefactor *1.329 / 6768156.) 
    else :
        print "w+jets p 1200to2500 b3 empty"
        h_mWsubjet_b3_wjetsp6.Scale( 0.)

    if h_mWsubjet_b3_wjets7.Integral() > 0 : 
        h_mWsubjet_b3_wjets7.Scale(lumi * kfactorw * scalefactor *0.03216 / 253561.) 
    else :
        print "w+jets 2500toInf b3 empty"
        h_mWsubjet_b3_wjets7.Scale( 0.)
    if h_mWsubjet_b3_wjetsp7.Integral() > 0 : 
        h_mWsubjet_b3_wjetsp7.Scale(lumi * kfactorw * scalefactor *0.03216 / 253561. ) 
    else :
        print "w+jets p 2500toInf b3  empty"
        h_mWsubjet_b3_wjetsp7.Scale( 0.)
    #bin4
    if h_mWsubjet_b4_wjets1.Integral() > 0 : 
        h_mWsubjet_b4_wjets1.Scale(lumi * kfactorw * scalefactor *1345. / 27529599. ) 
    else :
        print "w+jets 100to200 b4 empty"
        h_mWsubjet_b4_wjets1.Scale( 0.)
    if h_mWsubjet_b4_wjetsp1.Integral() > 0 : 
        h_mWsubjet_b4_wjetsp1.Scale(lumi * kfactorw * scalefactor *1345. / 27529599. ) 
    else :
        print "w+jets p 100to200 b4 empty"
        h_mWsubjet_b4_wjetsp1.Scale( 0.)

    if h_mWsubjet_b4_wjets2.Integral() > 0 : 
        h_mWsubjet_b4_wjets2.Scale(lumi *kfactorw * scalefactor * 359.7 / 4963240.) 
    else :
        print "w+jets 200to400 b4 empty"
        h_mWsubjet_b4_wjets2.Scale( 0.)
    if h_mWsubjet_b4_wjetsp2.Integral() > 0 : 
        h_mWsubjet_b4_wjetsp2.Scale(lumi *kfactorw * scalefactor * 359.7 / 4963240.) 
    else :
        print "w+jets p 200to400 b4 empty"
        h_mWsubjet_b4_wjetsp2.Scale( 0.)

    if h_mWsubjet_b4_wjets3.Integral() > 0 : 
        h_mWsubjet_b4_wjets3.Scale(lumi * kfactorw * scalefactor *48.91/ 1963464. ) 
    else :
        print "w+jets 400to600 b4 empty"
        h_mWsubjet_b4_wjets3.Scale( 0.)
    if h_mWsubjet_b4_wjetsp3.Integral() > 0 : 
        h_mWsubjet_b4_wjetsp3.Scale(lumi * kfactorw * scalefactor *48.91/ 1963464.) 
    else :
        print "w+jets p 400to600 b4 empty"
        h_mWsubjet_b4_wjetsp3.Scale( 0.)    

    if h_mWsubjet_b4_wjets4.Integral() > 0 : 
        h_mWsubjet_b4_wjets4.Scale(lumi * kfactorw * scalefactor * 12.05/  3722395.) 
    else :
        print "w+jets 600to800 b4 empty"
        h_mWsubjet_b4_wjets4.Scale( 0.)
    if h_mWsubjet_b4_wjetsp4.Integral() > 0 : 
        h_mWsubjet_b4_wjetsp4.Scale(lumi * kfactorw * scalefactor *12.05 / 3722395. ) 
    else :
        print "w+jets p 600to800 b4 empty"
        h_mWsubjet_b4_wjetsp4.Scale( 0.)

    if h_mWsubjet_b4_wjets5.Integral() > 0 : 
        h_mWsubjet_b4_wjets5.Scale(lumi *kfactorw * scalefactor * 5.501 / 6314257.) 
    else :
        print "w+jets 800to1200 b4 empty"
        h_mWsubjet_b4_wjets5.Scale( 0.)
    if h_mWsubjet_b4_wjetsp5.Integral() > 0 : 
        h_mWsubjet_b4_wjetsp5.Scale(lumi * 5.501*kfactorw * scalefactor  / 6314257.) 
    else :
        print "w+jets p 800to1200 b4 empty"
        h_mWsubjet_b4_wjetsp5.Scale( 0.)

    if h_mWsubjet_b4_wjets6.Integral() > 0 : 
        h_mWsubjet_b4_wjets6.Scale(lumi  * kfactorw * scalefactor *1.329 / 6768156.) 
    else :
        print "w+jets 1200to2500 b4 empty"
        h_mWsubjet_b4_wjets6.Scale( 0.)
    if h_mWsubjet_b4_wjetsp6.Integral() > 0 : 
        h_mWsubjet_b4_wjetsp6.Scale(lumi * kfactorw * scalefactor *1.329 / 6768156.) 
    else :
        print "w+jets p 1200to2500 b4 empty"
        h_mWsubjet_b4_wjetsp6.Scale( 0.)

    if h_mWsubjet_b4_wjets7.Integral() > 0 : 
        h_mWsubjet_b4_wjets7.Scale(lumi * kfactorw * scalefactor * 0.03216 / 253561.) 
    else :
        print "w+jets 2500toInf b4 empty"
        h_mWsubjet_b4_wjets7.Scale( 0.)
    if h_mWsubjet_b4_wjetsp7.Integral() > 0 : 
        h_mWsubjet_b4_wjetsp7.Scale(lumi * kfactorw * scalefactor *0.03216 / 253561. ) 
    else :
        print "w+jets p 2500toInf b4 empty"
        h_mWsubjet_b4_wjetsp7.Scale( 0.)



    if h_mWsubjet_b1_st1.Integral() > 0 : 
        h_mWsubjet_b1_st1.Scale(lumi * 136.02 / 3279200. ) 
    else :
        print "st top b1 empty"
        h_mWsubjet_b1_st1.Scale( 0.)
    if h_mWsubjet_b1_stp1.Integral() > 0 : 
        h_mWsubjet_b1_stp1.Scale(lumi *  136.02 / 3279200.) 
    else :
        print "st p top b1 empty"
        h_mWsubjet_b1_stp1.Scale( 0.)

    if h_mWsubjet_b1_st2.Integral() > 0 : 
        h_mWsubjet_b1_st2.Scale(lumi * 80.95 / 1682400. ) 
    else :
        print "st antitop b1 empty"
        h_mWsubjet_b1_st2.Scale( 0.)
    if h_mWsubjet_b1_stp2.Integral() > 0 : 
        h_mWsubjet_b1_stp2.Scale(lumi * 80.95 / 1682400. ) 
    else :
        print "st p antitop b1 empty"
        h_mWsubjet_b1_stp2.Scale( 0.)

    if h_mWsubjet_b2_st1.Integral() > 0 : 
        h_mWsubjet_b2_st1.Scale(lumi * 136.02 / 3279200. ) 
    else :
        print "st top b2 empty"
        h_mWsubjet_b2_st1.Scale( 0.)
    if h_mWsubjet_b2_stp1.Integral() > 0 : 
        h_mWsubjet_b2_stp1.Scale(lumi *  136.02 / 3279200.) 
    else :
        print "st p top b2 empty"
        h_mWsubjet_b2_stp1.Scale( 0.)

    if h_mWsubjet_b2_st2.Integral() > 0 : 
        h_mWsubjet_b2_st2.Scale(lumi * 80.95 / 1682400. ) 
    else :
        print "st antitop b2 empty"
        h_mWsubjet_b2_st2.Scale( 0.)
    if h_mWsubjet_b2_stp2.Integral() > 0 : 
        h_mWsubjet_b2_stp2.Scale(lumi * 80.95 / 1682400. ) 
    else :
        print "st p antitop b2 empty"
        h_mWsubjet_b2_stp2.Scale( 0.)

    if h_mWsubjet_b3_st1.Integral() > 0 : 
        h_mWsubjet_b3_st1.Scale(lumi * 136.02 / 3279200. ) 
    else :
        print "st top b3 empty"
        h_mWsubjet_b3_st1.Scale( 0.)
    if h_mWsubjet_b3_stp1.Integral() > 0 : 
        h_mWsubjet_b3_stp1.Scale(lumi *  136.02 / 3279200.) 
    else :
        print "st p top b3 empty"
        h_mWsubjet_b3_stp1.Scale( 0.)

    if h_mWsubjet_b3_st2.Integral() > 0 : 
        h_mWsubjet_b3_st2.Scale(lumi * 80.95 / 1682400. ) 
    else :
        print "st antitop b3 empty"
        h_mWsubjet_b3_st2.Scale( 0.)
    if h_mWsubjet_b3_stp2.Integral() > 0 : 
        h_mWsubjet_b3_stp2.Scale(lumi * 80.95 / 1682400. ) 
    else :
        print "st p antitop b3 empty"
        h_mWsubjet_b3_stp2.Scale( 0.)

    if h_mWsubjet_b4_st1.Integral() > 0 : 
        h_mWsubjet_b4_st1.Scale(lumi * 136.02 / 3279200. ) 
    else :
        print "st top b4 empty"
        h_mWsubjet_b4_st1.Scale( 0.)
    if h_mWsubjet_b4_stp1.Integral() > 0 : 
        h_mWsubjet_b4_stp1.Scale(lumi *  136.02 / 3279200.) 
    else :
        print "st p top b4 empty"
        h_mWsubjet_b4_stp1.Scale( 0.)

    if h_mWsubjet_b4_st2.Integral() > 0 : 
        h_mWsubjet_b4_st2.Scale(lumi * 80.95 / 1682400. ) 
    else :
        print "st antitop b4 empty"
        h_mWsubjet_b4_st2.Scale( 0.)
    if h_mWsubjet_b4_stp2.Integral() > 0 : 
        h_mWsubjet_b4_stp2.Scale(lumi * 80.95 / 1682400. ) 
    else :
        print "st p antitop b4 empty"
        h_mWsubjet_b4_stp2.Scale( 0.)

    h_mWsubjet_b1_wjets1.Sumw2()
    h_mWsubjet_b1_wjets2.Sumw2()
    h_mWsubjet_b1_wjets3.Sumw2()
    h_mWsubjet_b1_wjets4.Sumw2()
    h_mWsubjet_b1_wjets5.Sumw2()
    h_mWsubjet_b1_wjets6.Sumw2()
    h_mWsubjet_b1_wjets7.Sumw2()

    h_mWsubjet_b2_wjets1.Sumw2()
    h_mWsubjet_b2_wjets2.Sumw2()
    h_mWsubjet_b2_wjets3.Sumw2()
    h_mWsubjet_b2_wjets4.Sumw2()
    h_mWsubjet_b2_wjets5.Sumw2()
    h_mWsubjet_b2_wjets6.Sumw2()
    h_mWsubjet_b2_wjets7.Sumw2()

    h_mWsubjet_b3_wjets1.Sumw2()
    h_mWsubjet_b3_wjets2.Sumw2()
    h_mWsubjet_b3_wjets3.Sumw2()
    h_mWsubjet_b3_wjets4.Sumw2()
    h_mWsubjet_b3_wjets5.Sumw2()
    h_mWsubjet_b3_wjets6.Sumw2()
    h_mWsubjet_b3_wjets7.Sumw2()

    h_mWsubjet_b4_wjets1.Sumw2()
    h_mWsubjet_b4_wjets2.Sumw2()
    h_mWsubjet_b4_wjets3.Sumw2()
    h_mWsubjet_b4_wjets4.Sumw2()
    h_mWsubjet_b4_wjets5.Sumw2()
    h_mWsubjet_b4_wjets6.Sumw2()
    h_mWsubjet_b4_wjets7.Sumw2()


    h_mWsubjet_b1_wjets.Add(h_mWsubjet_b1_wjets1)
    h_mWsubjet_b1_wjets.Add(h_mWsubjet_b1_wjets2)
    h_mWsubjet_b1_wjets.Add(h_mWsubjet_b1_wjets3)
    h_mWsubjet_b1_wjets.Add(h_mWsubjet_b1_wjets4)
    h_mWsubjet_b1_wjets.Add(h_mWsubjet_b1_wjets5)
    h_mWsubjet_b1_wjets.Add(h_mWsubjet_b1_wjets6)
    h_mWsubjet_b1_wjets.Add(h_mWsubjet_b1_wjets7)

    h_mWsubjet_b2_wjets.Add(h_mWsubjet_b2_wjets1)
    h_mWsubjet_b2_wjets.Add(h_mWsubjet_b2_wjets2)
    h_mWsubjet_b2_wjets.Add(h_mWsubjet_b2_wjets3)
    h_mWsubjet_b2_wjets.Add(h_mWsubjet_b2_wjets4)
    h_mWsubjet_b2_wjets.Add(h_mWsubjet_b2_wjets5)
    h_mWsubjet_b2_wjets.Add(h_mWsubjet_b2_wjets6)
    h_mWsubjet_b2_wjets.Add(h_mWsubjet_b2_wjets7)

    h_mWsubjet_b3_wjets.Add(h_mWsubjet_b3_wjets1)
    h_mWsubjet_b3_wjets.Add(h_mWsubjet_b3_wjets2)
    h_mWsubjet_b3_wjets.Add(h_mWsubjet_b3_wjets3)
    h_mWsubjet_b3_wjets.Add(h_mWsubjet_b3_wjets4)
    h_mWsubjet_b3_wjets.Add(h_mWsubjet_b3_wjets5)
    h_mWsubjet_b3_wjets.Add(h_mWsubjet_b3_wjets6)
    h_mWsubjet_b3_wjets.Add(h_mWsubjet_b3_wjets7)

    h_mWsubjet_b4_wjets.Add(h_mWsubjet_b4_wjets1)
    h_mWsubjet_b4_wjets.Add(h_mWsubjet_b4_wjets2)
    h_mWsubjet_b4_wjets.Add(h_mWsubjet_b4_wjets3)
    h_mWsubjet_b4_wjets.Add(h_mWsubjet_b4_wjets4)
    h_mWsubjet_b4_wjets.Add(h_mWsubjet_b4_wjets5)
    h_mWsubjet_b4_wjets.Add(h_mWsubjet_b4_wjets6)
    h_mWsubjet_b4_wjets.Add(h_mWsubjet_b4_wjets7)

    h_mWsubjet_b1_wjetsp.Add(h_mWsubjet_b1_wjetsp1)
    h_mWsubjet_b1_wjetsp.Add(h_mWsubjet_b1_wjetsp2)
    h_mWsubjet_b1_wjetsp.Add(h_mWsubjet_b1_wjetsp3)
    h_mWsubjet_b1_wjetsp.Add(h_mWsubjet_b1_wjetsp4)
    h_mWsubjet_b1_wjetsp.Add(h_mWsubjet_b1_wjetsp5)
    h_mWsubjet_b1_wjetsp.Add(h_mWsubjet_b1_wjetsp6)
    h_mWsubjet_b1_wjetsp.Add(h_mWsubjet_b1_wjetsp7)

    h_mWsubjet_b2_wjetsp.Add(h_mWsubjet_b2_wjetsp1)
    h_mWsubjet_b2_wjetsp.Add(h_mWsubjet_b2_wjetsp2)
    h_mWsubjet_b2_wjetsp.Add(h_mWsubjet_b2_wjetsp3)
    h_mWsubjet_b2_wjetsp.Add(h_mWsubjet_b2_wjetsp4)
    h_mWsubjet_b2_wjetsp.Add(h_mWsubjet_b2_wjetsp5)
    h_mWsubjet_b2_wjetsp.Add(h_mWsubjet_b2_wjetsp6)
    h_mWsubjet_b2_wjetsp.Add(h_mWsubjet_b2_wjetsp7)

    h_mWsubjet_b3_wjetsp.Add(h_mWsubjet_b3_wjetsp1)
    h_mWsubjet_b3_wjetsp.Add(h_mWsubjet_b3_wjetsp2)
    h_mWsubjet_b3_wjetsp.Add(h_mWsubjet_b3_wjetsp3)
    h_mWsubjet_b3_wjetsp.Add(h_mWsubjet_b3_wjetsp4)
    h_mWsubjet_b3_wjetsp.Add(h_mWsubjet_b3_wjetsp5)
    h_mWsubjet_b3_wjetsp.Add(h_mWsubjet_b3_wjetsp6)
    h_mWsubjet_b3_wjetsp.Add(h_mWsubjet_b3_wjetsp7)

    h_mWsubjet_b4_wjetsp.Add(h_mWsubjet_b4_wjetsp1)
    h_mWsubjet_b4_wjetsp.Add(h_mWsubjet_b4_wjetsp2)
    h_mWsubjet_b4_wjetsp.Add(h_mWsubjet_b4_wjetsp3)
    h_mWsubjet_b4_wjetsp.Add(h_mWsubjet_b4_wjetsp4)
    h_mWsubjet_b4_wjetsp.Add(h_mWsubjet_b4_wjetsp5)
    h_mWsubjet_b4_wjetsp.Add(h_mWsubjet_b4_wjetsp6)
    h_mWsubjet_b4_wjetsp.Add(h_mWsubjet_b4_wjetsp7)

    h_mWsubjet_b1_st1.Sumw2()
    h_mWsubjet_b1_st2.Sumw2()

    h_mWsubjet_b2_st1.Sumw2()
    h_mWsubjet_b2_st2.Sumw2()

    h_mWsubjet_b3_st1.Sumw2()
    h_mWsubjet_b3_st2.Sumw2()

    h_mWsubjet_b4_st1.Sumw2()
    h_mWsubjet_b4_st2.Sumw2()

    h_mWsubjet_b1_st.Add(h_mWsubjet_b1_st1)
    h_mWsubjet_b1_st.Add(h_mWsubjet_b1_st2)

    h_mWsubjet_b2_st.Add(h_mWsubjet_b2_st1)
    h_mWsubjet_b2_st.Add(h_mWsubjet_b2_st2)

    h_mWsubjet_b3_st.Add(h_mWsubjet_b3_st1)
    h_mWsubjet_b3_st.Add(h_mWsubjet_b3_st2)

    h_mWsubjet_b4_st.Add(h_mWsubjet_b4_st1)
    h_mWsubjet_b4_st.Add(h_mWsubjet_b4_st2)

    h_mWsubjet_b1_stp.Add(h_mWsubjet_b1_stp1)
    h_mWsubjet_b1_stp.Add(h_mWsubjet_b1_stp2)

    h_mWsubjet_b2_stp.Add(h_mWsubjet_b2_stp1)
    h_mWsubjet_b2_stp.Add(h_mWsubjet_b2_stp2)

    h_mWsubjet_b3_stp.Add(h_mWsubjet_b3_stp1)
    h_mWsubjet_b3_stp.Add(h_mWsubjet_b3_stp2)

    h_mWsubjet_b4_stp.Add(h_mWsubjet_b4_stp1)
    h_mWsubjet_b4_stp.Add(h_mWsubjet_b4_stp2)

    print "          ****Cut Flow Table****         "
    print "total number of events of type {0:s} passing each cut".format(options.dtype) 
    print "..................................................."
    print "                Electrons                          "
    print "..................................................."
    print "Pt cut:                    {0}".format(passcuts[0]  )
    print "Eta cut:                   {0}".format(passcuts[1]  ) 
    print "MET cut :                  {0}".format(passcuts[2]  ) 
    print "ALL Electron cuts :        {0}".format(passcuts[18] )
    print "..................................................."
    print "                   Muons                           "
    print "..................................................."
    print "Pt cut:                    {0}".format(passcuts[3]  )
    print "Eta cut:                   {0}".format(passcuts[19] ) 
    print "MET cut :                  {0}".format(passcuts[20] ) 
    print "Iso cut :                  {0}".format(passcuts[4]  ) 
    print "ALL Muon cuts :            {0}".format(passcuts[21] )
    print "..................................................."
    print "                  Lepton                           "
    print "..................................................."
    print "DR(lepton, AK4) cut:       {0}".format(passcuts[22] )
    print "DR(lepton, AK8) cut:       {0}".format(passcuts[7] )
    print "ALL Lepton cuts:           {0}".format(passcuts[5]  )
    print "..................................................."
    print "                   AK4                             "
    print "..................................................."
    print "Pt cut:                    {0}".format(passcuts[13]  )
    print "CSVv2 Bdisc cut:           {0}".format(passcuts[12]  )
    print "DR(AK4, AK8) cut:          {0}".format(passcuts[23]  )
    print "ALL AK4 cuts:              {0}".format(passcuts[24]  )

    if options.Type2:

        print "..................................................."
        print "                 Type 2 AK8                        "
        print "..................................................."



        print "total passing W jet pt and eta cut:   " + str(passcuts[14] ) #passWkin)
        print "total passing W jet mass cut:         " + str(passcuts[16] ) #pass7)

        print "total passing pre-selection : " + str(passcuts[17] ) #passkin FIX THIS)

        print "total passing final selection : " + str(passcuts[18] ) #passOp)

    else :
        print "..................................................."
        print "                 Type 1 AK8                        "
        print "..................................................."
        print "total passing top pt cut: " + str(passcuts[8] ) #passkin)
        print "total passing top tau32 cut: " + str(passcuts[9] ) #passT)
        print "total passing top mass: " + str(passcuts[10] ) # pass4)

        print "total passing 2D cut: " + str(passcuts[11] ) #pass2D)
        print "total passing B tag bdisc: " + str(passcuts[12] ) #passB)
        print "total passing B tag pt: " + str(passcuts[13] ) #pass5)

        print "total passing W subjet pt and eta cut:   " + str(passcuts[14] ) #passWkin)
        print "total passing W subjet tau21 cut:        " + str(passcuts[15]) #pass6)
        print "total passing W subjet mass cut:         " + str(passcuts[16] ) #pass7)


        print "total passing pre-selection : " + str(passcuts[17] ) #passkin FIX THIS)

        print "total passing final selection : " + str(passcuts[18] ) #passOp)



    fout.cd() 
    fout.Write()
    fout.Close()

if __name__ == "__main__" :
    Wtag_Selector(sys.argv)
