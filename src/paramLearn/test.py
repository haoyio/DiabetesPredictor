import unittest
from paramLearn import *    
from tree import *

class TestSubmission(unittest.TestCase):

    def test_paramLearn_getChildren(self):
        graph = Tree('testData.gph')
        pLearn = ParamLearn('testData.csv')
        pLearn.domains["sBP"] = [1,0]
        pLearn.domains["code280289"] = [1,0]
        node_id = 'sBP'
        node_val = '1'
        params = {'code280289': '0'}
        self.assertEquals(pLearn.getParentJointProb(node_id, node_val, params), (1.0/2.0))

    def test_nodeTree(self):
        graph = Tree('testData.gph')

        n = graph.getNode('sBP')
        self.assertEquals(n.id, 'sBP')
        self.assertEquals([p.id for p in n.getChildren()], ['weight', 'dBP'])
        self.assertEquals([p.id for p in n.getParents()], ['code280289'])

if __name__ == '__main__':
    unittest.main()