import numpy as np
class GameProcessor:
    def __init__(self):
        self.data = np.array([])
    def load_data(self, new_data):
        self.data = np.append(self.data, new_data)
    def optimize_performance(self):
        self.data = np.unique(self.data)
    def calculate_average(self):
        if self.data.size == 0:
            return 0
        return np.mean(self.data)
    def run(self, new_data):
        self.load_data(new_data)
        self.optimize_performance()
        return self.calculate_average()

if __name__ == '__main__':
    processor = GameProcessor()
    print(processor.run([1, 2, 2, 3, 4, 4, 5]))