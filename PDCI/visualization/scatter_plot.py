'''
Created on 18-Oct-2019

@author: akash
'''
import matplotlib.pyplot as plt


class scatter_plot:
    def __init__(self):
        pass

    def scatter_plot(self, D, Y):
        plt.scatter(D, Y, c="blue", alpha=0.5)
        plt.scatter(10, -5, c="Red", alpha=0.5)
        plt.title('Scatter plot')
        plt.xlabel('x')
        plt.ylabel('y')
        return plt.show()
