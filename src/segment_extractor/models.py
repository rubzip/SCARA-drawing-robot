from dataclasses import dataclass

@dataclass
class Point:
    x: float 
    y: float

    def distance(self, p: "Point") -> float:
        return (self.x - p.x) ** 2 + (self.y - p.y) ** 2
    
    def to_json(self) -> tuple[float, float]:
        return (float(self.x), float(self.y))
    
    def __hash__(self):
        return hash(self.to_json())

@dataclass
class Segment:
    points: list[Point]

    def first(self) -> Point:
        return self.points[0]
    
    def last(self) -> Point:
        return self.points[-1]
    
    def to_json(self) -> tuple[tuple[float, float]]:
        return tuple(p.to_json() for p in self.points)
    
    def __len__(self) -> float:
        return len(self.points)

    def __iter__(self):
        return iter(self.points)
