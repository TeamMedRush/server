#!/usr/bin/env bash
set -e

git fetch origin main:main

BRANCH=$(git rev-parse --abbrev-ref HEAD)
COMMIT=$(git rev-parse HEAD)
REPO_URL=$(git config --get remote.origin.url)

IS_PR=${IS_PR:-true}
NUMBER=${NUMBER}
REPO=${REPO}

get_local_version() {
  grep -E '^version\s*=' pyproject.toml | head -1 | sed -E 's/.*"([^"]+)".*/\1/'
}

get_main_branch_version() {
  git show main:pyproject.toml \
    | grep -E '^version\s*=' \
    | head -1 \
    | sed -E 's/.*"([^"]+)".*/\1/'
}

# fetch available labels
AVAILABLE_LABELS=$(gh label list --repo "$REPO" --json name -q '.[].name' | paste -sd "," -)

if [ "$IS_PR" = "true" ]; then
  INPUT_CONTENT=$(git diff main HEAD)
else
  INPUT_CONTENT=$(gh issue view "$NUMBER" --repo "$REPO" --json body -q .body)
fi

CONTENT=$(cat <<EOF
You are a label generator.

Rules:
- Output ONLY a CSV list of labels
- Choose ONLY from the provided labels
- No explanations
- No extra text

Available Labels:
$AVAILABLE_LABELS

Version Information:
- Current Branch Version: $(get_local_version)
- Main Branch Version: $(get_main_branch_version)

Note:
- You can add more than one label if applicable.
- Only apply the `RELEASE` label if the version has changed compared to main.
  - You also need to add `MAJOR`, `MINOR` based on the type of version change.
    - `1.0.0` -> `2.0.0` is a MAJOR change
    - `x.1.0` -> `x.2.0` is also a MAJOR change
    - `x.y.0` -> `x.y.1` is a MINOR change
- Do not apply tags like `FEAT`, `FIX`, etc. if there are more relevant tags available based on the content.
  - For example, if there is a `ENV` label available, and the changes are only related to environment folders like `ci` or `.github` or `dev.sh` or `scripts` or so on, then prefer `ENV` over `FEAT` or `FIX`.

Content:
$INPUT_CONTENT
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

IFS=',' read -ra TAGS <<< "$AI_RESPONSE"

APPLIED_TAGS=()

for TAG in "${TAGS[@]}"; do
  CLEAN_TAG=$(echo "$TAG" | xargs)
  if [ -n "$CLEAN_TAG" ]; then
    APPLIED_TAGS+=("$CLEAN_TAG")
    if [ "$IS_PR" = "true" ]; then
      gh pr edit "$NUMBER" --repo "$REPO" --add-label "$CLEAN_TAG"
    else
      gh issue edit "$NUMBER" --repo "$REPO" --add-label "$CLEAN_TAG"
    fi
  fi
done

TAGS_STR=$(IFS=, ; echo "${APPLIED_TAGS[*]}")

if [ -n "$TAGS_STR" ]; then
  if [ "$IS_PR" = "true" ]; then
    gh pr comment "$NUMBER" --repo "$REPO" --body "🏷️ Labels added: \`$TAGS_STR\` (commit \`$COMMIT\`)"
  else
    gh issue comment "$NUMBER" --repo "$REPO" --body "🏷️ Labels added: \`$TAGS_STR\`"
  fi
fi

echo "✅ Labels applied: $TAGS_STR"

