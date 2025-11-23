import streamlit as st
import pandas as pd
from openai import OpenAI
import os

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("commerial_dataset_merged_supply demand.csv")

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Market Attractiveness Dashboard",
    page_icon="💹",
    layout="centered",
)

# -----------------------------
# OpenAI Client
# -----------------------------
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# -----------------------------
# Page Title
# -----------------------------
st.markdown("""
    <h1 style='text-align:center; color:#0B6E4F;'>Market Attractiveness Evaluation</h1>
    <p style='text-align:left; font-size:17px; color:#444;'>
    A data-driven evaluation of market category attractiveness based on demand, supply, and entry cost indicators.
    </p>
""", unsafe_allow_html=True)

# -----------------------------
# Category Selector
# -----------------------------
categories = ["-- Select Category --"] + sorted(df["Category_Main"].unique())
choice = st.selectbox("Select a Market Category:", categories)

# -----------------------------
# Initial values (empty before selection)
# -----------------------------
if choice == "-- Select Category --":
    demand = supply = cost = score = None
    level = "N/A"
else:
    row = df[df["Category_Main"] == choice].iloc[0]
    demand = row["Demand_Index"]
    supply = row["Supply_Index"]
    cost = row["Cost_Index"]
    score = row["Attractiveness"]
    level = row["Category_Level"]

# -----------------------------
# Color Mapping
# -----------------------------
color_map = {
    "Highly Attractive": "🟢",
    "Attractive": "🟡",
    "Moderate": "🟠",
    "Not Attractive": "🔴",
    "N/A": "⚪"
}
symbol = color_map.get(level, "⚪")

# -----------------------------
# Display Results (Static)
# -----------------------------
st.markdown(f"<h2 style='color:#0B6E4F;'>Category Results:</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.metric("Demand Index", "---" if demand is None else f"{demand:.3f}")
    st.metric("Cost Index", "---" if cost is None else f"{cost:.3f}")

with col2:
    st.metric("Supply Index", "---" if supply is None else f"{supply:.3f}")
    st.metric("Attractiveness Score", "---" if score is None else f"{score:.3f}")

st.markdown(f"""
    <h3 style='margin-top:20px;'>Final Classification: 
        {symbol} <span style='color:#333;'>{level}</span>
    </h3>
""", unsafe_allow_html=True)

# -----------------------------
# Recommendations
# -----------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Strategic Recommendations")

if choice == "-- Select Category --":
    st.info("Please select a category to view recommendations.")
else:
    if level == "Highly Attractive":
        st.markdown("""
        **🟢 Excellent Market Opportunity**
        - High demand  
        - Stable supply chain  
        - Low entry cost  
        **A strong category for beginners—especially with high-quality, well-reviewed products.**
        """)

    elif level == "Attractive":
        st.markdown("""
        **🟡 Good Market Potential**
        - Demand is solid  
        - Entry costs are reasonable  
        **Suitable for entry, but requires careful product selection due to competition.**
        """)

    elif level == "Moderate":
        st.markdown("""
        **🟠 Moderate Market Potential**
        - Demand is not weak  
        - Supply is moderate  
        **Better suited to more experienced sellers—not ideal for new beginners.**
        """)

    else:
        st.markdown("""
        **🔴 Low Market Potential**
        - Low demand  
        - Limited suppliers  
        - Higher entry cost  
        **Avoid this category unless a clear specialized strategy is planned.**
        """)

# -----------------------------
# AI Insights Section
# -----------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("AI Insights")

explain_btn = st.button("Get AI Market Explanation")

if explain_btn:
    if choice == "-- Select Category --":
        st.warning("Please select a category first.")
    else:
        user_question = f"""
        Provide a clear explanation for this e-commerce market category:

        Category: {choice}
        Demand Index: {demand:.3f}
        Supply Index: {supply:.3f}
        Cost Index: {cost:.3f}
        Attractiveness Score: {score:.3f}
        Level: {level}

        Explain:
        - What these indicators mean
        - Why the category is attractive or not
        - Expected capital range for a beginner seller
        - Key risks
        - Suggested product strategy
        - Keep the explanation simple, practical, and beginner-friendly.
        """

        with st.spinner("AI is analyzing this category..."):
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": user_question}],
                temperature=0.4,
            )

            msg_obj = completion.choices[0].message
            ai_text = msg_obj.content if hasattr(msg_obj, "content") else msg_obj["content"]

            st.write(ai_text)
