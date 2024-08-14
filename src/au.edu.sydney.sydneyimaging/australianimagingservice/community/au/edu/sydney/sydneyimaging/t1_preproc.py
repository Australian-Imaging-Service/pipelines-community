# from fileformats.medimage_mrtrix3 import ImageFormat as MIF
# from pydra.tasks.fastsurfer.latest import fastsurfer

from pydra import Workflow, mark, ShellCommandTask
from pydra.engine.specs import SpecInfo, BaseSpec, ShellSpec, ShellOutSpec, File
from pydra.tasks.mrtrix3.v3_0 import (
    LabelConvert,
    LabelSgmfix,
    Fivett2Vis,
    FivettGen_Hsvs,
)
from fileformats.medimage_mrtrix3 import ImageFormat
from pydra.tasks.fastsurfer.v2_2 import Fastsurfer
from pathlib import Path
import os


os.environ["SUBJECTS_DIR"] = ""


def t1_processing_pipeline(parcellation: str, mrtrix_lut_dir: Path, fs_license: Path) -> Workflow:
    # Define the input values using input_spec
    input_spec = {"t1w": File, "parcellation": str}
    # Define the output_spec for the workflow
    output_spec = {"parc_image": ImageFormat}
    wf = Workflow(
        name="t1_processing_pipeline", input_spec=input_spec, output_spec=output_spec
    )

    # ###################
    # # FASTSURFER TASK #
    # ###################

    wf.add(
        fastsurfer(
            T1_files=wf.lzin.t1w,
            fs_license=wf.lzin.fs_license,
            subject_id="FS_outputs",
            name="FastSurfer_task",
            py="python3.11",
            norm_img="norm.mgz",
            aparcaseg_img="aparcaseg.mgz",
            fsaparc=True,
            parallel=True,
            threads=24,
        )
    )

    # #################################################
    # # FIVE TISSUE TYPE Generation and visualisation #
    # #################################################
    if (
        parcellation == "desikan"
    ):  # to avoid repeating this on every iteration of loop, only exectute on one (first) parcellation
        # ftt_image=os.path.join(output_path,"5TT_hsvs.mif")
        # vis_image=os.path.join(output_path,"5TTvis_hsvs.mif")

        # Five tissue-type task
        wf.add(
            FivettGen_Hsvs(
                in_file=wf.FastSurfer_task.lzout.subjects_dir_output,
                # out_file=ftt_image,
                name="fTTgen_task",
                nocrop=True,
                sgm_amyg_hipp=True,
                nocleanup=True,
                white_stem=True,
            )
        )

        # Five tissue-type visualisation task
        wf.add(
            Fivett2Vis(
                in_file=wf.fTTgen_task.lzout.out_file,
                # out_file=vis_image,
                name="fTTvis_task",
            )
        )

    #################################
    # PARCELLATION IMAGE GENERATION #
    #################################

    @mark.task
    @mark.annotate(
        {
            "parcellation": str,
            "FS_dir": str,
            "freesurfer_home": str,
            "return": {
                "parc": str,
                "fsavg_dir": str,
                "parc_lut_file": str,
                "mrtrix_lut_file": str,
                "output_parcellation_filename": str,
                "lh_annotation": str,
                "rh_annotation": str,
                "source_annotation_file_lh": str,
                "source_annotation_file_rh": str,
                "node_image": str,
                "output_parcellation_filename": str,
                "normimg_path": str,
                "final_parc_image": str,
            },
        }
    )
    def join_task_catalogue(
        parcellation: str,
        FS_dir: str,
        freesurfer_home: str,
        mrtrix_lut_dir: Path,
        # output_path: Path,
    ):
        node_image = parcellation + "_nodes.mif"
        final_parc_image ="parcellation_image_" + parcellation + ".mif.gz"
        normimg_path = os.path.join(FS_dir, "mri", "norm.mgz")
        parc = parcellation

        if parcellation == "desikan":
            # DESIKAN definitions
            fsavg_dir = ""
            parc_lut_file = os.path.join(os.environ["FREESURFER_HOME"], "FreeSurferColorLUT.txt")
            mrtrix_lut_file = os.path.join(mrtrix_lut_dir, "fs_default.txt")
            output_parcellation_filename = os.path.join(FS_dir, "mri", "aparc+aseg.mgz")
            lh_annotation = ""
            rh_annotation = ""
            source_annotation_file_lh = ""
            source_annotation_file_rh = ""

            return (
                parc,
                fsavg_dir,
                parc_lut_file,
                mrtrix_lut_file,
                output_parcellation_filename,
                lh_annotation,
                rh_annotation,
                source_annotation_file_lh,
                source_annotation_file_rh,
                node_image,
                normimg_path,
                final_parc_image,
            )

        elif parcellation == "destrieux":
            # DESTRIEUX definitions
            fsavg_dir = ""
            parc_lut_file = os.path.join(freesurfer_home, "FreeSurferColorLUT.txt")
            mrtrix_lut_file = os.path.join(mrtrix_lut_dir, "fs_a2009s.txt")
            output_parcellation_filename = os.path.join(
                FS_dir, "mri", "aparc.a2009s+aseg.mgz"
            )
            lh_annotation = ""
            rh_annotation = ""
            source_annotation_file_lh = ""
            source_annotation_file_rh = ""

            return (
                parc,
                fsavg_dir,
                parc_lut_file,
                mrtrix_lut_file,
                output_parcellation_filename,
                lh_annotation,
                rh_annotation,
                source_annotation_file_lh,
                source_annotation_file_rh,
                node_image,
                normimg_path,
                final_parc_image,
            )

        elif parcellation == "HCPMMP1":
            # HCPMMP1 definitions
            fsavg_dir = os.path.join(freesurfer_home, "subjects", "fsaverage")
            parc_lut_file = os.path.join(mrtrix_lut_dir, "HCPMMP1_original.txt")
            mrtrix_lut_file = os.path.join(mrtrix_lut_dir, "HCPMMP1_ordered.txt")
            output_parcellation_filename = os.path.join(
                FS_dir, "mri", "aparc.HCPMMP1+aseg.mgz"
            )
            lh_annotation = os.path.join(FS_dir, "label", "lh.HCPMMP1.annot")
            rh_annotation = os.path.join(FS_dir, "label", "rh.HCPMMP1.annot")
            source_annotation_file_lh = os.path.join(
                fsavg_dir, "label", "lh.HCPMMP1.annot"
            )
            source_annotation_file_rh = os.path.join(
                fsavg_dir, "label", "rh.HCPMMP1.annot"
            )

            return (
                parc,
                fsavg_dir,
                parc_lut_file,
                mrtrix_lut_file,
                output_parcellation_filename,
                lh_annotation,
                rh_annotation,
                source_annotation_file_lh,
                source_annotation_file_rh,
                node_image,
                normimg_path,
                final_parc_image,
            )

        elif parcellation == "Yeo7":
            # yeo7 definitions
            fsavg_dir = os.path.join(freesurfer_home, "subjects", "fsaverage5")
            parc_lut_file = os.path.join(
                freesurfer_home, "Yeo2011", "Yeo2011_7networks_Split_Components_LUT.txt"
            )
            mrtrix_lut_file = os.path.join(mrtrix_lut_dir, "Yeo2011_7N_split.txt")
            output_parcellation_filename = os.path.join(
                FS_dir, "mri", "aparc.Yeo7+aseg.mgz"
            )
            lh_annotation = os.path.join(FS_dir, "label", "lh.Yeo7.annot")
            rh_annotation = os.path.join(FS_dir, "label", "rh.Yeo7.annot")
            source_annotation_file_lh = os.path.join(
                fsavg_dir, "label", "lh.Yeo2011_7Networks_N1000.split_components.annot"
            )
            source_annotation_file_rh = os.path.join(
                fsavg_dir, "label", "rh.Yeo2011_7Networks_N1000.split_components.annot"
            )

            return (
                parc,
                fsavg_dir,
                parc_lut_file,
                mrtrix_lut_file,
                output_parcellation_filename,
                lh_annotation,
                rh_annotation,
                source_annotation_file_lh,
                source_annotation_file_rh,
                node_image,
                normimg_path,
                final_parc_image,
            )

        elif parcellation == "Yeo17":
            # yeo17 definitions
            fsavg_dir = os.path.join(freesurfer_home, "subjects", "fsaverage5")
            parc_lut_file = os.path.join(
                freesurfer_home,
                "Yeo2011",
                "Yeo2011_17networks_Split_Components_LUT.txt",
            )
            mrtrix_lut_file = os.path.join(mrtrix_lut_dir, "Yeo2011_17N_split.txt")
            output_parcellation_filename = os.path.join(
                FS_dir, "mri", "aparc.Yeo17+aseg.mgz"
            )
            lh_annotation = os.path.join(FS_dir, "label", "lh.Yeo17.annot")
            rh_annotation = os.path.join(FS_dir, "label", "rh.Yeo17.annot")
            source_annotation_file_lh = os.path.join(
                fsavg_dir, "label", "lh.Yeo2011_17Networks_N1000.split_components.annot"
            )
            source_annotation_file_rh = os.path.join(
                fsavg_dir, "label", "rh.Yeo2011_17Networks_N1000.split_components.annot"
            )

            return (
                parc,
                fsavg_dir,
                parc_lut_file,
                mrtrix_lut_file,
                output_parcellation_filename,
                lh_annotation,
                rh_annotation,
                source_annotation_file_lh,
                source_annotation_file_rh,
                node_image,
                normimg_path,
                final_parc_image,
            )

    wf.add(
        join_task_catalogue(
            FS_dir=wf.FastSurfer_task.lzout.subjects_dir_output,
            parcellation=parcellation,
            freesurfer_home=freesurfer_home,
            mrtrix_lut_dir=mrtrix_lut_dir,
            output_path=output_path,
            name="join_task",
        )
    )

    ###########################
    # mri_surf2surf spec info #
    ###########################

    mri_s2s_input_spec = SpecInfo(
        name="Input",
        fields=[
            (
                "source_subject_id",
                str,
                {
                    "help_string": "source subject",
                    "argstr": "--srcsubject",
                    "mandatory": True,
                },
            ),
            (
                "target_subject_id",
                str,
                {
                    "help_string": "target subject",
                    "argstr": "--trgsubject",
                    "mandatory": True,
                },
            ),
            (
                "source_annotation_file",
                str,
                {
                    "help_string": "annotfile : map annotation",
                    "argstr": "--sval-annot",
                    "mandatory": True,
                },
            ),
            (
                "target_annotation_file",
                str,
                {
                    "help_string": "path of file in which to store output values",
                    "argstr": "--tval",
                    "mandatory": True,
                },
            ),
            (
                "hemisphere",
                str,
                {
                    "help_string": "hemisphere : (lh or rh) for both source and targ",
                    "argstr": "--hemi",
                    "mandatory": True,
                },
            ),
            (
                "annot",
                str,
                {
                    "help_string": "dummy parameter to help with dependencies",
                    "mandatory": False,
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    mri_s2s_output_spec = SpecInfo(
        name="Output",
        fields=[
            (
                "target_annotation_file",
                str,
                {
                    "help_string": "path of file in which to store output values",
                    "argstr": "--tval",
                    "mandatory": True,
                },
            ),
            (
                "annot",
                str,
                {
                    "help_string": "dummy parameter to help with dependencies",
                    "mandatory": False,
                },
            ),
        ],
        bases=(ShellOutSpec,),
    )

    # ############################
    # # mri_aparc2aseg spec info #
    # ############################

    mri_a2a_input_spec = SpecInfo(
        name="Input",
        fields=[
            (
                "subject",
                str,
                {
                    "help_string": "Name of the subject as found in the SUBJECTS_DIR",
                    "argstr": "--s",
                    "mandatory": True,
                },
            ),
            (
                "old_ribbon",
                bool,
                {
                    "help_string": "use mri/hemi.ribbon.mgz as a mask for the cortex",
                    "argstr": "--old-ribbon",
                    "mandatory": True,
                },
            ),
            (
                "annotname",
                str,
                {
                    "help_string": "Use annotname surface annotation. By default, uses ?h.aparc.annot. With this option, it will load ?h.annotname.annot. The output file will be set to annotname+aseg.mgz, but this can be changed with --o. Note: running --annot aparc.a2009s is NOT the same as running --a2009s. The index numbers will be different.",
                    "argstr": "--annot",
                    "mandatory": True,
                },
            ),
            (
                "volfile",
                str,
                {
                    "help_string": "Full path of file to save the output segmentation in. Default is mri/aparc+aseg.mgz",
                    "argstr": "--o",
                    "mandatory": True,
                },
            ),
        ],
        bases=(ShellSpec,),
    )

    mri_a2a_output_spec = SpecInfo(
        name="Output",
        fields=[
            (
                "volfile",
                str,
                {
                    "help_string": "Full path of file to save the output segmentation in. Default is mri/aparc+aseg.mgz",
                    "argstr": "--o",
                    "mandatory": True,
                },
            ),
        ],
        bases=(ShellOutSpec,),
    )

    ##########################################################
    # # additional mapping for 'HCPMMP1', 'yeo17', 'yeo7 #
    ##########################################################

    volfile = wf.join_task.lzout.output_parcellation_filename

    if parcellation in ["HCPMMP1", "Yeo17", "Yeo7"]:
        ##################################
        # mri_surf2surf task - lh and rh #
        ##################################
        hemispheres = ["lh", "rh"]
        for hemi in hemispheres:
            wf.add(
                ShellCommandTask(
                    name=f"mri_s2s_task_{hemi}",
                    executable="mri_surf2surf",
                    input_spec=mri_s2s_input_spec,
                    output_spec=mri_s2s_output_spec,
                    # cache_dir=output_path,
                    source_subject_id=wf.join_task.lzout.fsavg_dir,
                    target_subject_id=wf.FastSurfer_task.lzout.subjects_dir_output,
                    source_annotation_file=getattr(
                        wf.join_task.lzout, f"source_annotation_file_{hemi}"
                    ),
                    target_annotation_file=getattr(
                        wf.join_task.lzout, f"{hemi}_annotation"
                    ),
                    hemisphere=hemi,
                    annot=parcellation,
                )
            )

        # ########################
        # # mri_aparc2aseg task  #
        # ########################

        wf.add(
            ShellCommandTask(
                name="mri_a2a_task",
                executable="mri_aparc2aseg",
                input_spec=mri_a2a_input_spec,
                output_spec=mri_a2a_output_spec,
                # cache_dir=output_path,
                subject=wf.FastSurfer_task.lzout.subjects_dir_output,
                old_ribbon=True,
                annotname=wf.mri_s2s_task_rh.lzout.annot,
                volfile=volfile,
            )
        )

        volfile = wf.mri_a2a_task.lzout.volfile

    ##########################################################
    # PARCELLATION EDITS - applies to all parcellation types #
    ##########################################################

    # relabel segmenetation to integers
    wf.add(
        LabelConvert(
            path_in=volfile,
            lut_in=wf.join_task.lzout.parc_lut_file,
            lut_out=wf.join_task.lzout.mrtrix_lut_file,
            image_out=wf.join_task.lzout.node_image,
            name="LabelConvert_task",
        )
    )

    # # # # Replace FreeSurfer’s estimates of sub-cortical grey matter structures with estimates from FSL’s FIRST tool
    wf.add(
        LabelSgmfix(
            parc=wf.LabelConvert_task.lzout.image_out,
            t1=wf.join_task.lzout.normimg_path,
            lut=wf.join_task.lzout.mrtrix_lut_file,
            out_file=wf.join_task.lzout.final_parc_image,
            name="SGMfix_task",
            nocleanup=True,
            premasked=True,
            sgm_amyg_hipp=True,
        )
    )

    # Set parcellation image to the workflow output
    wf.set_output(("parc_img", wf.SGMfix_task.lzout.out_file))

    return wf
