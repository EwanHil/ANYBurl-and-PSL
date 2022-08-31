from classes.Dataset import get_dataset_name

class RuleImporter():
    def __init__(self, filename=f'rules/{get_dataset_name()}/alpha-100.txt'):
        self.filename = filename
        self.rules =[]
        
    def import_rules(self):
        with open(self.filename, encoding='utf-8') as rules:
            for rule in rules:
                self.rules.append(rule)  
