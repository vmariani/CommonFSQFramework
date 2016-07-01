#include "CommonFSQFramework/Core/interface/METView.h"
#include <DataFormats/TrackReco/interface/Track.h>
#include <DataFormats/VertexReco/interface/Vertex.h>
#include "CommonFSQFramework/Core/interface/TestTrackData.h"
//#include <PFMET.h>
#include <DataFormats/METReco/interface/PFMET.h>


METView::METView(const edm::ParameterSet& iConfig, TTree * tree, edm::ConsumesCollector && iC):
EventViewBase(iConfig,  tree)
{
 registerVecP4("MET_p4", tree);
 registerVecFloat("abspT", tree);

 m_maxEta = iConfig.getParameter<double>("maxEta");
 m_minPt = iConfig.getParameter<double>("minPt");
 m_inputCol = iConfig.getParameter<edm::InputTag>("pfMET");
 // register consumes
 iC.consumes< std::vector<reco::Vertex> >(edm::InputTag("offlinePrimaryVerticesWithBS"));
 iC.consumes< std::vector<reco::PFMET> >(m_inputCol);  
    
}
void METView::fillSpecific(const edm::Event& iEvent, const edm::EventSetup& iSetup){

 edm::Handle<std::vector<reco::PFMET> > hIn;
 iEvent.getByLabel(m_inputCol, hIn);
 double px = 0, py = 0, pz = 0, E = 0, iso = 0;

 for (unsigned int i = 0; i< hIn->size();++i){
  if (hIn->at(i).pt() < m_minPt ) continue;
  if (std::abs(hIn->at(i).eta()) > m_maxEta ) continue;

  px = hIn->at(i).px();
  py = hIn->at(i).py();
  pz = hIn->at(i).pz();
  E = px*px + py*py + pz*pz;
  addToP4Vec("MET_p4", reco::Candidate::LorentzVector(px,py,pz,E));
  addToFVec("abspT", hIn->at(i).pt());
 }
}
