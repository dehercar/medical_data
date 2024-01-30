import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')


# Add 'overweight' column
df['overweight'] = (df['weight'] / (df['height'] / 100)**2 > 25).astype(int)

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df,
                   id_vars=['cardio'],
                   value_vars=[
                       'cholesterol', 'gluc', 'smoke','alco', 'active', 'overweight'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat_grouped = df_cat.groupby(['cardio','variable','value'], as_index=False)
    df_cat_grouped = df_cat_grouped['value'].size()
    df_cat_grouped.rename(columns={'size':'total'}, inplace=True)
    
    # Draw the catplot with 'sns.catplot()'
    # sns.set(style="whitegrid")

    # Creating the catplot with two columns
    fig = sns.catplot(x="variable", y="total", hue="value",
                    data=df_cat_grouped, kind="bar", col="cardio")


    # Get the figure for the output


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig

# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df.loc[(df['ap_lo'] <= df['ap_hi'])
                     & (df['height'] >= df['height'].quantile(0.025))
                     & (df['height'] <= df['height'].quantile(0.975))
                     & (df['weight'] >= df['weight'].quantile(0.025))
                     & (df['weight'] <= df['weight'].quantile(0.975))
                     ]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr,dtype = bool))
    # Set up the matplotlib figure

    sns.color_palette("icefire", as_cmap=True)

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(11, 9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data=corr,
                cbar=True,
                mask=mask,
                annot=True,
                vmin=corr.values.min(),
                vmax=corr.values.max(),
                fmt=".1f")
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig