from dataclasses import dataclass
@dataclass
class Movie:
    id: int
    name: str
    year: int
    rank: float


    def __str__(self):
        return f'{self.id} - {self.name}'

    def __hash__(self):
        return hash(self.id)