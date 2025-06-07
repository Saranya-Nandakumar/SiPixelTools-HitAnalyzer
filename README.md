# HitAnalzyer

Various codes to test pixel simHits, digis, clusters and recHits.


## Software setup

Prepare your working directory with CMSSW

```
export SCRAM_ARCH=el8_amd64_gcc12
cmsrel CMSSW_15_0_5
cd CMSSW_15_0_5/src
cmsenv
git clone https://github.com/CMSTrackerDPG/SiPixelTools-HitAnalyzer.git SiPixelTools/HitAnalyzer
scram b -j 8
cd SiPixelTools/HitAnalyzer/
```
