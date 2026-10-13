import os
import sys
import json
import argparse
from openai import OpenAI

# Change this to any model your account can access:
#   gpt-6-astra     -> newest frontier, highest quality
#   gpt-5.6-sol     -> OpenAI's recommended production model (default below)
#   gpt-5.4-mini    -> cheaper / faster, good enough for this task
#   gpt-5.4-nano    -> cheapest
#   chat-latest     -> stable alias that always points to the latest chat model
DEFAULT_MODEL = "gpt-5.6-sol"
GUIDELINES_FILE = "guidelines.md"


def load_guidelines(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    sys.exit(f"Guidelines file not found: {path}")


def read_pasted_text():
    print("Paste your copy below.")
    print("When you're done, type END on its own line and press Enter:\n")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:   # Ctrl+Z then Enter (Windows) / Ctrl+D (Mac/Linux)
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def extract_json(text):
    """Pull the JSON object out of the reply, tolerating stray text/fences."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```", 2)[1]
        if text.lstrip().startswith("json"):
            text = text.lstrip()[4:]
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON found in model response.")
    return json.loads(text[start:end + 1])


def lint(copy_text, guidelines, model):
    client = OpenAI()   # reads OPENAI_API_KEY from environment
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": guidelines},
            {"role": "user", "content": f"Copy to review:\n\n{copy_text}"},
        ],
        response_format={"type": "json_object"},   # forces valid JSON back
    )
    return extract_json(resp.choices[0].message.content)


def print_report(result):
    issues = result.get("issues", [])
    order = {"high": 0, "medium": 1, "low": 2}
    issues.sort(key=lambda i: order.get(i.get("severity", "low"), 3))

    print("\n" + "=" * 60)
    print("BRAND VOICE LINT REPORT")
    print("=" * 60)

    if not issues:
        print("\nNo issues found.")
    else:
        counts = {}
        for i in issues:
            s = i.get("severity", "low")
            counts[s] = counts.get(s, 0) + 1
        summary = ", ".join(f"{v} {k}" for k, v in counts.items())
        print(f"\n{len(issues)} issue(s) found  ({summary})\n")

        for n, issue in enumerate(issues, 1):
            sev = issue.get("severity", "low").upper()
            cat = issue.get("category", "").upper()
            print(f"[{sev} / {cat}]  Issue {n}")
            print(f'   Text : "{issue.get("snippet", "")}"')
            print(f'   Rule : {issue.get("rule", "")}')
            print(f'   Fix  : {issue.get("suggestion", "")}\n')

    print("-" * 60)
    print(f"Verdict: {result.get('verdict', 'n/a')}")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Simplilearn brand voice linter")
    parser.add_argument("--file", help="Path to a .txt file of copy (instead of pasting)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model to use")
    parser.add_argument("--guidelines", default=GUIDELINES_FILE, help="Path to guidelines file")
    args = parser.parse_args()

    guidelines = load_guidelines(args.guidelines)

    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            copy_text = f.read().strip()
    else:
        copy_text = read_pasted_text()

    if not copy_text:
        sys.exit("No copy provided.")

    try:
        result = lint(copy_text, guidelines, args.model)
    except Exception as e:
        sys.exit(f"Error: {e}")

    print_report(result)


if __name__ == "__main__":
    main()