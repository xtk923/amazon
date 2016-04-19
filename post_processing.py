from pre_processing import *
import matplotlib.pyplot as plt


def plot_problem(problem, ax=None, plot_demand=True):
    # This function creates a plot representing the problem to solve. It plots the depot, the clients (and the client's
    # demand if plot_demand is True)
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("Number of clients = {}, total demand = {}".format(problem.number_of_clients(), problem.total_demand))
    ax.grid(False)
    # You should complete the x_depot, y_depot, x_clients and y_clients variables. Each of these variables should be a
    # python list of floats.
    x_depot = []
    y_depot = []
    x_clients = []
    y_clients = []
    ax.plot(x_depot, y_depot, marker="s", color="red", label="Depot", linestyle="None", ms=7, zorder=2)
    ax.plot(x_clients, y_clients, marker="o", color="blue", label="Client (demand)", linestyle="None", ms=3, zorder=1)
    if plot_demand:
        # plot demand for each client. Use ax.text(x, y, "some string", style="italic", fontsize=8, color="blue",
        # ha="center", va="bottom", zorder=1) which is a matplotlib function to add text on a plot.
        pass
        for client in problem.clients_list:
            ax.text(client.x, client.y, str(client.demand), style="italic",
                    fontsize=8, color="blue", ha="center", va="bottom", zorder=1)
    return ax


def plot_solution(solution, ax, color):
    # This function plots a solution. More precisely, it plots all the deliveries of the solution on the axe 'ax' with
    # the color 'color'.

    # Plotting of the wind
    xy = (0., 0.)
    winds_list = solution.get_winds_list()
    if len(winds_list) > 0:
        xy = (winds_list[0].x, winds_list[0].y)
    ax.annotate('', xy=xy, xytext=(0., 0.), zorder=1, arrowprops=dict(facecolor='gray'))
    # generation of a random dashed template for the deliveries.
    dashes = np.random.random_integers(5, 20, 4)
    dashes[1] = 5
    dashes[3] = 5
    # plotting of the deliveries of the solution
    for i, delivery in enumerate(solution.deliveries_list):
        label = None
        if i == 0:
            label = solution.name
        # Here, you should generate the x_list and y_list variables
        x_list = []
        y_list = []
        line, = ax.plot(x_list, y_list, color=color, marker="", linestyle="-", label=label, zorder=0)
        line.set_dashes(dashes)  # remove/comment this line to plot continuous lines instead of dashes
    ax.legend(loc=0, fontsize='x-small', numpoints=1)


def _get_random_color(color_list, number_of_generated_candidates=10):
    # This function randomly generates a color that contrasts the most with the colors that are in color_list.
    # This function actually generates number_of_generated_candidates colors and selects the one that contrasts the most
    # with the other colors.
    # color_list is a python list of colors. A color is an array (or a list) of 3 floats between 0 and 1.
    color = None
    color_candidates_matrix = np.random.rand(number_of_generated_candidates, 3)
    norm = 0.
    for i in range(0, number_of_generated_candidates):
        candidate_color = color_candidates_matrix[i]
        candidate_norm = np.min([np.linalg.norm(existing_color-candidate_color) for existing_color in color_list])
        if candidate_norm > norm:
            norm = candidate_norm
            color = candidate_color
    color_list.append(color)
    return color


def plot_problem_solutions(problem, ax=None, plot_demand=True):
    # This function should plot a problem and its solutions.
    colors_list = [np.array([1., 1., 1.])]  # [1., 1., 1.] = white (background color of the figure)
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    pass
    return ax
