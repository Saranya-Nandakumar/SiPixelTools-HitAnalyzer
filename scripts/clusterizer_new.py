import FWCore.ParameterSet.Config as cms
    
process = cms.Process( "TEST" )

# enable alpaka and GPU support
process.load("Configuration.StandardSequences.Accelerators_cff")

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
# load and override the CUDAService
process.load("HeterogeneousCore.CUDAServices.CUDAService_cfi")  # brings in the CUDAService with its defaults
# now bump up the printf FIFO to, say, 10 MiB
process.CUDAService.limits.cudaLimitPrintfFifoSize = cms.untracked.int32(10 * 1024 * 1024)



# reconstruct data form run 383631
process.load("run383631_cff")

# enable multithreading
#process.options.numberOfThreads = 1
#process.maxEvents.input = 10000
#process.options.numberOfStreams = 1
#process.maxEvents = cms.untracked.PSet(
#    input = cms.untracked.int32(1)
#)


# configure the global tag
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(None, globaltag = '142X_mcRun3_2025_realistic_v7')


# alpaka-based EventSetup modules
process.siPixelGainCalibrationForHLTSoAESProducer = cms.ESProducer( "SiPixelGainCalibrationForHLTSoAESProducer@alpaka",
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string( "" )
    )
)

process.siPixelCablingSoAESProducer = cms.ESProducer( "SiPixelCablingSoAESProducer@alpaka",
    CablingMapLabel = cms.string( "" ),
    UseQualityInfo = cms.bool( False ),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string( "" )
    )
)     

# alpaka-based pixel unpacker and clusterizer
process.hltSiPixelClustersSoA = cms.EDProducer( "SiPixelRawToClusterPhase1@alpaka",
    IncludeErrors = cms.bool( True ),
    UseQualityInfo = cms.bool( False ),
    clusterThreshold_layer1 = cms.int32( 4000 ),
    clusterThreshold_otherLayers = cms.int32( 4000 ),
    VCaltoElectronGain = cms.double( 1.0 ),
    VCaltoElectronGain_L1 = cms.double( 1.0 ),
    VCaltoElectronOffset = cms.double( 0.0 ),
    VCaltoElectronOffset_L1 = cms.double( 0.0 ),
    InputLabel = cms.InputTag( "rawDataCollector" ),
    Regions = cms.PSet(  ),
    DoDigiMorphing = cms.bool(False),
    CablingMapLabel = cms.string( "" ),
    alpaka = cms.untracked.PSet(
        backend = cms.untracked.string( "" )
    ),
    DigiMorphing = cms.PSet(
        kernel1 = cms.vint32(1, 1, 1, 1,1,1,1,1,1),  # Example kernel values
        kernel2 = cms.vint32(0, 1, 0, 1,1,1,0,1,1),  # Example kernel values
        )

)

# pixel cluster conversion to legacy format
process.hltSiPixelClusters = cms.EDProducer( "SiPixelDigisClustersFromSoAAlpakaPhase1",
    src = cms.InputTag( "hltSiPixelClustersSoA" ),
    clusterThreshold_layer1 = cms.int32( 4000 ),
    clusterThreshold_otherLayers = cms.int32( 4000 ),
    produceDigis = cms.bool( False ),
    storeDigis = cms.bool( False )
)

# run the pixel clusterizer
process.path = cms.Path(
    process.hltSiPixelClustersSoA +
    process.hltSiPixelClusters
)

# process up to 10300 events
#process.maxEvents.input = 1

# print a message every 100 events
#process.MessageLogger.cerr.FwkReport.reportEvery = 100

# do not print the time and trigger reports at the end of the job
process.options.wantSummary = False

process.NVProfilerService = cms.Service("NVProfilerService",
    showModulePrefetching = cms.untracked.bool(False)
)

# === 1) Define the output module ===
process.out = cms.OutputModule("PoolOutputModule",
    fileName       = cms.untracked.string("myClustersmorph.root"),
    # pick a pre-defined “event content” or roll your own:
    outputCommands = cms.untracked.vstring('keep *')
    # optionally only write events that passed your Path:
    # SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('path') )
)

# === 2) Hook it into an EndPath ===
process.endpath = cms.EndPath(process.out)

# === 3) Make sure your schedule includes both the processing Path and the EndPath ===
process.schedule = cms.Schedule(process.path, process.endpath)
