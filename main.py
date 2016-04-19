from pre_processing import *
from processing import *
from post_processing import *
from unit_tests.test import test




problem = Problem()
problem.import_csv('Test50.csv')
drone100 = Drone(capacity=100)
wind = Wind()
processing._clarke_and_wright_init(problem, drone100, wind)
