# Past LinkedIn Posts

Archive of the author's own published LinkedIn posts, kept so drafts can match
the voice that already exists on the profile instead of a generic template.

Source: https://www.linkedin.com/in/yenhaohuang/recent-activity/all/

## Collection Status

Captured 2026-10-04 from the signed-out public profile. LinkedIn only serves a
truncated preview to signed-out readers, so the bodies below stop where the
`…more` cut-off was and the outbound links were stripped by LinkedIn, not by
the capture. Post dates are derived from LinkedIn's relative timestamps and are
approximate.

When the author supplies a full post body, replace the truncated entry with the
complete text and drop its truncation note.

## Post 1 — Custom NPU IP on PYNQ-Z1 (~2026-09, listed as "3w")

Status: truncated preview.

```text
🚀Building a Custom NPU IP with GPT: Running ResNet-18 on PYNQ-Z1

🔗 <link stripped by LinkedIn>

What if you could turn that hardware idea in your head into something running
on a real FPGA? With GPT's help, I brought mine to life: a custom NPU IP which
can sucessfully run ResNet-18 on FPGA borad - PYNQ-Z1.

⚙️ Hardware Layer

Architecture definition → Hardware ABI → RTL implementation → FPGA deployment
and validation

We follow a verification-first approach: Icarus Verilog for RTL simulation, and
AMD/Xilinx Vivado for synthesis, placement and routing, timing analysis, and
bitstream generation.

[truncated at "…more"]
```

## Post 2 — On-device voice AI (~2026-04, listed as "6mo")

Status: body appears complete through the hashtag line.

```text
🚀 From On-Device Text Chat to On-Device Voice AI

🔗 Project Repo: <link stripped by LinkedIn>

Recently, I extended my on-device LLM workflow from text chat to full voice
chat on Apple devices. This project now supports a complete voice pipeline
running locally on iPhone and macOS: ASR → LLM → TTS

In other words, a user can speak to the app, have the speech transcribed
on-device, generate a response with a local LLM, and hear the response.

✨ Updates
• Added voice chat support on edge devices
• Upgraded to state-of-the-art Qwen3.5 models
• Updated the architecture into a clearer end-to-end voice AI pipeline

📱 Current Features
• Text chat with on-device LLM inference
• Voice chat with a full local pipeline: ASR → LLM → TTS
• Support for multiple model families, including Qwen3/3.5, LLaMA, Gemma
• Native deployment on iOS and macOS

🛠️ Tech Stack
• ASR: WhisperKit
• LLM runtime: ExecuTorch
• TTS: TTSKit / AVSpeechSynthesizer fallback

#AI #OnDeviceAI #VoiceAI #ExecuTorch #iOS #macOS #Qwen35
```

## Observed Voice

Rules read off the archive above. They refine the defaults in
`style-guide.md`; where the two disagree, the archive wins.

- Posts are written in English.
- The title line opens with 🚀 and names the artifact plus where it runs, in
  the shape `<what was built>: <what it does / where it runs>`.
- A `🔗` link line sits directly under the title.
- One short paragraph follows the title: a second-person question or a plain
  "Recently, I ..." sentence, then the concrete claim of what now works.
- Section labels are a single emoji plus two or three words: `⚙️ Hardware
  Layer`, `✨ Updates`, `📱 Current Features`, `🛠️ Tech Stack`.
- Bullets use `•`, not `-`, and stay to one line each.
- Pipelines and flows are written with arrows: `ASR → LLM → TTS`,
  `Architecture definition → Hardware ABI → RTL implementation`.
- Named tools are listed exactly and in full, including the vendor when it
  matters: `Icarus Verilog`, `AMD/Xilinx Vivado`, `WhisperKit`, `ExecuTorch`.
- Methodology is stated as a stance in one sentence, for example
  "We follow a verification-first approach: ...".
- Hashtags, when used at all, are a single run at the very end and are
  camel-cased topic tags.
- Voice is first person, "I" for authorship and "we" for method.
