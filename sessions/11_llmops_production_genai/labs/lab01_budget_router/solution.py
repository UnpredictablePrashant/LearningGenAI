#!/usr/bin/env python3
"""Lab 01: Budget Router (SOLUTION)"""


ROUTES = [
    {"name": "fast-small", "quality": 0.78, "p95_ms": 650, "cost": 0.002},
    {"name": "balanced", "quality": 0.86, "p95_ms": 1100, "cost": 0.007},
    {"name": "deep", "quality": 0.93, "p95_ms": 3200, "cost": 0.035},
]


REQUESTS = [
    {"id": "chat-autocomplete", "min_quality": 0.75, "max_p95_ms": 800, "max_cost": 0.005},
    {"id": "incident-triage", "min_quality": 0.85, "max_p95_ms": 1500, "max_cost": 0.010},
    {"id": "postmortem-draft", "min_quality": 0.90, "max_p95_ms": 5000, "max_cost": 0.050},
]


def route_fits(route: dict, request: dict) -> bool:
    return (
        route["quality"] >= request["min_quality"]
        and route["p95_ms"] <= request["max_p95_ms"]
        and route["cost"] <= request["max_cost"]
    )


def choose_route(routes: list[dict], request: dict) -> dict:
    candidates = [route for route in routes if route_fits(route, request)]
    if not candidates:
        return {"name": "human-review", "reason": "no route fits budgets"}
    return min(candidates, key=lambda route: route["cost"])


def retry_plan(route: dict) -> dict:
    if route["name"] == "human-review":
        return {"max_attempts": 0, "timeout_ms": None, "fallback": "manual_queue"}
    return {
        "max_attempts": 2,
        "timeout_ms": route["p95_ms"] * 2,
        "fallback": "human-review",
    }


def main() -> None:
    print("\nLab 01: Budget Router (Solution)\n")

    for request in REQUESTS:
        route = choose_route(ROUTES, request)
        print(f"{request['id']:<20} -> {route['name']:<12} retry={retry_plan(route)}")


if __name__ == "__main__":
    main()

