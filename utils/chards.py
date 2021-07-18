import numpy as np
from matplotlib import pyplot as plt


def graph(file, data):
    height = []
    names = []
    alltasks = 0

    for x in data:
        alltasks += x[0]

    for x in data:
        height.append(x[0])
        names.append(x[1])

    x_pos = np.arange(len(names))

    plt.subplots(figsize=(7, len(names) * 0.23))
    plt.barh(x_pos, height)
    plt.title('Total: ' + str(alltasks), color='orange')

    plt.yticks(x_pos, names, color='orange')
    plt.xticks(color='orange')

    poss = 0
    for i in range(len(height)):
        plt.text(y=poss - 0.25, x=height[i] + 0.1, s=height[i], size=8, color='orange')
        poss += 1

    plt.subplots_adjust(left=0.225)

    plt.savefig(fname=file, transparent=True)
    plt.close()


def pie(file, data):
    height = []
    names = []
    alltasks = 0

    for x in data:
        alltasks += x[0]

    for x in data:
        height.append(x[0] / alltasks * 100)
        names.append(x[1])

    patches, texts = plt.pie(height, startangle=90)
    plt.axis('equal')
    plt.title('Total: ' + str(alltasks), color='orange')

    labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(names, height)]

    plt.legend(patches, labels, loc='upper left', bbox_to_anchor=(-0.1, 1.), fontsize=8)

    plt.savefig(file, transparent=True)
    plt.close()
