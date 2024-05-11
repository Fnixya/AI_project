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


class FuzzySetPlot:
    def __init__(self, fuzzyRisks: classes.FuzzySetsDict, fuzzyVars: classes.FuzzySetsDict):
        self.fuzzySets = fuzzyRisks
        self.fuzzySets.update(fuzzyVars)

        # Constants        
        self.VARS = ['Age', 'IncomeLevel', 'Assets', 'Amount', 'Job', 'History', 'Risk']
        self.LINE_STYLES = ['-g', '-y', '-r', '-k']
        self.PLOT_ROWS = 2
        self.PLOT_COLS = 4

        # Create plot
        self.fig, self.axis = plt.subplots(self.PLOT_ROWS, self.PLOT_COLS, figsize=(12, 5))
        self.fig.subplots_adjust(left=0.1, right=0.95, bottom=0.1, top=0.9, wspace=0.4, hspace=0.3)
        self.axis[0][0].grid(True) 
        # self.axis.set_aspect('equal')

        # Create axis for Risk
        gs = self.axis[0, -1].get_gridspec()
        for ax in self.axis[0:, -1]:
            ax.remove()
        self.axRisk = self.fig.add_subplot(gs[0:, -1])

        

    def plot(self) -> None:
        self.graphs = [[] for _ in range(7)]
        self.counts = [0] * len(self.VARS)
        self.labels = [[] for _ in range(7)]

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
        
    