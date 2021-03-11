import streamlit as st
import random
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


page = st.sidebar.radio("Which project would you like to run?",("Estimate pi","Confidence Interval","Correlation"))
code = st.sidebar.checkbox("Show the code")
st.sidebar.text("Shows the code below the project")

st.markdown(f"""<style>.reportview-container .main .block-container{{max-width:{1920}px;padding-right:{20}rem;padding-left:{20}rem;}}}}</style>""",unsafe_allow_html=True)


if page == "Estimate pi":
    if code:
        with st.echo('below'):
            st.title("Estimating pi")
            # Get number of points to generate
            samples = int(st.number_input('Enter the number of points to generate',min_value=1,value=100))
            # Run the simulation
            if st.button("Run"):
                # Generate points uniformly random
                pts = [(random.uniform(-1,1),random.uniform(-1,1)) for _ in range(samples)]

                # Find the points inside or outside the unit circle
                inside = []
                outside = []
                for pt in pts:
                    if np.linalg.norm(pt) <= 1:
                        inside.append(pt)
                    else:
                        outside.append(pt)

                fig = plt.figure(figsize=(5,5))
                ax = plt.gca()
                ax.set_ylim((-1,1))
                ax.set_xlim((-1,1))

                # Plot the points inside/outside
                if len(inside):
                    plt.scatter(*zip(*inside),s=3,c='blue')
                if len(outside):
                    plt.scatter(*zip(*outside),s=3,c='red')
                # Plot the unit circle
                ax.add_patch(plt.Circle((0,0),1,fill=False,ec='black'))

                # Approximate pi
                st.write(f"Approximation for pi : {4 * len(inside) / len(pts)}")

                # Show the plot
                st.write(fig)
    else:
        st.title("Estimating pi")
        # Get number of points to generate
        samples = int(st.number_input('Enter the number of points to generate',min_value=1,value=100))
        # Run the simulation
        if st.button("Run"):
            # Generate points uniformly random
            pts = [(random.uniform(-1,1),random.uniform(-1,1)) for _ in range(samples)]

            # Find the points inside or outside the unit circle
            inside = []
            outside = []
            for pt in pts:
                if np.linalg.norm(pt) <= 1:
                    inside.append(pt)
                else:
                    outside.append(pt)

            fig = plt.figure(figsize=(5,5))
            ax = plt.gca()
            ax.set_ylim((-1,1))
            ax.set_xlim((-1,1))

            # Plot the points inside/outside
            if len(inside):
                plt.scatter(*zip(*inside),s=3,c='blue')
            if len(outside):
                plt.scatter(*zip(*outside),s=3,c='red')
            # Plot the unit circle
            ax.add_patch(plt.Circle((0,0),1,fill=False,ec='black'))

            # Approximate pi
            st.write(f"Approximation for pi : {4 * len(inside) / len(pts)}")

            # Show the plot
            st.write(fig)


class Bernoulli(object):
    def __init__(self,p):
        self.p = p
        self.var = p * (1 - p)
        self.std = np.sqrt(p * (1 - p))
    def __call__(self):
        return 1 if random.uniform(0,1) < self.p else 0

def between(a,x,y):
    if a >= x and a <= y:
        return 1
    else:
        return 0

if page == "Confidence Interval":
    if code:
        with st.echo('below'):
            st.title("Confidence Interval")
            # Get the p
            p = st.number_input("Enter the probability for the Bernoulli trial",min_value=0.01,max_value=1.0,value=.5)
            # Create a Bernoulli Trial
            b = Bernoulli(p)

            # class Bernoulli(object):
            #     def __init__(self,p):
            #         self.p = p
            #         self.var = p * (1 - p)
            #         self.std = np.sqrt(p * (1 - p))
            #     def __call__(self):
            #         return 1 if random.uniform(0,1) < self.p else 0

            # Get the number of simulations
            trials = int(st.number_input("Enter the number of simulations to run",min_value=1,value=100))
            # Get the number of Bernoulli trials per simulation
            n = int(st.number_input("Enter the number of Bernoulli trials per simulation",min_value=1,value=10000))

            # Run the simulation
            if st.button("Run"):
                # For a trial in the number of simulations
                # Run a Bernoulli trial, trial number of times
                # Then count how many were successes
                successes = [np.array([b() for trial in range(n)]).sum() for run in range(trials)]
                # Calculate the 95% confidence interval
                CI = [(b.p - 2 * np.sqrt(b.var/n)) * n, (b.p + 2 * np.sqrt(b.var/n)) * n]
                st.write(f"95% Confidence Interval : [{CI[0] : .0f},{CI[1] : .0f}]")

                # Find how many times the number of successes was within the confidence interval
                btwns = np.array([between(cnt,CI[0],CI[1]) for cnt in successes]).sum()
                st.write(f"Number of times the number of successes was within the 95% confidence interval : {btwns}")
                st.write(f"Percentage of times the number of success was within the 95% confidence interval : {(btwns / trials) * 100 : .2f}%")
    else:
        st.title("Confidence Interval")
        # Get the p
        p = st.number_input("Enter the probability for the Bernoulli trial",min_value=0.01,max_value=1.0,value=.5)
        b = Bernoulli(p)
        trials = int(st.number_input("Enter the number of simulations to run",min_value=1,value=100))
        n = int(st.number_input("Enter the number of Bernoulli trials per trial",min_value=1,value=10000))

        # Run the simulation
        if st.button("Run"):
            successes = [np.array([b() for trial in range(n)]).sum() for run in range(trials)]
            #st.write(successes)
            #st.write(successes[0])
            CI = [(b.p - 2 * np.sqrt(b.var/n)) * n, (b.p + 2 * np.sqrt(b.var/n)) * n]
            st.write(f"95% Confidence Interval : [{CI[0] : .0f},{CI[1] : .0f}]")

            btwns = np.array([between(cnt,CI[0],CI[1]) for cnt in successes]).sum()
            st.write(f"Number of times the number of successes was within the 95% confidence interval : {btwns}")
            st.write(f"Percentage of times the number of success was within the 95% confidence interval : {(btwns / trials) * 100 : .2f}%")

@st.cache(suppress_st_warning=True)
def load_data(path):
    st.write("Loading data...")
    return pd.read_csv(path)

def correlation(data,col1,col2):
    st.write(f"Pair: {col1} and {col2}")
    mean1 = data[col1].mean()
    mean2 = data[col2].mean()
    st.write(f"{col1} mean: {mean1 : .2f}")
    st.write(f"{col2} mean: {mean2 : .2f}")

    std1 = data[col1].std()
    std2 = data[col2].std()
    st.write(f"{col1} standard deviation: {std1 : .2f}")
    st.write(f"{col2} standard deviation: {std2 : .2f}")

    n = len(data[col1].values)

    top = [(data[col1].values[i] - mean1) * (data[col2].values[i] - mean2) for i in range(n)]
    corr = np.sum(top) / ((n - 1) * std1 * std2)
    st.write(f"Correlation: {corr : .2f}")
    return corr

def check_against_correlation(data,label):
    other_columns = list(data.columns).copy()
    other_columns.remove(label)

    corrs = []
    for col in other_columns:
        st.write("----------------------------")
        corrs.append([correlation(data,col,label),col])
    return corrs

if page == "Correlation":
    if code:
        with st.echo('below'):
            st.title("Correlation")
            # Load the data
            data = load_data("./Coding2_Data.csv")
            # Calculate the correlations
            corrs = check_against_correlation(data,"Course Grade")
            # Create dataframe from the correlations, output to file
            df = pd.DataFrame(corrs,columns=["Correlation","Predictor"])
            df.sort_values(by="Correlation",inplace=True,ascending=False)
            df.to_csv("./Correlations.csv")

            # def correlation(data,col1,col2):
            #     st.write(f"Pair: {col1} and {col2}")
            #     # Calculate mean for each set
            #     mean1 = data[col1].mean()
            #     mean2 = data[col2].mean()
            #     st.write(f"{col1} mean: {mean1 : .2f}")
            #     st.write(f"{col2} mean: {mean2 : .2f}")
            #
            #     # Calculate std for each set
            #     std1 = data[col1].std()
            #     std2 = data[col2].std()
            #     st.write(f"{col1} standard deviation: {std1 : .2f}")
            #     st.write(f"{col2} standard deviation: {std2 : .2f}")
            #
            #     n = len(data[col1].values)
            #
            #     # Sum of (x_i - xbar) * (y_i - ybar)
            #     top = [(data[col1].values[i] - mean1) * (data[col2].values[i] - mean2) for i in range(n)]
            #     # Sum the top, divide by (n - 1) * s_x * s_y
            #     corr = np.sum(top) / ((n - 1) * std1 * std2)
            #     st.write(f"Correlation: {corr : .2f}")
            #     return corr
            #
            # def check_against_correlation(data,label):
            #     # Get the pairs of other columns
            #     other_columns = list(data.columns).copy()
            #     other_columns.remove(label)
            #
            #     # Calculate the correlation of each pair
            #     corrs = []
            #     for col in other_columns:
            #         st.write("----------------------------")
            #         corrs.append([correlation(data,col,label),col])
            #     return corrs
    else:
        st.title("Correlation")
        # Load the data
        data = load_data("./Coding2_Data.csv")

        # Calculate the correlations
        corrs = check_against_correlation(data,"Course Grade")
        # Create dataframe from the correlations, output to file
        df = pd.DataFrame(corrs,columns=["Correlation","Predictor"])
        df.sort_values(by="Correlation",inplace=True,ascending=False)
        df.to_csv("./Correlations.csv")
