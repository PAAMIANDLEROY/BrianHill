#Import Part
import yaml #beug with streamlit. Need correction
import matplotlib.pyplot as plt
import matplotlib as mpl
import base64
import numpy as np
from pywaffle import Waffle as Wf
#import class_range_slider as crs
#
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
import streamlit as st
import streamlit.components.v1 as components
import mpld3
#import fonction and Script
import algo as algo
import time
import math


#Config
st.set_page_config(
    page_title="Brian Hill", layout="wide", page_icon="images/flask.png"
)
if 'finish' not in st.session_state:
    st.session_state.finish=0
if 'config' not in st.session_state:
    st.session_state.config={}
if 'cmpt_page' not in st.session_state:
    st.session_state.cmpt_page=-3
if 'cmpt_exp' not in st.session_state:
    st.session_state.cmpt_exp=0
if 'save_bet' not in st.session_state:
    st.session_state.save_bet=[]
if 'all_save_bet' not in st.session_state:
    st.session_state.all_save_bet=[]
if 'new_bet' not in st.session_state:
    st.session_state.new_bet=[30,30]
if 'histo' not in st.session_state:
    st.session_state.histo=[]
if 'histo_opts' not in st.session_state:
    st.session_state.histo_opts=[]
if 'slider_value' not in st.session_state:
    st.session_state.slider_value=[30,30]
value_grey=[0.7]
color_Green='#54cc33'
color_Yellow='#e4e805'
color_Red='#ff0000'
color_Blue='#0000ff'
color_Grey='#b3b3b3'
color_White='#ffffff'
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))




#Useful function
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def RSlid():
    a=0.7
    color_left='green'
    color_middle='red'
    color_right='blue'
    ax_slider=plt.axes([0.1,0.5,0.75,0.3])#, facecolor=axcolor)
    defaults={'facecolor': 'blue', 'edgecolor': 'red', 'size': 30}
    valinit=[30,75]
    sfreq = RangeSlider(ax_slider, 'DoubleSlider', 1, 100,valstep=1,valinit=valinit,handle_style=defaults,color_left=color_left,color_middle=color_middle,color_right=color_right)#([a,a,a],[0.,0.,1.]))
    #plt.show()


def up_cmpt():
    st.session_state.cmpt_page+=1


def label(xy, text):
    y = xy[1] - 0.15  # shift y-value for label so that it's below the artist
    plt.text(xy[0], y, text, ha="center", family='sans-serif', size=14)
def validation(values,opts):
    st.session_state.histo.append(values)
    bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=algo.main(values,opts)
    bet=[int(bet[0]),int(bet[1])]
    
    return bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile




####################################################block 1 => ###########################



def front_choice_bias(Winning_amount,Number_of_ball,Freq_green):
    blue=st.session_state.new_bet[1]
    red=st.session_state.new_bet[0]
    grey=100-blue-red
    values_recup=st.session_state.slider_value
    col1,col3, col2 = st.columns([2,1,2])
    with col1:
        
        col1a,col1b=st.columns([2.3,3])#COL1A;COL1B
        with col1a:
            st.subheader("  ")
            st.write(str(Number_of_ball)+" draws were made, with "+str(int(Number_of_ball*Freq_green))+" green balls.")
            st.write("The others were yellow")
            fig3 = plt.figure(
                FigureClass=Wf,
                rows=int(math.sqrt(Number_of_ball)),
                #columns=10,  # Either rows or columns could be omitted
                values=[int(Number_of_ball*Freq_green), Number_of_ball-int(Number_of_ball*Freq_green)],
                colors=[color_Green,color_Yellow],
                characters='⬤',
                font_size=20)
            st.pyplot(fig3)
        with col1b:
            st.subheader("  ")
            st.subheader("Option A")
            fig1, ax1=plt.subplots()#figsize=(4,4))
            x1,y1 = ([0,-0.1,0], [-0.1,0,0.1])
            line1 = mpl.lines.Line2D(x1,y1, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(0.1, 0.1, "Green: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(0.1, -0.1, "Yellow: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax1.add_line(line1)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig1)
    with col3:
        st.subheader("  ")
        st.subheader("  ")
        st.subheader("  ")
        choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True,index=np.random.randint(2))
        choice='A' if choice=='Option A' else 'B'
        st.write("Option "+str(choice)+" is selected")
        if st.button(str(st.session_state.cmpt_page+1)):
            pass
        st.write("Experiment number "+str(st.session_state.cmpt_exp+1))
        button_val=st.button('Validation',key='val1')
        if button_val:
            button_val=False
            up_cmpt()
            st.session_state.save_bet.append([red,blue])
            st.session_state.histo_opts.append(choice)
            print(st.session_state.histo_opts)
            if st.session_state.cmpt_page%2==0:
                opts=st.session_state.histo_opts[-2:]
                bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=validation([red,blue],opts)
                st.session_state.new_bet=bet
                #st.session_state.save_bet=bet
                if finished:
                    algo.init()
                    st.session_state.histo.append(st.session_state.histo_opts)
                    st.session_state.all_save_bet.append(st.session_state.save_bet)
                    print(st.session_state.histo)
                    print(st.session_state.all_save_bet)
                    st.session_state.save_bet=[]
                    st.session_state.histo_ops=[]
                    st.session_state.new_bet=[30,30]
                    st.session_state.cmpt_exp+=1
                    st.session_state.cmpt_page=0
                    st.write("It's finished, we will send the results")
            st.experimental_rerun()
    with col2:
        
        col2a,col2b=st.columns([3,2.3])
        with col2b:
            st.subheader("  ")
            st.subheader("Option B")
            fig4 = plt.figure(
                FigureClass=Wf,
                rows=10,
                columns=10,  # Either rows or columns could be omitted
                values=[red,grey,blue],
                colors=[color_Red,color_Grey,color_Blue],
                characters='⬤',
                font_size=20,
                )
            st.pyplot(fig4)
        with col2a:
            st.subheader("  ")
            st.subheader("  ")
            st.subheader("  ")
            fig3, ax3=plt.subplots()#figsize=(4,4))
            x3,y3 = ([0,0.1,0], [-0.1,0,0.1])
            line3 = mpl.lines.Line2D(x3,y3, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(-0.1, 0.1, "Red: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(-0.1, -0.1, "Blue: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax3.add_line(line3)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig3)    
    return 0

################################################<=block1###############block 2 => ############################################################################

def front_choice_unbias(Winning_amount,Number_of_ball,Freq_green):
    blue=st.session_state.new_bet[1]
    red=st.session_state.new_bet[0]
    grey=100-blue-red
    values_recup=st.session_state.slider_value
    col1,col3, col2 = st.columns([2,1,2])
    with col1:
        
        col1a,col1b=st.columns([2.3,3])#COL1A;COL1B
        with col1a:
            st.subheader("  ")
            st.write(str(Number_of_ball)+" draws were made, with "+str(int(Number_of_ball*Freq_green))+" green balls.")
            st.write("The others were yellow")
            fig3 = plt.figure(
                FigureClass=Wf,
                rows=int(math.sqrt(Number_of_ball)),
                #columns=10,  # Either rows or columns could be omitted
                values=[int(Number_of_ball*Freq_green), Number_of_ball-int(Number_of_ball*Freq_green)],
                colors=[color_Green,color_Yellow],
                characters='⬤',
                font_size=20)
            st.pyplot(fig3)
        with col1b:
            st.subheader("  ")
            st.subheader("Option A")
            fig1, ax1=plt.subplots()#figsize=(4,4))
            x1,y1 = ([0,-0.1,0], [-0.1,0,0.1])
            line1 = mpl.lines.Line2D(x1,y1, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(0.1, 0.1, "Green: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(0.1, -0.1, "Yellow: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax1.add_line(line1)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig1)
    with col3:
        if not st.session_state.finish:
            st.subheader("  ")
            st.subheader("  ")
            st.subheader("  ")
            choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True,index=np.random.randint(2))
            choice='A' if choice=='Option A' else 'B'
            st.write("Option "+str(choice)+" is selected")
            st.write("Experiment number "+str(st.session_state.cmpt_exp+1))
            if st.button(str(st.session_state.cmpt_page+1)):
                pass
            button_val=st.button('Validation',key='val1')
            if button_val:
                button_val=False
                up_cmpt()
                st.session_state.save_bet.append([red,blue])
                st.session_state.histo_opts.append(choice)
                if st.session_state.cmpt_page%2==0:
                    opts=st.session_state.histo_opts[-2:]
                    bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=validation(st.session_state.slider_value,opts)
                    print(bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile)
                    st.session_state.new_bet=bet##a verifier
                    st.session_state.finish=finished
                    print('fini ',finished)
                    st.experimental_rerun()
                else:
                    st.experimental_rerun()
                    #st.session_state.save_bet=bet
    if st.session_state.finish:
        finish_part(red,blue,grey)
        
    with col2:
        
        col2a,col2b=st.columns([3,2.3])
        with col2b:
            st.subheader("  ")
            st.subheader("Option B")
            fig4 = plt.figure(
                FigureClass=Wf,
                rows=10,
                columns=10,  # Either rows or columns could be omitted
                values=[red,grey,blue],
                colors=[color_Red,color_Grey,color_Blue],
                characters='⬤',
                font_size=20,
                )
            st.pyplot(fig4)
        with col2a:
            st.subheader("  ")
            st.subheader("  ")
            st.subheader("  ")
            fig3, ax3=plt.subplots()#figsize=(4,4))
            x3,y3 = ([0,0.1,0], [-0.1,0,0.1])
            line3 = mpl.lines.Line2D(x3,y3, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(-0.1, 0.1, "Red: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(-0.1, -0.1, "Blue: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax3.add_line(line3)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig3)
    return 0
def finish_part(red,blue,grey):
    fig4b = plt.figure(figsize=(10,1))
    ax4b = fig4b.add_axes([0.05, 0.475, 0.9, 0.15])
    cmap = mpl.colors.ListedColormap([color_White,color_Blue])
    bounds = [0,red+grey,100]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb4b = mpl.colorbar.ColorbarBase(ax4b, cmap=cmap,
                                    norm=norm,
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='horizontal')
    ax4b.axis('off')
    st.pyplot(fig4b)
    fig4a = plt.figure(figsize=(10,1))
    ax4a = fig4a.add_axes([0.05, 0.475, 0.9, 0.15])
    cmap = mpl.colors.ListedColormap([color_Red,color_White])
    bounds = [0,red,100]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb4a = mpl.colorbar.ColorbarBase(ax4a, cmap=cmap,
                                    norm=norm,
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='horizontal')
    ax4a.axis('off')
    st.pyplot(fig4a)
            
    options=list(range(101))
    st.write('Option A')
    values_recup = st.select_slider(' ',options, value = (red,100-blue),format_func=lambda x:'')#on_change=_update_slider
    values_recup=list(values_recup)
    values_recup[1]=100-values_recup[1]
    st.session_state.slider_value=values_recup
    colR,colW, colB = st.columns([1.6,2,1])
    with colR:
        st.write('The Red value is equal to '+str(values_recup[0]))
    with colW:
        st.write("The Red value can't inferior than "+str(red)+". The Blue value can't inferior than "+str(blue))
        st.write("You can change only one color")
    with colB:
        st.write('The Blue value is equal to '+str(values_recup[1]))
    ColorMinMax = st.markdown(''' <style> div.stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] > div {
    background: rgb(1 1 1 / 0%); } </style>''', unsafe_allow_html = True)
    Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
    background-color: rgb(14, 38, 74); box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)
    #background: linear-gradient(to right, rgba(151, 166, 195, 0.25) 0%, rgba(151, 166, 195, 0.25) 20%, rgb(255, 75, 75) 20%, rgb(255, 75, 75) 70%, rgba(151, 166, 195, 0.25) 70%, rgba(151, 166, 195, 0.25) 100%);
    #st.write(values_recup[0],values_recup[1],t)
    r,g,b = int(values_recup[0]),100-int(values_recup[0])-int(values_recup[1]),int(values_recup[1])
    #red_rgb=str(hex_to_rgb(color_Red))
    #blue_rgb=str(hex_to_rgb(color_Blue))
    col1 = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div{{
    background: linear-gradient(90deg, red 0% {r}%, 
                            grey {r}% {100-b}%, 
                            blue {100-b}% 100%); }} </style>'''#rgb'''+red_rgb+''' 
    ColorSlider = st.markdown(col1, unsafe_allow_html = True)
    st.write('Option B')
    fig2a = plt.figure(figsize=(10,1))
    ax2a = fig2a.add_axes([0.05, 0.475, 0.9, 0.15])
    cmap = mpl.colors.ListedColormap([color_Blue,color_White])
    bounds = [0,red+grey,100]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb4a = mpl.colorbar.ColorbarBase(ax4a, cmap=cmap,
                                    norm=norm,
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='horizontal')
    ax2a.axis('off')
    st.pyplot(fig4a)
    fig2b = plt.figure(figsize=(10, 1))
    ax2b = fig2b.add_axes([0.05, 0.475, 0.9, 0.15])
    cmap = mpl.colors.ListedColormap([color_White,color_Red])
    bounds = 100-np.array([0,red,100])
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb2b = mpl.colorbar.ColorbarBase(ax2b, cmap=cmap,
                                    norm=norm,
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='horizontal')
    ax2b.axis('off')
    st.pyplot(fig2b)
    button_val_rez=st.button('Validation result')
    if button_val_rez:
        if values_recup[0]<red:
            st.write('red is too low')
        elif values_recup[1]<blue:
            st.write('blue is too low')
        elif values_recup[1]!=blue and values_recup[0]!=red:
            st.write('You can move only one handles')
        else:
            st.session_state.histo.append(st.session_state.histo_opts)
            st.session_state.all_save_bet.append(st.session_state.save_bet)
            print(st.session_state.histo)
            print(st.session_state.all_save_bet)
            st.session_state.save_bet=[]
            st.session_state.histo_ops=[]
            st.session_state.finish=0
            algo.init()
            st.session_state.new_bet=[30,30]
            st.session_state.cmpt_exp+=1
            st.session_state.cmpt_page=0
            st.write("It's finished, we will send the results")
            st.experimental_rerun()

    return 0


#############################################<=block2###################block 3=> ###############################################

def front_choice_stated(Winning_amount,Number_of_ball,Freq_green):
    blue=st.session_state.new_bet[1]
    red=st.session_state.new_bet[0]
    grey=100-blue-red
    values_recup=st.session_state.slider_value
    col1,col3, col2 = st.columns([2,1,2])
    with col1:
        
        col1a,col1b=st.columns([2.3,3])#COL1A;COL1B
        with col1a:
            st.subheader("  ")
            st.subheader(str(Number_of_ball)+" draws were made, with "+str(int(Number_of_ball*Freq_green))+" green balls.")
            st.subheader("The others were yellow")
            fig3 = plt.figure(
                FigureClass=Wf,
                rows=int(math.sqrt(Number_of_ball)),
                #columns=10,  # Either rows or columns could be omitted
                values=[int(Number_of_ball*Freq_green), Number_of_ball-int(Number_of_ball*Freq_green)],
                colors=[color_Green,color_Yellow],
                characters='⬤',
                font_size=20)
            st.pyplot(fig3)
        with col1b:
            st.subheader("  ")
            st.subheader("Option A")
            fig1, ax1=plt.subplots()#figsize=(4,4))
            x1,y1 = ([0,-0.1,0], [-0.1,0,0.1])
            line1 = mpl.lines.Line2D(x1,y1, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(0.1, 0.1, "Green: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(0.1, -0.1, "Yellow: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax1.add_line(line1)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig1)
    with col3:
        st.subheader("  ")
        st.subheader("  ")
        st.subheader("  ")
        #choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True,index=np.random.randint(2))
        #choice='A' if choice=='Option A' else 'B'
        #st.write("     You choose option "+str(choice))
        if st.button(str(st.session_state.cmpt_page+1)):
            pass
        button_val=st.button('Validation')
        if button_val:
            button_val=False
            up_cmpt()
            st.session_state.save_bet=values_recup
            st.session_state.histo_opts.append(choice)
            if st.session_state.cmpt_page%2==0:
##                opts=st.session_state.histo_opts[-2:]
##                print(opts)
##                print(st.session_state.histo_opts)
##                bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=validation(values_recup,opts)
                finished=1
                st.session_state.save_bet=bet##a verifier
                #st.session_state.save_bet=bet
            if finished:
                st.session_state.cmpt_exp+=1
                st.write("It's finished, we will send the results")
            else:
                st.experimental_rerun()
    with col2:
        
        col2a,col2b=st.columns([3,2.3])
        with col2b:
            st.subheader("  ")
            st.subheader("Option B")
            fig4 = plt.figure(
                FigureClass=Wf,
                rows=10,
                columns=10,  # Either rows or columns could be omitted
                values=[red,grey,blue],
                colors=[color_Red,color_Grey,color_Blue],
                characters='⬤',
                font_size=20,
                )
            st.pyplot(fig4)
        with col2a:
            st.subheader("  ")
            st.subheader("  ")
            st.subheader("  ")
            fig3, ax3=plt.subplots()#figsize=(4,4))
            x3,y3 = ([0,0.1,0], [-0.1,0,0.1])
            line3 = mpl.lines.Line2D(x3,y3, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(-0.1, 0.1, "Red: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(-0.1, -0.1, "Blue: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax3.add_line(line3)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig3)    

    if st.session_state.cmpt_page>=2:

        fig4b = plt.figure(figsize=(10,1))
        ax4b = fig4b.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap([color_White,color_Blue])
        bounds = [0,red+grey,100]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb4b = mpl.colorbar.ColorbarBase(ax4b, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        ax4b.axis('off')
        st.pyplot(fig4b)
        fig4a = plt.figure(figsize=(10,1))
        ax4a = fig4a.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap([color_Red,color_White])
        bounds = [0,red,100]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb4a = mpl.colorbar.ColorbarBase(ax4a, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        ax4a.axis('off')
        st.pyplot(fig4a)
                
        options=list(range(101))
        st.write('Option A')
        values_recup = st.select_slider(' ',options, value = (red,100-blue),format_func=lambda x:'')#on_change=_update_slider
        values_recup=list(values_recup)
        values_recup[1]=100-values_recup[1]
        st.session_state.slider_value=values_recup
        colR,colW, colB = st.columns([1.6,2,1])
        with colR:
            st.write('The Red value is equal to '+str(values_recup[0]))
        with colW:
            st.write("The Red value can't superior than "+str(red)+". The Blue value can't superior than "+str(blue))
        with colB:
            st.write('The Blue value is equal to '+str(values_recup[1]))
        ColorMinMax = st.markdown(''' <style> div.stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] > div {
        background: rgb(1 1 1 / 0%); } </style>''', unsafe_allow_html = True)
        Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
        background-color: rgb(14, 38, 74); box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)
        #background: linear-gradient(to right, rgba(151, 166, 195, 0.25) 0%, rgba(151, 166, 195, 0.25) 20%, rgb(255, 75, 75) 20%, rgb(255, 75, 75) 70%, rgba(151, 166, 195, 0.25) 70%, rgba(151, 166, 195, 0.25) 100%);
        #st.write(values_recup[0],values_recup[1],t)
        r,g,b = int(values_recup[0]),100-int(values_recup[0])-int(values_recup[1]),int(values_recup[1])
        #red_rgb=str(hex_to_rgb(color_Red))
        #blue_rgb=str(hex_to_rgb(color_Blue))
        col1 = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div{{
        background: linear-gradient(90deg, red 0% {r}%, 
                                grey {r}% {100-b}%, 
                                blue {100-b}% 100%); }} </style>'''#rgb'''+red_rgb+''' 
        ColorSlider = st.markdown(col1, unsafe_allow_html = True)
        st.write('Option B')
        fig2a = plt.figure(figsize=(10,1))
        ax2a = fig2a.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap([color_Blue,color_White])
        bounds = [0,red+grey,100]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb4a = mpl.colorbar.ColorbarBase(ax4a, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        ax2a.axis('off')
        st.pyplot(fig4a)
        fig2b = plt.figure(figsize=(10, 1))
        ax2b = fig2b.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap([color_White,color_Red])
        bounds = 100-np.array([0,red,100])
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb2b = mpl.colorbar.ColorbarBase(ax2b, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        ax2b.axis('off')
        st.pyplot(fig2b)
        if st.button('to_result'):
            st.session_state.cmpt_exp+=1
            st.experimental_rerun()
    else:
        pass

    return 0

#############################################<=block3############################################################################


         
        
def process(Winning_amount):
    if st.session_state.cmpt_page==-3:
##        Nb_group=st.number_input('Number of group?',value=1)
        id_number=st.text_input('What is your ID?')
        name=st.text_input('What is your first and last name?')
        subject=st.text_input('Subject')
        age=st.number_input('What is your age?',value=18)
        gender=st.radio("What is your gender?",('Men','Female','Other'))
##        Freq_green_input=st.number_input("number of green ball",0,100,value=int(Freq_green*100))
##        Freq_green=Freq_green_input/100
##        Winning_amount=st.number_input("Winning_amount",value=Winning_amount)
        if st.button('Validation'):
            if st.session_state.cmpt_page==-3:
                st.session_state.pers_info=[id_number,name,subject,age,gender]
            up_cmpt()
            st.experimental_rerun()
    elif st.session_state.cmpt_page==-2:
        tirage_groupe=np.random.randint(6)
        st.session_state.config=load_config(tirage_groupe)
        st.write(tirage_groupe+1)
        st.write('inserer une vidéo')
        st.video("https://www.youtube.com/watch?v=0lROkD7pVz0")
        st.write('inserer une vidéo')
        st.video("https://www.youtube.com/watch?v=P-km9ksZkyg")
        if st.button('Validation'):
            up_cmpt()
            st.experimental_rerun()
    elif st.session_state.cmpt_page==-1:
        st.write("Enter something")
        if st.button('Validation'):
            up_cmpt()
            st.experimental_rerun()
    elif st.session_state.cmpt_page==-5:
        st.write(st.session_state.pers_info)
        st.write(st.session_state.histo_opts)
        st.write(st.session_state.histo)
        st.write("Thank you")
        st.write("Add tirage session")
        if st.button('Send Result'):
            st.write('to dropbox')
        st.write('Owner Brian Hill')
        st.write('Contributor : Pierre-Antoine Amiand-Leroy')
        st.write('Thanks to Hi! PARIS')
    elif st.session_state.cmpt_page>=0 and st.session_state.cmpt_exp<=len(st.session_state.config):
        dev=st.button('go to 4')
        if dev:
            st.session_state.cmpt_page=-5            
        config_exp=st.session_state.config[st.session_state.cmpt_exp]
        if config_exp[0][:-1]=='Choice_bias':
            front_choice_bias(Winning_amount,config_exp[1],config_exp[2])
        elif config_exp[0][:-1]=='Choice_unbias':
            front_choice_unbias(Winning_amount,config_exp[1],config_exp[2])
        elif config_exp[0][:-1]=='Choice_stated':
            front_choice_stated(Winning_amount,config_exp[1],config_exp[2])
    else:
        st.session_state.cmpt_page=-5
        st.experimental_rerun()
#beug with streamlit. Need correction
def load_yaml():
    with open('parameter.yml', 'r', encoding='utf8') as file:
        data = yaml.safe_load(file)
    return data

def load_config(tirage_groupe):
    data=load_yaml()
    liste_option=["A1","A2","B1","B2","C1","C2"]
    option=liste_option[tirage_groupe]
    config=data[option]
    list_key=list(config.keys())
    config_list=[[key]+config[key] for key in list_key]
    return config_list
    
    

def main():
    #data=load_yaml()#beug with streamlit. Need correction
    if 'pers_info' not in st.session_state:
      st.session_state.pers_info=[]

    def hide_header_footer():
        hide_streamlit_style = """
                    <style>
                    footer {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    #hide_header_footer()
    #st.header("# Brian Hill 🖥")
##    st.subheader(
##        """
##        Decision  🧪
##        """
##    )
##    experiment_front()
    Winning_amount=20
    process(Winning_amount)



if __name__=='__main__':
    main()

#st.markdown(" ")
#st.markdown("### HEC Researcher Brian Hill " )
#st.image(['images/1.png'], width=230,caption=["Vadim Malvone"])

#st.markdown('# Made by Hi!Paris')
#images = Image.open('./images/hi-paris.png')
#st.image(images, width=250)
#st.write('    ')
#st.markdown('# Contributors:')
#PA=Image.open('./images/PA.jpg')
#Pierre=Image.open('./images/Pierre.jpg')
#GAE=Image.open('./images/gaetan.png')
#st.image([PA,GAE,Pierre],width=110)

def to_dropbox():
    import dropbox

    filename = "argument.csv"

    # Create a dropbox object using an API v2 key
    dbx = dropbox.Dropbox('k4hp6g0k9nhfo8h')

    with open(filename, 'rb') as f:
        dbx.files_upload(f.read(), path=f"/test.csv")
    
    return print('File uploaded !')



def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      # MainMenu {visibility: hidden;}
      footer {visibility: hidden;background - color: white}
     .stApp { bottom: 80px; }
    </style>
    """
    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1,

    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)






        


    #st.session_state.bet1, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=tirage(st.session_state.bet1,opts)



####################################################################################################################################################################
####################################################################################################################################################################    
####################################################################################################################################################################
####################################################################################################################################################################
####################################################################################################################################################################
def front_bias():
    blue=st.session_state.save_bet[1]
    red=st.session_state.save_bet[0]
    grey=100-blue-red
    values_recup=st.session_state.slider_value
    col1,col3, col2 = st.columns([2,1,2])
    with col1:
        
        col1a,col1b=st.columns([2.3,3])#COL1A;COL1B
        with col1a:
            st.subheader("  ")
            st.subheader("  ")
            st.subheader("  ")
            fig3 = plt.figure(
                FigureClass=Wf,
                rows=10,
                #columns=10,  # Either rows or columns could be omitted
                values=[int(Number_of_ball*Freq_green), Number_of_ball-int(Number_of_ball*Freq_green)],
                colors=[color_Green,color_Yellow],
                characters='⬤',
                font_size=20)
            st.pyplot(fig3)
        with col1b:
            st.subheader("  ")
            st.subheader("Option A")
            fig1, ax1=plt.subplots()#figsize=(4,4))
            x1,y1 = ([0,-0.1,0], [-0.1,0,0.1])
            line1 = mpl.lines.Line2D(x1,y1, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(0.1, 0.1, "Green: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(0.1, -0.1, "Yellow: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax1.add_line(line1)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig1)
    with col3:
        st.subheader("  ")
        st.subheader("  ")
        st.subheader("  ")
        choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True)
        choice='A' if choice=='Option A' else 'B'
        st.write("     You choose option "+str(choice))
        if st.button(str(st.session_state.cmpt_page+1)):
            pass
        button_val=st.button('Validation')
        if button_val:
            button_val=False
            if st.session_state.cmpt_page<1:
                up_cmpt()
                st.session_state.histo_opts.append(choice)
                print(st.session_state.histo_opts)
            else:
                print(values_recup[0],red,values_recup[1],blue)
                if values_recup[0]<=red and values_recup[1]<=blue:
                    up_cmpt()
                    st.session_state.save_bet=values_recup
                    st.session_state.histo_opts.append(choice)
                    print(st.session_state.histo_opts)
                    print(st.session_state.save_bet)
                    if st.session_state.cmpt_page%2==0:
                        opts=st.session_state.histo_opts[-2:]
                        print(opts)
                        print(st.session_state.histo_opts)
                        bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=validation(values_recup,opts)
                        print('fini')
                        print(finished)
                        #st.session_state.save_bet=bet
                        if finished:
                            st.session_state.cmpt_page=-5
                            st.write("It's finished, we will send the results")
                    st.experimental_rerun()
                else:
                    st.write("you can't validate. The left handles is inferior than red or the right value is inferior than blue")
    with col2:
        
        col2a,col2b=st.columns([3,2.3])
        with col2b:
            st.subheader("  ")
            st.subheader("Option B")
            blue=st.session_state.save_bet[1]
            red=st.session_state.save_bet[0]
            value=[red,blue]
            grey=100-blue-red
            fig4 = plt.figure(
                FigureClass=Wf,
                rows=10,
                columns=10,  # Either rows or columns could be omitted
                values=[red,grey,blue],
                colors=[color_Red,color_Grey,color_Blue],
                characters='⬤',
                font_size=20,
                )
            st.pyplot(fig4)
        with col2a:
            st.subheader("  ")
            st.subheader("  ")
            st.subheader("  ")
            fig3, ax3=plt.subplots()#figsize=(4,4))
            x3,y3 = ([0,0.1,0], [-0.1,0,0.1])
            line3 = mpl.lines.Line2D(x3,y3, lw=10., alpha=0.9)
            value_money=st.session_state.cmpt_page%2*Winning_amount
            plt.text(-0.1, 0.1, "Red: "+str(value_money)+"€", ha="center", family='sans-serif', size=30)
            plt.text(-0.1, -0.1, "Blue: "+str(20-value_money)+"€", ha="center", family='sans-serif', size=30)
            ax3.add_line(line3)
            plt.axis('equal')
            plt.axis('off')
            plt.tight_layout()
            st.pyplot(fig3)


######################################################################################################
    if st.session_state.cmpt_page>=2:

        fig4b = plt.figure(figsize=(10,1))
        ax4b = fig4b.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap([color_White,color_Blue])
        bounds = [0,red+grey,100]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb4b = mpl.colorbar.ColorbarBase(ax4b, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        ax4b.axis('off')
        st.pyplot(fig4b)
        fig4a = plt.figure(figsize=(10,1))
        ax4a = fig4a.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap([color_Red,color_White])
        bounds = [0,red,100]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb4a = mpl.colorbar.ColorbarBase(ax4a, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        ax4a.axis('off')
        st.pyplot(fig4a)
                
        options=list(range(101))
        st.write('Option A')
        values_recup = st.select_slider(' ',options, value = (red,100-blue),format_func=lambda x:'')#on_change=_update_slider
        values_recup=list(values_recup)
        values_recup[1]=100-values_recup[1]
        st.session_state.slider_value=values_recup
        colR,colW, colB = st.columns([1.6,2,1])
        with colR:
            st.write('The Red value is equal to '+str(values_recup[0]))
        with colW:
            st.write("The Red value can't superior than "+str(red)+". The Blue value can't superior than "+str(blue))
        with colB:
            st.write('The Blue value is equal to '+str(values_recup[1]))
        ColorMinMax = st.markdown(''' <style> div.stSlider > div[data-baseweb = "slider"] > div[data-testid="stTickBar"] > div {
        background: rgb(1 1 1 / 0%); } </style>''', unsafe_allow_html = True)
        Slider_Cursor = st.markdown(''' <style> div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
        background-color: rgb(14, 38, 74); box-shadow: rgb(14 38 74 / 20%) 0px 0px 0px 0.2rem;} </style>''', unsafe_allow_html = True)
        #background: linear-gradient(to right, rgba(151, 166, 195, 0.25) 0%, rgba(151, 166, 195, 0.25) 20%, rgb(255, 75, 75) 20%, rgb(255, 75, 75) 70%, rgba(151, 166, 195, 0.25) 70%, rgba(151, 166, 195, 0.25) 100%);
        #st.write(values_recup[0],values_recup[1],t)
        r,g,b = int(values_recup[0]),100-int(values_recup[0])-int(values_recup[1]),int(values_recup[1])
        #red_rgb=str(hex_to_rgb(color_Red))
        #blue_rgb=str(hex_to_rgb(color_Blue))
        col1 = f''' <style> div.stSlider > div[data-baseweb = "slider"] > div > div{{
        background: linear-gradient(90deg, red 0% {r}%, 
                                grey {r}% {100-b}%, 
                                blue {100-b}% 100%); }} </style>'''#rgb'''+red_rgb+''' 
        ColorSlider = st.markdown(col1, unsafe_allow_html = True)
        st.write('Option B')
        fig2a = plt.figure(figsize=(10,1))
        ax2a = fig2a.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap([color_Blue,color_White])
        bounds = [0,red+grey,100]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb4a = mpl.colorbar.ColorbarBase(ax4a, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        ax2a.axis('off')
        st.pyplot(fig4a)
        fig2b = plt.figure(figsize=(10, 1))
        ax2b = fig2b.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap([color_White,color_Red])
        bounds = 100-np.array([0,red,100])
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb2b = mpl.colorbar.ColorbarBase(ax2b, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        ax2b.axis('off')
        st.pyplot(fig2b)
        if st.button('to_result'):
            st.session_state.cmpt_page=-5
            st.experimental_rerun()
    else:
        pass
######################################################################################################


    
    return 0











    
