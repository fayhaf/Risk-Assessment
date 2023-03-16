import pandas as pd
import numpy as np

class CompareMetrics():

    def __init__(self, portfolio = 'sp500prices.pkl'):
      self.portfolio = pd.read_pickle(portfolio)
      self.myMetric = self.__my_metric()
      self.sharpeRatio = self.__sharpe_ratio()
      self.compareMetrics = self.__compare_metrics()
      self.correlationCoefficient = self.__get_correlation_coefficient()

    """ Part 1: Define your metric """
    #Calculates RDD for given list of returns
    def __my_metric(self) -> float:
         max_drawdown = 0
        peak = 0
        for i in range(len(returns)):
            if returns[i] > returns[peak]:
                peak = i
            drawdown = (returns[peak] - returns[i]) / returns[peak]
            if drawdown > max_drawdown:
                max_drawdown = drawdown
    annualized_return = (returns[-1] / returns[0]) ** (1 / (len(returns) / 252)) - 1
    rdd_ratio = annualized_return / max_drawdown
    return rdd_ratio

    def compute_rdd_ratio(self):
        #Load price data
        prices_df = pd.read_pickle(self.filename)

        #Compute the daily returns
        returns_df = prices_df.pct_change()

        #Compute the daily returns of the portfolio
        num_stocks = len(prices_df.columns)
        weights = [1 / num_stocks] * num_stocks
        portfolio_returns = returns_df.dot(weights)

        #Calculate and return the RDD ratio
        rdd_ratio = self.__my_metric(portfolio_returns.tolist())
        return rdd_ratio
       

    """ Part 2: Define the Sharpe Ratio """
    #Create a function that computes annualized sharpe ratio 
    def __sharpe_ratio(self, returns) -> float:
        returns = self.portfolio.diff().sum(axis=1)
        ann_return = np.mean(returns) * 252
        annvolatility = np.std(returns) * np.sqrt(252)
        #Create sharpe ratio calculation with current risk-free rate
        sharpe_ratio = (ann_return - 0.03982) / ann_volatility
        return sharpe_ratio 
 

    """ Part 3: Evaluate Metric Correlation """
    #Computes the RDD and Sharpe of a portfolio and returns a df.
    #We use 252 trading days in a year as a basis to annualize the returns
    #Uses the pandas.DataFrame.pct_change() method to compute the daily returns of each stock 
    def __compare_metrics(self) -> pd.DataFrame:
        rdd_ratio = self.__compute_rdd_ratio()
        sharpe_ratio = self.__sharpe_ratio()
        data = {'RDD Ratio': [rdd_ratio], 'Sharpe Ratio': [sharpe_ratio]}
        df = pd.DataFrame(data)
        return df

    #Return correlation coefficient between the two metrics
    def __get_correlation_coefficient(self) -> float:
       #Compute the RDD ratio and Sharpe ratio for the portfolio
        rdd_ratio = self.portfolio.__compute_rdd_ratio()
        sharpe_ratio = self.portfolio.__sharpe_ratio()
        
        #Load price data
        prices_df = pd.read_pickle(self.portfolio.filename)

        #Compute the daily returns of each stock
        returns_df = prices_df.pct_change()

        #Compute the daily returns of the portfolio
        num_stocks = len(prices_df.columns)
        weights = [1 / num_stocks] * num_stocks
        portfolio_returns = returns_df.dot(weights)

        #Compute the correlation coefficient between RDD ratio and Sharpe ratio and return
        corr_coeff = np.corrcoef(portfolio_returns, [rdd_ratio, sharpe_ratio])[0, 1:]
        return corr_coeff[0]
       
if __name__ == '__main__':

   sp500 = CompareMetrics() 
   # TODO: enter the name of the metric you chose
   myMetric = "RDD Ratio"

   print("1. " + myMetric + " of the portfolio is: " + str(sp500.myMetric))
   print("2. Sharpe Ratio of the portfolio is: " + str(sp500.sharpeRatio))
   print("3. Metric comparison is: " + '\n' + str(sp500.compareMetrics))
   print("4. Correlation Coefficient between " + myMetric + " and Sharpe Ratio is: " + str(sp500.correlationCoefficient))