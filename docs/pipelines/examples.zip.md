---
source_file: /home/runner/work/pipelines-community/pipelines-community/australian-imaging-service-community/examples/zip.yaml
title: examples.zip
weight: 10

---

## Package Info
|Key|Value|
|---|-----|
|Name|examples.zip|
|Title|Zip up a directory|
|Package version|3.0|
|Build|0|
|Base image|`ubuntu:jammy`|
|Maintainer|Thomas G. Close (thomas.close@sydney.edu.au)|
|Info URL|https://manpages.ubuntu.com/manpages/focal/man1/zip.1.html|

This is a simple pipeline that zips up the given directory


## Command
|Key|Value|
|---|-----|
|Task|arcana.common.tasks.shell:shell_cmd|
|Operates on|session|
#### Inputs
|Name|Required data-type|Default column data-type|Description|
|----|------------------|------------------------|-----------|
|`to_zip`|<span data-toggle="tooltip" data-placement="bottom" title="generic/fs-object" aria-label="generic/fs-object">generic/fs-object</span>|<span data-toggle="tooltip" data-placement="bottom" title="generic/fs-object" aria-label="generic/fs-object">generic/fs-object</span>|Input file-system object to zip|

#### Outputs
|Name|Required data-type|Default column data-type|Description|
|----|------------------|------------------------|-----------|
|`zipped`|<span data-toggle="tooltip" data-placement="bottom" title="archive/zip" aria-label="archive/zip">archive/zip</span>|<span data-toggle="tooltip" data-placement="bottom" title="archive/zip" aria-label="archive/zip">archive/zip</span>|Zipped FS Object|

#### Parameters
|Name|Data type|Description|
|----|---------|-----------|
|`compression`|`int`|the level of compression applied|

