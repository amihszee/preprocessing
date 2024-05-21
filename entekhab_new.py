import pandas as pd
from itertools import product

def get_final_output(university_data, category_data, period_data):
    # Category table
    value_category = 3
    category_flat = [item for sublist in category_data for item in sublist]
    df_category = pd.DataFrame({"Category": category_flat, "Value": [value_category] * len(category_flat)})
    start_value_category = 3.25
    reduction_category = 0.25
    new_values_category = [start_value_category - i * reduction_category for i in range(len(df_category))]
    df_category["new_value"] = new_values_category
    vv_values_category = []
    for i, sublist in enumerate(category_data):
        vv_values_category.extend([10 - i] * len(sublist))
    df_category["vv"] = vv_values_category
    n_category = len(category_data) - 1
    zarib_coefficient_category = value_category ** (1 / n_category)
    zarib_values_category = [value_category / (zarib_coefficient_category ** i) for i in range(len(df_category))]
    df_category["zarib"] = zarib_values_category
    df_category["product"] = df_category["vv"] * df_category["new_value"] * df_category["Value"] * df_category["zarib"]

    # University table
    value_university = 3.5
    university_flat = [item for sublist in university_data for item in sublist]
    df_university = pd.DataFrame({"University": university_flat})
    df_university["value"] = value_university
    start_value_university = 3.25
    reduction_university = 0.25
    num_rows_university = len(df_university)
    df_university["new_value"] = [start_value_university - i * reduction_university for i in range(num_rows_university)]
    vv_values_university = []
    for item in university_flat:
        for i, sublist in enumerate(university_data):
            if item in sublist:
                vv_values_university.append(10 - i)
                break
    df_university["vv"] = vv_values_university
    df_university["product"] = df_university["value"] * df_university["new_value"] * df_university["vv"]

    # Period table
    value_period = 4
    period_flat = [item for sublist in period_data for item in sublist]
    df_period = pd.DataFrame({"University": period_flat})
    df_period["value"] = value_period
    start_value_period = 3.25
    reduction_period = 0.25
    num_rows_period = len(df_period)
    df_period["new_value"] = [start_value_period - i * reduction_period for i in range(num_rows_period)]
    vv_values_period = []
    for item in period_flat:
        for i, sublist in enumerate(period_data):
            if item in sublist:
                vv_values_period.append(10 - i)
                break
    df_period["vv"] = vv_values_period
    df_period["product"] = df_period["value"] * df_period["new_value"] * df_period["vv"]

    all_combinations = list(product(df_university.iterrows(), df_category.iterrows(), df_period.iterrows()))

    product_values = []
    for (index_u, row_u), (index_c, row_c), (index_p, row_p) in all_combinations:
        product_values.append(row_u["product"] * row_c["product"] * row_p["product"])

    df_result = pd.DataFrame({"University": [row_u["University"] for (_, row_u), _, _ in all_combinations],
                              "Category": [row_c["Category"] for _, (_, row_c), _ in all_combinations],
                              "Period": [row_p["University"] for _, _, (_, row_p) in all_combinations],
                              "Product": product_values})

    df_result = df_result.sort_values(by="Product", ascending=False)

    return df_result

# Test the function
university_data = [['sarif', 'Tehran', 'amirkabir'], 
                   ['kashan', 'alame', "hamedan"], 
                   ['beheshti', 'kharazmi'], 
                   ['khaje', 'mashhad']]

category_data = [["riazi", "omran", "eghtedas"], [], ["shimi", "pysics", "cs"], ["ce", "mech", "naft"]]

period_data = [["azad", "dolati"], [], [], ["shabane"], ["pardis", "gheire"], ["azad sh"], ["azad T"]]

output = get_final_output(university_data, category_data, period_data)
print(output)
