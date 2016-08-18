#ifndef BJetView_h
#define BJetView_h

#include "CommonFSQFramework/Core/interface/EventViewBase.h"

class BJetView: public EventViewBase{
    public:
       BJetView(const edm::ParameterSet& ps, TTree * tree, edm::ConsumesCollector && iC);

    private:
      virtual void fillSpecific(const edm::Event&, const edm::EventSetup&);
       edm::InputTag m_inputCol;
      void resetLocal();



};
#endif
