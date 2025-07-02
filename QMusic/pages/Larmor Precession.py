import streamlit as st
import numpy as np
import qutip
import io
import soundfile as sf

st.set_page_config(page_title="Larmor Precession")
st.sidebar.header("Larmor Precession")
#Default:
aDefault=1/np.sqrt(2)
bDefault=1/np.sqrt(2)

with st.expander("How It Works?"):
    st.write(''' **For non-physicists**: In classical computing, information is encoded in binary numbers. Each binary digit is a **bit**.
             In quantum computing, the basic unit is a **qubit**. Unlike a bit, a qubit can exist as a combination of $0$ and $1$, with certain probabilities.
             A qubit can be realized by using a two-level quantum mechanical system. When a magnetic field is applied, the qubit state starts to precess.
             We simulate this quantum precession, or the so-called **Larmor precession**, and map the precession to sound.
             By adjusting the parameters of the magnetic field, we get different musical tones. :musical_note:
    ''')

with st.popover("Change Initial State"):
    st.markdown(r"Note that if you start with $|0 \rangle$ or $|1 \rangle$, you are not going to hear anything :(")
    Random=st.checkbox("Randomize")
    Normalize=False
    Error=False
    if Random==False:
        placeholder=st.empty()
        with placeholder.container():
            st.markdown(r"Initial State: $a|0 \rangle + b|1 \rangle$")
            st.markdown("Use j for complex numbers (For example, 2+3j)")
            st.markdown("We will do the normalization for you :)")
            a = st.text_input("a=", key="aval")
            b = st.text_input("b=", key='bval')
            if b and a:
                try:
                    b=complex(b)
                    a=complex(a)
                except:
                    st.error("Invalid Input!!!")
                    a=aDefault
                    b=bDefault
                    Error=True
                norm = np.sqrt(abs(a)**2+abs(b)**2)
                a = a/norm
                b = b/norm
    else:
        Randomize=st.button("Randomize")
        if Randomize==True:
            a = np.random.uniform(-1, 1) + 1.j * np.random.uniform(-1, 1)
            b = np.random.uniform(-1, 1) + 1.j * np.random.uniform(-1, 1)
            norm=np.sqrt(abs(a)**2+abs(b)**2)
            a=a/norm
            b=b/norm
            st.markdown(fr"Initial State:${a}|0 \rangle+{b}|1 \rangle$")
try:
    a and b
except:
    a=aDefault
    b=bDefault
if a=="" or b=="":
    a=aDefault
    b=bDefault

st.markdown(rf"Initial State: ${a}|0 \rangle+{b}|1 \rangle$")

st.markdown(r"External B-field:$B_0+B_1\cos(\omega t)$")
B0 = st.select_slider(
    "$B_0$",
    options=[
        1000,
        1100,
        1200,
        1300,
        1400,
        1500,
        1600,
        1700,
        1800,
        1900,
        2000
    ],)

B1 = st.select_slider(
    "$B_1$",
    options=[
        0,
        500,
        600,
        700,
        800,
        900,
        1000,
    ],)

omega = st.select_slider(
    "$\omega$",
    options=[
        10,
        20,
        30,
        40,
        50,
        60,
        70,
        80,
        90,
        100
    ],)

T = st.select_slider(
    "Time",
    options=[
        5,
        10,
        15,
        20
    ],)

open = st.checkbox("Open Quantum System")
if open == True:
    gamma = st.select_slider(
    "Decay rate",
    options=[
        0.5,
        0.75,
        1.0,
        1.25,
        1.5,
        1.75,
        2.0

    ],)

    c_ops = [np.sqrt(gamma)*qutip.operators.destroy(2)]  
else:
    c_ops=[]

Produce = st.button("Produce Sound")
if Produce == True:
    with st.status("Producing...", expanded=False) as status:
        psi = (a* qutip.basis(2, 0) + b*qutip.basis(2, 1)).unit()
        def periodic (t, args):
            return B0+B1*np.cos(omega*t)
        times = np.linspace(0, T, 44100*T)
        H = qutip.QobjEvo([[qutip.sigmaz(), periodic]], tlist=times)
        result = qutip.mesolve(H, psi, times, c_ops, [qutip.sigmay()])
        expectation=result.expect[0]
        st.audio(expectation, sample_rate=44100)
        audio=np.int16(expectation/np.max(np.abs(expectation))*32767)
        buffer = io.BytesIO()
        sf.write(buffer, audio, samplerate=44100, format='WAV', subtype='PCM_16')
        buffer.seek(0)
        st.download_button(
        label="Download WAV file",
        data=buffer,
        file_name="Sound of Larmor Precession.WAV",
        mime="audio",
        icon=":material/download:",
        )
        status.update(
        label="Completed!", state="complete", expanded=True
    )
