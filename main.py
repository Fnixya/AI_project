import MFIS_Classes as mfc
import MFIS_Read_Functions as mfr

debug = True

if __name__ == '__main__':
    # Read fuzzy sets file
    fuzzySetsDict = mfr.readFuzzySetsFile('Risks.txt')

    # Read rules file
    rules = mfr.readRulesFile()

    # Print fuzzy sets and rules
    if debug:
        fuzzySetsDict.printFuzzySetsDict()
        print("_____________ Rules ______________\n")
        rules.printRuleList()

    
    
    # Read applications file
    # applications = mfr.readApplicationsFile()
    # for app in applications:
    #     app.printApplication()
    