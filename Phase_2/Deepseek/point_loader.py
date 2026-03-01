from typing import List, Tuple

class PointLoadError(Exception):
    pass

class PointLoader:
    @staticmethod
    def load(file_path: str) -> List[Tuple[float, float]]:
        points = []
        with open(file_path, 'r') as f:
            lines = f.readlines()
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) != 2:
                raise PointLoadError(f"Ligne {line_num} invalide : {line}")
            try:
                x = float(parts[0].strip())
                y = float(parts[1].strip())
            except ValueError:
                raise PointLoadError(f"Coordonnées non numériques à la ligne {line_num} : {line}")
            points.append((x, y))
        return points