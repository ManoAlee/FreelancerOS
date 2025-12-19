
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FreelancerOS: Business & Financial Tools (70 Tools)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def calc_profit_margin(revenue, cost): return (revenue - cost) / revenue * 100
def calc_markup(cost, price): return (price - cost) / cost * 100
def calc_break_even(fixed_costs, price_per_unit, cost_per_unit): return fixed_costs / (price_per_unit - cost_per_unit)
def calc_roi(gain, cost): return (gain - cost) / cost * 100
def calc_yearly_salary(hourly_rate, hours_per_week=40): return hourly_rate * hours_per_week * 52
def calc_hourly_rate(yearly_salary, hours_per_week=40): return yearly_salary / (hours_per_week * 52)
def calc_tax_amount(income, tax_rate): return income * (tax_rate / 100)
def calc_net_income(gross, tax): return gross - tax
def calc_simple_interest(principal, rate, time): return principal * rate * time
def calc_compound_interest(principal, rate, time, n=12): return principal * ((1 + rate/n) ** (n*time))
def estimate_project_days(hours, hours_per_day): return hours / hours_per_day
def estimate_project_cost(hours, rate): return hours * rate
def calc_discount_price(price, discount_percent): return price * (1 - discount_percent/100)
def calc_sales_tax(price, tax_rate): return price * (tax_rate / 100)
def calc_gross_profit(revenue, cogs): return revenue - cogs
def calc_operating_margin(operating_income, revenue): return operating_income / revenue
def calc_ebitda(net_income, interest, taxes, dep, amort): return net_income + interest + taxes + dep + amort
def calc_burn_rate(starting_balance, ending_balance, months): return (starting_balance - ending_balance) / months
def calc_runway(balance, burn_rate): return balance / burn_rate
def calc_customer_acquisition_cost(marketing_spend, new_customers): return marketing_spend / new_customers
def calc_churn_rate(lost_customers, total_customers): return (lost_customers / total_customers) * 100
def calc_lifetime_value(avg_purchase, frequency, lifespan): return avg_purchase * frequency * lifespan
def calc_conversion_rate(conversions, visitors): return (conversions / visitors) * 100
def calc_average_order_value(revenue, orders): return revenue / orders
def calc_working_capital(assets, liabilities): return assets - liabilities
def calc_current_ratio(assets, liabilities): return assets / liabilities
def calc_quick_ratio(assets, inventory, liabilities): return (assets - inventory) / liabilities
def calc_debt_to_equity(debt, equity): return debt / equity
def calc_inventory_turnover(cogs, avg_inventory): return cogs / avg_inventory
def calc_days_sales_outstanding(receivables, credit_sales, days=365): return (receivables / credit_sales) * days
def calc_retention_rate(end_cust, new_cust, start_cust): return ((end_cust - new_cust) / start_cust) * 100
def calc_net_promoter_score(promoters, detractors, total): return ((promoters - detractors) / total) * 100
def calc_lead_value(total_value, total_leads): return total_value / total_leads
def calc_click_through_rate(clicks, impressions): return (clicks / impressions) * 100
def calc_cpc(cost, clicks): return cost / clicks
def calc_cpm(cost, impressions): return (cost / impressions) * 1000
def calc_cpl(cost, leads): return cost / leads
def calc_roas(revenue, ad_spend): return revenue / ad_spend
def calc_bounce_rate(single_page_visits, total_visits): return (single_page_visits / total_visits) * 100
def calc_monthly_recurring_revenue(users, avg_revenue): return users * avg_revenue
def calc_arr(mrr): return mrr * 12
def calc_employee_turnover(departures, avg_employees): return (departures / avg_employees) * 100
def calc_absenteeism(missed_days, total_days): return (missed_days / total_days) * 100
def calc_revenue_per_employee(revenue, employees): return revenue / employees
def calc_profit_per_employee(profit, employees): return profit / employees
def convert_usd_to_eur(usd, rate=0.92): return usd * rate
def convert_eur_to_usd(eur, rate=1.09): return eur * rate
def convert_usd_to_brl(usd, rate=5.0): return usd * rate
def convert_brl_to_usd(brl, rate=0.20): return brl * rate
def calc_overtime_pay(hourly_rate, overtime_hours, multiplier=1.5): return hourly_rate * multiplier * overtime_hours
def calc_freelance_tax_deduction(income, deduction_rate=0.3): return income * deduction_rate # Rough estimate
def calc_savings_goal(goal, monthly_saving): return goal / monthly_saving
def calc_loan_payment(principal, rate, months):
    r = rate / 1200
    return principal * (r * (1+r)**months) / ((1+r)**months - 1)
def calc_depreciation_straight_line(cost, salvage, life): return (cost - salvage) / life
def calc_double_declining_balance(cost, acc_dep, life): return 2 * (cost - acc_dep) / life
def calc_units_of_production(cost, salvage, life_units, produced): return ((cost - salvage) / life_units) * produced
def calc_market_cap(shares, price): return shares * price
def calc_eps(net_income, dividends, shares): return (net_income - dividends) / shares
def calc_pe_ratio(price, eps): return price / eps
def calc_dividend_yield(dividend, price): return dividend / price
def calc_payout_ratio(dividends, net_income): return dividends / net_income
def calc_book_value(assets, liabilities): return assets - liabilities
def calc_price_to_book(price, book_value): return price / book_value
def calc_enterprise_value(market_cap, debt, cash): return market_cap + debt - cash
def calc_free_cash_flow(operating_cash, cap_ex): return operating_cash - cap_ex
def calc_operating_cycle(days_inventory, days_receivables): return days_inventory + days_receivables
def calc_cash_conversion_cycle(days_inventory, days_receivables, days_payables): return days_inventory + days_receivables - days_payables
def calc_degree_operating_leverage(contribution_margin, noi): return contribution_margin / noi
def calc_degree_financial_leverage(ebit, ebt): return ebit / ebt
def calc_breakeven_units(fixed, price, var_cost): return fixed / (price - var_cost)
