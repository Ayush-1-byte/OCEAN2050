import pandas as pd

occ = pd.read_csv("data/processed/occurrences_with_sst.csv")
print("occurrences_with_sst.csv species counts:")
print(occ["species"].value_counts())

training = pd.read_csv("data/processed/training_data.csv")
print("\ntraining_data.csv species counts:")
print(training["species"].value_counts())