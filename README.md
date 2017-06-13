
### How to run the W-tagging scalefactor code ###
#########################################

## installation instructions
cmsenv in CMSSW_7_4_7

setup root:

```
setenv ROOFITSYS /cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/roofit/5.34.22-cms


source /cvmfs/cms.cern.ch/slc6_amd64_gcc491/lcg/root/5.34.22-cms/bin/thisroot.csh
```
### getting the code
```
git clone https://github.com/UBParker/boostedWScalefactorProducer.git -b TreeV5 
```
### compiling
```
cd boostedWScalefactorProducer/

python Automatic_Setup.py --vclean 1#To compile
```
### running
```
python Automatic_Setup.py  #To compile
python wSubjetTagSFfits.py -b --HP 0.35 --binmin 500 --binmax -1  #To run on W candidate subjets of pt > 500 GeV
python wSubjetTagSFfits.py -b --HP 0.4 --binmin 300 --binmax 500 --fitTT #To show fits to matched and unmatched ttbar
```

The basic script to be run is 

```
python wSubjetTagSFfits.py
```
It takes as input .root files containing a TTree with a branch for the mass distribution you want to calculate a scalefactor for. This branch can contain events after full selection is applied, or new selections can be implemented on the fly in wtagSFfits.py. In addition to a data and the separate background MC files, you need one file called "*pseudodata* wchich contains all MC added together (with their appropriate weights, using ROOT hadd).

   
   General Options:
```
    -b : To run without X11 windows
    -c : channel you are using(electron,muon or electron+muon added together)
    --HP : HP working point
    --LP : LP working point
    --fitTT : Only do fits to truth matched tt MC
    --fitMC : Only do fits to MC (test fit functions)
    --sample : name of TT MC eg --sample "herwig"
    --doBinned : to do binned simultaneous fit (default is unbinned)
    --76X : Use files with postfix "_76X" (change to postfix of your choice if running on several different samples)
    --useDDT : Uses DDT tagger instead of pruning+softdrop (ops! Requires softdrop variables)
    --usePuppiSD : Uses PUPPI + softdrop and PUPPI n-subjettiness
    --useN2DDT: Uses N2DDT
    --salsetup: Different sourcing for running locally 
    --binmin: Minimum Pt of SD subjet 0 of the leading AK8 jet
    --binmax: Maximum Pt of SD subjet 0 of the leading AK8 jet
```
