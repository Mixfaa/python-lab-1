import csv
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


FILENAME = "russia_losses_equipment.csv"

summer_start = datetime(2022, 6, 1)
summer_end = datetime(2022, 8, 31)


def is_summer_of_2022(date):
    return summer_start <= date <= summer_end


def task1(filename, target_row_name, cast_fn):
    with open(filename, newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar="|")

        values = []

        firstrow = True
        row_number = -1
        for row in reader:

            if firstrow:
                firstrow = False
                for i, row_name in enumerate(row):
                    if target_row_name == row_name:
                        row_number = i
                        break
            else:
                if row_number != -1:
                    values.append(cast_fn(row[row_number]))

        return np.array(values)


row = task1(FILENAME, "aircraft", int)

per_day = row

for i, value in enumerate(per_day[1:]):
    per_day[i ] = per_day[i ] - row[i + 1]


print("Aircrafts looses per day:")
print(per_day)


print("3 max aircraft losses per day")
sorted_indecies = per_day.argsort()
max3 = per_day[sorted_indecies][-3:]
print(max3)


DATE_CONVERTER = lambda date_str: datetime.strptime(date_str, "%Y-%m-%d")
dates = task1(FILENAME, "date", DATE_CONVERTER)

total_aircraft_per_summer_2022 = 0
for i, date in enumerate(dates):
    if is_summer_of_2022(date):
        total_aircraft_per_summer_2022 += per_day[i]

print("Total aircraft losses per summer 2022")
print(total_aircraft_per_summer_2022)


destroyed_counter = 0
for i, destroyed in enumerate(per_day):
    destroyed_counter += destroyed
    if i == 300:
        print("Average aircrafts losses for last 300 days")
        print(f"Avg = {destroyed_counter / 300}")
        break


destroyed_list = []
destroyed_dates = []

for i, destroyed in enumerate(reversed(per_day)):
    if i == 365:
        break
    destroyed_list.append(destroyed)
    destroyed_dates.append(dates[(dates.size - 1) - i])

xp = np.array(destroyed_dates)  # x-axis: dates
yp = np.array(destroyed_list)  # y-axis: destroyed counts

fig = plt.figure(figsize=(8, 16), dpi=60)
ax = fig.add_subplot(111)  
ax.plot(xp, yp, linestyle="--", marker="o", label="Destroyed Aircraft")
ax.set_xlabel("Date")
ax.set_ylabel("Destroyed Aircraft Count")
ax.set_title("Destroyed Aircraft per Day")
ax.grid(True, color="gray", linestyle="-.")
ax.legend()
# plt.show()
