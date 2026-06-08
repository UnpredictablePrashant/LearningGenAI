#!/usr/bin/env python3
"""Demo: a realtime voice-style event stream."""


EVENTS = [
    ("audio.started", ""),
    ("transcript.delta", "check pay"),
    ("transcript.delta", "ment logs"),
    ("transcript.final", "check payment logs"),
    ("tool.requested", "read_logs(payment-api)"),
    ("response.delta", "I found a spike"),
    ("response.completed", "I found a spike in payment-api 503s."),
]


def main() -> None:
    print("\nDemo: Realtime Event Flow\n")
    for event_type, payload in EVENTS:
        print(f"{event_type:<20} {payload}")


if __name__ == "__main__":
    main()

