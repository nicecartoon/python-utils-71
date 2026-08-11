import time
import numpy as np

class DataProcessor:
    def __init__(self, data):
        self.data = data

    def process_data(self):
        start_time = time.time()
        processed = self._optimize_and_compute(self.data)
        duration = time.time() - start_time
        print(f'Processing time: {duration:.4f} seconds')
        return processed

    def _optimize_and_compute(self, data):
        # Using numpy for vectorized operations
        data_array = np.array(data)
        return np.sqrt(data_array)  # example operation

if __name__ == '__main__':
    data = range(1, 1000000)
    processor = DataProcessor(data)
    result = processor.process_data()
    print(result[:10])  # display first 10 results