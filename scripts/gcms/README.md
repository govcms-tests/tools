# Local GovCMS refresh script

Running this script removes the previous GovCMS installation (by default located at `~/dev/GovCMS`) and clones a new one.
It also sets up the official repo as a remote.

To make it executable via `gcms`, do the following:

```shell
chmod +x gcms.sh
```

Create an alias and add the script's location to PATH:

```shell
alias gcms="gcms.sh"
export PATH="$PATH:<path to script directory>"
```
