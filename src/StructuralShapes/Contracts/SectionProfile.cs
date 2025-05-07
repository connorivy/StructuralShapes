namespace StructuralShapes.Contracts;

public interface ISectionProfile
{
    string Name { get; }
}

public interface IConstantSectionProfile : ISectionProfile
{
    public ForcePerLength NominalWeight { get; }
    public Area Area { get; }
}

public record SectionProfileData : IConstantSectionProfile
{
    public required string Name { get; init; }
    public required ForcePerLength NominalWeight { get; init; }
    public required Area Area { get; init; }
    public required AreaMomentOfInertia Ix { get; init; }
    public required AreaMomentOfInertia Iy { get; init; }
    public required AreaMomentOfInertia J { get; init; }
    public Area? StrongAxisShearArea { get; init; }
    public Area? WeakAxisShearArea { get; init; }
}
