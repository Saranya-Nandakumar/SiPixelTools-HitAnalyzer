import FWCore.ParameterSet.Config as cms
	
from Configuration.Eras.Era_Run3_2024_cff import Run3_2024
process = cms.Process("DigiToRaw1",Run3_2024)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '142X_mcRun3_2025_realistic_v5', '')

process.load("EventFilter.SiPixelRawToDigi.SiPixelDigiToRaw_cfi")
process.load("EventFilter.SiPixelRawToDigi.SiPixelRawToDigi_cfi")

# for simultaions
process.siPixelDigis.InputLabel = 'siPixelRawData'

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100))

process.source = cms.Source("PoolSource", 
  fileNames =  cms.untracked.vstring(
  'file:step2.root'
 )
)

process.MessageLogger = cms.Service("MessageLogger",
    debugModules = cms.untracked.vstring('siPixelRawData'),
    #destinations = cms.untracked.vstring('log'),
    #log = cms.untracked.PSet( threshold = cms.untracked.string('WARNING'))
)

process.out = cms.OutputModule("PoolOutputModule",
    fileName =  cms.untracked.string('file:digitFromRaw.root'),
   outputCommands = cms.untracked.vstring("drop *","keep *_siPixelDigis_*_*")
)

process.a = cms.EDAnalyzer("PixDigisTest",
    Verbosity = cms.untracked.bool(False),
    phase1 = cms.untracked.bool(True),
    src = cms.InputTag("siPixelDigis"),
)
process.TFileService = cms.Service("TFileService",
    fileName = cms.string('digis_histos.root')
)

process.p = cms.Path(process.siPixelRawData*process.siPixelDigis*process.a)
process.ep = cms.EndPath(process.out)

