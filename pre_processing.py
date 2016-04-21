import numpy as np
import sys

CELL_SEPARATOR = ";"


def cost(point_a, point_b, drone, wind):
    # Should return the cost to go from point_a to point_b using a given drone with a given wind.
    # everything is explianed by their names
    distance = np.linalg.norm((np.array((point_b.x, point_b.y))-np.array((point_a.x, point_a.y)))) # distance from point a to point b is the norm of the vector from point a to point b
    velocity_of_wind = wind._vector
    if np.linalg.norm((np.array((point_b.x, point_b.y))-np.array((point_a.x, point_a.y)))) !=0:
        unit_vector_from_point_a_to_point_b = (np.array((point_b.x, point_b.y))-np.array((point_a.x, point_a.y))) / np.linalg.norm((np.array((point_b.x, point_b.y))-np.array((point_a.x, point_a.y))))
        # find the vector from point_a to point_b, then divide by its norm, introduece max function to avoid divide by zero
        velocity_of_drone = drone.speed * unit_vector_from_point_a_to_point_b   # velocity of drone is the speed of drone multiply by the unit direction vector from a to b.
        relative_velocity_of_drone_to_wind = velocity_of_drone - velocity_of_wind   # the relative velocity is the differecne between the two velocities in vector form
        duration_of_route = distance / drone.speed                  # time = distance / speed
        power_consumed = np.linalg.norm(relative_velocity_of_drone_to_wind) * drone.force   # power consumed = the magnitude of relative velocity * force of drone
        energy =  power_consumed * duration_of_route    # energy consumed = power consumed * time
        return energy
    else:
        return 0


class Wind:
    def __init__(self, x=None, y=None, force=None, direction=None):
        self._x = x     # float
        self._y = y     # float
        self._force = force     # float
        self._direction = direction     # float
        self._vector = None     # numpy array of floats
        self.initialize()


    # # x
    # @property
    # def x(self):
    #     return self._x
    # @x.setter
    # def x(self, x):
    #     self._x = x
    #     self.calculate_force_direction()

    # # y
    # @property
    # def y(self):
    #     return self._y
    # @y.setter
    # def y(self, y):
    #     self._y = y
    #     self.calculate_force_direction()


    # # force
    # @property
    # def force(self):
    #     return self._force
    # @force.setter
    # def force(self, force):
    #     self._force = force
    #     self.calculate_xy()


    # # direction
    # @property
    # def direction(self):
    #     return self._direction
    # @direction.setter
    # def direction(self, x):
    #     self._direction = x
    #     self.calculate_xy()

    # # vector
    # @property
    # def vector(self):
    #     return self._vector

    # getters and setters
    def _get_x(self):
        return self._x

    def _set_x(self, x):
        self._x = x
        self.calculate_force_direction()

    def _get_y(self):
        return self._y

    def _set_y(self, y):
        self._y = y
        self.calculate_force_direction()

    def _get_force(self):
        return self._force

    def _set_force(self, force):
        self._force = force
        self.calculate_xy()

    def _get_direction(self):
        return self._direction

    def _set_direction(self, direction):
        self._direction = direction
        self.calculate_xy()

    def _get_vector(self):
        return self._vector

    x = property(_get_x, _set_x)
    y = property(_get_y, _set_y)
    force = property(_get_force, _set_force)
    direction = property(_get_direction, _set_direction)
    vector = property(_get_vector)



    # methods
    def initialize(self):
        if self._x is not None or self._y is not None:  # _x and _y are prioritized over _force and _direction
            if self._x is None:
                self._x = 0.
            if self._y is None:
                self._y = 0.
            self.calculate_force_direction()
        elif self._force is not None or self._direction is not None:
            if self._force is None:
                self._force = 1.
            if self._direction is None:
                self._direction = 0.
            self.calculate_xy()
        else:
            self._x = 0.
            self._y = 0.
            self._force = 0.
            self._direction = 0.
        self._vector = np.array((self._x, self._y))

    def calculate_force_direction(self):
        self._force = np.linalg.norm((self._x,self._y))
        self._direction = (270 - np.angle(self._x+self._y*1.0j, deg=True))%360   # we use 270 minus the angle calculated because: 
                                                                               # 1. The direction of the wind is opposite to where it comes from-->180-%. (% denotes the previous result)
                                                                               # 2. There's a 90 degree difference between compass and complex number angle--> 180+90-%
                                                                               # at last, the direction is kept within [0, 360]
        self._vector = np.array((self._x, self._y))
        # Given the attributes _x and _y, this function should define _force, _direction and _vector accordingly
        # The norm of a vector can be calculated using np.linalg.norm
        # The angle of a complex number can be calculated using np.angle
        # _direction should be expressed in degrees
        # _vector should be a numpy array (see np.array)

    def calculate_xy(self):
        self._x = self._force*np.cos((270.-self._direction)*np.pi/180)
        self._y = self._force*np.sin((270.-self._direction)*np.pi/180)
        self._vector = np.array((self._x, self._y))
        # Given the attributes _force and _direction, this function should define _x, _y and _vector
        # np.cos, np.sin and np.pi might come useful


class Drone:
    def __init__(self, capacity=100, speed=1., force=1.):
        self.capacity = capacity    # int. Capacity of the drone.
        self.speed = speed  # float. Speed relative to the ground
        self.force = force  # float. The greater the force, the greater the power consumption is.

    def cost(self, point_a, point_b, wind):
        # Should return the cost to go from point_a to point_b with wind
        return cost(point_a, point_b, self, wind)


# This class represents a point on the map (can be either a client or a depot)
class Point():
    def __init__(self, identifier="", x=0., y=0.):
        self.identifier = identifier    # string
        self.x = x  # float. x coordinate
        self.y = y  # float. y coordinate
        # A point is defined by a name or code or whatever identity string,
        # an x coordinate,
        # and a y coordinate.
    def cost(self, other_point, drone, wind):
        # should return the cost to go from this point to other_point given a drone and given some wind
        return cost(self, other_point, drone, wind)

    def __str__(self):
        # overwrites what should be displayed when calling print(some_point)
        return "identifier : {}, (x,y) : ({}, {})".format(self.identifier, self.x, self.y)
        # this should return "identifier : self.identifier, (x,y) : (self.x, self.y)
    def __repr__(self):
        # returns a printable representation of the object
        return "Point object with identifier : {}".format(self.identifier)
        # this should return "Point object with identifier : self.identifier"
        # the string.format() function fills the {}s inside the string with entries in the brackets of string.format() in sequence if not specified.

# The class Client inherits from Point. It adds an attribute : 'demand' which represents the client's demand
class Client(Point):
    def __init__(self, identifier="Client", x=0., y=0., demand=0):
        Point.__init__(self, identifier, x, y)  # constructor of super class
        self.demand = demand    # int, update the attribute "demand" with a certain value.

    def __str__(self):
        return "identifier : {}, (x,y) : ({}, {}), demand : {}".format(self.identifier, self.x, self.y, self.demand)
        # similar to previous parts, it returns a string stating the particulars of the client.

# The class Depot inherits from Point too.
# it is a subclass of Point
class Depot(Point):
    def __init__(self, identifier="Depot", x=0., y=0.):
        Point.__init__(self, identifier, x, y)

    '''
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.identifier == other.identifier
    '''

class Delivery:

    def __init__(self, clients_list=list(), depot=None, drone=None, wind=None):

        self._clients_list = clients_list   # python list containing instances of class Client

        if depot is None:
            self._depot = Depot()
        else:
            self._depot = depot     # instance of class Depot. A delivery always starts and ends at a depot.

        if drone is None:
            self._drone = Drone()
        else:
            self._drone = drone     # instance of class drone. A delivery is carried out using a drone.

        if wind is None:
            self._wind = Wind()
        else:
            self._wind = wind       # instance of class wind. A delivery is performed in a given wind condition.

        self._total_demand = 0.     # float. Sum of the demand of all the clients delivered in this delivery.

        self._total_cost = 0.   # float. represents the total cost of the delivery

        self._total_savings = 0.    # float. total savings of this delivery compared to the naive approach

        self.update() # calculate accordingly



    def __str__(self):

        self.print_delivery()

        return ""


    # # depot
    # @property
    # def depot(self):
    #     return self._depot

    # @depot.setter
    # def depot(self, depot):
    #     self._depot = depot
    #     self.update()

    # # clients_list
    # @property
    # def clients_list(self):
    #     return self._clients_list

    # @clients_list.setter
    # def clients_list(self, clients_list):
    #     self._clients_list = clients_list
    #     self.update()


    # # drone
    # @property
    # def drone(self):
    #     return self._drone

    # @drone.setter
    # def drone(self, drone):
    #     self._drone = drone
    #     self.update()


    # # wind
    # @property
    # def wind(self):            # just do it the same way as others
    #     return self._wind           #

    # @wind.setter
    # def wind(self, wind):      #
    #     self._wind = wind           #
    #     self.update()

    # # total_demand
    # @property
    # def total_demand(self):
    #     return self._total_demand

    # # total_cost
    # @property
    # def total_cost(self):      # total_cost should not be directly set but calculated
    #     return self._total_cost     #

    # # total_savings
    # @property
    # def total_savings(self):   # until here
    #     return self._total_savings

    # getters and setters
    def _get_depot(self):
        return self._depot

    def _set_depot(self, depot):
        self._depot = depot
        self.update()
        # when setting a new depot, all the attributes of this class that are impacted should be updated
       

    def _get_clients_list(self):
        return self._clients_list

    def _set_clients_list(self, clients_list):
        self._clients_list = clients_list
        self.update()
        # when setting a new clients list, all the attributes of this class that are impacted should be updated
        

    def _get_drone(self):
        return self._drone

    def _set_drone(self, drone):
        self._drone = drone
        self.update()
        # when setting a new drone, all the attributes of this class that are impacted should be updated
       

    def _get_wind(self):            # just do it the same way as others
        return self._wind           #


    def _set_wind(self, wind):      #
        self._wind = wind           #
        self.update()

    def _get_total_demand(self):
        return self._total_demand




    def _get_total_cost(self):      # total_cost should not be directly set but calculated
        return self._total_cost     #

    def _get_total_savings(self):   # until here
        return self._total_savings
    

    depot = property(_get_depot, _set_depot)
    clients_list = property(_get_clients_list, _set_clients_list)
    drone = property(_get_drone, _set_drone)
    total_demand = property(_get_total_demand)
    wind = property(_get_wind, _set_wind)   # the same way as others
    total_cost = property(_get_total_cost)
    total_savings = property(_get_total_savings)    # as usual
   


    # methods
    def print_clients_list(self):
        print("Clients list : ({} client(s))".format(len(self._clients_list)))
        for client in self._clients_list:
            print(client)

    def print_depot(self):
        print(self._depot)

    def print_delivery(self):
        print("printing delivery properties :")
        print("depot :")
        self.print_depot()
        self.print_clients_list()
        print("delivery properties :")
        print("drone capacity = {}, wind = {}, total demand = {}, total cost = {}, total savings = {}"
              .format(self._drone.capacity, self.wind.vector,
                      self._total_demand, self._total_cost, self._total_savings))

    def calculate_total_demand(self):
        # this method should update the _total_demand attribute
        if len(self._clients_list)==0:
            self._total_demand=0
        else:
            self._total_demand=0                                    #initialize the value
            for client in self._clients_list:                       #for every client, we take the demand attribute and sum them
                self._total_demand += client.demand

    def calculate_total_cost(self):
        # this method should update the _total_cost attribute
        if len(self._clients_list)==0:
            self._total_cost = 0
        else:
            self._total_cost = 0
            self._total_cost += cost(self._depot, self._clients_list[0], self._drone, self._wind)  #from the depot to the first client
            for i in range(0,len(self._clients_list)-1):                                                        #from the first client to all adjcent clients in the list
                self._total_cost +=  self._clients_list[i].cost(self._clients_list[i+1],self._drone,self._wind)
            self._total_cost += self._clients_list[-1].cost(self._depot,self._drone,self._wind) #from the last client back to the depot

    def calculate_total_savings(self):
        # this method should update the _total_savings attribute
        if len(self._clients_list)==0:
            self._total_savings = 0

        naive_cost = 0
        for client in self._clients_list:
            #for every client, calculate the cost form the depot to the client, and the cost way back
            #take these values from the _total_savings, which is initially zero, this give a negative value
            naive_cost +=  cost(self._depot, client, self._drone,self._wind) + cost(client, self._depot, self._drone,self._wind)
        #calculate the final _total_savings, which gives a positive value as long as the method proposed is more economic than the naive method.
        self.calculate_total_cost() # need to update total_cost
        self._total_savings = naive_cost - self._total_cost

    def update(self):
        self.calculate_total_demand()
        self.calculate_total_cost()
        self.calculate_total_savings()

    def check_same_depot(self, other_delivery):
        # this method should return true if this delivery has the same depot as other_delivery and false otherwise
        return self.depot == other_delivery.depot
        # return self._get_depot().__eq__(other_delivery._get_depot())

    def check_same_drone(self, other_delivery):
        if self._drone == other_delivery._drone:
            return True
        else:
        # this method should return True if this delivery has the same drone as other_delivery and False otherwise
            return False

    def check_same_wind(self, other_delivery):
        if self._wind == other_delivery._wind:
            return True
        else:
        # this method should return True if this delivery has the same wind as other_delivery and False otherwise
            return False

    def check_max_demand(self, other_delivery):
        n=0
        for client in self._clients_list:
            if client in other_delivery._clients_list:
                n += client.demand
            else:
                continue
        if self._total_demand+other_delivery._total_demand-n<=self._drone.capacity:
            return True
        else:
        # this method should return True if the total demand of this delivery plus the total demand of other_delivery
        # is less or equal to the drone capacity. Caution : the two deliveries might have one client in common.
            return False

    def check_compatibility(self, other_delivery):
        can_merge = self.check_same_depot(other_delivery)
        can_merge = can_merge and self.check_same_drone(other_delivery)
        can_merge = can_merge and self.check_same_wind(other_delivery)
        can_merge = can_merge and self.check_max_demand(other_delivery)
        return can_merge

    def can_merge_left(self, other_delivery, force_common_client=False):
        if len(self.clients_list)==0 or len(other_delivery.clients_list)==0:    #check if any client list is empty, if so, check the compatibility
            return self.check_compatibility(other_delivery)
        if not self.check_compatibility(other_delivery): # if the compatibility is False, return False anyway
            return False
        if not force_common_client:
            for i in range(len(self.clients_list)):
                if i==0:    # when force_common_client is false, if the first client in the self list is in the other_delivery list, but not at the last 
                    if self.clients_list[i] in other_delivery.clients_list[:len(other_delivery.clients_list)-1]:#return false
                        return False
                else:
                    if self.clients_list[i] in other_delivery.clients_list: #if any other element is in common, return False
                        return False
            return True # return True if the aforementioned conditions are not met
        else:   # now consider the case where force_common_client is True
            if self.clients_list[0] != other_delivery.clients_list[-1]: # if the client at boundary is not in common , return false
                return False
            else:
                for i in range(len(self.clients_list)): #similar to the previous case
                    if i==0:
                        if self.clients_list[i] in other_delivery.clients_list[:len(other_delivery.clients_list)-1]:
                            return False
                    else:
                        if self.clients_list[i] in other_delivery.clients_list:
                            return False
                return True
                               
##        if force_common_client:             #divide the situation into two cases: 1.force_common_client ==True. 2.force_common_client==False.
##            return self.check_compatibility(other_delivery) and self.clients_list[0] == other_delivery.clients_list[-1]
##        #common_client_list1 == common_client_list2
##        #for the case force_common_client ==True, check the compatibility and whether common clients are at the correct boundary.
##        else:
##            if self.check_compatibility(other_delivery): 
##                if common_client:
##                    common_list=[]
##                    for client in self.clients_list:
##                        if client in other_delivery.clients_list:
##                            common_list.append(client)
##                    if common_list<self.clients_list:
##                        common_list[::-1]
##                        other_delivery.clients_list[::-1]
##                    return common_list < other_delivery.clients_list
##                else:
##                    return True
##            else:
##                return False
        # for the case that force_common_client==False, check the compatibility. if ok, check if common clients exist
        # if there are common clients, check if they are at the correct boundary.
        
        # this method should return True if other_delivery can be merged to the left of the current delivery.
        # returns False otherwise. Caution : the two deliveries might have one client in common.
        # if force_common_client is True then this method should return False if the two deliveries don't have a common
        # client at their border.
        # Example :
        # other_delivery.clients_list = [client_10, client_5, client_6] and
        # self.clients_list = [client_6, client_8, client_1]
        # can be merged if no other rule (wind, drone, total demand, etc) is broken.
        # but,
        # other_delivery.clients_list = [client_12, client_2, client_8] and
        # self.clients_list = [client_7, client_8, client_10]
        # can't be merged anyway because of client_8.
        # If force_common_client is True then
        # other_delivery.clients_list = [client_10, client_5, client_6] and
        # self.clients_list = [client_7, client_8, client_1]
        # can't be merged anyway (return False).


    def can_merge_right(self, other_delivery, force_common_client=False):
        if len(self.clients_list)==0 or len(other_delivery.clients_list)==0: 
            return self.check_compatibility(other_delivery)
        if not self.check_compatibility(other_delivery): 
            return False
        if not force_common_client:
            for i in range(len(other_delivery.clients_list)):
                if i==0: 
                    if other_delivery.clients_list[i] in self.clients_list[:len(self.clients_list)-1]:
                        return False
                else:
                    if other_delivery.clients_list[i] in self.clients_list: 
                        return False
            return True 
        else:   
            if other_delivery.clients_list[0] != self.clients_list[-1]: 
                return False
            else:
                for i in range(len(other_delivery.clients_list)): 
                    if i==0:
                        if other_delivery.clients_list[i] in self.clients_list[:len(self.clients_list)-1]:
                            return False
                    else:
                        if other_delivery.clients_list[i] in self.clients_list:
                            return False
                return True                              
        # this is almost identical to can_merge_left
        
        # this method should return True if other_delivery can be merged to the right of the current delivery.
        # returns False otherwise. Caution : the two deliveries might have one client in common.
        # if force_common_client is True then this method should return False if the two deliveries don't have a common
        # client at their border.
        return False

    def can_merge(self, other_delivery, force_common_client=False):
        left = self.can_merge_left(other_delivery, force_common_client)
        right = self.can_merge_right(other_delivery, force_common_client)
        return left, right

    def merge_left(self, other_delivery, update=True):
        if len(self._clients_list)==0 or len(other_delivery._clients_list)==0: # if any of the two lists is empty, 
            self._clients_list=other_delivery._clients_list + self._clients_list   # simply add the two and define it as self.clients_list
        else:
            # check whether the boundary has the same client
            if other_delivery._clients_list[-1] == self._clients_list[0]:
                # combine two lists with one boundary not taken
                self._clients_list = other_delivery._clients_list[0:-1] + self._clients_list
            else:
                self._clients_list = other_delivery._clients_list + self._clients_list
                # combine two lists

        self.calculate_total_demand()
        if update:                                              # update all if update = True
            self.update()
        # this methods should modify the current clients list so that the new list is the combination of the one of the
        # other_delivery + the current clients list. Caution : the two deliveries might have one client in common.
        # if update is True then a full update must be performed after the modification of the list. Otherwise only the
        # total demand must be updated.
        

    def merge_right(self, other_delivery, update=True):
        if len(self._clients_list) == 0 or len(other_delivery._clients_list) == 0: # if any of the two lists is empty, 
            self._clients_list =  self._clients_list + other_delivery._clients_list # simply add the two and define it as self.clients_list
        else:
            # check whether the boundary has the same client
            if other_delivery._clients_list[0] == self._clients_list[-1]:
                # combine two lists with one boundary not taken
                self._clients_list =   self._clients_list + other_delivery._clients_list[1:]
            else:
                self._clients_list =   self._clients_list + other_delivery._clients_list
                # combine two lists

        self.calculate_total_demand()
        if update:                                              # update all if update = True
            self.update()
        # this methods should modify the current clients list so that the new list is the combination of the current
        # list + the list of other_delivery. Caution : the two deliveries might have one client in common.
        # if update is True then a full update must be performed after the modification of the list. Otherwise only the
        # total demand must be updated.
        


# A solution is a combination of deliveries (in the form of a list of deliveries).
# This class also stores the cost and savings matrices of the problem it solves.
# The total cost and total savings of the solution are stored as well.
class Solution:

    def __init__(self, name="Unnamed Solution", deliveries_list=list()):

        self.name = name    # string. Useful for identification and post-processing

        # if deliveries_list is None:         #if no list is given, create empty list

        #     self._deliveries_list = list()  # define the data type of _deliveries_list

        # else:

        self._deliveries_list = deliveries_list  # python list of deliveries.

        self.cost_matrix = None  # numpy two dimensional array. Cost matrix (for the given drone and wind)

        self.savings_matrix = None  # numpy two dimensional array. savings matrix (for the given drone and wind)

        self._total_cost = None  # float. total cost of the solution

        self._total_savings = None  # float. total savings of the solution

# This prints out the information of this solution.
    def print(self, detailed=True):
        print("Solution name : {}".format(self.name))
        print("number of deliveries = {}, total cost = {}, total savings = {}"
              .format(len(self._deliveries_list), self._total_cost, self._total_savings))
        if detailed:
            for delivery in self._deliveries_list:
                print(delivery)

# this calls the print funciton
    def __str__(self):
        self.print(detailed=False)
        return ""


# getters and setters
    def _get_deliveries_list(self):
        return self._deliveries_list

    def _set_deliveries_list(self, deliveries_list):
        self._deliveries_list = deliveries_list
        self.calculate_total_cost()
        self.calculate_total_savings()

    def _get_total_cost(self):
        return self._total_cost

    def _get_total_savings(self):
        return self._total_savings

# property() funciton allows writting e.g. self.deliveries_list instead of self._get_deliveries_list and self._set_deliveries_list
    deliveries_list = property(_get_deliveries_list, _set_deliveries_list)
    total_cost = property(_get_total_cost)
    total_savings = property(_get_total_savings)





    # # deliveries_list
    # @property
    # def deliveries_list(self):
    #     return self._deliveries_list

    # @deliveries_list.setter
    # def deliveries_list(self, deliveries_list):
    #     self._deliveries_list = deliveries_list
    #     self.calculate_total_cost()
    #     self.calculate_total_savings()

    # # total_cost
    # @property
    # def total_cost(self):
    #     return self._total_cost

    # # total_savings
    # @property
    # def total_savings(self):
    #     return self._total_savings

    def get_drones_list(self):
        return [delivery.drone for delivery in self.deliveries_list]

    def get_winds_list(self):
        return [delivery.wind for delivery in self.deliveries_list]

    def calculate_total_cost(self):
        # This method should calculate the _total_cost attribute
        self._total_cost = 0                   # initialize total cost
        for delivery in self._deliveries_list:
            delivery.update()
            self._total_cost += delivery._total_cost # add the total cost of each delivery to the total cost of the solution

    def calculate_total_savings(self):
        self._total_savings = 0                   # initialize total savings
        for delivery in self._deliveries_list:
            delivery.update()
            self._total_savings += delivery._total_savings # add the total savings of each delivery to the total savings of the solution
            # This method should calculate the _total_savings attribute




# A problem is a set of clients to deliver from a given depot.
# This class can also store a list of solutions.
class Problem:

    def __init__(self, depot=None, clients_list=list()):

        if depot is None:

            self._depot = Depot()

        else:

            self._depot = depot  # Depot.

        # if clients_list is None:

        #     self._clients_list = list()

        # else:

        self._clients_list = clients_list  # python list of Clients

        self._number_of_generated_clients = 0  # int. Useful for random problem generation.

        self.solutions_list = list()  # python list of solutions.

        self._total_demand = None  # int. total demand of all the clients to be delivered.

        self.calculate_total_demand()


    # # depot
    # @property
    # def depot(self):
    #     return self._depot

    # @depot.setter
    # def depot(self, depot):
    #     self._depot = depot
    #     self.solutions_list = list()

    # # clients_list
    # @property
    # def clients_list(self):
    #     return self._clients_list

    # @clients_list.setter
    # def clients_list(self, clients_list):
    #     self._clients_list = clients_list
    #     self.solutions_list = list()
    #     self.calculate_total_demand()

    # # number_of_generated_clients
    # @property
    # def number_of_generated_clients(self):
    #     return self._number_of_generated_clients

    # # total_demand
    # @property
    # def total_demand(self):
    #     return self._total_demand




    def _get_depot(self):
        return self._depot

    def _set_depot(self, depot):
        self._depot = depot
        self.solutions_list = list()

    def _get_clients_list(self):
        return self._clients_list

    def _set_clients_list(self, clients_list):
        self._clients_list = clients_list
        self.solutions_list = list()
        self.calculate_total_demand()

    def _get_number_of_generated_clients(self):
        return self._number_of_generated_clients

    def _get_total_demand(self):
        return self._total_demand

    depot = property(_get_depot, _set_depot)
    clients_list = property(_get_clients_list, _set_clients_list)
    number_of_generated_clients = property(_get_number_of_generated_clients)
    total_demand = property(_get_total_demand)

    def print_clients(self):
        for client in self._clients_list:
            print(client)

    def print_depot(self):
        print(self._depot)

    def number_of_clients(self):
        return len(self._clients_list)

    def print_solutions(self, detailed=False):
        for solution in self.solutions_list:
            print("")
            solution.print(detailed)
    # delete an Solution object by its index in the solution_list
    def remove_solution_index(self, index):
        del self.solutions_list[index]

    def remove_solution_named(self, name):
        for i, solution in enumerate(self.solutions_list):
            if solution["Name"] == name:
                del self.solutions_list[i]
                break

    def clear_solutions(self):
        self.solutions_list.clear()

    def calculate_total_demand(self):
        self._total_demand = sum([client.demand for client in self._clients_list]) # just add them up

    def generate_random_clients(self, amount=1, x=(-10, 10), y=(-10, 10), demand=(1, 100)):
        # create "amount" number of random clients
        while (amount >= 1):
            # create a random number between 0 and 1, multiply by the range of x, add it on the lower bound of x
            x_cor = np.random.rand() * (x[1] - x[0]) + x[0]
            y_cor = np.random.rand() * (y[1] - y[0]) + y[0]
            # generate a random integer between the boundary of demand
            demand_random = np.random.random_integers(demand[0], demand[1])
            # increase _number_of_generated_clients by 1
            self._number_of_generated_clients += 1
            # create such a client
            client = Client(identifier = "random client {}".format(self.number_of_generated_clients), x = x_cor, y = y_cor, demand = demand_random)
            self._clients_list.append(client)
            amount -= 1
        self.calculate_total_demand()



        # This method should add random clients to the current _clients_list and then update the _total_demand attribute
        # Every time a new client is generated, _number_of_generated_clients is increased by 1.
        # When a client is generated, its identifier should be "random client X" with X=_number_of_generated_clients
        # The x coordinate of the client should be randomly chosen between the limits given by the 'x' parameter.
        # (see np.random.rand)
        # The same thing goes for the y coordinate of the client.
        # The client's demand is also chosen randomly according to the 'demand' parameter. Remember that the demand is
        # an integer, not a float. (see np.random.random_integers)

    def export_csv(self, file_name):
        # This method exports the problem to a file in csv format.
        # file_name is a string
        try:
            output_csv = open(file_name, "w")
        except OSError:
            sys.stderr.write('Unable to open file "%s"\n' % file_name)
            sys.stderr.flush()
            return
        output_csv.write("Delivery optimization problem"+CELL_SEPARATOR)
        output_csv.write("\n")
        output_csv.write("type"+CELL_SEPARATOR)
        output_csv.write("identifier"+CELL_SEPARATOR)
        output_csv.write("x"+CELL_SEPARATOR)
        output_csv.write("y"+CELL_SEPARATOR)
        output_csv.write("demand"+CELL_SEPARATOR)
        output_csv.write("\n")
        output_csv.write("depot"+CELL_SEPARATOR)
        output_csv.write(self.depot.identifier+CELL_SEPARATOR)
        output_csv.write(str(self.depot.x)+CELL_SEPARATOR)
        output_csv.write(str(self.depot.y)+CELL_SEPARATOR)
        output_csv.write("\n")
        for client in self.clients_list:
            output_csv.write("client"+CELL_SEPARATOR)
            output_csv.write(client.identifier+CELL_SEPARATOR)
            output_csv.write(str(client.x)+CELL_SEPARATOR)
            output_csv.write(str(client.y)+CELL_SEPARATOR)
            output_csv.write(str(client.demand)+CELL_SEPARATOR)
            output_csv.write("\n")
        output_csv.flush()
        output_csv.close()

    def import_csv(self, file_name):
        # This method reads a problem from a file in csv format.
        # file_name is a string
        try:
            input_csv = open(file_name, "r")
        except OSError:
            sys.stderr.write('Unable to open file "%s"\n' % file_name)
            sys.stderr.flush()
            return
        if input_csv.readline()[:29] != "Delivery optimization problem":  # +CELL_SEPARATOR+"\n":
            print("incorrect file !")
            return
        next(input_csv)
        clients_list = list()
        for line in input_csv:
            line = line.rstrip('\r\n')
            line = line.rstrip('\n')
            cells = line.split(CELL_SEPARATOR)
            if len(cells) >= 1:
                if cells[0] == "depot":
                    if len(cells) >= 4:
                        identifier = cells[1]
                        x = float(cells[2])
                        y = float(cells[3])
                        self.depot = Depot(identifier, x, y)
                if cells[0] == "client":
                    if len(cells) >= 5:
                        identifier = cells[1]
                        x = float(cells[2])
                        y = float(cells[3])
                        demand = int(cells[4])
                        clients_list.append(Client(identifier, x, y, demand))
        self.clients_list = clients_list
        input_csv.close()

