from dataclasses import dataclass

from shapely import MultiPolygon, Polygon

from mapy.color import Color
from mapy.render.context import RenderContext


@dataclass
class FillItem:
    polygon: Polygon | MultiPolygon
    fill_color: Color
    line_color: Color
    line_width: int = 0


class FillLayer:
    def __init__(self, items: list[FillItem]) -> None:
        self.items = items

    def render(self, context: RenderContext) -> None:
        for item in self.items:
            polygon_in_img_crs = context.transformer.transform_to_image_crs(
                item.polygon
            )
            if isinstance(polygon_in_img_crs, MultiPolygon):
                for poly in polygon_in_img_crs.geoms:
                    context.render_backend.draw_polygon(
                        polygon=poly,
                        line_color=item.line_color,
                        fill_color=item.fill_color,
                        line_width=item.line_width,
                    )
            else:
                context.render_backend.draw_polygon(
                    polygon=polygon_in_img_crs,
                    line_color=item.line_color,
                    fill_color=item.fill_color,
                    line_width=item.line_width,
                )
