import FWCore.ParameterSet.Config as cms

process = cms.Process("Treemaker")

process.load("FWCore.MessageService.MessageLogger_cfi")

#process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))

process.MessageLogger.cerr.FwkReport.reportEvery = 100
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/data/Run2015C_25ns/SingleMuon/AOD/16Dec2015-v1/00000/62275A51-C5AF-E511-A27B-0CC47A4D76BE.root')
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

import CommonFSQFramework.Core.MuonTrackViewsConfigs
import CommonFSQFramework.Core.METViewsConfigs
import CommonFSQFramework.Core.VerticesViewsConfigs


process.Tree= cms.EDAnalyzer("CFFTreeProducer")
process.Tree._Parameterizable__setParameters(
        CommonFSQFramework.Core.VerticesViewsConfigs.get(["VerticesView"]))
process.Tree._Parameterizable__setParameters(
        CommonFSQFramework.Core.MuonViewsConfigs.get(["MuonView"]))
process.Tree._Parameterizable__setParameters(
        CommonFSQFramework.Core.METViewsConfigs.get(["METView"]))

process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.Tree)
