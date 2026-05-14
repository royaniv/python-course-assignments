# Day 05 - Composome Detection

## Description

This program analyzes a carpet plot image from the lab and detects composome regions.

The carpet plot is a similarity matrix:
- red/yellow areas represent similar compositions
- blue areas represent less similar compositions

Large red/yellow squares along the diagonal correspond to composomes.

The program:
- opens the image
- scans the diagonal region
- compares red intensity to blue intensity
- detects composome blocks
- counts red and non-red regions

---

## Files

- image_analysis.py  
  Main analysis program

- test_image_analysis.py  
  Automated tests

- composition_carpetplot.png  
  Input image from the lab

- requirements.txt  
  Required Python libraries

