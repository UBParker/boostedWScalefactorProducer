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

parser.add_option('--combineTrees', action='store_true',
              default=False,
              dest='combineTrees',
              help='Do you want to use combined ttrees???')

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

CMS_lumi.lumi_13TeV = "~12.3 fb^{-1}"
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



fout= ROOT.TFile('Wmass_meanrat_' + options.infile + '.root', "RECREATE")
if options.combineTrees : fout= ROOT.TFile('Wmass_meanrat_combinedTrees_' + options.infile + '.root', "RECREATE")
if options.pre :
    fout= ROOT.TFile('Wmass_meanrat_preWTag_' + options.infile + '.root', "RECREATE")
if options.pre and options.combineTrees :
    fout= ROOT.TFile('Wmass_meanrat_preWTag_combinedTrees_80x_' + str(options.infile) + '.root', "RECREATE")

ptBs =  array.array('d', [200., 300., 400., 500., 800.])
nptBs = len(ptBs) - 1


hpeak = ROOT.TH1F("hpeak", " ;p_{T} of SD subjet 0 (GeV); JMS ",  nptBs, ptBs)  ##frac{Mean Mass_{data}}{Mean Mass_{MC}}
hwidth = ROOT.TH1F("hwidth", " ;p_{T} of SD subjet 0 (GeV); JMR ", nptBs, ptBs) ##frac{#sigma_{data}}{#sigma_{MC}}



if options.pre :
    hNpassDataPre = ROOT.TH1F("hNpassDataPre", " ;;  ", nptBs, ptBs) 
    hNpassMCPre = ROOT.TH1F("hNpassMCPre", " ;;  ", nptBs, ptBs) 
    hmeanDataPre = ROOT.TH1F("hmeanDataPre", " ;;  ", nptBs, ptBs) 
    hmeanMCPre = ROOT.TH1F("hmeanMCPre", " ;;  ", nptBs, ptBs) 
    hsigmaDataPre = ROOT.TH1F("hsigmaDataPre", " ;;  ", nptBs, ptBs) 
    hsigmaMCPre = ROOT.TH1F("hsigmaMCPre", " ;;  ", nptBs, ptBs) 
else:
    hNpassDataPost = ROOT.TH1F("hNpassDataPost", " ;;  ", nptBs, ptBs) 
    hNpassMCPost = ROOT.TH1F("hNpassMCPost", " ;;  ", nptBs, ptBs) 
    hscale = ROOT.TH1F("hscale", " ; ;  ", nptBs, ptBs)
    hDataEff = ROOT.TH1F("hDataEff", " ; ; ", nptBs, ptBs)
    hMCEff = ROOT.TH1F("hMCEff", " ; ; ", nptBs, ptBs)


 
if options.combineTrees : 
    filein = ROOT.TFile.Open('./output80x/Wmass_pt_binned_CombinedTrees_80x_' + str(options.infile) + '.root') 
else : 
    filein = ROOT.TFile.Open('Wmass_pt_binned_' + options.infile + '.root')
lumi = 12.3 #2136.0

httbar = filein.Get("h_mWsubjet_ttjets")
ttbar_pt = filein.Get("h_ptWsubjet_ttjets")

httbar2 = filein.Get("h_mWjet_ttjets")
ttbar_pt2 = filein.Get("h_ptWjet_ttjets")

# Mass of SD subjet 0 of the AK8 jet in semi-leptonic Z' selection, binned in pt. 0-200 GeV, 200-400 GeV, 400-600 Gev, 600-Infinity GeV
httbar_b1 = filein.Get("h_mWsubjet_b1_ttjets")
httbar_b2 = filein.Get("h_mWsubjet_b2_ttjets")
httbar_b3 = filein.Get("h_mWsubjet_b3_ttjets")
httbar_b4 = filein.Get("h_mWsubjet_b4_ttjets")

httbar_b1p = filein.Get("h_mWsubjet_b1_ttjetsp")
httbar_b2p = filein.Get("h_mWsubjet_b2_ttjetsp")
httbar_b3p = filein.Get("h_mWsubjet_b3_ttjetsp")
httbar_b4p = filein.Get("h_mWsubjet_b4_ttjetsp")

singlemu_m = filein.Get("h_mWsubjet_MuData")
singlemu_pt = filein.Get("h_ptWsubjet_MuData")

singlemu_m_b1 = filein.Get("h_mWsubjet_b1_MuData")
singlemu_m_b2 = filein.Get("h_mWsubjet_b2_MuData")
singlemu_m_b3 = filein.Get("h_mWsubjet_b3_MuData")
singlemu_m_b4 = filein.Get("h_mWsubjet_b4_MuData")

singlemu_mp = filein.Get("h_mWsubjet_MuDatap")
singlemu_ptp = filein.Get("h_ptWsubjet_MuDatap")

singlemu_m_b1p = filein.Get("h_mWsubjet_b1_MuDatap")
singlemu_m_b2p = filein.Get("h_mWsubjet_b2_MuDatap")
singlemu_m_b3p = filein.Get("h_mWsubjet_b3_MuDatap")
singlemu_m_b4p = filein.Get("h_mWsubjet_b4_MuDatap")

singleel_m = filein.Get("h_mWsubjet_EleData")
singleel_pt = filein.Get("h_ptWsubjet_EleData")

singleel_m_b1 = filein.Get("h_mWsubjet_b1_EleData")
singleel_m_b2 = filein.Get("h_mWsubjet_b2_EleData")
singleel_m_b3 = filein.Get("h_mWsubjet_b3_EleData")
singleel_m_b4 = filein.Get("h_mWsubjet_b4_EleData")

singleel_mp = filein.Get("h_mWsubjet_EleDatap")
singleel_ptp = filein.Get("h_ptWsubjet_EleDatap")

singleel_m_b1p = filein.Get("h_mWsubjet_b1_EleDatap")
singleel_m_b2p = filein.Get("h_mWsubjet_b2_EleDatap")
singleel_m_b3p = filein.Get("h_mWsubjet_b3_EleDatap")
singleel_m_b4p = filein.Get("h_mWsubjet_b4_EleDatap")

hdata = filein.Get("h_mWsubjet_Data")
muel_pt = filein.Get("h_ptWsubjet_Data")

hdata_b1 = filein.Get("h_mWsubjet_b1_Data")
hdata_b2 = filein.Get("h_mWsubjet_b2_Data")
hdata_b3 = filein.Get("h_mWsubjet_b3_Data")
hdata_b4 = filein.Get("h_mWsubjet_b4_Data")

hdatap = filein.Get("h_mWsubjet_Datap")
muel_ptp = filein.Get("h_ptWsubjet_Datap")

hdata_b1p = filein.Get("h_mWsubjet_b1_Datap")
hdata_b2p = filein.Get("h_mWsubjet_b2_Datap")
hdata_b3p = filein.Get("h_mWsubjet_b3_Datap")
hdata_b4p = filein.Get("h_mWsubjet_b4_Datap")

hpts = filein.Get("h_ptWsubjet_Data_Type1")
hpts2 = filein.Get("h_ptWsubjet_Data_Type2")

hptsMC = filein.Get("h_ptWsubjet_MC_Type1")
hpts2MC = filein.Get("h_ptWsubjet_MC_Type2")

nMCpre = array.array('d', [0., 0., 0., 0.])
nDatapre = array.array('d', [0., 0., 0., 0.])
nMCupre = array.array('d', [0., 0., 0., 0.])
nDataupre = array.array('d', [0., 0., 0., 0.])


MCmeans = array.array('d', [0., 0., 0., 0.])
MCsigmas = array.array('d', [0., 0., 0., 0.])
Datameans = array.array('d', [0., 0., 0., 0.])
Datasigmas = array.array('d', [0., 0., 0., 0.])

nMCpost = array.array('d', [0., 0., 0., 0.])
nDatapost = array.array('d', [0., 0., 0., 0.])
nMCupost = array.array('d', [0., 0., 0., 0.])
nDataupost = array.array('d', [0., 0., 0., 0.])

if not options.pre :
    if options.combineTrees : filein2 = ROOT.TFile.Open('./Wmass_meanrat_preWTag_combinedTrees_80x_' + options.infile + '.root') 
    else : filein2 = ROOT.TFile.Open('Wmass_meanrat_preWTag_' + options.infile + '.root') 
    h_NpassDataPre = filein2.Get("hNpassDataPre")
    h_NpassMCPre = filein2.Get("hNpassMCPre")
 
    h_meanDataPre = filein2.Get("hmeanDataPre")
    h_meanMCPre = filein2.Get("hmeanMCPre")
    h_sigmaDataPre = filein2.Get("hsigmaDataPre")
    h_sigmaMCPre = filein2.Get("hsigmaMCPre")


    for ibin in xrange(0,h_NpassMCPre.GetNbinsX()) :
        nMCpre[ibin] = h_NpassMCPre.GetBinContent(ibin+1)
        nDatapre[ibin] = h_NpassDataPre.GetBinContent(ibin+1)
        print "For bin " + str(ibin)+" : preselection in data and mc are" + str(nDatapre[ibin]) + '  and ' + str(nMCpre[ibin])
    
    print "Reading means and widths of --pre Gaussian Fits for use in constraining the post W tag fits!"
    for ibin in xrange(0,h_sigmaMCPre.GetNbinsX() ) :
        MCmeans[ibin] = h_meanMCPre.GetBinContent(ibin+1)
        MCsigmas[ibin] = h_sigmaMCPre.GetBinContent(ibin+1)
        Datameans[ibin] = h_meanDataPre.GetBinContent(ibin+1)
        Datasigmas[ibin] = h_sigmaDataPre.GetBinContent(ibin+1)        


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


for ipt in xrange(0, len(ptBs)-1 ) :
#for ipt, pt in enumerate(ptBs) :
    #print "pt variable is : " + str(pt)
    #print "ipt variable is : " + str(ipt)
    pt = ptBs[ipt]
    if (ipt == 0) :
        binlabel = "200 < P_{T} < 300"
        httbarT = httbar_b1.Clone()
        hdataT = hdata_b1.Clone()
        httbarTp = httbar_b1p.Clone()
        hdataTp = hdata_b1p.Clone()
        hdataT.Rebin(5)
        httbarT.Rebin(5)
        hdataTp.Rebin(5)
        httbarTp.Rebin(5)
    if (ipt == 1) :
        binlabel = "300 < P_{T} < 400"
        httbarT = httbar_b2.Clone()
        hdataT = hdata_b2.Clone()
        httbarTp = httbar_b2p.Clone()
        hdataTp = hdata_b2p.Clone()
        hdataT.Rebin(5)
        httbarT.Rebin(5)
        hdataTp.Rebin(5)
        httbarTp.Rebin(5)
    if (ipt == 2) :
        binlabel = "400 < P_{T} < 500"
        httbarT = httbar_b3.Clone()
        hdataT = hdata_b3.Clone()
        httbarTp = httbar_b3p.Clone()
        hdataTp = hdata_b3p.Clone()
        hdataT.Rebin(10)
        httbarT.Rebin(10)
        hdataTp.Rebin(10)
        httbarTp.Rebin(10)
    if (ipt == 3) :
        binlabel = "P_{T} > 500 "
        httbarT = httbar_b4.Clone()
        hdataT = hdata_b4.Clone()
        httbarTp = httbar_b4p.Clone()
        hdataTp = hdata_b4p.Clone()
        hdataT.Rebin(10)
        httbarT.Rebin(10)
        hdataTp.Rebin(10)
        httbarTp.Rebin(10)



    if httbarT.Integral() > 0 : 
        httbarT.Scale( hdataT.GetEntries()/ httbarT.Integral())
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt empty"
        httbarT.Scale( 0.)
    httbarT.SetFillColor(ROOT.kGreen + 2)

    if httbarTp.Integral() > 0 : 
        httbarTp.Scale( hdataTp.GetEntries()/ httbarTp.Integral())
        # t tbar - https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO used top mass as 172.5, uncertainties on twiki
    else :
        print "tt empty"
        httbarTp.Scale( 0.)





    httbarTp.SetFillColor(ROOT.kGreen + 2)

    hdataT.SetMarkerStyle(20)
    hdataTp.SetMarkerStyle(20)
    #hdataT_b1p.SetTitle( title )

    if options.pre :
        httbarT = httbarTp.Clone()
        hdataT = hdataTp.Clone()

    mc = ROOT.THStack('WmaSS','; Subjet Soft Drop Mass ( GeV ) ;Number of Events') #Mass_{SD subjet_{0} }
    #mc.Add( hzjets )
    #mc.Add( hwjets )
    #mc.Add( hsingletop )
    mc.Add( httbarT)

    # IMPORTANT: must match data_mean and data_sigma as well as corresponding MC values in other plotting script Plot_Wsubjet.py

    #fitting
    #fitter_data = ROOT.TF1("fitter_data", "gaus",  50. , 150. ) #65.0, 105.0, )   
    if (ipt >= 2) :
        fitter_data = ROOT.TF1("fitter_data", "gaus",options.min2 , options.max2 )
        data_meanval = Datameans[2]
        data_sigmaval = Datasigmas[2] 
        if ipt > 2 :
            fitter_data = ROOT.TF1("fitter_data", "gaus",options.min3 , options.max3 )
            data_meanval = Datameans[3]
            data_sigmaval = Datasigmas[3] 
    else:
        fitter_data = ROOT.TF1("fitter_data", "gaus", options.min0 , options.max0 )
        data_meanval = Datameans[0]
        data_sigmaval = Datasigmas[0] 
        if ipt > 0 :
            fitter_data = ROOT.TF1("fitter_data", "gaus", options.min1 , options.max1 )
            data_meanval = Datameans[1]
            data_sigmaval = Datasigmas[1] 

    if options.fixFit :
        fitter_data.FixParameter(1, data_meanval)
        fitter_data.FixParameter(2, data_sigmaval)
    #fitter_data.SetParLimits(1, data_mean_min , data_mean_max)
    #fitter_data.SetParLimits(2, data_sigma_min , data_sigma_max)
    
    #if options.pre :
    #    fitter_data = ROOT.TF1("fitter_data", "gaus", 65.0, 105.0, )
    fitter_data.SetLineColor(1)
    fitter_data.SetLineWidth(2)
    fitter_data.SetLineStyle(2)
    if options.fixFit :
        hdataT.Fit(fitter_data,'B' )
    else :
        hdataT.Fit(fitter_data,'R' )

    amp_data    = fitter_data.GetParameter(0);
    eamp_data   = fitter_data.GetParError(0); 
    mean_data   = fitter_data.GetParameter(1);
    emean_data  = fitter_data.GetParError(1); 
    width_data  = fitter_data.GetParameter(2);
    ewidth_data = fitter_data.GetParError(2); 

    print 'amp_data    '+str(amp_data    ) 
    print 'eamp_data   '+str(eamp_data   ) 
    print 'mean_data   '+str(mean_data   ) 
    print 'emean_data  '+str(emean_data  ) 
    print 'width_data  '+str(width_data  ) 
    print 'ewidth_data '+str(ewidth_data ) 

    if options.pre :
        Datameans[ipt] = mean_data
        Datasigmas[ipt] = width_data

    mchist = httbarT.Clone()
     
    #mchist.Add( hsingletop )
    #mchist.Add( httbarT )


    if (ipt >= 2) :
        fitter_mc = ROOT.TF1("fitter_mc", "gaus", options.min2 , options.max2 )
        mc_meanval = MCmeans[2]
        mc_sigmaval = MCsigmas[2]
        if ipt > 2 :   
            fitter_mc = ROOT.TF1("fitter_mc", "gaus", options.min3 , options.max3 )
            mc_meanval = MCmeans[3]
            mc_sigmaval = MCsigmas[3]
    else:
        fitter_mc = ROOT.TF1("fitter_mc", "gaus", options.min0 , options.max0 )
        mc_meanval = MCmeans[0]
        mc_sigmaval = MCsigmas[0]
        if ipt > 0 :
            fitter_mc = ROOT.TF1("fitter_mc", "gaus", options.min1 , options.max1 )
            mc_meanval = MCmeans[1]
            mc_sigmaval = MCsigmas[1]

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
          
    print 'amp_mc    '+str(amp_mc    ) 
    print 'eamp_mc   '+str(eamp_mc   ) 
    print 'mean_mc   '+str(mean_mc   ) 
    print 'emean_mc  '+str(emean_mc  ) 
    print 'width_mc  '+str(width_mc  ) 
    print 'ewidth_mc '+str(ewidth_mc ) 

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

    mcAxis = mchist.GetXaxis()
    dataAxis = hdataT.GetXaxis()

    bminmc = mcAxis.FindBin(mclow)
    bmaxmc = mcAxis.FindBin(mchigh)

    bmindata = hdataT.FindBin(datalow)
    bmaxdata = hdataT.FindBin(datahigh)

    if options.pre :
        nMCpre[ipt] = mchist.Integral(bminmc , bmaxmc  ) #/ binSizeMC
        nDatapre[ipt] = hdataT.Integral(bmindata, bmaxdata  ) #/ binSizeData
        nMCupre[ipt] =  math.sqrt( nMCpre[ipt] )   #mchist.IntegralError(bminmc , bmaxmc  ) / binSizeMC
        nDataupre[ipt] = math.sqrt(nDatapre[ipt] ) #hdataT.IntegralError(bmindata, bmaxdata  ) / binSizeData
    else :
        nMCpost[ipt] = mchist.Integral(bminmc , bmaxmc  ) #/ binSizeMC
        nDatapost[ipt] = hdataT.Integral(bmindata, bmaxdata  ) #/ binSizeData
        nMCupost[ipt] =  math.sqrt( nMCpost[ipt] )  #mchist.IntegralError(bminmc , bmaxmc  ) / binSizeMC
        nDataupost[ipt] = math.sqrt(nDatapost[ipt] )#hdataT.IntegralError(bmindata, bmaxdata  ) / binSizeData

    if mean_mc > 0. :
        meanrat = mean_data / mean_mc
        meanrat_uncert = meanrat * math.sqrt( (emean_data/mean_data)**2 + (emean_mc/mean_mc)**2 )
    if width_mc > 0. :
        jms = width_data / width_mc
        jms_uncert = jms * math.sqrt( (ewidth_data/width_data)**2 + (ewidth_mc/width_mc)**2 )

    print 'data_over_mc peak :  '+str(meanrat)
    print '...........................................................'

    ibin = hpeak.GetXaxis().FindBin(pt)
    hpeak.SetBinContent(ibin, meanrat ) 
    hwidth.SetBinContent(ibin, jms )
    hpeak.SetBinError(ibin, meanrat_uncert)   
    hwidth.SetBinError(ibin, jms_uncert)
    if options.pre :
        ibin = hNpassDataPre.GetXaxis().FindBin(pt)
        hNpassDataPre.SetBinContent(ibin, nDatapre[ipt])
        hNpassMCPre.SetBinContent(ibin, nMCpre[ipt])
        hNpassDataPre.SetBinError(ibin, nDataupre[ipt])
        hNpassMCPre.SetBinError(ibin, nMCupre[ipt])
        hmeanDataPre.SetBinContent(ibin, Datameans[ipt]) 
        hmeanMCPre.SetBinContent(ibin, MCmeans[ipt] )
        hsigmaDataPre.SetBinContent(ibin, Datasigmas[ipt])
        hsigmaMCPre.SetBinContent(ibin,  MCsigmas[ipt] )
    else :
        ibin = hNpassDataPost.GetXaxis().FindBin(pt)
        hNpassDataPost.SetBinContent(ibin, nDatapost[ipt])
        hNpassMCPost.SetBinContent(ibin, nMCpost[ipt])
        hNpassDataPost.SetBinError(ibin, nDataupost[ipt])
        hNpassMCPost.SetBinError(ibin, nMCupost[ipt])


    #  DRAWING TIME!!!!!!!!!!!!


    ROOT.gStyle.SetOptFit(1111)
    ROOT.gStyle.SetOptStat(0000000000)
    cmsTextFont   = 61  

    #c = ROOT.TCanvas('WmaSS','WmaSS')
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
    '''
    leg.AddEntry( hwjets, 'W+Jets', 'f')
    leg.AddEntry( hzjets, 'Z+Jets', 'f')
    leg.AddEntry( hsingletop, 'Single Top Quark', 'f')

    '''
    max1 = hdataT.GetMaximum()
    max2 = mchist.GetMaximum() # mc.GetHistogram().GetMaximum()

    hdataT.SetMaximum( max (max1,max2) * 1.2 )

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
    c.Print('WsubjetSF/wMass_Bin'+ str(ipt) + '_' + sele + '.png', 'png' )
    c.Print('WsubjetSF/wMass_Bin'+ str(ipt) + '_' + sele + '.pdf', 'pdf' )
    c.Print('WsubjetSF/wMass_Bin'+ str(ipt) + '_' + sele + '.root', 'root' )


    ee = ROOT.TCanvas('wid','wid')
    hwidth.Draw('e')

    hwidth.SetMarkerStyle(20)
    #hwidth.GetYaxis().SetRange(0.8,1.0)
    hwidth.SetMaximum(3.0)
    hwidth.SetMinimum(0.0)

    CMS_lumi.CMS_lumi(ee, iPeriod, iPos)
    tlx = ROOT.TLatex()
    tlx.SetNDC()
    tlx.SetTextFont(42)
    tlx.SetTextSize(0.057)
    #tlx.DrawLatex(0.131, 0.91, "CMS Preliminary #sqrt{s}=13 TeV, " + str(lumi/1000.0) + " fb^{-1}")
    # tlx.DrawLatex(0.77, 0.86, "#bf{CMS}")
    # tlx.DrawLatex(0.72, 0.83, "#it{very preliminary}")
    tlx.SetTextSize(0.029)
    xInfo = 0.51
    yInfoTop = 0.475
    yInfo2 = yInfoTop-0.042
    yInfo3 = yInfo2-0.042
    yInfo4 = yInfo3-0.042
    yInfo5 = yInfo4-0.042
    yInfo6 = yInfo5-0.042
    yInfo7 = yInfo6-0.042
    yInfo8 = yInfo7-0.042

    #tlx.DrawLatex(xInfo, yInfo4+0.4,"#bf{65 < m_{SD subjet 0} (GeV) < 130}")

    #tlx.DrawLatex(xInfo, yInfo2, "#bf{anti-k_{T} R= 0.8, p_{T} > 400 (GeV)}")
    #tlx.DrawLatex(xInfo, yInfo3, "#bf{110 < m_{SD AK8 Jet}(GeV) < 250 , #tau_3 / #tau_2 < 0.6}")
    #tlx.DrawLatex(xInfo, yInfo3, "#bf{55 < m_{SD Subjet 0}(GeV) < 105 , #tau_2 / #tau_1 < 0.6}")
    #tlx.DrawLatex(xInfo, yInfo4,"#bf{m_{SD subjet 0} > 50, p_{T of SD subjet 0} > 200 (GeV)}")
    #tlx.DrawLatex(xInfo, yInfo5, "#bf{AK4 CSVv2 B disc. > 0.7}") 
    #tlx.DrawLatex(xInfo, yInfo6, "#bf{2D cut}") 
    #tlx.DrawLatex(xInfo, yInfo7, "#bf{e :p_{T} > 110 and p_{T of MET} > 120 (GeV)}") 
    #tlx.DrawLatex(xInfo, yInfo8, "#bf{#mu :p_{T} > 55 and (p_{T} + P_{T of MET} ) > 150 (GeV)}")

    ee.Update()
    ee.Draw()
    ee.Print('WsubjetSF/JMR_Wsubjet_AllBins' + '_' + options.filestr + '.png', 'png' )
    ee.Print('WsubjetSF/JMR_Wsubjet_AllBins' + '_' + options.filestr + '.pdf', 'pdf' )

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
    hpts2.SetMaximum(7000.)
    hpts2.SetMinimum(0.0001)
    hpts.SetMaximum(7000.)
    hpts.SetMinimum(0.0001)
    hpts2MC.SetMaximum(7000.)
    hpts2MC.SetMinimum(0.0001)
    hptsMC.SetMaximum(7000.)
    hptsMC.SetMinimum(0.0001)
    #hpts.SetMarkerStyle(20)
    #hpts.SetMaximum(3)
    #hpts.SetMinimum(0)

    CMS_lumi.CMS_lumi(ff, iPeriod, iPos)
    tlx = ROOT.TLatex()
    tlx.SetNDC()
    tlx.SetTextFont(42)
    tlx.SetTextSize(0.057)
    #tlx.DrawLatex(0.131, 0.91, "CMS Preliminary #sqrt{s}=13 TeV, " + str(lumi/1000.0) + " fb^{-1}")
    # tlx.DrawLatex(0.77, 0.86, "#bf{CMS}")
    # tlx.DrawLatex(0.72, 0.83, "#it{very preliminary}")
    tlx.SetTextSize(0.029)
    xInfo = 0.75
    yInfoTop = 0.475
    yInfo2 = yInfoTop-0.042
    yInfo3 = yInfo2-0.042
    yInfo4 = yInfo3-0.042
    yInfo5 = yInfo4-0.042
    yInfo6 = yInfo5-0.042
    yInfo7 = yInfo6-0.042
    yInfo8 = yInfo7-0.042
    
    legy = ROOT.TLegend( 0.68, 0.68, 0.799, 0.875)
    legy.SetFillColor(0)
    legy.SetBorderSize(0)

    legy.AddEntry( hpts, 'Data: Type 1', 'l')
    legy.AddEntry( hpts2, 'Data: Type 2', 'l')
    legy.AddEntry( hptsMC, 'MC: Type 1', 'l')
    legy.AddEntry( hpts2MC, 'MC: Type 2', 'l')
    legy.Draw()
#    tlx.DrawLatex(xInfo, yInfo4+0.4,"#bf{65 < m_{SD subjet 0} (GeV) < 130}")

    #tlx.DrawLatex(xInfo, yInfo2, "#bf{Type 1 : 1 anti-k_{T} R= 0.8 Jet, p_{T} > 400 (GeV)}")
    #tlx.DrawLatex(xInfo, yInfo3, "#bf{Type 2 : 2 anti-k_{T} R= 0.8 Jets, p_{T} > 200 (GeV)}")
    #tlx.DrawLatex(xInfo, yInfo3, "#bf{55 < m_{SD Subjet 0}(GeV) < 105 , #tau_2 / #tau_1 < 0.6}")
#    tlx.DrawLatex(xInfo, yInfo3, "#bf{110 < m_{SD AK8 Jet}(GeV) < 250 , #tau_3 / #tau_2 < 0.6}")
#    tlx.DrawLatex(xInfo, yInfo4,"#bf{m_{SD subjet 0} > 50, p_{T of SD subjet 0} > 200 (GeV)}")
#    tlx.DrawLatex(xInfo, yInfo5, "#bf{AK4 CSVv2 B disc. > 0.7}") 
#    tlx.DrawLatex(xInfo, yInfo6, "#bf{2D cut}") 
#    tlx.DrawLatex(xInfo, yInfo7, "#bf{e :p_{T} > 110 and p_{T of MET} > 120 (GeV)}") 
#    tlx.DrawLatex(xInfo, yInfo8, "#bf{#mu :p_{T} > 55 and (p_{T} + P_{T of MET} ) > 150 (GeV)}")

    ff.Update()
    ff.Draw()
    ff.Print('WsubjetSF/Pt_type1and2_' + options.filestr + '.png', 'png' )
    ff.Print('WsubjetSF/Pt_type1and2_' + options.filestr + '.pdf', 'pdf' )
    ff.Print('WsubjetSF/Pt_type1and2_' + options.filestr + '.root', 'root' )

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
    #tlx.DrawLatex(0.131, 0.91, "CMS Preliminary #sqrt{s}=13 TeV, " + str(lumi/1000.0) + " fb^{-1}")
    # tlx.DrawLatex(0.77, 0.86, "#bf{CMS}")
    # tlx.DrawLatex(0.72, 0.83, "#it{very preliminary}")
    tlx.SetTextSize(0.029)
    xInfo = 0.51
    yInfoTop = 0.475
    yInfo2 = yInfoTop-0.042
    yInfo3 = yInfo2-0.042
    yInfo4 = yInfo3-0.042
    yInfo5 = yInfo4-0.042
    yInfo6 = yInfo5-0.042
    yInfo7 = yInfo6-0.042
    yInfo8 = yInfo7-0.042

    #tlx.DrawLatex(xInfo, yInfo4+0.4,"#bf{65 < m_{SD subjet 0} (GeV) < 130}")
    #tlx.DrawLatex(xInfo, yInfo3, "#bf{55 < m_{SD Subjet 0}(GeV) < 105 , #tau_2 / #tau_1 < 0.6}")
    #tlx.DrawLatex(xInfo, yInfo2, "#bf{anti-k_{T} R= 0.8, p_{T} > 400 (GeV)}")
    #tlx.DrawLatex(xInfo, yInfo3, "#bf{110 < m_{SD AK8 Jet}(GeV) < 250 , #tau_3 / #tau_2 < 0.6}")
    #tlx.DrawLatex(xInfo, yInfo4,"#bf{m_{SD subjet 0} > 50, p_{T of SD subjet 0} > 200 (GeV)}")
    #tlx.DrawLatex(xInfo, yInfo5, "#bf{AK4 CSVv2 B disc. > 0.7}") 
    #tlx.DrawLatex(xInfo, yInfo6, "#bf{2D cut}") 
    #tlx.DrawLatex(xInfo, yInfo7, "#bf{e :p_{T} > 110 and p_{T of MET} > 120 (GeV)}") 
    #tlx.DrawLatex(xInfo, yInfo8, "#bf{#mu :p_{T} > 55 and (p_{T} + P_{T of MET} ) > 150 (GeV)}")

    gg.Update()
    gg.Draw()
    gg.Print('WsubjetSF/JMS_Wsubjet_AllBins' + '_' + options.filestr + '.png', 'png' )
    gg.Print('WsubjetSF/JMS_Wsubjet_AllBins' + '_' + options.filestr + '.pdf', 'pdf' )
    gg.Print('WsubjetSF/JMS_Wsubjet_AllBins' + '_' + options.filestr + '.root', 'root' )



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
        pt = ptBs[ipt]
        ptToFill = float(pt)
        if pt > 800. :
            ptToFill = 799.
        if (nDatapre[ipt] > 0. and nMCpre[ipt] > 0. and pt >= 301.) :
            SF =  ( float(nDatapost[ipt]) / float(nDatapre[ipt]) ) / ( float(nMCpost[ipt]) / float(nMCpre[ipt]) )
            SF_sd = SF * math.sqrt(   (- float(nDatapost[ipt]) + float(nDatapre[ipt]) ) / ( float(nDatapost[ipt]) * float(nDatapre[ipt]) )  + (-float(nMCpost[ipt]) + float(nMCpre[ipt])) / (float(nMCpost[ipt]) * float(nMCpre[ipt]))  )
            print "............................................"
            print "             SCALE FACTOR                   "
            print "............................................"
            print "pt Bin lower bound in GeV :  " + str(pt)
            print "Preliminary W tagging SF from subjet w : " + str(SF)
            print "Data efficiency for this  bin" + str(float(nDatapost[ipt]) / float(nDatapre[ipt]))
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
    #tlx.DrawLatex(0.131, 0.93, "CMS Preliminary #sqrt{s}=13 TeV, " + str(lumi) + " fb^{-1}")
    #tlx.DrawLatex(0.131, 0.95,  str(lumi) + " fb^{-1} (13TeV)")
    #tlx.DrawLatex(0.77, 0.86, "#bf{CMS}")
    #tlx.DrawLatex(0.72, 0.83, "#it{Preliminary}")
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

    #tlx.DrawLatex(xInfo, yInfo4+0.4,"#bf{65 < m_{SD subjet 0} (GeV) < 130}")

    #tlx.DrawLatex(xInfo, yInfo2, "#bf{anti-k_{T} R= 0.8, p_{T} > 400 (GeV)}")
    #tlx.DrawLatex(xInfo, yInfo3, "#bf{55 < m_{SD Subjet 0}(GeV) < 105 , #tau_2 / #tau_1 < 0.6}")
    #tlx.DrawLatex(xInfo, yInfo4,"#bf{m_{SD subjet 0} > 50, p_{T of SD subjet 0} > 200 (GeV)}")
    #tlx.DrawLatex(xInfo, yInfo5, "#bf{AK4 CSVv2 B disc. > 0.7}") 
    #tlx.DrawLatex(xInfo, yInfo6, "#bf{2D cut}") 
    #tlx.DrawLatex(xInfo, yInfo7, "#bf{e :p_{T} > 110 and p_{T of MET} > 120 (GeV)}") 
    #tlx.DrawLatex(xInfo, yInfo8, "#bf{#mu :p_{T} > 55 and (p_{T} + P_{T of MET} ) > 150 (GeV)}")
    d.Update()
    d.Draw()
    d.Print('WsubjetSF/ScaleFactor_Wsubjet_AllBins_' + options.filestr + '.png', 'png' )
    d.Print('WsubjetSF/ScaleFactor_Wsubjet_AllBins_' + options.filestr + '.pdf', 'pdf' )
    d.Print('WsubjetSF/ScaleFactor_Wsubjet_AllBins_' + options.filestr + '.root', 'root' )


fout.cd()
fout.Write()
fout.Close()
