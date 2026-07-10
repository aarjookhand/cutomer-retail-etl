import pandas as pd

def create_valid_dataframe():
    return pd.DataFrame(
        [
            {
                "Customer ID": 1,
                "Gender": "Female",
                "Age": 25,
                "City": "Paris",
                "Membership Type": "Gold",
                "Total Spend": 500.0,
                "Items Purchased": 10,
                "Average Rating": 4.5,
                "Discount Applied": True,
                "Days Since Last Purchase": 5,
                "Satisfaction Level": "Satisfied",
            }
        ]
    )