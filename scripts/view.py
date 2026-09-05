#!/usr/bin/env python3
"""Open an STL file in a basic interactive VTK viewer."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stl", type=Path, help="Path to an STL file")
    args = parser.parse_args()
    if not args.stl.is_file():
        raise FileNotFoundError(f"STL not found: {args.stl}")

    from vtkmodules.vtkIOGeometry import vtkSTLReader
    # Importing the backend registers the graphical X/OpenGL render window.
    # Without it, VTK can construct a non-graphical base window that exits at once.
    import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
    from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkRenderer, vtkRenderWindow, vtkRenderWindowInteractor

    reader = vtkSTLReader()
    reader.SetFileName(str(args.stl))
    reader.Update()
    if reader.GetOutput().GetNumberOfPoints() == 0:
        raise ValueError(f"No mesh geometry read from {args.stl}")

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(0.82, 0.53, 0.19)

    renderer = vtkRenderer()
    renderer.SetBackground(0.12, 0.14, 0.18)
    renderer.AddActor(actor)
    window = vtkRenderWindow()
    window.SetWindowName(f"AI CAD — {args.stl.name}")
    window.SetSize(1000, 800)
    window.AddRenderer(renderer)
    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    renderer.ResetCamera()
    window.Render()
    interactor.Initialize()
    print(f"Opening STL viewer: {args.stl.resolve()}")
    print("Controls: drag to rotate; mouse wheel to zoom; shift-drag to pan. Close the window to exit.")
    interactor.Start()


if __name__ == "__main__":
    main()
