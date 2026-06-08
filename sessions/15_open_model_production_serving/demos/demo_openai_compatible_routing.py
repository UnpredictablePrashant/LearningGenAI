#!/usr/bin/env python3
"""Demo: route OpenAI-compatible clients by base URL."""


ROUTES = {
    "local-dev": {"base_url": "http://localhost:11434/v1", "model": "llama3.2"},
    "gpu-vllm": {"base_url": "https://models.internal/v1", "model": "team-7b-instruct"},
    "hosted": {"base_url": "https://api.openai.com/v1", "model": "gpt-4.1-mini"},
}


def main() -> None:
    print("\nDemo: OpenAI-Compatible Routing\n")
    for name, route in ROUTES.items():
        print(f"{name:<10} base_url={route['base_url']:<32} model={route['model']}")

    print("\nSame client shape, different endpoint. Always verify feature compatibility.")


if __name__ == "__main__":
    main()

