import os
from model import VoronoiModel
from point_loader import PointLoader, PointLoadError
from exporters import SVGExporter, ImageExporter

class VoronoiController:
    def __init__(self, model: VoronoiModel, view):
        self.model = model
        self.view = view

    def on_load_points(self):
        file_path = self.view.ask_open_filename()
        if not file_path:
            return
        try:
            points = PointLoader.load(file_path)
            if len(points) < 2:
                self.view.show_warning("Attention", "Au moins deux points sont nécessaires.")
                return
            self.model.set_points(points)
            self.view.update_display(self.model)
            self.view.set_status(f"Fichier chargé: {os.path.basename(file_path)} - {len(points)} points")
        except PointLoadError as e:
            self.view.show_error("Erreur de chargement", str(e))
        except Exception as e:
            self.view.show_error("Erreur inattendue", str(e))

    def on_export_svg(self):
        self._export(SVGExporter(), "svg", [("SVG files", "*.svg")])

    def on_export_image(self):
        self._export(ImageExporter(), "png", [("PNG files", "*.png"), ("JPEG files", "*.jpg")])

    def _export(self, exporter, default_ext, filetypes):
        if not self.model.has_valid_diagram():
            self.view.show_warning("Export impossible", "Aucun diagramme à exporter.")
            return
        file_path = self.view.ask_save_filename(f".{default_ext}", filetypes)
        if file_path:
            try:
                exporter.export(self.model, file_path)
                self.view.show_info("Succès", f"Exporté vers {file_path}")
            except Exception as e:
                self.view.show_error("Erreur d'export", str(e))