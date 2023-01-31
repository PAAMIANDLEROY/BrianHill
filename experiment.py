import streamlit as st
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

value_grey=0.7
color_bar_init=[[1.,0.,0.],3*value_grey,[0.,0.,1.]]
def up_cmpt():
    st.session_state.cmpt_page+=1


def label(xy, text):
    y = xy[1] - 0.15  # shift y-value for label so that it's below the artist
    plt.text(xy[0], y, text, ha="center", family='sans-serif', size=14)


def experiment_front(bet):
    a=0.7
    col1,col3, col2 = st.columns([2,0.7,2])
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
        label(grid_txt1[0],"plus")
        label(grid_txt1[1],"moins")
        label(grid_txt_dollar1[0],"0 €")
        label(grid_txt_dollar1[1],"20 €")
        ax1.add_line(line1)
        ax1.set_title("plus ou moins que "+str(5)+"/20")
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        st.pyplot(fig1)
    with col3:
        choice=st.radio("Which option do you choose ?",('Option A', 'Option B'),horizontal=True)
        st.write("You choose option "+str(choice))
    with col2:
        st.subheader("Option B")
    ##    st.markdown(
    ##        """
    ##        [<img src='data:image/png;base64,{}' class='img-fluid' width=25 height=25>](https://github.com/hi-paris/agent-theory) <small> agent-theory 0.0.1 | September 2022</small>""".format(
    ##            img_to_bytes("./images/github.png")
    ##        ),
    ##        unsafe_allow_html=True,
    ##    )




        blue=bet[1]
        red=bet[0]
        grey=100-blue-red
        print("blue"+str(blue))
        print("red"+str(red))
        print("grey"+str(grey))
        fig4 = plt.figure(figsize=(8, 3))
        ax4 = fig4.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap([[1.,0.,0.],[a,a,a],[0.,0.,1.]])
        bounds = [0,red,red+grey,100]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb4 = mpl.colorbar.ColorbarBase(ax4, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        st.pyplot(fig4)
        values = st.slider('Select a range of values', 0, 100, (red,red+grey)) #int input => int output
        #TODO, choose an event ton change the freq of update
        red=int(values[0])
        grey=int(values[1])-red
        blue=100-grey-red
        print("values"+str(values))
        print("blue"+str(blue))
        print("red"+str(red))
        print("grey"+str(grey))
        

        fig2 = plt.figure(figsize=(8, 3))
        ax2 = fig2.add_axes([0.05, 0.475, 0.9, 0.15])
        cmap = mpl.colors.ListedColormap([[1.,0.,0.],[a,a,a],[0.,0.,1.]])
        bounds = [0,red,red+grey,100]
        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
        cb2 = mpl.colorbar.ColorbarBase(ax2, cmap=cmap,
                                        norm=norm,
                                        ticks=bounds,  # optional
                                        spacing='proportional',
                                        orientation='horizontal')
        st.pyplot(fig2)



        
        st.subheader("                  Option B")
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

    if st.button(str(st.session_state.cmpt_page)):
        pass
    if st.button('Validation'):
        up_cmpt()
        #st.experimental_rerun()
        if choice=='Option A':output_bet='A'
        else : output_bet='B'
    output_bet=[red,blue]
    return output_bet



