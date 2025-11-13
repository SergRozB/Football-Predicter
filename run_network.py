import network
import create_data_file
import matplotlib.pyplot as plt

training_data, validation_data = create_data_file.create_data()

def plot_cost(cost, accuracy, isTraining=False, isEvaluation=False, scatter=False, multiple=False):
    fig, ax1 = plt.subplots()
    ax1.set_xlabel("Epoch")
    ax1.set_ylabel("Cost")
    ax1.yaxis.label.set_color("red")
    ax2 = ax1.twinx()
    ax2.set_ylabel("Percentage Correct")
    ax2.yaxis.label.set_color("green")
    xEpoch = list(i for i in range(len(cost)))
    yCost = cost
    n_data = 0
    if isTraining: 
        n_data = len(training_data)
        plt.title("With Training Data")
    elif isEvaluation: 
        n_data = len(validation_data)
        plt.title("With Evaluation Data")
    yPercentage = list(i/n_data for i in accuracy)
    if scatter:
        ax1.scatter(xEpoch, yCost, color="r", s=10)
        ax2.scatter(xEpoch, yPercentage, color="g", s=10)
    ax1.plot(xEpoch, yCost, color="r")
    ax2.plot(xEpoch, yPercentage, color="g")
    fig.tight_layout()
    if not multiple:
        plt.show()

net = network.Network([11, 50, 3])
evaluation_cost, evaluation_accuracy, training_cost, training_accuracy = net.SGD(training_data=training_data, epochs=20, mini_batch_size=10, eta=0.01, lmbda = 5, 
                                               evaluation_data=validation_data, monitor_training_accuracy=True, monitor_training_cost=True, monitor_evaluation_accuracy=True, 
                                               monitor_evaluation_cost=True)

net.save("test_network")

plot_cost(cost=training_cost, accuracy=training_accuracy, isTraining=True, multiple=True, scatter=True)
plot_cost(cost=evaluation_cost, accuracy=evaluation_accuracy, isEvaluation=True, scatter=True)