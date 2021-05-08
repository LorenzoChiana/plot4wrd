import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

# plt.style.use('ggplot')

class AnimatedScatter(object):
    """Animated scatter plot using matplotlib.animations.FuncAnimation."""
    def __init__(self, numtimes=50, df_full=[], xfig=16.5,yfig=5):
        self.numtimes  = numtimes   # time instants of the simulation
        self.numpoints = 2          # num evolved poits
        self.colarray  = np.ones(2*numtimes)
        for i in range(numtimes):
           self.colarray[2*i] = 4
           self.colarray[2*i+1] = 1

        # inverto x con y per fare la figura larga
        self.stream = self.data_stream(df_full.y_1,df_full.x_1,
                                       df_full.y_2,df_full.x_2) # the data to plot

        # Setup figure
        self.fig, self.ax = plt.subplots(figsize=(xfig,yfig))
        img = plt.imread("stanza.PNG")
        self.ax.imshow(img,zorder=0, extent=[0, xfig, 0, yfig])
        # setup FuncAnimation.
        self.anim = animation.FuncAnimation(self.fig, self.update, interval=50, 
                                           init_func=self.setup_plot, blit=True,
                                           frames=self.numtimes-1)
        # se interessa il filmino mp4
        #self.anim.save('scatter.mp4', writer='ffmpeg')
        

    def data_stream(self, x1=[], y1=[], x2=[], y2=[]):
        """Return points up to a time"""
        xy = np.zeros((2*self.numtimes,2))
        i = 0
        while True:
            xy[2*i,0]=x1[i];
            xy[2*i,1]=y1[i]
            xy[2*i+1,0]=x2[i]
            xy[2*i+1,1]=y2[i]
            i = (i+1) % self.numtimes
            yield np.c_[xy[:,0], xy[:,1]]

    def setup_plot(self):
        """Initial drawing of the scatter plot."""
        x, y = next(self.stream).T
        c = 'tab:orange'
        s = 100
        self.scat = self.ax.scatter(x, y, c=c, s=s, 
                                    vmin=0, vmax=1,
                                    cmap="jet", edgecolor="k")
        self.ax.axis([0, 16.5, 0, 5])
        self.ax.set_ylabel('wouldbe x')
        self.ax.set_xlabel('wouldbe y')
        # return the updated artist to FuncAnimation
        # FuncAnimation expects a sequence of artists, thus the trailing comma.
        return self.scat,

    def update(self, i):
        """Update the scatter plot."""
        data = next(self.stream)

        # Set x and y data...
        self.scat.set_offsets(data[:, :2])
        # Set sizes...
        self.scat.set_sizes(np.ones(2*self.numtimes)*75)
        # Set colors..
        #self.scat.set_color('#22ff22')
        #self.scat.set_edgecolor('#000000')
        self.scat.set_array(self.colarray)

        # return the updated artist to FuncAnimation
        # FuncAnimation expects a sequence of artists, thus the trailing comma.
        return self.scat,
