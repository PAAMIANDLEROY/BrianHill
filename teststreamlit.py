#Import group 1 (Useful pckg)

import matplotlib.pyplot as plt
import matplotlib as mpl
import base64
import numpy as np
from pywaffle import Waffle as Wf
import class_range_slider as crs
#Import group 2 (Streamlit)
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
#config
st.set_page_config(
    page_title="Brian Hill", layout="wide", page_icon="images/flask.png"
)
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
    plt.show()



if 'cmpt_page' not in st.session_state:
    st.session_state.cmpt_page=-2
if 'save_bet' not in st.session_state:
    st.session_state.save_bet=[30,30]
if 'print_bet' not in st.session_state:
    st.session_state.print_bet=st.session_state.save_bet
if 'histo' not in st.session_state:
    st.session_state.histo=[]
if 'histo_opts' not in st.session_state:
    st.session_state.histo_opts=[]
value_grey=[0.7]
color_Green='#54cc33'
color_Yellow='#e4e805'
color_Red='#ff0000'
color_Blue='#0000ff'
color_Grey='#b3b3b3'
color_White='#ffffff'
Winning_amount=20
#color_bar_init=[[1.,0.,0.],3*value_grey,[0.,0.,1.]]

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

def experiment_front():
    col1,col3, col2 = st.columns([2,1,2])
    with col1: #parameter : Value_to_win, Win_with_more_or_less, Mark, 
        st.subheader("                  Option A")
        #st.write(" Have more than 5/20 ?")
        fig3 = plt.figure(
            FigureClass=Wf,
            rows=10,
            columns=10,  # Either rows or columns could be omitted
            values=[87, 13],
            colors=[color_Green,color_Yellow],
            characters='⬤',
            font_size=12)
        st.pyplot(fig3)
        fig1, ax1=plt.subplots()
        grid1=np.array([0.5,0.8])
        grid_txt1=np.array([[0.3,0.8],[0.7,0.8]])
        grid_txt_dollar1=np.array([[0.3,0.75],[0.7,0.75]])
        x1, y1 = ([-0.2, 0, 0.2], [-0.1,0,-0.1])
        line1 = mpl.lines.Line2D(x1 + grid1[0], y1 + grid1[1], lw=5., alpha=0.3)
        label(grid1, " ")
        label(grid_txt1[0],"Green")
        label(grid_txt1[1],"Yellow")
        value_money=st.session_state.cmpt_page%2*Winning_amount
        label(grid_txt_dollar1[0],str(value_money)+"€")
        label(grid_txt_dollar1[1],str(20-value_money)+"€")
        ax1.add_line(line1)
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        st.pyplot(fig1)
    with col3:
        choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True)
        choice='A' if choice=='Option A' else 'B'
        st.write("You choose option "+str(choice))
    with col2:
        st.subheader("Option B")
        blue=st.session_state.save_bet[1]
        red=st.session_state.save_bet[0]
        value=[red,blue]
        grey=100-blue-red
        
##      fig4 = plt.figure(figsize=(8, 3))
        fig4 = plt.figure(
            FigureClass=Wf,
            rows=10,
            columns=10,  # Either rows or columns could be omitted
            values=[red,grey,blue],
            colors=[color_Red,color_Grey,color_Blue],
            characters='⬤',
            font_size=12)
##        ax4 = fig4.add_axes([0.05, 0.475, 0.9, 0.15])
##        cmap = mpl.colors.ListedColormap(color_bar_init)
##        bounds = [0,red,red+grey,100]
##        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
##        cb4 = mpl.colorbar.ColorbarBase(ax4, cmap=cmap,
##                                        norm=norm,
##                                        ticks=bounds,  # optional
##                                        spacing='proportional',
##                                        orientation='horizontal')
        st.pyplot(fig4)
        
        #st.write(" Red or Blue ?")

        fig3, ax3=plt.subplots()
        grid3=np.array([0.5,0.8])
        grid_txt3=np.array([[0.3,0.8],[0.7,0.8]])
        grid_txt_dollar3=np.array([[0.3,0.75],[0.7,0.75]])
        x3, y3 = ([-0.2, 0, 0.2], [-0.1,0,-0.1])
        line3 = mpl.lines.Line2D(x3 + grid3[0], y3 + grid3[1], lw=5., alpha=0.3)
        label(grid3, " ")
        label(grid_txt3[0],"Red")
        label(grid_txt3[1],"Blue")
        value_money=st.session_state.cmpt_page%2*Winning_amount
        label(grid_txt_dollar3[0],str(value_money)+"€")
        label(grid_txt_dollar3[1],str(20-value_money)+"€")
        ax3.add_line(line3)
        #ax.set_title("plus ou moins que "+str(5)+"/20")
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        st.pyplot(fig3)

    if st.session_state.cmpt_page>=2:
        
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
        #a=0.7
        #color_left='green'
        #color_middle='red'
        #color_right='blue'
       # fig_slider = plt.figure(figsize=(10,1))
        #ax_slider=fig_slider.add_axes([0.1,0.5,0.75,0.3])#, facecolor=axcolor)
        #defaults={'facecolor': 'blue', 'edgecolor': 'red', 'size': 30}
        #valinit=[30,75]
        #sfreq = crs.RangeSlider(ax_slider, 'DoubleSlider', 1, 100,valstep=1,valinit=valinit,handle_style=defaults,color_left=color_left,color_middle=color_middle,color_right=color_right)#([a,a,a],[0.,0.,1.]))
        #fig_html = mpld3.fig_to_html(fig_slider)
        #components.html(fig_html, height=600)
        #st.pyplot(fig_slider,clear_figure=True)
        values_recup = st.slider('Select a range of values', 0, 100, (red,red+grey)) #int input => int output
        values=[values_recup[0],100-values_recup[1]]
        st.write(' ')
        #def change_display(x):
        #    return x*100
        #values = st.select_slider('Select a range of values', options=list(range(100)),value=[10,20],format_func=change_display)
        fig2a = plt.figure(figsize=(10,1))
        ax2a = fig2a.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap([color_Red,color_White])
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
        cmap = mpl.colors.ListedColormap([color_White,color_Blue])
        bounds = 100-np.array([0,red,100])
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb2b = mpl.colorbar.ColorbarBase(ax2b, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        ax2b.axis('off')
        st.pyplot(fig2b)
    else:
        pass
    





    
    col1,col3, col2 = st.columns([2.8,1,2])
    with col1:
        pass
    with col3:
        if st.button(str(st.session_state.cmpt_page)):
            pass
        opts=["A","A"]
        button_val=st.button('Validation')
        if button_val:
            up_cmpt()
            if st.session_state.cmpt_page%2==0:
                if 'values' not in vars():
                    values=st.session_state.save_bet
                #print(values)
                button_val=False
                opts=[st.session_state.histo_opts[-1],choice]
                st.session_state.histo_opts.append(choice)
                print(st.session_state.histo_opts)
                print(choice)
                st.session_state.save_bet=[values[0],100-values[1]]
                bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=validation(values,opts)
                #print(finished)
                st.session_state.save_bet=bet
            else:
                st.session_state.histo_opts.append(choice)
            st.experimental_rerun()
    with col2:
        pass
    return 0

        
        
def welcome():
    if st.button('Validation '):
        up_cmpt()
        st.experimental_rerun()
    if st.session_state.cmpt_page==-2:
        id_number=st.text_input('Quel est votre identifiant?')
        name=st.text_input('Quel est votre prénom et votre nom?')
        subject=st.text_input('Subject')
        age=st.slider('Quel est votre age?',18,125)
        gender=st.radio(" Quel est votre genre ?",('Homme','Femme','Autre','Préfère ne pas dire'))
    if st.session_state.cmpt_page==-1:
        st.write(str(st.session_state.cmpt_page))
        st.write('inserer une vidéo')   
    if st.button('Validation'):
        up_cmpt()
        st.experimental_rerun()




def main():
    def hide_header_footer():
        hide_streamlit_style = """
                    <style>
                    footer {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    hide_header_footer()
    st.markdown("# Brian Hill 🖥")
    st.subheader(
        """
        Decision  🧪
        """
    )
    if st.session_state.cmpt_page>=0:
        values_return=experiment_front()
    else:
        welcome()


    


    #st.session_state.bet1, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=tirage(st.session_state.bet1,opts)










if __name__=='__main__':
    main()

st.markdown(" ")
st.markdown("### HEC Researcher Brian Hill " )
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



st.markdown(f"#### Made by Hi!Paris,Link to Project Website [here]({'https://github.com/hi-paris/agent-theory'}) 🚀 ")



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

def footer2():
    myargs = [
        " Made by ",
        link("https://engineeringteam.hi-paris.fr/", "Hi! PARIS Engineering Team"),
        " 👩🏼‍💻 👨🏼‍💻"
    ]
    layout(*myargs)


if __name__ == "__main__":
    footer2()



    


