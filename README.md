# Fernando Donato — AI Evaluation & Data Annotation Portfolio

[View the published portfolio](https://fernando-ai-evaluation.fernandodr60.chatgpt.site/)

[Guia de publicação no GitHub e Netlify (português)](GUIA_PUBLICACAO_PTBR.md)

Demonstration projects focused on **side-by-side evaluation of archived real-model outputs** and **multilingual text annotation**. The site is written in English and contains annotation examples in Brazilian Portuguese and English.

## Projects

| Project | Evidence | Files |
|---|---|---|
| Response evaluation | 8 MT-Bench first-turn prompts paired across `claude-instant-v1` and `palm-2-chat-bison-001`; answer IDs, links to source outputs, four rubric dimensions, preferences, and rationales | [`dist/data/real_model_evaluations.csv`](dist/data/real_model_evaluations.csv), [`dist/data/evaluation_rubric.md`](dist/data/evaluation_rubric.md) |
| Intent annotation | 48 fictional support messages with primary intent and urgency labels; six classes and written precedence rules. All items are browsable and filterable on the site. | [`dist/data/intent_annotations.csv`](dist/data/intent_annotations.csv), [`dist/data/annotation_guidelines.md`](dist/data/annotation_guidelines.md) |

The first project re-evaluates **archived June 2023 outputs** from two named model IDs published by LMSYS. It did not run the models anew; the site paraphrases the outputs and links to their originals. The second project uses fictional messages. Analysis was drafted with AI assistance. See [project notes](dist/data/project_notes.md) for sources, limitations, and the personal review step before claiming the judgments as independently verified work.

## Site files

- `dist/` contains the ready-to-publish static site. `dist/index.html` is the entry point.
- `build_data.py` regenerates the synthetic annotation CSV and JSON in `dist/data/` with Python 3.
- `build_real_evaluations.py` exports the original analysis of the archived model records as CSV and JSON. The source text remains at the linked LMSYS files.
- `netlify.toml` points Netlify to `dist`; no build command or dependencies are needed.
- `GUIA_PUBLICACAO_PTBR.md` walks through the GitHub upload and Netlify deployment without terminal commands.

To preview locally, run `python3 -m http.server 8000 --directory dist` and open `http://localhost:8000`. The case selector fetches its JSON file, so opening `index.html` directly from disk may not load that interaction.

## Deploy on Netlify

Connect this GitHub repository through **Add new project → Import an existing project**, choose GitHub, and publish. The checked-in `netlify.toml` sets `dist` as the publish directory. Alternatively, drag the **`dist` folder** into Netlify Drop for a one-time manual deploy; Git-linked deployment is better for future edits.
