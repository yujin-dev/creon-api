import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_finance import candlestick_ohlc
import numpy as np

def draw_candlestick(df=None, index='time'):
    df['time'] = df['time'].apply(lambda x: int(x))
    if 'date' in df.columns:
        df = df.sort_values(by = ['date', 'time'])
    else:
        df = df.sort_values(by = ['date'])
    fig = plt.figure(figsize=(8,5))
    fig.set_facecolor("w")
    gs = gridspec.GridSpec(2, 1, height_ratios=[3,1])
    axes = [plt.subplot(gs[0])]
    axes.append(plt.subplot(gs[1], sharex = axes[0]))
    axes[0].get_xaxis().set_visible(False)
    index = np.arange(len(df.index))
    ohlc = df[['open', 'high', 'low', 'close']].astype(int).values
    dohlc = np.hstack((np.reshape(index, (-1, 1)), ohlc))
    candlestick_ohlc(axes[0], dohlc, width=0.5, colorup='r', colordown='b')
    axes[1].bar(index, df.volume, color = 'k', width=0.6, align='center')
    # axes[1].set_xticklabels(df[index].values, rotation=45, minor=False)
    plt.tight_layout()
    plt.show()
    return

if __name__ == "__main__":
    draw_candlestick()