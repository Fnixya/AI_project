import matplotlib.pyplot as plt
import MFIS_Classes as classes
import MFIS_Read_Functions as loader

# Configuration of what to print/show
config = {
    'fuzzySets': False,
    'rules': False,
    'applications': False,
    'plot': False
}

class FuzzySystem:
    def __init__(self, fuzzyRisks: classes.FuzzySetsDict, fuzzyVars: classes.FuzzySetsDict, rules: classes.RuleList):
        self.fuzzyRisks = fuzzyRisks
        self.fuzzyVars = fuzzyVars
        self.fuzzySets: dict = self.fuzzyRisks.copy()
        self.fuzzySets.update(fuzzyVars)

        self.rules = rules

# Fuzzy methods ______________________________________________

    def inference(self, application: classes.Application, method: str = None) -> float:
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
        consequents = self._compute_consequents(similarities)
        self._aggregation()
        return self._defuzzification(consequents, method if method else 'COA')       


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


    def _compute_consequents(self, similarities: dict, method: str = 'S') -> dict:
        if method == 'C' or method.lower() == 'clip':
            pass
        elif method == 'S' or method.lower() == 'scale':
            pass
    
    def _aggregation(self):
        pass

    def _defuzzification(self, fuzzyValues: dict, method: str = 'COA') -> float:
        if method == 'COA' or method.lower() == 'centroid of area':
            pass
        elif method == 'BOA' or method.lower() == 'bisector of area':
            pass
        elif method == 'MOM' or method.lower() == 'mean of maximum':
            pass
        elif method == 'SOM' or method.lower() == 'smallest of maximum':
            pass
        elif method == 'LOM' or method.lower() == 'largest of maximum':
            pass
        else:
            return -1



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

    def render(self) -> None:
        plt.show()

    def redraw(self) -> None:
        # algo asi
        # self.graph[i].set_ydata(...)
        plt.draw()

                  

if __name__ == '__main__':
    # Obtain
    fuzzyRisks = loader.readFuzzySetsFile('Risks.txt')
    fuzzyVars = loader.readFuzzySetsFile('InputVarSets.txt')
    rules = loader.readRulesFile()
    applications: list = loader.readApplicationsFile()
    
    fuzzySystem = FuzzySystem(fuzzyRisks, fuzzyVars, rules)


    # Print fuzzy sets
    if config["fuzzySets"]:
        print("_____________ Fuzzy Sets ______________\n")
        fuzzyRisks.printFuzzySetsDict()
        fuzzyVars.printFuzzySetsDict()
        
    # Print rules
    if config["rules"]:
        print("_____________ Rules ______________\n")
        rules.printRuleList()

    # Read applications file
    if config["applications"]:
        print("_____________ Applications ______________\n")
        for app in applications:
            app.printApplication()

    # Plot fuzzy sets
    if config["plot"]:
        fuzzySystem.plot()
        fuzzySystem.render()  

    # Vamos a ver el primer aplicante
    application = applications[0]
    application.printApplication()
    fv = fuzzySystem.inference(application)
    print(fv)