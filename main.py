import matplotlib.pyplot as plt
import skfuzzy as skf
import MFIS_Classes as classes
import MFIS_Read_Functions as loader
import copy as cp

class FuzzySystem:
    def __init__(self, fuzzyRisks: classes.FuzzySetsDict, fuzzyVars: classes.FuzzySetsDict, rules: classes.RuleList, options):
        self.fuzzyRisks = fuzzyRisks
        self.fuzzyVars = fuzzyVars
        self.fuzzySets: dict = self.fuzzyRisks.copy()
        self.fuzzySets.update(fuzzyVars)

        self.rules = rules
        self.options = options

# Fuzzy methods ______________________________________________

    def inference(self, application: classes.Application) -> float:
        # No se que hacer aqui la verdad
        # computation of antecedent: max of min
        # computation of consequent: clip or scale
        # aggregation: max (union of consequents)
        # defuzzification: centroid of area, bisector, mean of max, smallest of max, largest of max

        # dict = {variable : value}
        applicationData = {}
        for variable, value in application.data:
            applicationData[variable] = value

        similarities: dict = self._compute_antencedents(applicationData)
        risks = self._compute_consequents(similarities)
        aggregation = self._aggregation(risks)

        # self.plot_aggregation(risks, aggregation)

        defuzz = self._defuzzification(aggregation)       
        return defuzz
    

    def _compute_antencedents(self, applicationData: dict) -> list[classes.Rule]:
        # Create a dictionary of similarities
        similarity = {}
        for label in self.fuzzyRisks:
            similarity[label] = []
            
        # Compute the strength of each rule
        for rule in self.rules:
            # Evaluate the strength of each antecedent of the rule
            strengths: list[float] = []
            for antecedent in rule.antecedent :
                value = applicationData[antecedent.split("=")[0]]
                if value < 0:
                    strengths.append(self.fuzzySets[antecedent].y[0])
                elif len(self.fuzzySets[antecedent].y) <= value:
                    strengths.append(self.fuzzySets[antecedent].y[-1])
                else:
                    strengths.append(self.fuzzySets[antecedent].y[value])

            # Compute the strength of the rule
            rule.strength = min(strengths)
            if rule.strength:
                label = rule.consequent
                similarity[label].append(rule.strength)  

        # Obtain the maximum strength/similarity for each consequent
        for label in similarity:
            if similarity[label]:
                similarity[label] = max(similarity[label])
            else:
                similarity[label] = 0

        return similarity


    def _compute_consequents(self, similarities: dict) -> dict:
        risks = cp.deepcopy(self.fuzzyRisks)
        method = self.options["consequents_mode"] if self.options["consequents_mode"] else 'C'

       
        if method == 'C' or method.lower() == 'clip':
            for label in risks:
                risks[label].y = [
                    min(similarities[label], risks[label].y[i]) 
                    for i in range(len(risks[label].y))
                ]
        elif method == 'S' or method.lower() == 'scale':
            for label in risks:
                risks[label].y = [
                    similarities[label] * risks[label].y[i] 
                    for i in range(len(risks[label].y))
                ]        

        return risks
    
    def _aggregation(self, consequents: dict):
        # https://pythonhosted.org/scikit-fuzzy/api/skfuzzy.html#skfuzzy.fuzzy_min
        
        fuzzySets = [consequents[label] for label in consequents]
        output = skf.fuzzy_or(fuzzySets[0].x, fuzzySets[0].y, fuzzySets[1].x, fuzzySets[1].y)
        output = skf.fuzzy_or(output[0], output[1], fuzzySets[2].x, fuzzySets[2].y)
        
        return output

    # https://pythonhosted.org/scikit-fuzzy/auto_examples/plot_defuzzify.html
    def _defuzzification(self, aggregation) -> float:
        x = aggregation[0]
        y = aggregation[1]

        method = self.options["defuzz_mode"] if self.options["defuzz_mode"] else 'centroid'
        if method.lower() == 'coa' or method.lower() == 'centroid of area':
            method = 'centroid'
        elif method.lower() == 'boa' or method.lower() == 'bisector of area':
            method = 'bisector'
        elif method.lower() == 'mean of maximum':
            method = 'mom'
        elif method.lower() == 'smallest of maximum':
            method = 'som'
        elif method.lower() == 'largest of maximum':
            method = 'lom'
        
        defuzz = skf.defuzz(x, y, method)
        return defuzz
        

# Plot methods ______________________________________________

    def plot(self) -> None:
        # Constants        
        self.VARS = ['Age', 'IncomeLevel', 'Assets', 'Amount', 'Job', 'History', 'Risk']
        self.LINE_STYLES = ['-g', '-y', '-r', '-k']
        self.PLOT_ROWS = 2
        self.PLOT_COLS = 4

        # Create plot
        self.fig, self.axis = plt.subplots(self.PLOT_ROWS, self.PLOT_COLS, figsize=(12, 5))
        self.fig.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.9, wspace=0.4, hspace=0.3)
        self.fig.suptitle("Fuzzy Sets", fontsize=16)
        # self.axis.set_aspect('equal')

        # Create special axis for Risk
        gs = self.axis[0, -1].get_gridspec()
        for ax in self.axis[0:, -1]:
            ax.remove()
        self.axRisk = self.fig.add_subplot(gs[0:, -1])

        # Create graphs data structures
        self.graphs = [[] for _ in range(len(self.VARS))]
        self.counts = [0] * len(self.VARS)
        self.labels = [[] for _ in range(len(self.VARS))]

        # Plots graph for each fuzzy set in the dictionary
        for fuzzySet in self.fuzzySets:
            i = self.VARS.index(self.fuzzySets[fuzzySet].var)
            if i == 6:
                graph = self.axRisk.plot(
                    self.fuzzySets[fuzzySet].x, 
                    self.fuzzySets[fuzzySet].y,    
                    self.LINE_STYLES[self.counts[i]],
                    label=self.fuzzySets[fuzzySet].label
                )
            else:
                graph = self.axis[i%self.PLOT_ROWS][i//self.PLOT_ROWS].plot(
                    self.fuzzySets[fuzzySet].x, 
                    self.fuzzySets[fuzzySet].y,    
                    self.LINE_STYLES[self.counts[i]],
                    label=self.fuzzySets[fuzzySet].label
                )

            self.graphs[i].append(graph)
            self.labels[i].append(self.fuzzySets[fuzzySet].label)
            self.counts[i] += 1

        # Set graph labels and legends
        for i in range(0, 6):
            ax = self.axis[i%self.PLOT_ROWS][i//self.PLOT_ROWS]
            ax.set_xlabel(self.VARS[i])
            ax.set_ylabel("Degree of truth")
            ax.legend(self.labels[i], loc='lower right', fontsize='xx-small')

        self.axRisk.set_xlabel(self.VARS[6])
        self.axRisk.set_ylabel("Degree of truth")
        self.axRisk.legend(self.labels[6], loc='lower right', fontsize='xx-small')

    def plot_aggregation(self, risks, aggregation) -> None:
        fig, ax = plt.subplots()
        # self.fig.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.9, wspace=0.4, hspace=0.3)
        # self.fig.suptitle("Fuzzy Sets", fontsize=16)
        for label in self.fuzzyRisks:
            ax.plot(self.fuzzyRisks[label].x, self.fuzzyRisks[label].y, ':m', label=self.fuzzyRisks[label].label)
        for label in risks:
            ax.plot(risks[label].x, risks[label].y, ':r', label=risks[label].label)
        ax.plot(aggregation[0], aggregation[1], '-b', label='Aggregation')
        self.render()

    def render(self) -> None:
        plt.show()

    def redraw(self) -> None:
        # algo asi
        # self.graph[i].set_ydata(...)
        plt.draw()


# Debugging ______________________________________________
    def debug(self):
        # Print fuzzy sets
        if self.options["debug"]["fuzzySets"]:
            print("_____________ Fuzzy Sets ______________\n")
            fuzzyRisks.printFuzzySetsDict()
            fuzzyVars.printFuzzySetsDict()
            
        # Print rules
        if self.options["debug"]["rules"]:
            print("_____________ Rules ______________\n")
            rules.printRuleList()

        # Read applications file
        # if self.options["debug"]["applications"]:
        #     print("_____________ Applications ______________\n")
        #     for app in applications:
        #         app.printApplication()

        # Plot fuzzy sets
        if self.options["debug"]["plot"]:
            self.plot()
            self.render()  

def write_output(filename):
    
    
    pass                 

if __name__ == '__main__':
    # Obtain
    fuzzyRisks = loader.readFuzzySetsFile('Risks.txt')
    fuzzyVars = loader.readFuzzySetsFile('InputVarSets.txt')
    rules = loader.readRulesFile()
    applications: list = loader.readApplicationsFile()
    
    fuzzySystem = FuzzySystem(fuzzyRisks, fuzzyVars, rules, options={
        "consequents_mode": "S",
        "defuzz_mode": "mom",
        "debug" : {
            'fuzzySets': False,
            'rules': False,
            'applications': False,
            'plot': False
        }
    })
    fuzzySystem.debug()

    # test
    file = open("Results.txt", "w")
    for application in applications:
        risk = fuzzySystem.inference(application)
        file.write(f"Risk value of applicant {application.appId} = {risk}\n")
    file.close()