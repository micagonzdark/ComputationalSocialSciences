# ===== DSA Content Moderation Base Notebook =====

# Author: BELLAIS, Salomé; GONZALEZ DARDIK, Micaela; VEILLARD, Mathilde.

# Date: 2025-11-25

# ============================================================
# 1. Import libraries
# ============================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

# ============================================================
# 2. Load dataset
# ============================================================
data = pd.read_csv("sample-strat-april-10k.csv", on_bad_lines="skip", low_memory=False)

print("First 5 rows:")
display(data.head())

print("\nData info:")
print(data.info())

print("\nSummary statistics:")
display(data.describe(include='all'))

# === ANALYSIS: Dataset overview ===
# The dataset consists of 10,000 observations per platform.
# This stratified sampling ensures balance and prevents the graphs from comparing
# raw quantities that do not reflect real activity.

# ============================================================
# 3. Basic variable exploration
# ============================================================
print("\nModeration actions per platform:")
display(data['platform_name'].value_counts())

if 'moderation_type' in data.columns:
    print("\nModeration type counts:")
    display(data['moderation_type'].value_counts())

# === CONCLUSION ===
# Because the dataset is stratified, all platforms exhibit exactly 10,000 cases.
# This allows for unbiased comparison of proportions and eliminates differences arising from the actual size of each platform outside the dataset.

# ============================================================
# 4. Grouped analysis (example)
# ============================================================
if 'platform_name' in data.columns and 'automated_decision' in data.columns:
    print("\nAutomated decision per platform:")
    display(
        data.groupby('platform_name')['automated_decision'].value_counts()
    )

# === CONCLUSION ===
# Although the quantities per platform are identical, differences are already observed in
# how each company distributes its decisions between Manual / Semi-auto / Full-auto.
# This idea is explored further in the proportional visualizations below.

# ============================================================
# 5. Basic visualizations
# ============================================================

plt.figure(figsize=(8,5))
sns.countplot(
    data=data,
    x='platform_name',
    order=data['platform_name'].value_counts().index
)
plt.title("Moderation Actions per Platform (stratified)")
plt.xticks(rotation=45)
plt.show()

# ==============================================================
# Intermediate Conclusion:
# ============================================================
# This graph only confirms the stratification: all are equal.
# Relevant analyses should be proportional, not absolute.

# ============================================================
# 6. Automation Analysis (raw counts)
# ============================================================
df = data[["platform_name", "automated_decision"]]

counts = df.groupby(["platform_name", "automated_decision"]).size().unstack(fill_value=0)
print(counts)

counts.plot(kind="bar", figsize=(12,6))
plt.title("Automated Decisions per Platform")
plt.xlabel("Platform")
plt.ylabel("Number of Decisions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# === CONCLUSION ===
# Even with the same number of users per platform, some services show significantly more fully automated decisions
# while others rely on manual decisions.

# ============================================================
# 7. Moderator Profiles (Improved & Readable)
# ============================================================

moderator_cols = ["source_type", "automated_detection", "automated_decision", "platform_name"]
mod = data[moderator_cols].copy()

# ===== Clean labels ===== #
source_map = {
    "SOURCE_VOLUNTARY": "Voluntary",
    "SOURCE_TYPE_OTHER_NOTIFICATION": "User Report",
    "SOURCE_ARTICLE_16": "Gov. Notice",
    "SOURCE_TRUSTED_FLAGGER": "Trusted Flagger"
}

mod["source"] = mod["source_type"].map(source_map).fillna("Other")

detect_map = {"Yes": "Auto-detect", "No": "Human-detect"}
mod["detect"] = mod["automated_detection"].map(detect_map)

decision_map = {
    "AUTOMATED_DECISION_NOT_AUTOMATED": "Not auto decision",
    "AUTOMATED_DECISION_PARTIALLY": "Semi-automated decision",
    "AUTOMATED_DECISION_FULLY": "Automated decision "
}
mod["decision"] = mod["automated_decision"].map(decision_map)

mod["profile"] = mod["source"] + " | " + mod["detect"] + " | " + mod["decision"]

print("\n=== Source type ===")
display(mod["source"].value_counts())

print("\n=== Detection type ===")
display(mod["detect"].value_counts())

print("\n=== Decision type ===")
display(mod["decision"].value_counts())

print("\n=== Moderator profiles (clean) ===")
display(mod["profile"].value_counts())

plt.figure(figsize=(12,6))
mod["profile"].value_counts().head(10).plot(kind="bar")
plt.title("Top Moderator Profiles")
plt.xlabel("Profile")
plt.ylabel("Number of Decisions")
plt.xticks(rotation=60)
plt.tight_layout()
plt.show()

# === CONCLUSION ===
# The two dominant factors are:

# - Voluntary reports: the vast majority of inputs come from users.
# - Auto-detect YES combines strongly with Semi-auto and Fully-auto.

# This indicates hybrid pipelines where detection is usually automated
# but the final decision is not always.

# ============================================================
# 8. Moderator Profiles by Platform (Top 6)
# ============================================================

top_profiles = mod["profile"].value_counts().head(6).index

profile_by_platform = (
    mod[mod["profile"].isin(top_profiles)]
    .groupby(["platform_name", "profile"])
    .size()
    .unstack(fill_value=0)
)

profile_by_platform.plot(kind="bar", figsize=(14,6))

plt.title("Moderator Profiles by Platform (Top 6)")
plt.xlabel("Platform")
plt.ylabel("Number of Decisions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# === CONCLUSION ===
# Some platforms rely more on the following cycle:
# Voluntary → Auto-detect → Semi-auto
# while others prioritize:
# Voluntary → Human-detect → Manual
# These differences demonstrate distinct moderation strategies:
# some based on partial automation, others on human intervention.

# ============================================================
# 9. Proportional Analyses (core of the project)
# ============================================================



# Ratio: Automatic DETECTION by platform
detect_rate = (
    mod.groupby("platform_name")["automated_detection"]
       .value_counts(normalize=True)
       .rename("proportion")
       .reset_index()
)

detect_rate_pivot = detect_rate.pivot(index='platform_name', 
                                      columns='automated_detection', 
                                      values='proportion').fillna(0)

plt.figure(figsize=(10,6))
plt.bar(detect_rate_pivot.index, detect_rate_pivot["No"], label="No")
plt.bar(detect_rate_pivot.index, detect_rate_pivot["Yes"], bottom=detect_rate_pivot["No"], label="Yes")
plt.title("Automated detection")
plt.xticks(rotation=45)
plt.ylabel("Ratio")
plt.legend()
plt.tight_layout()
plt.show()


# ==========================================================
# Proportion: type of automated decision by platform
# ==========================================================

decision_rate = (
    mod.groupby("platform_name")["automated_decision"]
       .value_counts(normalize=True)
       .rename("proportion")
       .reset_index()
)

# pivot para alinear categorías y evitar shape mismatch
decision_rate_pivot = decision_rate.pivot(index='platform_name',
                                         columns='automated_decision',
                                         values='proportion').fillna(0)

categories = [
    "AUTOMATED_DECISION_NOT_AUTOMATED",
    "AUTOMATED_DECISION_PARTIALLY",
    "AUTOMATED_DECISION_FULLY"
]

plt.figure(figsize=(10,6))
bottom = np.zeros(len(decision_rate_pivot))
for cat in categories:
    plt.bar(decision_rate_pivot.index, decision_rate_pivot[cat], bottom=bottom, label=cat)
    bottom += decision_rate_pivot[cat].values

plt.title("Proporción de tipo de decisión automática por plataforma")
plt.xticks(rotation=45)
plt.ylabel("Proporción")
plt.legend()
plt.tight_layout()
plt.show()


# Heatmap platform × source_type
source_rate = (
    mod.groupby(["platform_name", "source_type"])
       .size()
       .groupby(level=0)
       .apply(lambda x: x/x.sum())
       .unstack(fill_value=0)
)

plt.figure(figsize=(10,6))
plt.imshow(source_rate, aspect='auto', cmap="Blues")
plt.xticks(range(len(source_rate.columns)), source_rate.columns, rotation=45)
plt.yticks(range(len(source_rate.index)), source_rate.index)
plt.colorbar(label="Ratio")
plt.title("Distribution ratio of SOURCE TYPE")
plt.tight_layout()
plt.show()


# === CONCLUSION ===
# - Voluntary reports dominate across all platforms, but some accept more Government Notices or User Reports.
# - Platforms with more Auto-detect tend to also have more Fully-auto decision-making → automated pipeline.
# - Those with less Auto-detect rely more on Manual decision-making → human-controlled pipeline.

# ============================================================
# 10. FINAL CONCLUSIONS OF THE SESSION
# ============================================================

print("\n==================== CONCLUSIONS ====================\n")

detect_yes = detect_rate[detect_rate["automated_detection"]=="Yes"]
top_detect = detect_yes.sort_values("proportion", ascending=False).iloc[0]

print(f"- Platform with greater automatic detection: "
      f"{top_detect['platform_name']} ({top_detect['proportion']:.2%}).")

auto_full = decision_rate[
    decision_rate["automated_decision"]=="AUTOMATED_DECISION_FULLY"
]
top_full = auto_full.sort_values("proportion", ascending=False).iloc[0]

print(f"- Platform with the highest proportion of fully automated decisions: "
      f"{top_full['platform_name']} ({top_full['proportion']:.2%}).")

not_auto = decision_rate[
    decision_rate["automated_decision"]=="AUTOMATED_DECISION_NOT_AUTOMATED"
]
top_human = not_auto.sort_values("proportion", ascending=False).iloc[0]

print(f"- Platform with the highest proportion of fully manual decisions: "
      f"{top_human['platform_name']} ({top_human['proportion']:.2%}).")

dominant_sources = source_rate.idxmax(axis=1)

print("\n- Dominant report type by platform:")
for platform, src in dominant_sources.items():
    print(f"   • {platform}: {src}")

print("\n======================================================\n")
