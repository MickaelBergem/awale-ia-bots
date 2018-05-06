# Bots performance

## 1. RandomIA

Takes a random move each turn.

## 2. Naive1Bot

Strategy: `last-step-victory`.

This bot is **13% better** than the random bot.

    Running 20000 iterations of A (random) against B (last-step-victory)
    20000 iterations complete, scores=Counter({'B': 12648, 'A': 7352})
    Agent B (strategy=last-step-victory) won in 63.2% of the tests, performance is 13% better.
