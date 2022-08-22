class RuleImporter():
    def __init__(self, filename='rules/alpha-10.txt'):
        self.filename = filename
        self.rules =[]
        
    def import_rules(self):
        with open(self.filename, encoding='utf-8') as rules:
            for rule in rules:
                self.rules.append(rule)  
