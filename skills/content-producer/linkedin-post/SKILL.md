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
3. Read `references/style-guide.md` for the default post structure, tone, and
   sample-derived rules.
4. Read `references/past-posts.md` and match the author's published voice. Where
   it conflicts with `references/style-guide.md`, the archive wins.
5. Draft a post in the user's language unless they request another language.
   The archive is written in English; keep English unless asked otherwise.
6. Keep the post skimmable: short paragraphs, section labels, and bullets for
   results or findings.
7. Preserve factual uncertainty. Do not invent metrics, dataset details, links,
   model names, or acknowledgements.
8. If the user provides only rough notes, produce a complete draft and mark any
   missing facts as bracketed placeholders.
9. After the author publishes a post, append its final text to
   `references/past-posts.md` so the archive stays current.

## Default Style

- Start with a direct hook that states the topic and why it matters.
- Include a link near the top when the user provides one.
- Use concrete benchmark numbers, dataset details, and methodology when
  available.
- Prefer practical findings over hype.
- End with a grounded takeaway, CTA, credit, or acknowledgement.
- Avoid excessive hashtags. Add hashtags only when requested or clearly useful.

## References

- Read `references/style-guide.md` when drafting, rewriting, or evaluating a
  LinkedIn post.
- Read `references/past-posts.md` for the author's previously published posts
  and the voice rules read off them.
