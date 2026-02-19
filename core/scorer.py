from rapidfuzz import process, fuzz
import pandas as pd


def score_items(items, catalog, threshold=75):

    product_list = catalog["norm"].tolist()
    results = []

    for item in items:

        match, score, _ = process.extractOne(
            item,
            product_list,
            scorer=fuzz.ratio
        )

        if score >= threshold:

            row = catalog[catalog["norm"] == match].iloc[0]

            results.append({
                "item_detected": item,
                "matched_product": match,
                "confidence": score,
                "impact_score": int(row["impact_score"]),
                "category": row["category"],
                "greener_alternative": row["greener_alternative"],
                "impact_reason": row["impact_reason"],
                "alternative_reason": row["alternative_reason"]
            })

        else:
            results.append({
                "item_detected": item,
                "matched_product": "UNKNOWN",
                "confidence": score,
                "impact_score": 5,
                "category": "Unknown",
                "greener_alternative": "Research alternatives",
                "impact_reason": "Environmental impact data not available.",
                "alternative_reason": "Consider researching sustainable alternatives."
            })

    return results


def summarize_results(results):
    df = pd.DataFrame(results)

    if df.empty:
        return df, 0, 0

    avg_score = round(df["impact_score"].mean(), 2)
    high_impact = len(df[df["impact_score"] >= 7])

    return df, avg_score, high_impact
