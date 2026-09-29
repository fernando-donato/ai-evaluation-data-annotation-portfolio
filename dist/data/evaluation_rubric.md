# Archived model response evaluation — rubric and method

## Scope

Eight **first-turn** MT-Bench prompts are paired with their archived responses from `claude-instant-v1` (candidate A) and `palm-2-chat-bison-001` (candidate B). Both model answers for each `question_id` were generated for the same benchmark prompt and published by LMSYS. This project re-evaluates existing June 2023 outputs; it did not run either model anew. The identifiers are those recorded in the source files. A more precise internal model snapshot or provider-side build number is not available in those records.

The site and CSV present original **paraphrases** of the outputs, not copied full response text. Follow each answer file link and search for the recorded `answer_id` to inspect the actual first-turn text before accepting any judgment. The prompt file uses the same `question_id`.

Sources: [MT-Bench questions](https://huggingface.co/spaces/lmsys/mt-bench/blob/main/data/mt_bench/question.jsonl), [Claude Instant v1 answers](https://huggingface.co/spaces/lmsys/mt-bench/blob/main/data/mt_bench/model_answer/claude-instant-v1.jsonl), [PaLM 2 chat-bison-001 answers](https://huggingface.co/spaces/lmsys/mt-bench/blob/main/data/mt_bench/model_answer/palm-2-chat-bison-001.jsonl). See the [FastChat evaluation documentation](https://github.com/lm-sys/FastChat/blob/main/fastchat/llm_judge/README.md) for the original benchmark and pre-generated answers.

## Scoring

Each first-turn response is scored independently from **0** (fails), **1** (partially satisfies), or **2** (satisfies) on four dimensions:

| Dimension | Review question |
|---|---|
| Correctness | Is the core answer consistent with the benchmark question and reference, or otherwise defensible? |
| Instruction following | Did it provide the requested form or reasoning, when specified? |
| Relevance | Does it address the user's actual question? |
| Clarity | Is the explanation understandable without needless confusion? |

The pairwise label is `A`, `B`, `Tie`, or `Both unacceptable`. A correct core answer normally outweighs polish. `Both unacceptable` means neither candidate supplies an acceptable core answer. Short rationales identify the decisive difference. The reference answer is recorded as a short restatement for checking, not copied from the benchmark.

## Selection and limits

The eight cases were purposively selected from reasoning and basic arithmetic questions because their outputs and reference answers can be inspected in a small portfolio. They are **not a random sample**, a leaderboard, or evidence of overall performance. Candidate identities were visible during this AI-assisted draft analysis; no blind review, independent second rater, or measured agreement is claimed. Fernando should read the original outputs and review each decision before presenting the judgments as his personally completed evaluation.

The output files contain answer IDs, source URLs, per-dimension scores, preferences, and rationales. The model answer files also contain second-turn replies, but **only first turns are scored here**. Results: A preferred in 3 cases, B in 2, Tie in 2, and Both unacceptable in 1. These counts describe this selected sample only.
