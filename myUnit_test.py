from pre_processing import *
from processing import *
from post_processing import *
from unit_tests.test import test
import unittest

class MyUnit_Test(unittest.TestCase):
    def setUp(self):
    # to compare two values to only 2 decimal places,
    # this avoids error due to fractions or roots are hangded as decimals
        self.wind1 = Wind(1,1)
        self.wind2 = Wind(2,2)
        self.wind3 = Wind(3,3)
        self.wind4 = Wind(4,4)
        self.wind5 = Wind(5,5)
        self.wind6 = Wind(6,6)

        self.drone100 = Drone(capacity=100)


        self.depot0 = Depot(x = 0, y = 0)
        self.depot1 = Depot(x = 1, y = 2)


        self.client1 = Client(identifier="client1", x =1 , y =1 , demand = 1)
        self.client2 = Client(identifier="client2", x =2 , y =2 , demand = 2)
        self.client3 = Client(identifier="client3", x =3 , y =3 , demand = 3)
        self.client4 = Client(identifier="client4", x =4 , y =4 , demand = 4)
        self.client5 = Client(identifier="client5", x =5 , y =5 , demand = 5)
        self.client6 = Client(identifier="client6", x =6 , y =6 , demand = 6)
        self.client7 = Client(identifier="client7", x =7 , y =7 , demand = 7)
        self.client8 = Client(identifier="client8", x =8 , y =8 , demand = 8)
        self.client9 = Client(identifier="client9", x =9 , y =9 , demand = 9)
        self.client10 = Client(identifier="client10", x =9 , y =9 , demand = 10)
        self.client11 = Client(identifier="client11", x =1 , y =1 , demand = 11)
        self.client12 = Client(identifier="client12", x =2 , y =2 , demand = 12)
        self.client13 = Client(identifier="client13", x =3 , y =3 , demand = 13)
        self.client14 = Client(identifier="client14", x =4 , y =4 , demand = 14)
        self.client15 = Client(identifier="client15", x =5 , y =5 , demand = 15)
        self.client16 = Client(identifier="client16", x =6 , y =6 , demand = 16)
        self.client17 = Client(identifier="client17", x =7 , y =7 , demand = 17)
        self.client18 = Client(identifier="client18", x =8 , y =8 , demand = 18)
        self.client19 = Client(identifier="client19", x =9 , y =9 , demand = 19)
        self.client20 = Client(identifier="client20",x =10 , y =10 , demand = 20)



        self.delivery1 = Delivery(clients_list = [self.client1, self.client10, self.client18], depot = self.depot0, drone = self.drone100, wind = self.wind1)
        self.delivery2 = Delivery(clients_list = [self.client2, self.client20, self.client17], depot = self.depot0, drone = self.drone100, wind = self.wind1)
        self.delivery3 = Delivery(clients_list = [self.client3, self.client13, self.client15], depot = self.depot0, drone = self.drone100, wind = self.wind1)
        self.delivery4 = Delivery(clients_list = [self.client10, self.client13, self.client15, self.client17, self.client19, self.client20], depot = self.depot0, drone = self.drone100, wind = self.wind1)



        self.solution1 = Solution(deliveries_list = [self.delivery1, self.delivery2, self.delivery3])


        self.problem1 = Problem(clients_list = [self.client1,
                                                self.client2,
                                                self.client3,
                                                self.client4,
                                                self.client5,
                                                self.client6,
                                                self.client7,
                                                self.client8,
                                                self.client9,
                                                self.client10,
                                                self.client11,
                                                self.client12,
                                                self.client13,
                                                self.client14,
                                                self.client15,
                                                self.client16,
                                                self.client17,
                                                self.client18,
                                                self.client19,
                                                self.client20])





    def equal2(self, a,b):
        return round(a,2)==round(b,2)

#####################
# pre_processing.py
#####################

# Q1: calculate_force_direction and calculate_xy
    def test_Wind_calculate_force_direction(self):
        wind0 = Wind(-1, -1)
        self.assertEqual(wind0.direction,45)
        # change x, and direction will be modifed accordingly
        wind0.x = 1
        self.assertEqual(wind0.direction, 315)

    def test_Wind_calculate_xy(self):
        wind = Wind()
        wind.direction = 315
        wind.force = np.sqrt(2)
        wind.calculate_xy()
        self.assertTrue(self.equal2(wind.x, 1) and self.equal2(wind.y, -1))


# Q2: cost
    def test_cost(self):
        wind042 = Wind(force=0.42, direction=337.)
        drone100 = Drone(capacity=100, speed=1.24, force=0.75)
        a = Point("a", 0, 0)
        b = Point("b", 1, 1)
        # test for both directions
        self.assertTrue(self.equal2(cost(a,b, drone100, wind042), 1.24))
        self.assertTrue(self.equal2(cost(b,a, drone100, wind042), 0.98))


# Q3: cost method in Point and Drone
    def test_Point_cost(self):
        wind042 = Wind(force=0.42, direction=337.)
        drone100 = Drone(capacity=100, speed=1.24, force=0.75)
        a = Point("a", 0, 0)
        b = Point("b", 1, 1)
        wind042.direction = 225
        self.assertTrue(self.equal2(a.cost(b, drone100, wind042), 0.70))

    def test_Drone_cost(self):
        wind042 = Wind(force=0.42, direction=337.)
        drone100 = Drone(capacity=100, speed=1.24, force=0.75)
        a = Point("a", 0, 0)
        b = Point("b", 1, 1)
        wind042.direction = 225
        self.assertTrue(self.equal2(drone100.cost(b, a, wind042), 1.4199))


# Q4: Delivery.calculate_total_demand
    def test_Delivery_calcualte_total_demand(self):
        delivery = Delivery()
        client10 = Client(identifier = 10, demand=10, x=1, y=2)
        client42 = Client(identifier = 42, demand=42, x=2, y=1)
        client18 = Client(identifier = 18, demand=18, x=3, y=1)
        clients_list_test = [client10, client42, client18]
        delivery.clients_list = clients_list_test
        delivery.calculate_total_demand()
        self.assertTrue(self.equal2(delivery.total_demand, 70))


# Q5: Delivery.calculate_total_cost
    def test_Delivery_calcualte_total_cost(self):
        drone100 = Drone(capacity=100)
        wind = Wind(-1, -1)
        delivery = Delivery(drone = drone100, wind = wind)
        client10 = Client(identifier = 10, demand=10, x=1, y=2)
        client42 = Client(identifier = 42, demand=42, x=2, y=1)
        client18 = Client(identifier = 18, demand=18, x=3, y=1)
        clients_list_test = [client10, client42, client18]
        delivery.clients_list = clients_list_test
        total_cost_by_hand = delivery.depot.cost(client10, drone100, wind) + client10.cost(client42, drone100, wind) + client42.cost(client18, drone100, wind)+client18.cost(delivery.depot, drone100, wind)
        delivery.calculate_total_cost()
        self.assertTrue(self.equal2(delivery.total_cost, total_cost_by_hand))


# Q6: Delivery.calculate_total_savings
    def test_Delivery_calcualte_total_savings(self):
        drone100 = Drone(capacity=100)
        wind = Wind(-1, -1)
        delivery = Delivery(drone = drone100, wind = wind)
        client10 = Client(identifier = 10, demand=10, x=1, y=2)
        client42 = Client(identifier = 42, demand=42, x=2, y=1)
        client18 = Client(identifier = 18, demand=18, x=3, y=1)
        clients_list_test = [client10, client42, client18]
        delivery.clients_list = clients_list_test
        cost_by_naive_method = delivery.depot.cost(client10, drone100, wind) + client10.cost(delivery.depot, drone100, wind)
        cost_by_naive_method += delivery.depot.cost(client42, drone100, wind) + client42.cost(delivery.depot, drone100, wind)
        cost_by_naive_method += delivery.depot.cost(client18, drone100, wind) + client18.cost(delivery.depot, drone100, wind)
        delivery.calculate_total_cost()
        total_savings_by_hand = cost_by_naive_method - delivery.total_cost
        delivery.calculate_total_savings()
        self.assertTrue(self.equal2(delivery.total_savings, total_savings_by_hand))


# Q7: Delivery._set_depot, Delivery._set_clients_list, Delivery._set_drone, Delivery.wind, Delivery.total_cost, Delivery.total_savings
    def test_Delivery_set_depot(self):
        delivery = Delivery()
        depot = Depot(x = 1, y = 2)
        delivery._set_depot(depot)
        self.assertEqual(depot, delivery._get_depot())

    def test_Delivery_set_client(self):
        delivery = Delivery()
        client1 = Client("dummy client", x = 10, y = 1, demand = 10)
        client2 = Client("dummy client", x = 10, y = 2, demand = 20)
        client3 = Client("dummy client", x = 10, y = 3, demand = 30)
        clients_list = [client1, client2, client3]
        delivery._set_clients_list(clients_list)
        self.assertEqual(clients_list, delivery._get_clients_list())

    def test_Delivery_set_drone(self):
        delivery = Delivery()
        drone = Drone(capacity=80)
        delivery._set_drone(drone)
        self.assertEqual(drone, delivery._get_drone())

    def test_Delivery_attribute_wind(self):
        delivery = Delivery()
        wind = Wind(direction=10)
        delivery._set_wind(wind)
        self.assertEqual(wind, delivery._get_wind())

    def test_Delivery_attribute_total_cost(self):
        delivery = Delivery()
        client1 = Client("dummy client", x = 10, y = 1, demand = 10)
        client2 = Client("dummy client", x = 10, y = 2, demand = 20)
        client3 = Client("dummy client", x = 10, y = 3, demand = 30)
        clients_list = [client1, client2, client3]
        delivery._set_clients_list(clients_list)
        delivery.calculate_total_cost()
        self.assertEqual(delivery.total_cost, delivery._get_total_cost())

    def test_Delivery_attribute_total_savings(self):
        delivery = Delivery()
        client1 = Client("dummy client", x = 10, y = 1, demand = 10)
        client2 = Client("dummy client", x = 10, y = 2, demand = 20)
        client3 = Client("dummy client", x = 10, y = 3, demand = 30)
        clients_list = [client1, client2, client3]
        delivery._set_clients_list(clients_list)
        delivery.calculate_total_savings()
        self.assertEqual(delivery.total_savings, delivery._get_total_savings())


# Q8: Delivery.check_same_depot()
# Here, I would think that two Depot objects declared with same attribute
# should be considered to be the same.
    def test_Delivery_check_same_depot(self):
        self.assertTrue(self.delivery1.check_same_depot(self.delivery2))

# Q9: Delivery.check_same_drone()
    def test_Delivery_check_same_drone(self):
        drone1 = Drone(capacity = 100)
        drone2 = Drone(capacity = 80)
        delivery1 = Delivery(drone = drone1)
        delivery2 = Delivery(drone = drone2)
        delivery3 = Delivery(drone = drone1)
        self.assertTrue(delivery1.check_same_drone(delivery3))
        self.assertFalse(delivery1.check_same_drone(delivery2))

# Q10: Delivery.check_same_wind()
    def test_Delivery_check_same_wind(self):
        wind1 = Wind(x = 1, y =1)
        wind2 = Wind(x = 2, y =2)
        delivery1 = Delivery(wind = wind1)
        delivery2 = Delivery(wind = wind2)
        delivery3 = Delivery(wind = wind1)

        self.assertTrue(delivery1.check_same_wind(delivery3))
        self.assertFalse(delivery1.check_same_wind(delivery2))

# Q11: Delivery.check_max_demand()
    def test_Delivery_check_max_demand(self):
        self.assertTrue(self.delivery1.check_max_demand(self.delivery2))
        self.assertFalse(self.delivery1.check_max_demand(self.delivery4))

# Q12: Delivery.can_merge_left()
    def test_Delivery_can_merge_left(self):
        clients_list1 = [self.client1, self.client2]
        clients_list2 = [self.client3, self.client4]
        delivery1 = Delivery(clients_list=clients_list1)
        delivery2 = Delivery(clients_list=clients_list2)
        # every attribute other than clients_list is identical
        delivery1._set_wind(self.wind1)
        delivery2._set_wind(self.wind1)
        delivery1._set_drone(self.drone100)
        delivery2._set_drone(self.drone100)
        delivery1._set_depot(self.depot0)
        delivery2._set_depot(self.depot0)
        self.assertTrue(delivery1.can_merge_left(delivery2))
        self.assertFalse(delivery1.can_merge_left(delivery2, force_common_client=True))
        delivery3 = Delivery()
        delivery3._set_clients_list([self.client3, self.client1])
        delivery3._set_wind(self.wind1)
        delivery3._set_drone(self.drone100)
        delivery3._set_depot(self.depot0)
        self.assertTrue(delivery1.can_merge_left(delivery3))
        self.assertTrue(delivery1.can_merge_left(delivery3, force_common_client=True))

# Q13: Delivery.can_merge_right()
    def test_Delivery_can_merge_right(self):
        clients_list1 = [self.client1, self.client2]
        clients_list2 = [self.client3, self.client4]
        delivery1 = Delivery(clients_list=clients_list1)
        delivery2 = Delivery(clients_list=clients_list2)
        # every attribute other than clients_list is identical
        delivery1._set_wind(self.wind1)
        delivery2._set_wind(self.wind1)
        delivery1._set_drone(self.drone100)
        delivery2._set_drone(self.drone100)
        delivery1._set_depot(self.depot0)
        delivery2._set_depot(self.depot0)
        self.assertTrue(delivery1.can_merge_right(delivery2))
        self.assertFalse(delivery1.can_merge_right(delivery2, force_common_client=True))
        delivery3 = Delivery()
        delivery3._set_clients_list([self.client2, self.client3])
        delivery3._set_wind(self.wind1)
        delivery3._set_drone(self.drone100)
        delivery3._set_depot(self.depot0)
        self.assertTrue(delivery1.can_merge_right(delivery3))
        self.assertTrue(delivery1.can_merge_right(delivery3, force_common_client=True))

# Q14: Delivery.merge_left()
    # test for no common client
    def test_Delivery_merge_left_no_common_client_update(self):
        self.delivery1.merge_left(self.delivery2, update=True)

        cost_by_hand = self.delivery2._depot.cost(self.client2, self.delivery2._drone, self.delivery2._wind)
        cost_by_hand += self.client2.cost(self.client20, self.delivery2._drone, self.delivery2._wind)
        cost_by_hand += self.client20.cost(self.client17, self.delivery2._drone, self.delivery2._wind)
        cost_by_hand += self.client17.cost(self.client1, self.delivery2._drone, self.delivery2._wind)
        cost_by_hand += self.client1.cost(self.client10, self.delivery2._drone, self.delivery2._wind)
        cost_by_hand += self.client10.cost(self.client18, self.delivery2._drone, self.delivery2._wind)
        cost_by_hand += self.client18.cost(self.delivery1._depot, self.delivery2._drone, self.delivery2._wind)

        naive_cost = self.delivery2._depot.cost(self.client2, self.delivery2._drone, self.delivery2._wind)
        naive_cost += self.client2.cost(self.delivery2._depot, self.delivery2._drone, self.delivery2._wind)
        naive_cost += self.delivery2._depot.cost(self.client20, self.delivery2._drone, self.delivery2._wind)
        naive_cost += self.client20.cost(self.delivery2._depot, self.delivery2._drone, self.delivery2._wind)
        naive_cost += self.delivery2._depot.cost(self.client17, self.delivery2._drone, self.delivery2._wind)
        naive_cost += self.client17.cost(self.delivery2._depot, self.delivery2._drone, self.delivery2._wind)
        naive_cost += self.delivery1._depot.cost(self.client1, self.delivery1._drone, self.delivery1._wind)
        naive_cost += self.client1.cost(self.delivery1._depot, self.delivery1._drone, self.delivery1._wind)
        naive_cost += self.delivery1._depot.cost(self.client10, self.delivery1._drone, self.delivery1._wind)
        naive_cost += self.client10.cost(self.delivery1._depot, self.delivery1._drone, self.delivery1._wind)
        naive_cost += self.delivery1._depot.cost(self.client18, self.delivery1._drone, self.delivery1._wind)
        naive_cost += self.client18.cost(self.delivery1._depot, self.delivery1._drone, self.delivery1._wind)


        savings_by_hand = naive_cost - cost_by_hand
#        self.delivery1 = Delivery(clients_list = [self.client1, self.client10, self.client18], depot = self.depot0, drone = self.drone100, wind = self.wind1)
#        self.delivery2 = Delivery(clients_list = [self.client2, self.client20, self.client17], depot = self.depot0, drone = self.drone100, wind = self.wind1)

        # test for update case
        self.assertTrue(self.delivery1._clients_list == [self.client2, self.client20, self.client17, self.client1, self.client10, self.client18])
        self.assertTrue(self.delivery1._total_demand == 2+20+17+1+10+18 )
        self.assertTrue(self.equal2(self.delivery1._total_cost, cost_by_hand))
        self.assertTrue(self.equal2(self.delivery1._total_savings, savings_by_hand))



    def test_Delivery_merge_left_no_common_client_no_update(self):
        self.delivery1.merge_left(self.delivery2, update=False)

        cost_by_hand = self.delivery1._depot.cost(self.client1, self.delivery1._drone, self.delivery1._wind)
        cost_by_hand += self.client1.cost(self.client10, self.delivery2._drone, self.delivery2._wind)
        cost_by_hand += self.client10.cost(self.client18, self.delivery2._drone, self.delivery2._wind)
        cost_by_hand += self.client18.cost(self.delivery1._depot, self.delivery2._drone, self.delivery2._wind)

        naive_cost = self.delivery1._depot.cost(self.client1, self.delivery1._drone, self.delivery1._wind)
        naive_cost += self.client1.cost(self.delivery1._depot, self.delivery1._drone, self.delivery1._wind)
        naive_cost += self.delivery1._depot.cost(self.client10, self.delivery1._drone, self.delivery1._wind)
        naive_cost += self.client10.cost(self.delivery1._depot, self.delivery1._drone, self.delivery1._wind)
        naive_cost += self.delivery1._depot.cost(self.client18, self.delivery1._drone, self.delivery1._wind)
        naive_cost += self.client18.cost(self.delivery1._depot, self.delivery1._drone, self.delivery1._wind)


        savings_by_hand = naive_cost - cost_by_hand

        # test for no update case
        self.assertTrue(self.delivery1._clients_list == [self.client2, self.client20, self.client17, self.client1, self.client10, self.client18])
        self.assertTrue(self.delivery1._total_demand == 2+20+17+1+10+18 )
        self.assertTrue(self.equal2(self.delivery1._total_cost, cost_by_hand))
        self.assertTrue(self.equal2(self.delivery1._total_savings, savings_by_hand))


    # test for common client case
    def test_Delivery_merge_left_common_client(self):
        delivery1 = Delivery(clients_list = [self.client2, self.client3])
        delivery1._wind = self.wind1
        delivery1._drone = self.drone100
        delivery1._depot = self.depot0
        delivery2 = Delivery(clients_list= [self.client1, self.client2])
        delivery1._wind = self.wind1
        delivery1._drone = self.drone100
        delivery1._depot = self.depot0

        delivery1.merge_left(delivery2)
        self.assertTrue(delivery1._clients_list == [self.client1, self.client2, self.client3])


# Q15: Delivery.merge_right()
    # test for no common client
    def test_Delivery_merge_right_no_common_client(self):
        clients_list1 = [self.client1, self.client2]
        clients_list2 = [self.client3, self.client4]
        delivery1 = Delivery(clients_list=clients_list1)
        delivery2 = Delivery(clients_list=clients_list2)
        delivery1._set_wind(self.wind1)
        delivery2._set_wind(self.wind1)
        delivery1._set_drone(self.drone100)
        delivery2._set_drone(self.drone100)
        delivery1._set_depot(self.depot0)
        delivery2._set_depot(self.depot0)
        delivery1.merge_right(delivery2, update=True)
        cost_by_hand = delivery1._get_depot().cost(self.client1, delivery1._get_drone(), delivery1._get_wind())
        cost_by_hand += self.client1.cost(self.client2, delivery1._get_drone(), delivery1._get_wind())
        cost_by_hand += self.client2.cost(self.client3, delivery1._get_drone(), delivery1._get_wind())
        cost_by_hand += self.client3.cost(self.client4, delivery1._get_drone(), delivery1._get_wind())
        cost_by_hand += self.client4.cost(delivery1._get_depot(), delivery1._get_drone(), delivery1._get_wind())

        naive_cost = delivery2._get_depot().cost(self.client3, delivery2._get_drone(), delivery2._get_wind())
        naive_cost += self.client3.cost(delivery2._get_depot(), delivery2._get_drone(), delivery2._get_wind())
        naive_cost += delivery2._get_depot().cost(self.client4, delivery2._get_drone(), delivery2._get_wind())
        naive_cost += self.client4.cost(delivery2._get_depot(), delivery2._get_drone(), delivery2._get_wind())
        naive_cost += delivery1._get_depot().cost(self.client1, delivery1._get_drone(), delivery1._get_wind())
        naive_cost += self.client1.cost(delivery1._get_depot(), delivery1._get_drone(), delivery1._get_wind())
        naive_cost += delivery1._get_depot().cost(self.client2, delivery1._get_drone(), delivery1._get_wind())
        naive_cost += self.client2.cost(delivery1._get_depot(), delivery1._get_drone(), delivery1._get_wind())

        savings_by_hand = naive_cost - cost_by_hand

        # test for update case
        self.assertTrue(delivery1._get_clients_list() == [self.client1, self.client2, self.client3, self.client4])
        self.assertTrue(delivery1._get_total_demand() == 10)
        self.assertTrue(self.equal2(delivery1._get_total_cost(), cost_by_hand))
        self.assertTrue(self.equal2(delivery1._get_total_savings(), savings_by_hand))

        # create delivery3 which is identical to delivery1 before merge
        delivery3 = Delivery(clients_list = clients_list1)
        delivery3._set_wind(self.wind1)
        delivery3._set_drone(self.drone100)
        delivery3._set_depot(self.depot0)
        cost3 = delivery3._get_total_cost()
        savings3 = delivery3._get_total_savings()
        delivery3.merge_right(delivery2, update= False)
        self.assertTrue(delivery3._get_clients_list() == [self.client1, self.client2, self.client3, self.client4])
        self.assertTrue(delivery3._get_total_demand() == 10)
        self.assertTrue(self.equal2(delivery3._get_total_cost(), cost3))
        self.assertTrue(self.equal2(delivery3._get_total_savings(), savings3))


    # test for common client case
    def test_Delivery_merge_right_common_client(self):
        delivery1 = Delivery(clients_list = [self.client2, self.client3])
        delivery1._set_wind(self.wind1)
        delivery1._set_drone(self.drone100)
        delivery1._set_depot(self.depot0)
        delivery2 = Delivery(clients_list= [self.client1, self.client2])
        delivery1._set_wind(self.wind1)
        delivery1._set_drone(self.drone100)
        delivery1._set_depot(self.depot0)

        delivery2.merge_right(delivery1)
        self.assertTrue(delivery2._clients_list == [self.client1, self.client2, self.client3])

# Q16: Solution.calculate_total_cost()
    def test_Solution_calculate_total_cost(self):
        self.solution1.calculate_total_cost()
        self.delivery1.calculate_total_cost()
        self.delivery2.calculate_total_cost()
        self.delivery3.calculate_total_cost()

        cost_by_hand = self.delivery1._total_cost + self.delivery2._total_cost + self.delivery3._total_cost
        self.assertTrue(self.equal2(cost_by_hand, self.solution1._total_cost))

# Q17: Solution.calculate_total_savings()
    def test_Solution_calculate_total_savings(self):
        self.solution1.calculate_total_savings()
        self.delivery1.calculate_total_savings()
        self.delivery2.calculate_total_savings()
        self.delivery3.calculate_total_savings()

        savings_by_hand = self.delivery1._total_savings + self.delivery2._total_savings + self.delivery3._total_savings
        self.assertTrue(self.equal2(savings_by_hand, self.solution1._total_savings))

# Q18: Problem.calculate_total_demand()
    def test_Problem_calculate_total_demand(self):
        self.problem1.calculate_total_demand()
        self.assertEqual(self.problem1._total_demand, 210)

# Q19: Problem.generate_random_clients()
    def test_Problem_generate_random_clients(self):
        problem = Problem()
        problem.generate_random_clients(amount=100, x =(-100, 100), y = (-30, 10), demand=(1,10))
        problem.export_csv("problem.csv")
        for client in problem._clients_list:
            self.assertTrue(-100 <= client.x <= 100)
            self.assertTrue(-30 <= client.y <= 10)
            self.assertTrue(1 <= client.demand <= 10)
        # test for naming
        i = 1
        while i <= 10:
            self.assertEqual(problem._clients_list[i-1].identifier, "random client {}".format(i))
            i += 1
        self.assertEqual(problem.number_of_generated_clients, 100)


#####################
# processing.py
#####################

# Q20: calculate_cost_matrix()
    def test_calculate_cost_matrix(self):
        cost_matrix = calculate_cost_matrix(self.problem1, self.drone100, self.wind1)
        # check dimension
        self.assertEqual(len(cost_matrix), len(self.problem1._clients_list)+1)
        # check values
        for i in range(len(cost_matrix)):
            for j in range(len(cost_matrix)):
                if i !=j:
                    if i != 0 and j!=0:
                        self.assertTrue(self.equal2(cost_matrix[i][j], cost(self.problem1._clients_list[i-1],  self.problem1._clients_list[j-1], self.drone100, self.wind1)))
                    elif i == 0:
                        self.assertTrue(self.equal2(cost_matrix[i][j], cost(self.problem1._depot, self.problem1._clients_list[j-1], self.drone100, self.wind1)))
                    elif j == 0:
                        self.assertTrue(self.equal2(cost_matrix[i][j], cost(self.problem1._clients_list[i-1], self.problem1._depot, self.drone100, self.wind1)))
                    else:
                        self.assertTrue(self.equal2(cost_matrix[i][j], cost(self.problem1._clients_list[i-1], self.problem1._clients_list[j-1], self.drone100, self.wind1)))
                if i == j:
                    self.assertTrue(cost_matrix[i][j] == 0)

# Q21: calculate_savings_matrix()
    def test_calculate_savings_matrix(self):
        savings_matrix = calculate_savings_matrix(self.problem1, self.drone100, self.wind1)
        # check dimension
        self.assertEqual(len(savings_matrix), len(self.problem1._clients_list))
        # check values
        for i in range(len(savings_matrix)):
            for j in range(len(savings_matrix)):
                if i == j:
                    self.assertTrue(savings_matrix[i][j] == 0)
                if i !=j:
                    self.assertTrue(
                        self.equal2(
                            savings_matrix[i][j],
                            (
                            cost(self.problem1._clients_list[i], self.problem1._depot, self.drone100, self.wind1)
                            + cost(self.problem1._depot, self.problem1._clients_list[j], self.drone100, self.wind1)
                            - cost(self.problem1._clients_list[i], self.problem1._clients_list[j], self.drone100, self.wind1)
                            )
                        )
                    )

# Q22: _clarke_and_wright_init()
    def test_clarke_and_wright_init(self):
        sorted, args = _clarke_and_wright_init(self.problem1, self.drone100, self.wind1, name='Some name')
        for i in range(len(sorted)-1):
            # test that args will give sorted list
            self.assertTrue
            (
                (cost(
                    _get_clients_pair_from_arg(self.problem1._clients_list, args[i])[0],
                    self.problem1._depot,
                    self.drone100,
                    self.wind1
                    )
                +
                cost(
                    self.problem1._depot,
                    _get_clients_pair_from_arg(self.problem1._clients_list, args[i])[1],
                    self.drone100,
                    self.wind1
                    )
                -
                cost(
                    _get_clients_pair_from_arg(self.problem1._clients_list, args[i])[0],
                    _get_clients_pair_from_arg(self.problem1._clients_list, args[i])[1],
                    self.drone100,
                    self.wind1
                    )
                )
                <=
                (cost(
                    _get_clients_pair_from_arg(self.problem1._clients_list, args[i+1])[0],
                    self.problem1._depot,
                    self.drone100,
                    self.wind1
                    )
                +
                cost(
                    self.problem1._depot,
                    _get_clients_pair_from_arg(self.problem1._clients_list, args[i+1])[1],
                    self.drone100,
                    self.wind1
                    )
                -
                cost(
                    _get_clients_pair_from_arg(self.problem1._clients_list, args[i+1])[0],
                    _get_clients_pair_from_arg(self.problem1._clients_list, args[i+1])[1],
                    self.drone100,
                    self.wind1
                    )
                )
            )






# Q23: _sequential_build_deliveries()
    def test_sequential_build_deliveries(self):
        pass





















test()


if __name__ == '__main__':
unittest.main()
