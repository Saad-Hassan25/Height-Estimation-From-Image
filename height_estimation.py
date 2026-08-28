"""Estimate a person's height from an image and a reference object.

The measurement uses a simple proportional model. Select the person and a
reference object in the same image; their real-world heights are related to
the heights of their bounding boxes in pixels.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import cv2
import numpy as np


@dataclass(frozen=True)
class BoundingBox:
    """A rectangular selection, represented in image pixels."""

    x: int
    y: int
    width: int
    height: int

    @classmethod
    def from_roi(cls, roi: Sequence[int | float]) -> "BoundingBox":
        """Create a box from OpenCV's ``selectROI`` return value."""
        x, y, width, height = (int(value) for value in roi)
        return cls(x=x, y=y, width=width, height=height)

    @property
    def is_valid(self) -> bool:
        """Whether the selection has a non-zero area."""
        return self.width > 0 and self.height > 0


def estimate_height(
    person_height_px: float,
    reference_height_px: float,
    reference_height_m: float,
) -> float:
    """Return the person's estimated height in metres.

    Both objects should be in the same plane (or at the same camera distance)
    to minimise perspective error.
    """
    if person_height_px <= 0:
        raise ValueError("Person height in pixels must be greater than zero.")
    if reference_height_px <= 0:
        raise ValueError("Reference height in pixels must be greater than zero.")
    if reference_height_m <= 0:
        raise ValueError("Reference height must be greater than zero.")

    return person_height_px * reference_height_m / reference_height_px


def _resize_for_display(image: np.ndarray, max_height: int = 900) -> tuple[np.ndarray, float]:
    """Resize only for easier ROI selection and return the display scale."""
    if image.shape[0] <= max_height:
        return image, 1.0
    scale = max_height / image.shape[0]
    return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA), scale


def _select_box(window_title: str, image: np.ndarray, prompt: str) -> BoundingBox:
    print(f"{prompt} Drag a rectangle and press Enter or Space to confirm; Esc cancels.")
    box = BoundingBox.from_roi(cv2.selectROI(window_title, image, showCrosshair=True))
    if not box.is_valid:
        raise ValueError("No selection was made.")
    return box


def _draw_box(image: np.ndarray, box: BoundingBox, colour: tuple[int, int, int], label: str) -> None:
    cv2.rectangle(image, (box.x, box.y), (box.x + box.width, box.y + box.height), colour, 2)
    cv2.putText(image, label, (box.x, max(24, box.y - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colour, 2)


def measure_interactively(image_path: Path, reference_height_m: float) -> float:
    """Open an image, collect two ROIs, display the annotation, and return metres."""
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    display_image, scale = _resize_for_display(image)
    window_title = "Height Estimation"
    try:
        person = _select_box(window_title, display_image, "Select the full person.")
        reference = _select_box(window_title, display_image, "Select the full reference object.")
        estimate_m = estimate_height(person.height / scale, reference.height / scale, reference_height_m)

        annotated = display_image.copy()
        _draw_box(annotated, person, (255, 120, 0), "Person")
        _draw_box(annotated, reference, (0, 200, 0), "Reference")
        label = f"Estimated height: {estimate_m:.2f} m ({estimate_m * 100:.0f} cm)"
        cv2.putText(annotated, label, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 3)
        cv2.putText(annotated, label, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 1)
        cv2.imshow("Height Estimation Result", annotated)
        print(label)
        print("Press any key in the image window to close it.")
        cv2.waitKey(0)
        return estimate_m
    finally:
        cv2.destroyAllWindows()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Estimate a person's height from an image and a known-height reference object."
    )
    parser.add_argument("image", type=Path, help="Path to a JPG, PNG, or other OpenCV-readable image.")
    parser.add_argument(
        "--reference-height",
        type=float,
        required=True,
        metavar="METRES",
        help="Known real-world height of the reference object, in metres.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        measure_interactively(args.image, args.reference_height)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
