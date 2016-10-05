#!it/usr/bin/env python
from optparse import OptionParser
from numpy import *
import CMS_lumi, tdrstyle
import ROOT
import array
import math


####    You should fit the pretag in EACH bin separately, and then constrain the tagged distribution to that in each bin.



parser = OptionParser()

parser.add_option('--infile', type='string', action='store',
                  dest='infile',
                  default = "",
                  help='Input file')

parser.add_option('--maxEvents', type='int', action='store',
              default=-1,
              dest='maxEvents',
              help='Number of events to run. -1 is all events')

parser.add_option('--TreeMaker', action='store_true',
                  default=False,
                  dest='TreeMaker',
                  help='Are the ttrees produced using B2GTTbarTreeMaker.cc ?')

parser.add_option('--treeLocation', type='string', action='store',
                  dest='treeLocation',
                  default = 'Last80xTrees',#'80xTTrees',
                  help='directory ??? where CRAB output ttrees created by NtupleReader are located /store/group/lpctlbsm/aparker/???') 

parser.add_option('--CSelect', action='store_true',
                  default=False,
                  dest='CSelect',
                  help='Are the histos made using the .cc code from jim whuch loops over the treemaker trees (only makes sense to use with --treemaker) ?')

parser.add_option('--passTau21', action='store_true',
                  default=True,
                  dest='passTau21',
                  help='Plot the mass of W candidate passing tau21 cut')

parser.add_option('--failTau21', action='store_true',
                  default=True,
                  dest='failTau21',
                  help='Plot the mass of W candidate failing the tau21 cut')

parser.add_option('--PlotPtTypes', action='store_true',
              default=False,
              dest='PlotPtTypes',
              help='Do you want to plot the Pts of type 1 vs Type 2 W jet candidates???')

parser.add_option('--filestr', type='string', action='store',
                  dest='filestr',
                  default = "nom",
                  help='Label for plots')

parser.add_option('--Type2', action='store_true',
                  default=True,
                  dest='Type2',
                  help='Do you want to apply selection for type 2 tops as described in AN-16-215 ?')

parser.add_option('--minval', type='float', action='store',
                  dest='minval',
                  default = 0.,
                  help='Minval for the plot')

parser.add_option('--maxval', type='float', action='store',
                  dest='maxval',
                  default = 250.,
                  help='Maxval for the plot')

parser.add_option('--80X', action='store_true',
                  default=True,
                  dest='80X',
                  help='Are the ttrees produced using CMSSW 80X?')

parser.add_option('--nbins', type='int', action='store',
                  dest='nbins',
                  default = 25,
                  help='Nbins for the plot')

parser.add_option('--legleft',  action='store_true',
                  dest='legleft',
                  default = False,
                  help='Plot legend on the left')

parser.add_option('--pre',  action='store_true',
                  dest='pre',
                  default = False,
                  help='Plot selection before tog tag cut.')

parser.add_option('--Eldata',  action='store_true',
                  dest='Eldata',
                  default = False,
                  help='Plot only electron data')

parser.add_option('--Mudata',  action='store_true',
                  dest='Mudata',
                  default = False,
                  help='Plot only muon data')

parser.add_option('--allMC', action='store_true',
                  default=False,
                  dest='allMC',
                  help='Do you want to plot all MC? (or just ttjets)')

parser.add_option('--quickPlot', action='store_true',
                  default=False,
                  dest='quickPlot',
                  help='only plot lepton pt and tau21 ?')

parser.add_option('--ttSF', action='store_true',
                  default=False,
                  dest='ttSF',
                  help='Apply a ttbar scale factor computed here ?')

parser.add_option('--fixFit',  action='store_true',
                  dest='fixFit',
                  default = True,
                  help='Constrain the mean and sigma of Gaussian.')

parser.add_option('--max0', type='float', action='store',
                  dest='max0',
                  default = 115.,
                  help='maximum mass for fitting range in W mass distribution for bin 0')

parser.add_option('--min0', type='float', action='store',
                  dest='min0',
                  default = 55.,
                  help='minimum mass for fitting range in W mass distribution for bin 0')

parser.add_option('--max1', type='float', action='store',
                  dest='max1',
                  default = 115.,
                  help='maximum mass for fitting range in W mass distribution for bin 1')

parser.add_option('--min1', type='float', action='store',
                  dest='min1',
                  default = 55.,
                  help='minimum mass for fitting range in W mass distribution for bin 1')

parser.add_option('--max2', type='float', action='store',
                  dest='max2',
                  default = 115.,
                  help='maximum mass for fitting range in W mass distribution for bin 2')

parser.add_option('--min2', type='float', action='store',
                  dest='min2',
                  default = 65.,
                  help='minimum mass for fitting range in W mass distribution for bin 2')

parser.add_option('--max3', type='float', action='store',
                  dest='max3',
                  default = 115.,
                  help='maximum mass for fitting range in W mass distribution for bin 3')

parser.add_option('--min3', type='float', action='store',
                  dest='min3',
                  default = 55.,
                  help='minimum mass for fitting range in W mass distribution for bin 3')

(options, args) = parser.parse_args()
argv = []

#This script was adapted from original myMacro.py from ghm.web.cern.ch/gmh/plots/ 

if options.TreeMaker and (not options.Type2):
    plotdir = 'JWsubjetSF'
if options.TreeMaker and  options.Type2 :
    plotdir = 'JWjetSF'
if (not options.TreeMaker) and (not options.Type2):
    plotdir = 'WsubjetSF'
if ( not options.TreeMaker) and  options.Type2 :
    plotdir = 'WjetSF'
# define the scaling operations

def scaleST(hstT1_, hstT2_, hstT3_, hstT4_):
    hstT_ = hstT1_.Clone()
    hstT_.Reset()
    hst34_ = hstT3_.Clone()
    hst34_.Reset()
    if hstT1_.Integral() > 0 : 
        hstT1_.Scale(lumi * 136.02 / 3279200. ) 
    else :
        print "st top bin {0} empty".format(int(ipt))
        hstT1_.Scale( 0.)
    if hstT2_.Integral() > 0 : 
        hstT2_.Scale(lumi * 80.95 / 1682400. ) 
    else :
        print "st antitop bin {0} empty".format(int(ipt))
        hstT2_.Scale( 0.)
    hst34_ = hstT3_.Clone()
    hst34_.SetDirectory(0)
    hst34_.Add(hstT4_)
    if hst34_.Integral() > 0 : 
        hst34_.Scale(lumi * 71.7 / (998400.+985000.) ) 
    else :
        print "st tW bin {0} empty".format(int(ipt))
        hst34_.Scale( 0.)
    hstT_ = hstT1_.Clone()
    hstT_.SetDirectory(0)
    hstT_.Sumw2()
    hstT_.Add(hstT2_)
    hstT_.Add(hst34_)
    return hstT_

def scaleSTp(hstTp1_, hstTp2_, hstTp3_, hstTp4_):

    if ipt <= 4 :
        if hstTp1_.Integral() > 0 : 
            hstTp1_.Scale(lumi *  136.02 / 3279200.) 
        else :
            print "st p top bin {0} empty".format(int(ipt))
            hstTp1_.Scale( 0.)
        if hstTp2_.Integral() > 0 : 
            hstTp2_.Scale(lumi * 80.95 / 1682400. ) 
        else :
            print "st p antitop bin {0} empty".format(int(ipt))
            hstTp2_.Scale( 0.)
        hstp34_ = hstTp3_.Clone()
        hstp34_.SetDirectory(0)
        hstp34_.Add(hstTp4_)
        if hstp34_.Integral() > 0 : 
            hstp34_.Scale(lumi * 71.7 / (998400.+985000.) ) 
        else :
            print "st p tW  bin {0} empty".format(int(ipt))
            hstp34_.Scale( 0.)
    hstTp_ = hstTp1_.Clone()
    hstTp_.SetDirectory(0)
    hstTp_.Sumw2()
    hstTp_.Add(hstTp2_)
    hstTp_.Add(hstp34_)
 
    return hstTp_

def scaleTT(httbarT_):
    if httbarT_.Integral() > 0 : 
        httbarT_.Scale(lumi* 831.76 /  91061600. *0.75) # fix this when tt sample is complete

        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt bin {0} empty".format(int(ipt))
        httbarT_.Scale( 0.)
    return httbarT_

def scaleTTp(httbarTp_):
    if ipt <=4 :
        if httbarTp_.Integral() > 0 : 
            httbarTp_.Scale(lumi * 831.76 /  91061600.) # hdataT.GetEntries()/ httbarT.Integral())
        else :
            print "tt p bin {0} empty".format(int(ipt))
            httbarTp_.Scale( 0.)
    return httbarTp_

def scaleWjets(hwjetsT1_, hwjetsT2_, hwjetsT3_, hwjetsT4_, hwjetsT5_, hwjetsT6_, hwjetsT7_) :
    hwjetsT_ = hwjetsT1_.Clone()
    hwjetsT_.Reset()
    scalefactor = 1.
    kfactorw = 1.21
    if hwjetsT1_.Integral() > 0 : 
        hwjetsT1_.Scale(lumi * kfactorw * scalefactor *1345. / 27529599. ) 
    else :
        print "w+jets 100to200 b{0} empty".format(str(ipt))
        hwjetsT1_.Scale( 0.)
    if hwjetsT2_.Integral() > 0 : 
        hwjetsT2_.Scale(lumi *kfactorw * scalefactor * 359.7 / 4963240.) 
    else :
        print "w+jets 200to400 b{0} empty".format(str(ipt))
        hwjetsT2_.Scale( 0.)
    if hwjetsT3_.Integral() > 0 : 
        hwjetsT3_.Scale(lumi * kfactorw * scalefactor *48.91/ 1963464. ) 
    else :
        print "w+jets 400to600 b{0} empty".format(str(ipt))
        hwjetsT3_.Scale( 0.)
    if hwjetsT4_.Integral() > 0 : 
        hwjetsT4_.Scale(lumi * kfactorw * scalefactor * 12.05/  3722395.) 
    else :
        print "w+jets 600to800 b{0} empty".format(str(ipt))
        hwjetsT4_.Scale( 0.)
    if hwjetsT5_.Integral() > 0 : 
        hwjetsT5_.Scale(lumi *kfactorw * scalefactor * 5.501 / 6314257.) 
    else :
        print "w+jets 800to1200 b{0} empty".format(str(ipt))
        hwjetsT5_.Scale( 0.)
    if hwjetsT6_.Integral() > 0 : 
        hwjetsT6_.Scale(lumi  * kfactorw * scalefactor *1.329 / 6768156.) 
    else :
        print "w+jets 1200to2500 b{0} empty".format(str(ipt))
        hwjetsT6_.Scale( 0.)
    if hwjetsT7_.Integral() > 0 : 
        hwjetsT7_.Scale(lumi * kfactorw * scalefactor * 0.03216 / 253561.) 
    else :
        print "w+jets 2500toInf b{0} empty".format(str(ipt))
        hwjetsT7_.Scale( 0.)

    hwjetsT_ = hwjetsT1_.Clone()
    hwjetsT_.SetDirectory(0)
    hwjetsT_.Sumw2()
    hwjetsT_.Add(hwjetsT2_)
    hwjetsT_.Add(hwjetsT3_)
    hwjetsT_.Add(hwjetsT4_)
    hwjetsT_.Add(hwjetsT5_)
    hwjetsT_.Add(hwjetsT6_)
    hwjetsT_.Add(hwjetsT7_)
    return hwjetsT_

def scaleWjetsp(hwjetsTp1_, hwjetsTp2_, hwjetsTp3_, hwjetsTp4_, hwjetsTp5_, hwjetsTp6_, hwjetsTp7_) :
    scalefactor = 1
    if ipt <=4:
        if hwjetsTp1_.Integral() > 0 : 
            hwjetsTp1_.Scale(lumi * kfactorw * scalefactor *1345. / 27529599. ) 
        else :
            print "w+jets p 100to200 b{0} empty".format(str(ipt))
            hwjetsTp1_.Scale( 0.)
        if hwjetsTp2_.Integral() > 0 : 
            hwjetsTp2_.Scale(lumi *kfactorw * scalefactor * 359.7 / 4963240.) 
        else :
            print "w+jets p 200to400 b{0} empty".format(str(ipt))
            hwjetsTp2_.Scale( 0.)
        if hwjetsTp3_.Integral() > 0 : 
            hwjetsTp3_.Scale(lumi * kfactorw * scalefactor *48.91/ 1963464.) 
        else :
            print "w+jets p 400to600 b{0} empty".format(str(ipt))
            hwjetsTp3_.Scale( 0.) 
        if hwjetsTp4_.Integral() > 0 : 
            hwjetsTp4_.Scale(lumi * kfactorw * scalefactor *12.05 / 3722395. ) 
        else :
            print "w+jets p 600to800 b4 empty"
            hwjetsTp4_.Scale( 0.)
        if hwjetsTp5.Integral() > 0 : 
            hwjetsTp5.Scale(lumi * 5.501*kfactorw * scalefactor  / 6314257.) 
        else :
            print "w+jets p 800to1200 b4 empty"
            hwjetsTp5.Scale( 0.)
        if hwjetsTp6.Integral() > 0 : 
            hwjetsTp6.Scale(lumi * kfactorw * scalefactor *1.329 / 6768156.) 
        else :
            print "w+jets p 1200to2500 b4 empty"
            hwjetsTp6.Scale( 0.)
            if hwjetsT7p.Integral() > 0 : 
                hwjetsT7p.Scale(lumi * kfactorw * scalefactor *0.03216 / 253561. ) 
            else :
                print "w+jets p 2500toInf b{0} empty".format(str(ipt))
                hwjetsT7p.Scale( 0.)
        hwjetspT_ = hwjetsTp1_.Clone()
        hwjetspT_.SetDirectory(0)
        hwjetspT_.Sumw2()
        hwjetspT_.Add(hwjetsTp2_)
        hwjetspT_.Add(hwjetsTp3_)
        hwjetspT_.Add(hwjetsTp4_)
        hwjetspT_.Add(hwjetsTp5_)
        hwjetspT_.Add(hwjetsTp6_)
        hwjetspT_.Add(hwjetsTp7_)
        return hwjetspT_

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)

CMS_lumi.lumi_13TeV = "12.3 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref


# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref


ROOT.gStyle.SetTitleOffset(1.0, "Y")

datatype = 'Alldata_'
if options.Mudata :
    datatype = 'Mudata_'
if options.Eldata :
    datatype = 'Eldata_'


type2 = '_'
if options.Type2 : type2 = '_type2_'

if options.TreeMaker:
    if not options.pre :
        fout= ROOT.TFile('./Joutput80xplotter/JWtag'+type2+datatype+'highPtSF_80x_' + options.infile + '_' + options.treeLocation+ '.root', "RECREATE")
    if options.pre :
        fout= ROOT.TFile('./Joutput80xplotter/JWtag' +type2+datatype+'highPtSF_preWTag_80x_'+ options.infile + '_' + options.treeLocation+'.root', "RECREATE")
if not options.TreeMaker:
    if not options.pre :
        fout= ROOT.TFile('./output80xplotter/Wtag'+type2+datatype+'highPtSF_80x_' + options.treeLocation +'_'+ options.infile  + '.root', "RECREATE")
    if options.pre :
        fout= ROOT.TFile('./output80xplotter/Wtag'+type2+datatype+'highPtSF_preWTag_80x_' + options.treeLocation+'_'+options.infile + '.root', "RECREATE")
            
ptBs =  array.array('d', [200., 300., 400., 500., 800.])
nptBs = len(ptBs) - 1


hpeak = ROOT.TH1F("hpeak", " ;p_{T} of SD subjet 0 (GeV); JMS ",  nptBs, ptBs)  ##frac{Mean Mass_{data}}{Mean Mass_{MC}}
hwidth = ROOT.TH1F("hwidth", " ;p_{T} of SD subjet 0 (GeV); JMR ", nptBs, ptBs) ##frac{#sigma_{data}}{#sigma_{MC}}

hpeakmu = ROOT.TH1F("hpeakmu", " ;p_{T} of SD subjet 0 (GeV); JMS ",  nptBs, ptBs)  ##frac{Mean Mass_{data}}{Mean Mass_{MC}}
hwidthmu = ROOT.TH1F("hwidthmu", " ;p_{T} of SD subjet 0 (GeV); JMR ", nptBs, ptBs) ##frac{#sigma_{data}}{#sigma_{MC}}

hpeakel = ROOT.TH1F("hpeakel", " ;p_{T} of SD subjet 0 (GeV); JMS ",  nptBs, ptBs)  ##frac{Mean Mass_{data}}{Mean Mass_{MC}}
hwidthel = ROOT.TH1F("hwidthel", " ;p_{T} of SD subjet 0 (GeV); JMR ", nptBs, ptBs) ##frac{#sigma_{data}}{#sigma_{MC}}


if options.pre :
    hNpassDataPre = ROOT.TH1F("hNpassDataPre", " ;;  ", nptBs, ptBs) 
    hNpassMuDataPre = ROOT.TH1F("hNpassMuDataPre", " ;;  ", nptBs, ptBs) 
    hNpassElDataPre = ROOT.TH1F("hNpassElDataPre", " ;;  ", nptBs, ptBs) 
    hNpassMCPre = ROOT.TH1F("hNpassMCPre", " ;;  ", nptBs, ptBs) 
    hmeanDataPre = ROOT.TH1F("hmeanDataPre", " ;;  ", nptBs, ptBs) 
    hmeanMuDataPre = ROOT.TH1F("hmeanMuDataPre", " ;;  ", nptBs, ptBs) 
    hmeanElDataPre = ROOT.TH1F("hmeanElDataPre", " ;;  ", nptBs, ptBs) 
    hmeanMCPre = ROOT.TH1F("hmeanMCPre", " ;;  ", nptBs, ptBs) 
    hsigmaDataPre = ROOT.TH1F("hsigmaDataPre", " ;;  ", nptBs, ptBs) 
    hsigmaMuDataPre = ROOT.TH1F("hsigmaMuDataPre", " ;;  ", nptBs, ptBs) 
    hsigmaElDataPre = ROOT.TH1F("hsigmaElDataPre", " ;;  ", nptBs, ptBs) 
    hsigmaMCPre = ROOT.TH1F("hsigmaMCPre", " ;;  ", nptBs, ptBs) 
else:
    hNpassDataPost = ROOT.TH1F("hNpassDataPost", " ;;  ", nptBs, ptBs) 
    hNpassMuDataPost = ROOT.TH1F("hNpassMuDataPost", " ;;  ", nptBs, ptBs) 
    hNpassElDataPost = ROOT.TH1F("hNpassElDataPost", " ;;  ", nptBs, ptBs) 
    hNpassMCPost = ROOT.TH1F("hNpassMCPost", " ;;  ", nptBs, ptBs) 
    hscale = ROOT.TH1F("hscale", " ; ;  ", nptBs, ptBs)
    hDataEff = ROOT.TH1F("hDataEff", " ; ; ", nptBs, ptBs)
    hMuDataEff = ROOT.TH1F("hMuDataEff", " ; ; ", nptBs, ptBs)
    hElDataEff = ROOT.TH1F("hElDataEff", " ; ; ", nptBs, ptBs)
    hMCEff = ROOT.TH1F("hMCEff", " ; ; ", nptBs, ptBs)

# Create input file list
if options.TreeMaker or not options.allMC: dtypes = ['data', 'ttjets' ]
else : dtypes = ['data', 'ttjets','st1', 'st2', 'st3', 'st4', 'wjets1', 'wjets2', 'wjets3', 'wjets4', 'wjets5', 'wjets6', 'wjets7'] 


filesin = [] 

for idt, dt in enumerate(dtypes) :

    if options.TreeMaker :
        if options.maxEvents > 0. :
            filesin.append('./Joutput80xselector/Jhistos' +str(type2)+'80x_' +str(options.maxEvents)+'_'+str(dt) + '_'+ options.filestr + '.root')
        else :
            filesin.append('./Joutput80xselector/Jhistos' +'_type2_'+'80x_' +str(dt) + '_'+ options.filestr + '.root')# fix this replace _ with str(type2)
    if not options.TreeMaker :
        if options.maxEvents > 0. :
            filesin.append('./output80xselector/histos' +str(type2)+'80x_' +str(options.maxEvents)+'_'+str(dt) +  '_'+ options.treeLocation + '_'+ options.filestr +'.root')
        else :
            filesin.append('./output80xselector/histos' +str(type2)+'80x_' +str(dt) +  '_'+ options.treeLocation + '_'+ options.filestr +'.root')    
print "Using input files :  {0}".format(filesin[0], filesin[1])

# Luminosity of input dataset
lumi = 12300. #2136.0

binlimit = 400.
numbins = 600

for ifin, fin in enumerate(filesin) :
    filei = ROOT.TFile.Open( fin )
    fileIs = ROOT.TFile(fin )
    fileIs.cd()
    print " data type {0}".format(str(dtypes[ifin])) 
    if str(dtypes[ifin]) == 'data' :
        hdata = ( filei.Get("h_mWsubjet_Data"))
        hdata.SetDirectory(0)
        hdata.Sumw2()

        heldata = ( filei.Get("h_mWsubjet_ElData"))
        heldata.SetDirectory(0)
        heldata.Sumw2()

        hmudata = ( filei.Get("h_mWsubjet_MuData"))
        hmudata.SetDirectory(0)
        hmudata.Sumw2()

        hdata_b1 =   filei.Get("h_mWsubjet_b1")
        hdata_b2 =   filei.Get("h_mWsubjet_b2")
        hdata_b3 =   filei.Get("h_mWsubjet_b3")
        hdata_b4 =   filei.Get("h_mWsubjet_b4")
        hdata_b5 =   filei.Get("h_mWsubjet_b5")


        hdata_b1.SetDirectory(0)
        hdata_b2.SetDirectory(0)
        hdata_b3.SetDirectory(0)
        hdata_b4.SetDirectory(0)
        hdata_b5.SetDirectory(0)


        hdata_b1.Sumw2()
        hdata_b2.Sumw2()
        hdata_b3.Sumw2()
        hdata_b4.Sumw2()
        hdata_b5.Sumw2()


        heldata_b1 =   filei.Get("h_mWsubjet_b1e")
        heldata_b2 =   filei.Get("h_mWsubjet_b2e")
        heldata_b3 =   filei.Get("h_mWsubjet_b3e")
        heldata_b4 =   filei.Get("h_mWsubjet_b4e")
        heldata_b5 =   filei.Get("h_mWsubjet_b5e")


        heldata_b1.SetDirectory(0)
        heldata_b2.SetDirectory(0)
        heldata_b3.SetDirectory(0)
        heldata_b4.SetDirectory(0)
        heldata_b5.SetDirectory(0)


        heldata_b1.Sumw2()
        heldata_b2.Sumw2()
        heldata_b3.Sumw2()
        heldata_b4.Sumw2()
        heldata_b5.Sumw2()


        hmudata_b1 =   filei.Get("h_mWsubjet_b1m")
        hmudata_b2 =   filei.Get("h_mWsubjet_b2m")
        hmudata_b3 =   filei.Get("h_mWsubjet_b3m")
        hmudata_b4 =   filei.Get("h_mWsubjet_b4m")
        hmudata_b5 =   filei.Get("h_mWsubjet_b5m")


        hmudata_b1.SetDirectory(0)
        hmudata_b2.SetDirectory(0)
        hmudata_b3.SetDirectory(0)
        hmudata_b4.SetDirectory(0)
        hmudata_b5.SetDirectory(0)


        hmudata_b1.Sumw2()
        hmudata_b2.Sumw2()
        hmudata_b3.Sumw2()
        hmudata_b4.Sumw2()
        hmudata_b5.Sumw2()


        hdata_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hdata_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hdata_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hdata_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hdata_b5p = ( filei.Get("h_mWsubjet_b5p"))


        hdata_b1p.SetDirectory(0)
        hdata_b2p.SetDirectory(0)
        hdata_b3p.SetDirectory(0)
        hdata_b4p.SetDirectory(0)
        hdata_b5p.SetDirectory(0)


        hdata_b1p.Sumw2()
        hdata_b2p.Sumw2()
        hdata_b3p.Sumw2()
        hdata_b4p.Sumw2()
        hdata_b5p.Sumw2()


        heldata_b1p = ( filei.Get("h_mWsubjet_b1pe"))
        heldata_b2p = ( filei.Get("h_mWsubjet_b2pe"))
        heldata_b3p = ( filei.Get("h_mWsubjet_b3pe"))
        heldata_b4p = ( filei.Get("h_mWsubjet_b4pe"))
        heldata_b5p = ( filei.Get("h_mWsubjet_b5pe"))


        heldata_b1p.SetDirectory(0)
        heldata_b2p.SetDirectory(0)
        heldata_b3p.SetDirectory(0)
        heldata_b4p.SetDirectory(0)
        heldata_b5p.SetDirectory(0)


        heldata_b1p.Sumw2()
        heldata_b2p.Sumw2()
        heldata_b3p.Sumw2()
        heldata_b4p.Sumw2()
        heldata_b5p.Sumw2()

        hmudata_b1p = ( filei.Get("h_mWsubjet_b1pm"))
        hmudata_b2p = ( filei.Get("h_mWsubjet_b2pm"))
        hmudata_b3p = ( filei.Get("h_mWsubjet_b3pm"))
        hmudata_b4p = ( filei.Get("h_mWsubjet_b4pm"))
        hmudata_b5p = ( filei.Get("h_mWsubjet_b5pm"))


        hmudata_b1p.SetDirectory(0)
        hmudata_b2p.SetDirectory(0)
        hmudata_b3p.SetDirectory(0)
        hmudata_b4p.SetDirectory(0)
        hmudata_b5p.SetDirectory(0)


        hmudata_b1p.Sumw2()
        hmudata_b2p.Sumw2()
        hmudata_b3p.Sumw2()
        hmudata_b4p.Sumw2()
        hmudata_b5p.Sumw2()


        hdata_leppt       = filei.Get("h_lepPt_Data")
        hdata_lepeta      = filei.Get("h_lepEta_Data")
        hdata_lephtlep    = filei.Get("h_lepHtLep_Data")
        hdata_lepht       = filei.Get("h_lepHt_Data")  
        hdata_lepst       = filei.Get("h_lepSt_Data") 
        hdata_ak8tau21    = filei.Get("h_AK8Tau21_Data") 
        hdata_ak8pt       = filei.Get("h_AK8Pt_Data")  
        hdata_ak8SJtau21  = filei.Get("h_AK8subjetTau21_Data")
        hdata_ak8SJpt     = filei.Get("h_AK8subjetPt_Data") 
 
        hdata_Pass        = filei.Get("h_mWsubjetPasstag_Data")
        hdata_Fail        = filei.Get("h_mWsubjetFailtag_Data")

        hdata_leppt.SetDirectory(0)
        hdata_lepeta.SetDirectory(0)
        hdata_lephtlep.SetDirectory(0)
        hdata_lepht.SetDirectory(0)
        hdata_lepst.SetDirectory(0) 
        hdata_ak8tau21.SetDirectory(0)
        hdata_ak8pt.SetDirectory(0) 
        hdata_ak8SJtau21.SetDirectory(0)
        hdata_ak8SJpt.SetDirectory(0)
 
        hdata_Pass.SetDirectory(0)
        hdata_Fail.SetDirectory(0)

        hdata_leppt.Sumw2()
        hdata_lepeta.Sumw2()
        hdata_lephtlep.Sumw2()
        hdata_lepht.Sumw2()
        hdata_lepst.Sumw2()
        hdata_ak8tau21.Sumw2()
        hdata_ak8pt.Sumw2()
        hdata_ak8SJtau21.Sumw2()
        hdata_ak8SJpt.Sumw2()
 
        hdata_Pass.Sumw2()
        hdata_Fail.Sumw2()

        heldata_leppt       = filei.Get("h_lepPt_ElData")
        heldata_lepeta      = filei.Get("h_lepEta_ElData")
        heldata_lephtlep    = filei.Get("h_lepHtLep_ElData")
        heldata_lepht       = filei.Get("h_lepHt_ElData")  
        heldata_lepst       = filei.Get("h_lepSt_ElData") 
        heldata_ak8tau21    = filei.Get("h_AK8Tau21_ElData") 
        heldata_ak8pt       = filei.Get("h_AK8Pt_ElData")  
        heldata_ak8SJtau21  = filei.Get("h_AK8subjetTau21_ElData")
        heldata_ak8SJpt     = filei.Get("h_AK8subjetPt_ElData") 
 
        heldata_Pass        = filei.Get("h_mWsubjetPasstag_ElData")
        heldata_Fail        = filei.Get("h_mWsubjetFailtag_ElData")

        heldata_leppt.SetDirectory(0)
        heldata_lepeta.SetDirectory(0)
        heldata_lephtlep.SetDirectory(0)
        heldata_lepht.SetDirectory(0)
        heldata_lepst.SetDirectory(0) 
        heldata_ak8tau21.SetDirectory(0)
        heldata_ak8pt.SetDirectory(0) 
        heldata_ak8SJtau21.SetDirectory(0)
        heldata_ak8SJpt.SetDirectory(0)
 
        heldata_Pass.SetDirectory(0)
        heldata_Fail.SetDirectory(0)

        heldata_leppt.Sumw2()
        heldata_lepeta.Sumw2()
        heldata_lephtlep.Sumw2()
        heldata_lepht.Sumw2()
        heldata_lepst.Sumw2()
        heldata_ak8tau21.Sumw2()
        heldata_ak8pt.Sumw2()
        heldata_ak8SJtau21.Sumw2()
        heldata_ak8SJpt.Sumw2()
 
        heldata_Pass.Sumw2()
        heldata_Fail.Sumw2()

        hmudata_leppt       = filei.Get("h_lepPt_MuData")
        hmudata_lepeta      = filei.Get("h_lepEta_MuData")
        hmudata_lephtlep    = filei.Get("h_lepHtLep_MuData")
        hmudata_lepht       = filei.Get("h_lepHt_MuData")  
        hmudata_lepst       = filei.Get("h_lepSt_MuData") 
        hmudata_ak8tau21    = filei.Get("h_AK8Tau21_MuData") 
        hmudata_ak8pt       = filei.Get("h_AK8Pt_MuData")  
        hmudata_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MuData")
        hmudata_ak8SJpt     = filei.Get("h_AK8subjetPt_MuData") 
 
        hmudata_Pass        = filei.Get("h_mWsubjetPasstag_MuData")
        hmudata_Fail        = filei.Get("h_mWsubjetFailtag_MuData")

        hmudata_leppt.SetDirectory(0)
        hmudata_lepeta.SetDirectory(0)
        hmudata_lephtlep.SetDirectory(0)
        hmudata_lepht.SetDirectory(0)
        hmudata_lepst.SetDirectory(0) 
        hmudata_ak8tau21.SetDirectory(0)
        hmudata_ak8pt.SetDirectory(0) 
        hmudata_ak8SJtau21.SetDirectory(0)
        hmudata_ak8SJpt.SetDirectory(0)
 
        hmudata_Pass.SetDirectory(0)
        hmudata_Fail.SetDirectory(0)

        hmudata_leppt.Sumw2()
        hmudata_lepeta.Sumw2()
        hmudata_lephtlep.Sumw2()
        hmudata_lepht.Sumw2()
        hmudata_lepst.Sumw2()
        hmudata_ak8tau21.Sumw2()
        hmudata_ak8pt.Sumw2()
        hmudata_ak8SJtau21.Sumw2()
        hmudata_ak8SJpt.Sumw2()
 
        hmudata_Pass.Sumw2()
        hmudata_Fail.Sumw2()

        fileIs.Close()

    if str(dtypes[ifin]) == 'ttjets' :
        httbar = (filei.Get("h_mWsubjet_MC"))
        httbar.SetDirectory(0)
        httbar.Sumw2()

        httjets_b1 = ( filei.Get("h_mWsubjet_b1"))
        httjets_b2 = ( filei.Get("h_mWsubjet_b2"))
        httjets_b3 = ( filei.Get("h_mWsubjet_b3"))
        httjets_b4 = ( filei.Get("h_mWsubjet_b4"))
        httjets_b5 = ( filei.Get("h_mWsubjet_b5"))


        httjets_b1.SetDirectory(0)
        httjets_b2.SetDirectory(0)
        httjets_b3.SetDirectory(0)
        httjets_b4.SetDirectory(0)
        httjets_b5.SetDirectory(0)


        httjets_b1.Sumw2()
        httjets_b2.Sumw2()
        httjets_b3.Sumw2()
        httjets_b4.Sumw2()
        httjets_b5.Sumw2()


        httjets_b1p = ( filei.Get("h_mWsubjet_b1p"))
        httjets_b2p = ( filei.Get("h_mWsubjet_b2p"))
        httjets_b3p = ( filei.Get("h_mWsubjet_b3p"))
        httjets_b4p = ( filei.Get("h_mWsubjet_b4p"))
        httjets_b5p = ( filei.Get("h_mWsubjet_b5p"))



        httjets_b1p.SetDirectory(0)
        httjets_b2p.SetDirectory(0)
        httjets_b3p.SetDirectory(0)
        httjets_b4p.SetDirectory(0)
        httjets_b5p.SetDirectory(0)


        httjets_b1p.Sumw2()
        httjets_b2p.Sumw2()
        httjets_b3p.Sumw2()
        httjets_b4p.Sumw2()
        httjets_b5p.Sumw2()


        httbar_leppt       = filei.Get("h_lepPt_MC")
        httbar_lepeta      = filei.Get("h_lepEta_MC")
        httbar_lephtlep    = filei.Get("h_lepHtLep_MC")
        httbar_lepht       = filei.Get("h_lepHt_MC")  
        httbar_lepst       = filei.Get("h_lepSt_MC") 

        httbarp_leppt       = filei.Get("hp_lepPt_MC")
        httbarp_lepeta      = filei.Get("hp_lepEta_MC")
        httbarp_lephtlep    = filei.Get("hp_lepHtLep_MC")
        httbarp_lepht       = filei.Get("hp_lepHt_MC")  
        httbarp_lepst       = filei.Get("hp_lepSt_MC") 

        httbar_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        httbar_ak8pt       = filei.Get("h_AK8Pt_MC")  
        httbar_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        httbar_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        httbar_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        httbar_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        httbar_leppt.SetDirectory(0)
        httbar_lepeta.SetDirectory(0)
        httbar_lephtlep.SetDirectory(0)
        httbar_lepht.SetDirectory(0)
        httbar_lepst.SetDirectory(0) 
        httbar_ak8tau21.SetDirectory(0)
        httbar_ak8pt.SetDirectory(0) 
        httbar_ak8SJtau21.SetDirectory(0)
        httbar_ak8SJpt.SetDirectory(0)
 
        httbar_Pass.SetDirectory(0)
        httbar_Fail.SetDirectory(0)

        httbar_leppt.Sumw2()
        httbar_lepeta.Sumw2()
        httbar_lephtlep.Sumw2()
        httbar_lepht.Sumw2()
        httbar_lepst.Sumw2()
        httbarp_leppt.Sumw2()
        httbarp_lepeta.Sumw2()
        httbarp_lephtlep.Sumw2()
        httbarp_lepht.Sumw2()
        httbarp_lepst.Sumw2()

        httbar_ak8tau21.Sumw2()
        httbar_ak8pt.Sumw2()
        httbar_ak8SJtau21.Sumw2()
        httbar_ak8SJpt.Sumw2()
 
        httbar_Pass.Sumw2()
        httbar_Fail.Sumw2()
        fileIs.Close()

    if str(dtypes[ifin]) == 'st1' :
        hst1 = (filei.Get("h_mWsubjet_MC"))
        hst1.SetDirectory(0)
        hst1.Sumw2()

        hst1_b1 = ( filei.Get("h_mWsubjet_b1"))
        hst1_b2 = ( filei.Get("h_mWsubjet_b2"))
        hst1_b3 = ( filei.Get("h_mWsubjet_b3"))
        hst1_b4 = ( filei.Get("h_mWsubjet_b4"))
        hst1_b5 = ( filei.Get("h_mWsubjet_b5"))


        hst1_b1.SetDirectory(0)
        hst1_b2.SetDirectory(0)
        hst1_b3.SetDirectory(0)
        hst1_b4.SetDirectory(0)
        hst1_b5.SetDirectory(0)


        hst1_b1.Sumw2()
        hst1_b2.Sumw2()
        hst1_b3.Sumw2()
        hst1_b4.Sumw2()
        hst1_b5.Sumw2()


        hst1_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hst1_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hst1_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hst1_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hst1_b5p = ( filei.Get("h_mWsubjet_b5p"))



        hst1_b1p.SetDirectory(0)
        hst1_b2p.SetDirectory(0)
        hst1_b3p.SetDirectory(0)
        hst1_b4p.SetDirectory(0)
        hst1_b5p.SetDirectory(0)


        hst1_b1p.Sumw2()
        hst1_b2p.Sumw2()
        hst1_b3p.Sumw2()
        hst1_b4p.Sumw2()
        hst1_b5p.Sumw2()


        hst1_leppt       = filei.Get("h_lepPt_MC")
        hst1_lepeta      = filei.Get("h_lepEta_MC")
        hst1_lephtlep    = filei.Get("h_lepHtLep_MC")
        hst1_lepht       = filei.Get("h_lepHt_MC")  
        hst1_lepst       = filei.Get("h_lepSt_MC") 
        hst1_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        hst1_ak8pt       = filei.Get("h_AK8Pt_MC")  
        hst1_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        hst1_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        hst1_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        hst1_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        hst1_leppt.SetDirectory(0)
        hst1_lepeta.SetDirectory(0)
        hst1_lephtlep.SetDirectory(0)
        hst1_lepht.SetDirectory(0)
        hst1_lepst.SetDirectory(0) 
        hst1_ak8tau21.SetDirectory(0)
        hst1_ak8pt.SetDirectory(0) 
        hst1_ak8SJtau21.SetDirectory(0)
        hst1_ak8SJpt.SetDirectory(0)
 
        hst1_Pass.SetDirectory(0)
        hst1_Fail.SetDirectory(0)

        hst1_leppt.Sumw2()
        hst1_lepeta.Sumw2()
        hst1_lephtlep.Sumw2()
        hst1_lepht.Sumw2()
        hst1_lepst.Sumw2()
        hst1_ak8tau21.Sumw2()
        hst1_ak8pt.Sumw2()
        hst1_ak8SJtau21.Sumw2()
        hst1_ak8SJpt.Sumw2()
 
        hst1_Pass.Sumw2()
        hst1_Fail.Sumw2()

        fileIs.Close()
    if str(dtypes[ifin]) == 'st2' :
        hst2 = (filei.Get("h_mWsubjet_MC"))
        hst2.SetDirectory(0)
        hst2.Sumw2()

        hst2_b1 = ( filei.Get("h_mWsubjet_b1"))
        hst2_b2 = ( filei.Get("h_mWsubjet_b2"))
        hst2_b3 = ( filei.Get("h_mWsubjet_b3"))
        hst2_b4 = ( filei.Get("h_mWsubjet_b4"))
        hst2_b5 = ( filei.Get("h_mWsubjet_b5"))


        hst2_b1.SetDirectory(0)
        hst2_b2.SetDirectory(0)
        hst2_b3.SetDirectory(0)
        hst2_b4.SetDirectory(0)
        hst2_b5.SetDirectory(0)


        hst2_b1.Sumw2()
        hst2_b2.Sumw2()
        hst2_b3.Sumw2()
        hst2_b4.Sumw2()
        hst2_b5.Sumw2()


        hst2_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hst2_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hst2_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hst2_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hst2_b5p = ( filei.Get("h_mWsubjet_b5p"))



        hst2_b1p.SetDirectory(0)
        hst2_b2p.SetDirectory(0)
        hst2_b3p.SetDirectory(0)
        hst2_b4p.SetDirectory(0)
        hst2_b5p.SetDirectory(0)


        hst2_b1p.Sumw2()
        hst2_b2p.Sumw2()
        hst2_b3p.Sumw2()
        hst2_b4p.Sumw2()
        hst2_b5p.Sumw2()


        hst2_leppt       = filei.Get("h_lepPt_MC")
        hst2_lepeta      = filei.Get("h_lepEta_MC")
        hst2_lephtlep    = filei.Get("h_lepHtLep_MC")
        hst2_lepht       = filei.Get("h_lepHt_MC")  
        hst2_lepst       = filei.Get("h_lepSt_MC") 
        hst2_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        hst2_ak8pt       = filei.Get("h_AK8Pt_MC")  
        hst2_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        hst2_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        hst2_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        hst2_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        hst2_leppt.SetDirectory(0)
        hst2_lepeta.SetDirectory(0)
        hst2_lephtlep.SetDirectory(0)
        hst2_lepht.SetDirectory(0)
        hst2_lepst.SetDirectory(0) 
        hst2_ak8tau21.SetDirectory(0)
        hst2_ak8pt.SetDirectory(0) 
        hst2_ak8SJtau21.SetDirectory(0)
        hst2_ak8SJpt.SetDirectory(0)
 
        hst2_Pass.SetDirectory(0)
        hst2_Fail.SetDirectory(0)

        hst2_leppt.Sumw2()
        hst2_lepeta.Sumw2()
        hst2_lephtlep.Sumw2()
        hst2_lepht.Sumw2()
        hst2_lepst.Sumw2()
        hst2_ak8tau21.Sumw2()
        hst2_ak8pt.Sumw2()
        hst2_ak8SJtau21.Sumw2()
        hst2_ak8SJpt.Sumw2()
 
        hst2_Pass.Sumw2()
        hst2_Fail.Sumw2()

        fileIs.Close()

    if str(dtypes[ifin]) == 'st3' :
        hst3 = (filei.Get("h_mWsubjet_MC"))
        hst3.SetDirectory(0)
        hst3.Sumw2()

        hst3_b1 = ( filei.Get("h_mWsubjet_b1"))
        hst3_b2 = ( filei.Get("h_mWsubjet_b2"))
        hst3_b3 = ( filei.Get("h_mWsubjet_b3"))
        hst3_b4 = ( filei.Get("h_mWsubjet_b4"))
        hst3_b5 = ( filei.Get("h_mWsubjet_b5"))


        hst3_b1.SetDirectory(0)
        hst3_b2.SetDirectory(0)
        hst3_b3.SetDirectory(0)
        hst3_b4.SetDirectory(0)
        hst3_b5.SetDirectory(0)


        hst3_b1.Sumw2()
        hst3_b2.Sumw2()
        hst3_b3.Sumw2()
        hst3_b4.Sumw2()
        hst3_b5.Sumw2()


        hst3_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hst3_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hst3_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hst3_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hst3_b5p = ( filei.Get("h_mWsubjet_b5p"))



        hst3_b1p.SetDirectory(0)
        hst3_b2p.SetDirectory(0)
        hst3_b3p.SetDirectory(0)
        hst3_b4p.SetDirectory(0)
        hst3_b5p.SetDirectory(0)


        hst3_b1p.Sumw2()
        hst3_b2p.Sumw2()
        hst3_b3p.Sumw2()
        hst3_b4p.Sumw2()
        hst3_b5p.Sumw2()


        hst3_leppt       = filei.Get("h_lepPt_MC")
        hst3_lepeta      = filei.Get("h_lepEta_MC")
        hst3_lephtlep    = filei.Get("h_lepHtLep_MC")
        hst3_lepht       = filei.Get("h_lepHt_MC")  
        hst3_lepst       = filei.Get("h_lepSt_MC") 
        hst3_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        hst3_ak8pt       = filei.Get("h_AK8Pt_MC")  
        hst3_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        hst3_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        hst3_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        hst3_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        hst3_leppt.SetDirectory(0)
        hst3_lepeta.SetDirectory(0)
        hst3_lephtlep.SetDirectory(0)
        hst3_lepht.SetDirectory(0)
        hst3_lepst.SetDirectory(0) 
        hst3_ak8tau21.SetDirectory(0)
        hst3_ak8pt.SetDirectory(0) 
        hst3_ak8SJtau21.SetDirectory(0)
        hst3_ak8SJpt.SetDirectory(0)
 
        hst3_Pass.SetDirectory(0)
        hst3_Fail.SetDirectory(0)

        hst3_leppt.Sumw2()
        hst3_lepeta.Sumw2()
        hst3_lephtlep.Sumw2()
        hst3_lepht.Sumw2()
        hst3_lepst.Sumw2()
        hst3_ak8tau21.Sumw2()
        hst3_ak8pt.Sumw2()
        hst3_ak8SJtau21.Sumw2()
        hst3_ak8SJpt.Sumw2()
 
        hst3_Pass.Sumw2()
        hst3_Fail.Sumw2()

        fileIs.Close()

    if str(dtypes[ifin]) == 'st4' :
        hst4 = (filei.Get("h_mWsubjet_MC"))
        hst4.SetDirectory(0)
        hst4.Sumw2()

        hst4_b1 = ( filei.Get("h_mWsubjet_b1"))
        hst4_b2 = ( filei.Get("h_mWsubjet_b2"))
        hst4_b3 = ( filei.Get("h_mWsubjet_b3"))
        hst4_b4 = ( filei.Get("h_mWsubjet_b4"))
        hst4_b5 = ( filei.Get("h_mWsubjet_b5"))


        hst4_b1.SetDirectory(0)
        hst4_b2.SetDirectory(0)
        hst4_b3.SetDirectory(0)
        hst4_b4.SetDirectory(0)
        hst4_b5.SetDirectory(0)


        hst4_b1.Sumw2()
        hst4_b2.Sumw2()
        hst4_b3.Sumw2()
        hst4_b4.Sumw2()
        hst4_b5.Sumw2()


        hst4_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hst4_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hst4_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hst4_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hst4_b5p = ( filei.Get("h_mWsubjet_b5p"))



        hst4_b1p.SetDirectory(0)
        hst4_b2p.SetDirectory(0)
        hst4_b3p.SetDirectory(0)
        hst4_b4p.SetDirectory(0)
        hst4_b5p.SetDirectory(0)


        hst4_b1p.Sumw2()
        hst4_b2p.Sumw2()
        hst4_b3p.Sumw2()
        hst4_b4p.Sumw2()
        hst4_b5p.Sumw2()


        hst4_leppt       = filei.Get("h_lepPt_MC")
        hst4_lepeta      = filei.Get("h_lepEta_MC")
        hst4_lephtlep    = filei.Get("h_lepHtLep_MC")
        hst4_lepht       = filei.Get("h_lepHt_MC")  
        hst4_lepst       = filei.Get("h_lepSt_MC") 
        hst4_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        hst4_ak8pt       = filei.Get("h_AK8Pt_MC")  
        hst4_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        hst4_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        hst4_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        hst4_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        hst4_leppt.SetDirectory(0)
        hst4_lepeta.SetDirectory(0)
        hst4_lephtlep.SetDirectory(0)
        hst4_lepht.SetDirectory(0)
        hst4_lepst.SetDirectory(0) 
        hst4_ak8tau21.SetDirectory(0)
        hst4_ak8pt.SetDirectory(0) 
        hst4_ak8SJtau21.SetDirectory(0)
        hst4_ak8SJpt.SetDirectory(0)
 
        hst4_Pass.SetDirectory(0)
        hst4_Fail.SetDirectory(0)

        hst4_leppt.Sumw2()
        hst4_lepeta.Sumw2()
        hst4_lephtlep.Sumw2()
        hst4_lepht.Sumw2()
        hst4_lepst.Sumw2()
        hst4_ak8tau21.Sumw2()
        hst4_ak8pt.Sumw2()
        hst4_ak8SJtau21.Sumw2()
        hst4_ak8SJpt.Sumw2()
 
        hst4_Pass.Sumw2()
        hst4_Fail.Sumw2()

        fileIs.Close()
    if str(dtypes[ifin]) == 'wjets1' :
        hwjets1 = (filei.Get("h_mWsubjet_MC"))
        hwjets1.SetDirectory(0)
        hwjets1.Sumw2()

        hwjets1_b1 = ( filei.Get("h_mWsubjet_b1"))
        hwjets1_b2 = ( filei.Get("h_mWsubjet_b2"))
        hwjets1_b3 = ( filei.Get("h_mWsubjet_b3"))
        hwjets1_b4 = ( filei.Get("h_mWsubjet_b4"))
        hwjets1_b5 = ( filei.Get("h_mWsubjet_b5"))


        hwjets1_b1.SetDirectory(0)
        hwjets1_b2.SetDirectory(0)
        hwjets1_b3.SetDirectory(0)
        hwjets1_b4.SetDirectory(0)
        hwjets1_b5.SetDirectory(0)


        hwjets1_b1.Sumw2()
        hwjets1_b2.Sumw2()
        hwjets1_b3.Sumw2()
        hwjets1_b4.Sumw2()
        hwjets1_b5.Sumw2()


        hwjets1_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hwjets1_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hwjets1_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hwjets1_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hwjets1_b5p = ( filei.Get("h_mWsubjet_b5p"))



        hwjets1_b1p.SetDirectory(0)
        hwjets1_b2p.SetDirectory(0)
        hwjets1_b3p.SetDirectory(0)
        hwjets1_b4p.SetDirectory(0)
        hwjets1_b5p.SetDirectory(0)


        hwjets1_b1p.Sumw2()
        hwjets1_b2p.Sumw2()
        hwjets1_b3p.Sumw2()
        hwjets1_b4p.Sumw2()
        hwjets1_b5p.Sumw2()


        hwjets1_leppt       = filei.Get("h_lepPt_MC")
        hwjets1_lepeta      = filei.Get("h_lepEta_MC")
        hwjets1_lephtlep    = filei.Get("h_lepHtLep_MC")
        hwjets1_lepht       = filei.Get("h_lepHt_MC")  
        hwjets1_lepst       = filei.Get("h_lepSt_MC") 
        hwjets1_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        hwjets1_ak8pt       = filei.Get("h_AK8Pt_MC")  
        hwjets1_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        hwjets1_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        hwjets1_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        hwjets1_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        hwjets1_leppt.SetDirectory(0)
        hwjets1_lepeta.SetDirectory(0)
        hwjets1_lephtlep.SetDirectory(0)
        hwjets1_lepht.SetDirectory(0)
        hwjets1_lepst.SetDirectory(0) 
        hwjets1_ak8tau21.SetDirectory(0)
        hwjets1_ak8pt.SetDirectory(0) 
        hwjets1_ak8SJtau21.SetDirectory(0)
        hwjets1_ak8SJpt.SetDirectory(0)
 
        hwjets1_Pass.SetDirectory(0)
        hwjets1_Fail.SetDirectory(0)

        hwjets1_leppt.Sumw2()
        hwjets1_lepeta.Sumw2()
        hwjets1_lephtlep.Sumw2()
        hwjets1_lepht.Sumw2()
        hwjets1_lepst.Sumw2()
        hwjets1_ak8tau21.Sumw2()
        hwjets1_ak8pt.Sumw2()
        hwjets1_ak8SJtau21.Sumw2()
        hwjets1_ak8SJpt.Sumw2()
 
        hwjets1_Pass.Sumw2()
        hwjets1_Fail.Sumw2()

        fileIs.Close()
    if str(dtypes[ifin]) == 'wjets2' :
        hwjets2 = (filei.Get("h_mWsubjet_MC"))
        hwjets2.SetDirectory(0)
        hwjets2.Sumw2()

        hwjets2_b1 = ( filei.Get("h_mWsubjet_b1"))
        hwjets2_b2 = ( filei.Get("h_mWsubjet_b2"))
        hwjets2_b3 = ( filei.Get("h_mWsubjet_b3"))
        hwjets2_b4 = ( filei.Get("h_mWsubjet_b4"))
        hwjets2_b5 = ( filei.Get("h_mWsubjet_b5"))


        hwjets2_b1.SetDirectory(0)
        hwjets2_b2.SetDirectory(0)
        hwjets2_b3.SetDirectory(0)
        hwjets2_b4.SetDirectory(0)
        hwjets2_b5.SetDirectory(0)


        hwjets2_b1.Sumw2()
        hwjets2_b2.Sumw2()
        hwjets2_b3.Sumw2()
        hwjets2_b4.Sumw2()
        hwjets2_b5.Sumw2()


        hwjets2_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hwjets2_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hwjets2_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hwjets2_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hwjets2_b5p = ( filei.Get("h_mWsubjet_b5p"))



        hwjets2_b1p.SetDirectory(0)
        hwjets2_b2p.SetDirectory(0)
        hwjets2_b3p.SetDirectory(0)
        hwjets2_b4p.SetDirectory(0)
        hwjets2_b5p.SetDirectory(0)


        hwjets2_b1p.Sumw2()
        hwjets2_b2p.Sumw2()
        hwjets2_b3p.Sumw2()
        hwjets2_b4p.Sumw2()
        hwjets2_b5p.Sumw2()


        hwjets2_leppt       = filei.Get("h_lepPt_MC")
        hwjets2_lepeta      = filei.Get("h_lepEta_MC")
        hwjets2_lephtlep    = filei.Get("h_lepHtLep_MC")
        hwjets2_lepht       = filei.Get("h_lepHt_MC")  
        hwjets2_lepst       = filei.Get("h_lepSt_MC") 
        hwjets2_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        hwjets2_ak8pt       = filei.Get("h_AK8Pt_MC")  
        hwjets2_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        hwjets2_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        hwjets2_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        hwjets2_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        hwjets2_leppt.SetDirectory(0)
        hwjets2_lepeta.SetDirectory(0)
        hwjets2_lephtlep.SetDirectory(0)
        hwjets2_lepht.SetDirectory(0)
        hwjets2_lepst.SetDirectory(0) 
        hwjets2_ak8tau21.SetDirectory(0)
        hwjets2_ak8pt.SetDirectory(0) 
        hwjets2_ak8SJtau21.SetDirectory(0)
        hwjets2_ak8SJpt.SetDirectory(0)
 
        hwjets2_Pass.SetDirectory(0)
        hwjets2_Fail.SetDirectory(0)

        hwjets2_leppt.Sumw2()
        hwjets2_lepeta.Sumw2()
        hwjets2_lephtlep.Sumw2()
        hwjets2_lepht.Sumw2()
        hwjets2_lepst.Sumw2()
        hwjets2_ak8tau21.Sumw2()
        hwjets2_ak8pt.Sumw2()
        hwjets2_ak8SJtau21.Sumw2()
        hwjets2_ak8SJpt.Sumw2()
 
        hwjets2_Pass.Sumw2()
        hwjets2_Fail.Sumw2()

        fileIs.Close()
    if str(dtypes[ifin]) == 'wjets3' :
        hwjets3 = (filei.Get("h_mWsubjet_MC"))
        hwjets3.SetDirectory(0)
        hwjets3.Sumw2()

        hwjets3_b1 = ( filei.Get("h_mWsubjet_b1"))
        hwjets3_b2 = ( filei.Get("h_mWsubjet_b2"))
        hwjets3_b3 = ( filei.Get("h_mWsubjet_b3"))
        hwjets3_b4 = ( filei.Get("h_mWsubjet_b4"))
        hwjets3_b5 = ( filei.Get("h_mWsubjet_b5"))


        hwjets3_b1.SetDirectory(0)
        hwjets3_b2.SetDirectory(0)
        hwjets3_b3.SetDirectory(0)
        hwjets3_b4.SetDirectory(0)
        hwjets3_b5.SetDirectory(0)


        hwjets3_b1.Sumw2()
        hwjets3_b2.Sumw2()
        hwjets3_b3.Sumw2()
        hwjets3_b4.Sumw2()
        hwjets3_b5.Sumw2()


        hwjets3_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hwjets3_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hwjets3_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hwjets3_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hwjets3_b5p = ( filei.Get("h_mWsubjet_b5p"))



        hwjets3_b1p.SetDirectory(0)
        hwjets3_b2p.SetDirectory(0)
        hwjets3_b3p.SetDirectory(0)
        hwjets3_b4p.SetDirectory(0)
        hwjets3_b5p.SetDirectory(0)


        hwjets3_b1p.Sumw2()
        hwjets3_b2p.Sumw2()
        hwjets3_b3p.Sumw2()
        hwjets3_b4p.Sumw2()
        hwjets3_b5p.Sumw2()


        hwjets3_leppt       = filei.Get("h_lepPt_MC")
        hwjets3_lepeta      = filei.Get("h_lepEta_MC")
        hwjets3_lephtlep    = filei.Get("h_lepHtLep_MC")
        hwjets3_lepht       = filei.Get("h_lepHt_MC")  
        hwjets3_lepst       = filei.Get("h_lepSt_MC") 
        hwjets3_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        hwjets3_ak8pt       = filei.Get("h_AK8Pt_MC")  
        hwjets3_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        hwjets3_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        hwjets3_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        hwjets3_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        hwjets3_leppt.SetDirectory(0)
        hwjets3_lepeta.SetDirectory(0)
        hwjets3_lephtlep.SetDirectory(0)
        hwjets3_lepht.SetDirectory(0)
        hwjets3_lepst.SetDirectory(0) 
        hwjets3_ak8tau21.SetDirectory(0)
        hwjets3_ak8pt.SetDirectory(0) 
        hwjets3_ak8SJtau21.SetDirectory(0)
        hwjets3_ak8SJpt.SetDirectory(0)
 
        hwjets3_Pass.SetDirectory(0)
        hwjets3_Fail.SetDirectory(0)

        hwjets3_leppt.Sumw2()
        hwjets3_lepeta.Sumw2()
        hwjets3_lephtlep.Sumw2()
        hwjets3_lepht.Sumw2()
        hwjets3_lepst.Sumw2()
        hwjets3_ak8tau21.Sumw2()
        hwjets3_ak8pt.Sumw2()
        hwjets3_ak8SJtau21.Sumw2()
        hwjets3_ak8SJpt.Sumw2()
 
        hwjets3_Pass.Sumw2()
        hwjets3_Fail.Sumw2()

        fileIs.Close()
    if str(dtypes[ifin]) == 'wjets4' :
        hwjets4 = (filei.Get("h_mWsubjet_MC"))
        hwjets4.SetDirectory(0)
        hwjets4.Sumw2()

        hwjets4_b1 = ( filei.Get("h_mWsubjet_b1"))
        hwjets4_b2 = ( filei.Get("h_mWsubjet_b2"))
        hwjets4_b3 = ( filei.Get("h_mWsubjet_b3"))
        hwjets4_b4 = ( filei.Get("h_mWsubjet_b4"))
        hwjets4_b5 = ( filei.Get("h_mWsubjet_b5"))


        hwjets4_b1.SetDirectory(0)
        hwjets4_b2.SetDirectory(0)
        hwjets4_b3.SetDirectory(0)
        hwjets4_b4.SetDirectory(0)
        hwjets4_b5.SetDirectory(0)


        hwjets4_b1.Sumw2()
        hwjets4_b2.Sumw2()
        hwjets4_b3.Sumw2()
        hwjets4_b4.Sumw2()
        hwjets4_b5.Sumw2()


        hwjets4_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hwjets4_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hwjets4_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hwjets4_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hwjets4_b5p = ( filei.Get("h_mWsubjet_b5p"))



        hwjets4_b1p.SetDirectory(0)
        hwjets4_b2p.SetDirectory(0)
        hwjets4_b3p.SetDirectory(0)
        hwjets4_b4p.SetDirectory(0)
        hwjets4_b5p.SetDirectory(0)


        hwjets4_b1p.Sumw2()
        hwjets4_b2p.Sumw2()
        hwjets4_b3p.Sumw2()
        hwjets4_b4p.Sumw2()
        hwjets4_b5p.Sumw2()


        hwjets4_leppt       = filei.Get("h_lepPt_MC")
        hwjets4_lepeta      = filei.Get("h_lepEta_MC")
        hwjets4_lephtlep    = filei.Get("h_lepHtLep_MC")
        hwjets4_lepht       = filei.Get("h_lepHt_MC")  
        hwjets4_lepst       = filei.Get("h_lepSt_MC") 
        hwjets4_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        hwjets4_ak8pt       = filei.Get("h_AK8Pt_MC")  
        hwjets4_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        hwjets4_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        hwjets4_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        hwjets4_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        hwjets4_leppt.SetDirectory(0)
        hwjets4_lepeta.SetDirectory(0)
        hwjets4_lephtlep.SetDirectory(0)
        hwjets4_lepht.SetDirectory(0)
        hwjets4_lepst.SetDirectory(0) 
        hwjets4_ak8tau21.SetDirectory(0)
        hwjets4_ak8pt.SetDirectory(0) 
        hwjets4_ak8SJtau21.SetDirectory(0)
        hwjets4_ak8SJpt.SetDirectory(0)
 
        hwjets4_Pass.SetDirectory(0)
        hwjets4_Fail.SetDirectory(0)

        hwjets4_leppt.Sumw2()
        hwjets4_lepeta.Sumw2()
        hwjets4_lephtlep.Sumw2()
        hwjets4_lepht.Sumw2()
        hwjets4_lepst.Sumw2()
        hwjets4_ak8tau21.Sumw2()
        hwjets4_ak8pt.Sumw2()
        hwjets4_ak8SJtau21.Sumw2()
        hwjets4_ak8SJpt.Sumw2()
 
        hwjets4_Pass.Sumw2()
        hwjets4_Fail.Sumw2()

        fileIs.Close()
    if str(dtypes[ifin]) == 'wjets5' :
        hwjets5 = (filei.Get("h_mWsubjet_MC"))
        hwjets5.SetDirectory(0)
        hwjets5.Sumw2()

        hwjets5_b1 = ( filei.Get("h_mWsubjet_b1"))
        hwjets5_b2 = ( filei.Get("h_mWsubjet_b2"))
        hwjets5_b3 = ( filei.Get("h_mWsubjet_b3"))
        hwjets5_b4 = ( filei.Get("h_mWsubjet_b4"))
        hwjets5_b5 = ( filei.Get("h_mWsubjet_b5"))


        hwjets5_b1.SetDirectory(0)
        hwjets5_b2.SetDirectory(0)
        hwjets5_b3.SetDirectory(0)
        hwjets5_b4.SetDirectory(0)
        hwjets5_b5.SetDirectory(0)


        hwjets5_b1.Sumw2()
        hwjets5_b2.Sumw2()
        hwjets5_b3.Sumw2()
        hwjets5_b4.Sumw2()
        hwjets5_b5.Sumw2()


        hwjets5_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hwjets5_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hwjets5_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hwjets5_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hwjets5_b5p = ( filei.Get("h_mWsubjet_b5p"))



        hwjets5_b1p.SetDirectory(0)
        hwjets5_b2p.SetDirectory(0)
        hwjets5_b3p.SetDirectory(0)
        hwjets5_b4p.SetDirectory(0)
        hwjets5_b5p.SetDirectory(0)


        hwjets5_b1p.Sumw2()
        hwjets5_b2p.Sumw2()
        hwjets5_b3p.Sumw2()
        hwjets5_b4p.Sumw2()
        hwjets5_b5p.Sumw2()


        hwjets5_leppt       = filei.Get("h_lepPt_MC")
        hwjets5_lepeta      = filei.Get("h_lepEta_MC")
        hwjets5_lephtlep    = filei.Get("h_lepHtLep_MC")
        hwjets5_lepht       = filei.Get("h_lepHt_MC")  
        hwjets5_lepst      = filei.Get("h_lepSt_MC") 
        hwjets5_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        hwjets5_ak8pt       = filei.Get("h_AK8Pt_MC")  
        hwjets5_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        hwjets5_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        hwjets5_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        hwjets5_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        hwjets5_leppt.SetDirectory(0)
        hwjets5_lepeta.SetDirectory(0)
        hwjets5_lephtlep.SetDirectory(0)
        hwjets5_lepht.SetDirectory(0)
        hwjets5_lepst.SetDirectory(0) 
        hwjets5_ak8tau21.SetDirectory(0)
        hwjets5_ak8pt.SetDirectory(0) 
        hwjets5_ak8SJtau21.SetDirectory(0)
        hwjets5_ak8SJpt.SetDirectory(0)
 
        hwjets5_Pass.SetDirectory(0)
        hwjets5_Fail.SetDirectory(0)

        hwjets5_leppt.Sumw2()
        hwjets5_lepeta.Sumw2()
        hwjets5_lephtlep.Sumw2()
        hwjets5_lepht.Sumw2()
        hwjets5_lepst.Sumw2()
        hwjets5_ak8tau21.Sumw2()
        hwjets5_ak8pt.Sumw2()
        hwjets5_ak8SJtau21.Sumw2()
        hwjets5_ak8SJpt.Sumw2()
 
        hwjets5_Pass.Sumw2()
        hwjets5_Fail.Sumw2()

        fileIs.Close()
    if str(dtypes[ifin]) == 'wjets6' :
        hwjets6 = (filei.Get("h_mWsubjet_MC"))
        hwjets6.SetDirectory(0)
        hwjets6.Sumw2()

        hwjets6_b1 = ( filei.Get("h_mWsubjet_b1"))
        hwjets6_b2 = ( filei.Get("h_mWsubjet_b2"))
        hwjets6_b3 = ( filei.Get("h_mWsubjet_b3"))
        hwjets6_b4 = ( filei.Get("h_mWsubjet_b4"))
        hwjets6_b5 = ( filei.Get("h_mWsubjet_b5"))


        hwjets6_b1.SetDirectory(0)
        hwjets6_b2.SetDirectory(0)
        hwjets6_b3.SetDirectory(0)
        hwjets6_b4.SetDirectory(0)
        hwjets6_b5.SetDirectory(0)


        hwjets6_b1.Sumw2()
        hwjets6_b2.Sumw2()
        hwjets6_b3.Sumw2()
        hwjets6_b4.Sumw2()
        hwjets6_b5.Sumw2()


        hwjets6_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hwjets6_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hwjets6_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hwjets6_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hwjets6_b5p = ( filei.Get("h_mWsubjet_b5p"))



        hwjets6_b1p.SetDirectory(0)
        hwjets6_b2p.SetDirectory(0)
        hwjets6_b3p.SetDirectory(0)
        hwjets6_b4p.SetDirectory(0)
        hwjets6_b5p.SetDirectory(0)


        hwjets6_b1p.Sumw2()
        hwjets6_b2p.Sumw2()
        hwjets6_b3p.Sumw2()
        hwjets6_b4p.Sumw2()
        hwjets6_b5p.Sumw2()


        hwjets6_leppt       = filei.Get("h_lepPt_MC")
        hwjets6_lepeta      = filei.Get("h_lepEta_MC")
        hwjets6_lephtlep    = filei.Get("h_lepHtLep_MC")
        hwjets6_lepht       = filei.Get("h_lepHt_MC")  
        hwjets6_lepst       = filei.Get("h_lepSt_MC") 
        hwjets6_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        hwjets6_ak8pt       = filei.Get("h_AK8Pt_MC")  
        hwjets6_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        hwjets6_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        hwjets6_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        hwjets6_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        hwjets6_leppt.SetDirectory(0)
        hwjets6_lepeta.SetDirectory(0)
        hwjets6_lephtlep.SetDirectory(0)
        hwjets6_lepht.SetDirectory(0)
        hwjets6_lepst.SetDirectory(0) 
        hwjets6_ak8tau21.SetDirectory(0)
        hwjets6_ak8pt.SetDirectory(0) 
        hwjets6_ak8SJtau21.SetDirectory(0)
        hwjets6_ak8SJpt.SetDirectory(0)
 
        hwjets6_Pass.SetDirectory(0)
        hwjets6_Fail.SetDirectory(0)

        hwjets6_leppt.Sumw2()
        hwjets6_lepeta.Sumw2()
        hwjets6_lephtlep.Sumw2()
        hwjets6_lepht.Sumw2()
        hwjets6_lepst.Sumw2()
        hwjets6_ak8tau21.Sumw2()
        hwjets6_ak8pt.Sumw2()
        hwjets6_ak8SJtau21.Sumw2()
        hwjets6_ak8SJpt.Sumw2()
 
        hwjets6_Pass.Sumw2()
        hwjets6_Fail.Sumw2()

        fileIs.Close()
    if str(dtypes[ifin]) == 'wjets7' :
        hwjets7 = (filei.Get("h_mWsubjet_MC"))
        hwjets7.SetDirectory(0)
        hwjets7.Sumw2()

        hwjets7_b1 = ( filei.Get("h_mWsubjet_b1"))
        hwjets7_b2 = ( filei.Get("h_mWsubjet_b2"))
        hwjets7_b3 = ( filei.Get("h_mWsubjet_b3"))
        hwjets7_b4 = ( filei.Get("h_mWsubjet_b4"))
        hwjets7_b5 = ( filei.Get("h_mWsubjet_b5"))


        hwjets7_b1.SetDirectory(0)
        hwjets7_b2.SetDirectory(0)
        hwjets7_b3.SetDirectory(0)
        hwjets7_b4.SetDirectory(0)
        hwjets7_b5.SetDirectory(0)


        hwjets7_b1.Sumw2()
        hwjets7_b2.Sumw2()
        hwjets7_b3.Sumw2()
        hwjets7_b4.Sumw2()
        hwjets7_b5.Sumw2()


        hwjets7_b1p = ( filei.Get("h_mWsubjet_b1p"))
        hwjets7_b2p = ( filei.Get("h_mWsubjet_b2p"))
        hwjets7_b3p = ( filei.Get("h_mWsubjet_b3p"))
        hwjets7_b4p = ( filei.Get("h_mWsubjet_b4p"))
        hwjets7_b5p = ( filei.Get("h_mWsubjet_b5p"))



        hwjets7_b1p.SetDirectory(0)
        hwjets7_b2p.SetDirectory(0)
        hwjets7_b3p.SetDirectory(0)
        hwjets7_b4p.SetDirectory(0)
        hwjets7_b5p.SetDirectory(0)


        hwjets7_b1p.Sumw2()
        hwjets7_b2p.Sumw2()
        hwjets7_b3p.Sumw2()
        hwjets7_b4p.Sumw2()
        hwjets7_b5p.Sumw2()


        hwjets7_leppt       = filei.Get("h_lepPt_MC")
        hwjets7_lepeta      = filei.Get("h_lepEta_MC")
        hwjets7_lephtlep    = filei.Get("h_lepHtLep_MC")
        hwjets7_lepht       = filei.Get("h_lepHt_MC")  
        hwjets7_lepst      = filei.Get("h_lepSt_MC") 
        hwjets7_ak8tau21    = filei.Get("h_AK8Tau21_MC") 
        hwjets7_ak8pt       = filei.Get("h_AK8Pt_MC")  
        hwjets7_ak8SJtau21  = filei.Get("h_AK8subjetTau21_MC")
        hwjets7_ak8SJpt     = filei.Get("h_AK8subjetPt_MC") 
 
        hwjets7_Pass        = filei.Get("h_mWsubjetPasstag_MC")
        hwjets7_Fail        = filei.Get("h_mWsubjetFailtag_MC")

        hwjets7_leppt.SetDirectory(0)
        hwjets7_lepeta.SetDirectory(0)
        hwjets7_lephtlep.SetDirectory(0)
        hwjets7_lepht.SetDirectory(0)
        hwjets7_lepst.SetDirectory(0) 
        hwjets7_ak8tau21.SetDirectory(0)
        hwjets7_ak8pt.SetDirectory(0) 
        hwjets7_ak8SJtau21.SetDirectory(0)
        hwjets7_ak8SJpt.SetDirectory(0)
 
        hwjets7_Pass.SetDirectory(0)
        hwjets7_Fail.SetDirectory(0)

        hwjets7_leppt.Sumw2()
        hwjets7_lepeta.Sumw2()
        hwjets7_lephtlep.Sumw2()
        hwjets7_lepht.Sumw2()
        hwjets7_lepst.Sumw2()
        hwjets7_ak8tau21.Sumw2()
        hwjets7_ak8pt.Sumw2()
        hwjets7_ak8SJtau21.Sumw2()
        hwjets7_ak8SJpt.Sumw2()
 
        hwjets7_Pass.Sumw2()
        hwjets7_Fail.Sumw2()

        fileIs.Close()
'''
# Fix this, get type 1 and type 2 pt distributions of W candidates

#hpts = filei.Get("h_ptWsubjet_Data_Type1")
#hpts2 = filei.Get("h_ptWsubjet_Data_Type2")

#hptsMC = filei.Get("h_ptWsubjet_MC_Type1")
#hpts2MC = filei.Get("h_ptWsubjet_MC_Type2")
'''

nMCpre = array.array('d', [0., 0., 0., 0.])
nDatapre = array.array('d', [0., 0., 0., 0.])
nMuDatapre = array.array('d', [0., 0., 0., 0.])
nElDatapre = array.array('d', [0., 0., 0., 0.])
nMCupre = array.array('d', [0., 0., 0., 0.])
nDataupre = array.array('d', [0., 0., 0., 0.])
nMuDataupre = array.array('d', [0., 0., 0., 0.])
nElDataupre = array.array('d', [0., 0., 0., 0.])

MCmeans = array.array('d', [0., 0., 0., 0.])
MCsigmas = array.array('d', [0., 0., 0., 0.])
Datameans = array.array('d', [0., 0., 0., 0.])
Datasigmas = array.array('d', [0., 0., 0., 0.])
ElDatameans = array.array('d', [0., 0., 0., 0.])
ElDatasigmas = array.array('d', [0., 0., 0., 0.])
MuDatameans = array.array('d', [0., 0., 0., 0.])
MuDatasigmas = array.array('d', [0., 0., 0., 0.])

nMCpost = array.array('d', [0., 0., 0., 0.])
nDatapost = array.array('d', [0., 0., 0., 0.])
nMuDatapost = array.array('d', [0., 0., 0., 0.])
nElDatapost = array.array('d', [0., 0., 0., 0.])
nMCupost = array.array('d', [0., 0., 0., 0.])
nDataupost = array.array('d', [0., 0., 0., 0.])
nMuDataupost = array.array('d', [0., 0., 0., 0.])
nElDataupost = array.array('d', [0., 0., 0., 0.])

if not options.pre : 
    filein2 = ROOT.TFile.Open('./output80xplotter/Wtag'+type2+datatype+'highPtSF_preWTag_80x_'+ options.treeLocation +'_'+ options.infile+'.root') 
    h_NpassDataPre = filein2.Get("hNpassDataPre")
    h_NpassMuDataPre = filein2.Get("hNpassMuDataPre")
    h_NpassElDataPre = filein2.Get("hNpassElDataPre")
    h_NpassMCPre = filein2.Get("hNpassMCPre")
 
    h_meanDataPre = filein2.Get("hmeanDataPre")
    h_meanMuDataPre = filein2.Get("hmeanMuDataPre")
    h_meanElDataPre = filein2.Get("hmeanElDataPre")
    h_meanMCPre = filein2.Get("hmeanMCPre")
    h_sigmaDataPre = filein2.Get("hsigmaDataPre")
    h_sigmaMuDataPre = filein2.Get("hsigmaMuDataPre")
    h_sigmaElDataPre = filein2.Get("hsigmaElDataPre")
    h_sigmaMCPre = filein2.Get("hsigmaMCPre")


    for ibin in xrange(0,h_NpassMCPre.GetNbinsX()) :
        nMCpre[ibin] = h_NpassMCPre.GetBinContent(ibin+1)
        nDatapre[ibin] = h_NpassDataPre.GetBinContent(ibin+1)
        nMuDatapre[ibin] = h_NpassMuDataPre.GetBinContent(ibin+1)
        nElDatapre[ibin] = h_NpassElDataPre.GetBinContent(ibin+1)
        print "For bin " + str(ibin)+" : preselection in mudata {0:6.3}, eldata{0:6.3} and mc {0:6.3} ".format(nMuDatapre[ibin],nElDatapre[ibin], nMCpre[ibin])
    
    print "Reading means and widths of --pre Gaussian Fits for use in constraining the post W tag fits!"
    for ibin in xrange(0,h_sigmaMCPre.GetNbinsX() ) :
        MCmeans[ibin] = h_meanMCPre.GetBinContent(ibin+1)
        MCsigmas[ibin] = h_sigmaMCPre.GetBinContent(ibin+1)
        Datameans[ibin] = h_meanDataPre.GetBinContent(ibin+1)
        Datasigmas[ibin] = h_sigmaDataPre.GetBinContent(ibin+1)        
        MuDatameans[ibin] = h_meanMuDataPre.GetBinContent(ibin+1)
        MuDatasigmas[ibin] = h_sigmaMuDataPre.GetBinContent(ibin+1)
        ElDatameans[ibin] = h_meanElDataPre.GetBinContent(ibin+1)
        ElDatasigmas[ibin] = h_sigmaElDataPre.GetBinContent(ibin+1)

'''
titles = {
    'FatJetSDsubjetWpt':['SDsubjetWpt',';P_{T} of SD subjet 0 ( GeV ) ;Number of Events'],
    'FatJetSDsubjetWmass':['Wmass',';Mass_{SD subjet 0 }( GeV ) ;Number of Events'],
    }

variable = 'FatJetSDsubjetWmass'
cut = options.cut
name = titles[variable][0]
title = titles[variable][1]
'''

minval = options.minval
maxval = options.maxval
nbins = options.nbins
histbins = "(" + str(nbins) + ',' + str(minval) + ',' + str(maxval) + ")"


binlabels = [ "200 < P_{T} < 300  ",
              "300 < P_{T} < 400  ",
              "400 < P_{T} < 500  ",
                    "P_{T} > 500  ",
              "200 < P_{T} < 800  ",
              " #tau_{21} < 0.6 ",
              " #tau_{21} > 0.6 "]

# Rebin Values for Pt binned W candidate Mass histograms
rebinBybin = [ 1, 1, 1, 1, 1, 1, 1]

for ipt in xrange(0, len(binlabels) ) :
    if ipt <= 3: pt = ptBs[int(ipt)]
    binlabel = binlabels[int(ipt)]
    # Get the W candidate mass histograms
    if ipt == 0 :
        hdataT = hdata_b1.Clone()
        hdataTp = hdata_b1p.Clone()
        httbarT = httjets_b1.Clone()
        httbarTp = httjets_b1p.Clone()

        if options.allMC :
            hstT1 = hst1_b1.Clone()
            hstTp1 = hst1_b1p.Clone()
            hstT2 = hst2_b1.Clone()
            hstTp2 = hst2_b1p.Clone()
            hstT3 = hst3_b1.Clone()
            hstTp3 = hst3_b1p.Clone()
            hstT4 = hst4_b1.Clone()
            hstTp4 = hst4_b1p.Clone()
            hwjetsT1 = hwjets1_b1.Clone()
            hwjetsTp1 = hwjets1_b1p.Clone()
            hwjetsT2 = hwjets2_b1.Clone()
            hwjetsTp2 = hwjets2_b1p.Clone()
            hwjetsT3 = hwjets3_b1.Clone()
            hwjetsTp3 = hwjets3_b1p.Clone()
            hwjetsT4 = hwjets4_b1.Clone()
            hwjetsTp4 = hwjets4_b1p.Clone()
            hwjetsT5 = hwjets5_b1.Clone()
            hwjetsTp5 = hwjets5_b1p.Clone()
            hwjetsT6 = hwjets6_b1.Clone()
            hwjetsTp6 = hwjets6_b1p.Clone()
            hwjetsT7 = hwjets7_b1.Clone()
            hwjetsTp7 = hwjets7_b1p.Clone()

        #if options.Eldata:
        heldataT = heldata_b1.Clone()
        heldataTp = heldata_b1p.Clone() 
        #if options.Mudata:
        hmudataTp = hmudata_b1p.Clone()
        hmudataT = hmudata_b1.Clone()
    if ipt == 1 :
        hdataT = hdata_b2.Clone()
        hdataTp = hdata_b2p.Clone()
        httbarT = httjets_b2.Clone()
        httbarTp = httjets_b2p.Clone()

        if options.allMC :
            hstT1 = hst1_b2.Clone()
            hstTp1 = hst1_b2p.Clone()
            hstT2 = hst2_b2.Clone()
            hstTp2 = hst2_b2p.Clone()
            hstT3 = hst3_b2.Clone()
            hstTp3 = hst3_b2p.Clone()
            hstT4 = hst4_b2.Clone()
            hstTp4 = hst4_b2p.Clone()
            hwjetsT1 = hwjets1_b2.Clone()
            hwjetsTp1 = hwjets1_b2p.Clone()
            hwjetsT2 = hwjets2_b2.Clone()
            hwjetsTp2 = hwjets2_b2p.Clone()
            hwjetsT3 = hwjets3_b2.Clone()
            hwjetsTp3 = hwjets3_b2p.Clone()
            hwjetsT4 = hwjets4_b2.Clone()
            hwjetsTp4 = hwjets4_b2p.Clone()
            hwjetsT5 = hwjets5_b2.Clone()
            hwjetsTp5 = hwjets5_b2p.Clone()
            hwjetsT6 = hwjets6_b2.Clone()
            hwjetsTp6 = hwjets6_b2p.Clone()
            hwjetsT7 = hwjets7_b2.Clone()
            hwjetsTp7 = hwjets7_b2p.Clone()
        #if options.Eldata:
        heldataT = heldata_b2.Clone()
        heldataTp = heldata_b2p.Clone() 
        #if options.Mudata:
        hmudataTp = hmudata_b2p.Clone()
        hmudataT = hmudata_b2.Clone()
    if ipt == 2 :
        hdataT = hdata_b3.Clone()
        hdataTp = hdata_b3p.Clone()
        httbarT = httjets_b3.Clone()
        httbarTp = httjets_b3p.Clone()
        if options.allMC :
            hstT1 = hst1_b3.Clone()
            hstTp1 = hst1_b3p.Clone()
            hstT2 = hst2_b3.Clone()
            hstTp2 = hst2_b3p.Clone()
            hstT3 = hst3_b3.Clone()
            hstTp3 = hst3_b3p.Clone()
            hstT4 = hst4_b3.Clone()
            hstTp4 = hst4_b3p.Clone()
            hwjetsT1 = hwjets1_b3.Clone()
            hwjetsTp1 = hwjets1_b3p.Clone()
            hwjetsT2 = hwjets2_b3.Clone()
            hwjetsTp2 = hwjets2_b3p.Clone()
            hwjetsT3 = hwjets3_b3.Clone()
            hwjetsTp3 = hwjets3_b3p.Clone()
            hwjetsT4 = hwjets4_b3.Clone()
            hwjetsTp4 = hwjets4_b3p.Clone()
            hwjetsT5 = hwjets5_b3.Clone()
            hwjetsTp5 = hwjets5_b3p.Clone()
            hwjetsT6 = hwjets6_b3.Clone()
            hwjetsTp6 = hwjets6_b3p.Clone()
            hwjetsT7 = hwjets7_b3.Clone()
            hwjetsTp7 = hwjets7_b3p.Clone()
        #if options.Eldata:
        heldataT = heldata_b3.Clone()
        heldataTp = heldata_b3p.Clone() 
        #if options.Mudata:
        hmudataTp = hmudata_b3p.Clone()
        hmudataT = hmudata_b3.Clone()
    if ipt == 3 :
        hdataT = hdata_b4.Clone()
        hdataTp = hdata_b4p.Clone()
        httbarT = httjets_b4.Clone()
        httbarTp = httjets_b4p.Clone()
        if options.allMC :
            hstT1 = hst1_b4.Clone()
            hstTp1 = hst1_b4p.Clone()
            hstT2 = hst2_b4.Clone()
            hstTp2 = hst2_b4p.Clone()
            hstT3 = hst3_b4.Clone()
            hstTp3 = hst3_b4p.Clone()
            hstT4 = hst4_b4.Clone()
            hstTp4 = hst4_b4p.Clone()
            hwjetsT1 = hwjets1_b4.Clone()
            hwjetsTp1 = hwjets1_b4p.Clone()
            hwjetsT2 = hwjets2_b4.Clone()
            hwjetsTp2 = hwjets2_b4p.Clone()
            hwjetsT3 = hwjets3_b4.Clone()
            hwjetsTp3 = hwjets3_b4p.Clone()
            hwjetsT4 = hwjets4_b4.Clone()
            hwjetsTp4 = hwjets4_b4p.Clone()
            hwjetsT5 = hwjets5_b4.Clone()
            hwjetsTp5 = hwjets5_b4p.Clone()
            hwjetsT6 = hwjets6_b4.Clone()
            hwjetsTp6 = hwjets6_b4p.Clone()
            hwjetsT7 = hwjets7_b4.Clone()
            hwjetsTp7 = hwjets7_b4p.Clone()
        #if options.Eldata:
        heldataT = heldata_b4.Clone()
        heldataTp = heldata_b4p.Clone() 
        #if options.Mudata:
        hmudataTp = hmudata_b4p.Clone()
        hmudataT = hmudata_b4.Clone()
    if ipt == 4 :
        hdataT = hdata_b5.Clone()
        hdataTp = hdata_b5p.Clone()
        httbarT = httjets_b5.Clone()
        httbarTp = httjets_b5p.Clone()
        if options.allMC :
            hstT1 = hst1_b5.Clone()
            hstTp1 = hst1_b5p.Clone()
            hstT2 = hst2_b5.Clone()
            hstTp2 = hst2_b5p.Clone()
            hstT3 = hst3_b5.Clone()
            hstTp3 = hst3_b5p.Clone()
            hstT4 = hst4_b5.Clone()
            hstTp4 = hst4_b5p.Clone() 
            hwjetsT1 = hwjets1_b5.Clone()
            hwjetsTp1 = hwjets1_b5p.Clone()
            hwjetsT2 = hwjets2_b5.Clone()
            hwjetsTp2 = hwjets2_b5p.Clone()
            hwjetsT3 = hwjets3_b5.Clone()
            hwjetsTp3 = hwjets3_b5p.Clone()
            hwjetsT4 = hwjets4_b5.Clone()
            hwjetsTp4 = hwjets4_b5p.Clone()
            hwjetsT5 = hwjets5_b5.Clone()
            hwjetsTp5 = hwjets5_b5p.Clone()
            hwjetsT6 = hwjets6_b5.Clone()
            hwjetsTp6 = hwjets6_b5p.Clone()
            hwjetsT7 = hwjets7_b5.Clone()
            hwjetsTp7 = hwjets7_b5p.Clone()
        #if options.Eldata:
        heldataT = heldata_b5.Clone()
        heldataTp = heldata_b5p.Clone() 
        #if options.Mudata:
        hmudataTp = hmudata_b5p.Clone()
        hmudataT = hmudata_b5.Clone()
    if ipt == 5 :
        hdataT = hdata_Pass.Clone()
        httbarT = httbar_Pass.Clone()
        if options.allMC :
            hwjetsT1 = hwjets1_Pass.Clone()
            hwjetsT2 = hwjets2_Pass.Clone()
            hwjetsT3 = hwjets3_Pass.Clone()
            hwjetsT4 = hwjets4_Pass.Clone()
            hwjetsT5 = hwjets5_Pass.Clone()
            hwjetsT6 = hwjets6_Pass.Clone()
            hwjetsT7 = hwjets7_Pass.Clone()
            hstT1 = hst1_Pass.Clone()
            hstT2 = hst2_Pass.Clone()
            hstT3 = hst3_Pass.Clone()
            hstT4 = hst4_Pass.Clone() 
        heldataT = heldata_Pass.Clone()
        hmudataT = hmudata_Pass.Clone()
    if ipt == 6 :
        hdataT = hdata_Fail.Clone()
        httbarT = httbar_Fail.Clone()
        if options.allMC :
            hstT1 = hst1_Fail.Clone()
            hstT2 = hst2_Fail.Clone()
            hstT3 = hst3_Fail.Clone()
            hstT4 = hst4_Fail.Clone()
            hwjetsT1 = hwjets1_Fail.Clone()
            hwjetsT2 = hwjets2_Fail.Clone()
            hwjetsT3 = hwjets3_Fail.Clone()
            hwjetsT4 = hwjets4_Fail.Clone()
            hwjetsT5 = hwjets5_Fail.Clone()
            hwjetsT6 = hwjets6_Fail.Clone()
            hwjetsT7 = hwjets7_Fail.Clone()
        heldataT = heldata_Fail.Clone()
        hmudataT = hmudata_Fail.Clone()

    # Scale the histograms appropriately

    lumi = 12300.
    kfactorw = 1.21

    httbarT = scaleTT(httbarT)

    if options.allMC :
        hstT = scaleST(hstT1, hstT2, hstT3, hstT4)
        hwjetsT = scaleWjets(hwjetsT1, hwjetsT2, hwjetsT3, hwjetsT4, hwjetsT5, hwjetsT6, hwjetsT7)

    if ipt <=4 :

        httbarTp = scaleTTp(httbarTp)
        if options.allMC :
            hstTp = scaleSTp(hstTp1, hstTp2, hstTp3, hstTp4)
            hwjetsTp = scaleWjetsp(hwjetsTp1, hwjetsTp2, hwjetsTp3, hwjetsTp4, hwjetsTp5, hwjetsTp6, hwjetsTp7)
        
    # Find the tt scale factor
    sf = 0.
    scalefactortt = 0.
    if options.Eldata : 
        hdata = heldata.Clone()
        hdata.SetDirectory(0)
    if options.Mudata : 
        hdata = hmudata.Clone()
        hdata.SetDirectory(0)

    #if (httbar.Integral() > 0.):
        #httbar.Scale(lumi* 831.76 /97994456.) # 182123200.)
    hMC = httbar.Clone()
    hMC.SetDirectory(0)
    hMC.Sumw2()
    if options.allMC:
        hMC.Add(hstT)
        hMC.Add(hwjetsT)
    if (hdata.Integral() > 0.) and (hMC.Integral() > 0.) and options.ttSF: 
        diff = float(hdata.Integral())- float(  hMC.Integral()  )
        sf = abs(    diff/ float(  httbar.Integral()    +1.      )     )     
    if not options.ttSF: 
        sf = 1.
    if sf < 0. : print "NEGATIVE tt SCALE FACTOR"

    scalefactortt = sf 
    if options.ttSF: print "TT SCALE FACTOR APPLIED WAS : " + str(scalefactortt)

    if httbarT.Integral() > 0 : 
        httbarT.Scale( scalefactortt ) 
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt bin {0} empty".format(int(ipt))
        httbarT.Scale( 0.)
    if ipt < 5 :
        if httbarTp.Integral() > 0 : 
            httbarTp.Scale( scalefactortt )
        else :
            print "tt p bin {0} empty".format(int(ipt))
            httbarTp.Scale( 0.)

    # Rebin
    hdataT.Rebin(rebinBybin[ipt])
    hmudataT.Rebin(rebinBybin[ipt])
    heldataT.Rebin(rebinBybin[ipt])
    httbarT.Rebin(rebinBybin[ipt])

    if ipt < 5 :
        hdataTp.Rebin(rebinBybin[ipt])
        hmudataTp.Rebin(rebinBybin[ipt])
        heldataTp.Rebin(rebinBybin[ipt])
        httbarTp.Rebin(rebinBybin[ipt])
        if options.allMC :
            hstTp.Rebin(rebinBybin[ipt])
            hwjetsTp.Rebin(rebinBybin[ipt])
            hstTp.SetFillColor(ROOT.kCyan )
    if options.allMC :
        hstT.Rebin(rebinBybin[ipt])
        hwjetsT.Rebin(rebinBybin[ipt])
        hwjetsTp.SetFillColor(ROOT.kRed )
        hwjetsT.SetFillColor(ROOT.kRed)
        hstT.SetFillColor(ROOT.kCyan )

    httbarT.SetFillColor(ROOT.kGreen + 2)

    if ipt < 5 :
        httbarTp.SetFillColor(ROOT.kGreen + 2)

        hdataTp.SetMarkerStyle(20)
        hmudataTp.SetMarkerStyle(20)
        heldataTp.SetMarkerStyle(20)



    hdataT.SetMarkerStyle(20)
    hmudataT.SetMarkerStyle(20)
    heldataT.SetMarkerStyle(20)

    mc = ROOT.THStack('WmaSS','; Soft Drop Mass ( GeV ) ;Number of Events')
    if options.allMC :
        mc.Add( hwjetsT)
        mc.Add( hstT)
    mc.Add( httbarT)

    mchist = httbarT.Clone()
    if options.allMC : 
        mchist.Add( hwjetsT )
        mchist.Add( hstT )

    if options.pre :
        httbarT = httbarTp.Clone()

        if options.allMC :
            hwjetsT = hwjetsTp.Clone()
            hstT = hstTp.Clone()
        hdataT = hdataTp.Clone()
        hmudataT = hmudataTp.Clone()
        heldataT = heldataTp.Clone()

    #fitting

    if (2 <=ipt <= 3) :
        minn = options.min2
        maxx = options.max2
        if ipt > 2 :   
            minn = options.min3
            maxx = options.max3
    if ipt < 2:
        if ipt ==0 :
            minn = options.min0
            maxx = options.max0
        if ipt > 0 :
            minn = options.min1
            maxx = options.max1 

    fitter_data = ROOT.TF1("fitter_data", "gaus", minn , maxx )
    fitter_mudata = ROOT.TF1("fitter_mudata", "gaus",  minn , maxx  )
    fitter_eldata = ROOT.TF1("fitter_eldata", "gaus",  minn , maxx  )
    if ipt <= 3:
        data_meanval = Datameans[ipt]
        data_sigmaval = Datasigmas[ipt] 
        mudata_meanval = MuDatameans[ipt]
        mudata_sigmaval = MuDatasigmas[ipt] 
        eldata_meanval = ElDatameans[ipt]
        eldata_sigmaval = ElDatasigmas[ipt] 


    if options.fixFit :
        fitter_data.FixParameter(1, data_meanval)
        fitter_data.FixParameter(2, data_sigmaval)
        fitter_mudata.FixParameter(1, mudata_meanval)
        fitter_mudata.FixParameter(2, mudata_sigmaval)
        fitter_eldata.FixParameter(1, eldata_meanval)
        fitter_eldata.FixParameter(2, eldata_sigmaval)

    fitter_data.SetLineColor(1)
    fitter_data.SetLineWidth(2)
    fitter_data.SetLineStyle(2)
    fitter_mudata.SetLineColor(1)
    fitter_mudata.SetLineWidth(2)
    fitter_mudata.SetLineStyle(2)
    fitter_eldata.SetLineColor(1)
    fitter_eldata.SetLineWidth(2)
    fitter_eldata.SetLineStyle(2)
    if options.fixFit :
        hdataT.Fit(fitter_data,'B' )
        hmudataT.Fit(fitter_mudata,'B' )
        heldataT.Fit(fitter_eldata,'B' )
    else :
        hdataT.Fit(fitter_data,'R' )
        hmudataT.Fit(fitter_mudata,'R' )
        heldataT.Fit(fitter_eldata,'R' )

    amp_data    = fitter_data.GetParameter(0);
    eamp_data   = fitter_data.GetParError(0); 
    mean_data   = fitter_data.GetParameter(1);
    emean_data  = fitter_data.GetParError(1); 
    width_data  = fitter_data.GetParameter(2);
    ewidth_data = fitter_data.GetParError(2); 

    print 'Combined: amp_data {0:6.3}, eamp_data {1:6.3}, mean_data {2:6.3},emean_data {3:6.3}, width_data {4:6.3}, ewidth_data {5:6.3}  '.format(amp_data , eamp_data , mean_data, emean_data,  width_data, ewidth_data   ) 

    mamp_data    = fitter_mudata.GetParameter(0);
    meamp_data   = fitter_mudata.GetParError(0); 
    mmean_data   = fitter_mudata.GetParameter(1);
    memean_data  = fitter_mudata.GetParError(1); 
    mwidth_data  = fitter_mudata.GetParameter(2);
    mewidth_data = fitter_mudata.GetParError(2); 

    print 'Muon data: amp_data {0:6.3}, eamp_data {1:6.3}, mean_data {2:6.3},emean_data {3:6.3}, width_data {4:6.3}, ewidth_data {5:6.3}  '.format(mamp_data , meamp_data , mmean_data, memean_data,  mwidth_data, mewidth_data   ) 

    Eamp_data    = fitter_eldata.GetParameter(0);
    Eeamp_data   = fitter_eldata.GetParError(0); 
    Emean_data   = fitter_eldata.GetParameter(1);
    Eemean_data  = fitter_eldata.GetParError(1); 
    Ewidth_data  = fitter_eldata.GetParameter(2);
    Eewidth_data = fitter_eldata.GetParError(2); 

    print 'Electron data: amp_data {0:6.3}, eamp_data {1:6.3}, mean_data {2:6.3},emean_data {3:6.3}, width_data {4:6.3}, ewidth_data {5:6.3}  '.format(Eamp_data , Eeamp_data , Emean_data, Eemean_data,  Ewidth_data, Eewidth_data   ) 

    if options.pre and ipt <=3:
        Datameans[ipt] = mean_data
        Datasigmas[ipt] = width_data
        MuDatameans[ipt] = mmean_data
        MuDatasigmas[ipt] = mwidth_data
        ElDatameans[ipt] = Emean_data
        ElDatasigmas[ipt] = Ewidth_data




    fitter_mc = ROOT.TF1("fitter_mc", "gaus", minn , maxx )
    if ipt <=3:
        mc_meanval = MCmeans[ipt]
        mc_sigmaval = MCsigmas[ipt]


    if options.fixFit :
        fitter_mc.FixParameter(1, mc_meanval)
        fitter_mc.FixParameter(2, mc_sigmaval)

    fitter_mc.SetLineColor(4)
    fitter_mc.SetLineWidth(2)
    fitter_mc.SetLineStyle(4)
    if options.fixFit :
        mchist.Fit("fitter_mc",'B' )
    else :
        mchist.Fit("fitter_mc",'R' )
    amp_mc    = fitter_mc.GetParameter(0);
    eamp_mc   = fitter_mc.GetParError(0); 
    mean_mc   = fitter_mc.GetParameter(1);
    emean_mc  = fitter_mc.GetParError(1); 
    width_mc  = fitter_mc.GetParameter(2);
    ewidth_mc = fitter_mc.GetParError(2); 
          
    print 'MC : amp_mc {0:6.3}, eamp_mc {1:6.3}, mean_mc {2:6.3},emean_mc {3:6.3}, width_mc {4:6.3}, ewidth_mc {5:6.3}  '.format(amp_mc , eamp_mc , emean_mc, emean_mc,  width_mc, ewidth_mc   ) 
    if options.pre and ipt <=3 :
        MCmeans[ipt] = mean_mc
        MCsigmas[ipt] = width_mc


    meanrat = 1.0
    meanrat_uncert = meanrat
    jms = 1.0
    jms_uncert = jms
    
    binSizeData = hdataT.GetBinWidth(0)
    binSizeMC = mchist.GetBinWidth(0) # was mchist

    print "Bin size in data {0:1.2f} and MC  {1:1.2f}".format(binSizeData, binSizeMC )
    mclow = 0. 
    mchigh = 0.

    datalow = 0.
    datahigh = 0.
    if ipt <=3 :
        mclow = MCmeans[ipt] - MCsigmas[ipt] 
        mchigh = MCmeans[ipt] + MCsigmas[ipt] 

        datalow = Datameans[ipt] - Datasigmas[ipt] 
        datahigh = Datameans[ipt] + Datasigmas[ipt]

        mudatalow = MuDatameans[ipt] - MuDatasigmas[ipt] 
        mudatahigh = MuDatameans[ipt] + MuDatasigmas[ipt]

        eldatalow = ElDatameans[ipt] - ElDatasigmas[ipt] 
        eldatahigh = ElDatameans[ipt] + ElDatasigmas[ipt]

    mcAxis = mchist.GetXaxis()
    dataAxis = hdataT.GetXaxis()
    mudataAxis = hmudataT.GetXaxis()
    eldataAxis = heldataT.GetXaxis()

    bminmc = mcAxis.FindBin(mclow)
    bmaxmc = mcAxis.FindBin(mchigh)

    bmindata = hdataT.FindBin(datalow)
    bmaxdata = hdataT.FindBin(datahigh)

    bminmudata = hmudataT.FindBin(mudatalow)
    bmaxmudata = hmudataT.FindBin(mudatahigh)

    bmineldata = heldataT.FindBin(eldatalow)
    bmaxeldata = heldataT.FindBin(eldatahigh)

    if ipt <=3:
        if options.pre  :
            nMCpre[ipt] = mchist.Integral(bminmc , bmaxmc  ) #/ binSizeMC
            nDatapre[ipt] = hdataT.Integral(bmindata, bmaxdata  ) #/ binSizeData
            nMuDatapre[ipt] = hmudataT.Integral(bminmudata, bmaxmudata  ) #/ binSizeData
            nElDatapre[ipt] = heldataT.Integral(bmineldata, bmaxeldata  ) #/ binSizeData
            nMCupre[ipt] =  math.sqrt( nMCpre[ipt] )   #mchist.IntegralError(bminmc , bmaxmc  ) / binSizeMC
            nDataupre[ipt] = math.sqrt(nDatapre[ipt] ) #hdataT.IntegralError(bmindata, bmaxdata  ) / binSizeData
            nMuDataupre[ipt] = math.sqrt(nMuDatapre[ipt] ) 
            nElDataupre[ipt] = math.sqrt(nElDatapre[ipt] ) 
        else :
            nMCpost[ipt] = mchist.Integral(bminmc , bmaxmc  ) #/ binSizeMC
            nDatapost[ipt] = hdataT.Integral(bmindata, bmaxdata  ) #/ binSizeData
            nMuDatapost[ipt] = hmudataT.Integral(bminmudata, bmaxmudata  ) 
            nElDatapost[ipt] = heldataT.Integral(bmineldata, bmaxeldata  ) 
            nMCupost[ipt] =  math.sqrt( nMCpost[ipt] )  #mchist.IntegralError(bminmc , bmaxmc  ) / binSizeMC
            nDataupost[ipt] = math.sqrt(nDatapost[ipt] )#hdataT.IntegralError(bmindata, bmaxdata  ) / binSizeData
            nMuDataupost[ipt] = math.sqrt(nMuDatapost[ipt] )
            nElDataupost[ipt] = math.sqrt(nElDatapost[ipt] )

    meanrat = 0.
    meanrat_uncert = 0.
    meanratel_uncert = 0.
    meanratel = 0.
    meanratmu = 0.
    meanratmu_uncert = 0.
    if mean_mc > 0. : 
        meanrat = mean_data / mean_mc
        meanrat_uncert = meanrat * math.sqrt( (emean_data/mean_data)**2 + (emean_mc/mean_mc)**2 )
        if options.Mudata :
            meanratmu = mmean_data / mean_mc
            meanratmu_uncert = meanratmu * math.sqrt( (memean_data/mmean_data)**2 + (emean_mc/mean_mc)**2 )
        if options.Eldata :
            meanratel_uncert = 0.
            meanratel = 0.
            if  ( abs(Emean_data) > 0.01 ) and  ( abs(mean_mc) > 0.01 ) :
                meanratel = Emean_data / mean_mc
                meanratel_uncert = meanratel * math.sqrt( (Eemean_data/Emean_data)**2 + (emean_mc/mean_mc)**2 )
    jms = 0.
    jms_uncert = 0.
    jms_mu = 0.
    jms_mu_uncert = 0.
    jms_el = 0.
    jms_el_uncert = 0.
    if width_mc > 0. :
        jms = width_data / width_mc
        jms_uncert = jms * math.sqrt( (ewidth_data/width_data)**2 + (ewidth_mc/width_mc)**2 )
        if options.Mudata :
            jms_mu = mwidth_data / width_mc
            jms_mu_uncert = jms_mu * math.sqrt( (mewidth_data/mwidth_data)**2 + (ewidth_mc/width_mc)**2 )
        if options.Eldata :
            jms_el = Ewidth_data / width_mc
            jms_el_uncert =  0.0
            if abs(Ewidth_data) > 0.0001 :
                jms_el_uncert = jms_el * math.sqrt( (Eewidth_data/Ewidth_data)**2 + (ewidth_mc/width_mc)**2 )

    #print 'data_over_mc peak combined {0:6.3}, muon {1:6.3}, electron {2:6.3} '.format(meanrat, meanratmu, meanratel)
    #print '...........................................................'

    ibin = hpeak.GetXaxis().FindBin(pt)
    hpeak.SetBinContent(ibin, meanrat ) 
    hwidth.SetBinContent(ibin, jms )
    hpeak.SetBinError(ibin, meanrat_uncert)   
    hwidth.SetBinError(ibin, jms_uncert)

    if options.Mudata :
        hpeakmu.SetBinContent(ibin, meanratmu ) 
        hwidthmu.SetBinContent(ibin, jms_mu )
        hpeakmu.SetBinError(ibin, meanratmu_uncert)   
        hwidthmu.SetBinError(ibin, jms_mu_uncert)
    if options.Eldata :
        hpeakel.SetBinContent(ibin, meanratel ) 
        hwidthel.SetBinContent(ibin, jms_el )
        hpeakel.SetBinError(ibin, meanratel_uncert)   
        hwidthel.SetBinError(ibin, jms_el_uncert)

    if ipt <=3:
        if options.pre :
            ibin = hNpassDataPre.GetXaxis().FindBin(pt)
            hNpassDataPre.SetBinContent(ibin, nDatapre[ipt])
            hNpassMuDataPre.SetBinContent(ibin, nMuDatapre[ipt])
            hNpassElDataPre.SetBinContent(ibin, nElDatapre[ipt])
            hNpassMCPre.SetBinContent(ibin, nMCpre[ipt])
            hNpassDataPre.SetBinError(ibin, nDataupre[ipt])
            hNpassMuDataPre.SetBinError(ibin, nMuDataupre[ipt])
            hNpassElDataPre.SetBinError(ibin, nElDataupre[ipt])
            hNpassMCPre.SetBinError(ibin, nMCupre[ipt])
            hmeanDataPre.SetBinContent(ibin, Datameans[ipt]) 
            hmeanMuDataPre.SetBinContent(ibin, MuDatameans[ipt]) 
            hmeanElDataPre.SetBinContent(ibin, ElDatameans[ipt]) 
            hmeanMCPre.SetBinContent(ibin, MCmeans[ipt] )
            hsigmaDataPre.SetBinContent(ibin, Datasigmas[ipt])
            hsigmaMuDataPre.SetBinContent(ibin, MuDatasigmas[ipt])
            hsigmaElDataPre.SetBinContent(ibin, ElDatasigmas[ipt])
            hsigmaMCPre.SetBinContent(ibin,  MCsigmas[ipt] )
        else :
            ibin = hNpassDataPost.GetXaxis().FindBin(pt)
            hNpassDataPost.SetBinContent(ibin, nDatapost[ipt])
            hNpassMuDataPost.SetBinContent(ibin, nMuDatapost[ipt])
            hNpassElDataPost.SetBinContent(ibin, nElDatapost[ipt])
            hNpassMCPost.SetBinContent(ibin, nMCpost[ipt])
            hNpassDataPost.SetBinError(ibin, nDataupost[ipt])
            hNpassMuDataPost.SetBinError(ibin, nMuDataupost[ipt])
            hNpassElDataPost.SetBinError(ibin, nElDataupost[ipt])
            hNpassMCPost.SetBinError(ibin, nMCupost[ipt])


    #  DRAWING TIME!!!!!!!!!!!!

    if not options.quickPlot :
        ROOT.gStyle.SetOptFit(1111)
        ROOT.gStyle.SetOptStat(0000000000)
        cmsTextFont   = 61  

        if not (options.Mudata and options.Eldata) :
            c = ROOT.TCanvas('WmaSS','WmaSS',50,50,W,H)
            c.SetFillColor(0)
            c.SetBorderMode(0)
            c.SetFrameFillStyle(0)
            c.SetFrameBorderMode(0)
            c.SetLeftMargin( L/W )
            c.SetRightMargin( R/W )
            c.SetTopMargin( T/H )
            c.SetBottomMargin( B/H )
            c.SetTickx(0)
            c.SetTicky(0)

            #hdataT.Draw('e')
            mc.Draw("histsame")
            hdataT.Draw('esamex0')

            #hdataT.Draw('e same')
            #hdataT.Draw("axis same")
            fitter_mc.Draw("same")
            fitter_data.Draw("same")

            CMS_lumi.CMS_lumi(c, iPeriod, iPos)

            if not options.legleft : 
                leg = ROOT.TLegend( 0.698, 0.316, 0.816, 0.5106)  #leg = ROOT.TLegend( 0.746, 0.691, 0.864, 0.886)
            else :
                leg = ROOT.TLegend( 0.746, 0.691, 0.864, 0.886)
            leg.SetFillColor(0)
            leg.SetBorderSize(0)

            leg.AddEntry( hdataT, 'Data', 'p')
            leg.AddEntry( httbarT, 't#bar{t}', 'f')
            if options.allMC :
                leg.AddEntry( hwjetsT, 'W + jets', 'f')
                leg.AddEntry( hstT, 'Single Top', 'f')
            '''
            leg.AddEntry( hzjets, 'Z+Jets', 'f')

            '''
            max1 = hdataT.GetMaximum()
            max2 = mc.GetMaximum() # mc.GetHistogram().GetMaximum()

            hdataT.SetMaximum( max (max1,max2) * 1.618 )

            hdataT.GetXaxis().SetRangeUser( 40.0, 130. )
            mc.GetXaxis().SetRangeUser( 40.0, 130. )

            if options.Type2 :
                hdataT.SetXTitle("Soft Drop Jet Mass (GeV)")
            if not options.Type2 :
                hdataT.SetXTitle("Soft Drop Subjet Mass (GeV)")
            hdataT.SetYTitle("Events")
            hdata.BufferEmpty(1)
            hdataT.GetXaxis().SetTitleSize(0.047)
            hdataT.GetYaxis().SetTitleSize(0.047)

            leg.Draw()

            tlx = ROOT.TLatex()
            tlx.SetNDC()
            tlx.SetTextFont(42)
            tlx.SetTextSize(0.057)
            #tlx.DrawLatex(0.68, 0.957,  str(lumi) + " fb^{-1} (13TeV)")
            tlx.DrawLatex(0.67, 0.86, binlabel )
            c.Update()
            c.Draw()
            sele = options.filestr
            if options.pre :
                sele = options.filestr + '_preWTag'
            if ipt < 5 :
                c.Print(plotdir + '/AllData/wMass_Bin'+ str(ipt) + '_' + sele + '.png', 'png' )
                c.Print(plotdir + '/AllData/wMass_Bin'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
                c.Print(plotdir + '/AllData/wMass_Bin'+ str(ipt) + '_' + sele + '.root', 'root' )
            if ipt == 5 :
                c.Print(plotdir + '/AllData/wMass_passTau21Loose'+ str(ipt) + '_' + sele + '.png', 'png' )
                c.Print(plotdir + '/AllData/wMass_passTau21Loose'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
                c.Print(plotdir + '/AllData/wMass_passTau21Loose'+ str(ipt) + '_' + sele + '.root', 'root' )
            if ipt == 6 :
                c.Print(plotdir + '/AllData/wMass_failTau21Loose'+ str(ipt) + '_' + sele + '.png', 'png' )
                c.Print(plotdir + '/AllData/wMass_failTau21Loose'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
                c.Print(plotdir + '/AllData/wMass_failTau21Loose'+ str(ipt) + '_' + sele + '.root', 'root' )

        if options.Mudata:
            cc = ROOT.TCanvas('WmaSSMu','WmaSSMu',50,50,W,H)
            cc.SetFillColor(0)
            cc.SetBorderMode(0)
            cc.SetFrameFillStyle(0)
            cc.SetFrameBorderMode(0)
            cc.SetLeftMargin( L/W )
            cc.SetRightMargin( R/W )
            cc.SetTopMargin( T/H )
            cc.SetBottomMargin( B/H )
            cc.SetTickx(0)
            cc.SetTicky(0)

            hmudataT.Draw('e')
            mc.Draw("histsame")
            hmudataT.Draw('esamex0')

            hmudataT.Draw('e same')
            hmudataT.Draw("axis same")
            fitter_mc.Draw("same")
            fitter_mudata.Draw("same")

            CMS_lumi.CMS_lumi(cc, iPeriod, iPos)

            if not options.legleft : 
                leg = ROOT.TLegend( 0.698, 0.316, 0.816, 0.5106)  #leg = ROOT.TLegend( 0.746, 0.691, 0.864, 0.886)
            else :
                leg = ROOT.TLegend( 0.746, 0.691, 0.864, 0.886)
            leg.SetFillColor(0)
            leg.SetBorderSize(0)

            leg.AddEntry( hmudataT, 'Muon Data', 'p')
            leg.AddEntry( httbarT, 't#bar{t}', 'f')
            if options.allMC :
                leg.AddEntry( hwjetsT, 'W + jets', 'f')
                leg.AddEntry( hstT, 'Single Top', 'f')
            '''
            leg.AddEntry( hzjets, 'Z+Jets', 'f')

            '''
            max1 = hmudataT.GetMaximum()
            max2 = mc.GetMaximum() # mc.GetHistogram().GetMaximum()
            hmudataT.GetXaxis().SetRangeUser( 40.0, 130. )
            mc.GetXaxis().SetRangeUser( 40.0, 130. )

            hmudataT.SetMaximum( max (max1,max2) * 1.618 )

            hmudataT.SetXTitle("Subjet Soft Drop Mass (GeV)")
            hmudataT.SetYTitle("Events")
            hmudataT.BufferEmpty(1)
            hmudataT.GetXaxis().SetTitleSize(0.047)
            hmudataT.GetYaxis().SetTitleSize(0.047)
            hmudataT.GetXaxis().SetLabelSize(0.04)
            hmudataT.GetYaxis().SetLabelSize(0.04)

            leg.Draw()

            tlx = ROOT.TLatex()
            tlx.SetNDC()
            tlx.SetTextFont(42)
            tlx.SetTextSize(0.057)

            tlx.DrawLatex(0.67, 0.86, binlabel )

            cc.Update()
            cc.Draw()
            sele = options.filestr
            if options.pre :
                sele = options.filestr + '_preWTag'
            if ipt < 5 :
                cc.Print(plotdir + '/MuData/wMass_Bin'+ str(ipt) + '_' + sele + '.png', 'png' )
                cc.Print(plotdir + '/MuData/wMass_Bin'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
                cc.Print(plotdir + '/MuData/wMass_Bin'+ str(ipt) + '_' + sele + '.root', 'root' )
            if ipt == 5 :
                cc.Print(plotdir + '/MuData/wMass_passTau21Loose'+ str(ipt) + '_' + sele + '.png', 'png' )
                cc.Print(plotdir + '/MuData/wMass_passTau21Loose'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
                cc.Print(plotdir + '/MuData/wMass_passTau21Loose'+ str(ipt) + '_' + sele + '.root', 'root' )
            if ipt == 6 :
                hmudataT.SetMaximum( 300. )
                mc.SetMaximum( 300. )
                cc.Print(plotdir + '/MuData/wMass_failTau21Loose'+ str(ipt) + '_' + sele + '.png', 'png' )
                cc.Print(plotdir + '/MuData/wMass_failTau21Loose'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
                cc.Print(plotdir + '/MuData/wMass_failTau21Loose'+ str(ipt) + '_' + sele + '.root', 'root' )

        if options.Eldata :
            ccc = ROOT.TCanvas('WmaSSel','WmaSSel',50,50,W,H)
            ccc.SetFillColor(0)
            ccc.SetBorderMode(0)
            ccc.SetFrameFillStyle(0)
            ccc.SetFrameBorderMode(0)
            ccc.SetLeftMargin( L/W )
            ccc.SetRightMargin( R/W )
            ccc.SetTopMargin( T/H )
            ccc.SetBottomMargin( B/H )
            ccc.SetTickx(0)
            ccc.SetTicky(0)

            heldataT.Draw('e')
            mc.Draw("histsame")
            heldataT.Draw('esamex0')

            heldataT.Draw('e same')
            heldataT.Draw("axis same")
            fitter_mc.Draw("same")
            fitter_eldata.Draw("same")

            CMS_lumi.CMS_lumi(ccc, iPeriod, iPos)

            if not options.legleft : 
                leg = ROOT.TLegend( 0.698, 0.316, 0.816, 0.5106)  #leg = ROOT.TLegend( 0.746, 0.691, 0.864, 0.886)
            else :
                leg = ROOT.TLegend( 0.746, 0.691, 0.864, 0.886)
            leg.SetFillColor(0)
            leg.SetBorderSize(0)

            leg.AddEntry( heldataT, 'Electron Data', 'p')
            leg.AddEntry( httbarT, 't#bar{t}', 'f')
            if options.allMC :
                leg.AddEntry( hwjetsT, 'W + jets', 'f')
                leg.AddEntry( hstT, 'Single Top', 'f')

            max1 = heldataT.GetMaximum()
            max2 = mc.GetMaximum() # mc.GetHistogram().GetMaximum()

            heldataT.SetMaximum( max (max1,max2) * 1.618 )

            heldataT.SetXTitle("Subjet Soft Drop Mass (GeV)")
            heldataT.SetYTitle("Events")
            heldataT.BufferEmpty(1)
            heldataT.GetXaxis().SetTitleSize(0.047)
            heldataT.GetYaxis().SetTitleSize(0.047)
            heldataT.GetXaxis().SetLabelSize(0.04)
            heldataT.GetYaxis().SetLabelSize(0.04)

            leg.Draw()

            tlx = ROOT.TLatex()
            tlx.SetNDC()
            tlx.SetTextFont(42)
            tlx.SetTextSize(0.057)
            tlx.DrawLatex(0.67, 0.86, binlabel )


            ccc.Update()
            ccc.Draw()
            sele = options.filestr
            if options.pre :
                sele = options.filestr + '_preWTag'
            ccc.Print(plotdir + '/ElData/wMass_Bin'+ str(ipt) + '_' + sele + '.png', 'png' )
            ccc.Print(plotdir + '/ElData/wMass_Bin'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
            ccc.Print(plotdir + '/ElData/wMass_Bin'+ str(ipt) + '_' + sele + '.root', 'root' )
            if ipt == 5 :
                ccc.Print(plotdir + '/ElData/wMass_passTau21Loose'+ str(ipt) + '_' + sele + '.png', 'png' )
                ccc.Print(plotdir + '/ElData/wMass_passTau21Loose'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
                ccc.Print(plotdir + '/ElData/wMass_passTau21Loose'+ str(ipt) + '_' + sele + '.root', 'root' )
            if ipt == 6 :
                ccc.Print(plotdir + '/ElData/wMass_failTau21Loose'+ str(ipt) + '_' + sele + '.png', 'png' )
                ccc.Print(plotdir + '/ElData/wMass_failTau21Loose'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
                ccc.Print(plotdir + '/ElData/wMass_failTau21Loose'+ str(ipt) + '_' + sele + '.root', 'root' )

        if ipt <=4:
            ee = ROOT.TCanvas('wid','wid')
            hwidth.Draw('e')

            hwidth.SetMarkerStyle(20)
            hwidth.SetMaximum(3.0)
            hwidth.SetMinimum(0.0)

            CMS_lumi.CMS_lumi(ee, iPeriod, iPos)

            ee.Update()
            ee.Draw()

            if  options.Eldata : # working here 
                ee.Print(plotdir + '/ElData/JMR_W_' + str(options.filestr) + '.png', 'png' )
                ee.Print(plotdir + '/ElData/JMR_W_' + str(options.filestr) + '.pdf', 'pdf' )
                ee.Print(plotdir + '/ElData/JMR_W_' + str(options.filestr) + '.root', 'root' )
            elif options.Mudata : # working here 
                ee.Print(plotdir + '/MuData/JMR_W_' + str(options.filestr) + '.png', 'png' )
                ee.Print(plotdir + '/MuData/JMR_W_' + str(options.filestr) + '.pdf', 'pdf' )
                ee.Print(plotdir + '/MuData/JMR_W_' + str(options.filestr) + '.root', 'root' )
            elif not (options.Eldata and options.Mudata): # working here 
                ee.Print(plotdir + '/AllData/JMR_W_' + str(options.filestr) + '.png', 'png' )
                ee.Print(plotdir + '/AllData/JMR_W_' + str(options.filestr) + '.pdf', 'pdf' )
                ee.Print(plotdir + '/AllData/JMR_W_' + str(options.filestr) + '.root', 'root' )


        if options.PlotPtTypes : # FIX THIS : fill these histos in selector code
            ff = ROOT.TCanvas('P_t_Comparison','P_t_Comparison')
            ff.SetLogy()
            hpts.Draw()
            hpts2.Draw('same')
            hptsMC.Draw('same')
            hpts2MC.Draw('same')
            hpts.SetLineColor(ROOT.kBlue)
            hpts2.SetLineColor(ROOT.kCyan)
            hptsMC.SetLineColor(ROOT.kMagenta)
            hpts2MC.SetLineColor(ROOT.kGreen)
           
            xmax =  1000.

            hpts2.GetXaxis().SetRangeUser(0.0,xmax)
            hpts.GetXaxis().SetRangeUser(0.0, xmax)
            hpts2MC.GetXaxis().SetRangeUser(0.0,xmax)
            hptsMC.GetXaxis().SetRangeUser(0.0, xmax)

            maxpt2y = hpts2.GetMaximum()
            maxpty = hpts.GetMaximum()
            maxpt2MCy = hpts2MC.GetMaximum()
            maxptMCy = hptsMC.GetMaximum()

            maxpt = 1.618 * max(maxpt2y, maxpty, maxpt2MCy, maxptMCy)

            hpts2.SetMaximum(maxpt)
            #hpts2.SetMinimum(maxpt)
            hpts.SetMaximum(maxpt)
            #hpts.SetMinimum()
            hpts2MC.SetMaximum(maxpt)
            #hpts2MC.SetMinimum(0.0001)
            hptsMC.SetMaximum(maxpt)


            CMS_lumi.CMS_lumi(ff, iPeriod, iPos)
            tlx = ROOT.TLatex()
            tlx.SetNDC()
            tlx.SetTextFont(42)
            tlx.SetTextSize(0.057)

            legy = ROOT.TLegend( 0.68, 0.68, 0.799, 0.875)
            legy.SetFillColor(0)
            legy.SetBorderSize(0)

            legy.AddEntry( hpts, 'Data: Type 1', 'l')
            legy.AddEntry( hpts2, 'Data: Type 2', 'l')
            legy.AddEntry( hptsMC, 'MC: Type 1', 'l')
            legy.AddEntry( hpts2MC, 'MC: Type 2', 'l')
            legy.Draw()

            ff.Update()
            ff.Draw()
            ff.Print(plotdir + '/AllData/Pt_type1and2_' + options.filestr + '.png', 'png' )
            ff.Print(plotdir + '/AllData/Pt_type1and2_' + options.filestr + '.pdf', 'pdf' )
            ff.Print(plotdir + '/AllData/Pt_type1and2_' + options.filestr + '.root', 'root' )

        if ipt <= 3:
            gg = ROOT.TCanvas('peak','peak')
            hpeak.Draw('e')

            hpeak.SetMarkerStyle(20)
            #hpeak.GetYaxis().SetRange(0.8,1.0)
            hpeak.SetMaximum(3.0)
            hpeak.SetMinimum(0.0)

            CMS_lumi.CMS_lumi(gg, iPeriod, iPos)

            tlx = ROOT.TLatex()
            tlx.SetNDC()
            tlx.SetTextFont(42)
            tlx.SetTextSize(0.057)

            gg.Update()
            gg.Draw() 
            if  options.Eldata : # working here 
                gg.Print(plotdir + '/ElData/JMS_W_' + options.filestr + '.png', 'png' )
                gg.Print(plotdir + '/ElData/JMS_W_' + options.filestr + '.pdf', 'pdf' )
                gg.Print(plotdir + '/ElData/JMS_W_' + options.filestr + '.root', 'root' )
            elif options.Mudata : # working here 
                gg.Print(plotdir + '/MuData/JMS_W_' + options.filestr + '.png', 'png' )
                gg.Print(plotdir + '/MuData/JMS_W_' + options.filestr + '.pdf', 'pdf' )
                gg.Print(plotdir + '/MuData/JMS_W_' + options.filestr + '.root', 'root' )
            elif not (options.Mudata and options.Eldata): # working here 
                gg.Print(plotdir + '/AllData/JMS_W_' + options.filestr + '.png', 'png' )
                gg.Print(plotdir + '/AllData/JMS_W_' + options.filestr + '.pdf', 'pdf' )
                gg.Print(plotdir + '/AllData/JMS_W_' + options.filestr + '.root', 'root' )

if not options.quickPlot :
    #   SF =  ( nData / nDatap ) / ( nMC / nMCp )
    print "Integrals of fitted mass peak for W subjet of high Pt top:"


    print "##################  DATA  #############################"

    print "N pass post W tag Data pt 200-300 : " + str( nDatapost[0])
    print "N pass pre W tag Data pt 200-300 : " + str(nDatapre[0])

    print "N pass post W tag Data pt 300-400 : " + str(nDatapost[1])
    print "N pass pre W tag Data pt 300-400 : " + str(nDatapre[1])

    print "N pass post W tag Data pt 400-500 : " + str(nDatapost[2])
    print "N pass pre W tag Data pt 400-500 : " + str(nDatapre[2])

    print "N pass post W tag Data pt 500-inf : " + str(nDatapost[3])
    print "N pass pre W tag Data pt 500-inf : " + str(nDatapre[3])


    print "##################   MC   #############################"

    print "N pass post W tag MC pt 200-300 : " + str( nMCpost[0])
    print "N pass pre W tag MC pt 200-300 : " + str(nMCpre[0])

    print "N pass post W tag MC pt 300-400 : " + str(nMCpost[1])
    print "N pass pre W tag MC pt 300-400 : " + str(nMCpre[1])

    print "N pass post W tag MC pt 400-500 : " + str(nMCpost[2])
    print "N pass pre W tag MC pt 400-500 : " + str(nMCpre[2])

    print "N pass post W tag MC pt 500-inf : " + str(nMCpost[3])
    print "N pass pre W tag MC pt 500-inf : " + str(nMCpre[3])



    print "###############################################"




    if not options.pre :
        for ipt in xrange(0, len(ptBs)-1 ) :
            if options.Mudata :
                datapost = nMuDatapost[ipt] 
                datapre  = nMuDatapre[ipt] 

            if options.Eldata :
                datapost = nElDatapost[ipt] 
                datapre  = nElDatapre[ipt] 

            if not (options.Eldata and options.Mudata):
                datapost = nDatapost[ipt] 
                datapre  = nDatapre[ipt] 
            pt = ptBs[ipt]
            ptToFill = float(pt)
            if pt > 800. :
                ptToFill = 799.
            if (nDatapre[ipt] > 0. and nMCpre[ipt] > 0. and pt >= 301.) :
                SF =  ( float(datapost) / float(datapre) ) / ( float(nMCpost[ipt]) / float(nMCpre[ipt]) )
                SF_sd = SF * math.sqrt(   (- float(datapost) + float(datapre) ) / ( float(datapost) * float(datapre) )  + (-float(nMCpost[ipt]) + float(nMCpre[ipt])) / (float(nMCpost[ipt]) * float(nMCpre[ipt]))  )
                print "............................................"
                print "             SCALE FACTOR                   "
                print "............................................"
                print "pt Bin lower bound in GeV :  " + str(pt)
                print "Preliminary W tagging SF from subjet w : " + str(SF)
                print "Data efficiency for this  bin {0:5.3}".format(  float(datapost) / float(datapre) )
                print "MC efficiency for this  bin" + str(float(nMCpost[ipt]) / float(nMCpre[ipt]))
                print "standard deviation : " + str(SF_sd)
                print "............................................"
                ibin = hscale.GetXaxis().FindBin(ptToFill)
                hscale.SetBinContent(ibin, SF )
                hscale.SetBinError(ibin, SF_sd)
            else :
                ibin = hscale.GetXaxis().FindBin(ptToFill)
                hscale.SetBinContent(ibin, 0.0 )




        # DRAWING TIME!

         #ROOT.gStyle.SetOptFit(1111)
        ROOT.gStyle.SetOptStat(0000000000)

        #d = ROOT.TCanvas('sf','sf')
        d = ROOT.TCanvas('sf','sf',50,50,W,H)
        d.SetFillColor(0)
        d.SetBorderMode(0)
        d.SetFrameFillStyle(0)
        d.SetFrameBorderMode(0)
        d.SetLeftMargin( L/W )
        d.SetRightMargin( R/W )
        d.SetTopMargin( T/H )
        d.SetBottomMargin( B/H )
        d.SetTickx(0)
        d.SetTicky(0)



        hscale.Draw('P')

        hscale.SetMaximum(2.)
        hscale.SetMinimum(0.0)

        hscale.SetMarkerStyle(20)

        hscale.SetXTitle("Subjet P_{T} (GeV)")
        hscale.SetYTitle("Scale Factor")
        hscale.BufferEmpty(1)
        hscale.GetXaxis().SetTitleSize(0.047)
        hscale.GetYaxis().SetTitleSize(0.047)
        hscale.GetXaxis().SetLabelSize(0.04)
        hscale.GetYaxis().SetLabelSize(0.04)

        CMS_lumi.CMS_lumi(d, iPeriod, iPos)


        #hscale.GetYaxis().SetRange(0.8,1.0)

        tlx = ROOT.TLatex()
        tlx.SetNDC()
        tlx.SetTextFont(42)
        tlx.SetTextSize(0.057)
        tlx.SetTextSize(0.029)
        xInfo = 0.15
        yInfoTop = 0.475
        yInfo2 = yInfoTop-0.042
        yInfo3 = yInfo2-0.042
        yInfo4 = yInfo3-0.042
        yInfo5 = yInfo4-0.042
        yInfo6 = yInfo5-0.042
        yInfo7 = yInfo6-0.042
        yInfo8 = yInfo7-0.042

        d.Update()
        d.Draw()



if options.quickPlot or not options.quickPlot: 

    httbarT_lepst = scaleTT(httbar_lepst)
    httbarT_lepst.SetFillColor(ROOT.kGreen + 2)
    rb = 5
    httbarT_lepst.Rebin(rb)
    hdata_lepst.Rebin(rb)
    heldata_lepst.Rebin(rb)
    hmudata_lepst.Rebin(rb)

    if options.allMC :
        hstT_lepst = scaleST(hst1_lepst, hst2_lepst, hst3_lepst, hst4_lepst) 
        hwjetsT_lepst = scaleWjets(hwjets1_lepst , hwjets2_lepst, hwjets3_lepst, hwjets4_lepst, hwjets5_lepst, hwjets6_lepst, hwjets7_lepst)
        hstT_lepst.SetFillColor(ROOT.kCyan )
        hwjetsT_lepst.SetFillColor(ROOT.kRed)
        hstT_lepst.Rebin(rb)
        hwjetsT_lepst.Rebin(rb)


    mcst = ROOT.THStack('Lept','; st of Lepton ( GeV ) ;Number of Events') #Mass_{SD subjet_{0} }
    if options.allMC :
        mcst.Add( hwjetsT_lepst)
        mcst.Add( hstT_lepst)
    mcst.Add( httbarT_lepst)


    ffea = ROOT.TCanvas('lepton st','lepton st')
    ffea.SetFillColor(0)
    ffea.SetBorderMode(0)
    ffea.SetFrameFillStyle(0)
    ffea.SetFrameBorderMode(0)
    ffea.SetLeftMargin( L/W )
    ffea.SetRightMargin( R/W )
    ffea.SetTopMargin( T/H )
    ffea.SetBottomMargin( B/H )
    ffea.SetTickx(0)
    ffea.SetTicky(0)
    hdata_lepst.SetMarkerStyle(20)
    hmudata_lepst.SetMarkerStyle(20)
    heldata_lepst.SetMarkerStyle(20)
    max1 = hdata_lepst.GetMaximum()
    hdata_lepst.GetXaxis().SetLimits(50.,500.)
    heldata_lepst.GetXaxis().SetLimits(50.,500.)
    hmudata_lepst.GetXaxis().SetLimits(50.,500.)
    max2 = mcst.GetMaximum()
    hdata_lepst.SetMaximum( max (max1,max2) * 1.618 )
    heldata_lepst.SetMaximum( max (max1,max2) * 1.618 )
    hmudata_lepst.SetMaximum( max (max1,max2) * 1.618 )
    hdata_lepst.GetYaxis().SetTitleOffset(1.9)
    heldata_lepst.GetYaxis().SetTitleOffset(1.9)
    hmudata_lepst.GetYaxis().SetTitleOffset(1.9)
    heldata_lepst.SetXTitle("St (HT +HTLep) (GeV)")
    heldata_lepst.SetYTitle("Events")
    hmudata_lepst.SetXTitle("St (HT +HTLep) (GeV)")
    hmudata_lepst.SetYTitle("Events")
    hdata_lepst.SetXTitle("Pt (HT +HTLep) (GeV)")
    hdata_lepst.SetYTitle("Events")
    heldata_lepst.BufferEmpty(1)
    heldata_lepst.GetXaxis().SetTitleSize(0.057)
    heldata_lepst.GetYaxis().SetTitleSize(0.057)
    if options.Eldata :
        heldata_lepst.Draw('e')
    if options.Mudata :
        hmudata_lepst.Draw('e')
    if not (options.Mudata or options.Eldata ) :
        hdata_lepst.Draw('e')

    mcst.Draw("histsame")
    if options.Eldata :
        #heldata_lepst.Draw('e same')
        heldata_lepst.Draw('esamex0')
        heldata_lepst.Draw('axis same')
    elif options.Mudata :
        hmudata_lepst.Draw('esamex0')
        #hmudata_lepst.Draw('e same')
        hmudata_lepst.Draw('axis same')
    elif not (options.Mudata and options.Eldata ) :
        hdata_lepst.Draw('esamex0')
        #hdata_lepst.Draw('e same')
        hdata_lepst.Draw('axis same')

    CMS_lumi.CMS_lumi(ffea, iPeriod, iPos)

    leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

    if options.Eldata :
        leg.AddEntry( heldata_lepst, 'Electron Data', 'p')
    elif options.Mudata :
        leg.AddEntry( hmudata_lepst, 'Muon Data', 'p')
    elif not (options.Mudata and options.Eldata ) :
        leg.AddEntry( hdata_lepst, 'Data', 'p')


    leg.AddEntry( httbarT_lepst, 't#bar{t}', 'f')
    if options.allMC :
        leg.AddEntry( hwjetsT_lepst, 'W + jets', 'f')
        leg.AddEntry( hstT_lepst, 'Single Top', 'f')
    leg.Draw()

    ffea.Update()
    ffea.Draw()
    if options.Mudata :
        ffea.Print(plotdir + '/MuData/st_lepton_' + options.filestr + '.png', 'png' )
        ffea.Print(plotdir + '/MuData/st_lepton_' + options.filestr + '.pdf', 'pdf' )
        ffea.Print(plotdir + '/MuData/st_lepton_' + options.filestr + '.root', 'root' )
    elif options.Eldata :
        ffea.Print(plotdir + '/ElData/st_lepton_' + options.filestr + '.png', 'png' )
        ffea.Print(plotdir + '/ElData/st_lepton_' + options.filestr + '.pdf', 'pdf' )
        ffea.Print(plotdir + '/ElData/st_lepton_' + options.filestr + '.root', 'root' )
    elif not (options.Mudata and options.Eldata):
        ffea.Print(plotdir + '/AllData/st_lepton_' + options.filestr + '.png', 'png' )
        ffea.Print(plotdir + '/AllData/st_lepton_' + options.filestr + '.pdf', 'pdf' )
        ffea.Print(plotdir + '/AllData/st_lepton_' + options.filestr + '.root', 'root' )



    httbarT_taus = scaleTT(httbar_ak8SJtau21)
    httbarT_taus.SetFillColor(ROOT.kGreen + 2)

    rb = 5
    httbarT_taus.Rebin(rb)
    hdata_ak8SJtau21.Rebin(rb)
    heldata_ak8SJtau21.Rebin(rb)
    hmudata_ak8SJtau21.Rebin(rb)
    if options.allMC :
        hstT_taus = scaleST(hst1_ak8SJtau21, hst2_ak8SJtau21, hst3_ak8SJtau21, hst4_ak8SJtau21)
        hwjetsT_taus = scaleWjets(hwjets1_ak8SJtau21, hwjets2_ak8SJtau21, hwjets3_ak8SJtau21, hwjets4_ak8SJtau21, hwjets5_ak8SJtau21, hwjets6_ak8SJtau21, hwjets7_ak8SJtau21)
        hstT_taus.SetFillColor(ROOT.kCyan )
        hwjetsT_taus.SetFillColor(ROOT.kRed )
        hstT_taus.Rebin(rb)
        hwjetsT_taus.Rebin(rb)

    mctaus = ROOT.THStack('Leptaus',';Subjet #tau_21  ;Number of Events') #Mass_{SD subjet_{0} }
    if options.allMC :
        mctaus.Add( hwjetsT_taus)
        mctaus.Add( hstT_taus)
    mctaus.Add( httbarT_taus)

    if not options.Type2:
        ffezw = ROOT.TCanvas('subjet tau 21','subjet tau 21')
        ffezw.SetFillColor(0)
        ffezw.SetBorderMode(0)
        ffezw.SetFrameFillStyle(0)
        ffezw.SetFrameBorderMode(0)
        ffezw.SetLeftMargin( L/W )
        ffezw.SetRightMargin( R/W )
        ffezw.SetTopMargin( T/H )
        ffezw.SetBottomMargin( B/H )
        ffezw.SetTickx(0)
        ffezw.SetTicky(0)
        hdata_ak8SJtau21.SetMarkerStyle(20)
        hmudata_ak8SJtau21.SetMarkerStyle(20)
        heldata_ak8SJtau21.SetMarkerStyle(20)
        max1 = hdata_ak8SJtau21.GetMaximum()
        max2 = mctau.GetMaximum()
        hdata_ak8SJtau21.SetMaximum( max (max1,max2) * 1.618 )
        heldata_ak8SJtau21.SetMaximum( max (max1,max2) * 1.618 )
        hmudata_ak8SJtau21.SetMaximum( max (max1,max2) * 1.618 )
        hdata_ak8SJtau21.GetYaxis().SetTitleOffset(1.4)
        heldata_ak8SJtau21.GetYaxis().SetTitleOffset(1.4)
        hmudata_ak8SJtau21.GetYaxis().SetTitleOffset(1.4)
        heldata_ak8SJtau21.SetXTitle("Subjet #tau_{21}")
        heldata_ak8SJtau21.SetYTitle("Events")
        hmudata_ak8SJtau21.SetXTitle("Subjet #tau_{21}")
        hmudata_ak8SJtau21.SetYTitle("Events")
        hdata_ak8SJtau21.SetXTitle("subjet #tau_{21}")
        hdata_ak8SJtau21.SetYTitle("Events")
        heldata_ak8SJtau21.BufferEmpty(1)
        heldata_ak8SJtau21.GetXaxis().SetTitleSize(0.067)
        heldata_ak8SJtau21.GetYaxis().SetTitleSize(0.067)
        heldata_ak8SJtau21.GetXaxis().SetLabelSize(0.04)
        heldata_ak8SJtau21.GetYaxis().SetLabelSize(0.04)
        if options.Eldata :
            heldata_ak8SJtau21.Draw('e')
        if options.Mudata :
            hmudata_ak8SJtau21.Draw('e')
        if not (options.Mudata or options.Eldata ) :
            hdata_ak8SJtau21.Draw('e')

        mctaus.Draw("histsame")
        if options.Eldata :
            heldata_ak8SJtau21.Draw('esamex0')
            heldata_ak8SJtau21.Draw('axis same')
        if options.Mudata :
            hmudata_ak8SJtau21.Draw('esamex0')
            hmudata_ak8SJtau21.Draw('axis same')
        if not (options.Mudata or options.Eldata ) :
            hdata_ak8SJtau21.Draw('esamex0')
            hdata_ak8SJtau21.Draw('axis same')

        CMS_lumi.CMS_lumi(ffezw, iPeriod, iPos)

        leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
        leg.SetFillColor(0)
        leg.SetBorderSize(0)

        if options.Eldata :
            leg.AddEntry( heldata_ak8SJtau21, 'Electron Data', 'p')
        elif options.Mudata :
            leg.AddEntry( hmudata_ak8SJtau21, 'Muon Data', 'p')
        elif not (options.Mudata and options.Eldata ) :
            leg.AddEntry( hdata_ak8SJtau21, 'Data', 'p')


        leg.AddEntry( httbarT_taus, 't#bar{t}', 'f')
        if ptions.allMC:
            leg.AddEntry( hwjetsT_taus, 'W + jets', 'f')
            leg.AddEntry( hstT_taus, 'Single Top', 'f')
        leg.Draw()

        ffezw.Update()
        ffezw.Draw()
        if options.Eldata :
            ffezw.Print(plotdir + '/ElData/ak8SJtau21_' + options.filestr + '.png', 'png' )
            ffezw.Print(plotdir + '/ElData/ak8SJtau21_' + options.filestr + '.pdf', 'pdf' )
            ffezw.Print(plotdir + '/ElData/ak8SJtau21_' + options.filestr + '.root', 'root' )
        elif options.Mudata :
            ffezw.Print(plotdir + '/MuData/ak8SJtau21_' + options.filestr + '.png', 'png' )
            ffezw.Print(plotdir + '/MuData/ak8SJtau21_' + options.filestr + '.pdf', 'pdf' )
            ffezw.Print(plotdir + '/MuData/ak8SJtau21_' + options.filestr + '.root', 'root' )
        elif not (options.Mudata and options.Eldata):
            ffezw.Print(plotdir + '/AllData/ak8SJtau21_' + options.filestr + '.png', 'png' )
            ffezw.Print(plotdir + '/AllData/ak8SJtau21_' + options.filestr + '.pdf', 'pdf' )
            ffezw.Print(plotdir + '/AllData/ak8SJtau21_' + options.filestr + '.root', 'root' )

    httbarT_tau = scaleTT(httbar_ak8tau21)
    httbarT_tau.SetFillColor(ROOT.kGreen + 2)
    rb = 5
    httbarT_tau.Rebin(rb)

    if options.allMC:
        hstT_tau = scaleST(hst1_ak8tau21, hst2_ak8tau21, hst3_ak8tau21, hst4_ak8tau21)
        hwjetsT_tau = scaleWjets(hwjets1_ak8tau21, hwjets2_ak8tau21, hwjets3_ak8tau21, hwjets4_ak8tau21, hwjets5_ak8tau21, hwjets6_ak8tau21, hwjets7_ak8tau21)
        hstT_tau.SetFillColor(ROOT.kCyan )
        hwjetsT_tau.SetFillColor(ROOT.kRed )
        hstT_tau.Rebin(rb)
        hwjetsT_tau.Rebin(rb)
    hdata_ak8tau21.Rebin(rb)
    heldata_ak8tau21.Rebin(rb)
    hmudata_ak8tau21.Rebin(rb)

    mctau = ROOT.THStack('Leptau','; #tau_21  ;Number of Events') #Mass_{SD subjet_{0} }
    mctau.Add( httbarT_tau )
    if options.allMC :
        mctau.Add( hstT_tau)
        mctau.Add( hwjetsT_tau)


    ffez = ROOT.TCanvas('tau 21','tau 21')
    ffez.SetFillColor(0)
    ffez.SetBorderMode(0)
    ffez.SetFrameFillStyle(0)
    ffez.SetFrameBorderMode(0)
    ffez.SetLeftMargin( L/W )
    ffez.SetRightMargin( R/W )
    ffez.SetTopMargin( T/H )
    ffez.SetBottomMargin( B/H )
    ffez.SetTickx(0)
    ffez.SetTicky(0)
    hdata_ak8tau21.SetMarkerStyle(20)
    hmudata_ak8tau21.SetMarkerStyle(20)
    heldata_ak8tau21.SetMarkerStyle(20)
    max1 = hdata_ak8tau21.GetMaximum()
    max2 = mctau.GetMaximum()
    hdata_ak8tau21.SetMaximum( max (max1,max2) * 1.618 )
    heldata_ak8tau21.SetMaximum( max (max1,max2) * 1.618 )
    hmudata_ak8tau21.SetMaximum( max (max1,max2) * 1.618 )
    hdata_ak8tau21.GetYaxis().SetTitleOffset(1.4)
    heldata_ak8tau21.GetYaxis().SetTitleOffset(1.4)
    hmudata_ak8tau21.GetYaxis().SetTitleOffset(1.4)
    heldata_ak8tau21.SetXTitle("#tau_{21}")
    heldata_ak8tau21.SetYTitle("Events")
    hmudata_ak8tau21.SetXTitle("#tau_{21}")
    hmudata_ak8tau21.SetYTitle("Events")
    hdata_ak8tau21.SetXTitle("#tau_{21}")
    hdata_ak8tau21.SetYTitle("Events")
    heldata_ak8tau21.BufferEmpty(1)
    heldata_ak8tau21.GetXaxis().SetTitleSize(0.067)
    heldata_ak8tau21.GetYaxis().SetTitleSize(0.067)
    heldata_ak8tau21.GetXaxis().SetLabelSize(0.04)
    heldata_ak8tau21.GetYaxis().SetLabelSize(0.04)
    if options.Eldata :
        heldata_ak8tau21.Draw('e')
    if options.Mudata :
        hmudata_ak8tau21.Draw('e')
    if not (options.Mudata or options.Eldata ) :
        hdata_ak8tau21.Draw('e')

    mctau.Draw("histsame")
    if options.Eldata :
        heldata_ak8tau21.Draw('esamex0')
        heldata_ak8tau21.Draw('axis same')
    if options.Mudata :
        hmudata_ak8tau21.Draw('esamex0')
        hmudata_ak8tau21.Draw('axis same')
    if not (options.Mudata or options.Eldata ) :
        hdata_ak8tau21.Draw('esamex0')
        hdata_ak8tau21.Draw('axis same')

    CMS_lumi.CMS_lumi(ffez, iPeriod, iPos)

    leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

    if options.Eldata :
        leg.AddEntry( heldata_ak8tau21, 'Electron Data', 'p')
    elif options.Mudata :
        leg.AddEntry( hmudata_ak8tau21, 'Muon Data', 'p')
    elif not (options.Mudata and options.Eldata ) :
        leg.AddEntry( hdata_ak8tau21, 'Data', 'p')


    leg.AddEntry( httbarT_tau, 't#bar{t}', 'f')
    if options.allMC :
        leg.AddEntry( hwjetsT_tau, 'W + jets', 'f')
        leg.AddEntry( hstT_tau, 'Single Top', 'f')
    leg.Draw()

    ffez.Update()
    ffez.Draw()
    if options.Eldata :
        ffez.Print(plotdir + '/ElData/AK8tau21_' + options.filestr + '.png', 'png' )
        ffez.Print(plotdir + '/ElData/AK8tau21_' + options.filestr + '.pdf', 'pdf' )
        ffez.Print(plotdir + '/ElData/AK8tau21_' + options.filestr + '.root', 'root' )
    elif options.Mudata :
        ffez.Print(plotdir + '/MuData/AK8tau21_' + options.filestr + '.png', 'png' )
        ffez.Print(plotdir + '/MuData/AK8tau21_' + options.filestr + '.pdf', 'pdf' )
        ffez.Print(plotdir + '/MuData/AK8tau21_' + options.filestr + '.root', 'root' )
    elif not (options.Mudata and options.Eldata):
        ffez.Print(plotdir + '/AllData/AK8tau21_' + options.filestr + '.png', 'png' )
        ffez.Print(plotdir + '/AllData/AK8tau21_' + options.filestr + '.pdf', 'pdf' )
        ffez.Print(plotdir + '/AllData/AK8tau21_' + options.filestr + '.root', 'root' )







    # Plot the Lepton Pt before all selection except  # FINISH THEIS presleceyion lepton plots

    httbarTp_leppt = scaleTT(httbarp_leppt)

    print "TT SCALE FACTOR APPLIED to Lepton Pt WAS : " + str(1. )

    if httbarT_leppt.Integral() > 0 : 
        httbarT_leppt.Scale( 1. ) 
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt lepton pt histo is empty".format(int(ipt))
        httbarT_leppt.Scale( 0.)


    httbarT_leppt.SetFillColor(ROOT.kGreen + 2)
    httbarT_leppt.GetXaxis().SetLimits(50.,600.)
    rebinPt = 3
    httbarT_leppt.Rebin( rebinPt )
    hdata_leppt.Rebin( rebinPt )
    heldata_leppt.Rebin( rebinPt )
    hmudata_leppt.Rebin( rebinPt )

    if options.allMC :
        hstT_leppt = scaleST(hst1_leppt, hst2_leppt, hst3_leppt, hst4_leppt) 
        hwjetsT_leppt = scaleWjets(hwjets1_leppt , hwjets2_leppt, hwjets3_leppt, hwjets4_leppt, hwjets5_leppt, hwjets6_leppt, hwjets7_leppt)
        hstT_leppt.SetFillColor(ROOT.kCyan )
        hwjetsT_leppt.SetFillColor(ROOT.kRed)
        hstT_leppt.Rebin(  rebinPt )
        hwjetsT_leppt.Rebin(  rebinPt )
        hstT_leppt.GetXaxis().SetLimits(50.,600.)
        hwjetsT_leppt.GetXaxis().SetLimits(50.,600.)

    mcpts = ROOT.THStack('Lept','; Pt of Lepton ( GeV ) ;Number of Events') #Mass_{SD subjet_{0} }
    if options.allMC :
        mcpts.Add( hwjetsT_leppt)
        mcpts.Add( hstT_leppt)
    mcpts.Add( httbarT_leppt)


    ffe = ROOT.TCanvas('lepton pt','lepton pt')
    ffe.SetFillColor(0)
    ffe.SetBorderMode(0)
    ffe.SetFrameFillStyle(0)
    ffe.SetFrameBorderMode(0)
    ffe.SetLeftMargin( L/W )
    ffe.SetRightMargin( R/W )
    ffe.SetTopMargin( T/H )
    ffe.SetBottomMargin( B/H )
    ffe.SetTickx(0)
    ffe.SetTicky(0)
    hdata_leppt.SetMarkerStyle(20)
    hmudata_leppt.SetMarkerStyle(20)
    heldata_leppt.SetMarkerStyle(20)
    max1 = hdata_leppt.GetMaximum()
    max2 = mcpts.GetMaximum()
    hdata_leppt.GetXaxis().SetLimits(50.,600.)
    heldata_leppt.GetXaxis().SetLimits(50.,600.)
    hmudata_leppt.GetXaxis().SetLimits(50.,600.)

    hdata_leppt.SetMaximum( max (max1,max2) * 1.618 )
    heldata_leppt.SetMaximum( max (max1,max2) * 1.618 )
    hmudata_leppt.SetMaximum( max (max1,max2) * 1.618 )

    hdata_leppt.GetYaxis().SetTitleOffset(1.9)
    heldata_leppt.GetYaxis().SetTitleOffset(1.9)
    hmudata_leppt.GetYaxis().SetTitleOffset(1.9)
    heldata_leppt.SetXTitle("Pt of Lepton (GeV)")
    heldata_leppt.SetYTitle("Events")
    hmudata_leppt.SetXTitle("Pt of Lepton (GeV)")
    hmudata_leppt.SetYTitle("Events")
    hdata_leppt.SetXTitle("Pt of Lepton (GeV)")
    hdata_leppt.SetYTitle("Events")
    heldata_leppt.BufferEmpty(1)
    heldata_leppt.GetXaxis().SetTitleSize(0.057)
    heldata_leppt.GetYaxis().SetTitleSize(0.057)
    hdata_leppt.BufferEmpty(1)
    hdata_leppt.GetXaxis().SetTitleSize(0.057)
    hdata_leppt.GetYaxis().SetTitleSize(0.057)
    hmudata_leppt.BufferEmpty(1)
    hmudata_leppt.GetXaxis().SetTitleSize(0.057)
    hmudata_leppt.GetYaxis().SetTitleSize(0.057)      
    binSizeMuDataPt = hmudata_leppt.GetBinWidth(0)
    binSizeMCPt = httbarT_leppt.GetBinWidth(0)
    #if ( binSizeMuDataPt != binSizeMCPt ) :  
    print "Bin size: data {0:1.2f}, MC  {1:1.2f}- rebinpt is {2:1.0f}".format(binSizeMuDataPt, binSizeMCPt,  rebinPt )

    if options.Eldata :
        heldata_leppt.Draw('e')
    if options.Mudata :
        hmudata_leppt.Draw('e')
    if not (options.Mudata and options.Eldata ) :
        hdata_leppt.Draw('e')

    mcpts.Draw("histsame")
    if options.Eldata :
        #heldata_leppt.Draw('e same')
        heldata_leppt.Draw('esamex0')
        heldata_leppt.Draw('axis same')
    elif options.Mudata :
        hmudata_leppt.Draw('esamex0')
        hmudata_leppt.Draw('e same')
        hmudata_leppt.Draw('axis same')
    elif not (options.Mudata and options.Eldata ) :
        hdata_leppt.Draw('esamex0')
        #hdata_leppt.Draw('e same')
        hdata_leppt.Draw('axis same')


    CMS_lumi.CMS_lumi(ffe, iPeriod, iPos)

    leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

    if options.Eldata :
        leg.AddEntry( heldata_leppt, 'Electron Data', 'p')
    elif options.Mudata :
        leg.AddEntry( hmudata_leppt, 'Muon Data', 'p')
    elif not (options.Mudata and options.Eldata ) :
        leg.AddEntry( hdata_leppt, 'Data', 'p')


    leg.AddEntry( httbarT_leppt, 't#bar{t}', 'f')
    if options.allMC :
        leg.AddEntry( hwjetsT_leppt, 'W + jets', 'f')
        leg.AddEntry( hstT_leppt, 'Single Top', 'f')
    leg.Draw()

    ffe.Update()
    ffe.Draw()
    if options.Mudata :
        ffe.Print(plotdir + '/MuData/Pt_lepton_preSel_' + options.filestr + '.png', 'png' )
        ffe.Print(plotdir + '/MuData/Pt_lepton_preSel_' + options.filestr + '.pdf', 'pdf' )
        ffe.Print(plotdir + '/MuData/Pt_lepton_preSel_' + options.filestr + '.root', 'root' )
    elif options.Eldata :
        ffe.Print(plotdir + '/ElData/Pt_lepton_preSel_' + options.filestr + '.png', 'png' )
        ffe.Print(plotdir + '/ElData/Pt_lepton_preSel_' + options.filestr + '.pdf', 'pdf' )
        ffe.Print(plotdir + '/ElData/Pt_lepton_preSel_' + options.filestr + '.root', 'root' )
    elif not (options.Mudata and options.Eldata):
        ffe.Print(plotdir + '/AllData/Pt_lepton_preSel_' + options.filestr + '.png', 'png' )
        ffe.Print(plotdir + '/AllData/Pt_lepton_preSel_' + options.filestr + '.pdf', 'pdf' )
        ffe.Print(plotdir + '/AllData/Pt_lepton_preSel_' + options.filestr + '.root', 'root' )

    # Plot the Lepton Pt after selection

    httbarT_leppt = scaleTT(httbar_leppt)

    print "TT SCALE FACTOR APPLIED to Lepton Pt WAS : " + str(1. )

    if httbarT_leppt.Integral() > 0 : 
        httbarT_leppt.Scale( 1. ) 
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt lepton pt histo is empty".format(int(ipt))
        httbarT_leppt.Scale( 0.)


    httbarT_leppt.SetFillColor(ROOT.kGreen + 2)
    httbarT_leppt.GetXaxis().SetLimits(50.,600.)
    rebinPt = 3
    httbarT_leppt.Rebin( rebinPt )
    hdata_leppt.Rebin( rebinPt )
    heldata_leppt.Rebin( rebinPt )
    hmudata_leppt.Rebin( rebinPt )

    if options.allMC :
        hstT_leppt = scaleST(hst1_leppt, hst2_leppt, hst3_leppt, hst4_leppt) 
        hwjetsT_leppt = scaleWjets(hwjets1_leppt , hwjets2_leppt, hwjets3_leppt, hwjets4_leppt, hwjets5_leppt, hwjets6_leppt, hwjets7_leppt)
        hstT_leppt.SetFillColor(ROOT.kCyan )
        hwjetsT_leppt.SetFillColor(ROOT.kRed)
        hstT_leppt.Rebin(  rebinPt )
        hwjetsT_leppt.Rebin(  rebinPt )
        hstT_leppt.GetXaxis().SetLimits(50.,600.)
        hwjetsT_leppt.GetXaxis().SetLimits(50.,600.)

    mcpts = ROOT.THStack('Lept','; Pt of Lepton ( GeV ) ;Number of Events') #Mass_{SD subjet_{0} }
    if options.allMC :
        mcpts.Add( hwjetsT_leppt)
        mcpts.Add( hstT_leppt)
    mcpts.Add( httbarT_leppt)


    ffe = ROOT.TCanvas('lepton pt','lepton pt')
    ffe.SetFillColor(0)
    ffe.SetBorderMode(0)
    ffe.SetFrameFillStyle(0)
    ffe.SetFrameBorderMode(0)
    ffe.SetLeftMargin( L/W )
    ffe.SetRightMargin( R/W )
    ffe.SetTopMargin( T/H )
    ffe.SetBottomMargin( B/H )
    ffe.SetTickx(0)
    ffe.SetTicky(0)
    hdata_leppt.SetMarkerStyle(20)
    hmudata_leppt.SetMarkerStyle(20)
    heldata_leppt.SetMarkerStyle(20)
    max1 = hdata_leppt.GetMaximum()
    max2 = mcpts.GetMaximum()
    hdata_leppt.GetXaxis().SetLimits(50.,600.)
    heldata_leppt.GetXaxis().SetLimits(50.,600.)
    hmudata_leppt.GetXaxis().SetLimits(50.,600.)

    hdata_leppt.SetMaximum( max (max1,max2) * 1.618 )
    heldata_leppt.SetMaximum( max (max1,max2) * 1.618 )
    hmudata_leppt.SetMaximum( max (max1,max2) * 1.618 )

    hdata_leppt.GetYaxis().SetTitleOffset(1.9)
    heldata_leppt.GetYaxis().SetTitleOffset(1.9)
    hmudata_leppt.GetYaxis().SetTitleOffset(1.9)
    heldata_leppt.SetXTitle("Pt of Lepton (GeV)")
    heldata_leppt.SetYTitle("Events")
    hmudata_leppt.SetXTitle("Pt of Lepton (GeV)")
    hmudata_leppt.SetYTitle("Events")
    hdata_leppt.SetXTitle("Pt of Lepton (GeV)")
    hdata_leppt.SetYTitle("Events")
    heldata_leppt.BufferEmpty(1)
    heldata_leppt.GetXaxis().SetTitleSize(0.057)
    heldata_leppt.GetYaxis().SetTitleSize(0.057)
    hdata_leppt.BufferEmpty(1)
    hdata_leppt.GetXaxis().SetTitleSize(0.057)
    hdata_leppt.GetYaxis().SetTitleSize(0.057)
    hmudata_leppt.BufferEmpty(1)
    hmudata_leppt.GetXaxis().SetTitleSize(0.057)
    hmudata_leppt.GetYaxis().SetTitleSize(0.057)      
    binSizeMuDataPt = hmudata_leppt.GetBinWidth(0)
    binSizeMCPt = httbarT_leppt.GetBinWidth(0)
    #if ( binSizeMuDataPt != binSizeMCPt ) :  
    print "Bin size: data {0:1.2f}, MC  {1:1.2f}- rebinpt is {2:1.0f}".format(binSizeMuDataPt, binSizeMCPt,  rebinPt )

    if options.Eldata :
        heldata_leppt.Draw('e')
    if options.Mudata :
        hmudata_leppt.Draw('e')
    if not (options.Mudata and options.Eldata ) :
        hdata_leppt.Draw('e')

    mcpts.Draw("histsame")
    if options.Eldata :
        #heldata_leppt.Draw('e same')
        heldata_leppt.Draw('esamex0')
        heldata_leppt.Draw('axis same')
    elif options.Mudata :
        hmudata_leppt.Draw('esamex0')
        hmudata_leppt.Draw('e same')
        hmudata_leppt.Draw('axis same')
    elif not (options.Mudata and options.Eldata ) :
        hdata_leppt.Draw('esamex0')
        #hdata_leppt.Draw('e same')
        hdata_leppt.Draw('axis same')


    CMS_lumi.CMS_lumi(ffe, iPeriod, iPos)

    leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

    if options.Eldata :
        leg.AddEntry( heldata_leppt, 'Electron Data', 'p')
    elif options.Mudata :
        leg.AddEntry( hmudata_leppt, 'Muon Data', 'p')
    elif not (options.Mudata and options.Eldata ) :
        leg.AddEntry( hdata_leppt, 'Data', 'p')


    leg.AddEntry( httbarT_leppt, 't#bar{t}', 'f')
    if options.allMC :
        leg.AddEntry( hwjetsT_leppt, 'W + jets', 'f')
        leg.AddEntry( hstT_leppt, 'Single Top', 'f')
    leg.Draw()

    ffe.Update()
    ffe.Draw()
    if options.Mudata :
        ffe.Print(plotdir + '/MuData/Pt_lepton_postSel_' + options.filestr + '.png', 'png' )
        ffe.Print(plotdir + '/MuData/Pt_lepton_postSel_' + options.filestr + '.pdf', 'pdf' )
        ffe.Print(plotdir + '/MuData/Pt_lepton_postSel_' + options.filestr + '.root', 'root' )
    elif options.Eldata :
        ffe.Print(plotdir + '/ElData/Pt_lepton_postSel_' + options.filestr + '.png', 'png' )
        ffe.Print(plotdir + '/ElData/Pt_lepton_postSel_' + options.filestr + '.pdf', 'pdf' )
        ffe.Print(plotdir + '/ElData/Pt_lepton_postSel_' + options.filestr + '.root', 'root' )
    elif not (options.Mudata and options.Eldata):
        ffe.Print(plotdir + '/AllData/Pt_lepton_postSel_' + options.filestr + '.png', 'png' )
        ffe.Print(plotdir + '/AllData/Pt_lepton_postSel_' + options.filestr + '.pdf', 'pdf' )
        ffe.Print(plotdir + '/AllData/Pt_lepton_' + options.filestr + '.root', 'root' )

    #Plot the Ht of the lepton


    httbarT_lephtlep = scaleTT(httbar_lephtlep)
    httbarT_lephtlep.SetFillColor(ROOT.kGreen + 2)
    rb = 5
    httbarT_lephtlep.Rebin(rb)
    hdata_lephtlep.Rebin(rb)
    heldata_lephtlep.Rebin(rb)
    hmudata_lephtlep.Rebin(rb)

    if options.allMC :
        hstT_lephtlep = scaleST(hst1_lephtlep, hst2_lephtlep, hst3_lephtlep, hst4_lephtlep) 
        hwjetsT_lephtlep = scaleWjets(hwjets1_lephtlep , hwjets2_lephtlep, hwjets3_lephtlep, hwjets4_lephtlep, hwjets5_lephtlep, hwjets6_lephtlep, hwjets7_lephtlep)
        hstT_lephtlep.SetFillColor(ROOT.kCyan )
        hwjetsT_lephtlep.SetFillColor(ROOT.kRed)
        hstT_lephtlep.Rebin(rb)
        hwjetsT_lephtlep.Rebin(rb)


    mchtlep = ROOT.THStack('Lept','; Ht of Lepton ( GeV ) ;Number of Events') #Mass_{SD subjet_{0} }
    if options.allMC :
        mchtlep.Add( hwjetsT_lephtlep)
        mchtlep.Add( hstT_lephtlep)
    mchtlep.Add( httbarT_lephtlep)
    ffer = ROOT.TCanvas('lepton ht','lepton ht')
    ffer.SetFillColor(0)
    ffer.SetBorderMode(0)
    ffer.SetFrameFillStyle(0)
    ffer.SetFrameBorderMode(0)
    ffer.SetLeftMargin( L/W )
    ffer.SetRightMargin( R/W )
    ffer.SetTopMargin( T/H )
    ffer.SetBottomMargin( B/H )
    ffer.SetTickx(0)
    ffer.SetTicky(0)
    hdata_lephtlep.SetMarkerStyle(20)
    hmudata_lephtlep.SetMarkerStyle(20)
    heldata_lephtlep.SetMarkerStyle(20)
    max1 = hdata_lephtlep.GetMaximum()
    hdata_lephtlep.GetXaxis().SetLimits(50.,500.)
    heldata_lephtlep.GetXaxis().SetLimits(50.,500.)
    hmudata_lephtlep.GetXaxis().SetLimits(50.,500.)
    max2 = mchtlep.GetMaximum()
    hdata_lephtlep.SetMaximum( max (max1,max2) * 1.618 )
    heldata_lephtlep.SetMaximum( max (max1,max2) * 1.618 )
    hmudata_lephtlep.SetMaximum( max (max1,max2) * 1.618 )
    hdata_lephtlep.GetYaxis().SetTitleOffset(1.9)
    heldata_lephtlep.GetYaxis().SetTitleOffset(1.9)
    hmudata_lephtlep.GetYaxis().SetTitleOffset(1.9)
    heldata_lephtlep.SetXTitle("Ht of Lepton (GeV)")
    heldata_lephtlep.SetYTitle("Events")
    hmudata_lephtlep.SetXTitle("Ht of Lepton (GeV)")
    hmudata_lephtlep.SetYTitle("Events")
    hdata_lephtlep.SetXTitle("Ht of Lepton (GeV)")
    hdata_lephtlep.SetYTitle("Events")
    heldata_lephtlep.BufferEmpty(1)
    heldata_lephtlep.GetXaxis().SetTitleSize(0.057)
    heldata_lephtlep.GetYaxis().SetTitleSize(0.057)
    if options.Eldata :
        heldata_lephtlep.Draw('e')
    if options.Mudata :
        hmudata_lephtlep.Draw('e')
    if not (options.Mudata or options.Eldata ) :
        hdata_lephtlep.Draw('e')

    mchtlep.Draw("histsame")
    if options.Eldata :
        #heldata_lephtlep.Draw('e same')
        heldata_lephtlep.Draw('esamex0')
        heldata_lephtlep.Draw('axis same')
    elif options.Mudata :
        hmudata_lephtlep.Draw('esamex0')
        #hmudata_lephtlep.Draw('e same')
        hmudata_lephtlep.Draw('axis same')
    elif not (options.Mudata and options.Eldata ) :
        hdata_lephtlep.Draw('esamex0')
        #hdata_lephtlep.Draw('e same')
        hdata_lephtlep.Draw('axis same')

    CMS_lumi.CMS_lumi(ffer, iPeriod, iPos)

    leg = ROOT.TLegend(0.7,0.7,0.9,0.9)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)

    if options.Eldata :
        leg.AddEntry( heldata_lephtlep, 'Electron Data', 'p')
    elif options.Mudata :
        leg.AddEntry( hmudata_lephtlep, 'Muon Data', 'p')
    elif not (options.Mudata and options.Eldata ) :
        leg.AddEntry( hdata_lephtlep, 'Data', 'p')


    leg.AddEntry( httbarT_lephtlep, 't#bar{t}', 'f')
    if options.allMC :
        leg.AddEntry( hwjetsT_lephtlep, 'W + jets', 'f')
        leg.AddEntry( hstT_lephtlep, 'Single Top', 'f')
    leg.Draw()

    ffer.Update()
    ffer.Draw()
    if options.Mudata :
        ffer.Print(plotdir + '/MuData/ht_lepton_' + options.filestr + '.png', 'png' )
        ffer.Print(plotdir + '/MuData/ht_lepton_' + options.filestr + '.pdf', 'pdf' )
        ffer.Print(plotdir + '/MuData/ht_lepton_' + options.filestr + '.root', 'root' )
    elif options.Eldata :
        ffer.Print(plotdir + '/ElData/ht_lepton_' + options.filestr + '.png', 'png' )
        ffer.Print(plotdir + '/ElData/ht_lepton_' + options.filestr + '.pdf', 'pdf' )
        ffer.Print(plotdir + '/ElData/ht_lepton_' + options.filestr + '.root', 'root' )
    elif not (options.Mudata and options.Eldata):
        ffer.Print(plotdir + '/AllData/ht_lepton_' + options.filestr + '.png', 'png' )
        ffer.Print(plotdir + '/AllData/ht_lepton_' + options.filestr + '.pdf', 'pdf' )
        ffer.Print(plotdir + '/AllData/ht_lepton_' + options.filestr + '.root', 'root' )

fout.cd()
fout.Write()
fout.Close()
