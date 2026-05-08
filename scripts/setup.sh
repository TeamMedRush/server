echo "Starting setup..."

if [ -z "$(which python3.12)" ]; then
  echo "python3.12 is not installed."
  echo "Please install python3.12 and try again."
  exit 1
fi

echo "Setting up virtual environment..."
python3.12 -m venv .venv
source .venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Set up complete!"

