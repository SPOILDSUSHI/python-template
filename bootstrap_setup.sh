#!/bin/bash

sudo dnf install git zsh -y

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

curl -LsSf https://astral.sh/uv/install.sh | sh

cp -f .zshrc ~/.zshrc

uv python install 3.12

uv tool install pre-commit

