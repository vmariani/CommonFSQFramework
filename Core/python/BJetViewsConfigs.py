import FWCore.ParameterSet.Config as cms

def get(todo):
    defs = {}

    # RecoTrackView
    defs["BJetView"]  = cms.PSet(
        miniView = cms.string("BJetView"),
        branchPrefix = cms.untracked.string("BJets"),
        jets = cms.InputTag("pfCombinedInclusiveSecondaryVertexV2BJetTags")  
  )

 
    # main function
    ret = {}
    for t in todo:
        if t not in defs:
            raise Exception("miniView def not known "+t)

        ret[t] = defs[t]
    return ret


