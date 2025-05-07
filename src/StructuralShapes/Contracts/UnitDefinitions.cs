using System.Diagnostics.CodeAnalysis;

namespace StructuralShapes.Contracts;

public enum LengthUnit
{
    Undefined = 0,
    Centimeter,
    Foot,
    Inch,
    Meter,
    Millimeter,
}

public enum AreaUnit
{
    Undefined = 0,
    SquareCentimeter,
    SquareFoot,
    SquareInch,
    SquareMeter,
    SquareMillimeter,
}

public enum VolumeUnit
{
    Undefined = 0,
    CubicCentimeter,
    CubicFoot,
    CubicInch,
    CubicMeter,
    CubicMillimeter,
}

public enum AreaMomentOfInertiaUnit
{
    Undefined = 0,
    CentimeterToTheFourth,
    FootToTheFourth,
    InchToTheFourth,
    MeterToTheFourth,
    MillimeterToTheFourth,
}

public enum ForceUnit
{
    Undefined = 0,
    Kilonewton,
    KilopoundForce,
    Newton,
    PoundForce,
}

public enum AngleUnit
{
    Undefined = 0,
    Degree,
    Radian,
}

public enum TorqueUnit
{
    Undefined = 0,
    KilonewtonCentimeter,
    KilonewtonMeter,
    KilonewtonMillimeter,
    KilopoundForceFoot,
    KilopoundForceInch,
    NewtonCentimeter,
    NewtonMeter,
    NewtonMillimeter,
    PoundForceFoot,
    PoundForceInch,
}

public enum ForcePerLengthUnit
{
    Undefined = 0,
    KilonewtonPerCentimeter,
    KilonewtonPerMeter,
    KilonewtonPerMillimeter,
    KilopoundForcePerFoot,
    KilopoundForcePerInch,
    NewtonPerCentimeter,
    NewtonPerMeter,
    NewtonPerMillimeter,
    PoundForcePerFoot,
    PoundForcePerInch,
}

public enum PressureUnit
{
    Undefined = 0,
    KilonewtonPerSquareCentimeter,
    KilonewtonPerSquareMeter,
    KilonewtonPerSquareMillimeter,
    KilopoundForcePerSquareFoot,
    KilopoundForcePerSquareInch,
    NewtonPerSquareCentimeter,
    NewtonPerSquareMeter,
    NewtonPerSquareMillimeter,
    PoundForcePerSquareFoot,
    PoundForcePerSquareInch,
}

public readonly record struct Length
{
    public required double Value { get; init; }
    public required LengthUnit Unit { get; init; }

    public Length() { }

    [SetsRequiredMembers]
    public Length(double value, LengthUnit unit)
    {
        Value = value;
        Unit = unit;
    }
}

public readonly record struct Area
{
    public required double Value { get; init; }
    public required AreaUnit Unit { get; init; }

    public Area() { }

    [SetsRequiredMembers]
    public Area(double value, AreaUnit unit)
    {
        Value = value;
        Unit = unit;
    }
}

public readonly record struct Volume
{
    public required double Value { get; init; }
    public required VolumeUnit Unit { get; init; }

    public Volume() { }

    [SetsRequiredMembers]
    public Volume(double value, VolumeUnit unit)
    {
        Value = value;
        Unit = unit;
    }
}

public readonly record struct AreaMomentOfInertia
{
    public required double Value { get; init; }
    public required AreaMomentOfInertiaUnit Unit { get; init; }

    public AreaMomentOfInertia() { }

    [SetsRequiredMembers]
    public AreaMomentOfInertia(double value, AreaMomentOfInertiaUnit unit)
    {
        Value = value;
        Unit = unit;
    }
}

public readonly record struct Force
{
    public required double Value { get; init; }
    public required ForceUnit Unit { get; init; }

    public Force() { }

    [SetsRequiredMembers]
    public Force(double value, ForceUnit unit)
    {
        Value = value;
        Unit = unit;
    }
}

public readonly record struct Angle
{
    public required double Value { get; init; }
    public required AngleUnit Unit { get; init; }

    [SetsRequiredMembers]
    public Angle()
        : this(0, AngleUnit.Radian) { }

    [SetsRequiredMembers]
    public Angle(double value, AngleUnit unit)
    {
        Value = value;
        Unit = unit;
    }
}

public readonly record struct Torque
{
    public required double Value { get; init; }
    public required TorqueUnit Unit { get; init; }

    public Torque() { }

    [SetsRequiredMembers]
    public Torque(double value, TorqueUnit unit)
    {
        Value = value;
        Unit = unit;
    }
}

public readonly record struct ForcePerLength
{
    public required double Value { get; init; }
    public required ForcePerLengthUnit Unit { get; init; }

    public ForcePerLength() { }

    [SetsRequiredMembers]
    public ForcePerLength(double value, ForcePerLengthUnit unit)
    {
        Value = value;
        Unit = unit;
    }
}

public readonly record struct Pressure
{
    public required double Value { get; init; }
    public required PressureUnit Unit { get; init; }

    public Pressure() { }

    [SetsRequiredMembers]
    public Pressure(double value, PressureUnit unit)
    {
        Value = value;
        Unit = unit;
    }
}
