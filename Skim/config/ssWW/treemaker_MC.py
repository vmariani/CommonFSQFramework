import FWCore.ParameterSet.Config as cms

process = cms.Process("Treemaker")


process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

# Source
process.source = cms.Source("PoolSource",
   # fileNames = cms.untracked.vstring('/store/data/Run2015D/SingleMuon/AOD/16Dec2015-v1/10000/06CC1B3A-FDA7-E511-B02B-00259073E388.root')
     fileNames = cms.untracked.vstring('/store/mc/RunIISpring16DR80/WW_DoubleScattering_13TeV-pythia8/AODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/50000/54683627-2209-E611-89B9-2C768AAF879E.root')
    # fileNames = cms.untracked.vstring('/store/mc/Summer12_DR53X/WW_DoubleScattering_8TeV-pythia8/AODSIM/PU_S10_START53_V7A-v1/0000/24C8D9D4-52FC-E111-9A39-002590747DE2.root')

)

# Geometry and Detector Conditions
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_v9')
process.load("Configuration.StandardSequences.MagneticField_cff")

"""
# Jet corrections
from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.coreTools import *
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.tools.pfTools import *
from PhysicsTools.PatAlgos.cleaningLayer1.cleanPatCandidates_cff import *

process.load('JetMETCorrections.Configuration.JetCorrectionProducers_cff')
#process.load('JetMETCorrections.METPUSubtraction.mvaPFMET_leptons_data_cff')
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
process.load('CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi')
process.load('RecoJets.Configuration.RecoPFJets_cff')
process.load("RecoJets.Configuration.GenJetParticles_cff")
process.load("RecoJets.Configuration.RecoGenJets_cff")
process.load('CommonTools.ParticleFlow.pfParticleSelection_cff')

process.load("RecoJets.JetProducers.ak5PFJets_cfi")

process.ak5PFJets.doAreaFastjet = True
"""
# MET filters and corrections
process.load("RecoMET.METFilters.metFilters_cff")
process.load("JetMETCorrections.Type1MET.correctedMet_cff")
process.load("JetMETCorrections.Type1MET.correctionTermsCaloMet_cff")
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType1Type2_cff")
#process.corrPfMetType1.jetCorrLabel = cms.InputTag("ak5PFL1FastL2L3")
# process.corrPfMetType1.jetCorrLabel = cms.string("ak5PFL1FastL2L3Residual")
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0PFCandidate_cff")
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0RecoTrack_cff")

process.corrPfMetType1.jetCorrLabel = cms.InputTag("ak4PFCHSL1FastL2L3Corrector")
# process.corrPfMetShiftXY.parameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_data


# B tag process
process.load("RecoBTag.Configuration.RecoBTag_cff")

# Di muon Filter
#process.filtro = cms.EDFilter("DiMuonEventFilter")

# standard cff modue load
import CommonFSQFramework.Core.customizePAT

process = CommonFSQFramework.Core.customizePAT.customize(process)
process = CommonFSQFramework.Core.customizePAT.customizeGT(process)

process.MessageLogger.cerr.FwkReport.reportEvery = 100
# importing views
import CommonFSQFramework.Core.MuonViewsConfigs
import CommonFSQFramework.Core.BJetViewsConfigs
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
       CommonFSQFramework.Core.TriggerResultsViewsConfigs.get(["SingleMuon", "DoubleMuon"]))
process.Tree._Parameterizable__setParameters(
       CommonFSQFramework.Core.BJetViewsConfigs.get(["BJetView"]))

# ntuple processes
process.tree = cms.Sequence(
				process.metFilters + 
				process.correctionTermsPfMetType1Type2 +
				process.correctionTermsPfMetType0RecoTrack +
				process.correctionTermsPfMetType0PFCandidate +
				process.correctionTermsCaloMet +
				process.pfMetT0pcT1 *
				process.btagging *
				process.Tree)

process = CommonFSQFramework.Core.customizePAT.addTreeProducer(process, process.tree)
