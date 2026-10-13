# Brand Voice Linter

An AI-powered tool that checks marketing copy against a brand's voice and compliance rules — before a human reviewer ever sees it. Paste in an ad, email, or landing-page draft and get back a report flagging off-brand tone, risky claims, and deliverability problems, each with a suggested fix.

Think of it as a spell-checker for brand voice: it catches the obvious, repetitive issues automatically so the human editor can focus on the judgment calls a machine can't make.

## Why this exists

Any team producing high volumes of marketing copy — across performance ads, CRM emails, and landing pages — needs a consistent brand voice and a guard against over-promising. Doing that review manually on every draft is slow and error-prone. This linter acts as an automated first-pass "quality gate," enforcing a written rulebook so only clean, on-brand copy reaches final review.

The rulebook in this repo was derived from analysing a real corpus of ~1,300 marketing emails to capture the brand's actual voice patterns, then layered with compliance guardrails (for example, flagging "guaranteed job" style claims that over-promise outcomes).

## What it flags

- **Compliance risks (high severity)** — absolute outcome assurances and guarantee language ("guaranteed job", "assured placement", unprovable promises).
- **Deliverability / quality risks (medium severity)** — emoji stuffing, ALL-CAPS, spam-trigger phrasing, vague claims with no proof.
- **Voice & mechanics** — off-brand tone, passive voice, British vs US spelling, weak CTAs, wrong terminology.

Each issue comes back with the exact snippet, a severity level, the rule it breaks, and a suggested fix.

## How it works

All the brand logic lives in `guidelines.md` as plain English — no code. The script sends your copy plus that rulebook to an LLM, which returns structured JSON that the script formats into a readable report. Because the rules are separate from the code, a non-developer can read and tune them without touching Python.

## Project structure

```
.
├── brand_voice_linter.py   # the script
├── guidelines.md           # the editable brand rulebook
└── README.md
```

## Requirements

- Python 3.8+
- An OpenAI API key

## Setup

```bash
git clone https://github.com/your-username/brand-voice-linter.git
cd brand-voice-linter
pip install openai
```

Set your API key as an environment variable.

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "your-key-here"
```

**macOS / Linux:**
```bash
export OPENAI_API_KEY="your-key-here"
```

## Usage

**Paste mode** — run it, paste your copy, then type `END` on its own line:

```bash
python brand_voice_linter.py
```

**File mode** — check a draft saved in a text file:

```bash
python brand_voice_linter.py --file mycopy.txt
```

**Choose a model** — override the default for a run:

```bash
python brand_voice_linter.py --model gpt-5.4-mini
```

## Example output

```
============================================================
BRAND VOICE LINT REPORT
============================================================

2 issue(s) found  (1 high, 1 medium)

[HIGH / COMPLIANCE]  Issue 1
   Text : "Enroll now and get a 100% guaranteed job"
   Rule : Outcome assurance / guarantee language
   Fix  : Replace with provable proof, e.g. "join learners now working at top firms"

[MEDIUM / DELIVERABILITY]  Issue 2
   Text : "FREE COURSE — ACT NOW!!!"
   Rule : Spam-trigger phrasing / ALL-CAPS
   Fix  : "Start your free course today"

------------------------------------------------------------
Verdict: Mostly on-brand, but revise the guarantee claim before publishing.
============================================================
```

## Configuration

Edit `guidelines.md` to change what the linter enforces — add rules, adjust severities, or swap in a different brand's voice entirely. To change the default model, edit `DEFAULT_MODEL` near the top of `brand_voice_linter.py`.

## Security

Never commit your API key. Keep it in an environment variable, as above. If you add test files or generated reports, consider a `.gitignore`:

```gitignore
.env
*.txt
```

## License

MIT