from ultralytics.utils.benchmarks import benchmark

# Benchmark on GPU
if __name__ == '__main__':
    benchmark(model="./models/best.pt", 
          data="./data.yaml", imgsz=800, half=False, device='cpu')