# Azure Monitor Scripts

This repository contains Python scripts for querying Azure Monitor metrics.

## Files

- `azuremonitorv0.93.py` - Latest working version for querying Azure VM CPU metrics
- Other versions are development iterations

## Prerequisites

1. Python 3.6+
2. Azure CLI installed and authenticated (`az login`)
3. Required Python packages:
   ```bash
   pip install azure-mgmt-monitor azure-identity
   ```

## Configuration

Update the following variables in the script:
- `subscription_id` - Your Azure subscription ID
- `resource_group` - Your resource group name
- `vm_name` - Your VM name

## Usage

```bash
python3 azuremonitorv0.93.py
```

## Authentication

The script uses `DefaultAzureCredential` which works with:
- Azure CLI (`az login`)
- Environment variables
- Managed Identity (when running on Azure)

## Output

The script returns CPU percentage metrics for the last hour in 5-minute intervals.