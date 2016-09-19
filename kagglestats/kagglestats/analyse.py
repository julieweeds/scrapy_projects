__author__="juliewe"
import json,pandas as pd, matplotlib as plt


def analyse(filename):
    with open(filename) as json_data:
        d=json.load(json_data)

    mydict={}

    for dataset in d:
        filenames=dataset['filename']
        for filename in filenames:
            ext=filename.split('.')[-1]
            mydict[ext]=mydict.get(ext,0)+1
    print(mydict)
    df = pd.DataFrame(data=mydict.items())
    df.columns=['Data Format','Freq']

    pd.options.display.mpl_style = 'default'
    df_plot=df.plot(kind="bar",x=df["Data Format"],title="Data Formats for Hottest Kaggle Datasets",legend=False,fontsize=8)

    fig = df_plot.get_figure()
    fig.tight_layout()
    fig.savefig("data_formats.png")

if __name__=='__main__':
    items_filename="../items.json"
    analyse(items_filename)