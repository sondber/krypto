import csv
import math
from datetime import date

import numpy as np

import linreg


def final_three_rows(print_rows, n_obs_array, rsquared_array, aic_array, n_cols, n_rows, double_cols=0):
    # Dette fikser de tre nedreste radene

    for c in range(0, n_cols):
        n_obs = str(int(n_obs_array[c]))
        r2 = "{0:.3f}".format(rsquared_array[c])

        if aic_array[c] > 0:
            aic = str(int(aic_array[c]))
        else:
            aic = "$-$" + str(int(abs(aic_array[c])))

        print_rows[n_rows - 3] += "   " + n_obs
        for i in range(8 - len(n_obs)):
            print_rows[n_rows - 3] += " "
        print_rows[n_rows - 3] += "&"

        print_rows[n_rows - 2] += "   " + r2
        for i in range(8 - len(r2)):
            print_rows[n_rows - 2] += " "
        print_rows[n_rows - 2] += "&"

        print_rows[n_rows - 1] += " " + aic

        for i in range(10 - len(aic)):
            print_rows[n_rows - 1] += " "
        print_rows[n_rows - 1] += "&"

        if c % 2 == 1:
            if double_cols == 1:
                print_rows[n_rows - 3] += " &"
                print_rows[n_rows - 2] += " &"
                print_rows[n_rows - 1] += " &"

    return print_rows


def final_print_regressions_latex(print_rows):
    tightness = 1  #
    t_string = "[-" + str(tightness) + "ex]"

    for i in range(0, len(print_rows)):
        count = 0
        while (print_rows[i][len(print_rows[i]) - 1] == " " or print_rows[i][
                len(print_rows[i]) - 1] == "&") and count < 10:
            print_rows[i] = print_rows[i][0:len(print_rows[i]) - 1]
            count += 1
        if i == len(print_rows) - 3:
            print("        \\hline")
        if i < len(print_rows) - 3:
            if i % 2 == 0:
                print(print_rows[
                          i] + "  \\\\" + t_string)  # Fjerner det siste &-tegnet og legger til backslash og tightness
            else:
                print(print_rows[i] + "  \\\\")  # Fjerner det siste &-tegnet og legger til backslash
        else:
            print(print_rows[i] + "  \\\\" + "[-0.5ex]")  # Fjerner det siste &-tegnet og legger til backslash
    print()
    print()


def fill_blanks(in_list):
    out_list = in_list
    n = len(in_list)
    startlim = 60  # How many minutes of zero at the beginning of the list do we allow? i.e. if there is more than startlim zeros, we let them stay zero
    for i in range(0, n):
        try:
            if in_list[i] == 0:
                if i == 0:
                    j = 0
                    while in_list[j] == 0 and j < startlim:
                        j = j + 1
                    out_list[0] = in_list[j]
                else:
                    out_list[i] = in_list[i - 1]
        except IndexError:
            out_list[i] = in_list[i - 1]
            print("\033[0;31;0mThere was a problem on row %i \033[0;0;0m" % i)
    return out_list


def move_time_list(year, month, day, hour, minute, move_n_hours=0, single_time_stamp=0):
    if single_time_stamp == 1:
        if move_n_hours < 0:  # Funker ikke for single_time_stamp
            n = -move_n_hours
            if hour >= n:
                hour -= n
            else:
                hour = 24 - n + hour
                if day >= 2:
                    day -= 1
                else:  # I use "mo" and "y" for brevity, and let the long version be assigned at the end
                    if month == 1:
                        mo = 12
                        y = year - 1
                    else:
                        mo = month - 1
                        y = year
                    if mo == 1 or mo == 3 or mo == 5 or mo == 7 or mo == 8 or mo == 10 or mo == 12:
                        n_days = 31
                    elif mo == 2:
                        if y % 4 == 0:
                            n_days = 29
                        else:
                            n_days = 28
                    else:
                        n_days = 30
                    day = n_days
                    month = mo
                    year = y
        elif move_n_hours > 0:
            n = move_n_hours
            if hour <= 23 - n:
                hour += n
            else:
                hour = n + (hour - 24)
                mo = month
                y = year
                if mo == 1 or mo == 3 or mo == 5 or mo == 7 or mo == 8 or mo == 10 or mo == 12:
                    n_days = 31
                elif mo == 2:
                    if y % 4 == 0:
                        n_days = 29
                    else:
                        n_days = 28
                else:
                    n_days = 30

                if day < n_days:
                    day += 1
                else:
                    day = 1
                    if mo == 12:
                        month = 1
                        year += 1
                    else:
                        month += 1
    else:
        n_entries = len(year)
        if move_n_hours < 0:  # Funker ikke for single_time_stamp
            n = -move_n_hours
            for i in range(0, n_entries):
                if hour[i] >= n:
                    hour[i] -= n
                else:
                    hour[i] = 24 - n + hour[i]
                    if day[i] >= 2:
                        day[i] -= 1
                    else:  # I use "mo" and "y" for brevity, and let the long version be assigned at the end
                        if month[i] == 1:
                            mo = 12
                            y = year[i] - 1
                        else:
                            mo = month[i] - 1
                            y = year[i]
                        if mo == 1 or mo == 3 or mo == 5 or mo == 7 or mo == 8 or mo == 10 or mo == 12:
                            n_days = 31
                        elif mo == 2:
                            if y % 4 == 0:
                                n_days = 29
                            else:
                                n_days = 28
                        else:
                            n_days = 30
                        day[i] = n_days
                        month[i] = mo
                        year[i] = y
        elif move_n_hours > 0:
            n = move_n_hours
            for i in range(0, n_entries):
                if hour[i] <= 23 - n:
                    hour[i] += n
                else:
                    hour[i] = n + (hour[i] - 24)

                    mo = month[i]
                    y = year[i]
                    if mo == 1 or mo == 3 or mo == 5 or mo == 7 or mo == 8 or mo == 10 or mo == 12:
                        n_days = 31
                    elif mo == 2:
                        if y % 4 == 0:
                            n_days = 29
                        else:
                            n_days = 28
                    else:
                        n_days = 30

                    if day[i] < n_days:
                        day[i] += 1
                    else:
                        day[i] = 1
                        if mo == 12:
                            month[i] = 1
                            year[i] += 1
                        else:
                            month[i] += 1

    return year, month, day, hour, minute


def fix_time_list(time_list, move_n_hours=0, single_time_stamp=0):
    day = []
    month = []
    year = []
    hour = []
    minute = []
    if single_time_stamp == 0:
        for i in range(0, len(time_list)):
            day.append(int(time_list[i][0:2]))
            month.append(int(time_list[i][3:5]))
            year.append(int(time_list[i][6:10]))
            hour.append(int(time_list[i][11:13]))
            minute.append(int(time_list[i][14:16]))

    else:
        day = (int(time_list[0:2]))
        month = (int(time_list[3:5]))
        year = (int(time_list[6:10]))
        hour = (int(time_list[11:13]))
        minute = (int(time_list[14:16]))

    if move_n_hours != 0:
        year, month, day, hour, minute = move_time_list(year, month, day, hour, minute, move_n_hours=move_n_hours,
                                                        single_time_stamp=single_time_stamp)

    return year, month, day, hour, minute


def make_time_list(year, month, day, hour, minute):
    time_list_out = []
    for i in range(len(minute)):
        stamp = ""
        d = day[i]
        m = month[i]
        y = year[i]
        h = hour[i]
        mi = minute[i]

        if d < 10:
            stamp += "0" + str(d)
        else:
            stamp += str(d)
        stamp += "."
        if m < 10:
            stamp += "0" + str(m)
        else:
            stamp += str(m)
        stamp += "."
        stamp += str(y)
        stamp += " "
        if h < 10:
            stamp += "0" + str(h)
        else:
            stamp += str(h)
        stamp += ":"
        if mi < 10:
            stamp += "0" + str(mi)
        else:
            stamp += str(mi)

        time_list_out.append(stamp)
    return time_list_out


def data_analysis(in_list, number_of_intervals):
    b = number_of_intervals
    interval = max(in_list) / b
    print("With an interval size of %0.1f" % interval)
    int_count = np.zeros(b)
    maximum = max(in_list)
    print("The highest value in the dataset is = " + str(max(in_list)))
    print()
    lower = 0
    upper = interval
    i = 0

    while lower <= maximum:
        int_count[i] = (sum(float(num) <= upper for num in in_list)) - (sum(float(num) <= lower for num in in_list))
        print("There are %i minutes with values between %0.1f and %0.1f" % (int_count[i], lower, upper))
        lower = lower + interval
        upper = upper + interval
        i = i + 1
    int_count[0] = int_count[0] + (sum(float(num) == 0 for num in in_list))  # include the minutes with no trading


def moving_variance(price, mins_rolling):
    returns = logreturn(price)
    var = np.zeros(len(price))
    rolling_list = np.zeros(mins_rolling)  # rolling list
    for k in range(mins_rolling):
        rolling_list[k] = returns[k]
    var[mins_rolling - 1] = np.var(rolling_list)
    for i in range(len(returns) - mins_rolling + 1):
        j = mins_rolling + i - 1
        rolling_list[j % mins_rolling] = returns[j]
        var[j] = np.var(rolling_list)
        if i % 100000 == 0 and i != 0:
            perc = str(round(100 * i / len(price), 2)) + "%"
            print("%s" % perc)
    print("100%")
    return var


def logreturn(price):
    returnlist = np.zeros(len(price))
    for i in range(1, len(price)):
        try:
            returnlist[i] = math.log(price[i]) - math.log(price[i - 1])
        except ValueError:
            returnlist[i] = 0
    return returnlist


def make_totals(volumes, prices):  # Has to be all in USD
    print("Generating totals..")
    num_exchanges = np.size(volumes, 0)
    entries = np.size(volumes, 1)
    total_volume = np.zeros(entries)
    total_price = np.zeros(entries)
    for i in range(0, entries):
        total_volume[i] = sum(volumes[:, i])
        if total_volume[i] == 0:
            total_price[i] = total_price[i - 1]
        else:
            for j in range(0, num_exchanges):
                total_price[i] = (prices[j, i] * volumes[j, i]) + total_price[i]
            total_price[i] = float(total_price[i]) / float(total_volume[i])
    if total_price[0] == 0:
        r = 0
        while total_price[r] == 0:
            r = r + 1
        while r > 0:
            total_price[r - 1] = total_price[r]
            r = r - 1
    return total_volume, total_price


def convert_currencies(exchanges, prices):
    print("Converting currencies...")
    currency_handle = []
    for i in range(0, len(exchanges)):
        exc_name = exchanges[i]
        currency_handle.append(exc_name[len(exc_name) - 3: len(exc_name)])

    # her må vi legge inn valutakurser per dag/time/minutt og konvertere ordentlig. Dette er jalla som faen
    for i in range(0, len(exchanges)):
        if currency_handle[i] == "jpy":
            prices[i, :] = prices[i, :] / 112
        elif currency_handle[i] == "cny":
            prices[i, :] = prices[i, :] / 6.62
        elif currency_handle[i] == "eur":
            prices[i, :] = prices[i, :] * 1.19

    print("All prices converted to USD")
    prices_in_usd = prices
    return prices_in_usd


def count_rows(file_name):
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        n_rows = 0
        for row in reader:
            n_rows = n_rows + 1
        n_rows = int(n_rows)
    return n_rows


def get_ticks(time_list, number_of_ticks):
    n = number_of_ticks
    n_mins = len(time_list)
    x = np.arange(0, n_mins + 1, n_mins / (n - 1))
    myticks = []
    for i in range(0, n + 1):
        time_row = min(int((n_mins / (n - 1)) * i), n_mins - 1)
        timestamp = time_list[time_row]
        timestamp = timestamp[0:10]
        myticks.append(timestamp)
    return x, myticks


def get_rolls():
    file_name = "data/export_csv/relative_spreads_hourly.csv"
    rolls = []
    time_list = []
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        print("\033[0;32;0m Reading file '%s'...\033[0;0;0m" % file_name)
        i = 0
        next(reader)
        for row in reader:
            try:
                time_list.append(row[0])
            except ValueError:
                print("\033[0;31;0m There was an error on row %i in '%s'\033[0;0;0m" % (i + 1, file_name))
            try:
                rolls.append(float(row[1]))
            except ValueError:
                rolls.append(0)
            i = i + 1
        return time_list, rolls


def remove_list1_zeros_from_all_lists(time_list, time_list_removed_previous, list1, list2=[], list3=[], list4=[],
                                      list5=[], list6=[]):
    # threshold is in number of standard deviations
    # only chekcs for positive deviations
    t_list2 = False
    t_list3 = False
    t_list4 = False
    t_list5 = False
    t_list6 = False
    if len(list2) > 1:
        t_list2 = True
    if len(list3) > 1:
        t_list3 = True
    if len(list4) > 1:
        t_list4 = True
    if len(list5) > 1:
        t_list5 = True
    if len(list6) > 1:
        t_list6 = True

    time_list_removed = time_list_removed_previous  # from previous
    time_list_out = []
    n_in = len(list1)
    out_list1 = []
    if t_list2:
        out_list2 = []
        if len(list2) != n_in:
            print("Wrong length of list2!", len(list2), "instead of", n_in)
    if t_list3:
        out_list3 = []
        if len(list3) != n_in:
            print("Wrong length of list3!", len(list3), "instead of", n_in)
    if t_list4:
        out_list4 = []
        if len(list4) != n_in:
            print("Wrong length of list4!", len(list4), "instead of", n_in)
    if t_list5:
        out_list5 = []
        if len(list5) != n_in:
            print("Wrong length of list5!", len(list5), "instead of", n_in)
    if t_list6:
        out_list6 = []
        if len(list6) != n_in:
            print("Wrong length of list6!", len(list6), "instead of", n_in)
    for i in range(0, n_in):
        if list1[i] > 0 and not math.isinf(list1[i]):
            time_list_out.append(time_list[i])
            out_list1.append(list1[i])
            if t_list2:
                out_list2.append(list2[i])
            if t_list3:
                out_list3.append(list3[i])
            if t_list4:
                out_list4.append(list4[i])
            if t_list5:
                out_list5.append(list5[i])
            if t_list6:
                out_list6.append(list6[i])
        else:
            time_list_removed = np.append(time_list_removed, time_list[i])
    if t_list6:
        return time_list_out, time_list_removed, out_list1, out_list2, out_list3, out_list4, out_list5, out_list6
    elif t_list5:
        return time_list_out, time_list_removed, out_list1, out_list2, out_list3, out_list4, out_list5
    elif t_list4:
        return time_list_out, time_list_removed, out_list1, out_list2, out_list3, out_list4
    elif t_list3:
        return time_list_out, time_list_removed, out_list1, out_list2, out_list3
    elif t_list2:
        return time_list_out, time_list_removed, out_list1, out_list2
    else:
        return time_list_out, time_list_removed, out_list1


def autocorr(in_list, lag):
    n = len(in_list)
    list1 = in_list[0: n - lag]
    list2 = in_list[lag: n]
    corr = np.corrcoef(list1, list2)[0, 1]
    return corr


def mean_for_n_entries(in_list, n_lag):
    n_in = len(in_list)
    out_list = np.zeros(n_in - n_lag)
    initial_mean = np.mean(in_list[0:n_lag])
    out_list[0] = initial_mean
    for i in range(1, n_lag):
        out_list[i] = (initial_mean * (n_lag - i) + i * np.mean(in_list[n_lag - 1:n_lag - 1 + i])) / (n_lag - 1)
    for i in range(n_lag, n_in - n_lag):
        out_list[i] = np.mean(in_list[i: i + n_lag])
    return out_list


def standardize(in_list):
    mean = np.mean(in_list)
    out_list = in_list - mean
    std = np.std(in_list)
    out_list = np.divide(out_list, std)

    return out_list


def week_vars(time_list, move_n_hours=0):
    year, month, day, hour, minute = fix_time_list(time_list, move_n_hours=move_n_hours)
    n_entries = len(time_list)

    mon = np.zeros(n_entries)
    tue = np.zeros(n_entries)
    wed = np.zeros(n_entries)
    thu = np.zeros(n_entries)
    fri = np.zeros(n_entries)
    sat = np.zeros(n_entries)
    sun = np.zeros(n_entries)
    day_string = []
    for i in range(0, n_entries):
        daynum = int(date(year[i], month[i], day[i]).isoweekday()) - 1
        if daynum == 0:
            mon[i] = 1
        elif daynum == 1:
            tue[i] = 1
        elif daynum == 2:
            wed[i] = 1
        elif daynum == 3:
            thu[i] = 1
        elif daynum == 4:
            fri[i] = 1
        elif daynum == 5:
            sat[i] = 1
        elif daynum == 6:
            sun[i] = 1
    return mon, tue, wed, thu, fri, sat, sun


def import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                       std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array):
    for j in range(0, len(coeffs)):
        coeff_matrix[j, m_col] = coeffs[j]
        std_errs_matrix[j, m_col] = std_errs[j]
        p_values_matrix[j, m_col] = p_values[j]
    rsquared_array[m_col] = rsquared
    aic_array[m_col] = aic
    n_obs_array[m_col] = n_obs
    return coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array


def print_n(n):
    for k in range(n + 1):
        print()


def import_regressions(m_col, Y, X, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array,
                       n_obs_array, prints=0, intercept=1):
    coeffs, tvalues, rsquared, aic, p_values, std_errs, n_obs = linreg.reg_multiple(Y, X, intercept=intercept,
                                                                                    prints=prints)
    coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array = \
        import_to_matrices(m_col, coeffs, std_errs, p_values, rsquared, aic, n_obs, coeff_matrix,
                           std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array)
    m_col += 1
    return m_col, coeff_matrix, std_errs_matrix, p_values_matrix, rsquared_array, aic_array, n_obs_array


def fmt_print(print_loc, data, p_value=1, type="coeff"):
    if type == "coeff":
        if data >= 0:
            print_loc += "   "
        else:
            print_loc += "$-$"

        if abs(data) < 10:
            print_loc += "{0:.4f}".format(abs(data))
        else:
            print_loc += "{0:.3f}".format(abs(data))

        if p_value <= 0.01:
            stars = "**"
        elif p_value <= 0.05:
            stars = "* "
        else:
            stars = "  "
        print_loc += stars + "&"

    elif type == "std_err":
        print_loc += "  (" + str("{0:.3f}".format(data)) + ")" + "  &"
    else:
        pass

    return print_loc


def remove_extremes(time_list, data, threshold_upper, threshold_lower=0):
    for i in range(len(data)):
        if data[i] > threshold_upper or data[i] < threshold_lower:
            time_list.append(i)
    return time_list


def find_date_index(cutoff_date, time_list_hours):
    c_year, c_month, c_day, c_hour, c_minute = fix_time_list(cutoff_date, single_time_stamp=1)
    year, month, day, hour, minute = fix_time_list(time_list_hours)

    # print("cutoff: ", c_year, c_month, c_day, c_hour, c_minute)

    index = 0
    while year[index] < c_year:
        index += 1
    while month[index] < c_month:
        index += 1
    while day[index] < c_day:
        index += 1
    while hour[index] < c_hour:
        index += 1
    while minute[index] < c_minute:
        index += 1

    # print("The cutoff is", time_listH[index])
    return index


def time_of_day_dummies(time_list, hours_in_period=4):
    hour = fix_time_list(time_list)[3]
    n = len(time_list)

    if hours_in_period == 2:
        first = np.zeros(n)
        second = np.zeros(n)
        third = np.zeros(n)
        fourth = np.zeros(n)
        fifth = np.zeros(n)
        sixth = np.zeros(n)
        seventh = np.zeros(n)
        eigth = np.zeros(n)
        nineth = np.zeros(n)
        tenth = np.zeros(n)
        eleventh = np.zeros(n)
        twelwth = np.zeros(n)

        first_period = [0, 1]
        second_period = [2, 3]
        third_period = [4, 5]
        fourth_period = [6, 7]
        fifth_period = [8, 9]
        sixth_period = [10, 11]
        seventh_period = [12, 13]
        eighth_period = [14, 15]
        nineth_period = [16, 17]
        tenth_period = [18, 19]
        eleventh_period = [20, 21]
        twelwth_period = [22, 23]

        for i in range(0, n):
            hr = hour[i]
            if hr in first_period:
                first[i] = 1
            elif hr in second_period:
                second[i] = 1
            elif hr in third_period:
                third[i] = 1
            elif hr in fourth_period:
                fourth[i] = 1
            elif hr in fifth_period:
                fifth[i] = 1
            elif hr in sixth_period:
                sixth[i] = 1
            elif hr in seventh_period:
                seventh[i] = 1
            elif hr in eighth_period:
                eigth[i] = 1
            elif hr in nineth_period:
                nineth[i] = 1
            elif hr in tenth_period:
                tenth[i] = 1
            elif hr in eleventh_period:
                eleventh[i] = 1
            elif hr in twelwth_period:
                twelwth[i] = 1

        X_dummies = np.matrix(first)
        X_dummies = np.append(X_dummies, np.matrix(second), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(third), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(fourth), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(fifth), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(sixth), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(seventh), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(eigth), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(nineth), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(tenth), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(eleventh), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(twelwth), axis=0)
        X_dummies = np.transpose(X_dummies)

        n_dummies = 12  # Antall forklaringsvariable

    elif hours_in_period == 3:
        first = np.zeros(n)
        second = np.zeros(n)
        third = np.zeros(n)
        fourth = np.zeros(n)
        fifth = np.zeros(n)
        sixth = np.zeros(n)
        seventh = np.zeros(n)
        eigth = np.zeros(n)

        first_period = [0, 1, 2]
        second_period = [3, 4, 5]
        third_period = [6, 7, 8]
        fourth_period = [9, 10, 11]
        fifth_period = [12, 13, 14]
        sixth_period = [15, 16, 17]
        seventh_period = [18, 19, 20]
        eighth_period = [21, 22, 23]

        for i in range(0, n):
            hr = hour[i]
            if hr in first_period:
                first[i] = 1
            elif hr in second_period:
                second[i] = 1
            elif hr in third_period:
                third[i] = 1
            elif hr in fourth_period:
                fourth[i] = 1
            elif hr in fifth_period:
                fifth[i] = 1
            elif hr in sixth_period:
                sixth[i] = 1
            elif hr in seventh_period:
                seventh[i] = 1
            elif hr in eighth_period:
                eigth[i] = 1

        X_dummies = np.matrix(first)
        X_dummies = np.append(X_dummies, np.matrix(second), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(third), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(fourth), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(fifth), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(sixth), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(seventh), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(eigth), axis=0)
        X_dummies = np.transpose(X_dummies)

        n_dummies = 8  # Må bare være minst like stor som antall forklaringsvariable

    elif hours_in_period == 4:
        first = np.zeros(n)
        second = np.zeros(n)
        third = np.zeros(n)
        fourth = np.zeros(n)
        fifth = np.zeros(n)
        sixth = np.zeros(n)

        first_period = [0, 1, 2, 3]
        second_period = [4, 5, 6, 7]
        third_period = [8, 9, 4, 11]
        fourth_period = [12, 13, 14, 15]
        fifth_period = [16, 17, 18, 19]
        sixth_period = [20, 21, 22, 23]

        for i in range(0, n):
            hr = hour[i]
            if hr in first_period:
                first[i] = 1
            elif hr in second_period:
                second[i] = 1
            elif hr in third_period:
                third[i] = 1
            elif hr in fourth_period:
                fourth[i] = 1
            elif hr in fifth_period:
                fifth[i] = 1
            elif hr in sixth_period:
                sixth[i] = 1

        X_dummies = np.matrix(first)
        X_dummies = np.append(X_dummies, np.matrix(second), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(third), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(fourth), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(fifth), axis=0)
        X_dummies = np.append(X_dummies, np.matrix(sixth), axis=0)
        X_dummies = np.transpose(X_dummies)

        n_dummies = 6

    return X_dummies, n_dummies


def get_lagged_list(data, time_list, freq="h", lag=24):  # TIL JACOB
    if freq != "h":
        print("FUNCTIONALITY ONLY WRITTEN FOR HOURLY FREQUENCY")

    n_entries = len(data)
    lagged_list = np.zeros(n_entries)
    index_list = np.zeros(n_entries)
    found = 0

    y, mo, d, h, mi = fix_time_list(time_list, single_time_stamp=0, move_n_hours=-24)
    time_stamp = make_time_list(y, mo, d, h, mi)

    for i in range(len(time_stamp) - 1, -1, -1):
        for j in range(i, i - lag - 1, -1):
            if time_stamp[i] == time_list[j]:
                lagged_list[i] = data[j]
                index_list[i] = j
                found = 1
        if found == 0:
            lagged_list[i] = -1
            index_list[i] = -1
        found = 0

    return lagged_list, index_list


def get_last_day_average(data, time_list, index_list_prev_lag, freq="h", lag=24):
    partsum = 0
    n_avg = 0

    last_day_average = []

    for i in range(0, len(data)):
        if index_list_prev_lag[i] == -1:
            last_day_average = np.append(last_day_average,)
        for j in range(index_list_prev_lag[i],i):
            if

    return last_day_average


# Denne skal finne forrige entry på samme tidspunkt (i.e. samme klokkeslett en/to dager før)
def benchmark_hourly(Y, time_listH, HAR_config=0, hours_in_period=4):
    X_dummies, n_dummies = time_of_day_dummies(time_listH, hours_in_period=hours_in_period)  # Dette gir dummy variable

    X_HAR = []
    if HAR_config == 0:  # AR(1)
        X_HAR = Y[0:len(Y - 2)]
        max_lag = 1

    elif HAR_config == 1:  # Denne skal inkludere verdi 24 timer før, og snitt av 24 timer
        # 6.3 Finne forrige entry med samme tidspunkt

        lagged_list, index_list_prev_lag = get_lagged_list(Y, time_listH, lag=24)

        X_HAR = lagged_list
        last_day_average = get_last_day_average(Y, time_listH, index_list_prev_lag)
        X_HAR = np.append(X_HAR, last_day_average, axis=0)

        print("These lengths should be the same:")
        print(len(last_day_average))
        print(len(lagged_list))
        max_lag = 24

    # 6.3.1 Dette vil også være indeksen som skal brukes som 24-timerssnitt
    # 6.3.2 Hvis det ikke finnes noe tidligere tidspunkt så må det bare ikke tas noe gjennomsnitt

    # 6.4 Returnere en X_benchmark

    X_benchmark = np.append(X_dummies, X_HAR, axis=0)
    X_benchmark = np.transpose(X_benchmark)
    Y = Y[max_lag:len(Y) - 1]

    print("These lengths should be the same:")
    print(len(Y))
    print(np.size(X_benchmark, 1))

    return Y, X_benchmark, max_lag
