import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
sns.set()


dfRaw = pd.read_csv('MiningProcess_Flotation_Plant_Database.csv', decimal=",")
dfRaw['date'] =pd.to_datetime(dfRaw['date'])

ControlChart = ['date', '% Iron Concentrate']
dfControlChart = dfRaw[ControlChart]


#Generate monthyl control chart plots

def generateMonthlyPlots(start, end):

    dfMonth = dfControlChart[(dfRaw['date'] > start) & (dfControlChart['date'] < end)].reset_index(drop=True)
    monthName = dfMonth.iloc[0]['date'].month_name()

    mean = dfMonth['% Iron Concentrate'].mean()
    stdDev = dfMonth['% Iron Concentrate'].std()
    plus3Sigma = mean + (3 * stdDev)
    minus3Sigma = mean - (3 * stdDev)

    graph = sns.lineplot(x='date', y='% Iron Concentrate', data=dfMonth)
    graph.axhline(mean, linestyle='--')
    graph.axhline(plus3Sigma, color='r')
    graph.axhline(minus3Sigma, color='r')
    plt.title(f'% Iron Concentrate for {monthName}')
    plt.xticks(fontsize=4, rotation=90)
    graph.xaxis.set_label_text("")

    plt.show()

for month in range(3,10):

    start = datetime(2017,month,1)
    end = start + relativedelta(day=31)

    generateMonthlyPlots(start, end)
    print(start, end)


#Generate correlation matrix heatmap

corr = dfRaw.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
f, ax = plt.subplots(figsize=(11, 9))
cmap = sns.diverging_palette(230, 20, as_cmap=True)

sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})

plt.xticks(fontsize=4, rotation=90)
plt.yticks(fontsize=4, rotation=0)
plt.title('Correlation Matrix for Iron Floatation Process')

plt.show()

