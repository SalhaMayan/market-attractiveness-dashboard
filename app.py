import streamlit as st
import pandas as pd

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("commerial_dataset_merged_supply demand.csv")
   

st.set_page_config(
    page_title="Market Attractiveness Dashboard",
    page_icon="💹",
    layout="centered",
)

# -----------------------------
# Page Title
# -----------------------------
st.markdown("""
    <h1 style='text-align:center; color:#0B6E4F;'>Market Attractiveness Evaluation</h1>
    <p style='text-align:left; font-size:17px; color:#444;'>A data-driven evaluation of market category attractiveness based on demand, supply, and cost indicators</p>
""", unsafe_allow_html=True)

# -----------------------------
# Category Selector
# -----------------------------
categories = sorted(df["Category_Main"].unique())
choice = st.selectbox("Select a Market Category:", categories)

# -----------------------------
# Extract Selected Category Data
# -----------------------------
row = df[df["Category_Main"] == choice].iloc[0]

demand = row["Demand_Index"]
supply = row["Supply_Index"]
cost = row["Cost_Index"]
score = row["Attractiveness"]
level = row["Category_Level"]

# -----------------------------
# Color Mapping (Attractiveness Levels)
# -----------------------------
color_map = {
    "Highly Attractive": "🟢",
    "Attractive": "🟡",
    "Moderate": "🟠",
    "Not Attractive": "🔴"
}

symbol = color_map.get(level, "⚪")

# -----------------------------
# Display Results
# -----------------------------
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

# -----------------------------
# Recommendations
# -----------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Strategic Recommendations")

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
    **Fits more experienced sellers—not ideal for new beginners.**
    """)

else:
    st.markdown("""
    **🔴 Low Market Potential**
    - Low demand  
    - Fewer suppliers  
    - Higher entry cost  
    **Better to avoid this category until a clearer strategy exists.**
    """)
