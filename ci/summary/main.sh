#!/usr/bin/env bash
set -e

git fetch origin main:main

BRANCH=$(git rev-parse --abbrev-ref HEAD)
COMMIT=$(git rev-parse HEAD)
REPO_URL=$(git config --get remote.origin.url)

get_local_version() {
  grep -E '^version\s*=' pyproject.toml | head -1 | sed -E 's/.*"([^"]+)".*/\1/'
}

get_main_branch_version() {
  git show main:pyproject.toml \
    | grep -E '^version\s*=' \
    | head -1 \
    | sed -E 's/.*"([^"]+)".*/\1/'
}

echo "REPO URL: $REPO_URL"
echo "BRANCH: $BRANCH"
echo "COMMIT: $COMMIT"
echo "Local Branch Version: $(get_local_version)"
echo "Main Branch Version: $(get_main_branch_version)"

DIFF=$(git diff main HEAD)

TEMPLATE=$(cat .github/PULL_REQUEST_TEMPLATE.md 2>/dev/null || echo "")

CONTENT=$(cat <<EOF
You are a PR summarizer.

Rules:
- Use ONLY the provided template structure
- Do NOT add explanations, headings, or metadata outside the template
- Keep output strictly concise and PR-ready
- No extra text outside the final filled template
- If there is something in [abc] / [pqr] / [xyz] format, then these are options for you to choose from. In the final output, you should only include the chosen option, not the entire list and do not include the brackets.

Version Information:
- Current Branch Version: $(get_local_version)
- Main Branch Version: $(get_main_branch_version)

Template:
$TEMPLATE

Git Diff:
$DIFF
EOF
)

AI_RESPONSE=$(curl -sS "$URL" \
  -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"content\": $(echo "$CONTENT" | jq -Rs .),
    \"repo\": \"$REPO_URL\",
    \"branch\": \"$BRANCH\",
    \"commit\": \"$COMMIT\"
  }" | jq -r '.content')

BODY=$(cat <<EOF
$AI_RESPONSE
EOF
)

gh pr edit "$PR_NUMBER" --repo "$REPO" --body "$BODY"
gh pr comment "$PR_NUMBER" --repo "$REPO" --body "✅ PR summary updated using AI for commit \`$COMMIT\`."

