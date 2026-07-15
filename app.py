import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Admissions Incentive Dashboard",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.main{
    background:#f5f7fb;
}

.block-container{
    padding-top:2rem;
}

.metric-card{
    background:white;
    padding:15px;
    border-radius:15px;
    box-shadow:0px 2px 10px rgba(0,0,0,.08);
}

.success-box{
    background:#E8FFF0;
    padding:18px;
    border-radius:15px;
    border-left:8px solid #00C853;
    font-size:22px;
    font-weight:bold;
}

</style>
""",unsafe_allow_html=True)

# -----------------------------
# READ EXCEL
# -----------------------------

FILE="Incentive_Owner.xlsx"

if not os.path.exists(FILE):
    st.error("Excel file not found.")
    st.stop()

df=pd.read_excel(FILE)

# Numeric Columns
for col in ["NOIDA","LUCKNOW","JAIPUR","INDORE","TOTAL","Amount"]:
    df[col]=pd.to_numeric(df[col],errors="coerce").fillna(0)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("🎯 Filters")

owners=st.sidebar.multiselect(
    "Owner",
    sorted(df["Owner"].dropna().unique())
)

campus=st.sidebar.multiselect(
    "Campus",
    sorted(df["CAMPUS"].dropna().unique())
)

if owners:
    df=df[df["Owner"].isin(owners)]

if campus:
    df=df[df["CAMPUS"].isin(campus)]

# -----------------------------
# KPI
# -----------------------------

top_owner=df.loc[df["Amount"].idxmax(),"Owner"]
top_amount=df["Amount"].max()

total_owner=len(df)

total_admission=int(df["TOTAL"].sum())

total_incentive=df["Amount"].sum()

st.title("🎓 Admissions Incentive Dashboard")

st.markdown(f"""
<div class='success-box'>
🏆 Congratulations <span style='color:#0066cc'>{top_owner}</span>!
You are currently the <b>Top Performer</b> with
<b>₹ {top_amount:,.0f}</b> incentive.
</div>
""",unsafe_allow_html=True)

st.write("")

c1,c2,c3,c4=st.columns(4)

c1.metric("👥 Total Owners",total_owner)

c2.metric("🎯 Total Admissions",f"{total_admission:,}")

c3.metric("💰 Total Incentive",f"₹ {total_incentive:,.0f}")

c4.metric("🏆 Top Performer",top_owner)

st.divider()

# -----------------------------
# CHARTS
# -----------------------------

left,right=st.columns(2)

with left:

    top5=df.sort_values("Amount",ascending=False).head(5)

    fig=px.bar(
        top5,
        x="Amount",
        y="Owner",
        orientation="h",
        color="Amount",
        text="Amount",
        title="🏆 Top 5 Performers"
    )

    fig.update_layout(yaxis={'categoryorder':'total ascending'})

    st.plotly_chart(fig,use_container_width=True)

with right:

    campus_df=pd.DataFrame({

        "Campus":["NOIDA","LUCKNOW","JAIPUR","INDORE"],

        "Admissions":[

            df["NOIDA"].sum(),

            df["LUCKNOW"].sum(),

            df["JAIPUR"].sum(),

            df["INDORE"].sum()

        ]

    })

    fig2=px.pie(

        campus_df,

        names="Campus",

        values="Admissions",

        hole=.60,

        title="🏫 Campus Contribution"

    )

    st.plotly_chart(fig2,use_container_width=True)

st.divider()

# -----------------------------
# OWNER INCENTIVE
# -----------------------------

fig3=px.bar(

    df.sort_values("Amount",ascending=False),

    x="Owner",

    y="Amount",

    color="Amount",

    title="💰 Owner Wise Incentive"

)

st.plotly_chart(fig3,use_container_width=True)

# -----------------------------
# CAMPUS ADMISSION
# -----------------------------

campus_chart=pd.DataFrame({

"Campus":["NOIDA","LUCKNOW","JAIPUR","INDORE"],

"Admissions":[

df["NOIDA"].sum(),

df["LUCKNOW"].sum(),

df["JAIPUR"].sum(),

df["INDORE"].sum()

]

})

fig4=px.bar(

campus_chart,

x="Campus",

y="Admissions",

text="Admissions",

color="Admissions",

title="📊 Campus Wise Admissions"

)

st.plotly_chart(fig4,use_container_width=True)

# -----------------------------
# LEADERBOARD
# -----------------------------

st.subheader("🏅 Incentive Leaderboard")

leaderboard=df.sort_values(

"Amount",

ascending=False

)

leaderboard.index=leaderboard.index+1

st.dataframe(

leaderboard,

use_container_width=True,

height=600

)

st.caption("Designed by Himanshu Kumar | Admissions Incentive Dashboard")