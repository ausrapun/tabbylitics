from question_catalogue import question_catalogue
from data_loader import raw_survey_data
import pandas as pd
import re

# load the raw survey data
df = raw_survey_data

# Step 1: Reshape existing dataset to RespondentID, Question, Answer format
df_long = df.melt(
    id_vars=["RespondentID"],
    var_name="Question",
    value_name="Answer"
)

# Step 2: Apply transformations using the catalogue
tidy_frames = []

for question, meta in question_catalogue.items():
    qtype = meta["type"]

    # Filter only this question
    temp = df_long[df_long["Question"] == question].copy()

    # For multi-choice questions, split the answers into separate rows
    if qtype == "multi_choice":
        delimiter = meta.get("delimiter", "|")
        temp = temp.dropna()
        temp["Answer"] = temp["Answer"].str.split(rf"\s*{re.escape(delimiter)}\s*")
        temp = temp.explode("Answer")
        temp["Answer"] = temp["Answer"].str.strip()

    # Enforce datatype from catalogue (for questions with range answers because they are integers)
    dtype = meta.get("datatype", "string")
    if dtype == "int":
        temp["Answer"] = pd.to_numeric(temp["Answer"], errors="coerce").astype("Int64")
    elif dtype == "string":
        temp["Answer"] = temp["Answer"].astype(str)

    tidy_frames.append(temp)

# Step 3: Concatenate all into one unified df
df_unified_dataset = pd.concat(tidy_frames, ignore_index=True)


# some print statements for verification 

#print(df_unified_dataset.head(100).to_json(orient="records", indent=2))
#print(f"Total rows in df_unified_dataset: {len(df_unified_dataset)}")
#print("RespondentID range:", df_unified_dataset["RespondentID"].min(), "-", df_unified_dataset["RespondentID"].max())
