---
source_file: /home/runner/work/pipelines-community/pipelines-community/australian-imaging-service-community/examples/bet.yaml
title: examples.bet
weight: 10

---

## Package Info
|Key|Value|
|---|-----|
|Name|examples.bet|
|Title|Example BET pipeline|
|Package version|6.0.6.4|
|Build|1|
|Base image|`vnmd/fsl_6.0.6.4:20230618`|
|Maintainer|Thomas G. Close (thomas.close@sydney.edu.au)|
|Info URL|https://fsl.fmrib.ox.ac.uk/fsl/fslwiki|

An example wrapping BET in a XNAT pipeline


## Command
|Key|Value|
|---|-----|
|Task|arcana.common.tasks.shell:shell_cmd|
|Operates on|session|
#### Inputs
|Name|Required data-type|Default column data-type|Description|
|----|------------------|------------------------|-----------|
|`T1w`|<span data-toggle="tooltip" data-placement="bottom" title="medimage/nifti-gz" aria-label="medimage/nifti-gz">medimage/nifti-gz</span>|<span data-toggle="tooltip" data-placement="bottom" title="medimage/dicom-set" aria-label="medimage/dicom-set">medimage/dicom-set</span>|T1-weighted anatomical scan|

#### Outputs
|Name|Required data-type|Default column data-type|Description|
|----|------------------|------------------------|-----------|
|`brain`|<span data-toggle="tooltip" data-placement="bottom" title="medimage/nifti-gz" aria-label="medimage/nifti-gz">medimage/nifti-gz</span>|<span data-toggle="tooltip" data-placement="bottom" title="medimage/nifti-gz" aria-label="medimage/nifti-gz">medimage/nifti-gz</span>|Brain-extracted data|

#### Parameters
|Name|Data type|Description|
|----|---------|-----------|

