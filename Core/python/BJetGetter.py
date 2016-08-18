import BaseGetter

class RecoMuonsGetter(BaseGetter.BaseGetter): #con il primo cerca nella cartella per un file BaseGetter.py con l'altro cerca dentro quel file una classe chiamata BaseGetter
    def __init__(self, branchPrefix):
        BaseGetter.BaseGetter.__init__(self, branchPrefix)
        #self.knownVariations = set(["_central"])
        self.knownVariations = set()

    # Note: use the most used branch (so performance wont suffer from reading otherwise unused stuff)
    def getSize(self):
        srcBranch = "bjet_p4"
        return getattr(self.chain, srcBranch).size()

