import matplotlib.pyplot as plt
import MFIS_Classes as mfc
import MFIS_Read_Functions as mfr

# Configuration of what to print/show
config = {
    'fuzzySets': False,
    'rules': False,
    'applications': True,
    'plot': True
}

class FuzzyPlot:
    def __init__(self, fuzzySetsDict: mfc.FuzzySetsDict):
        self.fuzzySetsDict = fuzzySetsDict
        
        self.fig, self.ax = plt.subplots()
        self.fig.subplots_adjust(bottom=0.2)
        self.ax.grid(True)
        # self.ax.set_aspect('equal')
        

    def plot(self) -> None:
        line_styles = ['-g', '-y', '-r']
        self.graphs = []

        # Plots graph for each fuzzy set in the dictionary
        for fuzzySet in fuzzySetsDict:
            graph = self.ax.plot(
                fuzzySetsDict[fuzzySet].x, 
                fuzzySetsDict[fuzzySet].y,    
                line_styles.pop(0)
            ),
            self.graphs.append(graph)

        
        self.ax.set_xlabel("Risk")
        self.ax.set_ylabel("Degree of truth")

    def render(self) -> None:
        plt.show()

        
                  

if __name__ == '__main__':
    # Read fuzzy sets file
    fuzzySetsDict = mfr.readFuzzySetsFile('Risks.txt')

    # Read rules file
    rules = mfr.readRulesFile()

    # Print fuzzy sets and rules
    if config["fuzzySets"]:
        print("_____________ Fuzzy Sets ______________\n")
        fuzzySetsDict.printFuzzySetsDict()
        
    if config["rules"]:
        print("_____________ Rules ______________\n")
        rules.printRuleList()

    # Read applications file
    if config["applications"]:
        applications: list = mfr.readApplicationsFile()
        for app in applications:
            app.printApplication()

    # Plot fuzzy sets
    if config["plot"]:
        fuzzyPlot = FuzzyPlot(fuzzySetsDict)
        fuzzyPlot.plot()
        fuzzyPlot.render()  
    
    