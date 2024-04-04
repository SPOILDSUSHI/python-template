#!/bin/bash

set -e

ssh_init() {
    Email=""
    Password=""
    while getopts ":ep:" option; do
        case $option in
            e) # Email
                Email=$OPTARG;;
            p) # password
                Password=$OPTARG;;
            \?) # Invalid option
                echo "Error: Invalid option"
                exit;;
        esac
    done
    if ! test -f ~/.ssh/id_ed25519-github; then
        ssh-keygen -t ed25519 -C "$Email" -N "$Password" -f ~/.ssh/id_ed25519-github -q
    else
        echo "Key already exists"
    fi
}

poetry_init() {
    # remember to get correct python version setup with pyenv first 
    
    if ! test -d ~/.local/share/pypoetry; then
        curl -sSL https://install.python-poetry.org | python -
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
        mkdir $ZSH_CUSTOM/plugins/poetry
        poetry completions zsh > $ZSH_CUSTOM/plugins/poetry/_poetry

    else
        echo "Poetry is already installed"
    fi
}

"$@"

if ! test -d ~/.oh-my-zsh; then
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh) --unattended"
    sed -i -e 's/ZSH_THEME=.*/ZSH_THEME="af-magic"/' ~/.zshrc
    sed -i -e 's/plugins=.*/plugins=(git python poetry pyenv)/' ~/.zshrc
else
    echo "OMZ is already installed"
fi

if ! test -d ~/.pyenv; then
    curl https://pyenv.run | bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init -)"' >> ~/.zshrc
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zprofile
    echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zprofile
    echo 'eval "$(pyenv init -)"' >> ~/.zprofile
    export POETRY_VIRTUALENVS_IN_PROJECT=true
    export POETRY_KEYRING_ENABLED=false

else
    echo "Pyenv is already installed"
fi




#ssh key add to zshrc
# eval "$(ssh-agent -s)"
# ssh-add ~/.ssh/id_ed25519-github

