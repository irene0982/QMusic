import streamlit as st

st.set_page_config(page_title="Guidance")
st.sidebar.header("WTF is this?")

st.title("QMusic Tutorial")
st.markdown("""
    <p style='text-align: center; color: #8B0000; font-weight: bold; font-size: 20px; margin-top: 0;'>Quantum Mechanics 101</p>
""", unsafe_allow_html=True)

with st.expander("What is superposition?"):
    st.write(
    '''
    Imagine a cat and a radioactive atom placed in a sealed box. The atom may decay and release poison that kills the cat. We don't know whether the cat is alive or dead until we open the box.
    Before observation, quantum mechanics says that the cat exists in a combination of both outcomes. It's alive and dead at the same time (?!), in a certain proportion. Physicists say that the cat is in a **superposition** state.
    This thought experiment is known as Schrödinger's cat, which is used to illustrate how weird quantum theory is.
    ''')
    st.image("cat.jpg", caption = "My friend's cat trynna to stop me from working. Ofc I won't seal him in a box.")

with st.expander("What is spin?"):
    st.write(
        '''
    Each type of elementary particle possesses a unique property called **spin**. Just for clarification, nothing is spinning here. 
    Spin is just a property that determines how many possible states a particle can have.
    In our simulation, each particle has two spin states: spin-up and spin-down (Think of them like heads and tails on a coin). 
    According to quantum mechanics, a particle does not have to be just spin-up or spin-down but can exist in a combination of both states.
'''
    )

with st.expander("Visualization of superposition (Bloch sphere)"):
    st.write('''
    We can use a sphere in 3D (aka **Bloch sphere**) to visualize superposition. The north and south poles represent spin-up and spin-down respectively. Any other point on the sphere boundary is a superposition state.
''')
    st.image("0.jpg", caption = r'Spin-up and spin-down states are denoted by $|0\rangle$ and $|1\rangle$.')

with st.expander("What is Larmor precession?"):
    st.write('''
    What happens if we apply a magnetic field (pointing upward) to all particles? The particle's spin "feels" the magnetic field, causing the particle state to wobble around the vertical axis on the Bloch sphere. This wobbling motion is called Larmor precession.
''')
    st.image("Larmor.jpg",caption = "Motion of the particle state")
with st.expander("A realistic quantum system"):
    st.write('''In real life, a quantum system doesn't exist in vacuum. Air particles might bump into particles in the quantum system and change their quantum properties. 
            A system that interacts with the environment is called an open quantum system. The loss of quantum properties is called decoherence.''')

st.markdown("""
    <p style='text-align: center; color: #8B0000; font-weight: bold; font-size: 20px; margin-top: 0;'>About This Web App</p>
""", unsafe_allow_html=True)
st.markdown("This web app simulates Larmor precession and converts the quantum state's motion into sound. You are allowed to adjust several parameters in the quantum system we simulate.")

st.markdown("**Size and dimension**: You can change the number of particles and how they are arranged in space(1D chain or 2D lattice).")
st.markdown("**Initial state**: You can either specify or randomize the initial quantum state of the system.")
st.markdown("**Simulation time**: This parameter sets how long the quantum evolution lasts.")
st.markdown(r"**Magnetic field**: We apply an external magnetic field $\vec{B} (\vec{r},t)$ to observe Larmor precession. Here $\vec{B} (\vec{r},t)$ takes the form of $B_0+\nabla B\cdot\vec{r}+F(t)$, pointing in the $z$-direction. $B_0$ is a constant term, and the value is configurable. $F(t)$ is a periodic function that shows how the magnetic field changes with time. You can choose the waveform of $F(t)$. $\nabla B$ determines how the magnetic field changes in location")
st.markdown("**Interaction**: The particles interact with each other. The strength of interaction is determined by a configurable value $J$.")
st.markdown("**Noise**: To make the simulation more realistic, we also add noise to the magnetic field. You can change the strength of noise.")
st.markdown('''**Open quantum system**:  
            The user can choose to simulate an open quantum system or not. In addition, the user can decide the type of decoherence, as well as the decoherence constant (which describes how strong the system interacts with its environment).''')

st.markdown("""
    <p style='text-align: center; color: #8B0000; font-weight: bold; font-size: 20px; margin-top: 0;'>Motivation behind the Web App</p>
""", unsafe_allow_html=True)

st.markdown('''You've probably heard the buzzword *quantum computing*, which is an emerging field that applies quantum mechanics to computation.  In classical computing, we use bits to encode information. A bit is either 0 or 1. Wait, does that ring a bell? Classically, a cat is either alive or dead, but not both. In quantum mechanics, a cat can exist in a combination of both states. That's the idea of quantum computing: we use **qubits**, which are superpositions of 0 and 1, to encode information.
''')

st.markdown('''
        To be honest, I don't think practical quantum computers are achievable anytime soon because of the physical challenges. But the idea of *quantum music*, which is an area that explores the connection between quantum computing and sound, caught my attention instantly. I'm not insane. In 1956, Lejaren Hiller and Leonard Isaacson used the ILLIAC I (Illinois Automatic Computer) to compose the first algorithmic music. Today producers often use computers to write songs, but back then that idea sounded like science fictions. Some crazy ideas *do* eventually work out. Therefore, I spent a year working on quantum music. This web app is one small product.
''')

st.markdown('''
**Disclaimer:** some crazy ideas *don't* work out.  
I can't predict the future, and I don't want to make fake promises like some quantum computing business people. Quantum computers may or may not be realized. Quantum computers may or may not be used to make music. Still, I think the project is worthing doing. I learned to think creatively and to communicate across fields. Not every attempt needs to succeed, and that's the spirit of research.
(And yes, this app can totally be used for education, despite not being my original goal.)
''')
