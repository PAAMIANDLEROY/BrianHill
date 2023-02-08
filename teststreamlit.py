#Import group 1 (Useful pckg)

import matplotlib.pyplot as plt
import matplotlib as mpl
import base64
import numpy as np

#Import group 2 (Streamlit)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
import streamlit as st

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



if 'cmpt_page' not in st.session_state:
    st.session_state.cmpt_page=0
if 'save_bet' not in st.session_state:
    st.session_state.save_bet=[30,30]
if 'print_bet' not in st.session_state:
    st.session_state.print_bet=st.session_state.save_bet
if 'histo' not in st.session_state:
    st.session_state.histo=[]
if 'Marks' not in st.session_state:
    st.session_state.Marks=[4,6,8,10,12,14,16,18]
value_grey=[0.7]
color_bar_init=[[1.,0.,0.],3*value_grey,[0.,0.,1.]]
def up_cmpt():
    st.session_state.cmpt_page+=1


def label(xy, text):
    y = xy[1] - 0.15  # shift y-value for label so that it's below the artist
    plt.text(xy[0], y, text, ha="center", family='sans-serif', size=14)
def validation(values,opts):
    st.session_state.histo.append(values)
    bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=algo.main(values,opts)
    if len(st.session_state.Marks)>1:del st.session_state.Marks[0]
    bet=[int(bet[0]),int(bet[1])]
    
    return bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile

def experiment_front():
    col1,col3, col2 = st.columns([2,1,2])
    with col1: #parameter : Value_to_win, Win_with_more_or_less, Mark, 
        st.subheader("                  Option A")
        #st.write(" Have more than 5/20 ?")

        fig1, ax1=plt.subplots()
        grid1=np.array([0.5,0.8])
        grid_txt1=np.array([[0.3,0.8],[0.7,0.8]])
        grid_txt_dollar1=np.array([[0.3,0.75],[0.7,0.75]])
        x1, y1 = ([-0.2, 0, 0.2], [-0.1,0,-0.1])
        line1 = mpl.lines.Line2D(x1 + grid1[0], y1 + grid1[1], lw=5., alpha=0.3)
        label(grid1, "Line2D")
        label(grid_txt1[0],"More")
        label(grid_txt1[1],"Less")
        label(grid_txt_dollar1[0],"0 €")
        label(grid_txt_dollar1[1],"20 €")
        ax1.add_line(line1)
        ax1.set_title("More or less than "+str(st.session_state.Marks[0])+"/20")
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        st.pyplot(fig1)
    with col3:
        choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True)
        st.write("You choose option "+str(choice))
    with col2:
        st.subheader("Option B")
        blue=st.session_state.save_bet[1]
        red=st.session_state.save_bet[0]
        grey=100-blue-red
        fig4 = plt.figure(figsize=(8, 3))
        ax4 = fig4.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap(color_bar_init)
        bounds = [0,red,red+grey,100]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb4 = mpl.colorbar.ColorbarBase(ax4, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        st.pyplot(fig4)
        
        st.write(" Red or Blue ?")

        fig3, ax3=plt.subplots()
        grid3=np.array([0.5,0.8])
        grid_txt3=np.array([[0.3,0.8],[0.7,0.8]])
        grid_txt_dollar3=np.array([[0.3,0.75],[0.7,0.75]])
        x3, y3 = ([-0.2, 0, 0.2], [-0.1,0,-0.1])
        line3 = mpl.lines.Line2D(x3 + grid3[0], y3 + grid3[1], lw=5., alpha=0.3)
        label(grid3, "Line2D")
        label(grid_txt3[0],"Blue")
        label(grid_txt3[1],"Red")
        label(grid_txt_dollar3[0],"0 €")
        label(grid_txt_dollar3[1],"20 €")
        ax3.add_line(line3)
        #ax.set_title("plus ou moins que "+str(5)+"/20")
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        st.pyplot(fig3)


    fig4 = plt.figure(figsize=(10,1))
    ax4 = fig4.add_axes([0.05, 0.475, 0.9, 0.15])
    cmap = mpl.colors.ListedColormap(color_bar_init)
    bounds = [0,red,red+grey,100]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb4 = mpl.colorbar.ColorbarBase(ax4, cmap=cmap,
                                    norm=norm,
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='horizontal')
    st.pyplot(fig4)
    values = st.slider('Select a range of values', 0, 100, (red,red+grey)) #int input => int output
    values=[values[0],100-values[1]]
    def change_display(x):
        return x*100
    #values = st.select_slider('Select a range of values', options=list(range(100)),value=[10,20],format_func=change_display)

    fig2 = plt.figure(figsize=(10, 1))
    ax2 = fig2.add_axes([0.05, 0.475, 0.9, 0.15])
    cmap = mpl.colors.ListedColormap(color_bar_init)
    bounds = 100-np.array([0,red,red+grey,100])
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
                                    norm=norm,
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='horizontal')
    st.pyplot(fig2)





    if st.button(str(st.session_state.cmpt_page)):
        pass
    opts=["A","A"]
    if st.button('Validation'):
        up_cmpt()
        st.session_state.save_bet=[values[0],100-values[1]]
        bet, finished, sumlen, nzdict, ccomments, finishedBefMaxIter, finishedApartAlgo, useReturn, useWhile=validation(values,opts)
        st.session_state.save_bet=bet
        st.experimental_rerun()
    return 0

        
        









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
    
    values=experiment_front()


    


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



    


