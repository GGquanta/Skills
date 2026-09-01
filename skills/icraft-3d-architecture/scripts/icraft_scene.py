#!/usr/bin/env python3
"""iCraft 场景 JSON 小工具：元素工厂 + 闭合校验。

Agent 生成架构图时：
1. 复制本文件到任务目录，或直接 import。
2. 用 area() / model() / text_label() / line() 拼 scene 列表。
3. 调用 validate(scene) ，通过后再 dumps。

坐标：x 左右，z 前后，y 向上。连线 y 用 Y_LINE，文字 y 用 Y_TEXT。
"""
from __future__ import annotations

import json
from typing import Any

Y_LINE = 0.22
Y_TEXT = 0.21
Y_AREA = 0.0
FONT = "AlibabaPuHuiTi"


def _text_base(
    key: str,
    name: str,
    text: str,
    x: float,
    z: float,
    *,
    font_size: float,
    align: str,
    anchor_x: str,
    anchor_y: str,
    max_w: float,
) -> dict[str, Any]:
    return {
        "key": key,
        "type": "text",
        "options": {
            "name": name,
            "text": text,
            "color": "#000000",
            "fontSize": font_size,
            "outlineColor": "#ffffff",
            "lineHeight": 1.5,
            "outlineWidth": 0.02,
            "textAlign": align,
            "font": FONT,
            "weight": "Bold",
            "anchorX": anchor_x,
            "anchorY": anchor_y,
            "scale": 1,
            "whiteSpace": "normal",
            "overflowWrap": "break-word",
            "backgroundEnabled": False,
            "backgroundColor": "#ffffff",
            "backgroundRadius": 0,
            "backgroundShowBorder": False,
            "backgroundBorderColor": "#000000",
            "backgroundBorderDash": 0,
            "backgroundBorderWidth": 0.01,
            "backgroundOpacity": 1,
            "padding": 0.1,
            "tipLineColor": "#000000",
            "tipOpacity": 1,
            "key": key,
            "x": x,
            "y": Y_TEXT,
            "z": z,
            "maxWidth": max_w,
            "maxHeight": 0.5,
        },
    }


def area(
    key: str,
    name: str,
    x: float,
    z: float,
    w: float,
    length: float,
    color: str,
    border: str,
    text_key: str,
    title: str,
    title_x: float,
    title_z: float,
    max_w: float,
) -> list[dict[str, Any]]:
    """分区台面 + 左上角标题。x,z 为台面中心。"""
    return [
        {
            "key": key,
            "type": "area",
            "options": {
                "name": name,
                "width": w,
                "height": 0.19,
                "length": length,
                "radius": 0.3,
                "color": color,
                "materialType": "clay",
                "opacity": 0.7,
                "showBorder": True,
                "borderColor": border,
                "borderWidth": 0.02,
                "borderDash": False,
                "receiveShadow": True,
                "scale": 1,
                "tipLineColor": "#000000",
                "tipOpacity": 1,
                "key": key,
                "x": x,
                "y": Y_AREA,
                "z": z,
                "castShadow": True,
                "tipShow": False,
                "tipHeight": 1.6,
                "tipBackgroundColor": "#ffffff",
            },
        },
        _text_base(
            text_key,
            name,
            title,
            title_x,
            title_z,
            font_size=0.26,
            align="left",
            anchor_x="left",
            anchor_y="top",
            max_w=max_w,
        ),
    ]


def model(
    key: str,
    name: str,
    glb: str,
    x: float,
    y: float,
    z: float,
    colors: list[str],
    links: list[str],
    *,
    scale: float = 1,
    text_key: str | None = None,
    label: str | None = None,
    max_w: float = 1.2,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = [
        {
            "key": key,
            "type": "model",
            "options": {
                "name": name,
                "type": glb,
                "scale": scale,
                "tipShow": True,
                "tipHeight": 1.6,
                "tipBackgroundColor": "#ffffff",
                "materialType": "base",
                "opacity": 1,
                "castShadow": True,
                "receiveShadow": True,
                "tipLineColor": "#000000",
                "tipOpacity": 1,
                "key": key,
                "x": x,
                "y": y,
                "z": z,
                "linkLineKeys": links,
                "color": colors,
                "rotateX": 0,
                "rotateY": 0,
                "rotateZ": 0,
            },
        }
    ]
    if text_key:
        items.append(
            _text_base(
                text_key,
                name,
                label or name,
                x,
                z + 0.62,
                font_size=0.22,
                align="center",
                anchor_x="center",
                anchor_y="middle",
                max_w=max_w,
            )
        )
    return items


def line(
    key: str,
    points: list[float],
    start: str,
    end: str,
    *,
    show_arrow: bool = True,
    dashed: bool = False,
) -> dict[str, Any]:
    if len(points) < 6 or len(points) % 3 != 0:
        raise ValueError(f"{key}: points 必须是 3 的倍数且至少两个顶点")
    xs, ys, zs = points[0::3], points[1::3], points[2::3]
    return {
        "key": key,
        "type": "line",
        "options": {
            "name": "Line",
            "showArrow": show_arrow,
            "arrowSize": 0.8,
            "arrowPositionPercent": 0.72,
            "color": "#000000",
            "doubleArrow": False,
            "linewidth": 0.05,
            "dashed": dashed,
            "dashScale": 1,
            "opacity": 1,
            "routingMode": "normal",
            "tipLineColor": "#000000",
            "tipOpacity": 1,
            "key": key,
            "points": points,
            "startElementKey": start,
            "endElementKey": end,
            "x": sum(xs) / len(xs),
            "y": sum(ys) / len(ys),
            "z": sum(zs) / len(zs),
        },
    }


def default_light(key: str = "default-light") -> dict[str, Any]:
    return {
        "key": key,
        "type": "directionallight",
        "options": {
            "color": "#ffffff",
            "intensity": 3.5,
            "castShadow": True,
            "name": "平行光",
            "rotateX": -48,
            "y": 16,
            "shadowResolution": "high",
            "shadowSize": 48,
            "tipLineColor": "#000000",
            "tipOpacity": 1,
            "rotateY": -51,
            "rotateZ": -9,
            "defaultLight": True,
            "x": -15,
            "z": 10,
            "key": key,
        },
    }


def validate(scene: list[dict[str, Any]]) -> list[str]:
    """返回错误列表；空列表表示通过。"""
    errors: list[str] = []
    keys = [el.get("key") for el in scene]
    if len(keys) != len(set(keys)):
        errors.append("存在重复 key")
    by_key = {el["key"]: el for el in scene if "key" in el}
    models = {el["key"] for el in scene if el.get("type") == "model"}
    lines = {el["key"]: el for el in scene if el.get("type") == "line"}

    for el in scene:
        opt = el.get("options") or {}
        if opt.get("key") and opt["key"] != el.get("key"):
            errors.append(f"{el.get('key')}: options.key 与外层不一致")

    for mid in models:
        for lk in by_key[mid]["options"].get("linkLineKeys") or []:
            if lk not in lines:
                errors.append(f"{mid}: linkLineKeys 引用了不存在的线 {lk}")
            else:
                ends = (
                    lines[lk]["options"].get("startElementKey"),
                    lines[lk]["options"].get("endElementKey"),
                )
                if mid not in ends:
                    errors.append(f"{mid}: 列出了线 {lk}，但该线端点不是该模型")

    for lid, lel in lines.items():
        opt = lel["options"]
        pts = opt.get("points") or []
        if len(pts) < 6 or len(pts) % 3 != 0:
            errors.append(f"{lid}: points 非法")
        for end_name in ("startElementKey", "endElementKey"):
            ek = opt.get(end_name)
            if ek not in models:
                errors.append(f"{lid}: {end_name}={ek} 不是 model")
            elif lid not in (by_key[ek]["options"].get("linkLineKeys") or []):
                errors.append(f"{lid}: 端点 {ek} 的 linkLineKeys 未包含该线")
    return errors


def dumps(scene: list[dict[str, Any]], path: str) -> None:
    errs = validate(scene)
    if errs:
        raise SystemExit("校验失败:\n" + "\n".join(errs))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(scene, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"wrote {path} ({len(scene)} elements)")
