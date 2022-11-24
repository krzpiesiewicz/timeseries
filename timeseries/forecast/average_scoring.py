import time
import sys

import numpy as np
import timeseries as tss

from timeseries.forecast.scorings import get_scoring
from timeseries.forecast.utils.timing import timedelta_str
from timeseries.forecast.utils.float_precision import value_precision_str

from timeseries.utils.init_structs import init_if_none


def average_scores(
        model,
        ts,
        score_intv,
        scorings,
        n_steps,
        n_steps_jump=1,
        trans=None,
        score_ts=None,
        original_ts=None,
        seasonal_ts_seq=None,
        return_preds=False,
        return_all_scores=False,
        precision=3,
        precision_big=1,
        mute=False,
        update_params=None
):
    update_params = init_if_none(update_params, dict)
    if trans is not None:
        assert original_ts is not None
    if score_ts is None:
        score_ts = original_ts if original_ts is not None else ts
    index = score_intv.view(score_ts).index
    all_scores = {scoring_name: [] for scoring_name in scorings}
    saved_preds = []

    i_range = range(0, index.size - n_steps, n_steps_jump)
    all_examples = len(i_range)
    past_examples = 0
    sum_of_scores = {scoring_name: 0 for scoring_name in scorings}

    def print_progress(start_time=None, last_time=None):
        buff = f"\r{past_examples}/{all_examples} – "
        for j, scoring_name in enumerate(scorings):
            mean_score = sum_of_scores[
                             scoring_name] / past_examples if past_examples > 0 else 0
            buff += f"{scoring_name}: {value_precision_str(mean_score, precision, precision_big)}, "
        if start_time is not None:
            buff += f"elapsed time: {timedelta_str(time.time() - start_time)}"
        if last_time is not None:
            buff += f" (last: {timedelta_str(time.time() - last_time)})"
        buff += " " * 6
        print(buff, end="", file=sys.stderr)

    if not mute:
        print_progress()
    start_time = time.time()
    for i in i_range:
        last_time = time.time()
        begin = index[i]
        end = index[i + n_steps]
        intv = tss.Interval(score_ts, begin, end)
        ts_true = intv.view(score_ts)
        ts_pred = model.predict(ts, intv, original_ts=original_ts, seasonal_ts_seq=seasonal_ts_seq)
        if trans is not None:
            ts_true = intv.view(score_ts)
            true_prevs = intv.prev_view(original_ts)
            ts_pred = trans.detransform(ts_pred, true_prevs)
        for scoring_name in scorings:
            scoring = get_scoring(scoring_name)
            score = scoring(ts_true, ts_pred)
            sum_of_scores[scoring_name] += score
            all_scores[scoring_name].append(score)
        if return_preds:
            saved_preds.append(ts_pred)
        if i + n_steps_jump < index.size:
            model.update(ts,
                         tss.Interval(ts, index[i], index[i + n_steps_jump]),
                         original_ts=original_ts,
                         seasonal_ts_seq=seasonal_ts_seq,
                         update_params=update_params)
        past_examples += 1
        if not mute:
            print_progress(start_time, last_time)
    if not mute:
        time.sleep(1)
    mean_scores = {
        scoring_name: np.mean(all_scores[scoring_name]) for scoring_name in
        scorings
    }
    if return_preds or return_all_scores:
        res = (mean_scores,)
        if return_all_scores:
            res += (all_scores,)
        if return_preds:
            res += (saved_preds,)
        return res
    else:
        return mean_scores


# def average_scores2(
#         model,
#         ts,
#         score_intv,
#         scorings,
#         n_steps,
#         n_steps_jump=1,
#         trans=None,
#         score_ts=None,
#         original_ts=None,
#         seasonal_ts_seq=None,
#         return_preds=False,
#         return_all_scores=False,
#         precision=3,
#         precision_big=1,
#         mute=False,
#         update_params={}
# ):
#     if trans is not None:
#         assert original_ts is not None
#     if score_ts is None:
#         score_ts = original_ts if original_ts is not None else ts
#     all_scores = {scoring_name: [] for scoring_name in scorings}
#     saved_preds = []
#
#     score_intervals = score_intv if type(score_intv) is list else [score_intv]
#     begin = np.min([intv.begin for intv in score_intervals])
#     end = np.min([intv.end for intv in score_intervals])
#     score_intv = tss.Interval(score_ts, begin, end)
#     index = score_intv.view().index
#     i_lst = []
#     i = 0
#     intv_i = score_intervals[0]
#     while i + n_steps <= index.size() and intv_i < score_intervals.size():
#         intv = score_intervals[intv_i]
#         if index[i + n_steps - 1] >= intv.end:
#             intv_i += 1
#         else:
#             if index[i] >= intv.begin:
#                 i_lst.append(i)
#             i += n_steps_jump
#
#     all_examples = len(i_lst)
#     past_examples = 0
#     sum_of_scores = {scoring_name: 0 for scoring_name in scorings}
#
#     def print_progress(start_time=None, last_time=None):
#         buff = f"\r{past_examples}/{all_examples} – "
#         for j, scoring_name in enumerate(scorings):
#             mean_score = sum_of_scores[
#                              scoring_name] / past_examples if past_examples > 0 else 0
#             buff += f"{scoring_name}: {value_precision_str(mean_score, precision, precision_big)}, "
#         if start_time is not None:
#             buff += f"elapsed time: {timedelta_str(time.time() - start_time)}"
#         if last_time is not None:
#             buff += f" (last: {timedelta_str(time.time() - last_time)})"
#         buff += " " * 6
#         print(buff, end="", file=sys.stderr)
#
#     if not mute:
#         print_progress()
#     start_time = time.time()
#     last_end = index[0]
#     for i in i_lst:
#         last_time = time.time()
#         begin = index[i]
#         end = index[i + n_steps]
#         intv = tss.Interval(score_ts, begin, end)
#         if last_end != begin:
#             model.update(ts,
#                          tss.Interval(ts, last_end, begin),
#                          original_ts=original_ts,
#                          seasonal_ts_seq=seasonal_ts_seq,
#                          update_params=update_params)
#         last_end = end
#         ts_true = intv.view(score_ts)
#         ts_pred = model.predict(ts, intv, original_ts=original_ts, seasonal_ts_seq=seasonal_ts_seq)
#         if trans is not None:
#             ts_true = intv.view(score_ts)
#             true_prevs = intv.prev_view(original_ts)
#             ts_pred = trans.detransform(ts_pred, true_prevs)
#         for scoring_name in scorings:
#             scoring = get_scoring(scoring_name)
#             score = scoring(ts_true, ts_pred)
#             sum_of_scores[scoring_name] += score
#             all_scores[scoring_name].append(score)
#         if return_preds:
#             saved_preds.append(ts_pred)
#         past_examples += 1
#         if not mute:
#             print_progress(start_time, last_time)
#     if not mute:
#         time.sleep(1)
#     mean_scores = {
#         scoring_name: np.mean(all_scores[scoring_name]) for scoring_name in
#         scorings
#     }
#     if return_preds or return_all_scores:
#         res = (mean_scores,)
#         if return_all_scores:
#             res += (all_scores,)
#         if return_preds:
#             res += (saved_preds,)
#         return res
#     else:
#         return mean_scores
#
