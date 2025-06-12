# Template for python repo

<p align="center">
    <a href="./assets/coverage.svg" alt="Coverage">
        <img src="./assets/coverage.svg"/>
    </a>
</p>

Subtitle

# How to use this

### 1. Clean Fedora install
1. Install git and zsh
2. Install oh-my-zsh
3. Install uv
4. Replace .zshrc file with pre-configured options
5. Install Python 3.12
6. Install pre-commit

`./bootstrap_setup.sh`

### 2. Install user level dependencies

`pip install nox pre-commit`

### 3. Set up pre-commit

`pre-commit install`

### 4. Write great code with great tests!

`poetry run uvicorn src.app.main:app --reload --port=8080`

### 5. Use Nox for testing

`nox`
`nox -rs tests`
