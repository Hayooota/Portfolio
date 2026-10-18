import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.read_csv(
    r"C:\Users\Hayoo\Downloads\CS156\Portfolio\1\data\training-data.csv"
)

# Keep the original time values as datetimes so they can be filtered and plotted.
data["time_dt"] = pd.to_datetime(data["time"], format="%H:%M")

# Convert each time to minutes after midnight.
data["time_minutes"] = (
    data["time_dt"].dt.hour * 60
    + data["time_dt"].dt.minute
)

# Plot inspections at Hermannplatz during a six-hour midday window.
start_minutes = 11 * 60
end_minutes = 17 * 60

window = data[
    (data["station"] == "Alexanderplatz")
    & (data["time_minutes"] >= start_minutes)
    & (data["time_minutes"] < end_minutes)
]

# Twelve 30-minute intervals from 11:00 through 17:00.
bin_edges = range(start_minutes, end_minutes + 30, 30)

sns.set_theme(style="ticks", palette="pastel", font_scale=1.2)

sns.histplot(
    data=window,
    x="time_minutes",
    bins=bin_edges,
    stat="count",
    hue="day",
    multiple="stack",
    discrete=False,
    shrink=0.85,
)

tick_positions = list(range(start_minutes, end_minutes, 30))
tick_labels = [
    f"{minutes // 60:02d}:{minutes % 60:02d}"
    for minutes in tick_positions
]

plt.xticks(tick_positions, tick_labels, rotation=45)
plt.xlabel("Time")
plt.ylabel("Number of inspections")
plt.title("Inspections at Alexanderplatz by day, 11:00–17:00")
plt.tight_layout()

sns.despine()
plt.show()
