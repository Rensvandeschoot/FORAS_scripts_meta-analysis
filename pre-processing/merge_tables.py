import pandas as pd
import numpy as np
import re

# Load the data
df_general = pd.read_excel("../data/Data_extraction_general_data.xlsx")

df_model_results = pd.read_excel("../data/Data_extraction_model_results.xlsx")

grolts_scores = pd.read_csv("../data/grolts_scores.csv")
grolts_scores = grolts_scores[["paper_id", "score"]]
grolts_scores.rename(columns={"paper_id": "MID", "score": "Grolts"}, inplace=True)


def print_duplicates(df, name):
    dupes = df[df.duplicated("MID", keep=False)]
    if not dupes.empty:
        print(f"\n🔁 Non-unique MIDs in {name}:")
        print(dupes[["MID"]].drop_duplicates())
    else:
        print(f"\n✅ No duplicate MIDs in {name}.")


def print_common_mids(df1, df2, name1, name2, expected_count=None):
    mids1 = set(df1["MID"])
    mids2 = set(df2["MID"])

    common = mids1.intersection(mids2)
    actual_count = len(common)

    label = f"\n🔗 Common MIDs between {name1} and {name2}:"
    if expected_count is not None:
        if actual_count == expected_count:
            label = f"\n✅ Common MIDs between {name1} and {name2}"
            print(f"{label} matches expected value of {actual_count}")
        else:
            print(f"{label} ❌ {actual_count} (expected {expected_count})")
    else:
        print(label)
        print(f"{name1} count: {len(df1)}, {name2} count: {len(df2)}")
        print(f"Common MID count: {actual_count}")


def print_missing_mids(source_df, target_df, source_name, target_name, contains=False):
    if contains:
        target_mids = target_df["MID"].astype(str).tolist()

        def has_match(mid):
            # Check if mid (from source) starts with any target MID (the base)
            return any(mid.startswith(t) for t in target_mids)

        missing = source_df[~source_df["MID"].astype(str).apply(has_match)]
        count = len(missing)
    else:
        missing = source_df[~source_df["MID"].isin(target_df["MID"])]
        count = len(missing)

    label = f"\n🔍 MIDs in {source_name} but not in {target_name}:"
    if count == 0:
        label = f"\n✅ MIDs in {source_name} but not in {target_name}:"
        print(f"{label} {count}")
    else:
        print(f"{label} ❌ ({count} missing)")
        print(missing["MID"].tolist())


# === Run Sanity Checks ===

# 1. Duplicates
print_duplicates(df_general, "df_general")
print_duplicates(df_model_results, "df_model_results")
print_duplicates(grolts_scores, "grolts_scores")

# 2. Common MIDs
print_common_mids(df_general, df_model_results, "df_general", "df_model_results", 113)
print_common_mids(
    df_model_results, grolts_scores, "df_model_results", "grolts_scores", 99
)

# 3. Missing MIDs
print_missing_mids(df_general, df_model_results, "df_general", "df_model_results")
print_missing_mids(df_model_results, df_general, "df_model_results", "df_general")
print_missing_mids(
    df_model_results, grolts_scores, "df_model_results", "grolts_scores", contains=True
)
print_missing_mids(grolts_scores, df_model_results, "grolts_scores", "df_model_results")


# === Merge data ===

# 4. Merge the 4 DataFrames on 'MID', and drop duplicate columns
merged_df = df_general.merge(
    df_model_results, on="MID", suffixes=("_general", "_model_results")
)

merged_df["MID_base"] = merged_df["MID"].str.extract(r"^(MU?\d+)", expand=False)
merged_df = merged_df.merge(
    grolts_scores, left_on="MID_base", right_on="MID", how="left"
)
merged_df.drop(columns=["MID_base", "MID_y"], inplace=True)
merged_df.rename(columns={"MID_x": "MID"}, inplace=True)

# 5. Create Location_US column programmatically
merged_df["Location_US"] = merged_df["Location? Where the study is based"].apply(
    lambda x: "US" if re.fullmatch(r'(US|USA)', str(x), re.IGNORECASE) else "Other"
)

# 6. Select columns used in R analysis
merged_df = merged_df[
    [
        "Study",
        "Sample_name",
        "MID",
        "Grolts",
        "Sample_Size",
        "Mean_age",
        "Developmental_age",
        "Percentage_women",
        "Percentage_minority",
        "Percentage_partner",
        "High_education",
        "Location",
        "Location_US",
        "Assessed_trauma_type",
        "Discrete",
        "Health_First",
        "Trauma_type",
        "Military",
        "Occupational_trauma",
        "Trauma_exposure",
        "Scale_moderator",
        "Diagnostic_DSM",
        "Trajectory_analysis",
        "TP_assessments",
        "N_trajectories",
        "Trauma_TP1",
        "TP1_TPX",
        "Trauma_TPX",
        "Entropy",
        "Low",
        "Decreasing",
        "Increasing",
        "High",
        "Moderate",
        "Relapsing",
        "Worsened_improving",
        "Low_rate",
        "Low_percentage",
        "Decreasing_rate",
        "Decreasing_percentage",
        "Increasing_rate",
        "Increasing_percentage",
        "High_rate",
        "High_percentage",
        "Moderate_rate",
        "Moderate_percentage",
        "Relapsing_rate",
        "Merging",
        "Relabeling",
        "Worsened_improved_rate",
        "Worsened_improved_percentage",
    ]
]

# 7. Remove 'NR' from some columns (np.nan is NR in R analysis)
merged_df['Mean_age'] = merged_df['Mean_age'].apply(
    lambda x: np.nan if isinstance(x, str) and 'NR' in x.upper() else x
)

merged_df['Entropy'] = merged_df['Entropy'].apply(
    lambda x: np.nan if isinstance(x, str) and 'NR' in x.upper() else x
)

merged_df['High_education'] = merged_df['High_education'].apply(
    lambda x: np.nan if isinstance(x, str) and 'NR' in x.upper() else x
)

merged_df['Percentage_partner'] = merged_df['Percentage_partner'].apply(
    lambda x: np.nan if isinstance(x, str) and 'NR' in x.upper() else x
)

merged_df['Percentage_minority'] = merged_df['Percentage_minority'].apply(
    lambda x: np.nan if isinstance(x, str) and 'NR' in x.upper() else x
)

merged_df['Percentage_women'] = merged_df['Percentage_women'].apply(
    lambda x: np.nan if isinstance(x, str) and 'NR' in x.upper() else x
)

# 8. Convert numerical columns to the correct datatype (int or float)
merged_df["Mean_age"] = merged_df["Mean_age"].astype("float")
merged_df["Percentage_women"] = merged_df["Percentage_women"].astype("float")
merged_df["Percentage_minority"] = merged_df["Percentage_minority"].astype("float")
merged_df["Percentage_partner"] = merged_df["Percentage_partner"].astype("float")
merged_df["High_education"] = merged_df["High_education"].astype("float")
merged_df["Trauma_TP1"] = merged_df["Trauma_TP1"].astype("float")
merged_df["TP1_TPX"] = merged_df["TP1_TPX"].astype("float")
merged_df["Trauma_TPX"] = merged_df["Trauma_TPX"].astype("float")
merged_df["Entropy"] = merged_df["Entropy"].astype("float")
merged_df["Mean_age"] = merged_df["Mean_age"].astype("float")
merged_df["Low_rate"] = merged_df["Low_rate"].astype("float")
merged_df["Low_percentage"] = merged_df["Low_percentage"].astype("float")
merged_df["Decreasing_rate"] = merged_df["Decreasing_rate"].astype("float")
merged_df["Decreasing_percentage"] = merged_df["Decreasing_percentage"].astype("float")
merged_df["Increasing_rate"] = merged_df["Increasing_rate"].astype("float")
merged_df["Increasing_percentage"] = merged_df["Increasing_percentage"].astype("float")
merged_df["High_rate"] = merged_df["High_rate"].astype("float")
merged_df["High_percentage"] = merged_df["High_percentage"].astype("float")
merged_df["Moderate_rate"] = merged_df["Moderate_rate"].astype("float")
merged_df["Moderate_percentage"] = merged_df["Moderate_percentage"].astype("float")
merged_df["Relapsing_rate"] = merged_df["Relapsing_rate"].astype("float")
merged_df["Worsened_improved_percentage"] = merged_df["Worsened_improved_percentage"].astype("float")

merged_df["Sample_name)"] = merged_df["Sample_name"].round().astype("float")
merged_df["Sample_Size"] = merged_df["Sample_Size"].round().astype("Int64")
merged_df["N_trajectories"] = merged_df["N_trajectories"].round().astype("Int64")
merged_df["Low"] = merged_df["Low"].round().astype("Int64")
merged_df["Decreasing"] = merged_df["Decreasing"].round().astype("Int64")
merged_df["Increasing"] = merged_df["Increasing"].round().astype("Int64")
merged_df["High"] = merged_df["High"].round().astype("Int64")
merged_df["Moderate"] = merged_df["Moderate"].round().astype("Int64")
merged_df["Relapsing"] = merged_df["Relapsing"].round().astype("Int64")
merged_df["Worsened_improving"] = merged_df["Worsened_improving"].round().astype("Int64")
merged_df["Merging"] = merged_df["Merging"].round().astype("Int64")
merged_df["Relabeling"] = merged_df["Relabeling"].round().astype("Int64")
merged_df["Worsened_improved_rate"] = merged_df["Worsened_improved_rate"].round().astype("Int64")
merged_df["TP_assessments"] = merged_df["TP_assessments"].round().astype("Int64")

# 9. Save to file
merged_df.to_csv("./output/data_for_moderation_analyses.csv", index=False, sep=';')
