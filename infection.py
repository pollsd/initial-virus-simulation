import random
import matplotlib.pyplot as plt

def infection(days, N, rng):
    heard = [False] * N
    exposures = [0] * N
    active = [False] * N

    start_person = rng.randint(0, N - 1)
    heard[start_person] = True
    exposures[start_person] = 1
    active[start_person] = True

    percent_affected = []

    for day in range(days):
        senders = []
        for person in range(N):
            if active[person]:
                senders.append(person)

        new_infections = [0] * N

        for sender in senders:
            recipients = []

            while len(recipients) < 3:
                target = rng.randint(0, N - 1)
                if target != sender and target not in recipients:
                    recipients.append(target)

            for person in recipients:
                if rng.random() < 0.40:
                    new_infections[person] += 1

        for person in range(N):
            if new_infections[person] > 0:
                heard[person] = True
                exposures[person] += new_infections[person]

        for person in range(N):
            if heard[person] and exposures[person] < 2:
                active[person] = True
            else:
                active[person] = False

        total_heard = 0
        for person in range(N):
            if heard[person]:
                total_heard += 1

        percent = (total_heard / N) * 100
        percent_affected.append(percent)

    return percent_affected


def average_simulation(days, N, trials):
    all_runs = []

    for trial in range(trials):
        rng = random.Random(trial)
        result = infection(days, N, rng)
        all_runs.append(result)

    # Compute average percentage for each day
    average_percent = []
    for day in range(days):
        total = 0
        for trial in range(trials):
            total += all_runs[trial][day]
        average_percent.append(total / trials)

    return average_percent, all_runs


def first_day_reaching_threshold(avg_curve, threshold):
    for day in range(len(avg_curve)):
        if avg_curve[day] >= threshold:
            return day + 1
    return None


def main():
    days = 40
    trials = 100

    company_sizes = [100, 1000, 10000]
    average_curves = {}

    # Run simulations for each N
    for N in company_sizes:
        avg_curve, all_runs = average_simulation(days, N, trials)
        average_curves[N] = avg_curve

        print(f"\nResults for N = {N}")
        print(f"Average % affected after 3 days:  {avg_curve[2]:.2f}%")
        print(f"Average % affected after 20 days: {avg_curve[19]:.2f}%")
        print(f"Average % affected after 40 days: {avg_curve[39]:.2f}%")

    # Threshold results for N = 10000
    avg_curve_10000 = average_curves[10000]
    day_10 = first_day_reaching_threshold(avg_curve_10000, 10)
    day_50 = first_day_reaching_threshold(avg_curve_10000, 50)

    print(f"\nFor N = 10000:")
    print(f"Day when 10% are affected: {day_10}")
    print(f"Day when 50% are affected: {day_50}")

    # -------------------------------
    # Graph 1: Average spread for all N
    # -------------------------------
    x_values = list(range(1, days + 1))

    plt.figure(figsize=(10, 6))
    for N in company_sizes:
        plt.plot(x_values, average_curves[N], label=f"N = {N}")

    plt.title("Average Percentage of Employees Affected Over Time")
    plt.xlabel("Day")
    plt.ylabel("Average % Affected")
    plt.legend()
    plt.grid(True)
    plt.show()

    # -----------------------------------------
    # Graph 2: Threshold graph for N = 10000
    # -----------------------------------------
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, avg_curve_10000, label="N = 10000")
    plt.axhline(y=10, linestyle="--", label="10% threshold")
    plt.axhline(y=50, linestyle="--", label="50% threshold")

    if day_10 is not None:
        plt.axvline(x=day_10, linestyle=":")
    if day_50 is not None:
        plt.axvline(x=day_50, linestyle=":")

    plt.title("Threshold Days for N = 10000")
    plt.xlabel("Day")
    plt.ylabel("Average % Affected")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()