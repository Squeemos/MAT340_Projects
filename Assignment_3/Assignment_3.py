import streamlit as st
import random
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


page = st.sidebar.radio("Which project would you like to run?",("Gambler's Ruin II","Absorption Times","Polya's Urn","Random Walk"))


def make_probability_distribution(x):
    p_dict = {}
    for value in np.arange(0,1,.05):
        p_dict[round(value,2)] = 0
    for pt in x:
        for value in np.arange(0,1,.05):
            if pt >= value and pt < value + .05:
                p_dict[round(value,2)] += 1
    for key in p_dict.keys():
        p_dict[key] /= len(x)
    return p_dict

if page == "Gambler's Ruin II":
    st.title("Gambler's Ruin II")
    starting = st.number_input("Enter a dollar amount",min_value=0,value=10)
    win = st.number_input("Enter the number you would like to stop at",min_value=0,value=20)
    p = st.slider("Enter the probability of winning (p)",min_value = .01,max_value =1.0,value=.5)
    n = st.number_input("Enter the number of matches to play",min_value=1,value=100)

    initial = np.zeros(win + 1)
    initial[starting] = 1

    matrix = np.zeros((win + 1,win + 1))
    for loc in range(win + 1):
        if loc == 0 or loc == win:
            matrix[loc,loc] = 1
        else:
            matrix[loc,loc + 1] = p
            matrix[loc,loc - 1] = 1 - p
    dist = matrix.copy()
    for iteration in range(1,n):
        dist = dist @ matrix
    st.write((initial @ dist).reshape(1,-1))

if page == "Absorption Times":
    st.title("Absorption Times")
    num_heads = st.number_input("Enter the number of desired heads",value=3)
    trials = st.number_input("Enter the number of trials",value=2500,min_value=2500)

    num_flips = []
    for trial in range(trials):
        t_h = 0
        flips = 0
        while t_h < num_heads:
            p = random.random()
            if p <= .5:
                t_h += 1
            else:
                t_h = 0
            flips += 1
        num_flips.append(flips)
    mean = np.mean(num_flips)
    st.write(f"The expected number of flips in {trials} trials getting {num_heads} heads in a row is: {mean}")
    fig = plt.figure(figsize=(10,10))
    plt.hist(num_flips,bins=100)
    plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
    min_ylim, max_ylim = plt.ylim()
    plt.text(mean *1.1, max_ylim*0.9, f"Mean: {mean:.2f}")
    st.write(fig)
    st.button("Rerun")

if page == "Polya's Urn":
    st.title("Polya's Urn")
    x = st.number_input("Enter the number of green balls",min_value=1,value=50)
    y = st.number_input("Enter the number of orange balls",min_value=1,value=50)
    trials = st.number_input("Enter the number of trials",value=2500,min_value=2500)

    num_green = []

    for trial in range(trials):
        green = x
        orange = y

        for _ in range(1000):
            p_x = green / (green + orange)
            prob = random.random()
            if prob <= p_x:
                green += 1
            else:
                orange += 1
        num_green.append(green / (1000 + x + y))

    dist = make_probability_distribution(num_green)
    fig = plt.figure(figsize=(10,10))
    plt.bar(range(len(dist)),list(dist.values()),align='edge',color='green')
    plt.xticks(range(len(dist)),list(dist.keys()))
    plt.xlabel("Percent of balls that were green (left inclusive)")
    plt.ylabel("Percent of trials")
    plt.title("Probability Distribution of Green Balls")
    st.write(fig)
    st.button("Rerun")

if page == "Random Walk":
    st.title("Random Walk")

    d = st.number_input("Enter the dimension",min_value=1,value=2)
    n = st.number_input("Enter the number of steps to take",min_value=1,value=100)
    trials = st.number_input("Enter the number of trials",min_value=1,value=2500)

    dists = []
    for trial in range(trials):
        location = [0 for _ in range(d)]
        for step in range(n):
            pos = np.random.randint(0,2*d)
            if pos < d:
                location[pos] -= 1
            else:
                location[pos - d] += 1
        dists.append(np.linalg.norm(location))
    st.write(f"The average distance from the origin after {n} steps in {trials} trials is {np.mean(dists):.2f}")
    st.button("Rerun")
