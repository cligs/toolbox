#!/usr/bin/env python3
# Filename: visualize_metadata.py
# Author: #cf, #uh

"""
# Visualize some corpus properties.
"""

import pandas as pd
import matplotlib.pyplot as plt
import pygal
import os
import numpy as np
import itertools as iter

plot_colors = ["#3366CC","#DC3912","#FF9900","#109618","#990099","#3B3EAC","#0099C6","#DD4477","#66AA00","#B82E2E","#316395","#994499","#22AA99","#AAAA11","#6633CC","#E67300","#8B0707","#329262","#5574A6","#3B3EAC"]
        

def describe_corpus(wdir, metadatafile, category):
    """
    Plots corpus properties (default: bar chart, by decade).
    
    Author: cf, uh
    
    Arguments:
    
    wdir (string): current working directory
    metadatafile (string): filename of the metadata CSV file (in wdir)
    category (string): which metadata category to visualize
    
    Example of how to use this function:
        from extract import visualize_metadata        
        visualize_metadata.describe_corpus("/home/ulrike/novelas-hispam", "metadata.csv", "author-country")

    """
    with open(wdir+metadatafile, "r") as infile:
        metadata = pd.DataFrame.from_csv(infile, header=0)
        #print(metadata.head())
        
        ## Preparing data
        cat_xaxis = "decade"
        cat_bars = category 
        labels = sorted(set(metadata[cat_bars]))
        #print(labels)
        metadata = metadata[["idno",cat_xaxis,cat_bars]]
        grouped = metadata.groupby([cat_xaxis,cat_bars]).count()
        unstacked = grouped.unstack()
        unstacked.fillna("0", inplace=True)

        ## Plotting the data    
        """
        # matplotlib    
        myplot = grouped.unstack().plot(kind="bar", stacked=True, title="",figsize=(10, 8), color=plot_colors)
        myplot.set_title("Distribution of novels", fontsize=20)        
        myplot.set_xlabel("Decades", fontsize = 16)
        myplot.set_ylabel("Number",fontsize = 16)
        myplot.legend(labels) ## This is correct only by chance!! -- seems to be solved!
        plt.setp(plt.xticks()[1], rotation=40, fontsize = 14)   
        plt.tight_layout()
        figurename = "dist_by-"+category+".png"
        plt.savefig(wdir+figurename, dpi=300)
        plt.close()
        """
        
        # pygal
        my_style = pygal.style.Style(
		  background='white',
		  plot_background='white',
		  font_family = "FreeSans",
		  opacity = "1",
		  title_font_size = 20,
		  legend_font_size = 18,
		  label_font_size = 16,
		  colors=plot_colors)
          
        bar_chart = pygal.StackedBar(style=my_style, legend_at_bottom=True, print_values=False)
        bar_chart.title = 'Distribution of novels'
        bar_chart.x_title = "Decade"
        bar_chart.y_title = "Number of novels"
        
        md_unstacked = grouped.unstack()
        md_unstacked.fillna(0, inplace=True)
        
        bar_chart.x_labels = [str(i) for i in list(md_unstacked.index)]
        
        for label in labels:
            vals = md_unstacked["idno",label]
            bar_chart.add(label, vals.values)
        
        figurename = os.path.join(wdir, "dist_by-"+category+".svg")
        bar_chart.render_to_file(figurename)
        
        
        print("barchart " + category + " done")
        
        
        
        
def plot_pie(wdir, metadatafile, category):
    """
    Plots corpus properties (pie chart)
    
    Author: uh
    
    Arguments:
    
    wdir (string): current working directory
    metadatafile (string): filename of the metadata CSV file (in wdir)
    category (string): which metadata category to visualize
    
    Example of how to use this function:
        from extract import visualize_metadata        
        visualize_metadata.plot_pie("/home/ulrike/novelas-hispam", "metadata.csv", "subgenre_x")
    """
    with open(wdir+metadatafile, "r") as infile:
        metadata = pd.DataFrame.from_csv(infile, header=0)
                
        #plot_labels = sorted(set(metadata[category]))
        data_grouped = metadata.groupby([category]).count()
        data_unstacked = data_grouped.unstack()
        data_plot = data_unstacked.idno.sort_values()
        
        
        myplot = data_plot.plot(kind="pie", figsize=(7,7), colors=plot_colors, startangle=0, fontsize=9)
        # autopct='%1.f'
        myplot.set_title("Distribution of novels", fontsize=18, y=1.03)
        myplot.set_xlabel(" ",fontsize = 14, y=-1.06)
        myplot.set_ylabel(" ",fontsize = 14, x=-1.20)
        
        
        #myplot.legend(plot_labels)
        
        #plt.axis('equal')
        #plt.tight_layout()
        
        figurename = "piechart-"+category+".png"
        plt.savefig(wdir+figurename, dpi=300)
        plt.close()
        
    print("piechart done")

def chronological_heatmap(wdir, metadatafile, category, category_development = "year", amount_unities = 1):
    """
    Plots a heatmap with development of a category from a metadata file
    Author: jct

    Arguments:
    
    wdir (string): current working directory
    metadatafile (string): filename of the metadata CSV file (in wdir)
    category (string): which metadata category should be used in the y-axis
    category_development (string): which metadata category should be used for the x-axis. Defaul: year. Also possible: decade
    amount_unities (int): if we want to calculate using 1 or 2 years (default 1)    
    
    Example of how to use this function:
        from toolbox.extract import visualize_metadata        
        visualize_metadata.chronological_heatmap("/home/jose/cligs/ne/","metadata_beta-opt-obl.csv","author-name", amount_unities = 2)
    
    """
    #Metadata is imported
    metadata = pd.read_csv(wdir+metadatafile, encoding="utf-8", sep=",")
    
    if amount_unities == 2:
        metadata[str(amount_unities)+"_"+category_development] = ((metadata["year"] + (((-1)**(metadata["year"]+1))-1)/2)+1).map(lambda x: str(x)[0:4])
        category_development = str(amount_unities)+"_"+category_development

    #print(metadata)

    # We get the values for the vategory, normally author
    different_categories = sorted(list(set(metadata[category].tolist())))
    # We change the index 
    metadata = metadata.set_index([category])
    # The metadata is converted in a binear dataframe using index and the column selected, normally years
    metadata = pd.get_dummies(metadata[category_development])
    years = list(metadata.columns)
    # An empty dataframe with the category (authors) and the years is created
    table = pd.DataFrame(index = different_categories, columns = years)
    # We fill it with the sum of works from this category in this year
    for value in different_categories:
        for year in years:
            table[year][value] = metadata[year][value].sum()

    # We create a column with a sum
    table.loc["sum"] = table.sum()

    # We sort the table using the order of the columns, which corresponds to the order of the years
    table = table.sort(table.columns.tolist(), ascending=False)
    
    # We create the xticks
    summatory = table.loc["sum"].tolist()
    summatory = [int(i) for i in summatory]  
    columns = [int(i) for i in table.columns.tolist()]
    xticks = list(zip(columns, summatory))
    xticks = [list(elem) for elem in xticks]
    xticks = [str(str(elem[0])+" ("+str(elem[1])+")") for elem in xticks]
    # print(xticks)

    # We plot everything as a svg file    
    plt.figure(num=1,figsize=(20,10))
    plt.pcolor(table[1:], cmap='Reds', vmin=0, vmax=5, edgecolors="black")

    plt.yticks(np.arange(0.5, len(table.index), 1), table.index[1:])
    plt.xticks(np.arange(0.5, len(table.columns), 1), xticks , rotation=90)
    plt.title(r'Heatmap of the Development of works of '+category+" (" +category_development+")")

    plt.savefig(wdir+metadatafile[0:-4]+'.svg', dpi=300, format="svg")
    plt.show()


if __name__ == "__main__":
	describe_corpus(int(sys.argv[1]))

