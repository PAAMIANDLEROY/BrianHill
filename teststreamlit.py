#Import group 1 (Useful pckg)

import matplotlib.pyplot as plt
import matplotlib as mpl
import base64

#Import group 2 (Streamlit)
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb
import streamlit as st

#import fonction and Script
from experiment import *
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
if 'bet1' not in st.session_state:
    st.session_state.bet1=[30,30]

        
def main():
##    def max_width():
##        max_width_str = f"max-width: 1000px;"
##	st.markdown(f"""
##        <style>
##        .reportview-container .main .block-container{{
##            {max_width_str}
##        }}
##        </style>
##        """,
##            unsafe_allow_html=True,
##        )
    # Hide the Streamlit header and footer
    def hide_header_footer():
        hide_streamlit_style = """
                    <style>
                    footer {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    # increases the width of the text and tables/figures
##    _max_width_()
    # hide the footer
    hide_header_footer()
    st.markdown("# Brian Hill 🖥")
    st.subheader(
        """
        Decision  🧪
        """
    )
    st.session_state.bet1=experiment_front(st.session_state.bet1)
    opts=["A","B"]
    def tirage(bet,opts):
        tirage=np.random.randint(4,size=11)
        for opt in tirage:
            if opt==0:opts=["A","B"]
            elif opt==1:opts=["B","A"]
            elif opt==2:opts=["B","B"]
            else :opts=["A","A"]
        return algo.main(bet,opts)
        
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



    


