"""Générateur aléatoire du moteur de combat.

Toute la simulation passe par une instance unique de :class:`CombatRNG`
afin qu'une bataille soit rejouable à l'identique avec la même graine.
"""
from __future__ import annotations

import math
import random


class CombatRNG:
    def __init__(self, seed: int | None = None):
        self.seed = seed
        self.random = random.Random(seed)

    def prob_round(self, x: float) -> int:
        """Arrondi probabiliste : floor(x) + Bernoulli(partie décimale).

        C'est l'arrondi utilisé par le jeu pour le nombre d'attaques et de
        défenses (§8.4) — surtout pas un arrondi classique.
        """
        if x <= 0:
            return 0
        base = math.floor(x)
        frac = x - base
        return base + (1 if self.random.random() < frac else 0)

    def die(self, faces: int) -> int:
        """Jet de dé uniforme 1..faces."""
        return self.random.randint(1, faces)

    def chance(self, probability: float) -> bool:
        """Vrai avec la probabilité donnée (0..1)."""
        return self.random.random() < probability

    def shuffle(self, seq: list) -> None:
        self.random.shuffle(seq)

    def choice(self, seq):
        return self.random.choice(seq)

    def weighted_choice(self, items: list, weights: list[float]):
        return self.random.choices(items, weights=weights, k=1)[0]
