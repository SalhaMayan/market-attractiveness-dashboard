import streamlit as st
import pandas as pd
import os
from openai import OpenAI

# ============================================================
# 1) إعدادات الصفحة
# ============================================================
st.set_page_config(
    page_title="Market Attractiveness Dashboard",
    
    layout="centered",
)

# ============================================================
# 2) تحميل البيانات
# ============================================================
df = pd.read_csv("commerial_dataset_merged_supply demand.csv")

# ============================================================
# 3) واجهة التطبيق
# ============================================================
st.markdown("""
    <h1 style='text-align:center; color:#0B6E4F;'>Market Attractiveness Evaluation</h1>
    <p style='text-align:left; font-size:17px; color:#444;'>
        A data-driven evaluation of market category attractiveness based on demand, supply, and entry cost indicators.
    </p>
""", unsafe_allow_html=True)

# قائمة الفئات
categories = sorted(df["Category_Main"].unique())
choice = st.selectbox("Select a Market Category:", categories)

# بيانات الفئة
row = df[df["Category_Main"] == choice].iloc[0]

demand = row["Demand_Index"]
supply = row["Supply_Index"]
cost = row["Cost_Index"]
score = row["Attractiveness"]
level = row["Category_Level"]

# ============================================================
# 4) رموز الجاذبية
# ============================================================
color_map = {
    "Highly Attractive": "🟢",
    "Attractive": "🟡",
    "Moderate": "🟠",
    "Not Attractive": "🔴"
}

symbol = color_map.get(level, "⚪")

# ============================================================
# 5) عرض المؤشرات
# ============================================================
st.markdown(f"""
    <h2 style='color:#0B6E4F;'>Category Results: <b>{choice}</b></h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.metric("Demand Index", f"{demand:.3f}", help="Measures how strong consumer demand is in this market category.")
    st.metric("Cost Index", f"{cost:.3f}", help="Indicates how easy it is to enter financially (higher = cheaper entry).")

with col2:
    st.metric("Supply Index", f"{supply:.3f}", help="Shows supplier availability, reliability, and price stability.")
    st.metric("Attractiveness Score", f"{score:.3f}", help="Weighted combination of demand, supply, and cost.")

st.markdown(f"""
    <h3 style='margin-top:20px;'>Final Classification: {symbol}
    <span style='color:#333;'>{level}</span></h3>
""", unsafe_allow_html=True)

# ============================================================
# 6) توصيات مدمجة
# ============================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Strategic Recommendations")

if level == "Highly Attractive":
    st.markdown("""
    **🟢 Excellent Market Opportunity**
    - High demand  
    - Strong supplier ecosystem  
    - Low entry cost  
    Ideal for beginners with minimal risk.
    """)

elif level == "Attractive":
    st.markdown("""
    **🟡 Good Market Potential**
    - Stable demand  
    - Reasonable entry cost  
    Suitable for beginners but requires careful product differentiation.
    """)

elif level == "Moderate":
    st.markdown("""
    **🟠 Moderate Opportunity**
    - Mixed demand  
    - Moderate supplier depth  
    Better suited for sellers with some experience and capital.
    """)

else:
    st.markdown("""
    **🔴 Low Potential**
    - Weak demand  
    - High entry costs  
    - Limited supplier reliability  
    Not recommended for beginners at this stage.
    """)
# ============================================================
# 7)  AI Market Explanation
# ============================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("Need a deeper explanation?")

API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if st.button("AI Insight"):
    with st.spinner("AI is analyzing this category..."):

        msg = f"""
        Explain this market category to a beginner seller.

        Category: {choice}

        Demand Index: {demand:.3f}
        Supply Index: {supply:.3f}
        Cost Index: {cost:.3f}
        Attractiveness Score: {score:.3f}
        Level: {level}
        """

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": msg}],
            temperature=0.3,
        )

        st.markdown("### AI Explanation:")
        st.write(completion.choices[0].message["content"])
