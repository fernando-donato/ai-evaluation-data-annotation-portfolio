"""Export an AI-assisted evaluation draft of archived MT-Bench model outputs.

The original answer text is not copied into this repository. Answer IDs and
source URLs let readers inspect the first turn in LMSYS's published JSONL.
Summaries and judgments below are original analysis for this portfolio.
"""
from pathlib import Path
import csv
import json

OUT = Path(__file__).parent / "dist" / "data"
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = "https://huggingface.co/spaces/lmsys/mt-bench/blob/main/data/mt_bench"
QUESTION_URL = SOURCE + "/question.jsonl"
CLAUDE_URL = SOURCE + "/model_answer/claude-instant-v1.jsonl"
PALM_URL = SOURCE + "/model_answer/palm-2-chat-bison-001.jsonl"

# Reference judgments address first turns only. A = Claude Instant v1;
# B = PaLM 2 chat-bison-001. No claims of blind annotation or a new run.
cases = [
    (101, "Race position", "After overtaking the runner in second place, identify both runners' positions.", "Second place; the overtaken runner moves to third.",
     "A places the passing runner third and the overtaken runner fourth.", "B places the passing runner second and the overtaken runner third.",
     "HcseswvQjwTDwADkAxbRbR", "4PfAjntWZRhWMNBNcfUxJL", "B", "reasoning_error", "B is preferred: overtaking the runner in second puts the passer in second, which B states correctly. A shifts both runners one position too far back.",
     (0,1,2,1), (2,2,2,2)),
    (102, "Question interpretation", "Answer where the White House is despite distracting descriptions of other colored buildings.", "Washington, DC.",
     "A says it cannot see the described objects and does not answer the location question.", "B identifies Washington, DC and adds architectural context.",
     "MDgdPnLVAfd4RSoGayWBjX", "MsjtufbhP87yPEFpizm9yA", "B", "non_answer", "B is preferred because it gives the requested location. A responds to its lack of visual perception instead of the question being asked.",
     (0,1,0,2), (2,2,2,1)),
    (103, "Plausible explanations", "Suggest why a healthy person might visit a hospital every day.", "A job at the hospital is one valid possibility; other compatible reasons may fit.",
     "A lists work, volunteering, visiting, donation, and research as possibilities while noting uncertainty.", "B lists doctor, nurse, patient treatment, visiting, and volunteering as possibilities.",
     "Nn8RS8QGVkU9UVRhSgkjQF", "KqYUF5f8A9PhkzRHYcjDKz", "A", "context_fit", "A is preferred narrowly: its possibilities consistently explain a healthy person's visits and are presented as uncertain. B includes a treatment explanation that is less aligned with the stated healthy condition. Both are somewhat long.",
     (2,2,2,1), (1,2,2,1)),
    (104, "Shared sibling reasoning", "David has three sisters; each sister has one brother. Determine how many brothers David has.", "Zero: David is the brother referred to by each sister.",
     "A says the information is insufficient and suggests David may have one to three brothers.", "B multiplies three sisters by one brother and concludes David has three brothers.",
     "iPqy8XRYUKqj3wXYUCF8FE", "kj8pnoT58rX2SQH9eymTVG", "Both unacceptable", "shared_reference_error", "Neither answer recognizes that David can be the same brother of all three sisters. The reference answer is zero brothers; A invents ambiguity and B double-counts the shared sibling.",
     (0,1,2,1), (0,1,2,2)),
    (107, "Family relationship", "Given A is B's father and B is C's father, state A's relationship to C.", "Grandfather.",
     "A identifies A as C's grandfather with intermediate steps.", "B identifies A as C's grandfather in one sentence.",
     "ekGn4tGbwh8F7Wzqn8agQn", "fTUUosjrNCTdpiBkT9pyWC", "Tie", "none", "Both answers correctly identify the grandfather relationship. A explains the chain and B is concise; the prompt does not require a particular level of detail.",
     (2,2,2,2), (2,2,2,2)),
    (108, "Odd-one-out", "Choose the item that differs among tyre, steering wheel, car, and engine.", "Car: the other three are its components.",
     "A identifies the whole car as the odd item and explains that the others are parts.", "B chooses steering wheel because it is not an engine component, but does not explain how the other words form one group.",
     "dCyn4izn2ZBGGTcXi4hJiu", "ixfRkw7qWTSFESvJMTfvLo", "A", "classification_error", "A is preferred because it applies the part-versus-whole distinction. B's engine-component test does not separate the list: a tyre is not an engine component either, and a car is the whole vehicle.",
     (2,2,2,2), (0,1,1,1)),
    (109, "Directional reasoning", "At sunrise, a pole's shadow falls to a person's right; identify the shadow's direction and explain.", "West: the morning sun is in the east.",
     "A answers west and links the sunrise in the east to a westward shadow, but adds an unsupported claim about where Suresh faces.", "B answers west but gives only a brief restatement without the requested steps.",
     "LLzaRTi8dDZ5rWJuK9T9Dm", "Zhkf7jm4wyqjsVppmcGNkr", "A", "missing_reasoning", "A is preferred narrowly: it explains the east-sun/west-shadow relationship, while B omits the requested steps. A's extra statement about Suresh's facing direction is not established by the first-turn prompt.",
     (2,2,2,1), (2,1,2,2)),
    (112, "Arithmetic", "A startup spends $8,000 in year one and half as much in year two. Find the total.", "$12,000.",
     "A calculates $4,000 for year two and a $12,000 total, but the final amount has a spacing typo.", "B calculates $4,000 for year two and gives the $12,000 total concisely.",
     "mGE9yJ7mzqRTWSGFxe33yk", "YBnjdM8ufF6wzvA28yajqG", "Tie", "none", "Both compute $8,000 + $4,000 = $12,000. A's final line spaces the digits oddly, though its intermediate sum is clear; B is cleaner. The formatting issue does not change the core result.",
     (2,2,2,1), (2,2,2,2)),
]

rows = []
for (qid, task, summary, reference, a_summary, b_summary, a_id, b_id,
     preferred, error, rationale, score_a, score_b) in cases:
    row = dict(case_id=f"MT-{qid}", question_id=qid, turn=1, category=task,
               prompt_summary=summary, reference_answer=reference,
               candidate_a_model_id="claude-instant-v1", candidate_a_answer_id=a_id,
               candidate_a_summary=a_summary, candidate_b_model_id="palm-2-chat-bison-001",
               candidate_b_answer_id=b_id, candidate_b_summary=b_summary,
               a_correctness=score_a[0], a_instruction=score_a[1],
               a_relevance=score_a[2], a_clarity=score_a[3],
               b_correctness=score_b[0], b_instruction=score_b[1],
               b_relevance=score_b[2], b_clarity=score_b[3],
               preferred=preferred, primary_error=error, rationale=rationale,
               prompt_source_url=QUESTION_URL, candidate_a_source_url=CLAUDE_URL,
               candidate_b_source_url=PALM_URL, source_period="June 2023",
               analysis_provenance="AI-assisted draft; owner review pending")
    rows.append(row)

with (OUT / "real_model_evaluations.csv").open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
(OUT / "real_model_evaluations.json").write_text(
    json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"Exported {len(rows)} real-model evaluation records")
