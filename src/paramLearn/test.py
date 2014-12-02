import unittest
import paramLearn
import tree

class TestSubmission(unittest.TestCase):

    def test_one(self):
        tree = Tree('../output/train3.gph')
        pLearn = ParamLearn('../train2.csv')
        
        self.assertEquals(submission.extractWordFeatures("hello world"), {"hello":1, "world":1})
        test1 = "A duck and a boy went to the super-duper-pond a fortnight ago."
        test1_ans = {"A":1, "duck":1, "and":1, "a":2, "boy":1, "went": 1, "to":1, "the":1,\
         "super-duper-pond":1, "fortnight":1, "ago.":1}
        self.assertEquals(submission.extractWordFeatures(test1), test1_ans)
        test2 = "I am what I am"
        test2_ans = {"I":2, "am":2, "what":1}
        self.assertEquals(submission.extractWordFeatures(test2), test2_ans)



if __name__ == '__main__':
    unittest.main()