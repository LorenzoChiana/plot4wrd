import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys     # for comand line options
import animate # needs conda install fsspec

def init_df(df):
    df = df.replace('-', np.nan)
    df.time = df.time.astype('datetime64[ns]')
    df.x = df.x.astype(float)
    df.y = df.y.astype(float)
    df.z = df.z.astype(float)
    df.quality = df.quality.astype(float)
    # set time ad index of time series
    df.set_index('time', inplace=True)
    # fake distance
    df['distance'] = df[['x','y']].mean(axis=1)
    return df

def parse_cv_data():
    df = pd.DataFrame(pd.read_csv(source_path + cv_file_name,
                                  sep=',',
                                  names=['time', 'tagID', 'x', 'y', 'z', 'quality'],
                                  header=None))
    return init_df(df)

def parse_uwb_data():
    # keep only the lines that contain the 0) key string
    oldFormat = False
    if(oldFormat):
    # takes data by row
       df = pd.DataFrame(pd.read_csv(source_path + uwb_file_name,
                                     sep='\n',
                                     names=['time'],
                                     header=None))
       df = df[df['time'].str.contains('0\)')==True]
       # parse the various data contained in the key lines
       df['time'] = df['time'].map(lambda x: x.replace('[','|')
                                           .replace(']','')
                                           .replace('0)','')
                                           .replace(',x0D','')
                                           .replace('   ','|')
                                           .replace(',','|')
                                           .replace('|','',1))
       df[['time', 'tagID', 'x', 'y', 'z', 'quality']] = df.time.str.split('|', expand=True)
    else:
       df = pd.DataFrame(pd.read_csv(source_path + uwb_file_name,
                                     sep=',',
                                     names=['time', 'tagID', 'x', 'y', 'z', 'quality','nix'],
                                  header=None))
       df = df.drop(columns=['nix'])
    return init_df(df)

def plotStanza(xfig, yfig, fig=None):
    if fig is None:
        fig, ax = plt.subplots(figsize=(xfig, yfig))
    ax = plt.gca()
    img = plt.imread("../stanza.png")
    ax.imshow(img, zorder=0, extent=[0, xfig, 0, yfig])
    
def plotPath():
    xfig = 16.5       # room length
    yfig = 5          # room width
    fig, ax = plt.subplots(figsize=(xfig, yfig))
    
    ax.plot(anchors_df.y, anchors_df.x, 'rD', markersize=12)
    for anchor_name, anchor_pos in anchors_df.iterrows():
        ax.annotate(anchor_name, (anchor_pos.y, anchor_pos.x), xytext=(anchor_pos.y+0.25, anchor_pos.x), fontsize=18)
    
    ax.plot(cameras_df.y, cameras_df.x, 'kD', markersize=12)
    for cameras_name, cameras_pos in cameras_df.iterrows():
        ax.annotate(cameras_name, (cameras_pos.y, cameras_pos.x), xytext=(cameras_pos.y+0.25, cameras_pos.x-0.25), fontsize=18, color='black')
    
    ax.scatter(dfmerged['y_1'], dfmerged['x_1'], c="blue", label=dfmerged['tagID_1'], edgecolors='none')
    ax.scatter(dfmerged['y_2'], dfmerged['x_2'], c="orange", label=dfmerged['tagID_2'], edgecolors='none')
    
    
    #a = animate.AnimatedScatter(numtimes,dfmerged,xfig,yfig)
    plotStanza(xfig, yfig, fig)
    plt.show()

def main():  
    global anchors_df
    anchors_df = pd.DataFrame(np.array([[0, 12.1], [0, 4.6], [2.5, 0], [4.95, 4.6], [4.95, 12.1], [2.5, 16.9]]),
                              index=['CC90','D20C','CB1D','9028','198A','8418'],
                              columns=['x', 'y'])
    global cameras_df 
    cameras_df = pd.DataFrame(np.array([[2.35, 7.5]]),
                              index=['camera1'],
                              columns=['x', 'y'])
    
    uwb_df = parse_uwb_data()
    uwb_df.index = uwb_df.index.floor('10ms') # keep time down to centliseconds
    uwb_df.x = 5 - uwb_df.x
    
    cv_df = parse_cv_data()
    cv_df.index = cv_df.index.floor('10ms') # keep time down to centiseconds
    cv_df.x = 5 - cv_df.x
    
    global dfmerged 
    dfmerged = pd.merge_ordered(cv_df,uwb_df,on="time",suffixes=("_1","_2"), fill_method="ffill")
    #ax = plt.gca()
    
    numtimes = len(dfmerged)
    plotPath()
    
# Program entry point
if __name__ == "__main__":
    print("init")
    source_path=""
    cv_file_name=""
    uwb_file_name=""
    
    if len(sys.argv)>1:
       source_path=sys.argv[1]
       cv_file_name=sys.argv[2]
       uwb_file_name=sys.argv[3]
    else:
       source_path='c://AAAToBackup//progetti//4wrd//data//20201117//201117_Test1_EG//'
       cv_file_name='CV_L2_201117.csv'
       uwb_file_name='UWB_L2_201117.csv'

    main()
    print("end")
