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

    parser.add_option('--writeTree', action='store_true',
                      default=False,
                      dest='writeTree',
                      help='Write a ttree after the selection but before tau21 and tight W mass cuts')

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
                      help='Do you want to apply selection for type 2 tops as described in AN-16-215 ?')

    parser.add_option('--applyHIPCorr', action='store_true',
                      default=False,
                      dest='applyHIPCorr',
                      help='Do you want apply the HIP corrections to the muons ?')

    parser.add_option('--applyElSF', action='store_true',
                      default=False,
                      dest='applyElSF',
                      help='Do you want apply the scale factors to the electrons ?')
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
    if options.applyElSF :
        def getgsfTrackEffScaleFactor(eleta) : #{
            finSF = ROOT.TFile.Open( "/home/amp/WJets/80xTrees/SimpleSelect/egammaEffitxt_SF2D.root","READ")
            th2_EGamma_SF2D     = finSF.Get("EGamma_SF2D")
            gsfSF = th2_EGamma_SF2D.Eval( eleta)
            return gsfSF
            #}  
    if options.applyHIPCorr :
        if options.isMC :
            c=ROOT.KalmanMuonCalibrator("MC_80X_13TeV")
        else :
            c=ROOT.KalmanMuonCalibrator("DATA_80X_13TeV")
        def getHIPMuonCorr(pt, eta, phi, charge) : #{
            # apply HIP muon corrections as described here https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonScaleResolKalman
            if charge < 0. :
                chargeSign = -1 
            if charge > 0. :
                chargeSign = 1    
            CorrMuPt = c.getCorrectedPt(pt, eta, phi, charge)
            dpt = abs( pt- CorrMuPt )
            dptopt = dpt/ pt
            c.getCorrectedError(pt, eta, dptopt)#'Recall! This correction is only valid after smearing'
            c.smear(pt, eta)
            #print 'propagate the statistical error of the calibration
            #print 'first get number of parameters'
            N=c.getN()
            #print N,'parameters'
            for i in range(0,N):
                c.vary(i,+1)
                #print 'variation',i,'ptUp', c.getCorrectedPt(pt, eta phi, charge)
                c.vary(i,-1)
                #print 'variation',i,'ptDwn', c.getCorrectedPt(pt, eta phi, charge)
            c.reset()
            #print 'propagate the closure error 
            c.varyClosure(1)
            newpt = c.getCorrectedPt(pt, eta, phi, charge)
            if options.verbose : print 'After closure shift Pt = {0:4.3f}'.format(newpt)
            return newpt
            #} 


    # Create output ROOT file to store ttree after selection-When selection is good, produce final ttrees with No wtag cuts for Roofit input
    if options.writeTree :
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
        LeptonLoose         = array('f', [-1.])
        LeptonTight         = array('f', [-1.])
        LeptonCharge        = array('f', [-1.])

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
        TreeSemiLept.Branch('LeptonCharge'        , LeptonCharge        ,  'LeptonCharge/F'         )
        TreeSemiLept.Branch('LeptonLoose'         , LeptonLoose         ,  'LeptonLoose/F'         )
        TreeSemiLept.Branch('LeptonTight'         , LeptonTight         ,  'LeptonTight/F'         )        
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
        fout= ROOT.TFile('./output80xselector/histos_80x_' +options.dtype + '_'+ options.filestr + '.root', "RECREATE")
        filein =  './%s/Puppi_%s_80Xv2p0Ntuple.root'%(options.dtype, options.dtype)


    binlimit = 200.
    numbins = 300

    h_mWsubjet_b1  = ROOT.TH1F("h_mWsubjet_b1", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b2  = ROOT.TH1F("h_mWsubjet_b2", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b3  = ROOT.TH1F("h_mWsubjet_b3", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b4  = ROOT.TH1F("h_mWsubjet_b4", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b1p  = ROOT.TH1F("h_mWsubjet_b1p", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b2p  = ROOT.TH1F("h_mWsubjet_b2p", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b3p  = ROOT.TH1F("h_mWsubjet_b3p", "; ;  ", numbins, 0, binlimit)
    h_mWsubjet_b4p  = ROOT.TH1F("h_mWsubjet_b4p", "; ;  ", numbins, 0, binlimit)

    binlimit2 = 500.
    numbins2 = 300

    h_lepPt     = ROOT.TH1F("h_lepPt", "; ;  ", numbins2, 0, binlimit2)
    h_lepEta    = ROOT.TH1F("h_lepEta", "; ;  ", numbins2, -3., 3.)
    h_lepHt     = ROOT.TH1F("h_lepHt", "; ;  ", numbins2, 0, binlimit2)
    h_lepHtLep  = ROOT.TH1F("h_lepHtLep", "; ;  ", numbins2, 0, binlimit2)
    h_lepSt     = ROOT.TH1F("h_lepSt", "; ;  ", numbins2, 0, binlimit2)


    # Counters for cut flow table
    passcuts = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    fillTree = False
    passPre = 0
    passPost = 0

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
    LeptonCharge        = array.array('f', [-1.])
    LeptonLoose         = array.array('f', [-1.])
    LeptonTight         = array.array('f', [-1.]) 
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
    t.SetBranchAddress('BJet2bDisc'   , BJetbDisc )
    t.SetBranchAddress('BJet2Pt'      , BJetPt    )
    t.SetBranchAddress('BJet2Eta'     , BJetEta   )
    t.SetBranchAddress('BJet2Phi'     , BJetPhi   )
    t.SetBranchAddress('BJet2Mass'    , BJetMass  )
    t.SetBranchAddress('LeptonType'          , LeptonType          )
    t.SetBranchAddress('LeptonPt'            , LeptonPt            )
    t.SetBranchAddress('LeptonEta'           , LeptonEta           )
    t.SetBranchAddress('LeptonPhi'           , LeptonPhi           )
    t.SetBranchAddress('LeptonEnergy'        , LeptonEnergy        )
    t.SetBranchAddress('LeptonIso'           , LeptonIso           )
    t.SetBranchAddress('LeptonPtRel'         , LeptonPtRel         )
    t.SetBranchAddress('LeptonDRMin'         , LeptonDRMin         )
    t.SetBranchAddress('LeptonCharge'        , LeptonCharge        )
    t.SetBranchAddress('LeptonLoose'         , LeptonLoose         )
    t.SetBranchAddress('LeptonTight'         , LeptonTight         )
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
    t.SetBranchStatus('BJet2Pt' , 1)
    t.SetBranchStatus('BJet2Eta' , 1)
    t.SetBranchStatus('BJet2Phi' , 1 )
    t.SetBranchStatus('BJet2Mass' , 1)
    t.SetBranchStatus('BJet2bDisc' , 1)
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
    t.SetBranchStatus('FatJetSDsubjetBpt',1)
    t.SetBranchStatus('FatJetSDsubjetWmass',1)
    t.SetBranchStatus ('SemiLeptTrig', 1)
    t.SetBranchStatus ('DeltaPhiLepFat'  ,1   )
    t.SetBranchStatus ('DeltaRLepFat'    ,1   )
    t.SetBranchStatus ('DeltaRAK4AK8'    ,1   )
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
    t.SetBranchStatus ('LeptonCharge'        , 1)
    t.SetBranchStatus ('LeptonLoose'         , 1)
    t.SetBranchStatus ('LeptonTight'         , 1)
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
        LepPhi = theLepton.Phi()
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
        drAK4AK8 = DeltaRAK4AK8[0]

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

        # applying High Intensity Proton (HIP) muon corrections
        if options.applyHIPCorr and LepType == 2 and LepPt > 50 and abs(LepEta) < 2.1 and LeptonIso[0] < 0.1 and FatJetSD_pt > 200. : 
            HIPcorrPt = getHIPMuonCorr(LepPt, LepEta, LepPhi, +1) # ??? FIX THIS last should be LeptonCharge[0] 
            LepPt = HIPcorrPt

        # getting electron scale factors
        if options.applyElSF and LepType == 1 :
            ElScaleFactor = getgsfTrackEffScaleFactor(LepEta)


        realw = -1
        fakew = -1
        # Get Generator level matching Info
        if options.match and options.dtype == 'ttjets':
            # FIX THIS to read the Matched tree and get info or re-do the gen matching
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
        passLepcut =  passLepDrmin and (  passEl or passMu  ) # FIX this apply passHemidR 

        if passLepDrmin :
            passcuts[22] += 1
        if passHemidR:
            passcuts[7] += 1
        if passLepcut :
            passcuts[5] += 1

        if options.verbose and passLepcut and passEl: 
            print "Electron:  pt {0:3.2f}, eta {1:3.2f}, MET_pt {2:3.2f}".format(LepPt, abs(LepEta),  MET_pt) 
        if options.verbose and passLepcut and passMu: 
            print "Muon:  pt {0:3.2f}, eta {1:3.2f}, MET_pt {2:3.2f}".format(LepPt, abs(LepEta),  MET_pt) 

        # Lepton cuts applied
        if not passLepcut : continue

        TheWeight = weightS
        # applying electron scale factors
        if LepType == 1 and options.applyElSF :
            TheWeight = weightS * ElScaleFactor 

        fout.cd()
        h_lepPt.Fill(LepPt       , TheWeight)
        h_lepEta.Fill(LepEta     , TheWeight)

        HtLep = LepPt + MET_pt
        h_lepHt.Fill(HtLep       , TheWeight)

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
        Ht = 0.
        for iak4,ak4jet in enumerate(NearestAK4JetPt) :
            Ht += NearestAK4JetPt[iak4]

        h_lepHt.Fill(Ht ,     TheWeight )

        St = Ht + HtLep
        h_lepSt.Fill(St ,     TheWeight )

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

        else :                                                                                # Type 1 AK8 selection
            passWPre =   W_m > 50. 

            passWPostM = 55. < W_m < 115.
            passWPosttau = 0.1 < W_tau21 < options.tau21Cut 

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
            if passWPosttau:
                passcuts[15] +=1
            if passWPostM:
                passcuts[16] +=1
        
        # Type 2 cuts applied
        if options.Type2 :
            if passKin2:
                passPre +=1
                if  passWTagmass : # passWPosttau2 passWPostM2  
                    passPost +=1                                                        
                    fillTree = True

        # Type 1 cuts applied
        if not options.Type2 :
            if passKin:
                passPre +=1
                topandKin = passTopTagtau and passTopTagmass  and passWKin
                if  ( topandKin and pass2DCut ):
                    passPost +=1  
                    fillTree = True
                    if options.verbose < 0. :
                        print "Fat Jet: SD Mass {0:6.3}, Pt {1:6.3}, tau32 {2:0.4} - W Subjet: SD Mass {3:6.3}, Pt {4:6.3}, tau21 {5:0.4} - dRLepFat {6:6.3} ".format(FatJetSD_m, FatJetSD_pt, tau32, W_m, W_pt, W_tau21, DeltaRLepFat[0] )

        # FIX THIS -Fill the Combined Trees after selection here for later use as RooFit Input
        if fillTree:
            
            if options.writeTree :
                print "Tree writing is not yet enabled"

                tree.Fill()
                            
            if options.Type2 :
                thatMass = FatJetSD_m
                passPost = passWPosttau2
            else :
                thatMass = W_m
                passPost = passWPosttau

            if (options.dtype != 'data'): # ??? working here
                h_mWsubjet_MC.Fill(thatMass , TheWeight )
            if (options.dtype == 'data'):
                h_mWsubjet_Data.Fill(thatMass , TheWeight )
            if (options.dtype == 'ttjets') :
                h_mWsubjet_ttjets.Fill(thatMass , TheWeight )

            if ( W_pt > 200.0 and W_pt < 300.0 ):
                h_mWsubjet_b1p.Fill(thatMass, TheWeight )
            if ( W_pt > 300.0 and W_pt < 400.0 ) :                       
                h_mWsubjet_b2p.Fill(thatMass , TheWeight )
            if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                h_mWsubjet_b3p.Fill(thatMass, TheWeight )
            if ( W_pt > 500.0 ) : 
                h_mWsubjet_b4p.Fill(thatMass, TheWeight )

            if passPost :
                passOp += 1 
                if ( W_pt > 200.0 and W_pt < 300.0 ):
                    h_mWsubjet_b1.Fill(thatMass, TheWeight )
                if ( W_pt > 300.0 and W_pt < 400.0 ) :                       
                    h_mWsubjet_b2.Fill(thatMass , TheWeight )
                if ( W_pt > 400.0 and W_pt < 500.0 ) : 
                    h_mWsubjet_b3.Fill(thatMass, TheWeight )
                if ( W_pt > 500.0 ) : 
                    h_mWsubjet_b4.Fill(thatMass, TheWeight )


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
    print "DR(lepton, AK8) cut:       {0}".format(passcuts[7]  )
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



        print "total passing W jet pt and eta cut:   " + str(passcuts[14] ) 
        print "total passing W jet mass cut:         " + str(passcuts[16] ) 

        print "total passing pre-selection : " + str(passPre ) 

        print "total passing final selection : " + str(passPost )

    else :
        print "..................................................."
        print "                 Type 1 AK8                        "
        print "..................................................."
        print "total passing top pt cut: " + str(passcuts[8] ) 
        print "total passing top tau32 cut: " + str(passcuts[9] ) 
        print "total passing top mass: " + str(passcuts[10] ) 

        print "total passing 2D cut: " + str(passcuts[11] ) 
        print "total passing B tag bdisc: " + str(passcuts[12] ) 
        print "total passing B tag pt: " + str(passcuts[13] ) 

        print "total passing W subjet pt and eta cut:   " + str(passcuts[14] )
        print "total passing W subjet tau21 cut:        " + str(passcuts[15])
        print "total passing W subjet mass cut:         " + str(passcuts[16] )


        print "total passing pre-selection : " + str(passPre ) 

        print "total passing final selection : " + str(passPost )


    h_mWsubjet_b1.Write()
    h_mWsubjet_b2.Write()
    h_mWsubjet_b3.Write()
    h_mWsubjet_b4.Write()
    h_mWsubjet_b1p.Write()
    h_mWsubjet_b2p.Write()
    h_mWsubjet_b3p.Write()
    h_mWsubjet_b4p.Write()
    h_lepPt.Write()
    h_lepEta.Write()
    h_lepHt.Write()
    h_lepHtLep.Write()
    h_lepSt.Write()
    #fout.Write()
    fout.Close()

if __name__ == "__main__" :
    Wtag_Selector(sys.argv)
