import re
from classes.EntityConverter import EntityConverter
from classes.Dataset import get_dataset

class ANYBurlToPSLConverter():
    def __init__(self, rules = []):
        self.entity_converter = EntityConverter(get_dataset())
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

        output_rule = score +":" + predicate.replace(", ", " & ") + " & (" + e1 + " != " + e2 +") -> " + pred + "^2"

        for s in all_predicate_literal:
            try:
                if int(s) in self.entity_converter.entityindex_to_name:
                    output_rule = output_rule.replace(f"({s} ",f"('{s}' ")
                    output_rule = output_rule.replace(f" {s})",f" '{s}')")
                    output_rule = output_rule.replace(f"({s},",f"('{s}',")
                    output_rule = output_rule.replace(f",{s})",f",'{s}')")
            except ValueError:
                continue
            except TypeError:
                continue               
        return output_rule
