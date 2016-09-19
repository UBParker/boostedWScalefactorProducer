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

parser.add_option('--PlotPtTypes', action='store_true',
              default=False,
              dest='PlotPtTypes',
              help='Do you want to plot the Pts of type 1 vs Type 2 W jet candidates???')

parser.add_option('--filestr', type='string', action='store',
                  dest='filestr',
                  default = "nom",
                  help='Label for plots')

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

parser.add_option('--fixFit',  action='store_true',
                  dest='fixFit',
                  default = False,
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

0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref


ROOT.gStyle.SetTitleOffset(1.0, "Y")



fout= ROOT.TFile('./output80xplotter/Wtag_highPtScaleFactor_80x_' + str(datatype)+ '_'+ options.infile + '.root', "RECREATE")


if options.pre :
    datatype = 'Alldata'
    if options.Mudata :
        datatype = 'Mudata'
    if options.Eldata :
        datatype = 'Eldata'
    fout= ROOT.TFile('./output80xplotter/Wtag_highPtScaleFactor_preWTag_80x_'+str(datatype)+ '_'+ options.infile + '.root', "RECREATE")
        
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
dtypes = ['data', 'ttjets']
filesin = [] 
for dt in enumerate(dtypes) :
    filesin.append['./output80xselector/histos_80x_' + dt + '_'+ options.filestr + '.root'
print "Using input files :  {0}".format(filesin)

# Luminosity of input dataset
lumi = 12300. #2136.0

# Get histos from input files

h_data = []
h_eldata = []
h_mudata = []
h_ttjets = []
h_wjets = []
h_st = []

hp_data = []
hp_eldata = []
hp_mudata = []
hp_ttjets = []
hp_wjets = []
hp_st = []

for ifin, fin in enumerate(filesin) :
    filei = ROOT.TFile.Open( fin )
    if dtypes[ifin] == 'data' :
        hdata = filein.Get("h_mWsubjet_Data")

        h_data = [filein.Get("h_mWsubjet_b1"),
                  filein.Get("h_mWsubjet_b2"),
                  filein.Get("h_mWsubjet_b3"),
                  filein.Get("h_mWsubjet_b4")]
        hp_data = [filein.Get("h_mWsubjet_b1p"),
                   filein.Get("h_mWsubjet_b2p"),
                   filein.Get("h_mWsubjet_b3p"),
                   filein.Get("h_mWsubjet_b4p")]
        h_eldata = [filein.Get("h_mWsubjet_b1e"),
                    filein.Get("h_mWsubjet_b2e"),
                    filein.Get("h_mWsubjet_b3e"),
                    filein.Get("h_mWsubjet_b4e")]
        hp_eldata = [filein.Get("h_mWsubjet_b1pe"),
                     filein.Get("h_mWsubjet_b2pe"),
                     filein.Get("h_mWsubjet_b3pe"),
                     filein.Get("h_mWsubjet_b4pe")]
        h_mudata = [filein.Get("h_mWsubjet_b1m"),
                    filein.Get("h_mWsubjet_b2m"),
                    filein.Get("h_mWsubjet_b3m"),
                    filein.Get("h_mWsubjet_b4m")]
        hp_mudata = [filein.Get("h_mWsubjet_b1pm"),
                     filein.Get("h_mWsubjet_b2pm"),
                     filein.Get("h_mWsubjet_b3pm"),
                     filein.Get("h_mWsubjet_b4pm")]
        ''' 
        hdata_b1 = filein.Get("h_mWsubjet_b1")
        hdata_b2 = filein.Get("h_mWsubjet_b2")
        hdata_b3 = filein.Get("h_mWsubjet_b3")
        hdata_b4 = filein.Get("h_mWsubjet_b4")

        hmudata_b1 = filein.Get("h_mWsubjet_b1m")
        hmudata_b2 = filein.Get("h_mWsubjet_b2m")
        hmudata_b3 = filein.Get("h_mWsubjet_b3m")
        hmudata_b4 = filein.Get("h_mWsubjet_b4m")

        heldata_b1 = filein.Get("h_mWsubjet_b1e")
        heldata_b2 = filein.Get("h_mWsubjet_b2e")
        heldata_b3 = filein.Get("h_mWsubjet_b3e")
        heldata_b4 = filein.Get("h_mWsubjet_b4e")

        hdata_b1p = filein.Get("h_mWsubjet_b1p")
        hdata_b2p = filein.Get("h_mWsubjet_b2p")
        hdata_b3p = filein.Get("h_mWsubjet_b3p")
        hdata_b4p = filein.Get("h_mWsubjet_b4p")

        hmudata_b1p = filein.Get("h_mWsubjet_b1pm")
        hmudata_b2p = filein.Get("h_mWsubjet_b2pm")
        hmudata_b3p = filein.Get("h_mWsubjet_b3pm")
        hmudata_b4p = filein.Get("h_mWsubjet_b4pm")

        heldata_b1p = filein.Get("h_mWsubjet_b1pe")
        heldata_b2p = filein.Get("h_mWsubjet_b2pe")
        heldata_b3p = filein.Get("h_mWsubjet_b3pe")
        heldata_b4p = filein.Get("h_mWsubjet_b4pe")
        '''
    if dtypes[ifin] == 'ttjets' :
        httbar = filein.Get("h_mWsubjet_ttjets")
        httbar_MC  = filein.Get("h_mWsubjet_MC")

        h_ttjets = [filein.Get("h_mWsubjet_b1"),
                    filein.Get("h_mWsubjet_b2"),
                    filein.Get("h_mWsubjet_b3"),
                    filein.Get("h_mWsubjet_b4")]
        hp_ttjets = [filein.Get("h_mWsubjet_b1p"),
                     filein.Get("h_mWsubjet_b2p"),
                     filein.Get("h_mWsubjet_b3p"),
                     filein.Get("h_mWsubjet_b4p")]

# Fix this, get type 1 and type 2 pt distributions of W candidates

#hpts = filein.Get("h_ptWsubjet_Data_Type1")
#hpts2 = filein.Get("h_ptWsubjet_Data_Type2")

#hptsMC = filein.Get("h_ptWsubjet_MC_Type1")
#hpts2MC = filein.Get("h_ptWsubjet_MC_Type2")

# Find the tt scale factor
hMC = httbar_MC.Clone()
if options.allMC :
    hMC.Add(hwjets_MC)
    hMC.Add(hst_MC)

sf = 0.
#if options.Eldata : hdata =  FIX tHIS should scale individually el and mu data

if (hdata.Integral() > 0) and (hMC.Integral() > 0): 
    diff = hdata.Integral()-hMC.Integral()
    sf = diff/ (httbar.Integral())+1
lumi = 12300.
kfactorw = 1.21
scalefactor = 1.
scalefactortt = 1.

if sf < 0. : print "NEGATIVE tt SCALE FACTOR"

scalefactortt = sf
print "TT SCALE FACTOR APPLIED WAS : " + str(sf)


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
    filein2 = ROOT.TFile.Open('./output80xplotter/Wtag_highPtScaleFactor_preWTag_80x_'+str(datatype)+ '_'+ options.infile + '.root') 
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


binlabels = [ "200 < P_{T} < 300",
              "300 < P_{T} < 400",
              "400 < P_{T} < 500",
                   "P_{T} > 500 "]

# Rebin Values for Pt binned W candidate Mass histograms
rebinBybin = [ 15, 15, 30, 25 ]

for ipt in xrange(0, len(ptBs)-1 ) :
    pt = ptBs[ipt]
    binlabel = binlabels[ipt]
    # Get the W candidate mass histograms
    httbarT = h_ttjets[ipt].Clone()
    httbarTp = hp_ttjets[ipt].Clone()
    if options.allMC :
        hwjetsT = h_wjets[ipt].Clone()
        hwjetsTp = hp_wjets[ipt].Clone()
        hstT = h_st[ipt].Clone()
        hstTp = hp_st[ipt].Clone()
    hdataT = h_data[ipt].Clone()
    hmudataT = h_mudata[ipt].Clone()
    heldataT = h_eldata[ipt].Clone()
    hdataTp = hp_data[ipt].Clone()
    hmudataTp = hp_mudata[ipt].Clone()
    heldataTp = hp_eldata[ipt].Clone()
    # Save weighted sum errors
    httbarT.Sumw2()
    httbarTp.Sumw2()
    hdataT.Sumw2()
    hdataTp.Sumw2()
    hmudataT.Sumw2()
    hmudataTp.Sumw2()
    heldataT.Sumw2()
    heldataTp.Sumw2()
    if options.allMC :
        hwjetsT.Sumw2()
        hstT.Sumw2()
        hwjetsTp.Sumw2()
        hstTp.Sumw2()

    # Scale the histograms appropriately
    if httbarT.Integral() > 0 : 
        httbarT.Scale(lumi* scalefactortt * 831.76 / 182123200.) #hdataT.GetEntries()/ httbarT.Integral())
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt bin {0} empty".format(ibin)
        httbarT.Scale( 0.)

    if httbarTp.Integral() > 0 : 
        httbarTp.Scale(lumi* scalefactortt * 831.76 / 182123200.) #hdataT.GetEntries()/ httbarT.Integral())
    else :
        print "tt p bin {0} empty".format(ibin)
        httbarTp.Scale( 0.)

    if options.allMC :
        print "FIX THIS: add scaling for other MCs"

    # Rebin
    hdataT.Rebin(rebinBybin[ipt])
    hmudataT.Rebin(rebinBybin[ipt])
    heldataT.Rebin(rebinBybin[ipt])
    httbarT.Rebin(rebinBybin[ipt])
    hdataTp.Rebin(rebinBybin[ipt])
    hmudataTp.Rebin(rebinBybin[ipt])
    heldataTp.Rebin(rebinBybin[ipt])
    httbarTp.Rebin(rebinBybin[ipt])
    if options.allMC :
        hwjetsT.Rebin(rebinBybin[ipt])
        hstT.Rebin(rebinBybin[ipt])
        hwjetsTp.Rebin(rebinBybin[ipt])
        hstTp.Rebin(rebinBybin[ipt])

        

    httbarT.SetFillColor(ROOT.kGreen + 2)
    hwjetsT.SetFillColor(ROOT.kRed)
    hstT.SetFillColor(ROOT.kCyan )
    httbarTp.SetFillColor(ROOT.kGreen + 2)
    if options.allMC :
        hwjetsTp.SetFillColor(ROOT.kRed )
        hstTp.SetFillColor(ROOT.kCyan )

    hdataT.SetMarkerStyle(20)
    hdataTp.SetMarkerStyle(20)
    hmudataT.SetMarkerStyle(20)
    hmudataTp.SetMarkerStyle(20)
    heldataT.SetMarkerStyle(20)
    heldataTp.SetMarkerStyle(20)

    if options.pre :
        httbarT = httbarTp.Clone()
        if options.allMC :
            hwjetsT = hwjetsTp.Clone()
            hstT = hstTp.Clone()
        hdataT = hdataTp.Clone()
        hmudataT = hmudataTp.Clone()
        heldataT = heldataTp.Clone()

    mc = ROOT.THStack('WmaSS','; Subjet Soft Drop Mass ( GeV ) ;Number of Events') #Mass_{SD subjet_{0} }
    #mc.Add( hzjets )
    #mc.Add( hwjets )
    #mc.Add( hsingletop )
    if options.allMC :
        mc.Add( hwjetsT)
        mc.Add( hstT)
    mc.Add( httbarT)



    #fitting

    if (ipt >= 2) :
        minn = options.min2
        maxx = options.max2
        if ipt > 2 :   
            minn = options.min3
            maxx = options.max3
    else:
        minn = options.min0
        maxx = options.max0
        if ipt > 0 :
            minn = options.min1
            maxx = options.max1 

    fitter_data = ROOT.TF1("fitter_data", "gaus", minn , maxx )
    data_meanval = Datameans[ipt]
    data_sigmaval = Datasigmas[ipt] 
    fitter_mudata = ROOT.TF1("fitter_mudata", "gaus",  minn , maxx  )
    mudata_meanval = MuDatameans[ipt]
    mudata_sigmaval = MuDatasigmas[ipt] 
    fitter_eldata = ROOT.TF1("fitter_eldata", "gaus",  minn , maxx  )
    eldata_meanval = ElDatameans[ipt]
    eldata_sigmaval = ElDatasigmas[ipt] 


    if options.fixFit :
        fitter_data.FixParameter(1, data_meanval)
        fitter_data.FixParameter(2, data_sigmaval)
        fitter_mudata.FixParameter(1, mudata_meanval)
        fitter_mudata.FixParameter(2, mudata_sigmaval)
        fitter_eldata.FixParameter(1, eldata_meanval)
        fitter_eldata.FixParameter(2, eldata_sigmaval)
    #fitter_data.SetParLimits(1, data_mean_min , data_mean_max)
    #fitter_data.SetParLimits(2, data_sigma_min , data_sigma_max)
    
    #if options.pre :
    #    fitter_data = ROOT.TF1("fitter_data", "gaus", 65.0, 105.0, )
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

    if options.pre :
        Datameans[ipt] = mean_data
        Datasigmas[ipt] = width_data
        MuDatameans[ipt] = mmean_data
        MuDatasigmas[ipt] = mwidth_data
        ElDatameans[ipt] = Emean_data
        ElDatasigmas[ipt] = Ewidth_data

    mchist = httbarT.Clone()
    if options.allMC : 
        mchist.Add( hwjetsT )
        mchist.Add( hstT )


    fitter_mc = ROOT.TF1("fitter_mc", "gaus", minn , maxx )
    mc_meanval = MCmeans[ipt]
    mc_sigmaval = MCsigmas[ipt]


    if options.fixFit :
        fitter_mc.FixParameter(1, mc_meanval)
        fitter_mc.FixParameter(2, mc_sigmaval)


    #fitter_mc.SetParLimits(1, mc_mean_min , mc_mean_max)
    #fitter_mc.SetParLimits(2, mc_sigma_min , mc_sigma_max)
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
    if options.pre :
        MCmeans[ipt] = mean_mc
        MCsigmas[ipt] = width_mc


    meanrat = 1.0
    meanrat_uncert = meanrat
    jms = 1.0
    jms_uncert = jms
    
    binSizeData = hdataT.GetBinWidth(0)
    binSizeMC = mchist.GetBinWidth(0)

    mclow = 0. 
    mchigh = 0.

    datalow = 0.
    datahigh = 0.

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

    if options.pre :
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

    if mean_mc > 0. : # ??? working here 
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


    ROOT.gStyle.SetOptFit(1111)
    ROOT.gStyle.SetOptStat(0000000000)
    cmsTextFont   = 61  

    if not (options.Mudata or options.Eldata) :
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

        hdataT.Draw('e')
        mc.Draw("histsame")
        hdataT.Draw('esamex0')

        hdataT.Draw('e same')
        hdataT.Draw("axis same")
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
        max2 = mchist.GetMaximum() # mc.GetHistogram().GetMaximum()

        hdataT.SetMaximum( max (max1,max2) * 1.618 )

        hdataT.SetXTitle("Subjet Soft Drop Mass (GeV)")
        hdataT.SetYTitle("Events")
        hdata.BufferEmpty(1)
        hdataT.GetXaxis().SetTitleSize(0.047)
        hdataT.GetYaxis().SetTitleSize(0.047)
        hdataT.GetXaxis().SetLabelSize(0.04)
        hdataT.GetYaxis().SetLabelSize(0.04)

        leg.Draw()

        tlx = ROOT.TLatex()
        tlx.SetNDC()
        tlx.SetTextFont(42)
        tlx.SetTextSize(0.057)
        #tlx.DrawLatex(0.68, 0.957,  str(lumi) + " fb^{-1} (13TeV)")
        tlx.DrawLatex(0.67, 0.86, binlabel )
        #tlx.DrawLatex(0.70, 0.81, "#it{Preliminary}")


        tlx.SetTextSize(0.027)
        xInfo = 0.49
        yInfoTop = 0.475
        yInfo2 = yInfoTop-0.042
        yInfo3 = yInfo2-0.042
        yInfo4 = yInfo3-0.042
        yInfo5 = yInfo4-0.042
        yInfo6 = yInfo5-0.042
        yInfo7 = yInfo6-0.042
        yInfo8 = yInfo7-0.042
        yInfo9 = yInfo8-0.042
        #if not options.pre :
        #    tlx.DrawLatex(xInfo, yInfo4+0.13,"#bf{40 < m_{SD subjet 0} (GeV) < 120}")

        c.Update()
        c.Draw()
        sele = options.filestr
        if options.pre :
            sele = options.filestr + '_preWTag'
        c.Print('WsubjetSF/AllData/wMass_Bin'+ str(ipt) + '_' + sele + '.png', 'png' )
        c.Print('WsubjetSF/AllData/wMass_Bin'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
        c.Print('WsubjetSF/AllData/wMass_Bin'+ str(ipt) + '_' + sele + '.root', 'root' )

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
        leg.AddEntry( hwjetsT, 'W + jets', 'f')
        leg.AddEntry( hstT, 'Single Top', 'f')
        '''
        leg.AddEntry( hzjets, 'Z+Jets', 'f')

        '''
        max1 = hmudataT.GetMaximum()
        max2 = mchist.GetMaximum() # mc.GetHistogram().GetMaximum()

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
        cc.Print('WsubjetSF/Mudata/wMass_Bin'+ str(ipt) + '_' + sele + '.png', 'png' )
        cc.Print('WsubjetSF/Mudata/wMass_Bin'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
        cc.Print('WsubjetSF/Mudata/wMass_Bin'+ str(ipt) + '_' + sele + '.root', 'root' )

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
        max2 = mchist.GetMaximum() # mc.GetHistogram().GetMaximum()

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
        ccc.Print('WsubjetSF/ElData/wMass_Bin'+ str(ipt) + '_' + sele + '.png', 'png' )
        ccc.Print('WsubjetSF/ElData/wMass_Bin'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
        ccc.Print('WsubjetSF/ElData/wMass_Bin'+ str(ipt) + '_' + sele + '.root', 'root' )


    ee = ROOT.TCanvas('wid','wid')
    hwidth.Draw('e')

    hwidth.SetMarkerStyle(20)
    hwidth.SetMaximum(3.0)
    hwidth.SetMinimum(0.0)

    CMS_lumi.CMS_lumi(ee, iPeriod, iPos)

    ee.Update()
    ee.Draw()
    if not (options.Eldata and options.Mudata): # working here 
        ee.Print('WsubjetSF/AllData/JMR_W_' + options.filestr + '.png', 'png' )
        ee.Print('WsubjetSF/AllData/JMR_W_' + options.filestr + '.pdf', 'pdf' )
        ee.Print('WsubjetSF/AllData/JMR_W_' + options.filestr + '.root', 'root' )
    if  options.Eldata : # working here 
        ee.Print('WsubjetSF/ElData/JMR_W_' + options.filestr + '.png', 'png' )
        ee.Print('WsubjetSF/ElData/JMR_W_' + options.filestr + '.pdf', 'pdf' )
        ee.Print('WsubjetSF/ElData/JMR_W_' + options.filestr + '.root', 'root' )
    if options.Mudata : # working here 
        ee.Print('WsubjetSF/MuData/JMR_W_' + options.filestr + '.png', 'png' )
        ee.Print('WsubjetSF/MuData/JMR_W_' + options.filestr + '.pdf', 'pdf' )
        ee.Print('WsubjetSF/MuData/JMR_W_' + options.filestr + '.root', 'root' )

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
        ff.Print('WsubjetSF/AllData/Pt_type1and2_' + options.filestr + '.png', 'png' )
        ff.Print('WsubjetSF/AllData/Pt_type1and2_' + options.filestr + '.pdf', 'pdf' )
        ff.Print('WsubjetSF/AllData/Pt_type1and2_' + options.filestr + '.root', 'root' )

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
    if not (options.Eldata and options.Mudata): # working here 
        gg.Print('WsubjetSF/AllData/JMS_W_' + options.filestr + '.png', 'png' )
        gg.Print('WsubjetSF/AllData/JMS_W_' + options.filestr + '.pdf', 'pdf' )
        gg.Print('WsubjetSF/AllData/JMS_W_' + options.filestr + '.root', 'root' )
    if  options.Eldata : # working here 
        gg.Print('WsubjetSF/ElData/JMS_W_' + options.filestr + '.png', 'png' )
        gg.Print('WsubjetSF/ElData/JMS_W_' + options.filestr + '.pdf', 'pdf' )
        gg.Print('WsubjetSF/ElData/JMS_W_' + options.filestr + '.root', 'root' )
    if options.Mudata : # working here 
        gg.Print('WsubjetSF/MuData/JMS_W_' + options.filestr + '.png', 'png' )
        gg.Print('WsubjetSF/MuData/JMS_W_' + options.filestr + '.pdf', 'pdf' )
        gg.Print('WsubjetSF/MuData/JMS_W_' + options.filestr + '.root', 'root' )


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
    if not (options.Eldata and options.Mudata): # working here 
        d.Print('WsubjetSF/AllData/ScaleFactor_W_' + options.filestr + '.png', 'png' )
        d.Print('WsubjetSF/AllData/ScaleFactor_W_' + options.filestr + '.pdf', 'pdf' )
        d.Print('WsubjetSF/AllData/ScaleFactor_W_' + options.filestr + '.root', 'root' )
    if  options.Eldata : # working here 
        d.Print('WsubjetSF/ElData/ScaleFactor_W_' + options.filestr + '.png', 'png' )
        d.Print('WsubjetSF/ElData/ScaleFactor_W_' + options.filestr + '.pdf', 'pdf' )
        d.Print('WsubjetSF/ElData/ScaleFactor_W_' + options.filestr + '.root', 'root' )
    if options.Mudata : # working here 
        d.Print('WsubjetSF/MuData/ScaleFactor_W_' + options.filestr + '.png', 'png' )
        d.Print('WsubjetSF/MuData/ScaleFactor_W_' + options.filestr + '.pdf', 'pdf' )
        d.Print('WsubjetSF/MuData/ScaleFactor_W_' + options.filestr + '.root', 'root' )
fout.cd()
fout.Write()
fout.Close()
