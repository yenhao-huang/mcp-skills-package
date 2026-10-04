# Archive Rules

How `references/past-posts/` is filled and kept honest. Read this before
fetching the feed or writing a file into it.

## Source

```text
https://www.linkedin.com/in/yenhaohuang/recent-activity/all/
```

Fetch it at the start of every run of this skill, with whatever web-fetch tool
the harness provides. The feed carries the author's own posts, their reshares,
their comments, and posts they reacted to. Only the author's own posts are
archived; skip likes, reactions, comments, and other people's posts.

## What a Signed-Out Fetch Returns

LinkedIn gates this page. A signed-out fetch lands on the sign-in wall and
returns a public profile preview, which means:

- Only the most recent few of the author's own posts appear.
- Bodies are cut at a `…more` marker.
- Outbound links are stripped from the preview.
- Timestamps are relative ("3w", "6mo"), never absolute dates.

Treat all four as expected, not as a failure. Record what came back and mark
what did not.

## File Naming

One file per post:

```text
references/past-posts/<year>_<month>_<day>.md
```

Zero-padded, for example `2026_09_13.md`. Resolve a relative timestamp against
the fetch date and record the result as approximate. If two posts resolve to
the same day, append `_2`, `_3` and so on in feed order, newest first.

## File Contents

Front matter, then a short note, then the post body verbatim in a fenced
`text` block:

```text
---
date: <YYYY-MM-DD>
date_accuracy: exact | approximate
date_source: <how the date was determined>
source: <feed URL>
captured: <YYYY-MM-DD of the fetch>
completeness: complete | truncated
---

# <short title for the post>

<One or two lines on what the capture did and did not get.>

```text
<post body>
```
```

## Rules

- Reproduce the body verbatim, including the author's own typos, spacing, and
  emoji. It is their writing, not copy to be corrected.
- Never reconstruct a truncated body. End it at the cut and mark
  `completeness: truncated`.
- Never invent a link. Write `<link stripped by LinkedIn>` where the preview
  removed one.
- Do not overwrite a `complete` entry with a `truncated` re-capture of the same
  post. Keep the fuller version and update `captured`.
- When the author supplies a full body for a truncated entry, replace the body,
  set `completeness: complete`, and set `date_accuracy: exact` if they also give
  the real date.
- A post already present for a given date is not re-fetched or duplicated.
- After adding entries, check whether `references/voice.md` still describes the
  archive, and update it if the new posts change the pattern.
