#!/bin/bash
ssh-add --apple-use-keychain ~/.ssh/id_rsa -v
ssh-add --apple-use-keychain ~/.ssh/id_ed25519 -v
lagoon login
echo "drush uli" \
    | lagoon ssh -p ${1:-vanilla-govcms-10-beta} -e ${2:-test} \
    | sed -n -e "s|^.*amazee.io/||p" \
    | { read uli; echo "$uli"; echo "$uli" | tr -d '\n' | pbcopy;} 




