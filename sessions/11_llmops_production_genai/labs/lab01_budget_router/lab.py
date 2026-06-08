#!/usr/bin/env python3
"""
Lab 01: Budget Router
=====================
Choose the cheapest model route that satisfies quality and latency budgets.

Run:
    python lab.py

When stuck: check solution.py
"""


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
    # TODO 1:
    # Return True if route satisfies min_quality, max_p95_ms, and max_cost.
    pass


def choose_route(routes: list[dict], request: dict) -> dict:
    # TODO 2:
    # Return the cheapest route that fits.
    # If no route fits, return a fallback dict:
    # {"name": "human-review", "reason": "no route fits budgets"}
    pass


def retry_plan(route: dict) -> dict:
    # TODO 3:
    # Return a retry plan:
    # - human-review gets max_attempts 0
    # - all other routes get max_attempts 2 and timeout_ms = route["p95_ms"] * 2
    pass


def main() -> None:
    print("\nLab 01: Budget Router\n")

    for request in REQUESTS:
        route = choose_route(ROUTES, request)
        if route is None:
            print("TODO 2 not complete: choose_route returned None.")
            return
        print(f"{request['id']:<20} -> {route['name']:<12} retry={retry_plan(route)}")


if __name__ == "__main__":
    main()

