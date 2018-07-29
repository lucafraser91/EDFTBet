from Core import *
from time import sleep

""" 
    BID   = Side +1 = LAY runner
    OFFER = Side -1 = Back Runner
"""

application = EDFTBet()

#application.add_user(UserAccount("davisr", 0))

new_market = Market("Sun to Come out Tomorrow")
new_market.description = "Will the Sun Come out tomorrow?"
new_market.add_runner(Runner("Yes"))

#application.add_market(new_market)

new_market = Market("Sum19/Win18 Spread on 31MAR18")
new_market.description = "What will the HEREN settlement of the TTF S/W Spread be on COB 31MAR18"
new_market.add_runner(Runner("less than 0.5"))
new_market.add_runner(Runner("0.5 to 0.75"))
new_market.add_runner(Runner("0.75 to 1.00"))
new_market.add_runner(Runner("more than 1.00"))

#application.add_market(new_market)

#application.match_orders()


#application.add_limit_order(market_id=1, runner_id=1, user_id=1, price=2.00, stake=10.00, side=-1)
#application.add_limit_order(market_id=1, runner_id=1, user_id=1, price=1.10, stake=10.00, side=-1)
#application.add_limit_order(market_id=1, runner_id=1, user_id=1, price=5.20, stake=10.00, side=-1)
#application.add_limit_order(market_id=1, runner_id=1, user_id=1, price=5.30, stake=10.00, side=-1)
sleep(1)
#application.add_limit_order(market_id=1, runner_id=1, user_id=2, price=3.02, stake=10.00, side=1)

#application.match_orders()

#application.settle_market(market_id=1,outcome=0)

#application.users[0].print_trades()
#application.print_users_info()
sleep(1)

application.markets[3].active=True
#application.print_markets_info()
