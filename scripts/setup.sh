#!/bin/bash



export POETRY_VIRTUALENVS_IN_PROJECT=true

# add this to zshrc
export PATH="$HOME/.local/bin:$PATH"

mkdir $ZSH_CUSTOM/plugins/poetry
poetry completions zsh > $ZSH_CUSTOM/plugins/poetry/_poetry
