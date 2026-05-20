
# ── PHASE 1: Setup & Data Loading ───────────────────────────

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 5)

# Load the dataset 
df = pd.read_csv("netflix_titles.csv")


print("Shape:", df.shape)
print("\nFirst 5 rows:")
df.head()


# ── PHASE 2: Data Cleaning ───────────────────────────────────

# Check for missing values
print("\nMissing values:")
print(df.isnull().sum())

# Fill missing values in common columns
df["director"].fillna("Unknown", inplace=True)
df["cast"].fillna("Unknown", inplace=True)
df["country"].fillna("Unknown", inplace=True)
df["rating"].fillna("Not Rated", inplace=True)

# Convert 'date_added' to datetime
df["date_added"] = pd.to_datetime(df["date_added"].str.strip(), errors="coerce")

# Extract year and month from date_added
df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month

# Split genres (listed_in) into a list
df["genres"] = df["listed_in"].str.split(", ")

print("\nCleaned! Sample date_added:", df["date_added"].iloc[0])


# ── PHASE 3 & 4: Exploration & Visualizations ────────────────

# --- Chart 1: Movies vs TV Shows ---
type_counts = df["type"].value_counts()

plt.figure()
plt.pie(
    type_counts,
    labels=type_counts.index,
    autopct="%1.1f%%",
    colors=["#E50914", "#221F1F"],
    startangle=90,
    textprops={"color": "white"},
)
plt.title("Movies vs TV Shows on Netflix", fontsize=14)
plt.tight_layout()
plt.savefig("chart1_type_split.png", dpi=150)
plt.show()


# --- Chart 2: Content Added Per Year ---
yearly = df.groupby("year_added")["show_id"].count().dropna()

plt.figure()
yearly.plot(kind="bar", color="#E50914", edgecolor="none")
plt.title("Content Added to Netflix Per Year", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart2_content_per_year.png", dpi=150)
plt.show()


# --- Chart 3: Top 10 Countries ---
top_countries = (
    df[df["country"] != "Unknown"]["country"]
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)

plt.figure()
sns.barplot(x=top_countries.values, y=top_countries.index, palette="Reds_r")
plt.title("Top 10 Countries by Number of Titles", fontsize=14)
plt.xlabel("Number of Titles")
plt.ylabel("")
plt.tight_layout()
plt.savefig("chart3_top_countries.png", dpi=150)
plt.show()


# --- Chart 4: Top 10 Genres ---
top_genres = (
    df["genres"]
    .explode()
    .value_counts()
    .head(10)
)

plt.figure()
sns.barplot(x=top_genres.values, y=top_genres.index, palette="Blues_r")
plt.title("Top 10 Genres on Netflix", fontsize=14)
plt.xlabel("Number of Titles")
plt.ylabel("")
plt.tight_layout()
plt.savefig("chart4_top_genres.png", dpi=150)
plt.show()


# --- Chart 5: Movies vs TV Shows Over Time ---
type_year = df.groupby(["year_added", "type"]).size().unstack().dropna()

plt.figure()
type_year.plot(kind="line", marker="o", color=["#E50914", "#564d4d"])
plt.title("Movies vs TV Shows Added Over Time", fontsize=14)
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.legend(title="Type")
plt.tight_layout()
plt.savefig("chart5_type_over_time.png", dpi=150)
plt.show()


# ── BONUS: Quick Summary Stats ───────────────────────────────

print("\n===== QUICK INSIGHTS =====")
print(f"Total titles: {len(df)}")
print(f"Date range: {df['year_added'].min():.0f} – {df['year_added'].max():.0f}")
print(f"Top country: {top_countries.index[0]} ({top_countries.iloc[0]} titles)")
print(f"Top genre: {top_genres.index[0]} ({top_genres.iloc[0]} titles)")
print(f"Most common rating: {df['rating'].value_counts().index[0]}")
print("Charts saved as PNG files in the current folder.")
