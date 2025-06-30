# hipaa-text-masking
 NER-based text anonymization for PHI using Hugging Face and Microsoft presidio
# 🛡️ HIPAA Health Data Masking using Transformers & Presidio

This project provides two AI-powered approaches to anonymize Protected Health Information (PHI) from clinical or medical text using:
Transformers-based NER model d4data/biomedical-ner-all
Microsoft Presidio (rule-based + ML NER)

---

## 🔍 Features

- Detects and masks sensitive information (names, hospitals, dates, IDs)
- Skips masking `DISEASE` to retain clinical meaning
- Handles large documents with 250-word chunking
- Supports Presidio for customizable entity detection and policy control
- Tracks and logs entity types, masked values, and text positions

---

## 🧪 Sample Input

```text
Patient John Doe was admitted to Mercy Hospital on 2024-05-01 for diabetes treatment.
---tranformer output
Patient [PERSON_MASKED] was admitted to [HOSPITAL_MASKED] on [DATE_MASKED] for diabetes treatment.
---presidio output
Patient <PERSON> was admitted to <ORGANIZATION> on <DATE_TIME> for diabetes treatment.
