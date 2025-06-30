from presidio_analyzer import AnalyzerEngine
from tabulate import tabulate
from presidio_anonymizer import AnonymizerEngine
import time

start = time.time()

# Initialize Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Your text input
text = """
Patient Ramesh Kumar has PAN number AZZPK7190K and phone 9876543210.
His email is ramesh.kumar@example.com and DOB is 1985-02-10.
"""

# Start timing PDF/text load
mid = time.time()

# Analyze all entities
results = analyzer.analyze(text=text, language='en')

# ❌ Filter out the 'IN_PAN' entity from being masked
filtered_results = [r for r in results if r.entity_type != 'IN_PAN']

masked_result = anonymizer.anonymize(text=text, analyzer_results=filtered_results)


print("\nMasked Output:\n", masked_result.text)

print("\nDetected Entities:")


# Prepare data
table_data = []
for i, entity in enumerate(results):
    row = [
        i + 1,
        entity.entity_type,
        text[entity.start:entity.end],
        entity.start,
        entity.end
    ]
    table_data.append(row)

# Print as table
headers = ["#", "Entity Type", "Text", "Start", "End"]
print("\n📋 Detected Entities:\n")
print(tabulate(table_data, headers=headers, tablefmt="grid"))


# Time taken
end = time.time()
print("\n Time Report:")
print("🔹 Load document            :", mid - start, " sec")
print("🔹 Process & mask document  :", end - mid, " sec")
print("🔹 Total time               :", end - start, " sec")
