import FWCore.ParameterSet.Config as cms
	
from Configuration.Eras.Era_Run3_2024_cff import Run3_2024
process = cms.Process("DigiToRaw1",Run3_2024)

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.MagneticField_38T_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '142X_mcRun3_2025_realistic_v7', '')

process.load("EventFilter.SiPixelRawToDigi.SiPixelDigiToRaw_cfi")
process.load("EventFilter.SiPixelRawToDigi.SiPixelRawToDigi_cfi")

# for simultaions
process.siPixelDigis.InputLabel = 'siPixelRawData'

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10))

process.source = cms.Source("PoolSource", 
  fileNames =  cms.untracked.vstring(
  'file:/p/project1/training2508/cms_digi_morphing/store/relval/CMSSW_15_0_0/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_142X_mcRun3_2025_realistic_v7_STD_2025_PU-v3/2580000/1c2caeef-e246-4b6d-bebc-4fb6df4f9bbd.root'
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

