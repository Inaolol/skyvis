from ultralytics.utils.benchmarks import benchmark

# Benchmark on GPU
if __name__ == '__main__':
    benchmark(model="C:/Users/abdir/Desktop/models/best.pt", 
          data="coco8.yaml", imgsz=800, half=False, device=0)