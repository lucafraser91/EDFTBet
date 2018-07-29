import pickle
import os
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from getpass import getuser
from time import sleep
from GUI import *

# This file is going to be shared with no problems

""" 
    BID   = Side +1
    OFFER = Side -1
"""


class EDFTBet(Tk):
    def __init__(self):
        Tk.__init__(self)

        """ ------------------------------------------------------------------------------------------------------------
        CORE Code stuff ------------------------------------------------------------------------------------------------
         ---------------------------------------------------------------------------------------------------------------
        """

        # Saved and loaded objects defaults
        self.markets = list()
        self.users = list()
        self.order_id_count = 1
        self.trade_id_count = 1

        # Load on start up:
        # self.fileloc = r"C:\Users\lucaf\Documents\GitHub\EDFTBet\\"
        self.fileloc = r"Q:\Luca\Test\EDFTBet" + '\\'
        self.filename = "EDFTBet.pckl"

        self.load()
        try:
            self.last_loaded = os.stat(self.fileloc + "Markets_" + self.filename)[8]
        except FileNotFoundError:
            print("New System")

        # self.markets[0].active = True
        # self.save()

        # icon / title
        self.iconbitmap(r'Q:\Luca\Test\EDFTBet\output.ico')
        self.title("EDFTB")

        # Set current user
        self.current_username = getuser()  # +"_test"

        # list of approved users
        with open(self.fileloc + 'Approved.txt', 'r') as f:
            approved_users = f.readlines()
            f.close()
        self.approved_users = [x.strip() for x in approved_users]

        with open(self.fileloc + 'Admin Approved.txt', 'r') as f:
            admin_approved_users = f.readlines()
            f.close()
        self.admin_approved_users = [x.strip() for x in admin_approved_users]

        with open(self.fileloc + 'God Approved.txt', 'r') as f:
            god_approved_users = f.readlines()
            f.close()
        self.god_approved_users = [x.strip() for x in god_approved_users]

        if self.current_username not in self.approved_users:
            print("====================\nUsername not found...see U L8er\n====================")
            sleep(3)
            self.destroy()
            return None

        for user in self.users:
            if user.username == self.current_username:
                self.current_userid = user.id
                break
        else:
            new_user = UserAccount(self.current_username, 0)
            self.add_user(new_user)
            for user in self.users:
                if user.username == self.current_username:
                    self.current_userid = user.id
                    break

        self.market_make = False
        """ ------------------------------------------------------------------------------------------------------------
        GUI stuff ------------------------------------------------------------------------------------------------------
         ---------------------------------------------------------------------------------------------------------------
        """
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in (GUI_StartPage, HomePage, NewMarket, ControlTab):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.current_market = 1
        frame = ViewMarket(self.container, self, 1)
        self.frames[ViewMarket] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.frames[GUI_StartPage].welcome_text.configure(
            text="Welcome to EDFT Prediction Markets\n Username = %s" % self.current_username)

        # Update Account info display
        account_info_text = "Username = %s\n Account Funds: %s" % (
            self.current_username, self.get_user_available_funds(self.current_userid))

        account_info_text2 = "Open Orders: %s\n Total Trades: %s" % (
            str(len(self.get_user_open_orders(self.current_userid))),
            str(len(self.get_user_positions(self.current_userid))))

        self.frames[HomePage].user_account_info_text.configure(
            text=account_info_text)

        self.frames[HomePage].user_account_info_text2.configure(
            text=account_info_text2)

        # Show Frames
        self.current_frame = None
        self.show_frame(GUI_StartPage)

        # Make Amendments

        self.save()
        self.poll()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.current_frame = cont

    # Save & Load info
    def load(self):
        try:
            with open(self.fileloc + "users_" + self.filename, 'rb') as handle:
                self.users = pickle.load(handle)
                handle.close()

            with open(self.fileloc + "markets_" + self.filename, 'rb') as handle:
                self.markets = pickle.load(handle)
                handle.close()

            with open(self.fileloc + "order_id_count_" + self.filename, 'rb') as handle:
                self.order_id_count = pickle.load(handle)
                handle.close()

            with open(self.fileloc + "trade_id_count_" + self.filename, 'rb') as handle:
                self.trade_id_count = pickle.load(handle)
                handle.close()

            self.last_loaded = os.stat(self.fileloc + "Markets_" + self.filename)[8]

        except FileNotFoundError:
            print("Save file not found")

    def save(self):

        with open(self.fileloc + "users_" + self.filename, 'wb') as handle:
            pickle.dump(self.users, handle, protocol=pickle.HIGHEST_PROTOCOL)
            handle.close()

        with open(self.fileloc + "markets_" + self.filename, 'wb') as handle:
            pickle.dump(self.markets, handle, protocol=pickle.HIGHEST_PROTOCOL)
            handle.close()

        with open(self.fileloc + "order_id_count_" + self.filename, 'wb') as handle:
            pickle.dump(self.order_id_count, handle, protocol=pickle.HIGHEST_PROTOCOL)
            handle.close()

        with open(self.fileloc + "trade_id_count_" + self.filename, 'wb') as handle:
            pickle.dump(self.trade_id_count, handle, protocol=pickle.HIGHEST_PROTOCOL)
            handle.close()

        self.last_loaded = os.stat(self.fileloc + "Markets_" + self.filename)[8]

    def poll(self):
        # Poll markets file
        try:
            latest_update = os.stat(self.fileloc + "Markets_" + self.filename)[8]

            if self.last_loaded != latest_update:
                self.load()
                if self.current_frame == ViewMarket:
                    self.frames[ViewMarket].refresh()
                elif self.current_frame == HomePage:
                    self.refresh_home()
                elif self.current_frame == ControlTab:
                    # self.refresh_control()
                    pass
                else:
                    self.load()
            self.after(1500, self.poll)
        except:
            self.after(1500, self.poll)


    # refresh pages
    def login_as_market_maker(self):
        self.market_make = True
        self.users[self.current_userid-1].market_maker = True
        self.refresh_home()

    def refresh_home(self):
        self.load()

        self.frames[HomePage].destroy()
        self.frames[HomePage] = HomePage(self.container, self)
        self.frames[HomePage].grid(row=0, column=0, sticky="nsew")

        # Update Account info display
        account_info_text = "Username: %s" % self.current_username
        account_info_text2 = "Open Orders: %s\n Total Trades: %s" % (
            str(len(self.get_user_open_orders(self.current_userid))),
            str(len(self.get_user_positions(self.current_userid))))
        account_info_text3 = "Account Balance:"
        account_info_text4 = str(round(self.get_user_available_funds(self.current_userid), 2))

        if float(account_info_text4) > 0:
            self.frames[HomePage].user_account_info_text4.configure(font="helvetica 12 bold", fg="green")
        elif float(account_info_text4) < 0:
            self.frames[HomePage].user_account_info_text4.configure(font="helvetica 12 bold", fg="red")
        else:
            self.frames[HomePage].user_account_info_text4.configure(font="helvetica 12 bold", fg="blue")

        self.frames[HomePage].user_account_info_text.configure(text=account_info_text)
        self.frames[HomePage].user_account_info_text2.configure(text=account_info_text2)
        self.frames[HomePage].user_account_info_text3.configure(text=account_info_text3)
        self.frames[HomePage].user_account_info_text4.configure(text=account_info_text4)

        self.update_idletasks()
        self.show_frame(HomePage)

    def refresh_view_market(self, market_id):
        self.load()

        self.frames[ViewMarket].destroy()
        self.frames[ViewMarket] = ViewMarket(self.container, self, market_id)
        self.frames[ViewMarket].grid(row=0, column=0, sticky="nsew")

        market_info_text = "Market: " + self.markets[market_id - 1].name
        market_discription_text = "Description: " + self.markets[market_id - 1].description
        self.frames[ViewMarket].market_name_label.configure(text=market_info_text)
        self.frames[ViewMarket].market_description_label.configure(text=market_discription_text)

        self.update_idletasks()
        self.show_frame(ViewMarket)

    def refresh_control(self):
        self.load()
        self.frames[ControlTab].destroy()
        self.frames[ControlTab] = ControlTab(self.container, self)
        self.frames[ControlTab].grid(row=0, column=0, sticky="nsew")
        self.update_idletasks()
        self.show_frame(ControlTab)

    # Markets

    def add_market(self, market):
        self.load()
        self.markets.append(market)
        self.markets[-1].id = len(self.markets)
        self.save()

    def remove_market(self, market_id):
        self.load()
        self.markets[market_id - 1].active = False
        self.save()

    def print_markets_info(self):
        print("\n ALL MARKETS -------------------------------")
        for market in self.markets:
            if market.active or market.outcome != 0:
                market.print_info()

    def settle_market(self, market_id, outcome):

        self.load()
        # update Market
        self.markets[market_id - 1].outcome = outcome
        self.markets[market_id - 1].concluded = True

        # Settle trades

        for user_pointer, user in enumerate(self.users):
            for trade in user.trades:
                if trade.market == market_id and trade.settled == 0:
                    if trade.side == 1 and trade.runner == outcome:  # Win Buy
                        trade.settled = trade.stake * (100 - trade.price)
                        self.users[user_pointer].available_funds += trade.stake * (100 - trade.price)

                    elif trade.side == 1 and trade.runner != outcome:  # Lose Buy
                        trade.settled = trade.stake * (0 - trade.price)
                        self.users[user_pointer].available_funds += trade.stake * (0 - trade.price)

                    elif trade.side == -1 and trade.runner == outcome:  # Lose Sell
                        trade.settled = -trade.stake * (100 - trade.price)
                        self.users[user_pointer].available_funds += -trade.stake * (100 - trade.price)

                    elif trade.side == -1 and trade.runner != outcome:  # Win Sell
                        trade.settled = -trade.stake * (0 - trade.price)
                        self.users[user_pointer].available_funds += -trade.stake * (0 - trade.price)

            self.users[user_pointer].available_funds = round(self.users[user_pointer].available_funds, 3)

        self.save()
        # Remove/close all open orders
        for user_pointer, user in enumerate(self.users):

            for order in user.open_orders:
                if order.market == market_id:
                    self.remove_limit_order(user_id=user.id, order_id=order.order_id)

        self.markets[market_id - 1].active = False
        self.save()

    def get_all_markets(self):
        self.load()
        return self.markets

    # Users

    def add_user(self, user):
        self.load()
        self.users.append(user)
        self.users[-1].id = len(self.users)
        self.save()

    def print_users_info(self):
        self.load()
        print("\n ALL USERS -------------------------------")
        for user in self.users:
            user.print_info()

    def get_user_available_funds(self, user_id):
        self.load()
        return self.users[user_id - 1].available_funds

    def get_user_open_orders(self, user_id):
        self.load()
        return self.users[user_id - 1].open_orders

    def get_user_positions(self, user_id):
        self.load()
        positions = [x for x in self.users[user_id - 1].trades if x.settled == 0]
        return positions

    def get_intrinsic_position(self, user_id, runner, market_id):
        'Return the payoff to user if this outcome happens'
        ':returns Payoff if happens'
        payoff = 0

        for trade in self.users[user_id - 1].trades:
            if trade.market == market_id:
                if trade.runner == runner.id:
                    payoff += trade.side * trade.stake * (100 - trade.price)
                else:
                    payoff += trade.side * trade.stake * (0 - trade.price)

        return round(payoff, 0)

    # Orders

    def add_limit_order(self, market_id, runner_id, user_id, price, stake, side):
        self.load()
        # make the limit order object and set ID
        new_order = LimitOrder(user=user_id, price=price, stake=stake, side=side, market=market_id, runner_id=runner_id)
        new_order.order_id = self.order_id_count
        self.order_id_count += 1

        # add to the user account
        self.users[user_id - 1].open_orders.append(new_order)

        # add to the order book, assign order id
        if side == 1:  # Back
            for order_pointer, order in enumerate(self.markets[market_id - 1].runners[runner_id - 1].bids):
                if price > order.price:
                    self.markets[market_id - 1].runners[runner_id - 1].bids.insert(order_pointer, new_order)
                    break
            else:
                self.markets[market_id - 1].runners[runner_id - 1].bids.append(new_order)


        else:  # Lay
            for order_pointer, order in enumerate(self.markets[market_id - 1].runners[runner_id - 1].offers):
                if price < order.price:
                    self.markets[market_id - 1].runners[runner_id - 1].offers.insert(order_pointer, new_order)
                    break
            else:
                self.markets[market_id - 1].runners[runner_id - 1].offers.append(new_order)
        self.save()

    def remove_limit_order(self, user_id, order_id):
        self.load()
        for order in self.users[user_id - 1].open_orders:
            if order.order_id == order_id:

                # Remove order from order book
                if order.side == 1:
                    self.markets[order.market - 1].runners[order.runner - 1].bids = [x for x in self.markets[
                        order.market - 1].runners[order.runner - 1].bids if x.order_id != order_id]
                else:
                    self.markets[order.market - 1].runners[order.runner - 1].offers = [x for x in self.markets[
                        order.market - 1].runners[order.runner - 1].offers if x.order_id != order_id]

                # Remove from user account
                self.users[user_id - 1].open_orders = [x for x in self.users[user_id - 1].open_orders if
                                                       x.order_id != order_id]

        self.save()

    def remove_all_limit_order(self, user_id, market_id):
        self.load()
        for order in self.users[user_id - 1].open_orders:
            if order.market == market_id:

                # Remove order from order book
                if order.side == 1:
                    self.markets[order.market - 1].runners[order.runner - 1].bids = [x for x in self.markets[
                        order.market - 1].runners[order.runner - 1].bids if x.price_owner != user_id]
                else:
                    self.markets[order.market - 1].runners[order.runner - 1].offers = [x for x in self.markets[
                        order.market - 1].runners[order.runner - 1].offers if x.price_owner != user_id]

                # Remove from user account
                self.users[user_id - 1].open_orders = [x for x in self.users[user_id - 1].open_orders if
                                                       x.market != market_id]

        self.save()

    def amend_limit_order(self, user_id, order_id, new_price, new_stake, order):
        self.remove_limit_order(user_id=user_id, order_id=order_id)
        self.add_limit_order(market_id=order.market,
                             runner_id=order.runner,
                             user_id=user_id,
                             price=new_price,
                             stake=new_stake,
                             side=order.side)

    def match_orders(self):
        self.load()
        new_trades = []
        for market_n, market in enumerate(self.markets):
            for runner_n, runner in enumerate(market.runners):
                market_crossed = True

                while market_crossed:
                    try:
                        if runner.bids[0].price >= runner.offers[0].price:

                            # check what order was there first to set trade price
                            if runner.bids[0].time_added < runner.offers[0].time_added:
                                trade_price = runner.bids[0].price
                            else:
                                trade_price = runner.offers[0].price

                            trade_size = min([runner.bids[0].stake, runner.offers[0].stake])
                            trade_id = self.trade_id_count
                            self.trade_id_count += 1
                            new_trades.append(trade_id)

                            #  Add trade to backers account and provision max loss
                            new_trade = Trade(market=market.id,
                                              runner=runner.id,
                                              side=1,
                                              counterpart=runner.offers[0].price_owner,
                                              price=trade_price,
                                              stake=trade_size,
                                              trade_id=trade_id,
                                              market_name=market.name,
                                              runner_name=runner.name,
                                              counterpart_name=self.users[runner.offers[0].price_owner - 1].username
                                              )
                            self.users[runner.bids[0].price_owner - 1].trades.append(new_trade)

                            #  Add trade to sellers account and provision max loss
                            new_trade = Trade(market=market.id,
                                              runner=runner.id,
                                              side=-1,
                                              counterpart=runner.bids[0].price_owner,
                                              price=trade_price,
                                              stake=trade_size,
                                              trade_id=trade_id,
                                              market_name=market.name,
                                              runner_name=runner.name,
                                              counterpart_name=self.users[runner.bids[0].price_owner - 1].username
                                              )
                            self.users[runner.offers[0].price_owner - 1].trades.append(new_trade)

                            # Amend order book
                            if runner.bids[0].stake > runner.offers[0].stake:  # Bid is bigger, destroy offer
                                # Remove filled order
                                user_id = runner.offers[0].price_owner
                                order_id = runner.offers[0].order_id
                                self.users[user_id - 1].open_orders = [x for x in self.users[user_id - 1].open_orders if
                                                                       x.order_id != order_id]

                                self.markets[market_n].runners[runner_n].offers.pop(0)

                                # Amend part filled order in market and user objects
                                self.markets[market_n].runners[runner_n].bids[0].stake -= trade_size

                                user_id = runner.bids[0].price_owner
                                for order in self.users[user_id - 1].open_orders:
                                    if order.order_id == self.markets[market_n].runners[runner_n].bids[0].order_id:
                                        order.stake -= trade_size

                            elif runner.bids[0].stake < runner.offers[0].stake:  # offer is bigger, destroy bid
                                # Remove filled order
                                user_id = runner.bids[0].price_owner
                                order_id = runner.bids[0].order_id
                                self.users[user_id - 1].open_orders = [x for x in self.users[user_id - 1].open_orders if
                                                                       x.order_id != order_id]

                                self.markets[market_n].runners[runner_n].bids.pop(0)

                                # Amend part filled order in market and user objects
                                self.markets[market_n].runners[runner_n].offers[0].stake -= trade_size
                                user_id = runner.offers[0].price_owner
                                for order in self.users[user_id - 1].open_orders:
                                    if order.order_id == self.markets[market_n].runners[runner_n].offers[0].order_id:
                                        order.stake -= trade_size

                            else:
                                # Remove filled orders
                                user_id = runner.bids[0].price_owner
                                order_id = runner.bids[0].order_id
                                self.users[user_id - 1].open_orders = [x for x in self.users[user_id - 1].open_orders if
                                                                       x.order_id != order_id]
                                user_id = runner.offers[0].price_owner
                                order_id = runner.offers[0].order_id
                                self.users[user_id - 1].open_orders = [x for x in self.users[user_id - 1].open_orders if
                                                                       x.order_id != order_id]

                                self.markets[market_n].runners[runner_n].bids.pop(0)
                                self.markets[market_n].runners[runner_n].offers.pop(0)

                            print("New Trade ID: %s" % str(trade_id))

                        else:
                            market_crossed = False

                    except IndexError:  # no more trades
                        market_crossed = False
        self.save()

        # New trade confirmations message:
        for new_trade_id in new_trades:
            for trade in self.users[self.current_userid - 1].trades:
                if new_trade_id == trade.trade_id:
                    message_text = "Trade ID: %s\n\nMarket: %s\nSide: %s\nOutcome: %s\nPrice: %s\nStake: %s" % (
                        str(new_trade_id), trade.market_name, side_as_text(trade.side), trade.runner_name, trade.price,
                        trade.stake)
                    messagebox.showinfo("Trade Confirmation", message_text)


class Market(object):
    def __init__(self, market_name):
        self.active = True
        self.name = market_name
        self.id = 0
        self.description = "Market description"
        self.runners = list()
        self.concluded = False
        self.outcome = 0

    def print_info(self):
        print("__________________________________")
        print("Market Name: " + self.name)
        print("Market id: " + str(self.id))
        print("Description: " + self.description)
        print("Market Active: " + str(self.active))
        print("Runners:")
        for runner in self.runners:
            print("----")
            print("\tRunner ID: " + str(runner.id))
            print("\tRunner Name: " + runner.name)
            if self.active:
                try:
                    print("\tBest Bid:" + str(runner.bids[0].price))
                except IndexError:
                    print("\tBest Bid: -")

                try:
                    print("\tBest Offer:" + str(runner.offers[0].price))
                except IndexError:
                    print("\tBest Offer: -")
        print("----")
        print("Concluded: " + str(self.concluded))
        print("Outcome: Runner " + str(self.outcome))

    def add_runner(self, runner):
        self.runners.append(runner)
        self.runners[-1].id = len(self.runners)

    def remove_runner(self, runner_id):
        self.runners.pop(runner_id - 1)

    def check_arbitrage(self, side):
        bids_sum = int(0)
        offers_sum = int(0)
        try:
            for runner in self.runners:
                bids_sum += runner.bids[0].price
        except IndexError:
            bids_sum = "-"
        try:
            for runner in self.runners:
                offers_sum += runner.offers[0].price
        except IndexError:
            offers_sum = "-"

        if side == "bids":
            return bids_sum
        else:
            return offers_sum


class Runner(object):
    def __init__(self, runner_name):
        self.name = runner_name
        self.id = 0
        self.bids = list()
        self.offers = list()


class LimitOrder(object):
    def __init__(self, user, price, stake, market, runner_id, side):
        self.order_id = int()
        self.price_owner = user
        self.price = int(price)
        self.stake = int(stake)
        self.market = market
        self.runner = runner_id
        self.side = side
        self.time_added = datetime.now()

    def print_info(self):
        print("\tOrder ID: %s Market: %s Runner: %s Side: %s Price: %s Size: %s" % (
            self.order_id, self.market, self.runner, self.side, self.price, self.stake))


class Trade(object):
    def __init__(self, market, runner, side, counterpart, price, stake, trade_id, market_name, runner_name,
                 counterpart_name):
        self.trade_id = trade_id
        self.market = market
        self.market_name = market_name
        self.runner = runner
        self.runner_name = runner_name
        self.side = side
        self.counterpart = counterpart
        self.counterpart_name = counterpart_name
        self.price = price
        self.stake = stake
        self.settled = 0
        self.timestamp = datetime.now()

    def print_info(self):
        print("ID: %s, Market: %s, Runner: %s, Counterpart: %s, Side: %s, Volume: %s, Price: %s ....P&L: %s" % (
            str(self.trade_id),
            str(self.market_name),
            str(self.runner_name),
            self.counterpart_name,
            side_as_text(self.side),
            str(self.stake),
            str(self.price),
            str(self.settled)
        ))


class UserAccount(object):
    def __init__(self, username, available_funds=0, ):
        self.username = username
        self.id = 0
        self.available_funds = available_funds
        self.trades = list()
        self.open_orders = list()
        self.market_maker = False

    def print_info(self):
        print("\nUser Name: " + self.username)
        print("User id: " + str(self.id))
        print("Available Funds: " + str(self.available_funds))
        print("Total Trades: " + str(len(self.trades)))
        print("Open Orders: " + str(len(self.open_orders)))

    def print_trades(self):
        print("\n--------------------------------")
        print("All Trades for user: %s" % self.username)
        for trade in self.trades:
            trade.print_info()
        print("--------------------------------")

    def print_open_orders(self):
        print("\n--------------------------------")
        print("Open Orders for user: %s" % self.username)
        for order in self.open_orders:
            order.print_info()
        print("--------------------------------")


def side_as_text(side):
    if side == 1:
        return "Buy"
    else:
        return "Sell"


if __name__ == "__main__":
    GUI_app = EDFTBet()
    GUI_app.mainloop()

