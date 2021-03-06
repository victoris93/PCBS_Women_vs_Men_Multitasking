# Author: Victoria Shevchenko

"""The script first reads the .csv file previously generated with experiment_1.py.  Then, it attributes a 'Condition' factor to trials. They are either pure, mixed repeat or mixed switch. The mixed switch factor is of special interest: they bear information about the switching cost. The data are then grouped by trial condition, congruency and subject's sex. The error rate is calculated after the grouping (line 29). The plots are generated from the grouped data."""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

GRAPH_DIR  = 'Graphs/'

multitasking_data = pd.read_csv('experiment_1_data.csv', header = 1)
multitasking_data['Condition'] = np.where(multitasking_data.Block.str.contains("pure"), "Pure", None)

for i, row in multitasking_data.loc[multitasking_data['Block'] == "mixed",:].iterrows():
	if multitasking_data.loc[i - 1,'Task Type'] == multitasking_data.loc[i,'Task Type']:
		
		multitasking_data.loc[i,'Condition'] = "Mixed Repeat"
	else:
		multitasking_data.loc[i,'Condition'] = "Mixed Switch"

multitasking_data.describe()
RT_barplot = sns.catplot(x='Congruent Trial', y='RT', hue = 'Sex', col = 'Condition', kind = 'bar', data=multitasking_data, height = 3, aspect = 0.8)
RT_barplot.set_axis_labels("", "RT")
RT_barplot.set_titles("{col_name}")
RT_barplot.savefig(os.path.join(GRAPH_DIR, 'RT_condition_congruency_sex.png'))

grouped_data = multitasking_data.groupby(['Condition', 'Congruent Trial', 'Sex']).aggregate(lambda x: ','.join(map(str, x)))
correct_percentage_by_condition_and_congruency = multitasking_data.groupby(['Condition','Congruent Trial', 'Sex'])['Correct Response'].apply(lambda x: np.sum(x)/len(x))
grouped_data["Errors (%)"] = (1 - correct_percentage_by_condition_and_congruency) * 100
grouped_data = grouped_data.reset_index()

error_rate_barplot = sns.catplot(x='Congruent Trial', y='Errors (%)', hue = 'Sex', col = 'Condition', kind = 'bar', data=grouped_data, height = 3, aspect = 0.8)
error_rate_barplot.set_axis_labels("", "Errors %")
error_rate_barplot.set_titles("{col_name}")

error_rate_barplot.savefig(os.path.join(GRAPH_DIR, 'Error_rate_condition_congruency_sex.png'))