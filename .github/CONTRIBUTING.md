# Contribution Guidelines

## Prerequisites

This ecosystem relies on the following tools and libraries:
- Python 3.14 or higher

## Getting Started

Contributions to the ecosystem are welcome and encouraged! Here's how you can get started:

- Fork the repository
- Clone your forked repository
- Create a new branch
  - `feat/<feature-name>` for new features
  - `fix/<issue-name>` for bug fixes
  - `docs/<topic>` for documentation updates
- Make your changes
- Commit your changes
  - Add a message that explains the commit
  - Preferably, make small and focused commits
  - Make as many commits as you need, as long as sensible
  - Avoid weird messages like "stuff" (it's reserved for [AttAditya](https://github.com/AttAditya) only, since he's the only one maintaining the repository and can understand what "stuff" means since he wrote the code)
- Push your changes to your forked repository
- Open a pull request to the main repository
  - Start with the PR template
  - Provide a clear description of your changes and the problem they solve
  - Reference any related issues (e.g., "Fixes `#<issue-number>`")
  - Be responsive to feedback and make necessary revisions
- Celebrate your contribution to the ecosystem!

## Development Environment

This project uses a source file `dev.sh` to set up the development environment. To get started, follow these steps:

```sh
# Clone the repository
git clone https://github.com/<your-username>/<repository-name>.git
cd <repository-name>

# Source the development environment
source dev.sh

# Setup and run
dev setup
dev run
```

### Available Commands

Use the `dev` command to view and understand the available commands. Here are important commands:

- `dev setup`: Sets up the development environment, including installing dependencies and configuring necessary tools.
- `dev run`: Runs the main application or specific components for testing and development purposes.
- `dev fmt`: Formats the codebase according to the project's coding standards.

