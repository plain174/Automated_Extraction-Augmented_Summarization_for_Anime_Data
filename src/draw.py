import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.rcParams['font.family']='SimHei'
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
def bar(data):
    plt.barh(data)
    plt.show()
    plt.savefig('first.jpg',dpi=600)