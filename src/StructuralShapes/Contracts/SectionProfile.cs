using UnitsNet;

namespace StructuralShapes.Contracts;

public interface ISectionProfile
{
    string Name { get; }
}

public interface IConstantSectionProfile : ISectionProfile
{
    public ForcePerLength W { get; }
    public Area A { get; }
}

public record AiscWShapeData : IConstantSectionProfile
{
    public required string Name { get; init; }
    public required ForcePerLength W { get; init; }
    public required Area A { get; init; }
    public required Length d { get; init; }
    public required Length tw { get; init; }
    public required Length tf { get; init; }
    public required Length bf { get; init; }
    public required AreaMomentOfInertia Ix { get; init; }
    public required AreaMomentOfInertia Iy { get; init; }
    public required AreaMomentOfInertia J { get; init; }
    public required Volume Zx { get; init; }
    public required Volume Zy { get; init; }
    // public Area? StrongAxisShearArea { get; init; }
    // public Area? WeakAxisShearArea { get; init; }
}
