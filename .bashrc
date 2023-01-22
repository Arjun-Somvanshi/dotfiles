#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='exa -l --color=always --icons --group-directories-first'
alias ll='ls -la'
alias svim='sudo -E vim'
export PS1="\[\e[0;31m\]\u \[\e[0;33m\]@ \[\e[0;32m\]\h \[\e[0;35m\]\W \[\e[0;33m\]>>> \[\e[0m\]"

export PATH=$PATH:/home/zephyrus/.local/bin
export PYENV_ROOT="$HOME/.pyenv"
AWT_TOOLKIT=MToolkit
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
export ANDROID_HOME=/home/zephyrus/Android/Sdk
. "$HOME/.cargo/env"
