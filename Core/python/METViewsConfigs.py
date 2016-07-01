import FWCore.ParameterSet.Config as cms

def get(todo):
    defs = {}

    # RecoTrackView
    defs["METView"]  = cms.PSet(
        miniView = cms.string("METView"),
        branchPrefix = cms.untracked.string("reco"),
        maxEta = cms.double(2.5),
        maxDZ  = cms.double(15),
        minPt = cms.double(10),
        pfMet = cms.InputTag("pfMet")
    )

 
    # main function
    ret = {}
    for t in todo:
        if t not in defs:
            raise Exception("miniView def not known "+t)

        ret[t] = defs[t]
    return ret


