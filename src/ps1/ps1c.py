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



def get_best_saving_rate():
    """
    Calculate the duration of saving to cover a downpayment on a house in months

    Returns:
        int -- number of months needed to save for a downpaymnet on the house
    """
    semi_annual_raise = 0.07
    r = 0.04
    downpayment_rate = 0.25
    total_cost = 1000000
    downpayment = total_cost * downpayment_rate

    starting_salary = int(input('Enter the starting salary: '))
    
    current_savings = 0
    steps = 0
    high = 10000
    low = 0
    mid = (high + low) // 2
    epsilon = 100

    if 3 * starting_salary < downpayment:
        print('It is not possible to pay the down payment in three years.')
    else:

        while abs(current_savings - downpayment) > epsilon:

            current_savings = 0

            portion_saved = mid / 10000

            for i in range(1, 37):
                annual_salary = starting_salary
                
                current_savings += get_monthly_saving(current_savings, r, annual_salary, portion_saved)

                if i % 6 == 0:
                    annual_salary = annual_salary * (1 + semi_annual_raise)

            if current_savings > downpayment + epsilon:
                high = mid
            elif current_savings < downpayment + epsilon:
                low = mid
            mid = (high + low) // 2
            
            steps += 1

        print('Best saving rate:', portion_saved)
        print('Steps in bisection search:', steps)

get_best_saving_rate()