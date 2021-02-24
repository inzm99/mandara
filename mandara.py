# %%
import base64
import matplotlib.pyplot as plt
import math
import numpy as np
import pandas as pd
import streamlit as st

colorlist = ['#3ce03c', '#ffb400', '#ff9500', '#5fbeff', '#ff1daa', '#6bd13e', '#000000']

class Mandara:
    def __init__(self) -> None:
        self.fig = plt.figure(figsize=(8, 8))
        plt.tick_params(labelbottom=False,
                labelleft=False, 
                labelright=False, 
                labeltop=False,
                bottom=False,
                left=False,
                right=False)
        self.pins = 35
        self.lines = 1
        self.categories = ['ぐるぐる', '自由指定', '陰陽']
        self.df_mandara = pd.DataFrame()
        self.set_values('default.csv')

    def set_values(self, filename):
        df = self.load_csv(filename)
        self.df_mandara = df[df['category'].isin(self.categories + ['pins'])].copy()
        # self.df_mandara.number.astype(int)
        self.pins = int(df[df['category'] == 'pins'].iat[0,1])
        # self.lines = int(self.df_mandara.shape[0] - 1)
        
    def add_line(self):
        df = pd.DataFrame([['ぐるぐる', 0, 0, 0, '#111111']], columns=['category', 'number', 'list', 'start', 'color'])
        self.df_mandara = self.df_mandara.append(df, ignore_index=True)#, df]).reset_index().set_index('index')

    def get_df(self):
        return self.df_mandara

    def save_csv(self, filename):
        self.df_mandara = self.df_mandara.drop('index', axis=1)
        self.df_mandara.to_csv(filename, encoding='utf-8_sig',index=False)
        # TODO

    def load_csv(self, filename) -> pd.DataFrame:
        df = pd.read_csv(filename, encoding='utf-8_sig')
        df = df.fillna(0)
        # st.write(df)
        return df

    def save_guru(self, p):
        # df = pd.DataFrame(['GURU', p, [], 0, self.tmp_color])
        df = pd.DataFrame([['GURU', int(p), np.nan, np.nan, 'aaa']], columns=['category', 'number', 'list', 'start', 'color'])
        self.df_mandara = pd.concat([self.df_mandara, df]).reset_index()
    
    def save_free(self, category, number, free_list, start, color):
        df = pd.DataFrame([[category, number, free_list, start, color]], columns=['category', 'number', 'list', 'start', 'color'])
        self.df_mandara = pd.concat([self.df_mandara, df])
        
    def drawmandara(self, pnum:int, color:str) -> None:
        """ guru guru """
        # st.sidebar.subheader('ぐるぐる')
        pnum = int(pnum)
        # self.save_guru(pnum)

        # 索数番目のピンに糸をかける
        angle = 360 / self.pins
        x = []
        y = []

        for i in range(self.pins + 1):
            th = math.radians(angle * i * pnum)
            x.append(100 * math.cos(th))
            y.append(100 * math.sin(th))
        plt.plot(x,y,color=color)
        x.clear()
        y.clear()

    def drawline(self, lines, color):
        angle = 360 / self.pins
        x = []
        y = []
        p_list = list(map(int,lines.split()))
        for p in p_list:
            th = math.radians(angle * p)
            x.append(100 * math.cos(th))
            y.append(100 * math.sin(th))

        plt.plot(x,y,color=color)

    def drawinyo(self, start, color):
        angle = 360 / self.pins
        p_list = []
        yin = start
        x = []
        y = []
        for i in range(self.pins//2):
            p_list.append(yin + i)
            p_list.append(yin + self.pins//2 + 2*i)
            p_list.append(yin + self.pins//2 + 2*(i+1))
            p_list.append(yin + i + 1)
            
        for p in p_list:
            th = math.radians(angle * p)
            x.append(100 * math.cos(th))
            y.append(100 * math.sin(th))

        plt.plot(x,y,color=color)

    def draw_circle(self):
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
        angle = 360 / self.pins
        for i in range(self.pins):
            th = math.radians(angle * i)
            ax.plot([0,100 * math.cos(th)], [0,100 * math.sin(th)], color='gray', linewidth=0.5)
        circle = plt.Circle((0,0),100, fill=False)
        ax.add_patch(circle)
        st.write(fig2)

    def show_pin_number(self):
        angle = 360 / self.pins
        for i in range(self.pins):
            th = math.radians(angle * i)
            r = 105
            plt.text(r * math.cos(th), r * math.sin(th), str(i), fontsize=7, horizontalalignment='center')

    def download_link(self, df, filename='mandara.csv') -> None:
        """Generates a link allowing the data in a given panda dataframe to be downloaded
        in:  dataframe
        out: href string
        """
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV file</a>'
        st.markdown(href, unsafe_allow_html=True)

        
    def __call__(self) -> None:
        # csv upload
        csvfile = st.file_uploader('Upload CSV File', type=['csv'])
        if csvfile:
            self.set_values(csvfile)

        self.pins = int(st.sidebar.number_input('Number Of Pins', value=self.pins, format ='%d'))
        self.df_mandara.loc[self.df_mandara['category'] == 'pins', 'number'] = self.pins

        self.lines = int(st.sidebar.number_input('Number of Lines', value = self.df_mandara.shape[0]-1, format = '%d', min_value=self.df_mandara.shape[0]-1))
        # self.df_mandara.loc[self.df_mandara['category']=='pins', 'number'] = self.pins


        # if st.sidebar.button('Add category'):
        for _ in range(self.lines - self.df_mandara.shape[0] + 1):
            self.add_line()
        
        # for debug
        # st.write(self.df_mandara)

        for row in self.df_mandara.itertuples(): #range(1,self.lines+1):
            pnum = 0
            lines = '0 1'
            start = 0
            if row.category == 'pins':
                continue
            st.sidebar.subheader(f'Category{row[0]}')
            category = st.sidebar.selectbox(f'Category{str(row[0])}', options=self.categories, index=self.categories.index(row.category))
            if category == 'ぐるぐる':
                pnum = st.sidebar.number_input(f'Skip Number{str(row[0])}', value=int(row.number), format='%d')
                color =st.sidebar.color_picker(f'Color{str(row[0])}', value=row.color)#colorlist[row[0] % len(colorlist)])
                self.drawmandara(pnum, color)
            elif category == '自由指定':
                lines = st.sidebar.text_input(f'Pin Number List {str(row[0])}', value=row.list)#'1 4 8 16')
                color =st.sidebar.color_picker(f'Color{str(row[0])}', value=row.color)#colorlist[row[0] % len(colorlist)])
                # self.save_free(category, np.nan, lines, np.nan, color)
                self.drawline(lines, color)
            elif category == '陰陽':
                start = st.sidebar.number_input(f'Start Pin{str(row[0])}', value = row.start)
                color =st.sidebar.color_picker(f'Color{str(row[0])}', value=row.color)#colorlist[l % len(colorlist)])
                # self.save_free(category, np.nan, np.nan, start, color)
                self.drawinyo(start, color)
            self.df_mandara.at[row[0], 'category'] = category
            self.df_mandara.at[row[0], 'number'] = pnum
            self.df_mandara.at[row[0], 'list'] = lines
            self.df_mandara.at[row[0], 'start'] = start
            self.df_mandara.at[row[0], 'color'] = color


        # pin number
        if st.sidebar.checkbox('Show pin number'):
            self.show_pin_number()
        
        # plot fig
        st.write(self.fig)

        # 台紙
        if st.sidebar.checkbox('台紙'):
            self.draw_circle()

        # csv download
        self.download_link(self.df_mandara)
        # if st.button('CSV Download'):
        #     filename = 'mandara.csv'
        #     self.save_csv(filename)

# %%

if __name__ == "__main__":
    st.sidebar.title('MANDARA')
    # n = st.sidebar.number_input('Number of Pins', value=35)
    
    # # mandara
    # st.sidebar.subheader('ぐるぐる')
    # pnum_text = st.sidebar.text_input('Skip Number list', value='11 101 3 17')
    # pnum = list(map(int,pnum_text.split()))

    mandara = Mandara()
    # mandara.save_guru(pnum)# df = save_df('GURU', p, [], 0, '#3ce03c')

    # # inyo
    # st.sidebar.subheader('陰陽')
    # start = st.sidebar.number_input('Start Pin', value = 0)
    # color =st.sidebar.color_picker(f'Color', value=colorlist[6])
    # drawinyo(n, start, color)

    # free lines
    # st.sidebar.subheader('追加')
    # lines = st.sidebar.number_input('Number of Lines', value = 3)
    # for l in range(1,lines+1):
    #     category = st.sidebar.selectbox(f'Category{str(l)}', options=['陰陽', '自由指定'], index=1)
    #     if category == '自由指定':
    #         lines = st.sidebar.text_input(f'Pin Number List {str(l)}', value='1 4 8 16')
    #         color =st.sidebar.color_picker(f'Color{str(l)}', value=colorlist[l % len(colorlist)])
    #         mandara.save_free(category, np.nan, lines, np.nan, color)
    #         drawline(n, lines, color)
    #     elif category == '陰陽':
    #         start = st.sidebar.number_input(f'Start Pin{str(l)}', value = 0)
    #         color =st.sidebar.color_picker(f'Color{str(l)}', value=colorlist[l % len(colorlist)])
    #         mandara.save_free(category, np.nan, np.nan, start, color)
    #         drawinyo(n, start, color)

    # drawmandara(n, pnum)



    # # if st.sidebar.button('OK'):



    mandara()
    st.write(mandara.get_df())
