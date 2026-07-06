# LinkedIn Post Style Guide

## Target Style

The default style is a professional technical LinkedIn post for AI, privacy,
benchmarking, engineering, and research updates.

Use this shape:

1. Hook with an emoji or strong title line.
2. Link line if provided.
3. Problem context in 1-3 short paragraphs.
4. What was evaluated or built.
5. Results section with concrete numbers.
6. Key findings section with bullets.
7. Methodology section when the post involves evaluation.
8. Practical takeaway or recommendation.
9. Credit or acknowledgement when relevant.

## Tone

- Clear, credible, and technical.
- Direct rather than promotional.
- Evidence-first: claims should be supported by metrics, setup, or examples.
- Suitable for AI engineers, ML practitioners, technical founders, and data
  privacy/security readers.
- Use emoji sparingly for section labels, not decoration.

## Formatting

- Keep paragraphs short.
- Use section labels such as:
  - `📊 Overall Results`
  - `🔍 Key Findings`
  - `📐 Evaluation Methodology`
  - `🧩 What We Built`
  - `⚙️ How It Works`
  - `🚀 Why It Matters`
- Use bullet points for findings and method details.
- Use model/tool names exactly as provided.
- Keep numbers and labels close together.
- Put a link near the top if the user provides one.

## Benchmark Post Pattern

```text
🧠 <Title: what was benchmarked and why>
🔗 <link>

<Why the problem matters now.>

<What was benchmarked, on what dataset/task, and for what purpose.>

📊 Overall Results

<System A>
• <Metric>: <value>

<System B>
• <Metric>: <value>

🔍 Key Findings
• <Finding 1 grounded in a number or observation.>
• <Finding 2 with comparison.>
• <Finding 3 with limitation or surprise.>

📐 Evaluation Methodology
• Dataset: <dataset details>
• Metric: <metric details>
• Inference/setup: <runtime or system details>
• Baseline/customization: <baseline details>

<Practical takeaway.>

<Acknowledgement or credit if relevant.>
```

## Sample-Derived Rules

The user's sample post follows these rules:

- Title line combines topic, tools/models, and "benchmarked".
- The first paragraph frames a business/engineering risk.
- The second paragraph explains why the evaluation matters.
- Results are separated from interpretation.
- Findings include both strengths and weaknesses.
- Methodology is concise but reproducible enough to understand the benchmark.
- Final sentence gives a practical recommendation.
- Acknowledgement credits dataset creators or relevant upstream work.

## Do Not

- Do not invent benchmark results, dataset size, categories, or links.
- Do not overstate a result as production-ready if the evidence is only a
  benchmark.
- Do not add many hashtags by default.
- Do not bury the main result below long background.
- Do not turn the post into an academic abstract; keep it readable on LinkedIn.

## Optional Ending Patterns

Use one of these when appropriate:

```text
If you are evaluating <use case>, <tool/model> is worth testing in your own
environment.
```

```text
The main takeaway: <concise practical conclusion>.
```

```text
Thanks to <creator/project> for making <dataset/tool> publicly available.
```
