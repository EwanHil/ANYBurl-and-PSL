class ANYBurlToPSLConverter():
    def __init__(self, rules = None):
        if(rules is None):
            self.original_rules = []
            self.converted_rules = [] 
        else:
            self.original_rules = rules
            self.converted_rules = self.convert_rules()      
    
    def convert_rules(self):     
            return [self.covert_rule(rule) for rule in self.original_rules]
    
    def covert_rule(self,rule):
        prediction, predicate = rule.split("<=")
        n1,n2,score,pred = prediction.split("\t")
        e1,e2 = prediction[prediction.find("(")+1:prediction.find(")")].split(',')       
        return score +":" + predicate.replace(", ", " & ") + " & (" + e1 + " != " + e2 +") -> " + pred + "^2"
