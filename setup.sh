#!/bin/bash

function printStatement() {
    echo $1
}

# poetry setup
function setupPoetry() {
    printStatement "installing poetry"
    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
    if [ $? == 0 ]; then
        printStatement 'adding bin to path variable'
        echo 'export PATH=$HOME/.poetry/bin:$PATH' >>$HOME/.bashrc
        source $HOME/.bashrc
        poetry --version
    fi
}

setupPoetry