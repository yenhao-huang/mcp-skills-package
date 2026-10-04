---
name: linkedin-post
description: >
  Write, rewrite, and polish LinkedIn posts for technical AI, benchmark,
  privacy, data, engineering, research, product, and open-source updates. Use
  when the user asks for a LinkedIn post, LinkedIn announcement, professional
  social post, benchmark summary, launch post, research update, or asks to match
  the provided LinkedIn sample style.
---

# LinkedIn Post

Use this skill to turn technical notes into a clear LinkedIn post with a strong
hook, concise context, concrete results, and practical takeaways.

## Workflow

1. Identify the post goal: announce, benchmark, explain, launch, recruit
   feedback, or summarize findings.
2. Extract the audience, topic, claim, evidence, numbers, methods, links, and
   acknowledgements from the user input.
3. Refresh the archive from the author's LinkedIn activity feed, following
   `references/rules/archive.md`. Do this before drafting, every time the skill
   runs. If the fetch fails or the harness has no web access, say so and draft
   from whatever `references/past-posts/` already holds.
4. Read `references/style-guide.md` for the default post structure, tone, and
   sample-derived rules.
5. Read `references/voice.md` and the entries in `references/past-posts/`, and
   match the author's published voice. Where they conflict with
   `references/style-guide.md`, the archive wins.
6. Draft a post in the user's language unless they request another language.
   The archive is written in English; keep English unless asked otherwise.
7. Keep the post skimmable: short paragraphs, section labels, and bullets for
   results or findings.
8. Preserve factual uncertainty. Do not invent metrics, dataset details, links,
   model names, or acknowledgements.
9. If the user provides only rough notes, produce a complete draft and mark any
   missing facts as bracketed placeholders.
10. After the author publishes a post, add its final text to
    `references/past-posts/` under the same naming and front matter rules, and
    re-derive `references/voice.md` if the new post changes the pattern.

## Default Style

- Start with a direct hook that states the topic and why it matters.
- Include a link near the top when the user provides one.
- Use concrete benchmark numbers, dataset details, and methodology when
  available.
- Prefer practical findings over hype.
- End with a grounded takeaway, CTA, credit, or acknowledgement.
- Avoid excessive hashtags. Add hashtags only when requested or clearly useful.

## References

- Read `references/rules/archive.md` before fetching the activity feed or
  writing anything into `references/past-posts/`.
- Read `references/style-guide.md` when drafting, rewriting, or evaluating a
  LinkedIn post.
- Read `references/voice.md` for the voice rules read off the author's own
  published posts.
- Read `references/past-posts/` for those posts. One file per post, named
  `<year>_<month>_<day>.md`.
