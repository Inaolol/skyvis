"""
Check whether PyTorch, CUDA and cuDNN are installed and whether PyTorch can access the GPU.

Usage: python3 scripts/check_cuda_pytorch.py

Exit codes:
 0 = OK (PyTorch + CUDA + cuDNN available and GPU accessible)
 2 = Missing components or GPU not available to PyTorch
 3 = Script error / unexpected exception
"""
from __future__ import annotations

import sys


def main() -> int:
    info = {}

    try:
        import torch

        info['torch_version'] = getattr(torch, '__version__', 'unknown')
        info['cuda_available'] = torch.cuda.is_available()
        # cudnn availability and version
        try:
            info['cudnn_available'] = torch.backends.cudnn.is_available()
        except Exception:
            info['cudnn_available'] = False
        try:
            info['cudnn_version'] = torch.backends.cudnn.version()
        except Exception:
            info['cudnn_version'] = None

        if info['cuda_available']:
            try:
                info['gpu_count'] = torch.cuda.device_count()
                current = torch.cuda.current_device()
                info['device_name'] = torch.cuda.get_device_name(current)
            except Exception as e:
                info['device_error'] = str(e)

    except Exception as e:  # ImportError or runtime error
        info['torch_import_error'] = str(e)

    # Print concise report
    print('=' * 70)

    if 'torch_import_error' in info:
        print('PyTorch is not installed or failed to import:')
        print(info['torch_import_error'])
        print('\nInstall suggestion:')
        print('  pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118')
        ok = False
    else:
        print('PyTorch version: ', info.get('torch_version'))
        print('CUDA available to PyTorch: ', info.get('cuda_available'))
        print('cuDNN available: ', info.get('cudnn_available'))
        print('cuDNN version: ', info.get('cudnn_version'))
        if info.get('cuda_available'):
            print('GPU count: ', info.get('gpu_count'))
            print('Device name: ', info.get('device_name'))
        ok = bool(info.get('cuda_available') and info.get('cudnn_available'))

    print('=' * 70)

    if ok:
        print('OK: PyTorch + CUDA + cuDNN available and GPU accessible to PyTorch.')
        return 0
    else:
        print('WARNING: Missing components or GPU not available to PyTorch.')
        return 2


if __name__ == '__main__':
    try:
        rc = main()
        sys.exit(rc)
    except Exception as exc:
        print('Unhandled exception while running the check script:')
        print(repr(exc))
        sys.exit(3)
