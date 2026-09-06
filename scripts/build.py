#!/usr/bin/env python3
"""Build, validate, and export a named CadQuery design."""

from __future__ import annotations

import argparse
import importlib.util
import shutil
import sys
from pathlib import Path

import cadquery as cq

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def nearly_equal(actual: float, expected: float, tolerance: float) -> bool:
    return abs(actual - expected) <= tolerance


def validate_test_plate(model: cq.Workplane, parameters) -> list[str]:
    """Validate known dimensions and the two through-holes of the baseline plate."""
    solid = model.val()
    if not solid.isValid():
        raise ValueError("CadQuery produced an invalid solid")
    solids = model.solids().vals()
    if len(solids) != parameters.EXPECTED_SOLID_COUNT:
        raise ValueError(f"Expected {parameters.EXPECTED_SOLID_COUNT} solid, found {len(solids)}")

    box = solid.BoundingBox()
    checks = {
        "X width": (box.xlen, parameters.WIDTH),
        "Y depth": (box.ylen, parameters.DEPTH),
        "Z thickness": (box.zlen, parameters.THICKNESS),
    }
    for name, (actual, expected) in checks.items():
        if not nearly_equal(actual, expected, parameters.DIMENSION_TOLERANCE):
            raise ValueError(f"{name} is {actual:.4f} mm; expected {expected:.4f} mm")

    cylindrical_faces = [face for face in solid.Faces() if face.geomType() == "CYLINDER"]
    holes = [
        face
        for face in cylindrical_faces
        if nearly_equal(face.BoundingBox().xlen, parameters.HOLE_DIAMETER, parameters.DIMENSION_TOLERANCE)
        and nearly_equal(face.BoundingBox().ylen, parameters.HOLE_DIAMETER, parameters.DIMENSION_TOLERANCE)
        and nearly_equal(face.BoundingBox().zlen, parameters.THICKNESS, parameters.DIMENSION_TOLERANCE)
    ]
    if len(holes) != 2:
        raise ValueError(f"Expected two {parameters.HOLE_DIAMETER:.2f} mm through-hole faces, found {len(holes)}")

    expected_positions = sorted((-parameters.HOLE_SPACING / 2.0, parameters.HOLE_SPACING / 2.0))
    actual_positions = sorted(face.Center().x for face in holes)
    for actual, expected in zip(actual_positions, expected_positions, strict=True):
        if not nearly_equal(actual, expected, parameters.DIMENSION_TOLERANCE):
            raise ValueError(f"Hole X position is {actual:.4f} mm; expected {expected:.4f} mm")

    return ["valid solid", "one solid", "outer dimensions", "two 5.00 mm through-holes at requested spacing"]


def validate_mini_delivery_bag(model: cq.Workplane, parameters) -> list[str]:
    """Validate the envelope and single-solid construction of the miniature bag."""
    solid = model.val()
    if not solid.isValid():
        raise ValueError("CadQuery produced an invalid solid")
    solids = model.solids().vals()
    if len(solids) != parameters.EXPECTED_SOLID_COUNT:
        raise ValueError(f"Expected {parameters.EXPECTED_SOLID_COUNT} solid, found {len(solids)}")

    box = solid.BoundingBox()
    checks = {
        "X width": (box.xlen, parameters.BODY_WIDTH),
        "Y finished depth": (box.ylen, parameters.EXPECTED_OVERALL_DEPTH),
        "Z finished height": (box.zlen, parameters.EXPECTED_OVERALL_HEIGHT),
    }
    for name, (actual, expected) in checks.items():
        if not nearly_equal(actual, expected, parameters.DIMENSION_TOLERANCE):
            raise ValueError(f"{name} is {actual:.4f} mm; expected {expected:.4f} mm")
    return ["valid solid", "one solid", "finished outer dimensions"]


def validate_aero_coffee_mug(model: cq.Workplane, parameters) -> list[str]:
    """Validate the finished envelope and one-piece construction of the mug."""
    solid = model.val()
    if not solid.isValid():
        raise ValueError("CadQuery produced an invalid solid")
    solids = model.solids().vals()
    if len(solids) != parameters.EXPECTED_SOLID_COUNT:
        raise ValueError(f"Expected {parameters.EXPECTED_SOLID_COUNT} solid, found {len(solids)}")

    box = solid.BoundingBox()
    checks = {
        "X finished width": (box.xlen, parameters.EXPECTED_OVERALL_WIDTH),
        "Y finished depth": (box.ylen, parameters.EXPECTED_OVERALL_DEPTH),
        "Z finished height": (box.zlen, parameters.EXPECTED_OVERALL_HEIGHT),
    }
    for name, (actual, expected) in checks.items():
        if not nearly_equal(actual, expected, parameters.DIMENSION_TOLERANCE):
            raise ValueError(f"{name} is {actual:.4f} mm; expected {expected:.4f} mm")
    return ["valid solid", "one solid", "finished outer dimensions"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("design", help="Directory name under designs/")
    args = parser.parse_args()

    design_dir = REPOSITORY_ROOT / "designs" / args.design
    part_path = design_dir / "part.py"
    parameters_path = design_dir / "parameters.py"
    if not part_path.is_file() or not parameters_path.is_file():
        raise FileNotFoundError(f"Design '{args.design}' needs part.py and parameters.py in {design_dir}")

    sys.path.insert(0, str(design_dir))
    part = load_module(part_path, f"{args.design}_part")
    parameters = load_module(parameters_path, f"{args.design}_parameters")
    model = part.build_model()
    if not isinstance(model, cq.Workplane):
        raise TypeError("build_model() must return a cadquery.Workplane")

    if args.design == "test_plate":
        results = validate_test_plate(model, parameters)
    elif args.design == "mini_delivery_bag":
        results = validate_mini_delivery_bag(model, parameters)
    elif args.design == "aero_coffee_mug":
        results = validate_aero_coffee_mug(model, parameters)
    else:
        solid = model.val()
        if not solid.isValid() or len(model.solids().vals()) != 1:
            raise ValueError("Model must contain exactly one valid solid")
        results = ["valid solid", "one solid"]

    output_dir = REPOSITORY_ROOT / "output" / args.design
    staging_dir = output_dir.with_name(f".{args.design}-staging")
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True)
    step_path = staging_dir / "part.step"
    stl_path = staging_dir / "part.stl"
    # Capture exact BREP dimensions before STL export.  The tessellation export
    # can slightly alter CadQuery's in-memory bounding-box cache.
    source_box = model.val().BoundingBox()
    cq.exporters.export(model, str(step_path))
    cq.exporters.export(model, str(stl_path), tolerance=0.05, angularTolerance=0.1)

    imported_step = cq.importers.importStep(str(step_path))
    imported_box = imported_step.val().BoundingBox()
    tolerance = getattr(parameters, "DIMENSION_TOLERANCE", 0.01)
    for axis in ("xlen", "ylen", "zlen"):
        if not nearly_equal(getattr(source_box, axis), getattr(imported_box, axis), tolerance):
            raise ValueError(f"STEP reimport changed {axis}")

    if output_dir.exists():
        shutil.rmtree(output_dir)
    staging_dir.rename(output_dir)

    print(f"Built: {args.design}")
    print("Checks: " + "; ".join(results) + "; STEP reimport dimensions")
    print("Bounding box:")
    print(f"  X: {source_box.xlen:.3f} mm")
    print(f"  Y: {source_box.ylen:.3f} mm")
    print(f"  Z: {source_box.zlen:.3f} mm")
    print(f"STEP: {output_dir / 'part.step'}")
    print(f"STL:  {output_dir / 'part.stl'}")


if __name__ == "__main__":
    main()
