def get_monthly_saving(current_savings, r, annual_salary, portion_saved):
    """
    Calculate the increase of savings after each month

    Parameters:
        current_savings (float) -- amount of money saved
        r (float) -- annual return on investment rate
        annual_salary (float) -- annual income
        portion_saved (float) -- portion of income to save every month

    Returns:
        float -- increase in current savings after one month
    """
    return_on_investment = current_savings * r / 12
    monthly_salary = annual_salary / 12
    monthly_saving = monthly_salary * portion_saved

    increase_in_savings = return_on_investment + monthly_saving

    return increase_in_savings



def get_saving_time(portion_down_payment=0.25, r=0.04):
    """
    Calculate the duration of saving to cover a downpayment on a house in months

    Parameters:
        portion_down_payment (float) -- the portion of total house cost as downpayment, default=0.25
        r (float) -- return on investment rate, default=0.04
    
    Returns:
        int -- number of months needed to save for a downpaymnet on the house
    """
    # initiate current savings and n_months
    current_savings = 0
    n_months = 0

    # take the input of the missing information
    annual_salary = float(input("Enter your annual salary: "))
    portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))
    total_cost = float(input("Enter the cost of your dream home: "))
    semi_annual_raise = float(input("Enter the semi-annual raise, as a decimal: "))

    # calculate downpayment cost
    down_payment = total_cost * portion_down_payment

    # loop until current savings >= downpayment
    while current_savings < down_payment:
        # calculate monthly savings
        increase_in_savings = get_monthly_saving(current_savings, r, annual_salary, portion_saved)
        
        # recalculate current savings
        current_savings += increase_in_savings
        n_months += 1

        # increase the annual salary every 6 months
        if n_months % 6 == 0:
            annual_salary = annual_salary * (1 + semi_annual_raise)

    return n_months


print("Number of months:", get_saving_time())