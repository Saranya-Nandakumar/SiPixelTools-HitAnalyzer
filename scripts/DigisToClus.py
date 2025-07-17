import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_2024_cff import Run3_2024

process = cms.Process("ClusTest", Run3_2024)

# Standard services, geometry, magnetic field, and GlobalTag
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '142X_mcRun3_2025_realistic_v5', '')

# Raw-to-Digi: convert raw files into SiPixelDigis
process.load("EventFilter.SiPixelRawToDigi.SiPixelRawToDigi_cfi")
# Use rawDataCollector input (from RAW files)
process.siPixelDigis.InputLabel   = cms.InputTag('rawDataCollector')
process.siPixelDigis.IncludeErrors = cms.bool(True)
process.siPixelDigis.UsePhase1     = cms.bool(True)

# Local reconstruction (cluster & rechits)
process.load("RecoLocalTracker.Configuration.RecoLocalTracker_cff")

# Pixel cluster producer (takes SiPixelDigis)
process.siPixelClusters = cms.EDProducer(
    "SiPixelClusterProducer",
    src = cms.InputTag("siPixelDigis")
)

# Analysis module to test clusters
process.analysis = cms.EDAnalyzer(
    "PixClusterTest",
    Verbosity = cms.untracked.bool(False),
    src       = cms.InputTag("siPixelClusters")
)

# Source: point to your RAW input file(s)
#process.source = cms.Source("PoolSource",
#  fileNames = cms.untracked.vstring(
    # example RAW file
#    '/store/express/Commissioning2021/ExpressPhysics/FEVT/Express-v1/000/346/512/00000/05d4e531-3560-40bd-ba85-d18f4fa78981.root'
#  )
#)
process.load('run383631_cff')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))

# a service to use root histos
process.TFileService = cms.Service("TFileService",
    fileName = cms.string('histoClus.root')
)

# Optional output of clusters
process.o1 = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('drop *','keep *_*_*_ClusTest'),
    fileName       = cms.untracked.string('file:clus2new.root')
)

# Logging
process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring('SiPixelClusterProducer','PixClusterTest'),
    cout         = cms.untracked.PSet(threshold = cms.untracked.string('INFO'))
)

# Path: RAW -> Digi -> Clusters -> Analysis
process.p1 = cms.Path(
    process.siPixelDigis *
    process.siPixelClusters *
    process.analysis
)

# EndPath (if writing output)
process.outpath = cms.EndPath(process.o1)
