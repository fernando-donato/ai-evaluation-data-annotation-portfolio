# Portfolio project notes

## Project 01 — Archived real-model response evaluation

- **Objective:** demonstrate side-by-side judgment of actual model outputs with source-traceable evidence.
- **Source:** LMSYS MT-Bench question and pre-generated answer files. Eight first-turn responses from each of `claude-instant-v1` and `palm-2-chat-bison-001`, paired by `question_id`. The archived generation records are from June 2023.
- **Model identification:** the source names the above API/model IDs, but does not expose a more precise provider-side snapshot. This analysis did not generate new outputs.
- **Method:** score correctness, instruction following, relevance, and clarity (0–2); choose A, B, Tie, or Both unacceptable; explain the decisive observation. The site shows original paraphrases and links to the full archived answers identified by `answer_id`.
- **Files:** `real_model_evaluations.csv`, `real_model_evaluations.json`, `evaluation_rubric.md`.
- **Result in this selected sample:** A 3, B 2, Tie 2, Both unacceptable 1. The selection is not a general model benchmark.
- **Authorship:** analysis and wording were drafted with AI assistance. Fernando's independent review and dated sign-off have not been claimed.

## Project 02 — Multilingual intent annotation

- **Objective:** demonstrate one-label intent classification and simple urgency triage for support messages.
- **Material:** 48 synthetic messages, 30 Brazilian Portuguese and 18 English. All six intent classes have examples in both languages.
- **Method:** use written label definitions and precedence rules; record primary intent and urgency.
- **Files:** `intent_annotations.csv`, `intent_annotations.json`, `annotation_guidelines.md`. The site displays all 48 messages with language and intent filters.
- **Result:** labeled demonstration dataset and boundary examples. No independent agreement score is claimed.

## Reuse and limits

The real-model output text remains at the linked LMSYS source. This portfolio stores short paraphrases, identifiers, and original analysis. No employer or client data is included. The small sample is intended to show evaluation process, not to establish comparative model performance. Before presenting the judgments as his own reviewed work, Fernando should inspect the linked first-turn outputs and revise or confirm all eight decisions.
