import random
import numpy as np
import matplotlib.pyplot as plt

class Room:
    def __init__(self, rows, cols, dirty_percent):
        self.rows = rows
        self.cols = cols
        self.dirty_percent = dirty_percent
        self.grid = np.zeros((rows, cols))
        self.initialize()

    def initialize(self):
        total_cells = self.rows * self.cols
        dirty_cells = int(total_cells * self.dirty_percent)
        for _ in range(dirty_cells):
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            self.grid[row][col] = 1

    def is_dirty(self, row, col):
        return self.grid[row][col] == 1

    def clean(self, row, col):
        self.grid[row][col] = 0

class Cleaner:
    def __init__(self, room):
        self.room = room
        self.row = 0
        self.col = 0

    def move(self):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        random.shuffle(directions)
        for dr, dc in directions:
            new_row = self.row + dr
            new_col = self.col + dc
            if 0 <= new_row < self.room.rows and 0 <= new_col < self.room.cols:
                self.row = new_row
                self.col = new_col
                break

    def clean_current_cell(self):
        if self.room.is_dirty(self.row, self.col):
            self.room.clean(self.row, self.col)

def simulate(rows, cols, dirty_percent, num_agents, max_time):
    room = Room(rows, cols, dirty_percent)
    cleaners = [Cleaner(room) for _ in range(num_agents)]
    time = 0
    total_moves = 0

    while time < max_time:
        all_clean = all(not room.is_dirty(r, c) for r in range(rows) for c in range(cols))
        if all_clean:
            break

        for cleaner in cleaners:
            cleaner.clean_current_cell()
            cleaner.move()
            total_moves += 1

        time += 1

    cleaned_percent = (1 - np.sum(room.grid) / (rows * cols)) * 100
    return time, cleaned_percent, total_moves

def run_simulations(rows, cols, dirty_percent, max_time, num_agent_list):
    results = []
    for num_agents in num_agent_list:
        total_time = 0
        total_cleaned_percent = 0
        total_moves = 0
        for _ in range(10):  # Realizamos 10 simulaciones por cantidad de agentes para obtener promedios
            time, cleaned_percent, moves = simulate(rows, cols, dirty_percent, num_agents, max_time)
            total_time += time
            total_cleaned_percent += cleaned_percent
            total_moves += moves
        avg_time = total_time / 10
        avg_cleaned_percent = total_cleaned_percent / 10
        avg_moves = total_moves / 10
        results.append((num_agents, avg_time, avg_cleaned_percent, avg_moves))
    return results

def plot_results(results):
    num_agents = [r[0] for r in results]
    avg_time = [r[1] for r in results]
    avg_cleaned_percent = [r[2] for r in results]
    avg_moves = [r[3] for r in results]

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(num_agents, avg_time, marker='o')
    plt.title('Average Time Taken vs. Number of Agents')
    plt.xlabel('Number of Agents')
    plt.ylabel('Average Time Taken')

    plt.subplot(1, 2, 2)
    plt.plot(num_agents, avg_moves, marker='o', color='r')
    plt.title('Average Number of Moves vs. Number of Agents')
    plt.xlabel('Number of Agents')
    plt.ylabel('Average Number of Moves')

    plt.tight_layout()
    plt.show()

def main():
    rows = 5
    cols = 5
    dirty_percent = 0.2
    max_time = 100
    num_agent_list = [1, 2, 3, 4, 5]

    results = run_simulations(rows, cols, dirty_percent, max_time, num_agent_list)
    print("Simulation Results:")
    print("Num Agents | Avg Time | Avg Cleaned % | Avg Moves")
    for result in results:
        print("{:<10} | {:<8.2f} | {:<13.2f} | {:<9.2f}".format(result[0], result[1], result[2], result[3]))

    plot_results(results)

if __name__ == "__main__":
    main()
