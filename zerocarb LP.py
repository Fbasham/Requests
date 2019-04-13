
# Import PuLP modeler functions
from pulp import *

# Creates a list of the Ingredients
Ingredients =['EGGS', 'BEEF', 'CHEESE', 'BACON', 'CREAM']

# A dictionary of the costs of each of the Ingredients is created
costs = {'EGGS': 5,
         'BEEF': 5,
         'CHEESE': 8,
         'BACON': 7,
         'CREAM': 6}

# A dictionary of the protein percent in each of the Ingredients is created
proteinPercent = {'EGGS': 0.35,
                  'BEEF': 0.42,
                  'CHEESE': 0.26,
                  'BACON': 0.15,
                  'CREAM': 0.03}

# A dictionary of the fat percent in each of the Ingredients is created
fatPercent = {'EGGS': 0.63,
              'BEEF': 0.58,
              'CHEESE': 0.72,
              'BACON': 0.75,
              'CREAM': 0.94}

# A dictionary of the carbs percent in each of the Ingredients is created
carbPercent = {'EGGS': 0.02,
              'BEEF': 0.0,
              'CHEESE': 0.02,
              'BACON': 0.1,
              'CREAM': 0.03}

# A dictionary of the salt percent in each of the Ingredients is created
fullnessPercent = {'EGGS': 0.2,
              'BEEF': 0.85,
              'CHEESE': 0.75,
              'BACON': 0.95,
              'CREAM': 0.95}

# Create the 'prob' variable to contain the problem data
prob = pulp.LpProblem("ZeroCarb", LpMinimize)

# A dictionary called 'ingredient_vars' is created to contain the referenced Variables
ingredient_vars = LpVariable.dicts("Ingr",Ingredients)

# The objective function is added to 'prob' first
prob += lpSum([costs[i]*ingredient_vars[i] for i in Ingredients]), "Total Cost of Ingredients "

# The five constraints are added to 'prob'
prob += lpSum([ingredient_vars[i] for i in Ingredients]) == 1, "PercentagesSum"
prob += lpSum([proteinPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 0.15, "ProteinRequirement"
prob += lpSum([fatPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 0.8, "FatRequirement"
prob += lpSum([carbPercent[i] * ingredient_vars[i] for i in Ingredients]) <= 0.1, "carbRequirement"
prob += lpSum([fullnessPercent[i] * ingredient_vars[i] for i in Ingredients]) >= 1, "fullnessRequirement"

# The problem data is written to an .lp file
#prob.writeLP("ZeroCarb.lp")

# The problem is solved using PuLP's choice of Solver
prob.solve()

# The status of the solution is printed to the screen
print("Status:", LpStatus[prob.status])

# Each of the variables is printed with it's resolved optimum value
for v in prob.variables():
    print(v.name, "=", v.varValue)

# The optimised objective function value is printed to the screen
print("Total Cost of Ingredients = ", value(prob.objective))