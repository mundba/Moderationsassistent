import pandas as pd

df = pd.read_excel("rp-classified.xlsx")

selected_df = df[["content","llm", "person"]]
selected_df["person"] = selected_df["person"].str.replace(", ", " ").str.replace(",", " ").str.split().str.join(", ").str.strip()
selected_df["llm"] = selected_df["llm"].str.lower().str.strip()
selected_df["person"] = selected_df["person"].str.lower().str.strip()

def count_common_words(row):
   llm_words = set(row["llm"].split(", "))
   person_words = set(row["person"].split(", "))
   common_words = llm_words.intersection(person_words)
   return len(common_words)

def count_total_words(row):
   llm_words = set(row["llm"].split(", "))
   person_words = set(row["person"].split(", "))
   return len(llm_words), len(person_words)

selected_df["common_words"] = selected_df.apply(count_common_words, axis=1)
total_common = selected_df["common_words"].sum()

total_llm = 0
total_person = 0
for _, row in selected_df.iterrows():
   llm_count, person_count = count_total_words(row)
   total_llm += llm_count
   total_person += person_count

average_percent = (2 * total_common / (total_llm + total_person)) * 100

print(f"Gesamtanzahl Wörter LLM: {total_llm}")
print(f"Gesamtanzahl Wörter Person: {total_person}")
print(f"Gesamtanzahl gemeinsamer Wörter: {total_common}")
print(f"Prozentuale Übereinstimmung: {average_percent:.2f}%")
import time
selected_df.to_excel(f"results/{time.strftime('%H-%M-%S')}_common_words.xlsx", index=False)