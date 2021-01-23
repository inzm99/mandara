# %%

import matplotlib.pyplot as plt
import math

import streamlit as st

# %%

colorlist = ['#3ce03c', '#ffb400', '#ff9500', '#5fbeff', '#ff1daa', '#6bd13e', '#000000']

def drawmandara(n, pnum):
    # 索数番目のピンに糸をかける
    angle = 360 / n
    x = []
    y = []
    for p in pnum:
        for i in range(n + 1):
            th = math.radians(angle * i * p)
            x.append(100 * math.cos(th))
            y.append(100 * math.sin(th))
        plt.plot(x,y)
        x.clear()
        y.clear()

def drawline(n, lines, color):
    angle = 360 / n
    x = []
    y = []
    p_list = list(map(int,lines.split()))
    for p in p_list:
        th = math.radians(angle * p)
        x.append(100 * math.cos(th))
        y.append(100 * math.sin(th))

    plt.plot(x,y,color=color)

def drawinyo(n, start, color):
    angle = 360 / n
    p_list = []
    yin = start
    x = []
    y = []
    for i in range(n//2):
        p_list.append(yin + i)
        p_list.append(yin + n//2 + 2*i)
        p_list.append(yin + n//2 + 2*(i+1))
        p_list.append(yin + i + 1)
        
    for p in p_list:
        th = math.radians(angle * p)
        x.append(100 * math.cos(th))
        y.append(100 * math.sin(th))

    plt.plot(x,y,color=color)

def show_pin_number(n):
    angle = 360 / n
    for i in range(n):
        th = math.radians(angle * i)
        r = 105
        plt.text(r * math.cos(th), r * math.sin(th), str(i), fontsize=7, horizontalalignment='center')

def draw_circle(n,):
    fig2 = plt.figure(figsize=(8, 8))

    # disappear ticks
    plt.tick_params(labelbottom=False,
                    labelleft=False, 
                    labelright=False, 
                    labeltop=False,
                    bottom=False,
                    left=False,
                    right=False)
    ax = fig2.add_subplot(1,1,1)
    # ax = plt.axes()
    angle = 360 / n
    for i in range(n):
        th = math.radians(angle * i)
        ax.plot([0,100 * math.cos(th)], [0,100 * math.sin(th)], color='gray', linewidth=0.5)
    circle = plt.Circle((0,0),100, fill=False)
    ax.add_patch(circle)
    st.write(fig2)


# %%

if __name__ == "__main__":
    # set figure
    fig = plt.figure(figsize=(8, 8))

    # disappear ticks
    plt.tick_params(labelbottom=False,
                    labelleft=False, 
                    labelright=False, 
                    labeltop=False,
                    bottom=False,
                    left=False,
                    right=False)

    st.sidebar.header('MANDARA')
    n = st.sidebar.number_input('Number of Pins',value=35)
    
    # mandara
    st.sidebar.subheader('ぐるぐる')
    pnum_text = st.sidebar.text_input('Skip Number list', value='11 101 3 17')
    pnum = list(map(int,pnum_text.split()))

    # # inyo
    # st.sidebar.subheader('陰陽')
    # start = st.sidebar.number_input('Start Pin', value = 0)
    # color =st.sidebar.color_picker(f'Color', value=colorlist[6])
    # drawinyo(n, start, color)

    # free lines
    st.sidebar.subheader('追加')
    lines = st.sidebar.number_input('Number of Lines', value = 3)
    for l in range(1,lines+1):
        category = st.sidebar.selectbox(f'Category{str(l)}', options=['陰陽', '自由指定'])
        if category == '自由指定':
            lines = st.sidebar.text_input(f'Pin Number List {str(l)}', value='1 4 8 16')
            color =st.sidebar.color_picker(f'Color{str(l)}', value=colorlist[l % len(colorlist)])
            drawline(n, lines, color)
        elif category == '陰陽':
            start = st.sidebar.number_input(f'Start Pin{str(l)}', value = 0)
            color =st.sidebar.color_picker(f'Color{str(l)}', value=colorlist[l % len(colorlist)])
            drawinyo(n, start, color)

    drawmandara(n, pnum)

    # pin number
    if st.sidebar.checkbox('Show pin number'):
        show_pin_number(n)

    # if st.sidebar.button('OK'):
    st.write(fig)

    if st.sidebar.button('台紙'):
        draw_circle(n)


# plt.show()
