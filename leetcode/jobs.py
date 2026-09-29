"""Weighted interval scheduling (strict input format).

This module implements the solution for the problem as stated: input must be
exactly the following format.

Input:
- First line: integer `n` (number of jobs).
- Next `3*n` lines: for each job 3 lines in order:
		1) `start_time` as HHMM (e.g. 0900)
		2) `end_time` as HHMM (e.g. 1730)
		3) `profit` as integer

Output:
- Two integers separated by a space: `remaining_jobs remaining_profit`.

The algorithm: sort jobs by end time, compute with binary search for each job
the previous non-overlapping job, then run DP to maximize profit. We also
track the count of chosen jobs so we can compute how many jobs remain.
"""

import sys
from bisect import bisect_right


def parse_time(hhmm: str) -> int:
	"""Convert HHMM string to minutes since midnight.

	Examples:
	- '0900' -> 9*60 + 0 = 540
	- '1330' -> 13*60 + 30 = 810
	"""
	t = int(hhmm)
	h = t // 100
	m = t % 100
	return h * 60 + m


def solve(lines: list[str]) -> str:
	"""Parse input lines (strict 3*n format) and return the output string.

	This function assumes the caller provides the full input (read from stdin)
	as `lines`. It enforces the exact format described in the problem: after
	the first line containing `n`, there must be exactly `3*n` lines describing
	the jobs. If the input does not match this format, the behavior is to
	return "0 0".
	"""

	# Expect at least one line (n)
	if not lines:
		return "0 0"

	first = lines[0].strip()
	if not first:
		return "0 0"

	n_jobs = int(first)
	rest = [line.strip() for line in lines[1:]]

	# Enforce exact 3*n lines for jobs
	if len(rest) < 3 * n_jobs:
		return "0 0"

	jobs = []
	for i in range(n_jobs):
		s = rest[3 * i]
		e = rest[3 * i + 1]
		p = rest[3 * i + 2]
		jobs.append((parse_time(s), parse_time(e), int(p)))

	total_jobs = len(jobs)
	total_profit = sum(p for _, _, p in jobs)

	# --- Weighted interval scheduling core ---
	# Sort jobs by their end time (required for the DP/BinarySearch method)
	jobs.sort(key=lambda x: x[1])
	ends = [job[1] for job in jobs]  # list of end times (in minutes)
	n = len(jobs)

	# p[i] = index of the rightmost job that finishes <= jobs[i].start,
	# or -1 if none. We compute this with binary search on `ends`.
	p = [-1] * n
	for i in range(n):
		s_i = jobs[i][0]
		j = bisect_right(ends, s_i) - 1
		p[i] = j

	# dp_profit[i] = maximum profit considering jobs[0..i]
	# dp_count[i]  = number of jobs chosen in that optimal selection
	dp_profit = [0] * n
	dp_count = [0] * n

	for i in range(n):
		profit_i = jobs[i][2]
		# profit and count if we include jobs[i]
		incl_profit = profit_i + (dp_profit[p[i]] if p[i] != -1 else 0)
		incl_count = 1 + (dp_count[p[i]] if p[i] != -1 else 0)

		if i == 0:
			# base case: choose the only option
			dp_profit[i] = incl_profit
			dp_count[i] = incl_count
		else:
			# option 1: exclude jobs[i] -> keep dp[i-1]
			excl_profit = dp_profit[i - 1]
			excl_count = dp_count[i - 1]

			# choose the option with higher profit; break ties by taking
			# the one that includes more jobs for Anirudh (arbitrary tie-break)
			if incl_profit > excl_profit:
				dp_profit[i] = incl_profit
				dp_count[i] = incl_count
			elif incl_profit < excl_profit:
				dp_profit[i] = excl_profit
				dp_count[i] = excl_count
			else:
				if incl_count >= excl_count:
					dp_profit[i] = incl_profit
					dp_count[i] = incl_count
				else:
					dp_profit[i] = excl_profit
					dp_count[i] = excl_count

	selected_profit = dp_profit[n - 1] if n > 0 else 0
	selected_jobs = dp_count[n - 1] if n > 0 else 0

	# remaining (for other employees) = totals - chosen_by_Anirudh
	remaining_jobs = total_jobs - selected_jobs
	remaining_profit = total_profit - selected_profit

	return f"{remaining_jobs} {remaining_profit}"


if __name__ == '__main__':
	data = sys.stdin.read().strip().splitlines()
	print(solve(data))

