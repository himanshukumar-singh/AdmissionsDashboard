import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Admissions Incentive Dashboard",
    page_icon="🎓",
    layout="wide"
)

FILE = "Incentive_Owner.xlsx"

if not os.path.exists(FILE):
    st.error("❌ Incentive_Owner.xlsx file project folder me nahi mili.")
    st.stop()

df = pd.read_excel(FILE)

# Numeric columns
for col in ["NOIDA","LUCKNOW","JAIPUR","INDORE","Total","Incentive Amount"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Sidebar
st.sidebar.title("🎯 Filters")

owners = st.sidebar.multiselect(
    "Owner",
    sorted(df["Owner"].dropna().unique())
)

if owners:
    df = df[df["Owner"].isin(owners)]

st.title("🎓 Admissions Incentive Dashboard")

col1,col2,col3,col4 = st.columns(4)

col1.metric("👥 Total Owners", len(df))
col2.metric("🎯 Total Admissions", int(df["Total"].sum()))
col3.metric("💰 Total Incentive", f"₹ {df['Incentive Amount'].sum():,.0f}")

top_owner = df.loc[df["Incentive Amount"].idxmax(),"Owner"]
top_amt = df["Incentive Amount"].max()

col4.metric("🏆 Top Performer", top_owner)

st.divider()

left,right = st.columns(2)

with left:
    fig = px.bar(
        df.sort_values("Incentive Amount",ascending=False),
        x="Owner",
        y="Incentive Amount",
        color="Incentive Amount",
        title="Owner Wise Incentive"
    )
    st.plotly_chart(fig,use_container_width=True)

with right:
    campus = pd.DataFrame({
        "Campus":["NOIDA","LUCKNOW","JAIPUR","INDORE"],
        "Admissions":[
            df["NOIDA"].sum(),
            df["LUCKNOW"].sum(),
            df["JAIPUR"].sum(),
            df["INDORE"].sum()
        ]
    })

    fig2 = px.pie(
        campus,
        names="Campus",
        values="Admissions",
        hole=0.5,
        title="Campus Contribution"
    )

    st.plotly_chart(fig2,use_container_width=True)

st.divider()

st.subheader("🏆 Incentive Leaderboard")

leaderboard = df.sort_values(
    "Incentive Amount",
    ascending=False
)

st.dataframe(
    leaderboard,
    use_container_width=True,
    hide_index=True
)