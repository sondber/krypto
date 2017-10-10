import numpy as np
import csv
import jacob_csv_handling
import matplotlib.pyplot as plt
import sondre_support_formulas as supp

def variance(returns, time_list, units_rolling): # takes in the list of logreturns and minutes rolling required
    var = np.zeros(int(len(returns)/units_rolling)) # to be returned
    j = 0
    hourlist = []
    for i in range(0, len(returns)-units_rolling+1, units_rolling):
        var[j] = np.var(returns[i:(i+units_rolling)]) # are we confident on this var-calculation
        hourlist.append(time_list[i]) #timestamps variance calc with start of window
        j += 1
        if i%100000==0:
            print("Progress in calculation:", round(i/(len(returns)-units_rolling+1)*100, 2), "%")
    return var, hourlist


file_name =  "data/export_csv/logreturns_all_minute.csv"
returns = []
time_list = []

with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        i = 0
        next(reader)
        for row in reader:
                time_list.append(row[0]) # Her leser den første kolonne og lagrer det
                returns.append(float(row[1])) # Her leser den andre kolonne og lagrer det som float
                i = i + 1
print("The data is loaded")


variance, hourlist = variance(returns, time_list, 60) #one hour variances


x, ticks = supp.get_ticks(hourlist,5)
plt.plot(variance)
plt.xticks(x,ticks)
plt.ylim(0, 0.0001)
plt.show()

print("The variances are calculated")
jacob_csv_handling.write_to_file(hourlist, variance, "data/export_csv/rolling_variance_all.csv", "One-hour variance")