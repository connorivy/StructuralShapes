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
    def generate_cs_code(self, row: pd.Series) -> str:
        """Generate C# code for a specific shape."""
        pass


class AiscWShapeGenerator(ShapeGenerator):
    """Generator for W-shapes."""

    def generate_cs_code(self, row: pd.Series) -> str:
        shape_name = row["AISC_Manual_Label"].replace("W", "W").replace("X", "x")
        weight = row.get("W", 0)
        area = row.get("A", 0)
        d = row.get("d", 0)
        tw = row.get("tw", 0)
        tf = row.get("tf", 0)
        bf = row.get("bf", 0)
        inertia_x = row.get("Ix", 0)
        inertia_y = row.get("Iy", 0)
        torsion_constant = row.get("J", 0)
        zx = row.get("Zx", 0)
        zy = row.get("Zy", 0)

        return f"""    public static AiscWShapeData {shape_name.replace(".", "_")} => Create(\"{shape_name}\", {weight}, {area}, {d}, {tw}, {tf}, {bf}, {inertia_x}, {inertia_y}, {torsion_constant}, {zx}, {zy});
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
        code.write(generator.generate_cs_code(row))
        shape_names.append(row["AISC_Manual_Label"].replace("W", "W").replace("X", "x"))

    # Create helper method to assign the correct units to all shape properties instead of declaring them every time.
    # This is used to save space in the generated code.
    code.write("""
    public static AiscWShapeData Create(
        string name, 
        double w,
        double a, 
        double d, 
        double tw, 
        double tf, 
        double bf, 
        double ix, 
        double iy, 
        double j,
        double zx,
        double zy
    ) => new()
    {
        Name = name,
        W = new ForcePerLength(w, ForcePerLengthUnit.PoundForcePerFoot),
        A = new Area(a, AreaUnit.SquareInch),
        d = new Length(d, LengthUnit.Inch),
        tw = new Length(tw, LengthUnit.Inch),
        tf = new Length(tf, LengthUnit.Inch),
        bf = new Length(bf, LengthUnit.Inch),
        Ix = new AreaMomentOfInertia(ix, AreaMomentOfInertiaUnit.InchToTheFourth),
        Iy = new AreaMomentOfInertia(iy, AreaMomentOfInertiaUnit.InchToTheFourth),
        J = new AreaMomentOfInertia(j, AreaMomentOfInertiaUnit.InchToTheFourth),
        Zx = new Volume(zx, VolumeUnit.CubicInch),
        Zy = new Volume(zy, VolumeUnit.CubicInch)
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
        code.write(f'            "{name}",\n')
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
    public static AiscWShapeData? GetShapeByName(string name)
    {
        return name.ToLowerInvariant() switch
        {
""")
    for name in shape_names:
        code.write(f'            "{name.lower()}" => {name.replace(".", "_")},\n')
    code.write("""            _ => null,
        };
    }
""")

    code.write("}")
    return code.getvalue()


def main() -> None:
    print(f"Reading Excel file: {excel_path}")
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


if __name__ == "__main__":
    main()
