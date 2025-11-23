import streamlit as st
import pandas as pd
from openai import OpenAI
import os

# Load data
df = pd.read_csv("commerial_dataset_merged_supply demand.csv")

st.set_page_config(
    page_title="Market Attractiveness Dashboard",
    page_icon="💹",
    layout="centered",
)

# Title
st.markdown("""
    <h1 style='text-align:center; color:#0B6E4F;'>Market Attractiveness Evaluation</h1>
    <p style='text-align:left; font-size:17px; color:#444;'>A data-driven evaluation of market category attractiveness based on demand, supply, and cost indicators</p>
""", unsafe_allow_html=True)

# -----------------------------
# Category Selector With Empty Option
# -----------------------------
categories = ["-- Select Category --"] + sorted(df["Category_Main"].unique())

if "selected_category" not in st.session_state:
    st.session_state.selected_category = "-- Select Category --"


choice = st.selectbox(
    "Select a Market Category:",
    categories,
    index=categories.index(st.session_state.selected_category)
)

# Clear Button
if st.button("Clear Selection"):
    st.session_state.selected_category = "-- Select Category --"
    st.experimental_rerun()

# If user selects a valid category → Show results
if choice != "-- Select Category --":
    st.session_state.selected_category = choice

    row = df[df["Category_Main"] == choice].iloc[0]

    demand = row["Demand_Index"]
    supply = row["Supply_Index"]
    cost = row["Cost_Index"]
    score = row["Attractiveness"]
    level = row["Category_Level"]

    color_map = {
        "Highly Attractive": "🟢",
        "Attractive": "🟡",
        "Moderate": "🟠",
        "Not Attractive": "🔴"
    }
    symbol = color_map.get(level, "⚪")

    # Display Results
    st.markdown(f"""
        <h2 style='color:#0B6E4F;'>Category Results: <b>{choice}</b></h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Demand Index", f"{demand:.3f}")
        st.metric("Cost Index", f"{cost:.3f}")

    with col2:
        st.metric("Supply Index", f"{supply:.3f}")
        st.metric("Attractiveness Score", f"{score:.3f}")

    st.markdown(f"""
        <h3 style='margin-top:20px;'>Final Classification: {symbol}
            <span style='color:#333;'>{level}</span>
        </h3>
    """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("Strategic Recommendations")

    if level == "Highly Attractive":
        st.markdown("""
        **🟢 Excellent Market Opportunity**
        - High demand  
        - Stable supply chain  
        - Low entry cost  
        **Very suitable for beginners—especially with high-quality, well-reviewed products.**
        """)

    elif level == "Attractive":
        st.markdown("""
        **🟡 Good Market Potential**
        - Solid demand  
        - Reasonable entry cost  
        **Good option for new sellers with careful product selection.**
        """)

    elif level == "Moderate":
        st.markdown("""
        **🟠 Moderate Potential**
        - Demand is not weak  
        - Supply is moderate  
        **Better suited for intermediate sellers rather than beginners.**
        """)

    else:
        st.markdown("""
        **🔴 Low Market Potential**
        - Low demand  
        - Limited suppliers  
        - Higher entry cost  
        **Avoid unless you have a specialized strategy.**
        """)
else:
    st.info("Please select a category to view analysis.")

# ============================================================
# 7)  AI Market Explanation
# ============================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Need a deeper explanation?")

API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("AI Insight"):
    with st.spinner("AI is analyzing this category..."):

        mmsg = f"""
You are an assistant explaining a market category to a beginner e-commerce seller.

Use the definitions below exactly — do NOT guess or change meanings:

DEFINITIONS:
- Demand Index = consumer demand on Amazon (monthly sales, product rating, and low competition). Higher means customers actively buy.
- Supply Index = supplier availability and quality on Alibaba (number of suppliers, supplier ratings, entry cost, stability of price ranges). Higher means sourcing is easier and more reliable.
- Cost Index = how affordable it is for a beginner seller to enter this category (MOQ, unit cost, shipping cost). Higher means lower financial risk.
- Attractiveness Score = weighted combination of demand (40%), supply (30%), and cost (30%).
- Attractiveness Level = final recommended classification.

Your job:
Explain the indicators in simple business language, without changing the definitions.

Now evaluate the category:

Category: {choice}

Demand Index: {demand:.3f}
Supply Index: {supply:.3f}
Cost Index: {cost:.3f}
Attractiveness Score: {score:.3f}
Attractiveness Level: {level}
"""

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg}],
            temperature=0.3,
        )

        ai_text = completion.choices[0].message.content
        st.markdown("### AI Explanation")
        st.markdown(ai_text)


