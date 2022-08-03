class ANYBurlToPSLConverter():
    def __init__(self, rules = None):
        if(rules is None):
            self.OriginalRules = []
            self.ConvertedRules = [] 
        else:
            self.OriginalRules = rules
            self.ConvertedRules = self.ConvertRules()      
    
    def ConvertRules(self):     
            return [self.ConvertANYBurlRuleToPSLRule(rule) for rule in self.OriginalRules]
    
    def ConvertANYBurlRuleToPSLRule(self,rule):
        prediction, predicate = rule.split("<=")
        n1,n2,score,pred = prediction.split("\t")
        e1,e2 = prediction[prediction.find("(")+1:prediction.find(")")].split(',')
        return score +":" + predicate.replace(", ", " & ") + " & (" + e1 + " != " + e2 +") -> " + pred + "^2"

def main():
    example_rule_list = ["19	2	0.10526315789473684	occupation(X,stage%20actor) <= member%20of(X,Phi%20Beta%20Kappa%20Society)"]
    converter = ANYBurlToPSLConverter(example_rule_list)
    
    for rule in converter.ConvertedRules:
        print(rule)

if (__name__ == '__main__'):
    main()