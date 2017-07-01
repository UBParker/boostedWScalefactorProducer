#/Usr50/bin/env python
from optparse import OptionParser
import ROOT
import sys
import os
import time
import math
import CMS_lumi, tdrstyle
from ROOT import *

parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('-c', '--channel',action="store",type="string",dest="channel",default="em")
parser.add_option('--HP', action="store", type="float",dest="tau2tau1cutHP",default=0.35)
parser.add_option('--LP', action="store", type="float",dest="tau2tau1cutLP",default=0.75)
parser.add_option('--sample', action="store",type="string",dest="sample",default="powheg")
parser.add_option('--fitTT', action='store_true', dest='fitTT', default=False, help='Only do ttbar fits')
parser.add_option('--fitMC', action='store_true', dest='fitMC', default=False, help='Only do MC fits')
parser.add_option('--doBinned',dest="doBinnedFit", default=False, action="store_true", help="Do binned fit")
parser.add_option('--76X',dest="use76X", default=False, action="store_true", help="Use 76X samples")
parser.add_option('--useDDT',dest="useDDT", default=False, action="store_true", help="Use DDT tagger")
parser.add_option('--useN2DDT',dest="useN2DDT", default=False, action="store_true", help="Use N_2^DDT tagger")
parser.add_option('--usePuppiSD',dest="usePuppiSD", default=True, action="store_true", help="Use PUPPI+softdrop")
parser.add_option('--salsetup',dest="salsetup", default=False, action="store_true", help="Sal's setup")
parser.add_option('--binmin',dest="ptbinmin", default=300, type=int,help="Minimum subjet 0 pt")
parser.add_option('--binmax',dest="ptbinmax", default=500, type=int,help="Maximum subjet 0 pt")
parser.add_option('--v5',dest="v5", default=True, action="store_true", help="Use latest b2g ttrees ?")
parser.add_option('--noQCD',dest="noQCD", default=False, action="store_true", help=" Don't use QCD")
parser.add_option('--noST',dest="noST", default=False, action="store_true", help="Don't use ST")

(options, args) = parser.parse_args()

if options.ptbinmax < 0. :
    options.ptbinmax = float('inf')

#Added these 2 lines - Michael
# For running on lpc
if not options.salsetup: 
    ROOT.gSystem.Load("/cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/roofit/5.34.22-cms3/lib/libRooFitCore.so")
    ROOT.gSystem.Load("/cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/roofit/5.34.22-cms3/lib/libRooFit.so")    
# For running on local machine
#ROOT.gSystem.Load("/opt/local/libexec/root6/lib/root/libRooFitCore.so")
#ROOT.gSystem.Load("/opt/local/libexec/root6/lib/root/libRooFit.so")

ROOT.gSystem.Load(".//PlotStyle/Util_cxx.so")
ROOT.gSystem.Load(".//PlotStyle/PlotUtils_cxx.so")
ROOT.gSystem.Load(".//PDFs/PdfDiagonalizer_cc.so")
ROOT.gSystem.Load(".//PDFs/HWWLVJRooPdfs_cxx.so")
ROOT.gSystem.Load(".//PDFs/MakePdf_cxx.so")
ROOT.gSystem.Load(".//BiasStudy/BiasUtils_cxx.so")
ROOT.gSystem.Load(".//FitUtils/FitUtils_cxx.so")

tdrstyle.setTDRStyle()
CMS_lumi.lumi_13TeV = "35.8 fb^{-1}"
if options.use76X: CMS_lumi.lumi_13TeV = "35.8 fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)
iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12
iPeriod = 4

gInterpreter.GenerateDictionary("std::map<std::string,std::string>", "map;string;string")
gStyle.SetOptTitle(0)
RooMsgService.instance().setGlobalKillBelow(RooFit.FATAL)

if options.noX: gROOT.SetBatch(True)


def getLegend():
  legend = TLegend(0.6010112,0.7183362,0.8202143,0.919833)
  legend.SetTextSize(0.032)
  legend.SetLineColor(0)
  legend.SetShadowColor(0)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  legend.SetMargin(0.35)
  return legend

def getPavetext():
#  addInfo = TPaveText(0.18,0.3,0.25,0.4,"NDC")
  addInfo = TPaveText(0.18,0.74,0.25,0.84,"NDC")
  addInfo.SetFillColor(0)
  addInfo.SetLineColor(0)
  addInfo.SetFillStyle(0)
  addInfo.SetBorderSize(0)
  addInfo.SetTextFont(42)
  addInfo.SetTextSize(0.030)
  addInfo.SetTextAlign(12)
  return addInfo
    
def drawFrameGetChi2(self, variable,fitResult,dataset,pdfModel,isData):
    
    wpForPlotting ="%.2f"%options.tau2tau1cutHP
    wpForPlotting = wpForPlotting.replace(".","v")
    postfix=""
    if options.usePuppiSD: postfix = "_PuppiSD"
    if options.useDDT: postfix = "_PuppiSD_DDT"
    if options.useN2DDT: postfix = "_PuppiSD_N2DDT"
    title = "Pruned jet mass (GeV)"
    if options.usePuppiSD or options.useDDT or options.useN2DDT:  title = "W Subjet Mass "
    
    
    frame = variable.frame()
    if(isData): dataset.plotOn(frame,RooFit.DataError(RooAbsData.Poisson),RooFit.Name(dataset.GetName ()))
    else: dataset.plotOn(frame,RooFit.DataError(RooAbsData.SumW2),RooFit.Name(dataset.GetName ()))
    pdfModel.plotOn(frame,RooFit.VisualizeError(fitResult,1), RooFit.Name("Fit error"),RooFit.FillColor(kGray),RooFit.LineColor(kGray)) #,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    pdfModel.plotOn(frame,RooFit.LineColor(kBlack),RooFit.Name(pdfModel.GetName())) #,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    chi2 = frame.chiSquare(pdfModel.GetName(), dataset.GetName ())
    pdfModel.plotOn(frame,RooFit.Name( "Gaussian 2" ),RooFit.Components("gaus2*"),RooFit.LineStyle(kSolid),RooFit.LineColor(kBlue+3),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    #pdfModel.plotOn(frame,RooFit.Name( "model_bkg" ),RooFit.Components("model_bkg*"),RooFit.LineStyle(9),RooFit.LineColor(kBlue+2),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    pdfModel.plotOn(frame,RooFit.Name( "model_pdf_exp" ),RooFit.Components("model_pdf_exp*"),RooFit.LineStyle(9),RooFit.LineColor(kRed+5),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    pdfModel.plotOn(frame,RooFit.Name( "Gaussian 1" ),RooFit.Components("gaus1*"),RooFit.LineStyle(kDashed),RooFit.LineColor(kRed+3),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    pdfModel.plotOn(frame,RooFit.Name( "Chebyshev comp." ),RooFit.Components("cheb*"),RooFit.LineStyle(kDashed),RooFit.LineColor(kBlue+3),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    if(isData): dataset.plotOn(frame,RooFit.DataError(RooAbsData.Poisson),RooFit.Name(dataset.GetName ()))
    else: dataset.plotOn(frame,RooFit.DataError(RooAbsData.SumW2),RooFit.Name(dataset.GetName ()))
    c1 =TCanvas("data_fail","",800,800)
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleOffset(0.90)
    frame.SetName("mjjFit")
    frame.GetYaxis().SetTitle("Events")
    frame.GetXaxis().SetTitle(title)
    frame.Draw()
    frame.GetYaxis().SetRangeUser(0,1500)
    frame.SetMinimum(0.)
    legend = getLegend()
    if(isData): legend.AddEntry(frame.findObject(dataset.GetName ()),"Data","lpe")
    else: legend.AddEntry(frame.findObject(dataset.GetName ()),"Total MC","lpe")
    legend.AddEntry(frame.findObject(pdfModel.GetName()),"Sim. fit","l")
    if frame.findObject("Gaussian 1"):
      legend.AddEntry(frame.findObject("Gaussian 1"),frame.findObject("Gaussian 1").GetName(),"l")
    if frame.findObject("Chebyshev comp."):
      legend.AddEntry(frame.findObject("Chebyshev comp."),frame.findObject("Chebyshev comp.").GetName(),"l")
    if frame.findObject("Gaussian 2"):
      legend.AddEntry(frame.findObject("Gaussian 2"),frame.findObject("Gaussian 2").GetName(),"l")
    if frame.findObject("model_pdf_exp"):
      legend.AddEntry(frame.findObject("model_pdf_exp"),frame.findObject("model_pdf_exp").GetName(),"l")
      
    #    pdfModel.plotOn(frame,RooFit.Name( "model_pdf_exp" ),RooFit.Components("model_pdf_exp*"),RooFit.LineStyle(9),RooFit.LineColor(kRed+5),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    
    legend.Draw("same")
    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
    addInfo = getPavetext()
    addInfo.AddText("#chi^{2}/nDOF = %.3f"%chi2)
    addInfo.Draw()
    c1.Update()
    cname = pdfModel.GetName()
    c1.SaveAs("plots/%s_%s_%s.png"%(cname,options.sample, self.boostedW_fitter_em.wtagger_label  ))
    c1.SaveAs("plots/%s_%s_%s.root"%(cname,options.sample, self.boostedW_fitter_em.wtagger_label ))
    return chi2

def drawDataAndMC(self, variable,fitResult,dataset,pdfModel,isData,variable2,fitResult2,dataset2,pdfModel2,isData2):

    wpForPlotting ="%.2f"%options.tau2tau1cutHP
    wpForPlotting = wpForPlotting.replace(".","v")
    postfix=""
    if options.usePuppiSD: postfix = "_PuppiSD"
    if options.useDDT: postfix = "_PuppiSD_DDT"
    if options.useN2DDT: postfix = "_PuppiSD_N2DDT"
    title = "Pruned jet mass (GeV)"
    if options.usePuppiSD or options.useDDT or options.useN2DDT:  title = "W Subjet Mass "


    frame = variable.frame()
    if(isData): dataset.plotOn(frame,RooFit.DataError(RooAbsData.Poisson),RooFit.Name(dataset.GetName ()))
    else: dataset.plotOn(frame,RooFit.DataError(RooAbsData.SumW2),RooFit.Name(dataset.GetName ()))
#    pdfModel.plotOn(frame,RooFit.VisualizeError(fitResult,1), RooFit.Name("Fit error"),RooFit.FillColor(kGray),RooFit.LineColor(kGray)) #,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    pdfModel.plotOn(frame,RooFit.LineColor(kBlack),RooFit.Name(pdfModel.GetName())) #,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    chi2 = frame.chiSquare(pdfModel.GetName(), dataset.GetName ())
    pdfModel.plotOn(frame,RooFit.Name( "Gaussian 2" ),RooFit.Components("gaus2*"),RooFit.LineStyle(kSolid),RooFit.LineColor(kBlue+3),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    #pdfModel.plotOn(frame,RooFit.Name( "Data_bkg comp." ),RooFit.Components("model_bkg*"),RooFit.LineStyle(9),RooFit.LineColor(kBlue+2),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))

    pdfModel.plotOn(frame,RooFit.Name( "model_pdf_exp" ),RooFit.Components("model_pdf_exp*"),RooFit.LineStyle(9),RooFit.LineColor(kRed+5),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
     
    pdfModel.plotOn(frame,RooFit.Name( "Gaussian Data comp." ),RooFit.Components("gaus1*"),RooFit.LineStyle(kDashed),RooFit.LineColor(kRed+3),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    pdfModel.plotOn(frame,RooFit.Name( "Chebyshev comp." ),RooFit.Components("cheb*"),RooFit.LineStyle(kDashed),RooFit.LineColor(kBlue+3),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    if(isData): dataset.plotOn(frame,RooFit.DataError(RooAbsData.Poisson),RooFit.Name(dataset.GetName ()))
    else: dataset.plotOn(frame,RooFit.DataError(RooAbsData.SumW2),RooFit.Name(dataset.GetName ()))


    if(isData2): dataset2.plotOn(frame,RooFit.DataError(RooAbsData.Poisson),RooFit.Name(dataset2.GetName ()),RooFit.MarkerColor(kBlue),RooFit.LineColor(kBlue))
    else: dataset2.plotOn(frame,RooFit.DataError(RooAbsData.SumW2),RooFit.Name(dataset2.GetName ()),RooFit.MarkerColor(kBlue),RooFit.LineColor(kBlue))
#    pdfModel2.plotOn(frame,RooFit.VisualizeError(fitResult2,1), RooFit.Name("Fit error"),RooFit.FillColor(kGray),RooFit.LineColor(kGray)) #,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    pdfModel2.plotOn(frame,RooFit.LineColor(kGreen),RooFit.Name(pdfModel2.GetName())) #,RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    chi2_2 = frame.chiSquare(pdfModel2.GetName(), dataset2.GetName ())
    pdfModel2.plotOn(frame,RooFit.Name( "Gaussian 2 MC" ),RooFit.Components("gaus2*"),RooFit.LineStyle(kSolid),RooFit.LineColor(kBlue+3),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    pdfModel2.plotOn(frame,RooFit.Name( "model_bkg MC comp." ),RooFit.Components("model_bkg*"),RooFit.LineStyle(9),RooFit.LineColor(kMagenta+2),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    pdfModel2.plotOn(frame,RooFit.Name( "Gaussian MC comp." ),RooFit.Components("gaus1*"),RooFit.LineStyle(kDashed),RooFit.LineColor(kOrange-3),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    pdfModel2.plotOn(frame,RooFit.Name( "Gaussian MC comp." ),RooFit.Components("model_pdf_exp*"),RooFit.LineStyle(kDashed),RooFit.LineColor(kGreen-3),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    pdfModel2.plotOn(frame,RooFit.Name( "Chebyshev comp. MC" ),RooFit.Components("cheb*"),RooFit.LineStyle(kDashed),RooFit.LineColor(kBlue+3),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
    if(isData2): dataset2.plotOn(frame,RooFit.DataError(RooAbsData.Poisson),RooFit.Name(dataset2.GetName ()),RooFit.MarkerColor(kGreen+3),RooFit.LineColor(kGreen+3))
    else: dataset2.plotOn(frame,RooFit.DataError(RooAbsData.SumW2),RooFit.Name(dataset2.GetName ()),RooFit.MarkerColor(kGreen+3),RooFit.LineColor(kGreen+3))

    c1 =TCanvas("data_fail","",800,800)
    frame.GetYaxis().SetTitleSize(0.05)
    frame.GetYaxis().SetTitleOffset(0.90)
    frame.SetName("mjjFit")
    frame.GetYaxis().SetTitle("Events")
    frame.GetXaxis().SetTitle(title)
    frame.Draw()
    frame.SetMinimum(0.)

    legend = getLegend()
    if(isData): legend.AddEntry(frame.findObject(dataset.GetName ()),"Data","lpe")
    else: legend.AddEntry(frame.findObject(dataset.GetName ()),"Total MC","lpe")
    legend.AddEntry(frame.findObject(dataset2.GetName ()),"Total MC","lpe")
    legend.AddEntry(frame.findObject(pdfModel.GetName()),"Sim. Data fit","l")
    legend.AddEntry(frame.findObject(pdfModel2.GetName()),"Sim. MC fit","l")
    if frame.findObject("Gaussian Data comp."):
      legend.AddEntry(frame.findObject("Gaussian Data comp."),frame.findObject("Gaussian Data comp.").GetName(),"l")
      legend.AddEntry(frame.findObject("Gaussian MC comp."),frame.findObject("Gaussian MC comp.").GetName(),"l")
    if frame.findObject("Chebyshev comp."):
      legend.AddEntry(frame.findObject("Chebyshev comp."),frame.findObject("Chebyshev comp.").GetName(),"l")
    if frame.findObject("Gaussian 2"):
      legend.AddEntry(frame.findObject("Gaussian Data comp."),frame.findObject("Gaussian Data comp.").GetName(),"l")
      legend.AddEntry(frame.findObject("Gaussian MC comp."),frame.findObject("Gaussian MC comp.").GetName(),"l")
    #if frame.findObject("Data_bkg comp."):
      #legend.AddEntry(frame.findObject("Data_bkg comp."),frame.findObject("Data_bkg comp.").GetName(),"l")
      #legend.AddEntry(frame.findObject("model_bkg MC comp."),frame.findObject("model_bkg MC comp.").GetName(),"l")
    if frame.findObject("model_pdf_exp"):
      legend.AddEntry(frame.findObject("model_pdf_exp"),frame.findObject("model_pdf_exp").GetName(),"l")
      
    #pdfModel.plotOn(frame,RooFit.Name( "model_pdf_exp" ),RooFit.Components("model_pdf_exp*"),RooFit.LineStyle(9),RooFit.LineColor(kRed+5),RooFit.Normalization(1.0,RooAbsReal.RelativeExpected))
     
    legend.Draw("same")
    CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
    addInfo = getPavetext()
    addInfo.AddText("Data #chi^{2}/nDOF = %.3f"%chi2)
    addInfo.AddText("MC #chi^{2}/nDOF = %.3f"%chi2_2)
    addInfo.Draw()
    c1.Update()
    cname = pdfModel.GetName()
    c1.SaveAs("plots/CombinedPlot_%s_%s.png"%(cname, self.boostedW_fitter_em.wtagger_label))
    c1.SaveAs("plots/CombinedPlot_%s_%s.root"%(cname, self.boostedW_fitter_em.wtagger_label))
    return chi2

    
def getSF():
    print "Getting W-tagging SF for cut " ,options.tau2tau1cutHP
    if options.useDDT: 
      options.usePuppiSD = True
      options.use76X = True
    boostedW_fitter_sim = doWtagFits()

def doFitsToMatchedTT():
    workspace4fit_ = RooWorkspace("workspace4fit_","workspace4fit_")
    ttMC_fitter = initialiseFits("em", options.sample, 50, 140, workspace4fit_)

    ttMC_fitter.get_mj_dataset(ttMC_fitter.file_TTbar_mc,"_TTbar_realW")
    ttMC_fitter.get_mj_dataset(ttMC_fitter.file_TTbar_mc,"_TTbar_fakeW")
    
    print"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    print"RealWs Passing tau21 cut :)  {0}".format(ttMC_fitter.countRealWsInPass)
    print"RealWs Failing tau21 cut :(  {0}".format(ttMC_fitter.countRealWsInFail)
    print"FakeWs Passing tau21 cut :(  {0}".format(ttMC_fitter.countFakeWsInPass)
    print"FakeWs Failing tau21 cut :)  {0}".format(ttMC_fitter.countFakeWsInFail)
    print"..............................................."
    if  ttMC_fitter.whighMass : # <--- FIX THIS:  reference to whighMass redefine as self.whighMass   
      print"   Here W candidate is most massive subjet     "
    else :
      print"   Here W candidate is lowest Bdisc subjet     "
    print"..............................................."
    print"W candidate is SJ 0 :  {0}".format(ttMC_fitter.countWisSJ0)
    print"W candidate is SJ 1 :  {0}".format(ttMC_fitter.countWisSJ1)
    print"..............................................."
    print"W cand has highest bdisc :)  {0}".format(ttMC_fitter.countWhighMassandBdisc)
    print"W cand has lowest  bdisc :(  {0}".format(ttMC_fitter.countWhighMassLowBdisc)
    print"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

    print ttMC_fitter.file_TTbar_mc
    print "_TTbar_realW"
    print ttMC_fitter.mj_shape["TTbar_realW"]
    print ttMC_fitter.channel
    print ttMC_fitter.wtagger_label

    fit_mj_single_MC(ttMC_fitter.workspace4fit_,ttMC_fitter.file_TTbar_mc,"_TTbar_realW",ttMC_fitter.mj_shape["TTbar_realW"],ttMC_fitter.channel,ttMC_fitter.wtagger_label)
    fit_mj_single_MC(ttMC_fitter.workspace4fit_,ttMC_fitter.file_TTbar_mc,"_TTbar_realW_failSubjetTau21cut",ttMC_fitter.mj_shape["TTbar_realW_fail"],ttMC_fitter.channel,ttMC_fitter.wtagger_label)
    fit_mj_single_MC(ttMC_fitter.workspace4fit_,ttMC_fitter.file_TTbar_mc,"_TTbar_fakeW",ttMC_fitter.mj_shape["TTbar_fakeW"],ttMC_fitter.channel,ttMC_fitter.wtagger_label)
    fit_mj_single_MC(ttMC_fitter.workspace4fit_,ttMC_fitter.file_TTbar_mc,"_TTbar_fakeW_failSubjetTau21cut",ttMC_fitter.mj_shape["TTbar_fakeW_fail"],ttMC_fitter.channel,ttMC_fitter.wtagger_label)
    
    print "Finished fitting matched tt MC! Plots can be found in plots_*_MCfits. Printing workspace:"
    workspace4fit_.Print()
        
def doFitsToMC():
    workspace4fit_ = RooWorkspace("workspace4fit_","workspace4fit_")
    boostedW_fitter_em = initialiseFits("em", options.sample, 50, 140, workspace4fit_)
    boostedW_fitter_em.get_datasets_fit_minor_bkg()
    print"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    print"RealWs in Pass:  {0}".format(boostedW_fitter_em.countRealWsInPass)
    print"RealWs in Fail:  {0}".format(boostedW_fitter_em.countRealWsInFail)
    print"FakeWs in Pass:  {0}".format(boostedW_fitter_em.countFakeWsInPass)
    print"FakeWs in Fail:  {0}".format(boostedW_fitter_em.countFakeWsInFail)
    print"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"

    print "Finished fitting MC! Plots can be found in plots_*_MCfits. Printing workspace:"
    workspace4fit_.Print()
                    
def GetWtagScalefactors( workspace,fitter):

    #------------- Calculate scalefactors -------------
    ### Efficiency in data and MC
    rrv_eff_MC_em   = workspace.var("eff_ttbar_TotalMC_em_mj")
    rrv_mean_MC_em  = workspace.var("rrv_mean1_gaus_ttbar_TotalMC_em_mj")
    rrv_sigma_MC_em = workspace.var("rrv_sigma1_gaus_ttbar_TotalMC_em_mj")

    rrv_eff_data_em   = workspace.var("eff_ttbar_data_em_mj")
    rrv_mean_data_em  = workspace.var("rrv_mean1_gaus_ttbar_data_em_mj")
    rrv_sigma_data_em = workspace.var("rrv_sigma1_gaus_ttbar_data_em_mj")

    ## GET HP SCALEFACTOR AND UNCERTIANTIES
    wtagger_sf_em             = rrv_eff_data_em.getVal()/rrv_eff_MC_em.getVal()
    wtagger_sf_em_err         = wtagger_sf_em * ( (rrv_eff_data_em.getError()/rrv_eff_data_em.getVal() )**2 + (rrv_eff_MC_em.getError()/rrv_eff_MC_em.getVal())**2 )**0.5

    wtagger_mean_shift_em     = rrv_mean_data_em.getVal()-rrv_mean_MC_em.getVal()
    wtagger_mean_shift_err_em = (rrv_mean_data_em.getError()**2 + rrv_mean_MC_em.getError()**2)**0.5

    wtagger_sigma_enlarge_em     = rrv_sigma_data_em.getVal()/rrv_sigma_MC_em.getVal()
    wtagger_sigma_enlarge_err_em = ((rrv_sigma_data_em.getError()/rrv_sigma_data_em.getVal())**2 + (rrv_sigma_MC_em.getError()/rrv_sigma_MC_em.getVal())**2 )**0.5* wtagger_sigma_enlarge_em

    mean_sf_error  = (rrv_mean_data_em.getVal()/rrv_mean_MC_em.getVal())   * ( (rrv_mean_data_em.getError()/rrv_mean_data_em.getVal())**2   +  (rrv_mean_MC_em.getError() /rrv_mean_MC_em.getVal())**2    )**0.5
    sigma_sf_error = (rrv_sigma_data_em.getVal()/rrv_sigma_MC_em.getVal()) * ( (rrv_sigma_data_em.getError()/rrv_sigma_data_em.getVal())**2 +  (rrv_sigma_MC_em.getError()/rrv_sigma_MC_em.getVal())**2   )**0.5
    eff_sf_error   = (rrv_eff_data_em.getVal()/rrv_eff_MC_em.getVal())     * ( (rrv_eff_data_em.getError()/rrv_eff_data_em.getVal())**2     +  (rrv_eff_MC_em.getError()  /rrv_eff_MC_em.getVal())**2     )**0.5

    ## GET EXTREME FAIL NUMBERS IN ORDER TO COMPUTE LP SF:
    rrv_number_ttbar_TotalMC_extremefailSubjetTau21cut_em_mj = workspace.var("rrv_number_ttbar_TotalMC_extremefailSubjetTau21cut_em_mj")
    rrv_number_ttbar_data_extremefailSubjetTau21cut_em_mj    = workspace.var("rrv_number_ttbar_data_extremefailSubjetTau21cut_em_mj")

    rrv_number_total_ttbar_TotalMC_em = workspace.var("rrv_number_ttbar_TotalMC_beforetau2tau1cut_em_mj")
    rrv_number_total_ttbar_data_em    = workspace.var("rrv_number_ttbar_data_beforetau2tau1cut_em_mj")

    eff_MC_em_extremefail   = rrv_number_ttbar_TotalMC_extremefailSubjetTau21cut_em_mj.getVal() / rrv_number_total_ttbar_TotalMC_em.getVal()
    eff_data_em_extremefail = rrv_number_ttbar_data_extremefailSubjetTau21cut_em_mj.getVal()    / rrv_number_total_ttbar_data_em.getVal()

    eff_MC_em_extremefail_error = 0.1
#    eff_MC_em_extremefail_error   = eff_MC_em_extremefail   * ( (rrv_number_ttbar_TotalMC_extremefailSubjetTau21cut_em_mj.getError()/rrv_number_ttbar_TotalMC_extremefailSubjetTau21cut_em_mj.getVal() )**2 + (rrv_number_total_ttbar_TotalMC_em.getError()/rrv_number_total_ttbar_TotalMC_em.getVal())**2 )**0.5
    eff_data_em_extremefail_error = 0.1
#    eff_data_em_extremefail_error = eff_data_em_extremefail * ( (rrv_number_ttbar_data_extremefailSubjetTau21cut_em_mj.getError()/rrv_number_ttbar_data_extremefailSubjetTau21cut_em_mj.getVal()       )**2 + (rrv_number_total_ttbar_data_em.getError()   /rrv_number_total_ttbar_data_em.getVal()   )**2 )**0.5

    eff_SF_extremefail       = 0.1
    eff_SF_extremefail_error = 0.1
#    eff_SF_extremefail       = eff_data_em_extremefail/eff_MC_em_extremefail
#    eff_SF_extremefail_error = eff_SF_extremefail * ( (eff_data_em_extremefail_error/eff_data_em_extremefail)**2 + (eff_MC_em_extremefail_error/eff_MC_em_extremefail)**2 )**0.5


    # w/ extreme fail
    eff_MC_em_LP   = 1.-rrv_eff_MC_em.getVal()   - eff_MC_em_extremefail
    eff_data_em_LP = 1.-rrv_eff_data_em.getVal() - eff_data_em_extremefail

    eff_MC_em_LP_err   = TMath.Sqrt( rrv_eff_MC_em.getError()  **2 + eff_MC_em_extremefail_error**2 )
    eff_data_em_LP_err = TMath.Sqrt( rrv_eff_data_em.getError()**2 + eff_data_em_extremefail_error**2 )

    wtagger_sf_em_LP     = eff_data_em_LP / eff_MC_em_LP
    wtagger_sf_em_LP_err = wtagger_sf_em_LP * ( (eff_data_em_LP_err/eff_data_em_LP)**2 + (eff_MC_em_LP_err/eff_MC_em_LP)**2 )**0.5

    # w/o extreme fail
    tmpq_eff_MC_em_LP   = 1. - rrv_eff_MC_em.getVal()
    tmpq_eff_data_em_LP = 1. - rrv_eff_data_em.getVal()

    tmpq_eff_MC_em_LP_err   = TMath.Sqrt( rrv_eff_MC_em.getError()  **2)
    tmpq_eff_data_em_LP_err = TMath.Sqrt( rrv_eff_data_em.getError()**2)

    pureq_wtagger_sf_em_LP = tmpq_eff_data_em_LP / tmpq_eff_MC_em_LP
    pureq_wtagger_sf_em_LP_err = pureq_wtagger_sf_em_LP*TMath.Sqrt( (tmpq_eff_data_em_LP_err/tmpq_eff_data_em_LP)**2 + (tmpq_eff_MC_em_LP_err/tmpq_eff_MC_em_LP)**2 )


    #------------- Print results -------------
    print "--------------------------------------------------------------------------------------------"
    print "                                             HP                                             "
    print "--------------------------------------------------------------------------------------------"
    print "W-tagging SF      : %0.3f +/- %0.3f (rel. error = %0.1f percent)" %(wtagger_sf_em, wtagger_sf_em_err,(wtagger_sf_em_err/wtagger_sf_em*100))
    print "Mass shift [GeV]  : %0.3f +/- %0.3f" %(wtagger_mean_shift_em, wtagger_mean_shift_err_em)
    print "Mass resolution SF: %0.3f +/- %0.3f" %(wtagger_sigma_enlarge_em, wtagger_sigma_enlarge_err_em)
    print ""
    print "Parameter             Data               Simulation        Data/Simulation"
    print " < m >           %0.3f +/- %0.3f      %0.3f +/- %0.3f      %0.3f +/- %0.3f" %(rrv_mean_data_em.getVal(),rrv_mean_data_em.getError(),rrv_mean_MC_em.getVal(),rrv_mean_MC_em.getError()    , rrv_mean_data_em.getVal()/rrv_mean_MC_em.getVal()  ,  mean_sf_error)
    print " #sigma          %0.3f +/- %0.3f      %0.3f +/- %0.3f      %0.3f +/- %0.3f" %(rrv_sigma_data_em.getVal(),rrv_sigma_data_em.getError(),rrv_sigma_MC_em.getVal(),rrv_sigma_MC_em.getError(), rrv_sigma_data_em.getVal()/rrv_sigma_MC_em.getVal(),  sigma_sf_error)
    print ""
    print "HP W-tag eff+SF  %0.3f +/- %0.3f      %0.3f +/- %0.3f      %0.3f +/- %0.3f" %(rrv_eff_data_em.getVal(),rrv_eff_data_em.getError(),rrv_eff_MC_em.getVal(),rrv_eff_MC_em.getError()        , rrv_eff_data_em.getVal()/rrv_eff_MC_em.getVal()    ,  eff_sf_error)
    print "--------------------------------------------------------------------------------------------"
    print "                                        EXTREME FAIL                                        "
    print "--------------------------------------------------------------------------------------------"
    print "Parameter                     Data            Simulation            Data/Simulation"
    print "Extreme fail eff+SF     %0.3f +/- %0.3f      %0.3f +/- %0.3f      %0.3f +/- %0.3f" %(eff_data_em_extremefail,eff_data_em_extremefail_error,eff_MC_em_extremefail,eff_MC_em_extremefail_error, eff_SF_extremefail, eff_SF_extremefail_error)
    print "--------------------------------------------------------------------------------------------"
    print "                                             LP                                             "
    print "--------------------------------------------------------------------------------------------"
    print "Parameter                               Data              Simulation         Data/Simulation"
    print "LP W-tag eff+SF ( w/ext fail)      %0.3f +/- %0.3f      %0.3f +/- %0.3f      %0.3f +/- %0.3f" %(eff_data_em_LP,eff_data_em_LP_err,eff_MC_em_LP,eff_MC_em_LP_err,wtagger_sf_em_LP,wtagger_sf_em_LP_err)
    print "LP W-tag eff+SF (wo/ext fail)      %0.3f +/- %0.3f      %0.3f +/- %0.3f      %0.3f +/- %0.3f" %(tmpq_eff_data_em_LP,tmpq_eff_data_em_LP_err,tmpq_eff_MC_em_LP,tmpq_eff_MC_em_LP_err,pureq_wtagger_sf_em_LP,pureq_wtagger_sf_em_LP_err)
    print "--------------------------------------------------------------------------------------------"
    print "--------------------------------------------------------------------------------------------"
    print ""; print "";

    #Write results to file
    fitter.file_out_ttbar_control.write("\n                                     HP                                    ")
    fitter.file_out_ttbar_control.write("\n-----------------------------------------------------------------------------------------------------------------------------")
    fitter.file_out_ttbar_control.write("\n")
    fitter.file_out_ttbar_control.write("\nW-tagging SF      : %0.3f +/- %0.3f (rel. error = %.1f percent)" %(wtagger_sf_em, wtagger_sf_em_err, (wtagger_sf_em_err/wtagger_sf_em*100)))
    fitter.file_out_ttbar_control.write("\n")
    fitter.file_out_ttbar_control.write("\nMass shift [GeV]  : %0.3f +/- %0.3f" %(wtagger_mean_shift_em, wtagger_mean_shift_err_em))
    fitter.file_out_ttbar_control.write("\nMass resolution SF: %0.3f +/- %0.3f" %(wtagger_sigma_enlarge_em, wtagger_sigma_enlarge_err_em))
    fitter.file_out_ttbar_control.write("\n")
    fitter.file_out_ttbar_control.write("\nParameter                 Data                          Simulation                          Data/Simulation")
    fitter.file_out_ttbar_control.write("\n < m >              %0.3f +/- %0.3f                  %0.3f +/- %0.3f                        %0.3f +/- %0.3f" %(rrv_mean_data_em.getVal(),rrv_mean_data_em.getError(),rrv_mean_MC_em.getVal(),rrv_mean_MC_em.getError()    , rrv_mean_data_em.getVal()/rrv_mean_MC_em.getVal()  ,  mean_sf_error))
    fitter.file_out_ttbar_control.write("\n #sigma             %0.3f +/- %0.3f                  %0.3f +/- %0.3f                        %0.3f +/- %0.3f" %(rrv_sigma_data_em.getVal(),rrv_sigma_data_em.getError(),rrv_sigma_MC_em.getVal(),rrv_sigma_MC_em.getError(), rrv_sigma_data_em.getVal()/rrv_sigma_MC_em.getVal(),  sigma_sf_error))
    fitter.file_out_ttbar_control.write("\n")
    fitter.file_out_ttbar_control.write("\n")
    fitter.file_out_ttbar_control.write("\nHP W-tag eff+SF     %0.3f +/- %0.3f                  %0.3f +/- %0.3f                        %0.3f +/- %0.3f" %(rrv_eff_data_em.getVal(),rrv_eff_data_em.getError(),rrv_eff_MC_em.getVal(),rrv_eff_MC_em.getError(), rrv_eff_data_em.getVal()/rrv_eff_MC_em.getVal(),  eff_sf_error))
    fitter.file_out_ttbar_control.write("\n")
    fitter.file_out_ttbar_control.write("\n-----------------------------------------------------------------------------------------------------------------------------")
    fitter.file_out_ttbar_control.write("\n                                EXTREME FAIL                               ")
    fitter.file_out_ttbar_control.write("\n-----------------------------------------------------------------------------------------------------------------------------")
    fitter.file_out_ttbar_control.write("\nParameter                     Data                          Simulation                          Data/Simulation")
    fitter.file_out_ttbar_control.write("\nExtreme fail eff+SF     %0.3f +/- %0.3f                  %0.3f +/- %0.3f                        %0.3f +/- %0.3f" %(eff_data_em_extremefail,eff_data_em_extremefail_error,eff_MC_em_extremefail,eff_MC_em_extremefail_error, eff_SF_extremefail, eff_SF_extremefail_error))
    fitter.file_out_ttbar_control.write("\n-----------------------------------------------------------------------------------------------------------------------------")
    fitter.file_out_ttbar_control.write("\n                                    LP                                     ")
    fitter.file_out_ttbar_control.write("\n-----------------------------------------------------------------------------------------------------------------------------")
    fitter.file_out_ttbar_control.write("\n")
    fitter.file_out_ttbar_control.write("\nParameter                                   Data                          Simulation                          Data/Simulation")
    fitter.file_out_ttbar_control.write("\nLP W-tag eff+SF ( w/ext fail)         %0.3f +/- %0.3f                  %0.3f +/- %0.3f                        %0.3f +/- %0.3f" %(eff_data_em_LP,eff_data_em_LP_err,eff_MC_em_LP,eff_MC_em_LP_err,wtagger_sf_em_LP,wtagger_sf_em_LP_err))
    fitter.file_out_ttbar_control.write("\nLP W-tag eff+SF (wo/ext fail)         %0.3f +/- %0.3f                  %0.3f +/- %0.3f                        %0.3f +/- %0.3f" %(tmpq_eff_data_em_LP,tmpq_eff_data_em_LP_err,tmpq_eff_MC_em_LP,tmpq_eff_MC_em_LP_err,pureq_wtagger_sf_em_LP,pureq_wtagger_sf_em_LP_err))
    fitter.file_out_ttbar_control.write("\n")
    fitter.file_out_ttbar_control.write("\n-----------------------------------------------------------------------------------------------------------------------------")


class initialiseFits:

    # Constructor: Input is channel (mu,ele,em), range in mj and a workspace
    def __init__(self, in_channel, in_sample, in_mj_min=50, in_mj_max=140, input_workspace=None):
      
      RooAbsPdf.defaultIntegratorConfig().setEpsRel(1e-9)
      RooAbsPdf.defaultIntegratorConfig().setEpsAbs(1e-9)

      #Define counts of Gen Matched Ws in each category              
      self.countRealWsInFail = 0
      self.countRealWsInPass = 0
      self.countFakeWsInFail = 0
      self.countFakeWsInPass = 0
      self.countWhighMassandBdisc = 0 
      self.countWhighMassLowBdisc = 0
      self.countWisSJ0 = 0
      self.countWisSJ1 = 0

      # Set channel 
      self.channel = in_channel
      
      print "CHANNEL = %s" %in_channel
      print "Using Tau21 HP cut of " ,options.tau2tau1cutHP 

      # Map of shapes to be used for the various fits (defined in PDFs/MakePdf.cxx)                                                                                                                                         
      self.mj_shape = ROOT.std.map(ROOT.std.string,ROOT.std.string)()
      
      # Fit functions for matched tt MC
#      self.mj_shape["TTbar_realW"]      = "ExpGaus"
      self.mj_shape["TTbar_realW"]      = "Gaus_ttbar" # "ExpGaus" #"GausErfExp_ttbar" #before "2Gaus_ttbar"
#      self.mj_shape["TTbar_realW_fail"] = "GausExp_failSubjetTau21cut"
      self.mj_shape["TTbar_realW_fail"] =  "Gaus_ttbar"  #"ExpGaus" # "ExpGaus" #"GausChebychev_ttbar_failSubjetTau21cut"
      self.mj_shape["TTbar_fakeW"]      =  "ErfExp" #  "GausErfExp_ttbar"  #"GausErfExp_ttbar_fakeW"
      self.mj_shape["TTbar_fakeW_fail"] = "ErfExp" #"GausErfExp_ttbar_failSubjetTau21cut"
      if options.ptbinmin == 500  and options.tau2tau1cutHP==0.55 :
            self.mj_shape["TTbar_fakeW"]      = "GausErfExp_ttbar_failSubjetTau21cut" # "ErfExp" #  "GausErfExp_ttbar"  #"GausErfExp_ttbar_fakeW"                                                                                                                                                                
            self.mj_shape["TTbar_fakeW_fail"] = "GausErfExp_ttbar_failSubjetTau21cut"  

      if (options.useDDT): 
        self.mj_shape["TTbar_realW_fail"]       = "GausChebychev_ttbar_failSubjetTau21cut"  
        
      # Fit functions for minor backgrounds
#      self.mj_shape["VV"]                 = "ExpGaus"
#      self.mj_shape["VV_fail"]            = "ExpGaus"
      self.mj_shape["WJets0"]             = "ExpGaus"  #"GausErfExp_Wjets" #"ErfExp"
#      self.mj_shape["WJets0"]             = "Exp"
      self.mj_shape["WJets0_fail"]        = "Exp"
#      self.mj_shape["WJets0_fail"]        = "Exp"
      if not options.noQCD :
          self.mj_shape["QCD"]                =  "ExpGaus" #"Gaus_QCD"                                                                                                    
          self.mj_shape["QCD_fail"]           =  "ExpGaus" #"Gaus_QCD"                                                                                                    
          if ( (options.ptbinmin == 300 and options.ptbinmax == 500) or (options.ptbinmin == 200  and options.ptbinmax != 300) ) and options.tau2tau1cutHP==0.55 :
              self.mj_shape["QCD"]                =  "DeuxGausChebychev" #"GausChebychev_QCD" #"DeuxGaus" # "Exp"                                                         
              self.mj_shape["QCD_fail"]           = "DeuxGausChebychev" # "GausChebychev_QCD" #"DeuxGaus" #"Exp"                                                          
          if options.ptbinmin == 500  and options.tau2tau1cutHP==0.55 :
              self.mj_shape["QCD"]                =  "ExpGaus"#"Gaus_QCD" #"DeuxGausChebychev" #"GausChebychev_QCD" #"DeuxGaus" # "Exp"                                  \
                                                                                                                                                                          
              self.mj_shape["QCD_fail"]           = "ExpGaus"#"Gaus_QCD"                                                                                                  
          if options.ptbinmin == 200  and options.ptbinmax == 300 and options.tau2tau1cutHP==0.55 :
              self.mj_shape["QCD"]                =  "Gaus_QCD"
              self.mj_shape["QCD_fail"]           = "Gaus_QCD"


      if not options.noST :
          #self.mj_shape["STop"]               = "ExpGaus_sp"
          self.mj_shape["STop"]               = "ExpGaus"
          self.mj_shape["STop_fail"]          = "ExpGaus"  
          if (options.usePuppiSD): 
              self.mj_shape["STop_fail"]          = "ExpGaus"  

#      if (options.useN2DDT):
#        self.mj_shape["STop_fail"]          = "ErfExpGaus_sp"
#        self.mj_shape["STop_fail"]          = "ExpGaus"
#        #self.mj_shape["STop_fail"]          = "ExpGaus"

#      if (options.tau2tau1cutHP==0.60): 
#        self.mj_shape["QCD_fail"]     = "Exp"
#        self.mj_shape["QCD"]          = "Exp"
#        self.mj_shape["WJets0_fail"] = "Exp" 
        
#      #if (options.useDDT):
#        self.mj_shape["VV"]                 = "ExpGaus"
#        self.mj_shape["VV_fail"]            = "ErfExpGaus_sp"
#        self.mj_shape["STop_fail"]          = "ErfExpGaus_sp" 
#        self.mj_shape["STop"]               = "ExpGaus"  
        
      # Fit functions used in simultaneous fit of pass and fail categories
      self.mj_shape["bkg_mc_fail"]          = "Exp"
      self.mj_shape["bkg_data_fail"]        = "Exp"#"GausErfExp_ttbar_failSubjetTau21cut"
      
      self.mj_shape["signal_mc_fail"]       = "Gaus_ttbar" #"GausErfExp_ttbar_failSubjetTau21cut"  #"Gaus_ttbar"
      self.mj_shape["signal_data_fail"]     = "Gaus_ttbar" #"GausErfExp_ttbar_failSubjetTau21cut"
# was "ExpGaus"  below !!!
      self.mj_shape["bkg_data"]             = "ExpGaus" #"GausChebychev_ttbar"  #"ExpGaus" #"GausChebychev_ttbar"  
      self.mj_shape["bkg_mc"]               = "ExpGaus" #"GausChebychev_ttbar"  #"ExpGaus"  
      if options.ptbinmin == 200 and options.ptbinmax == 300 :
          self.mj_shape["bkg_data"]             = "ExpGaus" #"GausChebychev_ttbar"  #"ErfExpGaus_sp"
          ### NOTE: "ExpGaus" may be better !!!
          self.mj_shape["bkg_mc"]               = "ExpGaus" #"GausChebychev_ttbar" #"ErfExpGaus_sp"
      if options.ptbinmin == 300 and options.ptbinmax == 500 and options.tau2tau1cutHP==0.35 :
          self.mj_shape["bkg_mc_fail"]          =  "ExpGaus"
          self.mj_shape["bkg_data_fail"]        =  "ExpGaus"

          self.mj_shape["signal_mc_fail"]       = "ExpGaus" 
          self.mj_shape["signal_data_fail"]     = "ExpGaus"  

          self.mj_shape["bkg_data"]             =  "ExpGaus" 
          self.mj_shape["bkg_mc"]               =  "ExpGaus"
  
          self.mj_shape["signal_data"]          = "Gaus_ttbar"                               
          self.mj_shape["signal_mc"]            = "Gaus_ttbar"

      if options.ptbinmin == 200 and options.ptbinmax == 300  and options.tau2tau1cutHP==0.55 :
          self.mj_shape["bkg_mc_fail"]          = "Exp"
          self.mj_shape["bkg_data_fail"]        = "Exp"

          self.mj_shape["signal_mc_fail"]       = "GausErfExp_ttbar" #"ExpGaus"
          self.mj_shape["signal_data_fail"]     = "GausErfExp_ttbar" #"ExpGaus"

          self.mj_shape["bkg_data"]             = "ExpGaus" # "Exp"
          self.mj_shape["bkg_mc"]               = "ExpGaus" # "Exp"

          self.mj_shape["signal_data"]          =  "ExpGaus" #"GausErfExp_ttbar" #"Gaus_ttbar"
          self.mj_shape["signal_mc"]            =  "ExpGaus" #"GausErfExp_ttbar" #"Gaus_ttbar"

    
      if options.ptbinmin == 300 and options.ptbinmax == 500 and options.tau2tau1cutHP==0.55 :
          self.mj_shape["bkg_mc_fail"]          = "DeuxGausChebychev" # "GausChebychev_QCD" # "DeuxGaus"  #"ExpGaus"
          self.mj_shape["bkg_data_fail"]        = "DeuxGausChebychev" # "GausChebychev_QCD" # "DeuxGaus"  #"ExpGaus"

          self.mj_shape["signal_mc_fail"]       = "ExpGaus" #"Gaus_ttbar" #"ExpGaus"                                                                                                                                                   
          self.mj_shape["signal_data_fail"]     = "ExpGaus"                                                                                                                                                   

          self.mj_shape["bkg_data"]             =  "ExpGaus"
          self.mj_shape["bkg_mc"]               =  "ExpGaus"

          self.mj_shape["signal_data"]          = "ExpGaus" #"Gaus_ttbar"
          self.mj_shape["signal_mc"]            = "ExpGaus" #"Gaus_ttbar"

      if options.ptbinmin == 500  and options.tau2tau1cutHP==0.55 :
          self.mj_shape["bkg_mc_fail"]          = "GausChebychev_ttbar_failSubjetTau21cut" #"DeuxGausChebychev" #"DeuxGaus"  #"ExpGaus" #"GausChebychev_ttbar_failSubjetTau21cut"  #"DeuxGausChebychev" # "GausChebychev_QCD" # "DeuxGaus"  #"ExpGaus"                                                                                                                                                                                              
          self.mj_shape["bkg_data_fail"]        =  "GausChebychev_ttbar_failSubjetTau21cut" #"DeuxGausChebychev" # "DeuxGaus"  #"ExpGaus" #"GausChebychev_ttbar_failSubjetTau21cut" # "DeuxGausChebychev" # "GausChebychev_QCD" # "DeuxGaus"  #"ExpGaus"                                                                                                                                                                                              

          self.mj_shape["signal_mc_fail"]       =  "DeuxGaus" #"GausChebychev_ttbar_failSubjetTau21cut" #"ExpGaus" #"Gaus_ttbar" #"ExpGaus"                                                                                                                                                                                                                              
          self.mj_shape["signal_data_fail"]     =  "DeuxGaus" #"GausChebychev_ttbar_failSubjetTau21cut" #"ExpGaus"

          self.mj_shape["bkg_data"]             =  "GausChebychev_ttbar_failSubjetTau21cut" #"ExpGaus"
          self.mj_shape["bkg_mc"]               =  "GausChebychev_ttbar_failSubjetTau21cut" #"ExpGaus"

          self.mj_shape["signal_data"]          = "Gaus"#"Gaus_ttbar"                                                                                                                                                                                                                                         
          self.mj_shape["signal_mc"]            = "Gaus" # "Gaus_ttbar"  

      if options.ptbinmin == 200 and options.ptbinmax != 300  and options.tau2tau1cutHP==0.55 :
          self.mj_shape["bkg_mc_fail"]          = "DeuxGausChebychev" # "DeuxGaus" #"Exp"
          self.mj_shape["bkg_data_fail"]        = "DeuxGausChebychev"  #"DeuxGaus" #"Exp"

          self.mj_shape["signal_mc_fail"]       = "ExpGaus"                                                                                                   
          self.mj_shape["signal_data_fail"]     = "ExpGaus"                                                                                                   

          self.mj_shape["bkg_data"]             = "ExpGaus" # "Exp"                                                                                                               
          self.mj_shape["bkg_mc"]               = "ExpGaus" # "Exp"                                                                                                               

          self.mj_shape["signal_data"]          =  "ExpGaus" #"ExpGaus" #"GausErfExp_ttbar" #"Gaus_ttbar"                                                                                    
          self.mj_shape["signal_mc"]            =  "ExpGaus" #"ExpGaus" #"GausErfExp_ttbar" #"Gaus_ttbar" 

      # ptbinmin
      #self.mj_shape["signal_data"]          = "Gaus_ttbar" #Before 2Gaus_ttbar
      #self.mj_shape["signal_mc"]            = "Gaus_ttbar"
      # if  options.ptbinmin == 500 :
      #     self.mj_shape["signal_data"]          = "GausErfExp_ttbar" #"GausChebychev_ttbar" #"Gaus_ttbar" #Before 2Gaus_ttbar                                                                                   
      #     self.mj_shape["signal_mc"]            = "GausErfExp_ttbar" #"GausChebychev_ttbar" #"Gaus_ttbar"

      
#      if (options.useDDT): 
#        self.mj_shape["signal_mc_fail"]       = "GausChebychev_ttbar_failSubjetTau21cut" 
#        self.mj_shape["signal_data_fail"]     = "GausChebychev_ttbar_failSubjetTau21cut"
      
      # # #TESTS USING OLD METHOD, EG ADDING TWO ADDITIONAL FIT FUNCTIONS
#       self.mj_shape["signal_data"]          = "2Gaus_ttbar"
#       self.mj_shape["signal_mc"]            = "2Gaus_ttbar"
#       self.mj_shape["signal_mc_fail"]       = "GausChebychev_ttbar_failSubjetTau21cut"
#       self.mj_shape["signal_data_fail"]     = "GausChebychev_ttbar_failSubjetTau21cut"
      
      #Set lumi  
      self.Lumi= 35860.#  35800.
      # self.Lumi=2198. #74
      if options.use76X: self.Lumi=35800. #76
          
      self.BinWidth_mj = 7.
      self.narrow_factor = 1.

      self.BinWidth_mj = self.BinWidth_mj/self.narrow_factor
      nbins_mj         = int( (in_mj_max - in_mj_min) / self.BinWidth_mj )
      in_mj_max        = in_mj_min+nbins_mj*self.BinWidth_mj
      
      jetMass = "PUPPI + SoftDrop jet mass"
      if options.usePuppiSD: jetMass =  "W Subjet Mass "  #"("+str(options.ptbinmin)+"<pt<"+str(options.ptbinmax)+") PUPPI Softdrop Subjet0 Mass"
      if options.useN2DDT: jetMass = "("+str(options.ptbinmin)+"<pt<"+str(options.ptbinmax)+") PUPPI Softdrop Subjet0 Mass"

      rrv_mass_j = RooRealVar("rrv_mass_j", jetMass ,(in_mj_min+in_mj_max)/2.,in_mj_min,in_mj_max,"GeV")
      rrv_mass_j.setBins(nbins_mj)
 
      # Create workspace and import fit variable
      if input_workspace is None:
          self.workspace4fit_ = RooWorkspace("workspace4fit_","Workspace4fit_")
      else:
          self.workspace4fit_ = input_workspace
      getattr(self.workspace4fit_,"import")(rrv_mass_j)

      # Signal region between 65 and 105 GeV
      self.mj_sideband_lo_min = in_mj_min
      self.mj_sideband_lo_max = 65
      self.mj_signal_min      = 65
      self.mj_signal_max      = 105
      self.mj_sideband_hi_min = 105
      self.mj_sideband_hi_max = in_mj_max
 
      # Setting ranges...
      rrv_mass_j.setRange("sb_lo",self.mj_sideband_lo_min,self.mj_sideband_lo_max) # 30-65 GeV
      rrv_mass_j.setRange("signal_region",self.mj_signal_min,self.mj_signal_max)   # 65-105 GeV
      rrv_mass_j.setRange("sb_hi",self.mj_sideband_hi_min,self.mj_sideband_hi_max) # 105-135 GeV
      rrv_mass_j.setRange("controlsample_fitting_range",50,140) # ---> what is this????
        

      # Directory and input files
      if not options.salsetup: 
        self.file_Directory         = "/uscms_data/d3/aparker/Wtag/ForkofB2GTTBar_V4Branch/CMSSW_8_0_22/src/Analysis/B2GTTbar/test/pyttbarfw/"
      else:
        self.file_Directory         = "/Users/rappoccio/fwlite/B2G/boostedWScalefactorProducer/data/"
      #self.file_Directory = "/Users/rappoccio/fwlite/B2G/boostedWScalefactorProducer/data/"
#"/uscms_data/d3/aparker/Wtag/ForkofB2GTTBar_V4Branch/CMSSW_8_0_22/src/Analysis/B2GTTbar/test/pyttbarfw/"
#      self.file_Directory         = "$HOME/EXOVVAnalysisRunII/AnalysisOutput/Wtag_80X/WWTree_%s/"%(self.channel) #For 80X!!!!
      # self.file_Directory         = "$HOME/EXOVVAnalysisRunII/AnalysisOutput/Wtag/PRUNED/WWTree_%s/"%(self.channel)
    
      # if options.usePuppiSD :
#         self.file_Directory       = "$HOME/EXOVVAnalysisRunII/AnalysisOutput/Wtag_80X/WWTree_%s/"%(self.channel)
#         if options.use76X:
#            self.file_Directory       = "$HOME/EXOVVAnalysisRunII/AnalysisOutput/Wtag/PUPPISD_newcorr/WWTree_%s/"%(self.channel)

      postfix = ""
      if options.use76X: postfix ="_76X"  
      if not options.v5 :
        self.nameTag = "METmu40el80ptRel30" # <-- have same MET cuts as "looserMETandPtRelCuts" just more gen particle and subjet 1 info branches in the ttree (all V4 ttrees)
        # "looserMETandPtRelCuts"<-- have MET cuts of 40 GeV for muon and 80 GeV for electrons and Pt Rel 30 
        # "noTopTagSkimWeights3" <-- have MET cuts of 50 GeV for muon and 120 GeV for electrons and Pt Rel 40 
        self.file_data              = ("singlemuandel_run2016_highmass_"+ self.nameTag +".root")# ("ExoDiBosonAnalysis.WWTree_data_76X_PUPPISD.root")
        self.file_pseudodata        = ("pseudodata_highmass_"+ self.nameTag +".root")#("ExoDiBosonAnalysis.WWTree_pseudodata_76X_PUPPISD.root")     
        self.file_WJets0_mc         = ("wjets_highmass_"+ self.nameTag +".root ")#("ExoDiBosonAnalysis.WWTree_WJets_76X_PUPPISD.root")
        self.file_QCD_mc             = ("QCD_highmass_"+ self.nameTag +".root")# ("ExoDiBosonAnalysis.WWTree_VV_76X_PUPPISD.root")        
        self.file_TTbar_mc          = ("ttbarTTuneCUETP8M2T4_highmass_"+ self.nameTag +".root") #("ExoDiBosonAnalysis.WWTree_TTbar_powheg_76X_PUPPISD.root")
        self.file_STop_mc           = ("ST_highmass_"+ self.nameTag +".root")# ("ExoDiBosonAnalysis.WWTree_STop_76X_PUPPISD.root")
      if options.v5 :   
        self.nameTag = "June11"
        self.file_data              = ("singlemuandel_run2016_highmass_"+ self.nameTag +".root") #singlemuandel_run2016_highmass_June1.root
        self.file_pseudodata        = ("pseudodata_highmass_"+ self.nameTag +".root") #pseudodata_highmass_June1.root
        self.file_WJets0_mc         = ("wjets_highmass_"+ self.nameTag +".root ") # wjets_highmass_June1.root
        if not options.noQCD :
            self.file_QCD_mc             = ("QCD_highmass_"+ self.nameTag +".root") # QCD_highmass_June1.root
        self.file_TTbar_mc          = ("ttbarTTuneCUETP8M2T4_highmass_"+ self.nameTag +".root") # ttbarTuneCUETP8M2T4_highmass_June1.root
        if not options.noST :
            self.file_STop_mc           = ("ST_highmass_"+ self.nameTag +".root") # ST_highmass_June1.root

      #self.file_data              = ("Data_2Trans.root")
      #self.file_WJets0_mc         = ("WJets_2Trans.root") 
      #self.file_VV_mc             = ("VV_2Trans.root")
      #self.file_QCD_mc            = ("QCD.root")
      #self.file_STop_mc           = ("ST_2Trans.root")
      #self.file_TTbar_mc          = ("TT_2Trans.root")
      #self.file_pseudodata        = ("PsuedoData_2Trans.root")      
      #Important! ROOT tree containing all backgrounds added together (tt+singleT+VV+Wjets). Used for fit to total MC
      # self.file_pseudodata        = ("pseudodata_weighted.root")
      # Define Tau21 WP
      self.wtagger_label = "HP"
      self.wtagger_cut = options.tau2tau1cutHP
      self.wtagger_cut_min = 0.
      
      if options.usePuppiSD: 
        postfix = postfix + "_PuppiSD"
      if options.useDDT: 
        postfix = postfix + "_PuppiSD_DDT"    
      if options.useN2DDT: postfix = postfix + "_PuppiSD_N2DDT"

      # Define label used for plots and choosing fit paramters in PDFs/MakePdf.cxx  
      wp = "%.2f" %options.tau2tau1cutHP
      wp = wp.replace(".","v")
      ptBin = "ptSubjet"+str(options.ptbinmin)+"To"+str(options.ptbinmax)+"_ttSF0p9"
      subjetBtag = "subjetisBmedCSV"
      fitrangeis = "_fit50to140"
      self.wtagger_label = self.wtagger_label + "%s%s%s%s%s%s"%(wp,in_sample,postfix, ptBin, subjetBtag, fitrangeis ) 

      
      #Color pallett for plots
      self.color_palet = ROOT.std.map(ROOT.std.string, int) ()
      self.color_palet["data"]              = 1
      self.color_palet["WJets"]             = 2
      #self.color_palet["VV"]                = 4
      if not options.noQCD:
          self.color_palet["QCD"]               = 5
      if not options.noST:
          self.color_palet["STop"]              = 7
      self.color_palet["TTbar"]             = 210
      self.color_palet["TTbar_realW"]       = 210
      self.color_palet["TTbar_fakeW"]       = 419
      self.color_palet["Signal"]            = 1
      self.color_palet["Uncertainty"]       = 1
      self.color_palet["Other_Backgrounds"] = 1    
      
      # Cuts (dont need these cuts if they are already implemented in ROOT tree)
      self.vpt_cut      = 150   # hadronic and leptonic W cut
      self.mass_lvj_max = 5000. # invariant mass of 3 body max
      self.mass_lvj_min = 0.    # invariant mass of 3 body min
      self.pfMET_cut    = 40.    # missing transverse energy
      self.lpt_cut      = 53.    # lepton pT
      self.AK8_pt_min   = 200.
      self.AK8_pt_max   = 10000.
      if self.channel  == "el":
        self.pfMET_cut = 80.
        self.lpt_cut = 53.      
      
      # Out .txt file with final SF numbers
      self.file_ttbar_control_txt = "WtaggingSF"+str(self.wtagger_label)+".txt"
      self.file_out_ttbar_control = open(self.file_ttbar_control_txt,"w")
                                                                                                                                                             
      setTDRStyle()

    def get_datasets_fit_minor_bkg(self):
        
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j")
        if not options.noST :
            # Build single-t fit pass and fail distributions
            print "##################################################"
            print "############### Single Top DataSet ###############"
            print "##################################################"
            print ""

            self.get_mj_dataset(self.file_STop_mc,"_STop")
            fit_mj_single_MC(self.workspace4fit_,self.file_STop_mc,"_STop"                        ,self.mj_shape["STop"],self.channel,self.wtagger_label) #Start value and range of parameters defined in PDFs/MakePDF.cxx
            fit_mj_single_MC(self.workspace4fit_,self.file_STop_mc,"_STop_failSubjetTau21cut"        ,self.mj_shape["STop_fail"],self.channel,self.wtagger_label)

        ### Build WJet fit pass and fail distributions
        print "###########################################"
        print "############### WJets Pythia ##############"
        print "###########################################"
        print ""

        self.get_mj_dataset(self.file_WJets0_mc,"_WJets0")
        fit_mj_single_MC(self.workspace4fit_,self.file_WJets0_mc,"_WJets0",self.mj_shape["WJets0"],self.channel,self.wtagger_label)
        fit_mj_single_MC(self.workspace4fit_,self.file_WJets0_mc,"_WJets0_failSubjetTau21cut",self.mj_shape["WJets0_fail"],self.channel,self.wtagger_label)


        # Build VV fit pass and fail distributions
#        print "#########################################"
##        print "############### VV Pythia ###############"
#        print "#########################################"
#        print ""
#        print ""

#        self.get_mj_dataset(self.file_VV_mc,"_VV")
#        fit_mj_single_MC(self.workspace4fit_,self.file_VV_mc,"_VV",self.mj_shape["VV"],self.channel,self.wtagger_label)
#        fit_mj_single_MC(self.workspace4fit_,self.file_VV_mc,"_VV_failSubjetTau21cut",self.mj_shape["VV_fail"],self.channel,self.wtagger_label)
        
        if not options.noQCD:
            print "#########################################"
            print "################## QCD ##################"
            print "#########################################"
            print ""
            print ""
       
            self.get_mj_dataset(self.file_QCD_mc,"_QCD")
            fit_mj_single_MC(self.workspace4fit_,self.file_QCD_mc,"_QCD",self.mj_shape["QCD"],self.channel,self.wtagger_label)
            fit_mj_single_MC(self.workspace4fit_,self.file_QCD_mc,"_QCD_failSubjetTau21cut",self.mj_shape["QCD_fail"],self.channel,self.wtagger_label)
            

        if options.fitMC:
            return

        # Get dataset for ttbar
        print "#########################################"
        print "################ TTbar %s################"%options.sample
        print "#########################################"
        print ""

        self.get_mj_dataset(self.file_TTbar_mc,"_TTbar")
        self.get_mj_dataset(self.file_TTbar_mc,"_TTbar_realW")
        self.get_mj_dataset(self.file_TTbar_mc,"_TTbar_fakeW")

        # Get dataset used for fit to total MC
        print "################################################"
        print "############## Pseudo Data Powheg ##############"
        print "################################################"
        print ""
        self.get_mj_dataset(self.file_pseudodata,"_TotalMC")

        print "#################################"
        print "############# Data ##############"
        print "#################################"
        print ""
        print ""
        self.get_mj_dataset(self.file_data,"_data")

        # print "Saving workspace in myworkspace.root! To save time when debugging use option --WS myworkspace.root to avoid recreating workspace every time"
        # filename = "myworkspace.root"
        # self.workspace4fit_.writeToFile(filename)

    def get_sim_fit_components(self):
#      self.print_yields()
      self.constrainslist_data = ROOT.std.vector(ROOT.std.string)()
      self.constrainslist_mc   = ROOT.std.vector(ROOT.std.string)()
        
      #Construct pass/fail models (fix minor backgrounds, create sim. fit total PDFS)
      ScaleFactorTTbarControlSampleFit(self.workspace4fit_,self.mj_shape,self.color_palet,self.constrainslist_data,self.constrainslist_mc,"",self.channel,self.wtagger_label,self.AK8_pt_min,self.AK8_pt_max)
     
      #Get data/MC scalefactors
      rrv_scale_number                      = self.workspace4fit_.var("rrv_scale_number_TTbar_STop_QCD_WJets").getVal()
      rrv_scale_number_fail                 = self.workspace4fit_.var("rrv_scale_number_TTbar_STop_QCD_WJets_fail").getVal()
      
      #Print data/MC scalefactors
      print " Pass MC / all data = %.3f" %(rrv_scale_number)
      print " Fail MC / all data = %.3f" %(rrv_scale_number_fail)
        
    def print_yields(self):

        # Print dataset yields in the signal region
        print ""
        print ""
        print ""
        self.workspace4fit_.var("rrv_number_dataset_signal_region_data_"    +self.channel+"_mj").Print()
#        self.workspace4fit_.var("rrv_number_dataset_signal_region_VV"      +self.channel+"_mj").Print()
        self.workspace4fit_.var("rrv_number_dataset_signal_region_WJets0_"  +self.channel+"_mj").Print()
        if not options.noQCD :
            self.workspace4fit_.var("rrv_number_dataset_signal_region_QCD_"     +self.channel+"_mj").Print()
        if not options.noST :
            self.workspace4fit_.var("rrv_number_dataset_signal_region_STop_"    +self.channel+"_mj").Print()
        self.workspace4fit_.var("rrv_number_dataset_signal_region_TTbar_"   +self.channel+"_mj").Print()
        print ""
        print ""
        print ""

        number_dataset_signal_region_data_mj                      = self.workspace4fit_.var("rrv_number_dataset_signal_region_data_"+self.channel+"_mj").getVal()
        number_dataset_signal_region_error2_data_mj               = self.workspace4fit_.var("rrv_number_dataset_signal_region_error2_data_"+self.channel+"_mj").getVal()
        
        number_dataset_signal_region_TotalMC_mj                   = self.workspace4fit_.var("rrv_number_dataset_signal_region_TotalMC_"+self.channel+"_mj").getVal()
        number_dataset_signal_region_error2_TotalMC_mj            = self.workspace4fit_.var("rrv_number_dataset_signal_region_error2_TotalMC_"+self.channel+"_mj").getVal()
        
        number_dataset_signal_region_before_cut_data_mj           = self.workspace4fit_.var("rrv_number_dataset_signal_region_before_cut_data_"+self.channel+"_mj").getVal()
        number_dataset_signal_region_before_cut_error2_data_mj    = self.workspace4fit_.var("rrv_number_dataset_signal_region_before_cut_error2_data_"+self.channel+"_mj").getVal()
        
        number_dataset_signal_region_before_cut_TotalMC_mj        = self.workspace4fit_.var("rrv_number_dataset_signal_region_before_cut_TotalMC_"+self.channel+"_mj").getVal()
        number_dataset_signal_region_before_cut_error2_TotalMC_mj = self.workspace4fit_.var("rrv_number_dataset_signal_region_before_cut_error2_TotalMC_"+self.channel+"_mj").getVal()
        
        wtagger_eff_MC                                            = number_dataset_signal_region_TotalMC_mj/number_dataset_signal_region_before_cut_TotalMC_mj
        wtagger_eff_data                                          = number_dataset_signal_region_data_mj/number_dataset_signal_region_before_cut_data_mj

        wtagger_eff_reweight                                      = wtagger_eff_data/wtagger_eff_MC
        wtagger_eff_reweight_err                                  = wtagger_eff_reweight*TMath.Sqrt(number_dataset_signal_region_error2_data_mj/number_dataset_signal_region_data_mj/number_dataset_signal_region_data_mj + number_dataset_signal_region_error2_TotalMC_mj/number_dataset_signal_region_TotalMC_mj/number_dataset_signal_region_TotalMC_mj +number_dataset_signal_region_before_cut_error2_data_mj/number_dataset_signal_region_before_cut_data_mj/number_dataset_signal_region_data_mj + number_dataset_signal_region_before_cut_error2_TotalMC_mj/number_dataset_signal_region_before_cut_TotalMC_mj/number_dataset_signal_region_before_cut_TotalMC_mj)
        
        print ""
        print "Nr. data events in signal_region                  : %s +/- sqrt(%s)"%(number_dataset_signal_region_data_mj, number_dataset_signal_region_error2_data_mj**.5)
        print ""
        print "Nr. MC events in signal_region                    : %s +/- sqrt(%s)"%(number_dataset_signal_region_TotalMC_mj, number_dataset_signal_region_error2_TotalMC_mj)
        print ""
        print "Nr. dataevents in signalregion before cut on tau21: %s +/- sqrt(%s)"%(number_dataset_signal_region_before_cut_data_mj, number_dataset_signal_region_before_cut_error2_data_mj)
        print ""
        print "Nr. MC events in signalregion before cut on tau21 : %s +/- sqrt(%s) "%(number_dataset_signal_region_before_cut_TotalMC_mj, number_dataset_signal_region_before_cut_error2_TotalMC_mj)
        print ""                                                     
        print "W-tagging efficiency (pre-fit):"
        print "W-tagging eff. MC       = %.3f "%(wtagger_eff_MC)
        print "W-tagging eff. data     = %.3f "%(wtagger_eff_data)
        print "W-tagging SF            = %.3f +/- %.3f"%(wtagger_eff_reweight, wtagger_eff_reweight_err)
        print ""
        print ""
        
        self.file_out_ttbar_control.write("%s channel SF: \n"%(self.channel))
        self.file_out_ttbar_control.write("Nr. events in signal_region                        : %s +/- sqrt(%s)\n"%(number_dataset_signal_region_data_mj, number_dataset_signal_region_error2_data_mj))
        self.file_out_ttbar_control.write("Nr. TotalMC in signal_region                       : %s +/- sqrt(%s) \n"%(number_dataset_signal_region_TotalMC_mj, number_dataset_signal_region_error2_TotalMC_mj))
        self.file_out_ttbar_control.write("event number of data in signalregion before_cut    : %s +/- sqrt(%s)\n"%(number_dataset_signal_region_before_cut_data_mj, number_dataset_signal_region_before_cut_error2_data_mj))
        self.file_out_ttbar_control.write("event number of TotalMC in signal_region before_cut: %s +/- sqrt(%s) \n"%(number_dataset_signal_region_before_cut_TotalMC_mj, number_dataset_signal_region_before_cut_error2_TotalMC_mj))
        self.file_out_ttbar_control.write("wtagger_eff_MC         = %s       \n"%(wtagger_eff_MC ))
        self.file_out_ttbar_control.write("wtagger_eff_data       = %s       \n"%(wtagger_eff_data ))
        self.file_out_ttbar_control.write("wtagger_eff_reweight   = %s +/- %s\n"%(wtagger_eff_reweight, wtagger_eff_reweight_err))
            
    # Loop over trees
    def get_mj_dataset(self,in_file_name, label, jet_mass= "JetPuppiSDsubjet0mass" ): 

      if options.usePuppiSD or options.useDDT or options.useN2DDT: 
        jet_mass="JetPuppiSDsubjet0mass"
      
      print "Using mass variable " ,jet_mass
    
      fileIn_name = TString(self.file_Directory+in_file_name)
      
      print "Using file " ,fileIn_name
      
      fileIn      = TFile(fileIn_name.Data())
      treeIn      = fileIn.Get("TTreeSemiLeptSkim")
      treeIn2      = fileIn.Get("TTreeWeights")
      treeIn.AddFriend(treeIn2)
      
      rrv_mass_j = self.workspace4fit_.var("rrv_mass_j")
      rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,10000000.)

      # Mj dataset before tau2tau1 cut : Passed
      rdataset_mj     = RooDataSet("rdataset"     +label+"_"+self.channel+"_mj","rdataset"    +label+"_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) )
      rdataset4fit_mj = RooDataSet("rdataset4fit" +label+"_"+self.channel+"_mj","rdataset4fit"+label+"_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) )
      rrv_number_pass = RooRealVar("rrv_number_ttbar"+label+"_passtau2tau1cut_em_mj","rrv_number_ttbar"+label+"_passtau2tau1cut_em_mj",0.,10000000.) #LUCA
  
      # Mj dataset before tau2tau1 cut : Total
      rdataset_beforetau2tau1cut_mj     = RooDataSet("rdataset"     +label+"_beforetau2tau1cut_"+self.channel+"_mj","rdataset"    +label+"_beforetau2tau1cut_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) )
      rdataset4fit_beforetau2tau1cut_mj = RooDataSet("rdataset4fit" +label+"_beforetau2tau1cut_"+self.channel+"_mj","rdataset4fit"+label+"_beforetau2tau1cut_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) )
      rrv_number_before = RooRealVar("rrv_number_ttbar"+label+"_beforetau2tau1cut_em_mj","rrv_number_ttbar"+label+"_beforetau2tau1cut_em_mj",0.,10000000.) #LUCA
 
      ### Mj dataset failed tau2tau1 cut :
      rdataset_failSubjetTau21cut_mj     = RooDataSet("rdataset"     +label+"_failSubjetTau21cut_"+self.channel+"_mj","rdataset"    +label+"_failSubjetTau21cut_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) )
      rdataset4fit_failSubjetTau21cut_mj = RooDataSet("rdataset4fit" +label+"_failSubjetTau21cut_"+self.channel+"_mj","rdataset4fit"+label+"_failSubjetTau21cut_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) )
      rrv_number_fail = RooRealVar("rrv_number_ttbar"+label+"_failSubjetTau21cut_em_mj","rrv_number_ttbar"+label+"_failSubjetTau21cut_em_mj",0.,10000000.) #LUCA

      ### Mj dataset extreme failed tau2tau1 cut: > 0.75
      rdataset_extremefailSubjetTau21cut_mj     = RooDataSet("rdataset"    +label+"_extremefailSubjetTau21cut_"+self.channel+"_mj","rdataset"     +label+"_extremefailSubjetTau21cut_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) )
      rdataset4fit_extremefailSubjetTau21cut_mj = RooDataSet("rdataset4fit"+label+"_extremefailSubjetTau21cut_"+self.channel+"_mj","rdataset4fit" +label+"_extremefailSubjetTau21cut_"+self.channel+"_mj",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight) )
      rrv_number_extremefail = RooRealVar("rrv_number_ttbar"+label+"_extremefailSubjetTau21cut_em_mj","rrv_number_ttbar"+label+"_extremefailSubjetTau21cut_em_mj",0.,10000000.) #LUCA
      
      # category_cut = RooCategory("category_cut"+"_"+self.channel,"category_cut"+"_"+self.channel) #---->Think this can be removed!!!!
 #      category_cut.defineType("cut",1)
 #      category_cut.defineType("beforecut",2)
 #      combData4cut = RooDataSet("combData4cut"+"_"+self.channel,"combData4cut"+"_"+self.channel,RooArgSet(rrv_mass_j, category_cut, rrv_weight),RooFit.WeightVar(rrv_weight) )
      
      
      # Define categories
      if self.workspace4fit_.cat("category_p_f"+"_"+self.channel):
        category_p_f = self.workspace4fit_.cat("category_p_f"+"_"+self.channel)
      else:
        category_p_f = RooCategory("category_p_f"+"_"+self.channel,"category_p_f"+"_"+self.channel)
        category_p_f.defineType("pass")
        category_p_f.defineType("fail")
        getattr(self.workspace4fit_,"import")(category_p_f)
      
      combData_p_f = RooDataSet("combData_p_f"+label+"_"+self.channel,"combData_p_f"+label+"_"+self.channel,RooArgSet(rrv_mass_j, category_p_f, rrv_weight),RooFit.WeightVar(rrv_weight))
      
      print "N entries: ", treeIn.GetEntries()
      
      hnum_4region                    = TH1D("hnum_4region"       +label+"_"+self.channel,"hnum_4region"        +label+"_"+self.channel,4, -1.5, 2.5) # m_j -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total
      hnum_4region_error2             = TH1D("hnum_4region_error2"+label+"_"+self.channel,"hnum_4region_error2" +label+"_"+self.channel,4, -1.5, 2.5) # m_j -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total

      hnum_4region_before_cut         = TH1D("hnum_4region_before_cut"        +label+"_"+self.channel,"hnum_4region_before_cut"       +label+"_"+self.channel,4,-1.5,2.5);# m_j -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total
      hnum_4region_before_cut_error2  = TH1D("hnum_4region_before_cut_error2" +label+"_"+self.channel,"hnum_4region_before_cut_error2"+label+"_"+self.channel,4,-1.5,2.5);# m_j -1: sb_lo; 0:signal_region; 1: sb_hi; 2:total

      hnum_2region                    = TH1D("hnum_2region"       +label+"_"+self.channel,"hnum_2region"        +label+"_"+self.channel,2,-0.5,1.5);# m_lvj 0: signal_region; 1: total --> There is only 1 and that is SIGNAL REGION?!
      hnum_2region_error2             = TH1D("hnum_2region_error2"+label+"_"+self.channel,"hnum_2region_error2" +label+"_"+self.channel,2,-0.5,1.5);# m_lvj 0: signal_region; 1: total
      
  
      #-------------------------------------------------------------------------------------------
      # Loop over tree entries
      tmp_scale_to_lumi = 1
      i = 0
      for i in range(treeIn.GetEntries()):
          if i % 10000 == 0: print "iEntry: ",i
          treeIn.GetEntry(i)
         
          PuppiJetCorr = getattr(treeIn,"JetPuppiCorrFactor")
          
          self.ak8PuppiSDJetP4_Subjet0 = ROOT.TLorentzVector()
          self.ak8PuppiSDJetP4_Subjet0.SetPtEtaPhiM( getattr(treeIn,"JetPuppiSDsubjet0pt"),
                                                     getattr(treeIn,"JetPuppiSDsubjet0eta"), 
                                                     getattr(treeIn,"JetPuppiSDsubjet0phi"), 
                                                     getattr(treeIn,"JetPuppiSDsubjet0mass")  )
                                                     
          self.ak8PuppiSDJetP4_Subjet0Raw =   self.ak8PuppiSDJetP4_Subjet0 
          self.ak8PuppiSDJetP4_Subjet0 =   self.ak8PuppiSDJetP4_Subjet0  * PuppiJetCorr
          self.ak8subjet0PuppiSD_m = self.ak8PuppiSDJetP4_Subjet0.M()


          self.ak8PuppiSDJetP4_Subjet1 = ROOT.TLorentzVector()
          self.ak8PuppiSDJetP4_Subjet1.SetPtEtaPhiM( getattr(treeIn,"JetPuppiSDsubjet1pt"),
                                                     getattr(treeIn,"JetPuppiSDsubjet1eta"), 
                                                     getattr(treeIn,"JetPuppiSDsubjet1phi"), 
                                                     getattr(treeIn,"JetPuppiSDsubjet1mass")  )
          self.ak8PuppiSDJetP4_Subjet1Raw =   self.ak8PuppiSDJetP4_Subjet1 
          self.ak8PuppiSDJetP4_Subjet1 =   self.ak8PuppiSDJetP4_Subjet1 * PuppiJetCorr
          self.ak8subjet1PuppiSD_m = self.ak8PuppiSDJetP4_Subjet1.M()


          self.ak8PuppiSDJetP4Raw =  self.ak8PuppiSDJetP4_Subjet0Raw +  self.ak8PuppiSDJetP4_Subjet1Raw
          #self.ak8PuppiSDJetP4Raw =   self.ak8PuppiSDJetP4
          self.ak8PuppiSDJetP4 =   self.ak8PuppiSDJetP4Raw * PuppiJetCorr
            
          self.ak8PuppiSD_m  = float(self.ak8PuppiSDJetP4.M())       
          fatjetTau32 = getattr(treeIn, "JetPuppiTau32")
          
          self.ptRelLepAK4 = getattr(treeIn,"PtRel"),
          self.dRLepAK4 = getattr(treeIn,"AK4_dRminLep_dRlep")
          ### Top mass window cut
          
          if  not ( 105. <= self.ak8PuppiSD_m <= 250.) : continue

          ### Top tag loose n-subjettiness cut

          if  not ( fatjetTau32 < 0.8 ) : continue

          ### 2-D Cut to reduced QCD contamination
          if not ( self.ptRelLepAK4 > 30. or self.dRLepAK4 > 0.4 ): continue

          ### Wtag mass window cut
          #if  not ( 10. <=  self.ak8subjet0PuppiSD_m <= 140.) : continue

          ### Pick our W candidate from the 2 subjets. Higher mass /lower B disc than the b candidate
          self.subjet0isW = False
          self.subjet1isW = False

          ### Throw away events where subjets are too light
          #if (self.ak8PuppiSDJetP4_Subjet0.M() and self.ak8PuppiSDJetP4_Subjet1.M()) < 10. : continue

          ### Decide on how W candidate subjet is picked
          self.whighMass =  True
          self.wlowBdisc =  False
          ### Pick the most massive as the W candidate
          if self.whighMass:
            if (self.ak8PuppiSDJetP4_Subjet0.M() > self.ak8PuppiSDJetP4_Subjet1.M()) :
              self.subjet0isW   = True
              self.countWisSJ0 += 1
            else:  
              self.subjet1isW   = True
              self.countWisSJ1 += 1
      
          ### NOTE: Next testing option of SJ with lowest b disc being W candidate, see below.

          SJ0tau1 = getattr(treeIn,"JetPuppiSDsubjet0tau1")  
          SJ0tau2 = getattr(treeIn,"JetPuppiSDsubjet0tau2")
          SJ1tau1 = getattr(treeIn,"JetPuppiSDsubjet1tau1") 
          SJ1tau2 = getattr(treeIn,"JetPuppiSDsubjet1tau2")

       #if fatjet0Mass < 210. : print"Fat jet mass is {0:2.2f} and tau32 is {1:2.2f} and SD subjet 0 mass is {2:2.2f} and tau1{3:2.2f} and tau2 {4:2.2f} and SJ pt {5:2.2f}".format(fatjet0Mass, fatjetTau32, subjet0Mass, SJtau1 , SJtau2, subjet0Pt)
          wtagger  = 0.
          SJ0tau21 = 0.
          SJ1tau21 = 0.
          if SJ0tau1 >= 0.1 :
            SJ0tau21 = SJ0tau2/ SJ0tau1
          else:
            SJ0tau21 = 10.

          if SJ1tau1 >= 0.1 :
            SJ1tau21 = SJ1tau2/ SJ1tau1
          else:
            SJ1tau21 = 10.

          ### Count instances where W candidate has higher mass and lower bdisc 
          
          SJ0Bdisc = getattr(treeIn,"JetPuppiSDsubjet0bdisc")
          SJ1Bdisc = getattr(treeIn,"JetPuppiSDsubjet1bdisc")

          ### Pick the lowest Bdisc as the W candidate
          if self.wlowBdisc :                                                                                                                                                          
            if SJ0Bdisc < SJ1Bdisc :                                                                                                                           
              self.subjet0isW   = True                                                                                                                                                                          
              self.countWisSJ0 += 1                                                                                                                                                                             
            else:                                                                                                                                                                                               
              self.subjet1isW   = True                                                                                                                                                                          
              self.countWisSJ1 += 1  

          if   self.subjet0isW and  SJ0tau21 < 10:
              wtagger = SJ0tau21
          elif self.subjet1isW and  SJ1tau21 < 10:
              wtagger = SJ1tau21
          else :
              wtagger = 10.

          #if wtagger == 10. : continue

          ### Count instances where W candidate has higher mass and higher bdisc 
          if self.subjet0isW :
            if SJ0Bdisc > SJ1Bdisc :
              self.countWhighMassandBdisc +=1
            if SJ0Bdisc < SJ1Bdisc :
              self.countWhighMassLowBdisc +=1
          elif self.subjet1isW :
            if SJ0Bdisc < SJ1Bdisc :
              self.countWhighMassandBdisc +=1
            if SJ0Bdisc > SJ1Bdisc :
              self.countWhighMassLowBdisc +=1

          #print"W candidate(higher mass subjet) has higher Bdisc than b candidate"

          #if fatjet0Mass < 210. : print"Fat jet mass is {0:2.2f} and tau32 is {1:2.2f} and SD subjet 0 mass is {2:2.2f}".format(fatjet0Mass, fatjetTau32, subjet0Mass)
          #if self.ak8subjet0PuppiSD_m > 50. : print"Fat jet SD subjet 0 mass is {0:2.2f} ,tau21 is {1:2.2f}, pt is {2:2.2f}".format( self.ak8PuppiSD_m , wtagger,  self.ak8PuppiSDJetP4_Subjet0.Perp() )

          ### Gen matching for ttbar only

          isRealW = None
          isFakeW = None
          #if (getattr(treeIn,"JetGenMatched_DeltaR_pup0_Wd1") > 0.40) or  (getattr(treeIn,"JetGenMatched_DeltaR_pup0_Wd2") > 0.4) or 
          if self.subjet0isW :
            if (getattr(treeIn,"JetGenMatched_DeltaR_pup0_Wd1") < 0.4)  and  (getattr(treeIn,"JetGenMatched_DeltaR_pup0_Wd2") < 0.4)  and  min(getattr(treeIn,"JetGenMatched_DeltaR_pup1_Wd2"), getattr(treeIn,"JetGenMatched_DeltaR_pup1_Wd1")) > 0.5  :
            #if (getattr(treeIn,"JetGenMatched_DeltaR_pup0_Wd1") < getattr(treeIn,"JetGenMatched_DeltaR_pup0_b"))  and  (getattr(treeIn,"JetGenMatched_DeltaR_pup0_Wd2") < getattr(treeIn,"JetGenMatched_DeltaR_pup0_b")) :
              isRealW = 1
              isFakeW = 0
            else:
              isRealW = 0
              isFakeW = 1
          elif self.subjet1isW :
            if (getattr(treeIn,"JetGenMatched_DeltaR_pup1_Wd1") < 0.4)  and  (getattr(treeIn,"JetGenMatched_DeltaR_pup1_Wd2") < 0.4)  and  min(getattr(treeIn,"JetGenMatched_DeltaR_pup0_Wd2"), getattr(treeIn,"JetGenMatched_DeltaR_pup0_Wd1")) > 0.5  :
            #if (getattr(treeIn,"JetGenMatched_DeltaR_pup1_Wd1") < getattr(treeIn,"JetGenMatched_DeltaR_pup1_b"))  and  (getattr(treeIn,"JetGenMatched_DeltaR_pup1_Wd2") < getattr(treeIn,"JetGenMatched_DeltaR_pup1_b")) :  
              isRealW = 1
              isFakeW = 0
            else:
              isRealW = 0
              isFakeW = 1
          ### See how many gen matched Ws pass and fail the tau21 cut

          if  isRealW == 1 :
            if wtagger >= options.tau2tau1cutHP :
              #print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
              #print"A Gen Matched W (RealW) Failed the HP tau21 cut"
              #print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
              self.countRealWsInFail += 1
            else :
              #print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"                                                              
              #print"A Gen Matched W (RealW) Passed the HP tau21 cut"                                                              
              #print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"                                                              
              self.countRealWsInPass += 1
          else  :
            if wtagger >= options.tau2tau1cutHP :
              #print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"  
              #print"A Un Matched W (FakeW) Failed the HP tau21 cut"  
              #print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"  
              self.countFakeWsInFail += 1
            else :
              #print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"                                                              
              #print"A Un Matched W (FakeW) Passed the HP tau21 cut"                                                               
              #print"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"                                                              
              self.countFakeWsInPass += 1

          if TString(label).Contains("ealW") and isRealW != 1 :
            continue
          if TString(label).Contains("akeW") and isFakeW != 1 :
            continue
 
          ### Require that one of the subjets be b-tagged use CSVv2 medium WP 0.8484
          if not (  max(SJ0Bdisc, SJ1Bdisc) > 0.8484 ) : continue

          if options.useDDT:
            if (getattr(treeIn,"JetPuppiSDsubjet0tau1") >= 0.1) and (getattr(treeIn,"JetPuppiSDsubjet0pt") >= 0.1) :
              wtagger = getattr(treeIn,"JetPuppiSDsubjet0tau2")/getattr(treeIn,"JetPuppiSDsubjet0tau1")+ (0.063 * TMath.log( (pow( getattr(treeIn,"JetPuppiSDsubjet0mass"),2))/getattr(treeIn,"JetPuppiSDsubjet0pt") ))        
            else : wtagger = 10.
          discriminantCut = 0
          if wtagger <= options.tau2tau1cutHP: # HP
              discriminantCut = 2
          elif wtagger > options.tau2tau1cutHP and wtagger <= options.tau2tau1cutLP: #LP
              discriminantCut = 1
          elif wtagger > options.tau2tau1cutLP: # Extreme fail
              discriminantCut = 0
          
          if self.subjet0isW :   
            tmp_jet_mass = self.ak8subjet0PuppiSD_m
          if self.subjet1isW:
            tmp_jet_mass = self.ak8subjet1PuppiSD_m          

          ### Choose which pt bin to plot                                                                                           
          if self.subjet0isW :
            if not (options.ptbinmin <= self.ak8PuppiSDJetP4_Subjet0.Perp() <= options.ptbinmax ): continue
          elif self.subjet1isW :
            if not (options.ptbinmin <= self.ak8PuppiSDJetP4_Subjet1.Perp() <= options.ptbinmax ): continue
          
          if i==0: 
            tmp_scale_to_lumi =  getattr(treeIn2,"SemiLeptLumiweight")  ## weigth for xs and lumi
          #print "TString(label). {}".format(TString(label))
          if not TString(label).Contains("data"):
            tmp_event_weight     =  getattr(treeIn2,"SemiLeptLumiweight") * getattr(treeIn2,"SemiLeptAllotherweights")
            tmp_event_weight4fit =  tmp_event_weight 
            #print"WEIGHT:::  tmp_event_weight4fit {0:2.2f} ".format( tmp_event_weight4fit )
            
          else:
            tmp_scale_to_lumi = 1.
            tmp_event_weight = 1.
            tmp_event_weight4fit = 1.

          
#          if options.fitTT:
#            tmp_event_weight4fit = 1.
                   

          #  HP category
          if discriminantCut == 2  and tmp_jet_mass > rrv_mass_j.getMin() and tmp_jet_mass < rrv_mass_j.getMax():   
             rrv_mass_j.setVal(tmp_jet_mass)
             
             rdataset_mj    .add(RooArgSet(rrv_mass_j), tmp_event_weight)
             rdataset4fit_mj.add(RooArgSet(rrv_mass_j), tmp_event_weight4fit)

             if tmp_jet_mass >= self.mj_sideband_lo_min and tmp_jet_mass < self.mj_sideband_lo_max:
                 hnum_4region.Fill(-1,tmp_event_weight )
                 
             if tmp_jet_mass >= self.mj_signal_min and tmp_jet_mass < self.mj_signal_max:
                 # hnum_2region.Fill(1,tmp_event_weight)
                 hnum_4region.Fill(0,tmp_event_weight)
                 hnum_4region_error2.Fill(0,tmp_event_weight*tmp_event_weight)
             if tmp_jet_mass >= self.mj_sideband_hi_min and tmp_jet_mass < self.mj_sideband_hi_max:
                 hnum_4region.Fill(1,tmp_event_weight)

             hnum_4region.Fill(2,tmp_event_weight) 
             
             category_p_f.setLabel("pass")
             combData_p_f.add(RooArgSet(rrv_mass_j,category_p_f),tmp_event_weight)
          
          # TOTAL category (no Tau21 )
          if discriminantCut == 2 or discriminantCut == 1 or discriminantCut == 0 and (rrv_mass_j.getMin() < tmp_jet_mass < rrv_mass_j.getMax()):   

              rrv_mass_j.setVal(tmp_jet_mass)

              if tmp_jet_mass >= self.mj_signal_min and tmp_jet_mass <self.mj_signal_max :
                 hnum_4region_before_cut.Fill(0,tmp_event_weight)
                 hnum_4region_before_cut_error2.Fill(0,tmp_event_weight*tmp_event_weight)

              rdataset_beforetau2tau1cut_mj.add(RooArgSet(rrv_mass_j),tmp_event_weight)
              rdataset4fit_beforetau2tau1cut_mj.add(RooArgSet(rrv_mass_j),tmp_event_weight4fit)
          
          # 1 minus HP category (LP+extreme fail)   
          if (discriminantCut==1 or discriminantCut==0) and (rrv_mass_j.getMin() < tmp_jet_mass < rrv_mass_j.getMax()):
  
              rrv_mass_j.setVal(tmp_jet_mass)

              rdataset_failSubjetTau21cut_mj     .add(RooArgSet(rrv_mass_j), tmp_event_weight)
              rdataset4fit_failSubjetTau21cut_mj .add(RooArgSet(rrv_mass_j), tmp_event_weight4fit )
    
              category_p_f.setLabel("fail");
              combData_p_f.add(RooArgSet(rrv_mass_j,category_p_f),tmp_event_weight)
           #-------------------------------------------------------------------------------------------
           # Extreme fail category (Tau21 > LP_max)   
          if discriminantCut==0 and (rrv_mass_j.getMin() < tmp_jet_mass < rrv_mass_j.getMax()):

            rdataset_extremefailSubjetTau21cut_mj     .add(RooArgSet(rrv_mass_j), tmp_event_weight)
            rdataset4fit_extremefailSubjetTau21cut_mj .add(RooArgSet(rrv_mass_j), tmp_event_weight4fit )

      #print "THIS IS WHERE??"
      print label
      print "rrv_scale_to_lumi"+label+"_"                       +self.channel
      rrv_scale_to_lumi                        = RooRealVar("rrv_scale_to_lumi"+label+"_"                       +self.channel,"rrv_scale_to_lumi"+label+"_"                       +self.channel,tmp_scale_to_lumi)
      rrv_scale_to_lumi_failSubjetTau21cut        = RooRealVar("rrv_scale_to_lumi"+label+"_failSubjetTau21cut_"       +self.channel,"rrv_scale_to_lumi"+label+"_failSubjetTau21cut_"       +self.channel,tmp_scale_to_lumi)
      rrv_scale_to_lumi_extremefailSubjetTau21cut = RooRealVar("rrv_scale_to_lumi"+label+"_extremefailSubjetTau21cut_"+self.channel,"rrv_scale_to_lumi"+label+"_extremefailSubjetTau21cut_"+self.channel,tmp_scale_to_lumi)
      
      getattr(self.workspace4fit_,"import")(rrv_scale_to_lumi)
      getattr(self.workspace4fit_,"import")(rrv_scale_to_lumi_failSubjetTau21cut)
      getattr(self.workspace4fit_,"import")(rrv_scale_to_lumi_extremefailSubjetTau21cut)
        
      rrv_number_pass.setVal(rdataset_mj.sumEntries())
      rrv_number_pass.setError(TMath.Sqrt(rdataset_mj.sumEntries()))
      # rrv_number_pass.Print()
      rrv_number_before.setVal(rdataset_beforetau2tau1cut_mj.sumEntries()) 
      rrv_number_before.setError(TMath.Sqrt(rdataset_beforetau2tau1cut_mj.sumEntries())) 
      # rrv_number_before.Print()
      rrv_number_fail.setVal(rdataset_failSubjetTau21cut_mj.sumEntries())
      rrv_number_fail.setError(TMath.Sqrt(rdataset_failSubjetTau21cut_mj.sumEntries()))
      # rrv_number_fail.Print()
      rrv_number_extremefail.setVal(rdataset_extremefailSubjetTau21cut_mj.sumEntries())
      rrv_number_extremefail.setError(TMath.Sqrt(rdataset_extremefailSubjetTau21cut_mj.sumEntries()))
      # rrv_number_extremefail.Print()
 
      getattr(self.workspace4fit_,"import")(rrv_number_pass)
      getattr(self.workspace4fit_,"import")(rrv_number_before)
      getattr(self.workspace4fit_,"import")(rrv_number_fail)
      getattr(self.workspace4fit_,"import")(rrv_number_extremefail)

      #prepare m_j dataset
      rrv_number_dataset_sb_lo_mj                 = RooRealVar("rrv_number_dataset_sb_lo"               +label+"_"+self.channel+"_mj","rrv_number_dataset_sb_lo"                +label+"_"+self.channel+"_mj",hnum_4region.GetBinContent(1))
      rrv_number_dataset_signal_region_mj         = RooRealVar("rrv_number_dataset_signal_region"       +label+"_"+self.channel+"_mj","rrv_number_dataset_signal_region"        +label+"_"+self.channel+"_mj",hnum_4region.GetBinContent(2))
      rrv_number_dataset_signal_region_error2_mj  = RooRealVar("rrv_number_dataset_signal_region_error2"+label+"_"+self.channel+"_mj","rrv_number_dataset_signal_region_error2" +label+"_"+self.channel+"_mj",hnum_4region_error2.GetBinContent(2))

      rrv_number_dataset_signal_region_before_cut_mj        = RooRealVar("rrv_number_dataset_signal_region_before_cut"        +label+"_"+self.channel+"_mj","rrv_number_dataset_signal_region_before_cut"       +label+"_"+self.channel+"_mj",hnum_4region_before_cut.GetBinContent(2))
      rrv_number_dataset_signal_region_before_cut_error2_mj = RooRealVar("rrv_number_dataset_signal_region_before_cut_error2" +label+"_"+self.channel+"_mj","rrv_number_dataset_signal_region_before_cut_error2"+label+"_"+self.channel+"_mj",hnum_4region_before_cut_error2.GetBinContent(2))
      rrv_number_dataset_sb_hi_mj                           = RooRealVar("rrv_number_dataset_sb_hi"                           +label+"_"+self.channel+"_mj","rrv_number_dataset_sb_hi"                          +label+"_"+self.channel+"_mj",hnum_4region.GetBinContent(3))

      getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_lo_mj)
      getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_mj)
      getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_error2_mj)
      getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_before_cut_mj)
      getattr(self.workspace4fit_,"import")(rrv_number_dataset_signal_region_before_cut_error2_mj)
      getattr(self.workspace4fit_,"import")(rrv_number_dataset_sb_hi_mj)
      getattr(self.workspace4fit_,"import")(combData_p_f)

      print "N_rdataset_mj: "
      getattr(self.workspace4fit_,"import")(rdataset_mj)
      getattr(self.workspace4fit_,"import")(rdataset4fit_mj)
      getattr(self.workspace4fit_,"import")(rdataset_beforetau2tau1cut_mj)
      getattr(self.workspace4fit_,"import")(rdataset4fit_beforetau2tau1cut_mj)
      getattr(self.workspace4fit_,"import")(rdataset_failSubjetTau21cut_mj)
      getattr(self.workspace4fit_,"import")(rdataset4fit_failSubjetTau21cut_mj)
      getattr(self.workspace4fit_,"import")(rdataset_extremefailSubjetTau21cut_mj)
      getattr(self.workspace4fit_,"import")(rdataset4fit_extremefailSubjetTau21cut_mj)

      rdataset_mj.Print()
      rdataset4fit_mj.Print()
      rdataset_failSubjetTau21cut_mj.Print()
      rdataset4fit_failSubjetTau21cut_mj.Print()
      rdataset_extremefailSubjetTau21cut_mj.Print()
      rdataset4fit_extremefailSubjetTau21cut_mj.Print()
      rrv_number_dataset_sb_lo_mj.Print()
      rrv_number_dataset_signal_region_mj.Print()
      rrv_number_dataset_signal_region_error2_mj.Print()
      rrv_number_dataset_signal_region_before_cut_mj.Print()
      rrv_number_dataset_signal_region_before_cut_error2_mj.Print()
      rrv_number_dataset_sb_hi_mj.Print()

      rdataset_mj.Print()
      rdataset_beforetau2tau1cut_mj.Print()
      rdataset_failSubjetTau21cut_mj.Print()
      rdataset_extremefailSubjetTau21cut_mj.Print()
      rrv_number_dataset_signal_region_mj.Print()
      rrv_number_dataset_signal_region_error2_mj.Print()
      rrv_number_dataset_signal_region_before_cut_mj.Print()
      rrv_number_dataset_signal_region_before_cut_error2_mj.Print()
      #print "WHAT!!!"
      combData_p_f.Print("v")
      

class doWtagFits():
    def __init__(self ):
        self.workspace4fit_ = RooWorkspace("workspace4fit_","workspace4fit_")                           # create workspace
        self.boostedW_fitter_em = initialiseFits("em", options.sample, 50, 140, self.workspace4fit_)    # Define all shapes to be used for Mj, define regions (SB,signal) and input files. 
        self.boostedW_fitter_em.get_datasets_fit_minor_bkg()                                            # Loop over intrees to create datasets om Mj and fit the single MCs.
       
        print "Printing workspace:"; self.workspace4fit_.Print(); print ""
        
        self.boostedW_fitter_em.get_sim_fit_components()     

        #Defining categories
        sample_type = RooCategory("sample_type","sample_type")
        sample_type.defineType("em_pass")
        sample_type.defineType("em_fail")

        #Importing fit variables
        rrv_mass_j = self.workspace4fit_.var("rrv_mass_j")
        rrv_weight = RooRealVar("rrv_weight","rrv_weight",0. ,10000000.)
        
        rdataset_data_em_mj      = self.workspace4fit_.data("rdataset_data_em_mj")
        rdataset_data_em_mj_fail = self.workspace4fit_.data("rdataset_data_failSubjetTau21cut_em_mj")

        #For binned fit (shorter computing time, more presise when no SumW2Error is used!)
        if options.doBinnedFit:
          #Converting to RooDataHist
          rdatahist_data_em_mj      = RooDataHist(rdataset_data_em_mj.binnedClone())
          rdatahist_data_em_mj_fail = RooDataHist(rdataset_data_em_mj_fail.binnedClone())

          #Converting back to RooDataSet
          rdataset_data_em_mj_2 = rdataset_data_em_mj.emptyClone()
          for i in range(0,rdatahist_data_em_mj.numEntries()):
            rdataset_data_em_mj_2.add(rdatahist_data_em_mj.get(i),rdatahist_data_em_mj.weight())

          rdataset_data_em_mj_fail_2 = rdataset_data_em_mj_fail.emptyClone()
          for i in range(0,rdatahist_data_em_mj_fail.numEntries()):
            rdataset_data_em_mj_fail_2.add(rdatahist_data_em_mj_fail.get(i),rdatahist_data_em_mj_fail.weight())

          #Combined dataset
          combData_data = RooDataSet("combData_data","combData_data",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight),RooFit.Index(sample_type),RooFit.Import("em_pass",rdataset_data_em_mj_2),RooFit.Import("em_fail",rdataset_data_em_mj_fail_2) )

        #For unbinned fit
        else:
          combData_data = RooDataSet("combData_data","combData_data",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight),RooFit.Index(sample_type),RooFit.Import("em_pass",rdataset_data_em_mj),RooFit.Import("em_fail",rdataset_data_em_mj_fail) )

        #-------------IMPORT MC-------------
        #Importing MC datasets
        rdataset_TotalMC_em_mj      = self.workspace4fit_.data("rdataset_TotalMC_em_mj")
        rdataset_TotalMC_em_mj_fail = self.workspace4fit_.data("rdataset_TotalMC_failSubjetTau21cut_em_mj")

        if options.doBinnedFit:
          #Converting to RooDataHist
          rdatahist_TotalMC_em_mj      = RooDataHist(rdataset_TotalMC_em_mj.binnedClone())
          rdatahist_TotalMC_em_mj_fail = RooDataHist(rdataset_TotalMC_em_mj_fail.binnedClone())

          #Converting back to RooDataSet
          rdataset_TotalMC_em_mj_2 = rdataset_TotalMC_em_mj.emptyClone()
          for i in range(0,rdatahist_TotalMC_em_mj.numEntries()):
            rdataset_TotalMC_em_mj_2.add(rdatahist_TotalMC_em_mj.get(i),rdatahist_TotalMC_em_mj.weight())

          rdataset_TotalMC_em_mj_fail_2 = rdataset_TotalMC_em_mj_fail.emptyClone()
          for i in range(0,rdatahist_TotalMC_em_mj_fail.numEntries()):
            rdataset_TotalMC_em_mj_fail_2.add(rdatahist_TotalMC_em_mj_fail.get(i),rdatahist_TotalMC_em_mj_fail.weight())

          #Combined MC dataset
          combData_TotalMC = RooDataSet("combData_TotalMC","combData_TotalMC",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight),RooFit.Index(sample_type),RooFit.Import("em_pass",rdataset_TotalMC_em_mj_2),RooFit.Import("em_fail",rdataset_TotalMC_em_mj_fail_2) )

        else:
         combData_TotalMC = RooDataSet("combData_TotalMC","combData_TotalMC",RooArgSet(rrv_mass_j,rrv_weight),RooFit.WeightVar(rrv_weight),RooFit.Index(sample_type),RooFit.Import("em_pass",rdataset_TotalMC_em_mj),RooFit.Import("em_fail",rdataset_TotalMC_em_mj_fail) )

        #-------------Define and perform fit to data-------------
        #Import pdf from single fits and define the simultaneous total pdf
        model_data_em      = self.workspace4fit_.pdf("model_data_em")
        model_data_fail_em = self.workspace4fit_.pdf("model_data_failSubjetTau21cut_em")

        simPdf_data = RooSimultaneous("simPdf_data_em","simPdf_data_em",sample_type)
        simPdf_data.addPdf(model_data_em,"em_pass")
        simPdf_data.addPdf(model_data_fail_em,"em_fail")

        #Import Gaussian constraints to propagate error to likelihood
        constrainslist_data_em = ROOT.std.vector(ROOT.std.string)()
        for i in range(self.boostedW_fitter_em.constrainslist_data.size()):
            constrainslist_data_em.push_back(self.boostedW_fitter_em.constrainslist_data.at(i))
            print self.boostedW_fitter_em.constrainslist_data.at(i)
        pdfconstrainslist_data_em = RooArgSet("pdfconstrainslist_data_em")
        for i in range(constrainslist_data_em.size()):
          pdfconstrainslist_data_em.add(self.workspace4fit_.pdf(constrainslist_data_em.at(i)) )
          pdfconstrainslist_data_em.Print()

        # Perform simoultaneous fit to data
        if options.doBinnedFit:
          rfresult_data = simPdf_data.fitTo(combData_data,RooFit.Save(kTRUE),RooFit.Verbose(kFALSE), RooFit.Minimizer("Minuit2"),RooFit.ExternalConstraints(pdfconstrainslist_data_em))#, RooFit.SumW2Error(kTRUE))
          rfresult_data = simPdf_data.fitTo(combData_data,RooFit.Save(kTRUE),RooFit.Verbose(kFALSE), RooFit.Minimizer("Minuit2"),RooFit.ExternalConstraints(pdfconstrainslist_data_em))#, RooFit.SumW2Error(kTRUE))
        else:
          rfresult_data = simPdf_data.fitTo(combData_data,RooFit.Save(kTRUE),RooFit.Verbose(kFALSE), RooFit.Minimizer("Minuit2"),RooFit.ExternalConstraints(pdfconstrainslist_data_em), RooFit.SumW2Error(kTRUE))
          rfresult_data = simPdf_data.fitTo(combData_data,RooFit.Save(kTRUE),RooFit.Verbose(kFALSE), RooFit.Minimizer("Minuit2"),RooFit.ExternalConstraints(pdfconstrainslist_data_em), RooFit.SumW2Error(kTRUE))

        #Draw       
        isData = True
        chi2FailData = drawFrameGetChi2(self, rrv_mass_j,rfresult_data,rdataset_data_em_mj_fail,model_data_fail_em,isData)
        chi2PassData = drawFrameGetChi2(self, rrv_mass_j,rfresult_data,rdataset_data_em_mj,model_data_em,isData)

        #Print final data fit results
        print "FIT parameters (DATA) :"; print ""
        print "CHI2 PASS = %.3f    CHI2 FAIL = %.3f" %(chi2PassData,chi2FailData)
        print ""; print rfresult_data.Print("v"); print ""

        #-------------Define and perform fit to MC-------------

        # fit TotalMC --> define the simultaneous total pdf
        model_TotalMC_em      = self.workspace4fit_.pdf("model_TotalMC_em")
        model_TotalMC_fail_em = self.workspace4fit_.pdf("model_TotalMC_failSubjetTau21cut_em")
        simPdf_TotalMC = RooSimultaneous("simPdf_TotalMC_em","simPdf_TotalMC_em",sample_type)
        simPdf_TotalMC.addPdf(model_TotalMC_em,"em_pass")
        simPdf_TotalMC.addPdf(model_TotalMC_fail_em,"em_fail")

        #Import Gaussian constraints  for fixed paramters to propagate error to likelihood
        constrainslist_TotalMC_em = ROOT.std.vector(ROOT.std.string)()
        for i in range(self.boostedW_fitter_em.constrainslist_mc.size()):
            constrainslist_TotalMC_em.push_back(self.boostedW_fitter_em.constrainslist_mc.at(i))
        pdfconstrainslist_TotalMC_em = RooArgSet("pdfconstrainslist_TotalMC_em")
        for i in range(constrainslist_TotalMC_em.size()):
          pdfconstrainslist_TotalMC_em.add(self.workspace4fit_.pdf(constrainslist_TotalMC_em[i]) )

        # Perform simoultaneous fit to MC
        if options.doBinnedFit:
          rfresult_TotalMC = simPdf_TotalMC.fitTo(combData_TotalMC,RooFit.Save(kTRUE),RooFit.Verbose(kFALSE), RooFit.Minimizer("Minuit2"),RooFit.ExternalConstraints(pdfconstrainslist_TotalMC_em))#, RooFit.SumW2Error(kTRUE))--> Removing due to unexected behaviour. See https://root.cern.ch/phpBB3/viewtopic.php?t=16917, https://root.cern.ch/phpBB3/viewtopic.php?t=16917
          rfresult_TotalMC = simPdf_TotalMC.fitTo(combData_TotalMC,RooFit.Save(kTRUE),RooFit.Verbose(kFALSE), RooFit.Minimizer("Minuit2"),RooFit.ExternalConstraints(pdfconstrainslist_TotalMC_em))#, RooFit.SumW2Error(kTRUE))        
        else:
          rfresult_TotalMC = simPdf_TotalMC.fitTo(combData_TotalMC,RooFit.Save(kTRUE),RooFit.Verbose(kFALSE), RooFit.Minimizer("Minuit2"),RooFit.ExternalConstraints(pdfconstrainslist_TotalMC_em), RooFit.SumW2Error(kTRUE))
          rfresult_TotalMC = simPdf_TotalMC.fitTo(combData_TotalMC,RooFit.Save(kTRUE),RooFit.Verbose(kFALSE), RooFit.Minimizer("Minuit2"),RooFit.ExternalConstraints(pdfconstrainslist_TotalMC_em), RooFit.SumW2Error(kTRUE))
          
        isData = False  
        chi2FailMC = drawFrameGetChi2(self,rrv_mass_j,rfresult_TotalMC,rdataset_TotalMC_em_mj_fail,model_TotalMC_fail_em,isData)
        chi2PassMC = drawFrameGetChi2(self,rrv_mass_j,rfresult_TotalMC,rdataset_TotalMC_em_mj,model_TotalMC_em,isData)
        
        #Print final MC fit results
        print "FIT Par. (MC) :"; print ""
        print "CHI2 PASS = %.3f    CHI2 FAIL = %.3f" %(chi2PassMC,chi2FailMC)
        print ""; print rfresult_TotalMC.Print("v"); print ""

        drawDataAndMC(self, rrv_mass_j,rfresult_data,rdataset_data_em_mj_fail,model_data_fail_em,True,rrv_mass_j,rfresult_TotalMC,rdataset_TotalMC_em_mj_fail,model_TotalMC_fail_em,False)

        drawDataAndMC(self, rrv_mass_j,rfresult_data,rdataset_data_em_mj,model_data_em,True,rrv_mass_j,rfresult_TotalMC,rdataset_TotalMC_em_mj,model_TotalMC_em,False)
        
        # draw the final fit results
        DrawScaleFactorTTbarControlSample(self.workspace4fit_,self.boostedW_fitter_em.color_palet,"","em",self.boostedW_fitter_em.wtagger_label,self.boostedW_fitter_em.AK8_pt_min,self.boostedW_fitter_em.AK8_pt_max,options.sample)
       
        # Get W-tagging scalefactor and efficiencies
        GetWtagScalefactors( self.workspace4fit_,self.boostedW_fitter_em)
        
        # wpForPlotting ="%.2f"%options.tau2tau1cutHP
        # wpForPlotting = wpForPlotting.replace(".","v")
        # pf=""
        # if options.usePuppiSD: pf = "_PuppiSD"
        # if options.useDDT: pf = "_PuppiSD_DDT"
        # postfix = "%s_%s" %(pf,wpForPlotting)
        # cmd =   "mv plots plots%s" %postfix
        # print cmd
        # os.system(cmd)
        # cmd =   "mv WtaggingSF.txt plots%s" %postfix
        # print cmd
        # os.system(cmd)

        self.workspace4fit_.Print()
        sys.exit()

        wout = ROOT.TFile.Open("Workspace.root","RECREATE")
        wout.cd()
        self.workspace4fit_.Write()        
        # Delete workspace
#        del self.workspace4fit_

### Start  main
if __name__ == '__main__':
    channel = options.channel ## ele, mu or ele+mu combined
    if options.fitTT:
        print "Doing fits to matched tt MC. Tree must contain branch with flag for match/no-match to generator level W!"
        doFitsToMatchedTT()
    elif options.fitMC:
        print "Doing fits to MC only"
        doFitsToMC()
    else:
        print 'Getting W-tagging scalefactor for %s sample for n-subjettiness < %.2f' %(channel,options.tau2tau1cutHP)
        getSF()

