import ROOT
import array as array
import numpy as np
from io import BytesIO
filelist = [
    'WtaggingSFHP0v35powheg_PuppiSDptSubjet200Toinf_ttSF0p9subjetisBmedCSV_fit50to140.txt',
    'WtaggingSFHP0v35powheg_PuppiSDptSubjet200To300_ttSF0p9subjetisBmedCSV_fit50to140.txt',
    'WtaggingSFHP0v40powheg_PuppiSDptSubjet200To300_ttSF0p9subjetisBmedCSV_fit50to140.txt',
    'WtaggingSFHP0v40powheg_PuppiSDptSubjet300To500_ttSF0p9subjetisBmedCSV_fit50to140.txt',
    'WtaggingSFHP0v40powheg_PuppiSDptSubjet500Toinf_ttSF0p9subjetisBmedCSV_fit50to140.txt',
    'WtaggingSFHP0v40powheg_PuppiSDptSubjet200Toinf_ttSF0p9subjetisBmedCSV_fit50to140.txt',
    'WtaggingSFHP0v55powheg_PuppiSDptSubjet200To300_ttSF0p9subjetisBmedCSV_fit50to140.txt',
]

SFlist = [ [],[],[]  ] 
SFerrlist =  [ [],[],[] ]
ptlist = [ [],[],[] ]


ptBs =  array.array('d', [100. ,200., 300., 500., 10000000000000000., 100000000000000000000.])
nptBs = len( ptBs) - 1
hSFs  = ROOT.TH1F("hSFs", " ;p_{T} of SD subjet 0 (GeV); # data/mc [Integral(mean+- sigma) post/pre ",  nptBs,  ptBs)

hSFsL  = ROOT.TH1F("hSFsL", " ;p_{T} of SD subjet 0 (GeV); # data/mc [Integral(mean+- sigma) post/pre ",  nptBs,  ptBs)
hSFsM  = ROOT.TH1F("hSFsM", " ;p_{T} of SD subjet 0 (GeV); # data/mc [Integral(mean+- sigma) post/pre ",  nptBs,  ptBs)
hSFsT  = ROOT.TH1F("hSFsT", " ;p_{T} of SD subjet 0 (GeV); # data/mc [Integral(mean+- sigma) post/pre ",  nptBs,  ptBs)

#W-tagging SF      : 333.896 +/- 24977542.793 
#for astring in sfStr:
#	print "astring : " + str(astring)
#        for lilstring in astring:
#            print lilstring
ifile = 0
wp = -1
for  fileis  in filelist :

    if "HP0v35" in fileis  : wp = 0 
    elif "HP0v40" in fileis  : wp= 1
    elif "HP0v55" in fileis  : wp= 2

    if "200To300" in fileis    : ptIs = 250
    elif "300To500" in fileis  : ptIs = 400
    elif "500To" in fileis : ptIs = 600
    ptlist.append(ptIs)
    with open(fileis) as f:
        lines = f.readlines()
    for n, line in enumerate(lines , 1):
        if n == 5 : 
            SFlist[wp].append( float(line[20:-50]) )
            SFerrlist[wp].append( float(line[32:-34] ))
            #print '{:2}.'.format(n), line[20:-50], line[32:-34] # line[20:-33]    #.rstrip()
    ifile +=1

print SFlist
print SFerrlist

#if wp == 0: hSFs = hSFsT
#elif wp == 1: hSFs = hSFsM
#elif wp == 2: hSFs = hSFsL
for iwp, thewp in enumerate(ptlist):
    if iwp == 0: hSFs = hSFsT
    elif iwp == 1: hSFs = hSFsM
    elif iwp == 2: hSFs = hSFsL
    for ipt, pt in enumerate( thewp ):
        ibin =  hSFs.GetXaxis().FindBin( pt )
        print "pt is {}".format(pt)
        hSFs.SetBinContent(ibin,  SFlist[iwp][ipt] )
        hSFs.SetBinError(ibin,  SFerrlist[iwp][ipt] )
        print "SF is {}".format(    SFlist[iwp][ipt] )
