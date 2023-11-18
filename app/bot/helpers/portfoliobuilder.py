from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import pandas as pd
from .historic_data_local import load_and_organize_data

def build_portfolio():
    print("building portfolio")
    
    data =  load_and_organize_data("historical_data.json")
    asset_prices = data.to_dict('list')

    # Convert to DataFrame
    df = pd.DataFrame(asset_prices)

    # Fill NA values
    df = df.fillna(method='pad')

    # Calculate expected returns and sample covariance
    mu = expected_returns.mean_historical_return(df)
    S = risk_models.sample_cov(df)

    # Optimize for maximal Sharpe ratio
    ef = EfficientFrontier(mu, S, weight_bounds=(0, 1))
    raw_weights = ef.max_sharpe()
    cleaned_weights = ef.clean_weights()
    print(cleaned_weights)
    return cleaned_weights