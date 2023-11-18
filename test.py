from app.bot.tools.Transaction.tool import TransactionTool
from app.bot.tools.Balances.tool import BalanceTool
from app.bot.tools.TokenPrices.tool import TokenPricesTool
from app.bot.tools.TokenPriceHistory.tool import TokenPriceHistoryTool
from app.bot.tools.PortfolioBuilder.tool import PortfolioBuilderTool


from app.bot.helpers.historic_data_local import load_and_organize_data
from app.bot.helpers.portfoliobuilder import build_portfolio



query = "Swap 3 ETH for USDC at the current market rate on behalf of the user, ensuring that the user's wallet has sufficient funds and that all necessary permissions are granted."
#PortfolioBuilderTool.test()

build_portfolio()