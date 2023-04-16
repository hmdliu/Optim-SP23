
import pickle
import seaborn as sns
import matplotlib.pyplot as plt

with open('./D/D.pkl', 'rb') as f:
    D = pickle.load(f)
ax = sns.heatmap(D, linewidth=0)
ax.set(xticklabels=[])
ax.set(yticklabels=[])
ax.tick_params(left=False, bottom=False)
plt.savefig('./D/D.png')
plt.show()
