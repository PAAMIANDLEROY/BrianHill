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


#config
st.set_page_config(
    page_title="Agent Theory", layout="wide", page_icon="images/flask.png"
)
def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded




        
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
    st.markdown("     ")
##    st.markdown(
##        """
##        [<img src='data:image/png;base64,{}' class='img-fluid' width=25 height=25>](https://github.com/hi-paris/agent-theory) <small> agent-theory 0.0.1 | September 2022</small>""".format(
##            img_to_bytes("./images/github.png")
##        ),
##        unsafe_allow_html=True,
##    )




    blue=3
    red=40
    grey=100-red-blue

    a=0.7

    fig = plt.figure(figsize=(8, 3))
    ax2 = fig.add_axes([0.05, 0.475, 0.9, 0.15])
    # The second example illustrates the use of a ListedColormap, a
    # BoundaryNorm, and extended ends to show the "over" and "under"
    # value colors.
    cmap = mpl.colors.ListedColormap([[1.,0.,0.],[a,a,a],[0.,0.,1.]])

    # If a ListedColormap is used, the length of the bounds array must be
    # one greater than the length of the color list.  The bounds must be
    # monotonically increasing.
    bounds = [0,blue,grey+blue,100]
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
    cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
                                    norm=norm,
                                    ticks=bounds,  # optional
                                    spacing='proportional',
                                    orientation='horizontal')

    cb2.set_label('Option B, Urne contenant :')
    st.pyplot(fig)













if __name__=='__main__':
    main()

st.markdown(" ")
st.markdown("### ** 👨🏼‍💻 Télécom Paris Researcher: **")
#st.image(['images/1.png'], width=230,caption=["Vadim Malvone"])

st.markdown('### Made by Hi!Paris')
#images = Image.open('./images/hi-paris.png')
#st.image(images, width=250)
st.write('    ')
st.markdown('### Contributors:')
#PA=Image.open('./images/PA.jpg')
#Pierre=Image.open('./images/Pierre.jpg')
#GAE=Image.open('./images/gaetan.png')
#st.image([PA,GAE,Pierre],width=110)



st.markdown(f"####  Link to Project Website [here]({'https://github.com/hi-paris/agent-theory'}) 🚀 ")



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



    


