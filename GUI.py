from Core import *
import tkinter as tk
from tkinter import messagebox, ttk


class GUI_StartPage(tk.Frame):
    ''' this is a test GUI to start projects from'''

    def __init__(self, parent, controller):
        # Initalise Frame'''
        Frame.__init__(self, parent)

        self.pack()

        self.welcome_text = Label(self, text="Welcome to EDFT Prediction Markets\n Username = %s" % "user")
        self.welcome_text.grid(row=0, column=0, columnspan=1, sticky=S)

        self.login_button = ttk.Button(self, text="Log In (Trader)", command=lambda: controller.refresh_home())
        self.login_button.grid(row=1, column=0, sticky="NSEW")

        self.login_button = ttk.Button(self, text="Log In (Market Maker)",
                                       command=lambda: controller.login_as_market_maker())
        self.login_button.grid(row=2, column=0, sticky="NSEW")


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        """ user_frame containing acocunt info"""
        self.user_frame = tk.LabelFrame(self, text="Account Info", padx=5, pady=5, relief="groove")
        self.user_frame.pack(padx=5, pady=5, fill="x", expand=NO, anchor=N, side=TOP)

        self.user_account_info_text = Label(self.user_frame, text="", width=15, anchor=W)
        self.user_account_info_text.grid(row=0, column=0, columnspan=1, sticky="NSEW")

        self.user_account_info_text2 = Label(self.user_frame, text="", width=15, anchor=W)
        self.user_account_info_text2.grid(row=0, column=1, columnspan=1, sticky="NSEW")

        self.user_account_info_text3 = Label(self.user_frame, text="", anchor=W)
        self.user_account_info_text3.grid(row=0, column=2, columnspan=1, sticky="NSEW")

        self.user_account_info_text4 = Label(self.user_frame, text="", width=50, anchor=W)
        self.user_account_info_text4.grid(row=0, column=3, columnspan=1, sticky="NSEW")

        """ market_frame containing markets"""
        self.market_frame = tk.LabelFrame(self, text="Markets Available", padx=5, pady=5, relief="groove")
        self.market_frame.pack(padx=5, pady=5, fill=X, expand=NO, anchor=N, side=TOP)

        self.control_frame = tk.LabelFrame(self, padx=5, pady=5, relief="flat")
        self.control_frame.pack(padx=5, pady=5, fill="x", expand="yes", anchor="n")

        self.account_tab_button = ttk.Button(self.user_frame, text="My Account", width=15,
                                             command=lambda: controller.refresh_control())
        self.account_tab_button.grid(row=0, column=99, columnspan=1, sticky=E)

        """ populate all markets info """
        self.market_containers = list()

        for n_market, market in enumerate(controller.markets):

            # Make a container for all
            new_frame = tk.LabelFrame(self.market_frame, text=market.name, padx=5, pady=5, relief="sunken")
            self.market_containers.append(new_frame)
            self.market_containers[-1].pack(fill="x", expand="yes", anchor="n")

            # If market is active, fill the container
            if market.active is True:
                self.market_description_text = Label(self.market_containers[-1], text=market.description, width=105,
                                                     anchor=W)
                self.market_description_text.pack(expand="yes", anchor="w", side=LEFT)

                self.open_market_button = ttk.Button(self.market_containers[-1], text="View", width=7,
                                                     command=lambda i=market.id: gui_view_market(i, controller))
                self.open_market_button.pack(expand="yes", anchor="e", side=RIGHT)

                if controller.current_username in controller.god_approved_users:
                    self.reomove_market_button = ttk.Button(self.market_containers[-1], text="Delete",
                                                            command=lambda i=market.id: gui_remove_market(i, controller,
                                                                                                          self))
                    self.reomove_market_button.pack(expand="yes", anchor="e", side=RIGHT)

        if controller.current_username in controller.admin_approved_users:
            self.new_market_button = ttk.Button(self.market_frame, text="New Market",
                                                command=lambda: controller.show_frame(NewMarket))
            self.new_market_button.pack(expand="yes", anchor="w")


def gui_remove_market(market_id, controller, gui_frame):
    controller.remove_market(market_id)
    gui_frame.destroy()
    controller.frames[HomePage] = HomePage(controller.container, controller)
    controller.frames[HomePage].grid(row=0, column=0, sticky="nsew")
    controller.show_frame(HomePage)
    controller.refresh_home()
    controller.update_idletasks()


def gui_view_market(market_id, controller):
    controller.current_market = market_id
    controller.refresh_view_market(market_id)


class NewMarket(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.grid()
        self.instructions = Label(self, text="Enter Market info, leave name blank to cancel without saving")
        self.instructions.grid(row=1, column=0, columnspan=2, sticky=E)

        self.market_name_label = Label(self, text="Market Name:")
        self.market_name_label.grid(row=2, column=0, columnspan=1, sticky=E)
        self.market_name_textbox = Text(self, height="1", width="80")
        self.market_name_textbox.grid(row=2, column=1)

        self.market_description_label = Label(self, text="Market Description:")
        self.market_description_label.grid(row=3, column=0, columnspan=1, sticky=E)
        self.market_description_textbox = Text(self, height="2", width="80")
        self.market_description_textbox.grid(row=3, column=1)

        self.runner1_label = Label(self, text="Outcome 1:")
        self.runner1_label.grid(row=4, column=0, columnspan=1, sticky=E)
        self.runner1_textbox = Text(self, height="1", width="80")
        self.runner1_textbox.grid(row=4, column=1)

        self.runner2_label = Label(self, text="Outcome 2:")
        self.runner2_label.grid(row=5, column=0, columnspan=1, sticky=E)
        self.runner2_textbox = Text(self, height="1", width="80")
        self.runner2_textbox.grid(row=5, column=1)

        self.runner3_label = Label(self, text="(Outcome 3:)")
        self.runner3_label.grid(row=6, column=0, columnspan=1, sticky=E)
        self.runner3_textbox = Text(self, height="1", width="80")
        self.runner3_textbox.grid(row=6, column=1)

        self.runner4_label = Label(self, text="(Outcome 4:)")
        self.runner4_label.grid(row=7, column=0, columnspan=1, sticky=E)
        self.runner4_textbox = Text(self, height="1", width="80")
        self.runner4_textbox.grid(row=7, column=1)

        self.runner5_label = Label(self, text="(Outcome 5:)")
        self.runner5_label.grid(row=8, column=0, columnspan=1, sticky=E)
        self.runner5_textbox = Text(self, height="1", width="80")
        self.runner5_textbox.grid(row=8, column=1)

        self.addnew_market_button = ttk.Button(self, text="Create Market",
                                               command=lambda: gui_add_market(controller, self))
        self.addnew_market_button.grid(row=9, column=1, sticky=W)


def gui_add_market(controller, gui_frame):
    market_name = gui_frame.market_name_textbox.get("1.0", "end-1c")
    market_description = gui_frame.market_description_textbox.get("1.0", "end-1c")
    runner1 = gui_frame.runner1_textbox.get("1.0", "end-1c")
    runner2 = gui_frame.runner2_textbox.get("1.0", "end-1c")
    runner3 = gui_frame.runner3_textbox.get("1.0", "end-1c")
    runner4 = gui_frame.runner4_textbox.get("1.0", "end-1c")
    runner5 = gui_frame.runner5_textbox.get("1.0", "end-1c")

    if market_name != "" and market_description != "" and runner1 != "" and runner2 != "":
        new_market = Market(market_name)
        new_market.description = market_description

        # add runners
        new_market.add_runner(Runner(runner1))
        new_market.add_runner(Runner(runner2))

        if runner3 != "":
            new_market.add_runner(Runner(runner3))
        if runner4 != "":
            new_market.add_runner(Runner(runner4))
        if runner5 != "":
            new_market.add_runner(Runner(runner5))

        controller.add_market(new_market)

    gui_frame.destroy()
    controller.frames[NewMarket] = NewMarket(controller.container, controller)
    controller.frames[NewMarket].grid(row=0, column=0, sticky="nsew")
    controller.show_frame(HomePage)
    controller.refresh_home()
    controller.update_idletasks()


class ViewMarket(tk.Frame):
    def __init__(self, parent, controller, market_id):
        Frame.__init__(self, parent)
        self.controller = controller
        self.market_id = market_id
        self.home_button = Button(self, text="Back To Markets", command=lambda: controller.refresh_home())
        self.home_button.pack(padx=0, pady=0, fill="x", expand=NO, anchor=N)

        self.market_name_label = Label(self, text="Market Name:")
        self.market_name_label.pack(padx=0, pady=5, anchor=NW)

        self.market_description_label = Label(self, text="Description:")
        self.market_description_label.pack(padx=0, pady=5, anchor=NW)

        """
        FOR MARKET MAKERS ----------------------------------------------------------------------------------
        """
        if controller.market_make is True:
            self.market_make_frame = LabelFrame(self, text="Market Maker Controls")
            self.market_make_frame.pack(padx=0, pady=5, anchor=NW)
            label = Label(self.market_make_frame, text="Probability Spread:")
            label.grid(row=0, column=0)

            self.spread_spinbox = Spinbox(self.market_make_frame, width="5",
                                          from_=1,
                                          to=99, increment=1, repeatinterval=30,
                                          command=lambda: update_shadow_orders(self)
                                          )

            self.spread_spinbox.delete(0, "end")
            self.spread_spinbox.insert(0, 5)
            self.spread_spinbox.grid(row=0, column=1)
            label = Label(self.market_make_frame, text="Clip Size:")
            label.grid(row=1, column=0)
            self.order_size_spinbox = Spinbox(self.market_make_frame, width="5",
                                              from_=1,
                                              to=99, increment=1, repeatinterval=30,
                                              )
            self.order_size_spinbox.delete(0, "end")
            self.order_size_spinbox.insert(0, 25)
            self.order_size_spinbox.grid(row=1, column=1)

            button = ttk.Button(self.market_make_frame, text="Post Orders", width=10,
                                command=lambda: post_mm_orders(self, controller, market_id))
            button.grid(row=2, column=0, columnspan=2)

            button = ttk.Button(self.market_make_frame, text="Switch to Trader View",
                                command=lambda: gui_switch_view(market_id, controller))
            button.grid(row=3, column=0, columnspan=2)

        else:
            button = ttk.Button(self, text="Market Maker View", command=lambda: gui_switch_view(market_id, controller))
            button.pack(padx=0, pady=5, anchor=NW)

        """runners_frame containing order book"""
        self.runner_frame = tk.LabelFrame(self, text="Possible Outcomes", padx=5, pady=5, relief="groove")
        self.runner_frame.pack(padx=5, pady=5, fill=X, expand=NO, anchor=N)

        self.runner_containers = []

        # for each runner in the market, make a frame container
        try:
            for n_runner, runner in enumerate(controller.markets[market_id - 1].runners):
                new_frame = tk.Frame(self.runner_frame, padx=5, pady=0)
                self.runner_containers.append(new_frame)
                self.runner_containers[-1].grid(row=n_runner, column=0)

                self.runner_name_label = Label(self.runner_containers[-1], text=runner.name, width=15)
                self.runner_name_label.grid(row=0, column=0, columnspan=1, sticky=N)

                # populate all order prices
                try:
                    price_text = str(runner.bids[2].price)
                except IndexError:
                    price_text = ""

                self.runner_containers[-1].bid3 = Button(self.runner_containers[-1], text=price_text, width=5,
                                                         bg="gray97", bd=1, fg="red",
                                                         relief="solid", font="helvetica 9 bold")
                self.runner_containers[-1].bid3.grid(row=0, column=1, sticky=W)
                try:
                    if runner.bids[2].price_owner == controller.current_userid:
                        # if users quote, assign amend order command
                        self.runner_containers[-1].bid3.config(bg="LightPink1")
                        self.runner_containers[-1].bid3.config(
                            command=lambda r=runner, o=runner.bids[2]: gui_amend_order(r, controller, o, market_id,self))
                    else:  # otherwise, place a standard trade.
                        self.runner_containers[-1].bid3.config(
                            command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                          side=-1,
                                                                          market_id=market_id,
                                                                          price=r.bids[2].price))
                except IndexError:
                    pass

                try:
                    price_text = str(runner.bids[1].price)
                except IndexError:
                    price_text = ""

                self.runner_containers[-1].bid2 = Button(self.runner_containers[-1], text=price_text, width=5,
                                                         bg="gray97", bd=2, fg="red",
                                                         relief="solid", font="helvetica 9 bold")
                self.runner_containers[-1].bid2.grid(row=0, column=2, sticky=W)
                try:
                    if runner.bids[1].price_owner == controller.current_userid:
                        # if users quote, assign amend order command
                        self.runner_containers[-1].bid2.config(bg="LightPink1")
                        self.runner_containers[-1].bid2.config(
                            command=lambda r=runner, o=runner.bids[1]: gui_amend_order(r, controller, o, market_id,self))
                    else:  # otherwise, place a standard trade.
                        self.runner_containers[-1].bid2.config(
                            command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                          side=-1,
                                                                          market_id=market_id,
                                                                          price=r.bids[1].price))
                except IndexError:
                    pass

                try:
                    price_text = str(runner.bids[0].price)
                except IndexError:
                    price_text = ""

                self.runner_containers[-1].bid1 = Button(self.runner_containers[-1], text=price_text, width=5,
                                                         font="helvetica 9 bold",
                                                         fg="red",
                                                         bg="gray97", bd=3, relief="solid")
                self.runner_containers[-1].bid1.grid(row=0, column=3, sticky=W)
                try:
                    if runner.bids[0].price_owner == controller.current_userid:
                        # if users quote, assign amend order command
                        self.runner_containers[-1].bid1.config(bg="LightPink1")
                        self.runner_containers[-1].bid1.config(
                            command=lambda r=runner, o=runner.bids[0]: gui_amend_order(r, controller, o, market_id,self))
                    else:  # otherwise, place a standard trade.
                        self.runner_containers[-1].bid1.config(
                            command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                          side=-1,
                                                                          market_id=market_id,
                                                                          price=r.bids[0].price))
                except IndexError:
                    pass

                self.spacer_label = Label(self.runner_containers[-1], text="<-Sell / Buy->")
                self.spacer_label.grid(row=0, column=4, columnspan=1, sticky=S)

                try:
                    price_text = str(runner.offers[0].price)
                except IndexError:
                    price_text = ""

                self.runner_containers[-1].offer1 = Button(self.runner_containers[-1], text=price_text, width=5,
                                                           font="helvetica 9 bold",
                                                           fg="green",
                                                           bg="gray97", bd=3, relief="solid")
                self.runner_containers[-1].offer1.grid(row=0, column=5, sticky=W)
                try:
                    if runner.offers[0].price_owner == controller.current_userid:
                        # if users quote, assign amend order command
                        self.runner_containers[-1].offer1.config(bg="PaleGreen2")
                        self.runner_containers[-1].offer1.config(
                            command=lambda r=runner, o=runner.offers[0]: gui_amend_order(r, controller, o, market_id,self))
                    else:  # otherwise, place a standard trade.
                        self.runner_containers[-1].offer1.config(
                            command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                          side=1,
                                                                          market_id=market_id,
                                                                          price=r.offers[0].price))
                except IndexError:
                    pass

                try:
                    price_text = str(runner.offers[1].price)
                except IndexError:
                    price_text = ""

                self.runner_containers[-1].offer2 = Button(self.runner_containers[-1], text=price_text, width=5,
                                                           bg="gray97", bd=2,
                                                           fg="green",
                                                           relief="solid", font="helvetica 9 bold")
                self.runner_containers[-1].offer2.grid(row=0, column=6, sticky=W)
                try:
                    if runner.offers[1].price_owner == controller.current_userid:
                        # if users quote, assign amend order command
                        self.runner_containers[-1].offer2.config(bg="PaleGreen2")
                        self.runner_containers[-1].offer2.config(
                            command=lambda r=runner, o=runner.offers[1]: gui_amend_order(r, controller, o, market_id,self))
                    else:  # otherwise, place a standard trade.
                        self.runner_containers[-1].offer2.config(
                            command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                          side=1,
                                                                          market_id=market_id,
                                                                          price=r.offers[1].price))
                except IndexError:
                    pass

                try:
                    price_text = str(runner.offers[2].price)
                except IndexError:
                    price_text = ""

                self.runner_containers[-1].offer3 = Button(self.runner_containers[-1], text=price_text, width=5,
                                                           bg="gray97", bd=1,
                                                           fg="green",
                                                           relief="solid", font="helvetica 9 bold")
                self.runner_containers[-1].offer3.grid(row=0, column=7, sticky=W)
                try:
                    if runner.offers[2].price_owner == controller.current_userid:
                        # if users quote, assign amend order command
                        self.runner_containers[-1].offer3.config(bg="PaleGreen2")
                        self.runner_containers[-1].offer3.config(
                            command=lambda r=runner, o=runner.offers[2]: gui_amend_order(r, controller, o, market_id,self))
                    else:  # otherwise, place a standard trade.
                        self.runner_containers[-1].offer3.config(
                            command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                          side=1,
                                                                          market_id=market_id,
                                                                          price=r.offers[2].price))
                except IndexError:
                    pass

                # Show payoff on each outcome
                payoff_yes = int(controller.get_intrinsic_position(controller.current_userid, runner, market_id))

                self.runner_containers[-1].payoff_label = Label(self.runner_containers[-1], text=" " + str(payoff_yes),
                                                                width=5)
                self.runner_containers[-1].payoff_label.grid(row=0, column=8, columnspan=1, sticky=W)

                if payoff_yes > 0:
                    self.runner_containers[-1].payoff_label.config(font="helvetica 10 bold", fg="green")
                elif payoff_yes < 0:
                    self.runner_containers[-1].payoff_label.config(font="helvetica 10 bold", fg="red")
                else:
                    self.runner_containers[-1].payoff_label.config(font="helvetica 10", fg="blue")

                """
                FOR TRADERS --------------------------------------------------------------------------------------------
                """
                if controller.market_make is False:
                    # order entry
                    self.order_price_label = Label(self.runner_containers[-1], text="Enter Price:")
                    self.order_price_label.grid(row=0, column=10, columnspan=1, sticky=W)

                    self.runner_containers[-1].order_price_textbox = Spinbox(self.runner_containers[-1], width="5",
                                                                             from_=1,
                                                                             to=99, increment=1, repeatinterval=30)
                    self.runner_containers[-1].order_price_textbox.delete(0, "end")

                    # Set default order price to the mid, or bid+1 or offer-1 (or is none, then 100/number of runners
                    try:
                        default_price = int((runner.offers[0].price + runner.bids[0].price) / 2)
                    except IndexError:
                        try:
                            default_price = runner.bids[0].price + 1
                        except IndexError:
                            try:
                                default_price = runner.offers[0].price - 1
                            except IndexError:
                                default_price = int(round((100 / len(controller.markets[market_id - 1].runners)), 0))

                    self.runner_containers[-1].order_price_textbox.insert(0, default_price)
                    self.runner_containers[-1].order_price_textbox.grid(row=0, column=11)

                    self.order_size_label = Label(self.runner_containers[-1], text=" Volume:")
                    self.order_size_label.grid(row=0, column=12, columnspan=1, sticky=W)

                    self.runner_containers[-1].order_size_textbox = Spinbox(self.runner_containers[-1], width="5",
                                                                            from_=1,
                                                                            to=100, increment=1, repeatinterval=50)
                    self.runner_containers[-1].order_size_textbox.delete(0, "end")
                    self.runner_containers[-1].order_size_textbox.insert(0, 25)
                    self.runner_containers[-1].order_size_textbox.grid(row=0, column=13, padx=5)

                    self.sell_trade_button = ttk.Button(self.runner_containers[-1], text="Offer", width=5,
                                                        command=lambda i=runner: gui_place_order(i, controller, self,
                                                                                                 side=-1,
                                                                                                 market_id=market_id))
                    self.sell_trade_button.grid(row=0, column=15, sticky=W)

                    self.buy_trade_button = ttk.Button(self.runner_containers[-1], text="Bid", width=5,
                                                       command=lambda i=runner: gui_place_order(i, controller, self,
                                                                                                side=1,
                                                                                                market_id=market_id))
                    self.buy_trade_button.grid(row=0, column=14, sticky=W)

                    """
                    FOR MARKET MAKERS ----------------------------------------------------------------------------------
                    """
                else:

                    # order entry
                    if n_runner != len(controller.markets[market_id - 1].runners) - 1:
                        # if it is not the last runner:
                        self.order_price_label = Label(self.runner_containers[-1], text="Enter Mid Probability:")
                        self.order_price_label.grid(row=0, column=10, columnspan=1, sticky=W)

                        self.runner_containers[-1].order_price_textbox = Spinbox(self.runner_containers[-1], width="5",
                                                                                 from_=1,
                                                                                 to=99, increment=1, repeatinterval=30,
                                                                                 command=lambda: update_shadow_orders(
                                                                                     self))
                        self.runner_containers[-1].order_price_textbox.delete(0, "end")

                        try:
                            default_price = int((runner.offers[0].price + runner.bids[0].price) / 2)
                        except IndexError:
                            try:
                                default_price = runner.bids[0].price + 1
                            except IndexError:
                                try:
                                    default_price = runner.offers[0].price - 1
                                except IndexError:
                                    default_price = int(
                                        round((100 / len(controller.markets[market_id - 1].runners)), 0))

                        self.runner_containers[-1].order_price_textbox.insert(0, default_price)
                        self.runner_containers[-1].order_price_textbox.grid(row=0, column=12)

                    else:
                        # For the last runner, set the probability to sum 100
                        self.order_price_label = Label(self.runner_containers[-1], text="           Mid Probability:")
                        self.order_price_label.grid(row=0, column=10, columnspan=1, sticky=W)

                        implied_prob = 100
                        for x in self.runner_containers[:-1]:
                            implied_prob -= int(x.order_price_textbox.get())

                        implied_prob = max([0, min([100, implied_prob])])
                        self.last_price_label = Label(self.runner_containers[-1], text=str(implied_prob), width=5)
                        self.last_price_label.configure(bg="white")
                        self.last_price_label.grid(row=0, column=12, columnspan=1, sticky=W)

                    self.runner_containers[-1].bid_price_label = Label(self.runner_containers[-1], text=str(5), width=5)
                    self.runner_containers[-1].bid_price_label.configure(bg="lightblue")
                    self.runner_containers[-1].bid_price_label.grid(row=0, column=11, columnspan=1, sticky=W)

                    self.runner_containers[-1].offer_price_label = Label(self.runner_containers[-1], text=str(6),
                                                                         width=5)
                    self.runner_containers[-1].offer_price_label.configure(bg="orange")
                    self.runner_containers[-1].offer_price_label.grid(row=0, column=13, columnspan=1, sticky=W)

                # Settle Market
                if controller.current_username in controller.god_approved_users:
                    self.spacer_label = Label(self.runner_containers[-1], text="             ")
                    self.spacer_label.grid(row=0, column=17, columnspan=1, sticky=S)

                    self.settle_market_button = ttk.Button(self.runner_containers[-1], text="Settle",
                                                           command=lambda i=runner: gui_settle_market(i, controller,
                                                                                                      self,
                                                                                                      market_id=market_id))
                    self.settle_market_button.grid(row=0, column=18, sticky=W)

            # Show book percentage
            new_frame = tk.Frame(self.runner_frame, padx=5, pady=5)
            self.runner_containers.append(new_frame)
            self.runner_containers[-1].grid(row=len(controller.markets[market_id - 1].runners) + 1, column=0)

            self.spacer_label = Label(self.runner_containers[-1], text="SELL ALL ->", fg="grey70")
            self.spacer_label.grid(row=0, column=0, columnspan=1, sticky=E)

            self.runner_containers[-1].bid_arb_label = Label(self.runner_containers[-1], font="helvetica 10 bold",
                                                             fg="grey50",
                                                             text=controller.markets[market_id - 1].check_arbitrage(
                                                                 "bids"))
            self.runner_containers[-1].bid_arb_label.grid(row=0, column=1, columnspan=1, sticky=E)

            self.spacer_label = Label(self.runner_containers[-1], text=" / ", fg="grey50")
            self.spacer_label.grid(row=0, column=2, columnspan=1, sticky=E)

            self.runner_containers[-1].offer_arb_label = Label(self.runner_containers[-1], font="helvetica 10 bold",
                                                               fg="grey50",
                                                               text=controller.markets[market_id - 1].check_arbitrage(
                                                                   "offers"))
            self.runner_containers[-1].offer_arb_label.grid(row=0, column=3, columnspan=1, sticky=E)

            self.spacer_label = Label(self.runner_containers[-1], text="<- BUY ALL", fg="grey70")
            self.spacer_label.grid(row=0, column=4, columnspan=1, sticky=E)

        except IndexError:
            pass

        self.remove_orders_button = ttk.Button(self, text="Pull Unmatched", width=15,
                                               command=lambda: gui_remove_user_orders(controller, self, market_id))
        self.remove_orders_button.pack(padx=0, pady=0, expand="no", anchor=NW)

        self.instructions_button = ttk.Button(self, text="Instructions", width=15,
                                              command=lambda: gui_show_instructions())
        self.instructions_button.pack(padx=0, pady=0, expand="no", anchor=S)

        try:
            update_shadow_orders(self)
        except AttributeError:
            pass

    def refresh(self):

        def flash(self, thing_to_flash, col, to_flash):
            if to_flash:
                def revert(thing, old_b, old_f, the_self):
                    thing.config(bg=old_b, fg=old_f)
                    the_self.update_idletasks()

                old_bg = thing_to_flash['bg']
                old_fg = thing_to_flash['fg']

                self.after(0, lambda: thing_to_flash.config(bg=col, fg="white"))
                self.update_idletasks()
                self.after(1500,
                           lambda thing=thing_to_flash, old_b=old_bg, old_f=old_fg, the_self=self: revert(thing, old_b,
                                                                                                          old_f, the_self))

        def changed(new,old):
            if new != old['text']:
                return True
            else:
                return False

        controller = self.controller
        market_id = self.market_id

        for n_runner, runner in enumerate(controller.markets[market_id - 1].runners):

            # populate all order prices
            try:
                price_text = str(runner.bids[2].price)
            except IndexError:
                price_text = ""
            to_flash = changed(price_text,self.runner_containers[n_runner].bid3)
            self.runner_containers[n_runner].bid3.config(text=price_text, width=5, bg="gray97",
                                                         bd=1, fg="red",
                                                         relief="solid", font="helvetica 9 bold")
            try:
                if runner.bids[2].price_owner == controller.current_userid:
                    # if users quote, assign amend order command
                    self.runner_containers[n_runner].bid3.config(bg="LightPink1")
                    self.runner_containers[n_runner].bid3.config(
                        command=lambda r=runner, o=runner.bids[2]: gui_amend_order(r, controller, o, market_id,self))
                else:  # otherwise, place a standard trade.
                    self.runner_containers[n_runner].bid3.config(
                        command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                      side=-1,
                                                                      market_id=market_id,
                                                                      price=r.bids[2].price))
            except IndexError:
                pass

            flash(self, self.runner_containers[n_runner].bid3, "blue", to_flash)

            try:
                price_text = str(runner.bids[1].price)
            except IndexError:
                price_text = ""
            to_flash = changed(price_text, self.runner_containers[n_runner].bid2)
            self.runner_containers[n_runner].bid2.config(text=price_text, width=5, bg="gray97",
                                                         bd=2, fg="red",
                                                         relief="solid", font="helvetica 9 bold")
            try:
                if runner.bids[1].price_owner == controller.current_userid:
                    # if users quote, assign amend order command
                    self.runner_containers[n_runner].bid2.config(bg="LightPink1")
                    self.runner_containers[n_runner].bid2.config(
                        command=lambda r=runner, o=runner.bids[1]: gui_amend_order(r, controller, o, market_id,self))
                else:  # otherwise, place a standard trade.
                    self.runner_containers[n_runner].bid2.config(
                        command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                      side=-1,
                                                                      market_id=market_id,
                                                                      price=r.bids[1].price))

            except IndexError:
                pass
            flash(self, self.runner_containers[n_runner].bid2, "blue", to_flash)
            try:
                price_text = str(runner.bids[0].price)
            except IndexError:
                price_text = ""
            to_flash = changed(price_text, self.runner_containers[n_runner].bid1)
            self.runner_containers[n_runner].bid1.config(text=price_text, width=5,
                                                         font="helvetica 9 bold",
                                                         fg="red",
                                                         bg="gray97", bd=3, relief="solid")
            try:
                if runner.bids[0].price_owner == controller.current_userid:
                    # if users quote, assign amend order command
                    self.runner_containers[n_runner].bid1.config(bg="LightPink1")
                    self.runner_containers[n_runner].bid1.config(
                        command=lambda r=runner, o=runner.bids[0]: gui_amend_order(r, controller, o, market_id,self))
                else:  # otherwise, place a standard trade.
                    self.runner_containers[n_runner].bid1.config(
                        command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                      side=-1,
                                                                      market_id=market_id,
                                                                      price=r.bids[0].price))

            except IndexError:
                pass
            flash(self, self.runner_containers[n_runner].bid1, "blue", to_flash)
            try:
                price_text = str(runner.offers[0].price)
            except IndexError:
                price_text = ""
            to_flash = changed(price_text, self.runner_containers[n_runner].offer1)
            self.runner_containers[n_runner].offer1.config(text=price_text, width=5,
                                                           font="helvetica 9 bold",
                                                           fg="green",
                                                           bg="gray97", bd=3, relief="solid")
            try:
                if runner.offers[0].price_owner == controller.current_userid:
                    # if users quote, assign amend order command
                    self.runner_containers[n_runner].offer1.config(bg="PaleGreen2")
                    self.runner_containers[n_runner].offer1.config(
                        command=lambda r=runner, o=runner.offers[0]: gui_amend_order(r, controller, o, market_id,self))
                else:  # otherwise, place a standard trade.
                    self.runner_containers[n_runner].offer1.config(
                        command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                      side=1,
                                                                      market_id=market_id,
                                                                      price=r.offers[0].price))

            except IndexError:
                pass
            flash(self, self.runner_containers[n_runner].offer1, "blue", to_flash)
            try:
                price_text = str(runner.offers[1].price)
            except IndexError:
                price_text = ""
            to_flash = changed(price_text, self.runner_containers[n_runner].offer2)
            self.runner_containers[n_runner].offer2.config(text=price_text, width=5,
                                                           bg="gray97", bd=2,
                                                           fg="green",
                                                           relief="solid", font="helvetica 9 bold")
            try:
                if runner.offers[1].price_owner == controller.current_userid:
                    # if users quote, assign amend order command
                    self.runner_containers[n_runner].offer2.config(bg="PaleGreen2")
                    self.runner_containers[n_runner].offer2.config(
                        command=lambda r=runner, o=runner.offers[1]: gui_amend_order(r, controller, o, market_id,self))
                else:  # otherwise, place a standard trade.
                    self.runner_containers[n_runner].offer2.config(
                        command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                      side=1,
                                                                      market_id=market_id,
                                                                      price=r.offers[1].price))

            except IndexError:
                pass
            flash(self, self.runner_containers[n_runner].offer2, "blue", to_flash)
            try:
                price_text = str(runner.offers[2].price)
            except IndexError:
                price_text = ""
            to_flash = changed(price_text, self.runner_containers[n_runner].offer3)
            self.runner_containers[n_runner].offer3.config(text=price_text, width=5,
                                                           bg="gray97", bd=1,
                                                           fg="green",
                                                           relief="solid", font="helvetica 9 bold")

            try:
                if runner.offers[2].price_owner == controller.current_userid:
                    # if users quote, assign amend order command
                    self.runner_containers[n_runner].offer3.config(bg="PaleGreen2")
                    self.runner_containers[n_runner].offer3.config(
                        command=lambda r=runner, o=runner.offers[2]: gui_amend_order(r, controller, o, market_id,self))
                else:  # otherwise, place a standard trade.
                    self.runner_containers[n_runner].offer3.config(
                        command=lambda r=runner: gui_click_order_book(r, controller, self,
                                                                      side=1,
                                                                      market_id=market_id,
                                                                      price=r.offers[2].price))

            except IndexError:
                pass
            flash(self, self.runner_containers[n_runner].offer3, "blue", to_flash)
            # Show payoff on each outcome
            payoff_yes = int(controller.get_intrinsic_position(controller.current_userid, runner, market_id))

            self.runner_containers[n_runner].payoff_label.config(text=" " + str(payoff_yes),
                                                                  width=5)

            if payoff_yes > 0:
                self.runner_containers[n_runner].payoff_label.config(font="helvetica 10 bold", fg="green")
            elif payoff_yes < 0:
                self.runner_containers[n_runner].payoff_label.config(font="helvetica 10 bold", fg="red")
            else:
                self.runner_containers[n_runner].payoff_label.config(font="helvetica 10", fg="blue")


            if controller.market_make is False:
                """
                FOR TRADERS --------------------------------------------------------------------------------------------
                """
                self.runner_containers[n_runner].order_price_textbox.delete(0, "end")

                # Set default order price to the mid, or bid+1 or offer-1 (or is none, then 100/number of runners
                try:
                    default_price = int((runner.offers[0].price + runner.bids[0].price) / 2)
                except IndexError:
                    try:
                        default_price = runner.bids[0].price + 1
                    except IndexError:
                        try:
                            default_price = runner.offers[0].price - 1
                        except IndexError:
                            default_price = int(round((100 / len(controller.markets[market_id - 1].runners)), 0))

                self.runner_containers[n_runner].order_price_textbox.insert(0, default_price)

            else:
                """
                FOR MARKET MAKERS ----------------------------------------------------------------------------------
                """
                if n_runner != len(controller.markets[market_id - 1].runners) - 1:
                    # if it is not the last runner:
                    self.runner_containers[n_runner].order_price_textbox.delete(0, "end")

                    try:
                        default_price = int((runner.offers[0].price + runner.bids[0].price) / 2)
                    except IndexError:
                        try:
                            default_price = runner.bids[0].price + 1
                        except IndexError:
                            try:
                                default_price = runner.offers[0].price - 1
                            except IndexError:
                                default_price = int(
                                    round((100 / len(controller.markets[market_id - 1].runners)), 0))

                    self.runner_containers[n_runner].order_price_textbox.insert(0, default_price)

                else:
                    # For the last runner, set the probability to sum 100

                    implied_prob = 100
                    for x in self.runner_containers[:-1]:
                        implied_prob -= int(x.order_price_textbox.get())

                    implied_prob = max([0, min([100, implied_prob])])
                    self.last_price_label.config(text=str(implied_prob), width=5)

        # Show book percentage
        self.runner_containers[-1].bid_arb_label.config(font="helvetica 10 bold", fg="grey50",
                                                        text=controller.markets[market_id - 1].check_arbitrage("bids"))

        self.runner_containers[-1].offer_arb_label.config(font="helvetica 10 bold", fg="grey50",
                                                          text=controller.markets[market_id - 1].check_arbitrage(
                                                              "offers"))
        try:
            update_shadow_orders(self)
        except AttributeError:
            pass

        self.update_idletasks()


def gui_show_instructions():
    # TODO Update
    messagebox.showinfo("Help",
                        """    
How it works:

    The market is traded as binary options on each outcome. 
    A single contract will pay 100 if the outcome happens and 0
    if not.
    The price is equivalent to the implied probability of the
    outcome. 

    BUYING: you are betting the outcome will happen. 

        Win Payoff = Volume * (100 – Price)
        Lose Payoff = Volume * (0 – Price)

    SELLING: you are betting it won’t happen

        Win Payoff = -Volume * (0 – Price)
        Lose Payoff = -Volume * (100 – Price)


Trading:

    You can add limit orders by setting a price and volume in
    the spinboxs and then clicking “bid” (you are asking to buy)
    or “offer” (you are asking to sell). If your limit order
    can be matched in the market then a new trade will 
    automatically be created.

    If there is an order in the market already, you can click it
    to place a 10-contract limit order at that price. 
    Any available volume will be immediately matched. 

    Your unmatched quotes are highlighted in the order book 
    and can be amended by clicking on them. 

""")


def gui_switch_view(market_id, controller):
    if controller.market_make is True:
        controller.market_make = False
    else:
        controller.market_make = True

    controller.refresh_view_market(market_id)


def update_shadow_orders(gui_frame):
    def update_imp_prob(gui_frame):
        implied_prob = 100
        for x in gui_frame.runner_containers[:-1]:
            try:
                implied_prob -= int(x.order_price_textbox.get())
            except AttributeError:
                pass

        implied_prob = max([0, min([100, implied_prob])])
        gui_frame.last_price_label.configure(text=str(implied_prob))

    update_imp_prob(gui_frame)

    for x in gui_frame.runner_containers:
        try:
            bid = int(x.order_price_textbox.get()) - int(gui_frame.spread_spinbox.get())
            offer = int(x.order_price_textbox.get()) + int(gui_frame.spread_spinbox.get())
        except AttributeError:
            bid = int(gui_frame.last_price_label.cget("text")) - int(gui_frame.spread_spinbox.get())
            offer = int(gui_frame.last_price_label.cget("text")) + int(gui_frame.spread_spinbox.get())

        if bid > 99 or bid < 1:
            bid = ""
        if offer > 99 or offer < 1:
            offer = ""

        try:
            x.bid_price_label.configure(text=str(bid))
            x.offer_price_label.configure(text=str(offer))
        except AttributeError:
            pass


def post_mm_orders(gui_frame, controller, market_id):
    controller.remove_all_limit_order(controller.current_userid, market_id)
    spread = int(gui_frame.spread_spinbox.get())
    for runner, x in enumerate(gui_frame.runner_containers):
        try:
            bid = int(x.order_price_textbox.get()) - spread
            offer = int(x.order_price_textbox.get()) + spread
        except AttributeError:
            bid = int(gui_frame.last_price_label.cget("text")) - spread
            offer = int(gui_frame.last_price_label.cget("text")) + spread

        try:
            if bid != "" and bid > 0:
                user = controller.current_userid
                stake = gui_frame.order_size_spinbox.get()
                controller.add_limit_order(market_id=market_id,
                                           runner_id=runner + 1,
                                           user_id=user,
                                           price=int(bid),
                                           stake=int(stake),
                                           side=1)
        except IndexError:
            pass

        try:
            if offer != "" and offer < 100:
                user = controller.current_userid
                stake = gui_frame.order_size_spinbox.get()
                controller.add_limit_order(market_id=market_id,
                                           runner_id=runner + 1,
                                           user_id=user,
                                           price=int(offer),
                                           stake=int(stake),
                                           side=-1)
        except IndexError:
            pass

    controller.match_orders()
    gui_frame.refresh()


def gui_click_order_book(runner, controller, gui_frame, side, market_id, price):
    message_text = "Confirm Trade:\n\nSide: %s\nOutcome: %s\nPrice: %s\nVolume: 10" % (
        side_as_text(side), runner.name, price)
    if messagebox.askokcancel("Confirm Trade", message_text):
        user = controller.current_userid
        controller.add_limit_order(market_id=market_id,
                                   runner_id=runner.id,
                                   user_id=user,
                                   price=int(price),
                                   stake=10,
                                   side=side)
        controller.match_orders()
        gui_frame.refresh()


def gui_amend_order(runner, controller, order, market_id, gui_frame):
    amend_order_window = tk.Toplevel()
    amend_order_window.wm_title("Edit Order")

    order_info_label_a = tk.Label(amend_order_window, text="Outcome:\nSide")
    order_info_label_a.grid(row=0, column=0)
    order_info_label_b = tk.Label(amend_order_window, text=runner.name + "\n" + side_as_text(order.side))
    order_info_label_b.grid(row=0, column=2)

    new_price_label = tk.Label(amend_order_window, width=10, text="Price:")
    new_price_label.grid(row=1, column=0)
    new_price_spinbox = Spinbox(amend_order_window, from_=1, to=99, increment=1, repeatinterval=50, width=8)
    new_price_spinbox.delete(0, "end")
    new_price_spinbox.insert(0, order.price)
    new_price_spinbox.grid(row=1, column=2)

    new_stake_label = tk.Label(amend_order_window, width=10, text="Volume:")
    new_stake_label.grid(row=2, column=0)
    new_stake_spinbox = Spinbox(amend_order_window, from_=1, to=100, increment=1, repeatinterval=50, width=8)
    new_stake_spinbox.delete(0, "end")
    new_stake_spinbox.insert(0, order.stake)
    new_stake_spinbox.grid(row=2, column=2)

    amend_button = ttk.Button(amend_order_window, width=15, text="Edit Order",
                              command=lambda o=order, m=market_id: amend_order(o,
                                                                               new_price_spinbox,
                                                                               new_stake_spinbox,
                                                                               controller,
                                                                               amend_order_window,
                                                                               m))
    amend_button.grid(row=10, column=0)

    remove_button = ttk.Button(amend_order_window, text="Pull Order", width=15,
                               command=lambda o=order, m=market_id: pull_order(o,
                                                                               controller,
                                                                               amend_order_window,
                                                                               m))
    remove_button.grid(row=10, column=2)

    # Set location of popup
    amend_order_window.update_idletasks()
    x = controller.winfo_x()
    y = controller.winfo_y()
    w = amend_order_window.winfo_width()
    h = amend_order_window.winfo_height()
    amend_order_window.geometry("%dx%d+%d+%d" % (w, h, x + 300, y + 150))

    def pull_order(order, controller, amend_order_window, market_id):
        controller.remove_limit_order(user_id=controller.current_userid, order_id=order.order_id)
        gui_frame.refresh()
        amend_order_window.destroy()

    def amend_order(order, new_price_spinbox, new_stake_spinbox, controller, amend_order_window, market_id):
        new_price = int(new_price_spinbox.get())
        new_stake = int(new_stake_spinbox.get())
        controller.amend_limit_order(order=order,
                                     user_id=controller.current_userid,
                                     order_id=order.order_id,
                                     new_price=new_price,
                                     new_stake=new_stake)
        controller.match_orders()
        gui_frame.refresh()
        amend_order_window.destroy()


def gui_place_order(runner, controller, gui_frame, side, market_id):
    user = controller.current_userid
    price = gui_frame.runner_containers[runner.id - 1].order_price_textbox.get()
    stake = gui_frame.runner_containers[runner.id - 1].order_size_textbox.get()

    try:
        if int(price) > 0 and int(price) < 100 and float(stake) > 0 and float(stake) <= 100:
            controller.add_limit_order(market_id=market_id,
                                       runner_id=runner.id,
                                       user_id=user,
                                       price=int(price),
                                       stake=int(stake),
                                       side=side)
            controller.match_orders()
            gui_frame.refresh()
    except ValueError:
        pass


def gui_remove_user_orders(controller, gui_frame, market_id):
    user = controller.current_userid
    controller.remove_all_limit_order(user, market_id)
    gui_frame.refresh()


def gui_settle_market(runner, controller, gui_frame, market_id):
    controller.settle_market(market_id, runner.id)
    controller.show_frame(HomePage)
    controller.refresh_home()


class ControlTab(tk.Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        userid = controller.current_userid

        self.home_button = Button(self, text="Back To Markets", command=lambda: controller.refresh_home())
        self.home_button.pack(padx=0, pady=0, fill="x", anchor=N)

        self.user_summary_frame = Frame(self)
        self.user_summary_frame.pack(padx=0, pady=5, fill="x", expand=True, anchor=N)

        """ NEW ****************************************************************************************************8"""

        self.trades_summary_frame = LabelFrame(self.user_summary_frame, text="Open Trades:", relief="flat")
        self.trades_summary_frame.pack(fill="x", expand=True)

        columns = ["ID", "Trade Date", "Side", "Outcome", "Size", "Price", "Counterparty"]
        columns_size = [70, 100, 40, 100, 40, 40, 80]
        self.trades_tree = ttk.Treeview(self.trades_summary_frame, columns=columns,
                                        displaycolumns=columns,
                                        height=8, selectmode="extended")

        for n_col, col in enumerate(columns):
            self.trades_tree.heading(col, text=col)
            self.trades_tree.column(col,
                                    anchor=N,
                                    width=columns_size[n_col],
                                    minwidth=columns_size[n_col])

        markets_with_trades = list()

        for n_trade, trade in list(enumerate(controller.users[userid - 1].trades)):
            if [trade.market, trade.market_name] not in markets_with_trades and trade.settled == 0:
                markets_with_trades.append([trade.market, trade.market_name])

        markets_ids = {}

        for n_market, market in enumerate(markets_with_trades):
            markets_ids[market[0]] = self.trades_tree.insert("", market[0], text=market[1], open=False)

        for n_trade, trade in list(enumerate(controller.users[userid - 1].trades)):
            if trade.settled == 0:
                trade_details = ["Trade " + str(trade.trade_id),
                                 '{:%d-%b-%y [%H:%M]}'.format(trade.timestamp),
                                 side_as_text(trade.side),
                                 str(trade.runner_name),
                                 str(trade.stake),
                                 str(trade.price),
                                 str(trade.counterpart_name)]

                self.trades_tree.insert(markets_ids[trade.market], n_trade, values=trade_details, open=False)

        self.tree_scroll = ttk.Scrollbar(self.trades_summary_frame, orient="vertical",
                                         command=self.trades_tree.yview)
        self.trades_tree.configure(yscrollcommand=self.tree_scroll.set)
        self.trades_tree.pack(side=LEFT, anchor=W)
        self.tree_scroll.pack(fill=Y, side=LEFT, anchor=W)

        """ CLODED TRADES"""

        self.trades_summary_frame2 = LabelFrame(self.user_summary_frame, text="Closed Trades:", relief="flat")
        self.trades_summary_frame2.pack(fill="x", expand=True)

        columns = ["ID", "Trade Date", "Side", "Outcome", "Size", "Price", "Counterparty", "P&L"]
        columns_size = [70, 100, 40, 100, 40, 40, 80, 55]
        self.trades_tree2 = ttk.Treeview(self.trades_summary_frame2, columns=columns,
                                         displaycolumns=columns,
                                         height=16, selectmode="extended")

        for n_col, col in enumerate(columns):
            self.trades_tree2.heading(col, text=col)
            self.trades_tree2.column(col,
                                     anchor=N,
                                     width=columns_size[n_col],
                                     minwidth=columns_size[n_col])

        markets_with_trades = list()

        for n_trade, trade in list(enumerate(controller.users[userid - 1].trades)):
            if [trade.market, trade.market_name] not in markets_with_trades and trade.settled != 0:
                markets_with_trades.append([trade.market, trade.market_name])

        markets_ids = {}
        markets_ids_pnls = {}

        for n_market, market in enumerate(markets_with_trades):
            markets_ids[market[0]] = self.trades_tree2.insert("", market[0], text=market[1], open=False)
            markets_ids_pnls[market[0]] = 0

        for n_trade, trade in list(enumerate(controller.users[userid - 1].trades)):
            if trade.settled != 0:
                markets_ids_pnls[trade.market] += trade.settled
                trade_details = ["Trade " + str(trade.trade_id),
                                 '{:%d-%b-%y [%H:%M]}'.format(trade.timestamp),
                                 side_as_text(trade.side),
                                 str(trade.runner_name),
                                 str(trade.stake),
                                 str(trade.price),
                                 str(trade.counterpart_name),
                                 str(trade.settled)]

                self.trades_tree2.insert(markets_ids[trade.market], n_trade, values=trade_details, open=False)

        for n_market, market in enumerate(markets_with_trades):
            self.trades_tree2.item(markets_ids[market[0]],
                                   values=['', '', '', '', '', '', '', markets_ids_pnls[market[0]]])

        self.tree_scroll2 = ttk.Scrollbar(self.trades_summary_frame2, orient="vertical",
                                          command=self.trades_tree2.yview)
        self.trades_tree2.configure(yscrollcommand=self.tree_scroll2.set)
        self.trades_tree2.pack(side=LEFT, anchor=W)
        self.tree_scroll2.pack(fill=Y, side=LEFT, anchor=W)

        """ NEW ****************************************************************************************************8"""

        # print all user open / setteled trades to GUI


        self.buttons_frame = LabelFrame(self.user_summary_frame, text="")
        self.buttons_frame.pack(anchor=W)

        self.print_markets_button = ttk.Button(self.buttons_frame, text="All Markets", width=12,
                                               command=lambda: controller.print_markets_info())
        self.print_markets_button.grid(row=0, column=0, padx=5, sticky=NW)

        if controller.current_username in controller.god_approved_users:  # Only admin can print all users
            self.print_users_button = ttk.Button(self.buttons_frame, text="All Users", width=12,
                                                 command=lambda: controller.print_users_info())
            self.print_users_button.grid(row=0, column=1, padx=5, sticky=NW)

        self.print_users_button = ttk.Button(self.buttons_frame, text="My Trades", width=12,
                                             command=lambda: controller.users[
                                                 controller.current_userid - 1].print_trades())
        self.print_users_button.grid(row=0, column=2, padx=5, sticky=NW)

        self.print_orders_button = ttk.Button(self.buttons_frame, text="My Orders", width=12,
                                              command=lambda: controller.users[
                                                  controller.current_userid - 1].print_open_orders())
        self.print_orders_button.grid(row=0, column=3, padx=5, sticky=NW)
