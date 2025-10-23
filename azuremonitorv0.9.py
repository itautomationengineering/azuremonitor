from datetime import timedelta, datetime
from azure.identity import DefaultAzureCredential  # works with `az login` or SP creds in env
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.monitor.models import MetricAggregationType

# ---- fill these in ----
subscription_id = "64123c42-874f-4264-8dc5-0fced890f33c"
resource_group  = "monintoring_automation"
vm_name         = "monitoringtest"

# Build the VM resource ID
resource_id = (
    f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}"
    f"/providers/Microsoft.Compute/virtualMachines/{vm_name}"
)

# Auth: uses environment/managed identity/az login automatically
credential = DefaultAzureCredential()

# Create metrics client
client = MonitorManagementClient(credential, subscription_id)

# Calculate time range (last 1 hour)
end_time = datetime.now(datetime.timezone.utc)
start_time = end_time - timedelta(hours=1)

# Query Percentage CPU (platform metric) over the last 1 hour, 5-minute buckets
response = client.metrics.list(
    resource_uri=resource_id,
    timespan=f"{start_time.isoformat()}Z/{end_time.isoformat()}Z",
    interval="PT5M",  # 5-minute intervals in ISO 8601 duration format
    metricnames="Percentage CPU",
    aggregation="Average"
)

# Print the results
for metric in response.value:
    print(f"Metric: {metric.name.value}")
    for ts in metric.timeseries:
        for point in ts.data:
            # Only points that have values are populated
            if point.average is not None:
                print(point.time_stamp.isoformat(), point.average)

# (Optional) If you want the latest single value (most recent non-empty point):
latest = None
for m in response.value:
    for ts in m.timeseries:
        for p in ts.data:
            if p.average is not None and (latest is None or p.time_stamp > latest[0]):
                latest = (p.time_stamp, p.average)
if latest:
    print("\nLatest CPU (%):", round(latest[1], 2), "at", latest[0])
else:
    print("\nNo CPU datapoints returned in the selected window.")
