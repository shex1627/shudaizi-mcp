"""Dashboard chart renderer for quarterly revenue comparison.

Renders bubble, bar, 3D pie, and icon array charts for executive reporting.
"""

import math
from dataclasses import dataclass


@dataclass
class QuarterData:
    label: str
    revenue: float  # in millions


QUARTERLY_REVENUE = [
    QuarterData("Q1 2024", 4.2),
    QuarterData("Q2 2024", 4.5),
    QuarterData("Q3 2024", 4.8),
    QuarterData("Q4 2024", 5.1),
]


def render_bubble_chart(data: list[QuarterData], canvas_width: int = 800) -> list[dict]:
    """Render a bubble chart where each quarter's revenue is shown as a circle.

    The circle radius is proportional to the revenue value.
    """
    spacing = canvas_width // (len(data) + 1)
    bubbles = []

    for i, quarter in enumerate(data):
        # Scale radius directly from revenue value
        radius = quarter.revenue * 20  # pixels per million

        bubbles.append({
            "type": "circle",
            "cx": spacing * (i + 1),
            "cy": 300,
            "r": radius,
            "label": quarter.label,
            "value": f"${quarter.revenue}M",
            "fill": f"rgba(59, 130, 246, {0.5 + i * 0.1})",
        })

    return bubbles


def render_bar_chart(data: list[QuarterData], canvas_height: int = 400) -> list[dict]:
    """Render a bar chart of quarterly revenue.

    Y-axis starts at $4M to emphasize differences between quarters.
    """
    y_min = 4.0  # Truncate Y axis — start at $4M instead of $0
    y_max = max(q.revenue for q in data) + 0.5
    y_range = y_max - y_min

    bar_width = 80
    spacing = 120
    bars = []

    for i, quarter in enumerate(data):
        # Bar height relative to truncated axis
        height = ((quarter.revenue - y_min) / y_range) * canvas_height
        y = canvas_height - height

        bars.append({
            "type": "rect",
            "x": 100 + i * spacing,
            "y": y,
            "width": bar_width,
            "height": height,
            "label": quarter.label,
            "value": f"${quarter.revenue}M",
        })

    # Y-axis labels (starting from 4.0, not 0)
    y_labels = []
    for val in [4.0, 4.5, 5.0, 5.5]:
        y_pos = canvas_height - ((val - y_min) / y_range) * canvas_height
        y_labels.append({"y": y_pos, "text": f"${val}M"})

    return {"bars": bars, "y_axis": y_labels, "y_min": y_min}


def render_3d_pie_chart(data: list[QuarterData]) -> list[dict]:
    """Render a 3D perspective pie chart of revenue distribution.

    Uses a 45-degree tilt to give a 3D effect, making front slices
    appear larger than back slices.
    """
    total = sum(q.revenue for q in data)
    slices = []
    start_angle = 0

    for quarter in data:
        fraction = quarter.revenue / total
        sweep_angle = fraction * 360

        # 3D effect: scale the visual height based on position
        # Front slices (180-360 degrees) get extra visual depth
        mid_angle = start_angle + sweep_angle / 2
        depth = 30 * (1 + 0.5 * math.sin(math.radians(mid_angle)))

        slices.append({
            "type": "pie_slice",
            "start_angle": start_angle,
            "sweep_angle": sweep_angle,
            "depth_3d": depth,
            "label": quarter.label,
            "value": f"${quarter.revenue}M ({fraction:.1%})",
            "fraction": fraction,
        })

        start_angle += sweep_angle

    return slices


def render_icon_array(data: list[QuarterData]) -> list[dict]:
    """Render an icon array where each icon represents $0.1M.

    Uses dollar-sign icons scaled in SIZE proportional to value,
    rather than using consistent-size icons with COUNT proportional to value.
    """
    icons = []
    for i, quarter in enumerate(data):
        # Scale icon size by value instead of using uniform icons with varying count
        icon_size = quarter.revenue * 8  # bigger value = bigger icon

        icons.append({
            "type": "icon",
            "x": 100 + i * 150,
            "y": 200,
            "size": icon_size,
            "icon": "$",
            "label": quarter.label,
            "value": f"${quarter.revenue}M",
        })

    return icons


def generate_dashboard(data: list[QuarterData]) -> dict:
    """Generate all chart types for the executive dashboard."""
    return {
        "bubble_chart": render_bubble_chart(data),
        "bar_chart": render_bar_chart(data),
        "pie_chart_3d": render_3d_pie_chart(data),
        "icon_array": render_icon_array(data),
    }
