from __future__ import annotations

import sys
from typing import Optional

from pxr import Usd, UsdGeom, UsdRender, Sdf, Gf


def find_first_camera_path(stage: Usd.Stage) -> Optional[Sdf.Path]:
    """Return the path of the first camera found in the stage, or None."""
    for prim in stage.Traverse():
        if UsdGeom.Camera(prim):
            return prim.GetPath()
    return None


def ensure_render_product(stage: Usd.Stage, camera_path: Sdf.Path) -> None:
    """Create /Render/Product and /Render/Settings if missing, targeting camera_path."""
    # Ensure /Render scope exists
    if not stage.GetPrimAtPath(Sdf.Path("/Render")):
        stage.DefinePrim("/Render", "Scope")

    # Ensure RenderProduct
    rp_path = Sdf.Path("/Render/Product")
    rp = UsdRender.RenderProduct.Get(stage, rp_path)
    if not rp:
        rp = UsdRender.RenderProduct.Define(stage, rp_path)
        rp.CreateCameraRel().SetTargets([camera_path])
        rp.CreateResolutionAttr().Set(Gf.Vec2i(1920, 1080))
        rp.CreateProductNameAttr().Set("Capture.####.png")

    # Ensure RenderSettings referencing the product
    rs_path = Sdf.Path("/Render/Settings")
    rs = UsdRender.RenderSettings.Get(stage, rs_path)
    if not rs:
        rs = UsdRender.RenderSettings.Define(stage, rs_path)
        rs.CreateProductsRel().SetTargets([rp.GetPath()])


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: add_render_product.py <usd_or_usda_path>")
        return 2

    input_path = sys.argv[1]

    # Accept either filesystem path or already-prefixed file:/ URL
    if not input_path.startswith("file:/"):
        # Avoid f-string expression with backslashes (Python disallows backslashes inside {})
        stage_url = "file:/" + input_path.replace("\\", "/")
    else:
        stage_url = input_path

    stage = Usd.Stage.Open(stage_url)
    if not stage:
        print(f"ERROR: cannot open stage: {stage_url}")
        return 1

    camera_path = find_first_camera_path(stage)
    if camera_path is None:
        # Define a simple camera under /World if none exists
        cam = UsdGeom.Camera.Define(stage, Sdf.Path("/World/Camera1"))
        camera_path = cam.GetPath()

    ensure_render_product(stage, camera_path)

    stage.GetRootLayer().Save()

    print(f"OK: RenderProduct=/Render/Product camera={camera_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


