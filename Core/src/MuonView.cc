#include "CommonFSQFramework/Core/interface/MuonView.h"
#include <DataFormats/TrackReco/interface/Track.h>
#include <DataFormats/VertexReco/interface/Vertex.h>
#include "CommonFSQFramework/Core/interface/TestTrackData.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"

MuonView::MuonView(const edm::ParameterSet& iConfig, TTree * tree, edm::ConsumesCollector && iC):
EventViewBase(iConfig,  tree)
{
 registerVecP4("muons_p4", tree);
 registerVecFloat("dz", tree);
 registerVecFloat("d0", tree);
 registerVecFloat("dzErr", tree);
 registerVecFloat("d0Err", tree);
 registerVecFloat("vx", tree);
 registerVecFloat("vy", tree);
 registerVecFloat("vz", tree);

 registerVecInt(  "tight", tree);
 registerVecInt(  "loose", tree);
 registerVecInt(  "charge", tree);
 registerVecInt(  "isolation", tree);

 m_maxEta = iConfig.getParameter<double>("maxEta");
 m_minPt = iConfig.getParameter<double>("minPt");
 m_inputCol = iConfig.getParameter<edm::InputTag>("muons");
 // register consumes

 iC.consumes< std::vector<reco::BeamSpot> >(edm::InputTag("offlineBeamSpot"));
 iC.consumes< std::vector<reco::Vertex> >(edm::InputTag("offlinePrimaryVerticesWithBS"));
 iC.consumes< std::vector<reco::Muon> >(m_inputCol);  
    
}

void MuonView::fillSpecific(const edm::Event& iEvent, const edm::EventSetup& iSetup){

 edm::Handle<std::vector<reco::Vertex> > hVtx;
 iEvent.getByLabel(edm::InputTag("offlinePrimaryVerticesWithBS"), hVtx); // TODO: take from config
 reco::BeamSpot beamSpot;
 edm::Handle<reco::BeamSpot> beamSpotHandle;
 iEvent.getByLabel("offlineBeamSpot", beamSpotHandle);

 reco::Vertex primaryVertex;
 reco::Vertex primVertex_tmp;
 bool goodvertex = false;

 double bsx = 0, bsy = 0, bsz = 0;
 if ( beamSpotHandle.isValid() ){ beamSpot = *beamSpotHandle;
  bsx = beamSpot.x0();
  bsy = beamSpot.y0();
  bsz = beamSpot.z0();
 }
 GlobalPoint BeamSpotGP(bsx, bsy, bsz);

 for(unsigned int t = 0; t<hVtx->size(); t++){
  primVertex_tmp = hVtx->at(t);
  if(!primVertex_tmp.isFake() && primVertex_tmp.isValid() && primVertex_tmp.ndof() > 4 && fabs(primVertex_tmp.z()-bsz) < 10 ){
   goodvertex = true;
   primaryVertex = primVertex_tmp;
   break;
  }
 }
 if (goodvertex == false) return; // leaves empty tracks collection (filled below)
 edm::Handle<std::vector<reco::Muon> > hIn;
 iEvent.getByLabel(m_inputCol, hIn);
 float dz = 0;
 float dxy = 0;
 double px = 0, py = 0, pz = 0, E = 0, iso = 0;
 bool isTight = false;
 bool isLoose = false;
 bool isMedium = false;

 for (unsigned int i = 0; i< hIn->size();++i){
  if (hIn->at(i).pt() < m_minPt ) continue;
  if (std::abs(hIn->at(i).eta()) > m_maxEta ) continue;
  dz = hIn->at(i).globalTrack()->dz(primaryVertex.position());
  if (std::abs(dz) > m_maxDZ) continue;
  dxy = hIn->at(i).globalTrack()->dxy(primaryVertex.position() );

  px = hIn->at(i).px();
  py = hIn->at(i).py();
  pz = hIn->at(i).pz();
  E = px*px + py*py + pz*pz;
  isTight =  muon::isTightMuon(hIn->at(i), primaryVertex);
  isLoose =  muon::isLooseMuon( hIn->at(i));
  isMedium =  muon::isMediumMuon( hIn->at(i));
  if (isLoose == false) continue;
  if (isMedium == false) continue;
  // Note: all fills (below) should be done consistently after all cuts are applied
  iso = (hIn->at(i).pfIsolationR04().sumChargedHadronPt + std::max(0., hIn->at(i).pfIsolationR04().sumNeutralHadronEt + hIn->at(i).pfIsolationR04().sumPhotonEt - 0.5*hIn->at(i).pfIsolationR04().sumPUPt))/hIn->at(i).pt();
  if(isLoose == true || isMedium == true || isTight == true){  
   addToP4Vec("p4", reco::Candidate::LorentzVector(px,py,pz,E));
   addToFVec("dxy", dxy);
   addToFVec("dz", dz);
   addToFVec("dzErr", hIn->at(i).globalTrack()->dzError());
   addToFVec("d0", hIn->at(i).globalTrack()->d0());
   addToFVec("d0Err", hIn->at(i).globalTrack()->d0Error());
   addToFVec("vx", hIn->at(i).globalTrack()->vx());
   addToFVec("vy", hIn->at(i).globalTrack()->vy());
   addToFVec("vz", hIn->at(i).globalTrack()->vz());
   addToFVec("tight", isTight );
   addToFVec("loose", isLoose);
   addToFVec("charge",hIn->at(i).charge());
   addToFVec("isolation", iso);
     
  }
 }
}
