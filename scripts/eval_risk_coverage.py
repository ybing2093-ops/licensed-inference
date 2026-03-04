import argparse
import json


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", type=str, required=True)
    ap.add_argument("--bins", type=int, default=10)
    args = ap.parse_args()

    rows = []
    with open(args.jsonl, "r", encoding="utf-8") as f:
        for line in f:
            rows.append(json.loads(line))

    oks = [r.get("ok", "na") for r in rows]
    if all(o == "na" for o in oks):
        print("All ok=na. Risk–Coverage not defined. Provide verifier-labeled ok∈{0,1}.")
        return

    # Sweep threshold on license_score
    labeled = [(float(r["license_score"]), int(r["ok"])) for r in rows if r.get("ok", "na") != "na"]
    labeled.sort(key=lambda x: x[0], reverse=True)

    total = len(labeled)
    cum_ok = 0
    cum_n = 0

    print("thr,coverage,risk")
    for thr in [i / args.bins for i in range(args.bins, -1, -1)]:
        # include all with score >= thr
        while cum_n < total and labeled[cum_n][0] >= thr:
            cum_ok += labeled[cum_n][1]
            cum_n += 1
        if cum_n == 0:
            continue
        coverage = cum_n / total
        risk = 1.0 - (cum_ok / cum_n)
        print(f"{thr:.3f},{coverage:.3f},{risk:.3f}")


if __name__ == "__main__":
    main()
