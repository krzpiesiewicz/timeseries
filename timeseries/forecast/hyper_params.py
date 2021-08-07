import os
import sys
import numpy as np


def sorted_scores(scores):
    return sorted(scores, key=lambda t: t[0], reverse=False)


def grid_search_hyper_params(
        create_model,
        grid,
        ts,
        train_index,
        val_index,
        best=10,
        max_fails=20,
        scores=None,
        model_params={},
        fit_params={},
        score_params={},
):
    fails = 0
    if scores is None:
        scores = []
    best_score = np.inf
    best_valuation = None
    n = len(grid)
    print(f"0/{n}", end="")
    for i, hyper_params_values in enumerate(grid):
        if fails > max_fails:
            print(f"\nTerminating: more than {max_fails} fails")
            break
        try:
            old_stderr = sys.stderr
            sys.stderr = open(os.devnull, "w")
            model = create_model(**hyper_params_values, **model_params)
            model.fit(ts, train_index, **fit_params)
            score = model.score(ts, val_index, **score_params)
        except:
            score = np.inf
            fails += 1
        finally:
            sys.stderr.close()
            sys.stderr = old_stderr
        scores.append((score, hyper_params_values))
        if score < best_score:
            best_score = score
            best_valuation = hyper_params_values
        print(f"\r{i + 1}/{n}, best_score: {best_score}, valuation: "
              f"{best_valuation}", end="",)
    print("")
    scores = sorted_scores(scores)
    if best is None:
        return scores
    else:
        return scores[:best]


def make_grid(*args, **kwargs):
    if len(args) > 0:
        dct = args[0]
    else:
        dct = kwargs
    grid = []
    hyper_params_and_values = list(dct.items())

    def create_valuation(current, rest):
        if rest == []:
            grid.append(current.copy())
        else:
            param, values = rest[0]
            for value in values:
                current[param] = value
                create_valuation(current, rest[1:])

    create_valuation({}, hyper_params_and_values)

    return grid


def grid_from_values_sets(hyper_params, values_sets):
    grid = []
    for values in values_sets:
        assert len(values) == len(hyper_params)
        valuation = {}
        for param, value in zip(hyper_params, values):
            valuation[param] = value
        grid.append(valuation)
    return grid
