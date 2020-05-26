import argparse
import azureml.core
from azureml.core import Workspace, Experiment, Run
from azureml.core.compute import AmlCompute, ComputeTarget, DatabricksCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core.authentication import AzureCliAuthentication

print("In create_aml_cluster.py")

# Check core SDK version number
print("Azure ML SDK version:", azureml.core.VERSION)

parser = argparse.ArgumentParser("create_aml_cluster")
parser.add_argument("--aml_compute_target", type=str, help="compute target name", dest="aml_compute_target", required=True)
parser.add_argument("--path", type=str, help="path", dest="path", required=True)
args = parser.parse_args()

print("Argument 1: %s" % args.aml_compute_target)
print("Argument 2: %s" % args.path)

print('creating AzureCliAuthentication...')
cli_auth = AzureCliAuthentication()
print('done creating AzureCliAuthentication!')

print('get workspace...')
ws = Workspace.from_config(path=args.path, auth=cli_auth)
print('done getting workspace!')

# try:
#     aml_compute = AmlCompute(ws, args.aml_compute_target)
#     print("found existing compute target.")
# except ComputeTargetException:
#     print("creating new compute target")
    
#     provisioning_config = AmlCompute.provisioning_configuration(vm_size = "STANDARD_D2_V2",
#                                                                 min_nodes = 1, 
#                                                                 max_nodes = 1)    
#     aml_compute = ComputeTarget.create(ws, args.aml_compute_target, provisioning_config)
#     aml_compute.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)
    
# print("Aml Compute attached")

# ----------------------

try:
    aml_compute = DatabricksCompute(ws, args.aml_compute_target)
    print("found existing compute target.")
except:
    print("Attaching new ADB compute target")
    
    # See below for param description
    # https://docs.microsoft.com/en-us/python/api/azureml-core/azureml.core.compute.databrickscompute?view=azure-ml-py#attach-configuration-resource-group-none--workspace-name-none--resource-id-none--access-token----
    db_workspace_name = 'test-aml-adb-workspace'
    db_resource_group = 'test-aml-adb'
    db_access_token = 'dapi..........................'

    provisioning_config = DatabricksCompute.attach_configuration(resource_group=db_resource_group,
                                                       workspace_name=db_workspace_name,
                                                       access_token=db_access_token)

    databricks_compute = ComputeTarget.attach(ws, args.aml_compute_target, provisioning_config)
    databricks_compute.wait_for_completion(True)
    print("ADB compute target attached")
