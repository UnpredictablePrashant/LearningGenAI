#!/usr/bin/env python3
"""
Demo: Model Basics Before Fine-Tuning
=====================================
Show weights, bias, logits, softmax, inference, and simple quantization with
small numbers.

No API key required. Uses Python standard library only.

Run:
    python demos/demo_model_basics.py
"""

from __future__ import annotations

import math


def linear_score(features: list[float], weights: list[float], bias: float) -> float:
    return sum(feature * weight for feature, weight in zip(features, weights)) + bias


def softmax(logits: dict[str, float]) -> dict[str, float]:
    max_logit = max(logits.values())
    exp_values = {label: math.exp(value - max_logit) for label, value in logits.items()}
    total = sum(exp_values.values())
    return {label: value / total for label, value in exp_values.items()}


def predict_ticket(features: list[float]) -> tuple[str, dict[str, float]]:
    """
    Toy classifier.

    Features:
    0: contains IAM/access words
    1: contains cost/billing words
    2: contains DB/RDS words
    """
    class_weights = {
        "security": [2.5, -0.5, 0.2],
        "billing": [-0.4, 2.2, -0.2],
        "database": [0.1, -0.2, 2.4],
    }
    class_biases = {"security": 0.1, "billing": 0.0, "database": -0.1}

    logits = {
        label: linear_score(features, weights, class_biases[label])
        for label, weights in class_weights.items()
    }
    probabilities = softmax(logits)
    prediction = max(probabilities, key=probabilities.get)
    return prediction, probabilities


def quantize_int8(values: list[float]) -> tuple[list[int], float]:
    max_abs = max(abs(value) for value in values) or 1.0
    scale = max_abs / 127
    quantized = [round(value / scale) for value in values]
    return quantized, scale


def dequantize_int8(values: list[int], scale: float) -> list[float]:
    return [value * scale for value in values]


def main() -> None:
    print("\nDemo: Model Basics Before Fine-Tuning\n")

    features = [1.0, 0.0, 0.0]
    prediction, probabilities = predict_ticket(features)
    print("Toy inference")
    print("Features: IAM/access=1, cost=0, database=0")
    print("Probabilities:")
    for label, probability in sorted(probabilities.items()):
        print(f"  {label}: {probability:.3f}")
    print("Prediction:", prediction)

    weights = [2.5, -0.5, 0.2]
    quantized, scale = quantize_int8(weights)
    restored = dequantize_int8(quantized, scale)

    print("\nSimple int8-style quantization")
    print("Original weights: ", [round(value, 4) for value in weights])
    print("Quantized int8:   ", quantized)
    print("Scale:            ", round(scale, 6))
    print("Restored weights: ", [round(value, 4) for value in restored])
    print("\nObservation: quantization stores smaller integers plus a scale, trading precision for memory.")


if __name__ == "__main__":
    main()

