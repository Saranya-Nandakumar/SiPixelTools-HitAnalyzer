import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_2024_cff import Run3_2024

process = cms.Process("ClusTest", Run3_2024)

# First load standard services and conditions
process.load("Configuration.StandardSequences.Services_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '142X_mcRun3_2025_realistic_v5', '')

# Then load other standard sequences
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")

# Load accelerator support
process.load("Configuration.StandardSequences.Accelerators_cff")
process.load("HeterogeneousCore.CUDAServices.CUDAService_cfi")
process.CUDAService.limits.cudaLimitPrintfFifoSize = cms.untracked.int32(10 * 1024 * 1024)

# Clusterizer and reconstruction
process.load("RecoLocalTracker.Configuration.RecoLocalTracker_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

# For raw data processing
process.load("EventFilter.SiPixelRawToDigi.SiPixelDigiToRaw_cfi")
process.load("EventFilter.SiPixelRawToDigi.SiPixelRawToDigi_cfi")
process.load("RecoLocalTracker.SiPixelDigiReProducers.siPixelDigisMorphed_cfi")

# Configure the cluster producer
process.siPixelClusters = cms.EDProducer("SiPixelClusterProducer",
    src = cms.InputTag("siPixelDigisMorphed"))

# Configure the input source
#process.source = cms.Source("PoolSource", 
#    fileNames = cms.untracked.vstring(
#        'file:/p/project1/training2508/cms_digi_morphing/store/relval/CMSSW_15_0_0/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_142X_mcRun3_2025_realistic_v7_STD_2025_PU-v3/2580000/1c2caeef-e246-4b6d-bebc-4fb6df4f9bbd.root'
#    )
#)

process.load('run383631_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring('SiPixelClusterizer', 'siPixelDigisMorphed'),
    cout = cms.untracked.PSet(
        threshold = cms.untracked.string('INFO')
    )
)

process.TFileService = cms.Service("TFileService",
    fileName = cms.string('histoClusMorph.root')
)

# Analysis module
process.analysis = cms.EDAnalyzer("PixClusterTest",
    Verbosity = cms.untracked.bool(False),
    src = cms.InputTag("siPixelClusters"),
)

# Output module
process.o1 = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('drop *', 'keep *_*_*_ClusTest'),
    fileName = cms.untracked.string('file:clus2Morph.root')
)

# Processing path
process.p1 = cms.Path(
    process.siPixelRawData * 
    process.siPixelDigis * 
    process.siPixelDigisMorphed * 
    process.siPixelClusters * 
    process.analysis
)

process.outpath = cms.EndPath(process.o1)
process.schedule = cms.Schedule(process.p1, process.outpath)
