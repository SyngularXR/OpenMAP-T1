#!/usr/bin/env python3
"""
OpenMAP-T1 Mesh Export Script

This script provides easy-to-use functions for exporting 3D meshes from 
OpenMAP-T1 segmentation results using VTK's Marching Cubes algorithm.

Usage:
    python export_segment_mesh.py

Examples:
    # Test mesh export
    python export_segment_mesh.py

    # Or modify the script to specify your own segmentation file
"""

from segment_mesh import (
    export_segmentation_mesh,
    export_multi_segment_mesh,
    export_openmap_meshes,
    test_mesh_export
)
import os
import sys

# Add the current directory to Python path to import segment_mesh
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    """
    Main function to run mesh export with OpenMAP-T1 data.
    """

    print("🧠 OpenMAP-T1 Mesh Export Tool")
    print("=" * 50)

    # Look for OpenMAP-T1 output in standard locations
    possible_segmentation_files = [
        "output/MRI_AX_C_Reg/parcellated/MRI_AX_C_Reg_Type1_Level1.nii"
    ]

    segmentation_file = None
    for file_path in possible_segmentation_files:
        if os.path.exists(file_path):
            segmentation_file = file_path
            break

    if segmentation_file:
        print(f"📁 Found segmentation file: {segmentation_file}")

        # Run test first
        # print("\n🔧 Running diagnostic test...")
        # test_mesh_export(segmentation_file)

        # Ask user what to do next
        print("\n" + "=" * 50)
        print("Choose an export option:")
        print("1. Export key brain structures (recommended)")
        print("2. Export ALL 280 segments (takes longer)")
        print("3. Export specific segments")
        print("4. Exit")

        try:
            choice = input("\nEnter choice (1-4): ").strip()

            if choice == "1":
                print("\n🚀 Exporting key brain structures...")
                export_openmap_meshes(
                    openmap_output_dir="output/",  # Note: using "ouput" as in the original
                    mesh_output_dir="meshes/",
                    file_basename="MRI_AX_C_Reg"
                )

            elif choice == "2":
                print("\n🚀 Exporting ALL segments (this may take a while)...")
                export_multi_segment_mesh(
                    segmentation_data=segmentation_file,
                    output_dir="meshes/all_segments/",
                    resample_to_mm=(0.5, 0.5, 0.5),
                    smooth_iterations=5,
                    decimate_reduction=0.05,
                    output_format="stl",
                    use_anatomical_names=True
                )

            elif choice == "3":
                segments_input = input(
                    "Enter segment numbers (comma-separated, e.g., 75,76,83,84): ")
                try:
                    segment_values = [int(x.strip())
                                      for x in segments_input.split(",")]
                    print(f"\n🚀 Exporting segments: {segment_values}")
                    export_multi_segment_mesh(
                        segmentation_data=segmentation_file,
                        output_dir="meshes/custom_segments/",
                        segment_values=segment_values,
                        smooth_iterations=10,
                        decimate_reduction=0.1,
                        output_format="stl",
                        use_anatomical_names=True
                    )
                except ValueError:
                    print("❌ Invalid segment numbers. Please use format: 75,76,83,84")

            elif choice == "4":
                print("👋 Goodbye!")
                return

            else:
                print("❌ Invalid choice. Running test only.")

        except KeyboardInterrupt:
            print("\n\n👋 Export cancelled by user.")

    else:
        print("❌ No OpenMAP-T1 segmentation file found.")
        print("\nPlease ensure you have:")
        print("1. Run OpenMAP-T1 parcellation first")
        print("2. Check that output files exist in 'ouput/' or 'output/' directory")
        print("\nOr modify this script to point to your segmentation file.")

        # Still run test with any available file
        print("\n🔧 Running diagnostic test anyway...")
        test_mesh_export()


if __name__ == "__main__":
    main()
