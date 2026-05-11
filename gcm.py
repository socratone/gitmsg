#!/usr/bin/env python3
import os
import subprocess
import sys

from openai import OpenAI


def get_staged_diff():
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error running git diff: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def generate_commit_message(diff: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a git commit message generator. "
                    "Analyze the provided git diff and write a concise commit message in Korean. "
                    "Rules:\n"
                    "1. Use conventional commits format: feat, fix, refactor, docs, style, test, chore, etc.\n"
                    "2. If the diff touches files under multiple top-level directories (monorepo), "
                    "   detect the app/package name from the path (e.g. apps/web/... → web, packages/ui/... → ui) "
                    "   and add it as a scope: feat(web): ...\n"
                    "3. If all changes are within a single app/package, add that scope too.\n"
                    "4. If it's a single-root repo (no clear sub-app structure), omit the scope.\n"
                    "5. The description after the colon must be written in Korean.\n"
                    "6. Keep it under 72 characters total.\n"
                    "Output ONLY the commit message — no explanations, no backticks, no extra text."
                ),
            },
            {
                "role": "user",
                "content": f"Generate a commit message for this diff:\n\n{diff}",
            },
        ],
        max_tokens=200,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


def main():
    diff = get_staged_diff()

    if not diff:
        print("No staged changes. Run 'git add' first.", file=sys.stderr)
        sys.exit(1)

    message = generate_commit_message(diff)
    print(message)


if __name__ == "__main__":
    main()
