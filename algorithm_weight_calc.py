#%%
def calculate_weighted_score(soft_tags, NPS, distance, w1, w2, w3):
    if all(value == 0 for value in [soft_tags, NPS, distance]) or all(weight == 0 for weight in [w1, w2, w3]):
        return 0  # If all values are zero or all weights are zero, return zero directly
    
    weighted_score = (soft_tags * w1) + (NPS * w2) + (distance * w3)
    
    # Assuming raw weighted score could be any real number
    min_raw_score =0
    max_raw_score = 100

    # Linear mapping to the range [0, 100]
    mapped_score = ((weighted_score - min_raw_score) / (max_raw_score - min_raw_score)) *100


    return round(mapped_score, 2)
#%%
# Example usage:
soft_tags_value = 0
NPS_value = 0
distance_value = 0
weight_soft_tags = 0
weight_NPS = 0
weight_distance = 0

result = calculate_weighted_score(soft_tags_value, NPS_value, distance_value, weight_soft_tags, weight_NPS, weight_distance)
print("Weighted Score:", result)
# %%
