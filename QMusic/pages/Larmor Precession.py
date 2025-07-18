import streamlit as st
import numpy as np
import qutip
import io
import os
import soundfile as sf
from scipy import signal
from scipy.interpolate import interp1d

st.set_page_config(page_title="Larmor Precession")
st.sidebar.header("Larmor Precession")

st.title("Larmor Precession")

with st.expander("How It Works?"):
    st.write(''' **For non-physicists**: In classical computing, information is encoded in binary numbers. Each binary digit is a **bit**.
             In quantum computing, the basic unit is a **qubit**. Unlike a bit, a qubit can exist as a combination of $0$ and $1$, with certain probabilities.
             A qubit can be realized by using a two-level quantum mechanical system. When a magnetic field is applied, the qubit state starts to precess.
             We simulate this quantum precession, or the so-called **Larmor precession**, and map the precession to sound.
             By adjusting the parameters of the magnetic field, we get different musical tones. :musical_note:
             We could also increase the number of qubits and see how they interact with each other (Physicists call it **coupling**)
    ''')


'''
QMusic 2.0 Update: In version 1.0, we considered a single qubit. That was way too boring.
We extended our idea to multi-qubit systems. The user gets to pick the dimension. For now the maximum dimension is 2, but we can probably make this number larger in the future?
We assume the Heisenberg Nearest Neighbor model for the sake of simplicity. 
Just for fun, we use the idea of magnetic field gradient (which is common in MRI) here, so that the magnetic field is not uniform in space. Let's see what we can get out of this simulation!
'''

#For now the maximum number of qubits is 4
#Default is 1

st.header("Basic Setup", divider=True)
dim = st.radio(
    "Dimension of the spin system",
    ["***1D Chain***", "***2D Square Lattice***"],
    captions=[
        "You are free to choose the number of spins from 1 to 4. The model is assumed to be periodic.",
        "For now the 2D lattice is assumed to have 4 spins."
    ],
)
image_path1 = os.path.join(script_dir, "spinChain.jpg")
image_path2 = os.path.join(script_dir, "spinLattice.jpg")

if dim == "***1D Chain***":
    st.image(image_path1, caption="1D Spin Chain Diagram")
    num_qubit = st.select_slider(
        "Number of qubits",
        options = [1, 2, 3, 4]
    )
else:
    num_qubit = 4
    st.image(image_path2, caption="2D Spin Lattice Diagram")

factor_default = 1/np.sqrt(2**num_qubit)
initstate_default = np.ones(2**num_qubit)*factor_default
initstate = initstate_default

st.header("Initial State", divider=True)
st.markdown(r"The default initial state is $a_i = \frac{1}{\sqrt{2^N}}\forall i$, where $N$ is the number of qubits.")

initstate_mode = st.radio(
    "Select the initial state",
    ["***Use default initial state***", "***Customize initial state***", "***Randomize initial state***"],
)
if initstate_mode == "***Customize initial state***":
    st.markdown(r"The initial state of the system is $a_{0...0}|0...0\rangle+a_{0...1}|0...1\rangle+...+a_{1...1}|1...1\rangle$. Please enter the coeffcients a_i below, we'll do the normalization for you. Use $j$ for complex numbers (For example, $2+3j$)")
    col1, col2 = st.columns(2)
    tempinit = np.array([None]*(2**num_qubit))

    count1 = 0
    with col1:
        while count1 <= 2**num_qubit-1:
            temp = st.text_input(rf"$a_{{{bin(count1)[2:].zfill(num_qubit)}}}$")
            if temp != '':
                try:
                    tempinit[count1] = complex(temp)
                except ValueError:
                    st.error("Invalid Input!!!")
            count1 = count1 + 2

    count2 = 1
    with col2:
        while count2 <= 2**num_qubit-1:
            temp = st.text_input(rf"$a_{{{bin(count2)[2:].zfill(num_qubit)}}}$")
            if temp != '':
                try:
                    tempinit[count2] = complex(temp)
                except ValueError:
                    st.error("Invalid Input!!!")
            count2 = count2 + 2

    Done = st.button("Done")

    if Done == True and (tempinit == None).any():
        st.error("Did you forget to enter some of the coefficients/enter any invalid coefficients?")
    elif Done == True and (tempinit == None).any() == False:
        norm = np.linalg.norm(abs(tempinit))
        initstate = tempinit/norm

if initstate_mode == "***Randomize initial state***":
    Random = st.button ("Randomize")
    if Random == True:
        initstate = np.random.uniform(-1, 1, 2**num_qubit) + 1.j* np.random.uniform(-1, 1, 2**num_qubit)
        norm = np.linalg.norm(abs(initstate))
        initstate = initstate/norm

initstate_string=f"{initstate[0]}|"+"0"*num_qubit+r"\rangle"
for i in range(1, 2**num_qubit):
    initstate_string = initstate_string + rf"+{initstate[i]}|{bin(i)[2:].zfill(num_qubit)}\rangle"

st.markdown(rf"The initial state is: ${initstate_string}$")

st.header("Simulation Time", divider = True)
T = st.select_slider(
    "Time",
    options=[
        1,
        2,
        3,
        4,
        5
    ],)
times = np.linspace(0, T, 44100*T)

st.header("Hamiltonian", divider=True)
st.markdown(r"We apply an external magnetic field $\vec{B} (\vec{r},t)$ to the quantum spin system, which determines the Hamiltonian (a function that describes the energy of the system) that governs the system. The spins interact with each other through the Heisenberg nearest neighbor model. The strength of interaction is determined by the constant $J$. If $J>0$, then the system is called ferromagnetic; if $J<0$, then the system is anti-ferromagnetic. You are welcomed to change the magnetic field parameters and $J$!")
st.markdown(r"The Hamiltonian is $H=\sum_{i}^N\vec{B}(\vec{r},t)\cdot\vec{\sigma_i}+J\sum_{\langle i,j\rangle}\vec{\sigma_i}\cdot \vec{\sigma_j}$. Here $\vec{B} (\vec{r},t)$ takes the form of $B_0+\nabla B\cdot\vec{r}+F(t)$, pointing in the $z$-direction, where $F(t)$ is some periodic function. The gradient is assumed to be constant.")

st.markdown(r"**Magnetic field $\vec{B}$**")
tab_const, tab_space, tab_time = st.tabs(["Constant Term", "Space-dependent Term", "Time-dependent Term"])
with tab_const:
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

with tab_space:
    if dim == "***1D Chain***":
        st.markdown(r"Select a value for $\frac{\partial B}{\partial x}$.")
        grad = st.select_slider(
            r"$\frac{\partial B}{\partial x}$",
            options=[
                100,
                0,
                150,
                200,
                250,
                300
            ]
        )
    else:
        st.markdown(r"Select a value for $\frac{\partial B}{\partial x}$ and $\frac{\partial B}{\partial y}$.")
        gradx = st.select_slider(
            r"$\frac{\partial B}{\partial x}$",
            options=[
                0,
                100,
                150,
                200,
                250,
                300
            ]
        )
        grady = st.select_slider(
            r"$\frac{\partial B}{\partial y}$",
            options=[
                0,
                100,
                150,
                200,
                250,
                300
            ]
        )

with tab_time:
    amp = st.select_slider(
        "Amplitude of $F(t)$",
        options=[
                0,
                100,
                200,
                300,
                400,
                500,
                600
        ],)
    option = st.selectbox(
    "Waveform of f(t)",
    ("Sine Wave", "Square Wave", "Sawtooth Wave"),)
    if option == "Square Wave":
        duty = st.select_slider(
            "Duty Cycle",
            options=[
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9

            ]
        )
    if option == "Sawtooth Wave":
        w = st.select_slider(
            "Ratio of the Rising Ramp Width to Period",
            options=[
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.6,
                0.7,
                0.8,
                0.9,
                1.0

            ]
        )
    f = st.select_slider(
        "Frequency",
        options=[
                5,
                10,
                15,
                20,
                25,
                30
        ])

J = st.select_slider("J", options = [
    -20,
    -10,
    0,
    10,
    20
])

noise = st.checkbox("Add Noise to B-field")
if noise==True:
    std = st.select_slider(
    "Standard Deviation of Gaussian Noise",
    options=[
            50,
            100,
            150,
            200
    ],)
    noise_sig = noise*np.random.normal(0,std, len(times))
    noise_interp = interp1d(
    times,
    noise_sig,
    bounds_error=False,
    fill_value=(noise_sig[0], noise_sig[-1])
    )

if dim == "***1D Chain***":
    space_dependentH = 0*qutip.tensor([qutip.qeye(2) for _ in range(num_qubit)])
    obs_sum = space_dependentH
    for i in range(1, num_qubit):
        sx_i=qutip.tensor([qutip.sigmax() if j==i else qutip.qeye(2) for j in range(num_qubit)])
        sy_i=qutip.tensor([qutip.sigmay() if j==i else qutip.qeye(2) for j in range(num_qubit)])
        sz_i=qutip.tensor([qutip.sigmaz() if j==i else qutip.qeye(2) for j in range(num_qubit)])
        j=(i+1)%num_qubit
        sx_j=qutip.tensor([qutip.sigmax() if j==k else qutip.qeye(2) for k in range(num_qubit)])
        sy_j=qutip.tensor([qutip.sigmay() if j==k else qutip.qeye(2) for k in range(num_qubit)])
        sz_j=qutip.tensor([qutip.sigmaz() if j==k else qutip.qeye(2) for k in range(num_qubit)])
        obs_sum = obs_sum + sy_i
        space_dependentH = space_dependentH + grad*i*sz_i + sx_i * sx_j + sy_i * sy_j + sz_i * sz_j * J
else:
    space_dependentH = 0*qutip.tensor([qutip.qeye(2) for _ in range(num_qubit)])
    obs_sum = space_dependentH
    len = int(np.sqrt(num_qubit))
    for i in range(num_qubit):
        sx_i=qutip.tensor([qutip.sigmax() if j==i else qutip.qeye(2) for j in range(num_qubit)])
        sy_i=qutip.tensor([qutip.sigmay() if j==i else qutip.qeye(2) for j in range(num_qubit)])
        sz_i=qutip.tensor([qutip.sigmaz() if j==i else qutip.qeye(2) for j in range(num_qubit)])
        for j in range(i+1,num_qubit):
            if i+len==j or i+1==j:
                sx_j=qutip.tensor([qutip.sigmax() if j==k else qutip.qeye(2) for k in range(num_qubit)])
                sy_j=qutip.tensor([qutip.sigmay() if j==k else qutip.qeye(2) for k in range(num_qubit)])
                sz_j=qutip.tensor([qutip.sigmaz() if j==k else qutip.qeye(2) for k in range(num_qubit)])
                space_dependentH = space_dependentH + sx_i * sx_j + sy_i * sy_j + sz_i * sz_j * J
        x = i%len
        y = i//len
        obs_sum = obs_sum + sy_i
        space_dependentH = space_dependentH + (gradx*x +grady*y)*sz_i

if option=="Sine Wave":
    def periodic (t, args):
        H = B0+amp*np.sin(2*np.pi*f*t)
        if noise==True:
            H = H+noise_interp(t)
        return H
if option=="Square Wave":
    def periodic (t, args):
        H = B0+amp*signal.square(2*np.pi*f*t, duty)
        if noise==True:
            H = H+noise_interp(t)
        return H
if option=="Sawtooth Wave":
    def periodic (t, args):
        H = B0+amp*signal.sawtooth(2*np.pi*f*(t+1/f), w)
        if noise==True:
            H = H+noise_interp(t)
        return H

open = st.checkbox("Open Quantum System")

if open == True:
    gamma = st.select_slider(
    "Decay rate",
    options=[
        1.0,
        1.5,
        2.0,
        2.5,
        3.0,
        3.5,
        4.0

    ],)

    c_ops = [np.sqrt(gamma)*qutip.tensor([qutip.operators.destroy(2)]*num_qubit)]  
    #c_ops = [np.sqrt(gamma) * qutip.sigmaz()]
else:
    c_ops=[]

observable = st.radio("Choose an observable to measure",
        [r"$\bigotimes_{i=1}^N\sigma_y^{(i)}$", r"$\sum_{i=1}^N\sigma_y^{(i)}$"]
                      )
if observable == r"$\bigotimes_{i=1}^N\sigma_y^{(i)}$":
    obs=[qutip.tensor([qutip.sigmay()]*num_qubit)]
else:
    obs = obs_sum



Produce = st.button("Produce Sound")
if Produce == True:
    with st.status("Producing...", expanded=False) as status:
        psi = qutip.Qobj(initstate, dims=[[2]*num_qubit, [1]*num_qubit])
        H = qutip.QobjEvo([[qutip.tensor([qutip.sigmaz()]*num_qubit), periodic],space_dependentH], tlist=times)
        result = qutip.mesolve(H, psi, times, c_ops, obs)
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
            


        
            




