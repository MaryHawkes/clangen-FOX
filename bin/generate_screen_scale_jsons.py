import json
import math
import re


def multiply_numbers_in_string(s, multiplier):
    # Function to replace matched number with the floored multiplied value
    def replace(match):
        number = float(match.group())
        multiplied = math.floor(number * multiplier)
        return str(multiplied)

    # Use regex to find all numbers in the string
    return re.sub(r"(?<![#0x])(?<![#0X])-?\b\d+\.?\d*\b", replace, s)


def multiply_numbers(data, multiplier):
    if isinstance(data, dict):
        result = {}
        blacklist = ["prototype", "line_spacing"]
        for key, value in data.items():
            if key in blacklist:
                result[key] = value
            else:
                result[key] = multiply_numbers(value, multiplier)
        return result
    elif isinstance(data, list):
        return [multiply_numbers(element, multiplier) for element in data]
    elif isinstance(data, str):
        return multiply_numbers_in_string(data, multiplier)
    return data


def process_json(input_file, output_file, multiplier):
    with open(input_file, "r") as readfile:
        data = json.load(readfile)

    modified_data = multiply_numbers(data, multiplier)

    with open(output_file, "w") as writefile:
        json.dump(modified_data, writefile, indent=4)


if __name__ == "__main__":
    input_file = "resources/theme/fonts/master_text_scale.json"

    for i in [1.25, 1.5, 1.75, 2]:
        output_file = f"resources/theme/fonts/{i}_screen_scale.json"
        process_json(input_file, output_file, i)
