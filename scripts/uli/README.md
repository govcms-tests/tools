# Automated Drush ULI retrieval script

Make it executable:

```shell
chmod +x uli.sh
```

To be able to call this script without the extension anywhere, create an alias:

```shell
alias uli="uli.sh"
```

and add its location to PATH:

```shell
export PATH="$PATH:<path to script directory>"
```

## Compatability

Currently, this script is compatible with MacOS due to the use of `pbcopy`.
