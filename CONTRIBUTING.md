# Contributing to Computational Social Sciences

Thank you for your interest in contributing to this project! This guide will help you understand how to contribute effectively.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors. We expect:

- Consideration for diverse perspectives and experiences
- Focus on collaborative learning and knowledge sharing

## Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.12
- Git

### Setting Up Your Development Environment

1. **Clone the repo locally:**
   ```bash
   git clone https://github.com/micagonzdark/ComputationalSocialSciences.git
   cd ComputationalSocialSciences
   ```

2. **Create your own branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Do changes and commit:**
   Make your changes and commit them with descriptive messages.
   ``` bash
    git add . # better to add individual files, this is just an example
    git commit # afterwards a text editor will open to write the commit message, close it to save the message
    git push origin feature/your-feature-name
   ```

4. **Create a Pull Request:**
   Go to the repository on GitHub and create a pull request from your branch to the main branch. Mark your PR as a draft, this is to indicate that it is a work in progress.

This is done to ensure that you are able to push changes to the remote
repository and create a pull request without any permission issues.

## Development Workflow
1. Commit often with clear messages. For example:
   ```bash
      branch-name: short-description

      detailed-explanation-of-changes
   ```
2. Push your changes to your branch regularly.
   ```
    git push origin branch-name
   ```
3. Open a pull request when your work is complete.

4. Request 2 reviews from other contributors. This is setup such
that all changes are agreed upon by at least 2 other people before merging.

## Coding Standards
- Follow PEP 8 guidelines for Python code.
https://peps.python.org/pep-0008/

## Commit Guidelines
- Use present tense ("Add feature" not "Added feature").
- Use imperative mood ("Fix bug" not "Fixed bug").
- Limit the first line to 50 characters.
- Use the body to explain what and why vs. how.

## Pull Request Process
1. Ensure your branch is up to date with the main branch. Otherwise your pull request may be blocked.
2. Create a pull request with a clear title and description.
3. Assign 2 reviewers and wait for feedback. After 2 acknowledgments, you can merge your PR.
