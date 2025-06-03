# 🔧 Troubleshooting Guide

## Common Issues

### Installation Problems

**Issue**: `torch not found`
**Solution**: Install PyTorch first
```bash
pip install torch torchvision
```

**Issue**: `scipy missing`
**Solution**: Install scientific computing stack
```bash
pip install scipy numpy matplotlib
```

### Runtime Errors

**Issue**: `No temporal signals extracted`
**Solution**: Check that model has Conv2d or Linear layers with hooks

**Issue**: `FFT analysis fails`
**Solution**: Ensure sufficient signal length (>= 10 time points)

**Issue**: `CIFAR-10 download fails`
**Solution**: Check internet connection or use local data

### Performance Issues

**Issue**: Analysis takes too long
**Solution**: Reduce `max_batches` parameter

**Issue**: Memory errors
**Solution**: Reduce batch size or use smaller models

### Results Issues

**Issue**: All frequencies are zero
**Solution**: Check model is in correct mode (eval vs train)

**Issue**: State classification always returns 'idle'
**Solution**: Verify input data is not all zeros

## Getting Help

1. Check this troubleshooting guide
2. Review `getting-started.md` for basic usage
3. Examine working examples in `examples/`
4. Check GitHub issues for similar problems

## Reporting Bugs

Include in your bug report:
- Python version
- PyTorch version  
- Complete error message
- Minimal code to reproduce
- System information (OS, hardware)

## FAQ

**Q: Can I use my own model architecture?**
A: Yes, framework works with any PyTorch model

**Q: How accurate are the results?**
A: NN-EEG has been validated on CIFAR-10. NN-fMRI validation coming soon.

**Q: Can I use this in production?**
A: NN-EEG component is production-ready. Full framework after NN-fMRI complete.
