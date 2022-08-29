import re
from pykeen.datasets import CoDExSmall
from classes.EntityConverter import EntityConverter

class ANYBurlToPSLConverter():
    def __init__(self, rules = []):
        self.entity_converter = EntityConverter(CoDExSmall())
        self.original_rules = rules
        self.converted_rules = self.convert_rules()      
    
    def convert_rules(self):     
        return [self.convert_rule(rule) for rule in self.original_rules]
    
    def convert_rule(self,rule):
        prediction, predicate = rule.split("<=")
        n1,n2,score,pred = prediction.split("\t")
        predicate_literals = re.findall('\(.*?\)',predicate)
        all_predicate_literal = set()
        for predicate_literal in predicate_literals:
            for p in predicate_literal.replace("(","").replace(")","").split(','):
                all_predicate_literal.add(p)

        e1,e2 = prediction[prediction.find("(")+1:prediction.find(")")].split(',') 
        all_predicate_literal.add(e1)
        all_predicate_literal.add(e2)

        for s in all_predicate_literal:
            try:
                if int(s) in self.entity_converter.entityindex_to_name:
                    predicate = predicate.replace(s,f"'{s}'")
                    pred = pred.replace(s,f"'{s}'")
                    e1 = e1.replace(s,f"'{s}'")
                    e2 = e2.replace(s,f"'{s}'")
            except ValueError:
                continue
            except TypeError:
                continue               
        return score +":" + predicate.replace(", ", " & ") + " & (" + e1 + " != " + e2 +") -> " + pred + "^2"
