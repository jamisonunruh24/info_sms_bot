import json
import os

# Update this to your actual mounted path
MEMORY_FILE = "E:\\VapeMemory\\Vape_session.json"


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_memory(history):
    try:
        print(f"💾 Writing {len(history)} entries to memory...")
        with open(MEMORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
        print(f"✅ Saved to {MEMORY_FILE}")
    except Exception as e:
        print("❌ Error writing memory:", e)

