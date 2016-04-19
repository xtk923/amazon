from pre_processing import *
import numpy as np


def calculate_cost_matrix(problem, drone, wind):
    # This function should return the cost matrix of a problem for a given drone and a given wind.
    mat_dim = problem.number_of_clients() + 1 # We consider the depot and the clients, so the dimension of the matrix is number_of_clients + 1
    cost_matrix = np.zeros((mat_dim, mat_dim)) # Create a zero matrx of the correct dimension
    for i in range(1, mat_dim): # define for each element (i,j) of the matrix
        for j in range(1, mat_dim):
            cost_matrix[i,j] = problem.clients_list[i-1].cost(problem.clients_list[j-1], drone, wind) # for client to client
            cost_matrix[0,j] = problem.depot.cost(problem.clients_list[j-1],drone, wind) # for depot to client
            cost_matrix[i,0] = problem.clients_list[i-1].cost(problem.depot, drone, wind) # for client to depot
    return cost_matrix


def calculate_savings_matrix(problem, drone, wind):
    # This function should return the savings matrix of a problem for a given drone and a given wind.
    mat_dim = problem.number_of_clients()
    savings_matrix = np.zeros((mat_dim, mat_dim))
    for i in range(mat_dim): # define for each element (i,j) of the matrix
        for j in range(mat_dim):
            if i != j:
                # savings[i,j] = cost[i,0] - cost[i,j] + cost[j,0]
                savings_matrix[i,j] =(
                            cost(problem._clients_list[i], problem._depot, drone, wind)
                            + cost(problem._depot, problem._clients_list[j], drone, wind)
                            - cost(problem._clients_list[i], problem._clients_list[j], drone, wind)
                    )
            else:
                savings_matrix[i,j] = 0
    return savings_matrix

def _clarke_and_wright_init(problem, drone, wind, name="Unnamed solution"):
    # This function is used to initialize the Clarke and Wright algorithm.
    # This function should calculate the savings matrix
    # and store it in an instance of class Solution.
    # This solution should be appended to the solutions list of the problem.
    # This function should return a tuple (sorted_savings, arg_sorted_savings)
    # with sorted_savings = the sorted savings in a one-dimensional numpy array
    # and arg_sorted_savings = the arguments used to sort the sorted savings
    # (see the numpy 'flatten' and 'argsort' methods)
    savings_matrix = calculate_savings_matrix(problem, drone, wind) # calculate the savings matrix
    solution = Solution(name) # create an instance of class Solution
    solution.savings_matrix = savings_matrix # store the savings matrix to the solution instance
    problem.solutions_list.append(solution) # append the solution to the solution list
    sorted_savings = np.sort(solution.savings_matrix.flatten()) # flatten the saving matrix and sort it
    arg_sorted_savings = np.argsort(solution.savings_matrix.flatten()) # get a list of sort arguments
    # return a tuple
    return sorted_savings, arg_sorted_savings


def _get_clients_pair_from_arg(clients_list, arg_k):
    # This function returns a tuple (client_i, client_j) where both client_i and client_j are instance of class
    # Client.
    # the // operator corresponds to the floor division. ie : 5//2 = 2
    # the % operator correspond to the modulo operator. ie : 5%2 = 1
    number_of_clients = len(clients_list)
    client_i = arg_k // number_of_clients
    client_j = arg_k % number_of_clients
    return clients_list[client_i], clients_list[client_j]


def _sequential_merge_if_possible(current_delivery, candidate_delivery):
    # This function merges two deliveries if possible in the sequential version of Clarke and Wright (ie the two
    # deliveries MUST have a common client at their borders)
    # It returns True if the two deliveries have been merged and False otherwise.
    can_merge = current_delivery.can_merge(candidate_delivery, True)
    if can_merge[0]: # can_merge_left
        current_delivery.merge_left(candidate_delivery, update=False)
    elif can_merge[1]:
        current_delivery.merge_right(candidate_delivery, update=False)
    return can_merge[0] or can_merge[1]


def _sequential_build_deliveries(sorted_savings, arg_sorted_savings, clients_list, depot, drone, wind):
    # This function should return a list of instances of class Delivery calculated with the use of the sequential Clarke
    # and Wright algorithm.
    deliveries_list = []
    return deliveries_list


def _search_deliveries_for_client(client, deliveries_list, left_border=False, interior=False, right_border=False):
    # This function searches for a specified client in a list of deliveries. The search is performed at the border
    # and/or in the interior of the deliveries according to the value of the parameters.
    # The function returns True and the instance of class Delivery where the client has been found.
    # It returns False and None if the client has not been found in any of the deliveries.
    for delivery in deliveries_list:
        if interior and len(delivery.clients_list) >= 2:
            if client in delivery.clients_list[1:-1]:
                return True, delivery
        if left_border and len(delivery.clients_list) >= 1:
            if client == delivery.clients_list[0]:
                return True, delivery
        if right_border and len(delivery.clients_list) >= 1:
            if client == delivery.clients_list[-1]:
                return True, delivery
    return False, None


def _parallel_build_deliveries(sorted_savings, arg_sorted_savings, clients_list, depot, drone, wind):
    # This function should return a list of instances of class Delivery calculated with the use of the parallel Clarke
    # and Wright algorithm.
    deliveries_list = []
    return deliveries_list


def _build_deliveries(version, sorted_savings, arg_sorted_savings, clients_list, depot, drone, wind):
    if version == 'Sequential':
        return _sequential_build_deliveries(sorted_savings, arg_sorted_savings, clients_list, depot, drone, wind)
    if version == 'Parallel':
        return _parallel_build_deliveries(sorted_savings, arg_sorted_savings, clients_list, depot, drone, wind)
    return []


def add_single_client_deliveries(problem, deliveries_list, drone, wind):
    # This function should modify the deliveries_list argument by adding deliveries containing a single client.
    # Only clients that are not present in any delivery should be added. One have to check first that the client
    # can actually be delivered (the demand of the client do not exceed the capacity of the drone)
    pass


def clarke_and_wright(problem, drone, wind, version="Sequential", name=None):
    if version != "Sequential" and version != "Parallel":
        print("Unexpected version : {}".format(version))
        print("Please use 'Sequential' or 'Parallel'")
        return
    if name is None:
        name = version + " Clarke and Wright. Drone capacity : {}".format(drone.capacity)
    sorted_savings, arg_sorted_savings = _clarke_and_wright_init(problem, drone, wind, name)
    deliveries_list = _build_deliveries(version, sorted_savings, arg_sorted_savings,
                                        problem.clients_list, problem.depot, drone, wind)
    add_single_client_deliveries(problem, deliveries_list, drone, wind)
    problem.solutions_list[-1].deliveries_list = deliveries_list
