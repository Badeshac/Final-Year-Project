from typing import Callable, Sequence, Union

import cv2
import numpy as np


def adapt_to_dims(f: Callable) -> Callable:
    """
    Many bbox and polygon utilities should be able to work with a single input
    (1D) or with multiple (2D). Using this decorator we can make 1D inputs
    2D then flatten the result before returning it.
    The decorated function should take bboxes/polys as the first argument and
    must also return bboxes/polys.
    """

    def wrapper(*args, **kwargs):
        inp, args = args[0], args[1:]
        is_1d = False
        if len(inp.shape) == 1:
            is_1d = True
            inp = np.expand_dims(inp, axis=0)
        out = f(inp, *args, **kwargs)
        if is_1d:
            out = out.flatten()
        return out

    return wrapper


def resize_longest_edge(
    img: np.ndarray,
    length: int,
    interpolation: Union[int, str] = cv2.INTER_LINEAR,
    min_factor=np.float("-inf"),
    max_factor=np.float("inf"),
):
    """
    Resize image with locked aspect ratio such that its longest side is `length`
    pixels long BUT we keep into account min factor and max factor.
    `interpolation` specifies the cv2 interpolation type and defaults to
    cv2.INTER_LINERAR It may be specified as 'auto' in which case either
    cv2.INTER_AREA or cv2.INTERCUBIC is used depnding on whether we are
    downsizing or upsizing (respectively)
    """
    f = length / np.max(img.shape[:2])
    f = min(max_factor, f)
    f = max(min_factor, f)
    if isinstance(interpolation, str):
        assert (
            interpolation == "auto"
        ), "If `interpolation` is a str it can only be 'auto'"
        interpolation = cv2.INTER_AREA if f < 1 else cv2.INTER_CUBIC
    return cv2.resize(img, (0, 0), fx=f, fy=f, interpolation=interpolation)


@adapt_to_dims
def poly_abs_to_norm(
    polys: np.ndarray, img_shape: Sequence, inplace: bool = False
) -> np.ndarray:
    """
    Convert from absolute polygons (coordinate measured in array indices)
     to normalised polygons (all coordinates in [0, 1] normalised to image
     dimensions)
    Works on 1D and 2D inputs
    """
    if not inplace:
        polys = polys.astype(float)
    else:
        assert "int" not in polys.dtype, (
            "Input array is an int type. Output"
            + " needs to be a float type but you have set `inplace` to `True`"
        )
    polys[:, 0::2] /= img_shape[1]
    polys[:, 1::2] /= img_shape[0]
    return polys


@adapt_to_dims
def poly_norm_to_abs(
    polys: np.ndarray, img_shape: Sequence, inplace: bool = False
) -> np.ndarray:
    """
    Convert from normalised polygons (all coordinates in [0, 1] normalised
    to image dimensions) to absolute polygons
    Works on 1D and 2D inputs
    """
    if not inplace:
        polys = polys.copy()
    polys[:, 0::2] *= img_shape[1]
    polys[:, 1::2] *= img_shape[0]
    return polys


def resize_to_area(
    img: np.ndarray,
    area: int,
    interpolation=cv2.INTER_LINEAR,
    min_factor=np.float("-inf"),
    max_factor=np.float("inf"),
) -> np.ndarray:
    """
    resize an image such that:
     - aspect ratio is maintained
     - the area ~ `area` but we keep into account min factor and max factor
    `interpolation` specifies the cv2 interpolation type and defaults to
    cv2.INTER_LINEAR. It may be specified as 'auto' in which case either
    cv2.INTER_AREA or cv2.INTERCUBIC is used depnding on whether we are
    downsizing or upsizing (respectively)
    """
    original_area = np.prod(img.shape[:2])
    f = np.sqrt(area / original_area)
    f = min(max_factor, f)
    f = max(min_factor, f)
    if isinstance(interpolation, str):
        assert (
            interpolation == "auto"
        ), "If `interpolation` is a str it can only be 'auto'"
        interpolation = cv2.INTER_AREA if f < 1 else cv2.INTER_CUBIC
    return cv2.resize(img, (0, 0), fx=f, fy=f, interpolation=interpolation)


# Taken from
# https://github.com/open-mmlab/mmocr/blob/b8f7ead74cb0200ad5c422e82724ca6b2eb1c543/mmocr/datasets/pipelines/box_utils.py
def sort_vertices(vertices: np.ndarray, direction: str = "clockwise"):
    """
    Sort (N, 2) array of N vertices with xy coords such that the top-left
    vertex is first, and they are in clockwise or counter-clockwise order
    """
    valid_directions = ["clockwise", "counter-clockwise"]
    assert (
        direction in valid_directions
    ), f"`direction` not in valid directions: {', '.join(valid_directions)}"

    assert vertices.ndim == 2
    assert vertices.shape[-1] == 2
    N = vertices.shape[0]
    if N == 0:
        return vertices

    # Sort vertices in clockwise order starting from 3 o'clock about the
    # centroid
    centroid = np.mean(vertices, axis=0)
    directions = vertices - centroid
    angles = np.arctan2(directions[:, 1], directions[:, 0])
    sort_idx = np.argsort(-angles)
    if direction == "counter-clockwise":
        sort_idx = sort_idx[::-1]
    vertices = vertices[sort_idx]

    # Find the top left (closest to an axis-aligned bounding box top-left point)
    left_top = np.min(vertices, axis=0)
    # Rotate vertex indices such that the first is the top-left one
    dists = np.linalg.norm(left_top - vertices, axis=-1, ord=2)
    topleft_ix = np.argmin(dists)
    indices = (np.arange(N, dtype=np.int) + topleft_ix) % N
    return vertices[indices]


def _draw_outlines(
    outline_type: str,
    img: np.ndarray,
    outlines: Sequence[np.ndarray],
    thickness: int = 2,
    colors: Sequence[Sequence[int]] = [(0, 255, 0)],
    labels: Sequence[str] = [],
    label_font_size: float = 1.0,
) -> np.ndarray:
    """
    Draw either axis-aligned boxes (`outline_type == 'aab'`) or polygons
    (`outline_type == 'poly'`). The boxes would be expected in xyxy format and
    the polygons would be expected in xy... format.
    Both are expected to be in absolute co-ordinates relative to the image and
    with int dtype.
    `colors` may be a single color tuple, or a list of tuples, one for each
    outline
    """
    # Handle single color tuple of colors
    if len(colors) == 1 and len(outlines) > 1:
        colors = colors * len(outlines)
    if len(colors) == 3 and isinstance(colors[0], int):
        colors = [colors] * len(outlines)
    for i, (color, outline) in enumerate(zip(colors, outlines)):
        if outline_type == "poly":
            # Sort vertices is just for making sure the label is on the top left
            if len(labels):
                outline = sort_vertices(outline.reshape(-1, 2)).flatten()
            cv2.polylines(
                img,
                [outline.reshape(-1, 1, 2)],
                isClosed=True,
                color=color,
                thickness=thickness,
            )
        elif outline_type == "aab":
            cv2.rectangle(
                img,
                (outline[0], outline[1]),
                (outline[2], outline[3]),
                color,
                thickness=thickness,
            )
        if len(labels):
            label = f"{i:02d}" if len(labels) == 0 else labels[i]
            cv2.putText(
                img,
                label,
                (outline[0], outline[1] - 3),
                cv2.FONT_HERSHEY_SIMPLEX,
                label_font_size,
                color,
                thickness,
            )
    return img


def draw_polygons(
    img: np.ndarray,
    polys: Sequence[np.ndarray],
    thickness: int = 2,
    colors: Sequence[Sequence[int]] = [(0, 255, 0)],
    labeled: bool = False,
    labels: Sequence[str] = [],
    label_font_size: float = 1.0,
) -> np.ndarray:
    return _draw_outlines(
        "poly",
        img,
        polys,
        thickness=thickness,
        colors=colors,
        labels=labels,
        label_font_size=label_font_size,
    )
