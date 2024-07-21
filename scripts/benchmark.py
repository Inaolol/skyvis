from ultralytics.utils.benchmarks import benchmark

# Benchmark on GPU
if __name__ == '__main__':
    benchmark(model="C:/Users/abdir/Desktop/models/best.pt", 
          data="C:/Users/abdir/Desktop/Tkno-13/data.yaml", imgsz=800, half=False, device='cpu')