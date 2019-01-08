import matplotlib.pyplot as plt
import numpy as np 

def ols(x, y, color_seq, var_name, str_data1, str_data2, **options):
    
    fig, (ax, ax2) = plt.subplots(1,2, figsize=(18, 6))

    #ax.plot(x, y, ' x', label='data')
    ax.plot(y, y, '--', label='_nolegend_')
    disp = ax.scatter(x, y, c=color_seq, marker='o', s=20, cmap='jet', label='Data')
    ax.set_aspect('equal')
    ax.set_xlim([-.01,.21])
    ax.set_ylim([-.01,.21])
    ax.set_xlabel(var_name + ' (' + str_data1 + ')')
    ax.set_ylabel(var_name + ' (' + str_data2 + ')')
    


    p = np.poly1d(np.polyfit(x, y, 1))
    ax.plot(x, p(x), '--', label='Fit result: {}'.format(p))
    ax.legend()

    residual = p(x) - y
    ax2.scatter(x, residual, c=color_seq, s=20, cmap='jet',)
    ax2.set_xlabel(var_name)
    ax2.set_ylabel('Residual')
    ax2.axhline(y=0, xmin=-1, xmax=1)

    if options.get("data_var") == "aeronet_aod":
        ax.set_xlim([-.01,.21])
        ax.set_ylim([-.01,.21])
        ax.set_xticks(np.arange(0, 0.25, step=0.05))
        ax2.set_xlim([-.01,.21])
        ax2.set_ylim([-.05,.05])
    elif options.get("data_var") == "ecmwf_aod":
        ax.set_xlim([.0,.16])
        ax.set_ylim([.0,.16])
        ax.set_xticks(np.arange(0, 0.16, step=0.05))
        ax2.set_xlim([-.01,.16])
        ax2.set_ylim([-.1,.07])
        ax2.set_xticks(np.arange(0, 0.16, step=0.05))
    elif options.get("data_var") == "aeronet_ang":
        ax.set_xlim([.69, 2.01])
        ax.set_ylim([.69, 2.01])
        ax.set_xticks(np.arange(.69, 2.01, step=0.2))
        ax2.set_xlim([.98, 1.91])
        ax2.axhline(y=0, xmin=-1, xmax=1)
    elif options.get("data_var") == "ecmwf_ang":
        ax.set_xlim([1.01, 2.01])
        ax.set_ylim([1.01, 2.01])


    plt.subplots_adjust(bottom= 0.1, right=0.8, top=0.9)
    cb = fig.colorbar(disp, ax=ax2)
    cb.ax.set_ylabel('Month of year')
    plt.show()

    # plt.savefig('results/regression_pearl_opal.png')




    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    r2 = ssreg / sstot
    
    
    return r2