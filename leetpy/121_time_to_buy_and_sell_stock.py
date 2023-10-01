"""
You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

Example 1:
Input: prices = [7,1,5,3,6,4]
Output: 5
Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

Example 2:

Input: prices = [7,6,4,3,1]
Output: 0
Explanation: In this case, no transactions are done and the max profit = 0.



Constraints:

    1 <= prices.length <= 105
    0 <= prices[i] <= 104

"""

class Solution(object):

    def maxProfit(self, prices) -> int:
        """
        :type prices: List[int]
        :rtype: int
        """
        print(f"maxProfit({prices})")

        left = 0 #Buy
        right = 1 #Sell
        max_profit = 0
        while right < len(prices):
            currentProfit = prices[right] - prices[left]
            if currentProfit > 0:
                max_profit = max(currentProfit, max_profit)
            else:
                left = right
            right += 1
        return max_profit



sol = Solution()

prices = [7,1,5,3,6,4]
assert 5 == sol.maxProfit(prices)

prices = [7,6,4,3,1]
assert 0 == sol.maxProfit(prices)

prices = [101,102,103,104,105]
assert 4 == sol.maxProfit(prices)
prices = [101,102,103,102, 100,50]
assert 2 == sol.maxProfit(prices)
