
### How to run the W-tagging scalefactor code ###
#########################################

## installation instructions
```
export SCRAM_ARCH=slc6_amd64_gcc491
cmsrel CMSSW_7_1_5_patch2
cd CMSSW_7_1_5_patch2/src
cmsenv

```

### getting the code

```
export GITUSER=`git config user.github`
echo "Your github username has been set to \"$GITUSER\""
git clone git@github.com:${GITUSER}/boostedWScalefactorProducer.git
cd boostedWScalefactorProducer
git remote add originalRemote git@github.com:thaarres/boostedWScalefactorProducer.git
git fetch originalRemote
git checkout -b DevelopmentBranch thaarres/DevelopmentBranch
cd $CMSSW_BASE/src
scram b distclean
scram b -j8
cd boostedWScalefactorProducer
```

### running

```
python Automatic_Setup.py
python wtagSFfit_run2exoVV.py -b
```

The basic script to be run is 

```
python wtagSFfit_run2exoVV.py
```
It takes as input .root files containing a TTree with a branch for the mass distribution you want to calculate a scalefactor for. This branch can contain events after full selection is applied, or new selections can be implemented on the fly in wtagSFfit_run2exoVV.py. In addition to a data and the separate background MC files, you need one file called "*pseudodata* wchich contains all MC added together (with their appropriate weights).

   
   General Options:
```
    -b : To run without X11 windows
    -c : channel you are using(electron,muon or electron+muon added together)
    -s : to do simoultaneous fit (true when running em channel"
    --category  : HP or LP. Obsolete, HP and LP returned together
    --HP : HP working point
    --LP : LP working point
    --fitTT : Only do fits to truth matched tt MC
    --sample : pass different TT MC eg --sample "_herwig"
```
