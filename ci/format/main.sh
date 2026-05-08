#!/usr/bin/env bash
set -e

echo "Upgrading pip..."
python3 -m pip install --upgrade pip

echo "Installing cutypy globally..."
pip install cutypy

echo "Running dev setup..."
source dev.sh

echo "Formatting..."
dev fmt

echo "Committing changes..."
git config user.name "GitHub Actions"
git config user.email "github-actions@github.com"

git add .
git commit -m "chore: auto format" || echo "No changes to commit"

echo "Pushing changes..."
git push

