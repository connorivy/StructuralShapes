import os
import pandas as pd
from pathlib import Path
from typing import Any, Optional, Type
from abc import ABC, abstractmethod
from io import StringIO

# Define paths
project_root = Path(__file__).parent.parent
excel_path = (
    project_root
    / "assets"
    / "ShapeDatabases"
    / "AISC"
    / "aisc-shapes-database-v16.0.xlsx"
)
output_path = project_root / "src" / "StructuralShapes" / "Lib"

# Create the output directory if it doesn't exist
os.makedirs(output_path, exist_ok=True)


class ShapeGenerator(ABC):
    """Abstract base class for shape generators."""

    @abstractmethod
    def generate_code(self, row: pd.Series) -> str:
        """Generate C# code for a specific shape."""
        pass


class AiscWShapeGenerator(ShapeGenerator):
    """Generator for W-shapes."""

    def generate_code(self, row: pd.Series) -> str:
        shape_name = (
            row["AISC_Manual_Label"]
            .replace("W", "W")
            .replace("X", "x")
        )
        area = row.get("A", 0)
        weight = row.get("W", 0)
        inertia_x = row.get("Ix", 0)
        inertia_y = row.get("Iy", 0)
        torsion_constant = row.get("J", 0)

        return f"""    public static SectionProfileData {shape_name.replace(".", "_")} => Create(\"{shape_name}\", {weight}, {area}, {inertia_x}, {inertia_y}, {torsion_constant});
"""


def get_shape_generator(shape_type: str) -> Type[ShapeGenerator]:
    """Factory method to get the appropriate shape generator."""
    if shape_type.startswith("WT"):
        return None
    if shape_type.startswith("W"):
        return AiscWShapeGenerator()
    # Add other shape types here as needed
    raise ValueError(f"Unsupported shape type: {shape_type}")


def generate_wshapes_class(w_shapes_df: pd.DataFrame) -> str:
    """Generate a C# class file containing all shapes in the AISC namespace."""
    code = StringIO()
    code.write("""// Auto-generated code - Do not modify manually
using StructuralShapes.Contracts;

namespace StructuralShapes.Lib.AISC.v16_0;

/// <summary>
/// Contains definitions for all shapes according to AISC shapes database v16.0
/// </summary>
public static partial class WShapes
{
""")

    shape_names = []

    for _, row in w_shapes_df.iterrows():
        shape_type = row["AISC_Manual_Label"]
        generator = get_shape_generator(shape_type)
        code.write(generator.generate_code(row))
        shape_names.append(row["AISC_Manual_Label"].replace("W", "W").replace("X", "x"))

    # Create helper method to assign the correct units to all shape properties instead of declaring them every time.
    # This is used to save space in the generated code.
    code.write("""
    public static SectionProfileData Create(string name, double weight, double area, double inertiaX, double inertiaY, double torsionConstant) => new()
    {
        Name = name,
        NominalWeight = new ForcePerLength(weight, ForcePerLengthUnit.PoundForcePerFoot),
        Area = new Area(area, AreaUnit.SquareInch),
        Ix = new AreaMomentOfInertia(inertiaX, AreaMomentOfInertiaUnit.InchToTheFourth),
        Iy = new AreaMomentOfInertia(inertiaY, AreaMomentOfInertiaUnit.InchToTheFourth),
        J = new AreaMomentOfInertia(torsionConstant, AreaMomentOfInertiaUnit.InchToTheFourth),
    };
 
""")

    # Modify method to return filtered and sorted list of shape names
    code.write("""
    /// <summary>
    /// Returns a filtered and sorted list of all shape names.
    /// </summary>
    public static IList<string> GetAllShapeNamesSorted(string? filter = null)
    {
        string[] allNames = [
""")
    for name in sorted(shape_names):
        code.write(f"            \"{name}\",\n")
    code.write("""        ];

        if (string.IsNullOrEmpty(filter))
        {
            return allNames;
        }

        return allNames.Where(name => name.Contains(filter, StringComparison.OrdinalIgnoreCase)).ToList();
    }

""")

    # Add method to get SectionProfileData by name
    code.write("""
    /// <summary>
    /// Returns the SectionProfileData for a given shape name.
    /// </summary>
    public static SectionProfileData? GetShapeByName(string name)
    {
        return name switch
        {
""")
    for name in shape_names:
        code.write(f"            \"{name}\" => {name.replace(".", "_")},\n")
    code.write("""            _ => null,
        };
    }
""")

    code.write("}")
    return code.getvalue()


def main() -> None:
    print(f"Reading Excel file: {excel_path}")
    try:
        # Determine which sheet contains W-shapes
        # You might need to adjust this based on the actual Excel structure
        xl = pd.ExcelFile(excel_path)
        sheets = xl.sheet_names

        # Look for a sheet that might contain W-shapes (assuming the name contains "W" or "Shapes")
        shapes_sheet = None
        for sheet in sheets:
            if "Database" in sheet:
                shapes_sheet = sheet
                break

        if not shapes_sheet:
            shapes_sheet = sheets[0]  # Default to first sheet
            print(f"Warning: Could not identify W-shapes sheet, using '{shapes_sheet}'")
        else:
            print(f"Found W-shapes in sheet: '{shapes_sheet}'")

        # Read the Excel sheet
        df = pd.read_excel(excel_path, sheet_name=shapes_sheet)

        # Filter rows for W-shapes (might need adjustment based on actual data format)
        w_shapes_df = df[df["Type"] == "W"]

        if w_shapes_df.empty:
            print("No W-shapes found in the Excel file!")
            return

        print(f"Found {len(w_shapes_df)} W-shapes in the Excel file")

        # Generate the C# code
        wshapes_code = generate_wshapes_class(w_shapes_df)

        # Define the output file path
        output_file = output_path / "WShapes.cs"

        # Write the generated code to the file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(wshapes_code)

        print(f"W-shapes class file generated at: {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
