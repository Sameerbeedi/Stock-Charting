import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate_chart(df):
    fig, ax = plt.subplots()

    def update(num):
        ax.clear()
        data = df.iloc[:num+1]
        ax.plot(data['timestamp'], data['close'], color='black')
        ax.fill_between(data['timestamp'], data['low'], data['high'], alpha=0.3)
        ax.set_title(f"TSLA Candles up to {data['timestamp'].iloc[-1].date()}")

    ani = animation.FuncAnimation(fig, update, frames=len(df), repeat=False)
    ani.save("candlestick_animation.mp4", fps=10)
