#!/usr/bin/env python3
"""Render deterministic review views and a contact sheet for a built design."""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class ReviewView:
    name: str
    direction: tuple[float, float, float]
    view_up: tuple[float, float, float] = (0.0, 0.0, 1.0)
    perspective: bool = False
    silhouette: bool = False
    feature_edges: bool = False
    clipped: bool = False


VIEWS = (
    ReviewView("front", (0.0, -1.0, 0.0)),
    ReviewView("right", (1.0, 0.0, 0.0)),
    ReviewView("rear", (0.0, 1.0, 0.0)),
    ReviewView("top", (0.0, 0.0, 1.0), view_up=(0.0, 1.0, 0.0)),
    ReviewView("hero", (1.0, -1.0, 0.72), perspective=True),
    ReviewView("opposite", (-1.0, 1.0, 0.58), perspective=True),
    ReviewView("low", (1.0, -1.0, 0.18), perspective=True),
    ReviewView("silhouette", (0.0, -1.0, 0.0), silhouette=True),
    ReviewView("section_edges", (1.0, 0.0, 0.0), feature_edges=True, clipped=True),
)


def normalized(vector: tuple[float, float, float]) -> tuple[float, float, float]:
    length = math.sqrt(sum(component * component for component in vector))
    return tuple(component / length for component in vector)


def add_review_scene(renderer, polydata, view: ReviewView, bounds: tuple[float, ...]) -> None:
    from vtkmodules.vtkCommonDataModel import vtkPlane
    from vtkmodules.vtkFiltersCore import vtkFeatureEdges, vtkPolyDataNormals
    from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkTextActor

    xmin, xmax, ymin, ymax, zmin, zmax = bounds
    center = ((xmin + xmax) / 2.0, (ymin + ymax) / 2.0, (zmin + zmax) / 2.0)
    diagonal = math.sqrt((xmax - xmin) ** 2 + (ymax - ymin) ** 2 + (zmax - zmin) ** 2)

    normals = vtkPolyDataNormals()
    normals.SetInputData(polydata)
    normals.SetFeatureAngle(42.0)
    normals.SetConsistency(True)
    normals.SetAutoOrientNormals(True)
    normals.SetSplitting(True)
    normals.Update()

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())
    if view.clipped:
        plane = vtkPlane()
        plane.SetOrigin(*center)
        plane.SetNormal(1.0, 0.0, 0.0)
        mapper.AddClippingPlane(plane)

    actor = vtkActor()
    actor.SetMapper(mapper)
    prop = actor.GetProperty()
    if view.silhouette:
        prop.SetColor(0.03, 0.03, 0.03)
        prop.SetAmbient(1.0)
        prop.SetDiffuse(0.0)
        renderer.SetBackground(0.96, 0.96, 0.94)
    else:
        prop.SetColor(0.82, 0.53, 0.19)
        prop.SetAmbient(0.18)
        prop.SetDiffuse(0.78)
        prop.SetSpecular(0.28)
        prop.SetSpecularPower(32.0)
        renderer.SetBackground(0.10, 0.12, 0.16)
        renderer.GradientBackgroundOn()
        renderer.SetBackground2(0.24, 0.28, 0.34)
    renderer.AddActor(actor)

    if view.feature_edges:
        edges = vtkFeatureEdges()
        edges.SetInputConnection(normals.GetOutputPort())
        edges.BoundaryEdgesOn()
        edges.FeatureEdgesOn()
        edges.NonManifoldEdgesOn()
        edges.ManifoldEdgesOff()
        edges.SetFeatureAngle(32.0)
        edge_mapper = vtkPolyDataMapper()
        edge_mapper.SetInputConnection(edges.GetOutputPort())
        if view.clipped:
            edge_mapper.AddClippingPlane(plane)
        edge_actor = vtkActor()
        edge_actor.SetMapper(edge_mapper)
        edge_actor.GetProperty().SetColor(0.04, 0.05, 0.06)
        edge_actor.GetProperty().SetLineWidth(2.0)
        renderer.AddActor(edge_actor)

    label = vtkTextActor()
    label.SetInput(view.name.replace("_", " ").upper())
    label.SetPosition(18, 16)
    text_property = label.GetTextProperty()
    text_property.SetFontSize(24)
    text_property.SetBold(True)
    text_property.SetColor((0.08, 0.08, 0.08) if view.silhouette else (0.94, 0.95, 0.97))
    renderer.AddActor2D(label)

    direction = normalized(view.direction)
    view_angle = 24.0
    if view.perspective:
        distance = max(
            (diagonal * 0.5 * 1.18) / math.tan(math.radians(view_angle / 2.0)),
            1.0,
        )
    else:
        distance = max(diagonal * 3.2, 1.0)
    camera = renderer.GetActiveCamera()
    camera.SetFocalPoint(*center)
    camera.SetPosition(*(center[index] + direction[index] * distance for index in range(3)))
    camera.SetViewUp(*view.view_up)
    if view.perspective:
        camera.ParallelProjectionOff()
        camera.SetViewAngle(view_angle)
    else:
        camera.ParallelProjectionOn()
        camera.SetParallelScale(max(diagonal * 0.56, 1.0))
    renderer.ResetCameraClippingRange()


def save_window(window, path: Path) -> None:
    from vtkmodules.vtkIOImage import vtkPNGWriter
    from vtkmodules.vtkRenderingCore import vtkWindowToImageFilter

    window.Render()
    capture = vtkWindowToImageFilter()
    capture.SetInput(window)
    capture.SetInputBufferTypeToRGB()
    capture.ReadFrontBufferOff()
    capture.Update()
    writer = vtkPNGWriter()
    writer.SetFileName(str(path))
    writer.SetInputConnection(capture.GetOutputPort())
    writer.Write()


def make_window(width: int, height: int):
    # These imports register the interaction and OpenGL implementations.
    import vtkmodules.vtkInteractionStyle  # noqa: F401
    import vtkmodules.vtkRenderingFreeType  # noqa: F401
    import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
    from vtkmodules.vtkRenderingCore import vtkRenderWindow

    window = vtkRenderWindow()
    window.SetWindowName("AI CAD visual review")
    window.SetSize(width, height)
    window.SetMultiSamples(8)
    window.SetOffScreenRendering(1)
    return window


def render_individual_views(polydata, bounds: tuple[float, ...], output_dir: Path) -> None:
    from vtkmodules.vtkRenderingCore import vtkRenderer

    for view in VIEWS:
        window = make_window(900, 900)
        renderer = vtkRenderer()
        window.AddRenderer(renderer)
        add_review_scene(renderer, polydata, view, bounds)
        save_window(window, output_dir / f"{view.name}.png")
        window.Finalize()


def render_contact_sheet(polydata, bounds: tuple[float, ...], output_path: Path) -> None:
    from vtkmodules.vtkRenderingCore import vtkRenderer

    columns = 3
    rows = 3
    window = make_window(2100, 2100)
    for index, view in enumerate(VIEWS):
        row = rows - 1 - index // columns
        column = index % columns
        renderer = vtkRenderer()
        renderer.SetViewport(
            column / columns,
            row / rows,
            (column + 1) / columns,
            (row + 1) / rows,
        )
        window.AddRenderer(renderer)
        add_review_scene(renderer, polydata, view, bounds)
    save_window(window, output_path)
    window.Finalize()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("design", help="Directory name under designs/")
    args = parser.parse_args()

    stl_path = REPOSITORY_ROOT / "output" / args.design / "part.stl"
    if not stl_path.is_file():
        raise FileNotFoundError(
            f"STL not found: {stl_path}. Build it first with "
            f"'uv run python scripts/build.py {args.design}'."
        )

    from vtkmodules.vtkIOGeometry import vtkSTLReader

    reader = vtkSTLReader()
    reader.SetFileName(str(stl_path))
    reader.Update()
    polydata = reader.GetOutput()
    if polydata.GetNumberOfPoints() == 0:
        raise ValueError(f"No mesh geometry read from {stl_path}")

    bounds = polydata.GetBounds()
    render_dir = stl_path.parent / "renders"
    render_dir.mkdir(parents=True, exist_ok=True)
    render_individual_views(polydata, bounds, render_dir)
    contact_sheet = render_dir / "contact_sheet.png"
    render_contact_sheet(polydata, bounds, contact_sheet)

    print(f"Rendered: {args.design}")
    print(f"Views: {len(VIEWS)} individual PNGs")
    print(f"Contact sheet: {contact_sheet}")


if __name__ == "__main__":
    main()
