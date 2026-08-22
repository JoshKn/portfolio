# GTSRB CNN Walkthrough

I have implemented a Convolutional Neural Network (CNN) to classify traffic signs from the **German Traffic Sign Recognition Benchmark (GTSRB)** dataset.

## Dataset & Preprocessing
- **Source**: GTSRB dataset (via `torchvision.datasets`).
- **Classes**: 43 different traffic signs.
- **Preprocessing**:
    - Resized all images to **32x32** pixels.
    - Normalized using GTSRB specific mean/std stats: `mean=[0.3403, 0.3121, 0.3214]`, `std=[0.2724, 0.2608, 0.2669]`.
    - **Augmentation (Train)**: Random rotation (10 degrees), Color Jitter (brightness/contrast/saturation).

## Model Architecture
The model is a custom CNN with 3 convolutional blocks and fully connected layers:
1. **Block 1**: 2x Conv2d (32 filters), BatchNorm, ReLU, MaxPool, Dropout(0.25)
2. **Block 2**: 2x Conv2d (64 filters), BatchNorm, ReLU, MaxPool, Dropout(0.25)
3. **Block 3**: 1x Conv2d (128 filters), BatchNorm, ReLU, MaxPool, Dropout(0.25)
4. **Head**: Flatten -> Linear(512) -> BatchNorm -> ReLU -> Dropout(0.5) -> Output(43)

## Training Configuration
- **Optimizer**: Adam with Learning Rate **0.001**.
- **Scheduler**: `ReduceLROnPlateau` (factor 0.5, patience 3) to lower LR when accuracy plateaus.
- **Epochs**: 20.
- **Device**: MPS (Mac Metal Performance Shaders) if available, else CUDA/CPU.

## Results
*Training is currently in progress...*

### Next Steps
- Verify if test accuracy exceeds the target of **98.84%**.
- Check confusion matrix (if needed) to see which signs are confused.
