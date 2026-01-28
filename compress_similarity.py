import pickle # nosec
import joblib

# Load your original similarity.pkl
with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)  # nosec

# Compress and save
joblib.dump(similarity, "similarity_compressed.pkl", compress=3)

print("Compression complete! similarity_compressed.pkl created.")
