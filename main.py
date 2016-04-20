from pre_processing import *
from processing import *
from post_processing import *
from unit_tests.test import test




problem = Problem()
problem.import_csv("Test50.csv")
wind0 = Wind(0.4, 0)
drone100 = Drone(capacity=100, speed=1, force=1)
clarke_and_wright(problem, drone100,  wind0)
print(problem.solutions_list[-1]._total_cost)
print(problem.solutions_list[-1]._total_savings)
test()
