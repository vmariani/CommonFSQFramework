#include "CommonFSQFramework/Core/interface/BJetView.h"
#include <typeinfo>
#include "DataFormats/BTauReco/interface/JetTag.h"

BJetView::BJetView(const edm::ParameterSet& iConfig, TTree * tree, edm::ConsumesCollector && iC):
EventViewBase(iConfig,  tree)
{
    registerVecP4("p4", tree);

    registerVecFloat(  "discriminator", tree);

    m_inputCol = iConfig.getParameter<edm::InputTag>("jets");

    // register consumes
    iC.consumes< std::vector<reco::Track> >(m_inputCol); 
   iC.consumes< reco::JetTagCollection >(edm::InputTag("pfCombinedInclusiveSecondaryVertexV2BJetTags"));
}

void BJetView::fillSpecific(const edm::Event& iEvent, const edm::EventSetup& iSetup){
   // resetLocal();

 edm::Handle<reco::JetTagCollection> bTagHandle;
 iEvent.getByLabel("pfCombinedInclusiveSecondaryVertexV2BJetTags", bTagHandle);
 const reco::JetTagCollection & bTags = *(bTagHandle.product());

  for (unsigned int i = 0; i != bTags.size(); ++i) {
        double px = bTags[i].first->px();
        double py = bTags[i].first->py();
        double pz = bTags[i].first->pz();
        double E = px*px + py*py + pz*pz;                   
        addToP4Vec("p4", reco::Candidate::LorentzVector(px,py,pz,E));
        addToFVec("discriminator", bTags[i].second );
 
     }
    

}
