import matplotlib.pyplot as plt
import MFIS_Classes as classes
import MFIS_Read_Functions as loader

# Configuration of what to print/show
config = {
    'fuzzySets': True,
    'rules': False,
    'applications': False,
    'plot': True
}

VARS = ['Age', 'IncomeLevel', 'Assets', 'Amount', 'Job', 'History', 'Risk']
PLOT_ROWS = 2
PLOT_COLS = 4

class FuzzySetPlot:
    def __init__(self, fuzzyRisks: classes.FuzzySetsDict, fuzzyVars: classes.FuzzySetsDict):
        self.fuzzySets = fuzzyRisks
        self.fuzzySets.update(fuzzyVars)
        # self.fuzzyVars = fuzzyVars
        
        self.fig, self.axis = plt.subplots(PLOT_ROWS, PLOT_COLS)
        self.fig.subplots_adjust(bottom=0.2)
        self.axis[0][0].grid(True) 
        # self.ax.set_aspect('equal')
        

    def plot(self) -> None:
        line_styles = ['-g', '-y', '-r', '-m']
        self.graphs = [[]] * len(VARS)
        self.count = [0] * len(VARS)

        # Plots graph for each fuzzy set in the dictionary
        for fuzzySet in self.fuzzySets:
            i = VARS.index(self.fuzzySets[fuzzySet].var)
            graph = self.axis[i%PLOT_ROWS][i//PLOT_ROWS].plot(
                self.fuzzySets[fuzzySet].x, 
                self.fuzzySets[fuzzySet].y,    
                line_styles[self.count[i]]
            ),
            self.graphs[i].append(graph)
            self.count[i] += 1

        for i in range(0, 7):
            self.axis[i%PLOT_ROWS][i//PLOT_ROWS].set_xlabel(VARS[i])
            self.axis[i%PLOT_ROWS][i//PLOT_ROWS].set_ylabel("Degree of truth")

    def render(self) -> None:
        plt.show()

        
                  

if __name__ == '__main__':
    # Read
    fuzzyRisks = loader.readFuzzySetsFile('Risks.txt')
    fuzzyVars = loader.readFuzzySetsFile('InputVarSets.txt')
    rules = loader.readRulesFile()
    applications: list = loader.readApplicationsFile()


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
        fuzzyPlot = FuzzySetPlot(fuzzyRisks, fuzzyVars)
        fuzzyPlot.plot()
        fuzzyPlot.render()  

    # # Vamos a ver el primer aplicante
    # applicant = applications[0]
    # applicant.printApplication()
    # for rule in rules:
    #     rule.antecedent
        
    