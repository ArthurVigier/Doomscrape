import matplotlib.pyplot as plt
import requests
import time
import numpy as np

# Initialize a list to store the data points
data = []

# Create a figure and axis for the plot
fig, ax = plt.subplots()

# Set the background color to black
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

# Initialize a line object with empty data
line, = ax.plot([], [], color='white')

# Function to update the graph
def update_graph(movement):
    # Calculate the new data point
    if len(data) > 0:
        new_data_point = data[-1] + movement
    else:
        new_data_point = movement

    # Add the new data point to the data list
    data.append(new_data_point)

    # If the list of data points is too long, remove the first element
    if len(data) > 100:
        data.pop(0)

    # Update the y-data of the line
    line.set_ydata(data)

    # Update the x-data of the line
    line.set_xdata(np.arange(len(data)))

    # Set the x-ticks and their labels
    ax.set_xticks(np.arange(0, len(data), 10))
    ax.set_xticklabels(np.arange(0, len(data), 10))

    # Set the y-ticks and their labels
    ax.set_yticks(np.arange(0, max(data), 1))
    ax.set_yticklabels(np.arange(0, max(data), 1))

    # Adjust the plot limits
    ax.relim()
    ax.autoscale_view()

    # Redraw the line only
    line.draw(ax.figure.canvas.get_renderer())

    # Pause for a while
    plt.pause(0.01)

# Initialize the origin point
origin_point = 0  # or any other value that makes sense for your data

# Initialize the data list with the origin point
data = [origin_point]

# Main loop
while True:
    try:
        # Make an HTTP request to get the new data point
        response = requests.get('http://example.com/data')
        response.raise_for_status()  # This will raise an exception if the request failed

        # Parse the JSON response
        movement = response.json()

        # Calculate the new data point
        new_data_point = data[-1] + movement

        # Update the graph
        update_graph(new_data_point)

    except requests.exceptions.RequestException as e:
        print(f"Une erreur s'est produite lors de la réalisation de la requête HTTP : {e}")
    except ValueError as e:
        print(f"Une erreur s'est produite lors de l'analyse de la réponse JSON : {e}")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")

    # Wait for a while before the next update
    time.sleep(0.5)
