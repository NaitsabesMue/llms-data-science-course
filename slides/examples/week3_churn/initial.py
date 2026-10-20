# Reviewed teaching example, not a captured API response.

import matplotlib.pyplot as plt
plt.rcParams.update({"font.size": 14})

def analyze(df):
    summary = df.groupby("contract_type", sort=False)["churn"].agg(
        n_customers="size", n_churn="sum").reset_index()
    summary["churn_rate"] = summary["n_churn"] / summary["n_customers"]
    print(summary.to_string(index=False, float_format="{:.3f}".format))
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(summary["contract_type"], summary["churn_rate"])
    ax.set(ylabel="Churn rate", ylim=(0, 1))
    ax.set_title("Churn by contract type")
    fig.tight_layout()
