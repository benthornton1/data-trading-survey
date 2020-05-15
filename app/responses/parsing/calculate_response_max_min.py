
def calculate_response_min(response, data_value_label):
    min_val = float("inf")

    for data_value in response.data_values:
        if data_value.data_value_label == data_value_label:
            if data_value.value < min_val:
                min_val = data_value.value
    return min_val


def calculate_response_max(response, data_value_label):
    max_val = float("-inf")
    
    for data_value in response.data_values:
        if data_value.data_value_label == data_value_label:
            if data_value.value > max_val:
                max_val = data_value.value
    return max_val
