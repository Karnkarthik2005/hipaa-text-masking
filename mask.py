import time
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import torch
import gc

# ⏱ Start timer
start = time.time()

# 🔍 Load model and tokenizer
model_name = "d4data/biomedical-ner-all"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

# 🧠 Load NER pipeline with entity aggregation
nlp_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

# 📝 Sample large input (you can replace with your own 50K-word text)
text = (
    "Patient John Doe was admitted to Mercy Hospital on 2024-05-01 for diabetes treatment. "
    "He was later transferred to General Ward for further observations. "
    "Nurse Emily noted improvement in the patient’s response to insulin. "
    * 100  # Repeat to simulate long input
)

# ✂️ Chunking function — split text into 250-word blocks
def chunk_text(text, chunk_size=250):
    words = text.split()
    for i in range(0, len(words), chunk_size):
        yield ' '.join(words[i:i + chunk_size])

# 🔁 Process each chunk
final_masked_text = ""
global_offset = 0
all_masked_entities_info = []

for chunk in chunk_text(text):
    results = nlp_pipeline(chunk)
    results_sorted = sorted(results, key=lambda x: x['start'])

    masked_chunk = ""
    last_idx = 0

    for entity in results_sorted:
        start_idx = entity['start']
        end_idx = entity['end']
        original = chunk[start_idx:end_idx]
        entity_type = entity["entity_group"]

        if entity_type == "DISEASE":
            replacement = original
        else:
            replacement = f"[{entity_type}_MASKED]"

        masked_chunk += chunk[last_idx:start_idx] + replacement
        last_idx = end_idx

        if entity_type not in ["DISEASE", "Disease_disorder_MASKED"]:
            all_masked_entities_info.append({
                "Entity Type": entity_type,
                "Original Text": original,
                "Masked As": replacement,
                "Start": global_offset + start_idx,
                "End": global_offset + end_idx
            })

    masked_chunk += chunk[last_idx:]
    final_masked_text += masked_chunk + " "  # Add space between chunks
    global_offset += len(chunk) + 1  # Offset for next chunk

# 🖨️ Results
print("\n🔍 Masked Entity Info (excluding DISEASE):\n")
for i, info in enumerate(all_masked_entities_info, 1):
    print(f"{i}. Entity Type : {info['Entity Type']}")
    print(f"   Original    : '{info['Original Text']}'")
    print(f"   Masked As   : '{info['Masked As']}'")
    print(f"   Position    : Start={info['Start']}, End={info['End']}\n")

print("🔓 Original Paragraph (truncated):\n", text[:500], "...\n")
print("🔒 Masked Paragraph (truncated):\n", final_masked_text[:500], "...\n")

# ⏱ End timer
end = time.time()
print(f"\n⏱ Total Time Taken: {end - start:.2f} seconds")
