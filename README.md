# ha-icon-generator

Generate custom icon packs for Home Assistant from a directory of SVGs

Used by:

* [artifactory-icons](https://github.com/Perth-Artifactory/artifactory-icons)

## Generation

This script can either be used manually or configured via Github Actions.

### Manual

`generate.py <svg directory> <icon prefix>`

This will generate `<icon prefix>-icons.json` which you can then copy to your Home Assistant installation.

### Github Actions

* Add `example_workflow.yaml` to the appropriate directory within your Github repo
* Update the call to this script within the workflow with your desired prefix and SVG folder name. The default prefix is 'af' with SVGs stored in a directory called `svg` so the line is set to `python3 generator/generate.py svg af`
* Commit an icon to the repo
* Check that the action completed successfully. Malformed SVGs (or ones we haven't accounted for) will cause the action to fail. If you think the SVG is normal please raise an issue in this repo with the file so we can add support for that particular format.

## Installation and usage

* Clone or copy the repo to somewhere within your Home Assistant `www` directory.
* Reference the file either in `configuration.yaml` or a lovelace config

`configuration.yaml`
```
frontend:
  extra_module_url:
    - /local/af-icons.js
```

lovelace
```
resources:
  - type: js
    url: /local/af-icons.js
```

* Restart Home Assistant
* Use your icons the same way you would any other. ie: `mdi:sun` vs `af:better-sun` (not a real icon)

## Thanks

The format of the generated js and the installation instructions are based on [Emanuele's](https://github.com/elax46/) [custom brand icons](https://github.com/elax46/custom-brand-icons/) repo.