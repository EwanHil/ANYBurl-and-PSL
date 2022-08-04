class RuleImporter():
    def __init__(self, filename='rules/alpha-10'):
        self.filename = filename
        self.rules =[]
        
    def import_rules(self):
        with open(self.filename) as rules:
            for rule in rules:
                self.rules.append(rule)   
