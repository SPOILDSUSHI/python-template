#!/bin/bash

sudo dnf install git zsh -y

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

curl -LsSf https://astral.sh/uv/install.sh | sh

dirpath=$(realpath "$0" | sed 's|\(.*\)/.*|\1|')
abspath="${dirpath}/.zshrc"
cp -f $abspath ~/.zshrc

uv python install 3.12

uv tool install pre-commit
