import streamlit as st
import pandas as pd
from openai import OpenAI

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("commerial_dataset_merged_supply demand.csv")

# Initialize OpenAI client (uses Streamlit Secrets)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# Streamlit Page Settings
# -----------------------------
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
    <p style='text-align:left; font-size:17px; color:#444;'>
        A data-driven evaluation of market category attractiveness based on demand, supply, and cost indicators.
    </p>
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
# Color Mapping
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
    **Ideal for beginners with high-quality products.**
    """)

elif level == "Attractive":
    st.markdown("""
    **🟡 Good Market Potential**
    - Strong demand  
    - Reasonable entry cost  
    **Suitable for new sellers with some competition awareness.**
    """)

elif level == "Moderate":
    st.markdown("""
    **🟠 Moderate Market Potential**
    - Demand is acceptable  
    - Supply is moderate  
    **Better suited for experienced sellers.**
    """)

else:
    st.markdown("""
    **🔴 Low Market Potential**
    - Low demand  
    - Limited supplier availability  
    - High entry cost  
    **Not recommended for new or small sellers.**
    """)

# -----------------------------
# GPT Explanation Section
# -----------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("AI Explanation (GPT-Powered)")

if st.button("Explain this category using GPT"):
    with st.spinner("Generating explanation..."):
        
        prompt = f"""
        You are an expert in e-commerce market analysis.
        Explain the attractiveness classification for the category: {choice}.

        Data:
        - Demand Index: {demand:.3f}
        - Supply Index: {supply:.3f}
        - Cost Index: {cost:.3f}
        - Final Attractiveness Level: {level}

        Explain clearly:
        1. What this attractiveness level means in practical business terms.
        2. Whether this category is suitable for small/new sellers or experienced sellers.
        3. What the demand index indicates.
        4. What the supply index indicates.
        5. What the cost index indicates.
        6. An approximate investment level (low / medium / high).
        7. A short strategic recommendation.

        The explanation must be easy for non-technical users.
        """

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=350,
            temperature=0.4,
        )

        explanation = completion.choices[0].message["content"]

        st.markdown("### Detailed Explanation")
        st.write(explanation)
