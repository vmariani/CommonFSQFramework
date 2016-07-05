import FWCore.ParameterSet.Config as cms

process = cms.Process("Treemaker")

process.load("FWCore.MessageService.MessageLogger_cfi")

#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))

process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
process.source = cms.Source("PoolSource",
   # fileNames = cms.untracked.vstring('/store/data/Run2015D/SingleMuon/AOD/16Dec2015-v1/10000/06CC1B3A-FDA7-E511-B02B-00259073E388.root')
     fileNames = cms.untracked.vstring('/store/mc/RunIISpring16DR80/WW_DoubleScattering_13TeV-pythia8/AODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/50000/54683627-2209-E611-89B9-2C768AAF879E.root')

)

# Geometry and Detector Conditions
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')
process.load("Configuration.StandardSequences.MagneticField_cff")

import CommonFSQFramework.Core.customizePAT
process = CommonFSQFramework.Core.customizePAT.customize(process)
process = CommonFSQFramework.Core.customizePAT.customizeGT(process)

import CommonFSQFramework.Core.MuonViewsConfigs
import CommonFSQFramework.Core.METViewsConfigs
import CommonFSQFramework.Core.VerticesViewsConfigs
import CommonFSQFramework.Core.GenLevelViewsConfigs
import CommonFSQFramework.Core.TriggerResultsViewsConfigs

process.Tree= cms.EDAnalyzer("CFFTreeProducer")
process.Tree._Parameterizable__setParameters(
        CommonFSQFramework.Core.VerticesViewsConfigs.get(["VerticesView"]))
process.Tree._Parameterizable__setParameters(
        CommonFSQFramework.Core.MuonViewsConfigs.get(["MuonView"]))
process.Tree._Parameterizable__setParameters(
        CommonFSQFramework.Core.METViewsConfigs.get(["METView"]))
process.Tree._Parameterizable__setParameters(
        CommonFSQFramework.Core.GenLevelViewsConfigs.get(["GenPartView"]))
process.Tree._Parameterizable__setParameters(
       CommonFSQFramework.Core.TriggerResultsViewsConfigs.get(["SingleMuon"])
)


process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.Tree)
