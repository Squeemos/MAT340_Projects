'''
Written by Ben van Oostendorp

This is written for MAT 340
Spring 2021
DigiPen Insitute of Technology'''

import streamlit as st
import random
import pandas as pd
import numpy as np

page = st.sidebar.radio("Which project would you like to run",("Coupon Collector","Monty Hall","Monty Hall Simulation","Gambler's Ruin"))
code = st.sidebar.checkbox("Show the code")
st.sidebar.text("Shows the code below the project")

st.markdown(f"""<style>.reportview-container .main .block-container{{max-width:{1920}px;padding-right:{20}rem;padding-left:{20}rem;}}}}</style>""",unsafe_allow_html=True)

def trial(trials,num):
    '''trials is the number of trials to run
       num is the number of coupon types'''
    counts = []
    for _ in range(trials):
        coupons = []
        while len(set(coupons)) != num:
            coupons.append(random.randint(0,num))
        counts.append(len(coupons))

    return np.average(counts), counts

if page == "Coupon Collector":
    if code:
        with st.echo('below'):
            # Title and user input
            st.title("Coupon Collector")
            trials = int(st.number_input('How many trials would you like to run',min_value=1,value=100))
            coupons = int(st.number_input('How many coupon types are there',min_value=1,value=10))

            # Run when pressed
            if st.button("Run trials"):
                # Run the trial function (shown below as trial_dummy)
                avg, all_trials = trial(trials,coupons)
                st.text(f"The average number of coupons collected in {trials} trials with {coupons} coupon types is {avg}")

                # Create a dataframe to plot
                data = np.array(all_trials).T
                chart_data = pd.DataFrame(data,columns=['Trials'])
                chart_data['Average'] = avg
                st.line_chart(chart_data)

            # Renamed to preserve namespace
            def trial_dummy(trials,num):
                '''trials is the number of trials to run
                   num is the number of coupon types'''
                counts = []
                for _ in range(trials):
                    coupons = []
                    while len(set(coupons)) != num:
                        coupons.append(random.randint(0,num))
                    counts.append(len(coupons))

                return np.average(counts), counts
    else:
        st.title("Coupon Collector")
        trials = int(st.number_input('How many trials would you like to run',min_value=1,value=100))
        coupons = int(st.number_input('How many coupon types are there',min_value=1,value=10))
        if st.button("Run trials"):
            avg, all_trials = trial(trials,coupons)
            st.text(f"The average number of coupons collected in {trials} trials with {coupons} coupon types is {avg}")

            data = np.array(all_trials).T
            chart_data = pd.DataFrame(data,columns=['Trials'])
            chart_data['Average'] = avg
            st.line_chart(chart_data)

@st.cache(allow_output_mutation=True)
def door_mutable():
    return []

@st.cache(allow_output_mutation=True)
def chosen_mutable():
    return []

@st.cache(allow_output_mutation=True)
def swap_mutable():
    return []

if page == "Monty Hall":
    if code:
        with st.echo('below'):
            # Title
            st.title("Monty Hall")

            # Debug feature to make sure the result is correct
            debug = st.sidebar.checkbox("Show debug")
            st.sidebar.text("Show specifics")

            # List for choices
            door = door_mutable()
            chosen = chosen_mutable()
            swap = swap_mutable()

            # Clear the lists to play a new game
            if st.button("Reset"):
                door.clear()
                chosen.clear()
                swap.clear()

            # First door choices and select the winning door
            col1, col2, col3 = st.beta_columns(3)
            with col1:
                if st.button("First Door"):
                    chosen.append(1)
                    door.append(random.randint(1,3))
            with col2:
                if st.button("Second Door"):
                    chosen.append(2)
                    door.append(random.randint(1,3))
            with col3:
                if st.button("Third Door"):
                    chosen.append(3)
                    door.append(random.randint(1,3))

            # If a door has been chosen
            if len(chosen):
                # The selected door is winning, remove one of the others
                if chosen[0] == door[0]:
                    possible_doors = [1,2,3]
                    possible_doors.remove(chosen[0])
                    show_door = possible_doors[random.randint(0,1)]
                # The selected door is losing, remove the other door
                else:
                    possible_doors = [1,2,3]
                    possible_doors.remove(chosen[0])
                    possible_doors.remove(door[0])
                    show_door = possible_doors[0]
                # Tell the user what door they chose, and what door is losing
                # Ask to swap or stay
                st.write("")
                st.write(f"You have chosen Door {chosen[0]}")
                st.write(f"Door {show_door} does not have the prize")
                st.write("Would you like to swap or stay?")
                cols = st.beta_columns(10)
                with cols[2]:
                    if st.button("Swap"):
                        swap.append("Swap")
                with cols[5]:
                    if st.button("Stay"):
                        swap.append("Stay")
                # If the user has selected Stay/Swap
                if len(swap):
                    # Chosen door was winning, chose stay, win
                    if (chosen[0] == door[0]) and (swap[0] == "Stay"):
                        st.write("You win!")
                    # Chosen door was losing, chose swap, win
                    elif (chosen[0] != door[0]) and (swap[0] == "Swap"):
                        st.write("You win!")
                    # Chosen door was losing, chose stay, lose
                    # Chosen door was winning, chose swap, lose
                    else:
                        st.write("You lose :(")

            # Show the debug stats
            if debug:
                if len(chosen):
                    st.write(f"Winning door: {door[0]}")
                    st.write(f"Chosen door: {chosen[0]}")
                if len(swap):
                    st.write(f"Swap or Stay: {swap[0]}")
    else:
        st.title("Monty Hall")

        debug = st.sidebar.checkbox("Show debug")
        st.sidebar.text("Show specifics")

        st.write("Press this when done with a game to play again")
        # List for choices
        door = door_mutable()
        chosen = chosen_mutable()
        swap = swap_mutable()

        # Clear the lists to play a new game
        if st.button("Reset"):
            door.clear()
            chosen.clear()
            swap.clear()

        st.write("Choose a door by pressing on the buttons below!")
        col1, col2, col3 = st.beta_columns(3)
        with col1:
            if st.button("First Door"):
                chosen.append(1)
                door.append(random.randint(1,3))
        with col2:
            if st.button("Second Door"):
                chosen.append(2)
                door.append(random.randint(1,3))
        with col3:
            if st.button("Third Door"):
                chosen.append(3)
                door.append(random.randint(1,3))

        if len(chosen):
            if chosen[0] == door[0]:
                possible_doors = [1,2,3]
                possible_doors.remove(chosen[0])
                show_door = possible_doors[random.randint(0,1)]
            else:
                possible_doors = [1,2,3]
                possible_doors.remove(chosen[0])
                possible_doors.remove(door[0])
                show_door = possible_doors[0]
            st.write("")
            st.write(f"You have chosen Door {chosen[0]}")
            st.write(f"Door {show_door} does not have the prize")
            st.write("Would you like to swap or stay?")
            cols = st.beta_columns(10)
            with cols[2]:
                if st.button("Swap"):
                    swap.append("Swap")
            with cols[5]:
                if st.button("Stay"):
                    swap.append("Stay")
            if len(swap):
                if (chosen[0] == door[0]) and (swap[0] == "Stay"):
                    st.write("You win!")
                elif (chosen[0] != door[0]) and (swap[0] == "Swap"):
                    st.write("You win!")
                else:
                    st.write("You lose :(")

        if debug:
            if len(chosen):
                st.write(f"Winning door: {door[0]}")
                st.write(f"Chosen door: {chosen[0]}")
            if len(swap):
                st.write(f"Swap or Stay: {swap[0]}")

if page == "Monty Hall Simulation":
    st.title("Monty Hall Simulation")

def gamblers_ruin(start,stop,prob,trials):
    times_won = []
    for _ in range(trials):
        current = start
        while True:
            if(current == 0 or current == stop):
                break
            won = random.uniform(0,1)
            if won <= prob:
                current += 1
            else:
                current -= 1
        if current == 0:
            times_won.append(0)
        else:
            times_won.append(1)
    return times_won, np.sum(times_won)

if page == "Gambler's Ruin":
    if code:
        with st.echo('below'):
            # Title and user input
            st.title("Gambler's Ruin")
            start = int(st.number_input("How much money do you start with",min_value=1, value=10))
            stop = int(st.number_input("How much money should we stop at",min_value=start, value=start))
            prob = st.slider("What is the probability of winning",min_value=0.01,max_value=1.0,value=.5,step=.001)
            trials = int(st.number_input('How many trials would you like to run',min_value=1,value=100))

            # Run when pressed
            if st.button("Run trials"):
                # Run the gamblers_ruin function (renamed gamblers_ruin_dummy below)
                sequence, wins = gamblers_ruin(start,stop,prob,trials)

                st.write(f"The number of wins with {start} starting money stopping at 0 or {stop} is {wins}")

                # Make a graph to plot
                data = np.cumsum(np.array(sequence).T)
                chart_data = pd.DataFrame(data,columns=['Order'])
                st.line_chart(chart_data)

            # Renamed to preserve namespace
            def gamblers_ruin_dummy(start,stop,prob,trials):
                times_won = []
                for _ in range(trials):
                    current = start
                    while True:
                        if(current == 0 or current >= stop):
                            break
                        won = random.uniform(0,1)
                        if won <= prob:
                            current += 1
                        else:
                            current -= 1
                    if current == 0:
                        times_won.append(0)
                    else:
                        times_won.append(1)
                return times_won, np.sum(times_won)
    else:
        st.title("Gambler's Ruin")

        start = int(st.number_input("How much money do you start with",min_value=1, value=10))
        stop = int(st.number_input("How much money should we stop at",min_value=start, value=start))
        prob = st.slider("What is the probability of winning",min_value=0.01,max_value=1.0,value=.5,step=.001)

        trials = int(st.number_input('How many trials would you like to run',min_value=1,value=100))

        if st.button("Run trials"):
            sequence, wins = gamblers_ruin(start,stop,prob,trials)

            st.write(wins)

            data = np.cumsum(np.array(sequence).T)
            chart_data = pd.DataFrame(data,columns=['Order'])
            st.line_chart(chart_data)
