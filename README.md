# Healthcare Cost & Quality Analysis Project

## Project Overview

This repository contains code for analyzing the relationship between healthcare costs and quality metrics in the United States healthcare system. The project aims to investigate whether higher healthcare payments correspond to better quality outcomes by integrating data from two primary sources: Healthgrades hospital ratings and Medicare payment information.

## Data Sources

1. **Healthgrades Data**: Contains hospital names, locations, and quality ratings in JSON format
2. **Medicare Payment Data**: Contains hospital payment information, quality measures, and facility details in JSON format

## Current Progress

### Data Collection
- ✅ Successfully collected Healthgrades data via web scraping
- ✅ Successfully collected Medicare payment data via their API

### Data Processing
- ✅ Created parsers for both JSON data sources
- ✅ Implemented state name standardization to ensure proper merging
- ✅ Successfully merged the datasets based on hospital name and location
- ✅ Generated clean CSV files for:
 - Individual Healthgrades data
 - Individual Medicare data
 - Combined hospital data

## TODO List

### Analysis Implementation
- [ ] Implement cost-quality correlation analysis
- [ ] Calculate regional variations across states
- [ ] Identify high-value hospitals (high quality, low cost)
- [ ] Create scatter plots of cost vs. quality metrics
- [ ] Generate regional correlation comparison visualizations
- [ ] Build box plots showing payment distributions by quality level

### Data Enhancement
- [ ] Add normalization for hospital type/size
- [ ] Create categories for payment levels (low, medium, high)
- [ ] Clean outliers from both datasets
- [ ] Add additional quality metrics beyond ratings