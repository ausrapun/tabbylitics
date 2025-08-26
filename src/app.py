import streamlit as st
import pandas as pd
import plotly.express as px
from question_catalogue import question_catalogue
from unified_dataset import df_unified_dataset

# Load unified dataset
df = df_unified_dataset

# --- Define Streamlit sidebar dropdowns ---
question_options = list(question_catalogue.keys())
selected_question = st.sidebar.selectbox("Select Survey Question", question_options)

# dimension is optional
dimension_options = ["None"] + [
    q for q, meta in question_catalogue.items()
    if meta["type"] in ["single_choice", "scale"] and q != selected_question
]
selected_dimension = st.sidebar.selectbox("Select Comparative Dimension (optional)", dimension_options)

# Filter dataset for the selected question
df_question = df[df["Question"] == selected_question]
qtype = question_catalogue[selected_question]["type"]

# title of the app
st.write(f"## Satisfaction Survey Analysis")

# --- Bar chart for main question ---
if qtype not in ["free_text", "scale"]:
    counts = df_question["Answer"].value_counts().sort_values(ascending=True)
    total = counts.sum()
    percentages = (counts / total * 100).round(1).astype(str) + "%"

    fig = px.bar(
        x=counts.values,
        y=counts.index,
        orientation='h',
        text=percentages,
        labels={"x": "Number of Respondents", "y": "Answer"},
        title=f"Bar chart for {selected_question}"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

# --- Table for single question ---
st.write(f"{selected_question}")

if selected_dimension == "None":
    # No comparative dimension i.e. display free text answers
    if qtype == "free_text":
        st.write("**Text responses:**")
        for idx, answer in enumerate(df_question["Answer"], start=1):
            st.write(f"{idx}. {answer}")

    elif qtype == "scale":
        df_question["Answer"] = pd.to_numeric(df_question["Answer"], errors="coerce")
        avg_score = df_question["Answer"].mean()
        max_val = 10
        avg_percentage = (avg_score / max_val * 100).round(1)
        df_avg = pd.DataFrame({"AverageScore": [avg_score], "PercentageOfMax": [avg_percentage]})
        styled = df_avg.style.background_gradient(subset=["PercentageOfMax"], cmap="Purples").format({"AverageScore": "{:.1f}", "PercentageOfMax": "{:.1f}%"})
        st.write("**Average total score and the percentage of respondents who scored the maximum**")
        st.dataframe(styled)

    else:  # single_choice or multi_choice
        counts = df_question["Answer"].value_counts()
        total = counts.sum()
        percentages = (counts / total * 100).round(1)
        table = pd.DataFrame({
            "Answer": counts.index,
            "RespondentCount": counts.values,
            "Percentage": percentages.values
        })
        table = table.sort_values("Percentage", ascending=False)
        styled = table.style.background_gradient(subset=["Percentage"], cmap="Purples").format({"Percentage": "{:.1f}%"})
        st.dataframe(styled)

# --- Table for comparative dimension ---
else:
    # Comparative dimension selected
    df_dimension = df[df["Question"] == selected_dimension]
    merged = pd.merge(
        df_question, df_dimension,
        on="RespondentID",
        suffixes=("_main", "_dimension")
    )

    if qtype in ["single_choice", "multi_choice"]:
        pivot = pd.crosstab(
            merged["Answer_dimension"],
            merged["Answer_main"]
        )
        pivot_percentage = pivot.div(pivot.sum(axis=1), axis=0).multiply(100).round(1)
        pivot_percentage["MaxValue"] = pivot_percentage.max(axis=1)
        pivot_percentage = pivot_percentage.sort_values("MaxValue", ascending=False).drop(columns="MaxValue")
        styled = pivot_percentage.style.background_gradient(cmap="Purples").format("{:.1f}%")
        st.write(f"{selected_question} compared to {selected_dimension}")
        st.dataframe(styled)

# --- Free text and scale questions dont use charts for---
    elif qtype == "scale":
        merged["Answer_main"] = pd.to_numeric(merged["Answer_main"], errors="coerce")
        avg_scores = merged.groupby("Answer_dimension")["Answer_main"].mean().round(1)
        max_val = 10
        avg_percentages = (avg_scores / max_val * 100).round(1)
        df_avg = pd.DataFrame({
            selected_dimension: avg_scores.index,
            "AverageScore": avg_scores.values,
            "PercentageOfMax": avg_percentages.values
        })
        df_avg = df_avg.sort_values("PercentageOfMax", ascending=False)
        styled = df_avg.style.background_gradient(subset=["PercentageOfMax"], cmap="Purples").format({"AverageScore": "{:.1f}", "PercentageOfMax": "{:.1f}%"})
        st.write(f"**Average {selected_question} by {selected_dimension}:**")
        st.dataframe(styled)

    elif qtype == "free_text":
        st.write(f"**Text responses grouped by {selected_dimension}:**")
        grouped = merged.groupby("Answer_dimension")["Answer_main"].apply(list)
        for group, texts in grouped.items():
            st.write(f"**{selected_dimension}: {group}**")
            for idx, answer in enumerate(texts, start=1):
                st.write(f"{idx}. {answer}")

