import globus_sdk, time
from globus_sdk.scopes import TransferScopes

# CLIENT_SECRET = "BVaTBYLMQn7BeSfZDM/dCJANRGDi/cUMKqTwEh134hY="
# Client_secret_localAcer = "Vl+P9D2rk7j2hyfqIV1jv52Eyy+bt0yEb2gW3ThL8kM="
# CLIENT_ID = "b4da560a-a2e6-476c-bce5-b0243ff9c1c4"
# auth_client = globus_sdk.NativeAppAuthClient(CLIENT_ID)

# auth_client.oauth2_start_flow(requested_scopes=TransferScopes.all)
# authorize_url = auth_client.oauth2_get_authorize_url()
# print(f"Please go to this URL and login:\n\n{authorize_url}\n")
# auth_code = input("Please enter the code here: ").strip()

# tokens = auth_client.oauth2_exchange_code_for_tokens(auth_code)
# transfer_tokens = tokens.by_resource_server["transfer.api.globus.org"]

# # construct an AccessTokenAuthorizer and use it to construct the
# # TransferClient
# transfer_client = globus_sdk.TransferClient(
#     authorizer=globus_sdk.AccessTokenAuthorizer(transfer_tokens["access_token"])
# )

## secret way
CLIENT_ID = '8cbf76f8-04e7-4d6e-ab59-2e60b182ec83'
CLIENT_ID_2 = 'e9c03338-e33c-4be6-97a0-8595dc5fc01d'
# identity = "8cbf76f8-04e7-4d6e-ab59-2e60b182ec83@clients.auth.globus.org"
CLIENT_SECRET = 'BVaTBYLMQn7BeSfZDM/dCJANRGDi/cUMKqTwEh134hY='
CLIENT_SECRET_2 = "Vl+P9D2rk7j2hyfqIV1jv52Eyy+bt0yEb2gW3ThL8kM="
auth_client = globus_sdk.ConfidentialAppAuthClient(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    app_name="Tesi3",
)
tokens = auth_client.oauth2_client_credentials_tokens()
access_token = tokens.by_resource_server["transfer.api.globus.org"]["access_token"]
# authorizer = globus_sdk.ClientCredentialsAuthorizer(auth_client, CLIENT_SECRET)
# transfer_client = globus_sdk.TransferClient(authorizer=access_token)
transfer_client = globus_sdk.TransferClient(authorizer=globus_sdk.AccessTokenAuthorizer(access_token))

# at = globus_sdk.ClientCredentialsAuthorizer(auth_client, CLIENT_SECRET)

endpoints = {
    "3D_density_Quijote" : "bbcfa486-90ec-11ed-959b-63a4785a3eec",
    "DebianServer"       : "abf51c76-7723-11ee-b166-7d6eafac2be9",
    "DoraemonRicc"       : "9545d8ac-74d6-11ee-b164-7d6eafac2be9",
    "HDD1disk"           : "9eb93f5a-6c2a-11ee-ad2b-9197a4554f81",
    "VolD"               : "40f0f796-70d5-11ee-b162-7d6eafac2be9",
    "Quijote_NY"         : "e0eae0aa-5bca-11ea-9683-0e56c063f437"
}

source_endpoint_id = endpoints["Quijote_NY"]
dest_endpoint_id = endpoints["VolD"]
# assert dest_endpoint_id == "40f0f796-70d5-11ee-b162-7d6eafac2be9"

# create a Transfer task consisting of one or more items
task_data = globus_sdk.TransferData(source_endpoint=source_endpoint_id, destination_endpoint=dest_endpoint_id)

# task_data.add_item(
#     "/Snapshots/fiducial/0/snapdir_000/",
#     "/media/fuffolo97/VolD/Riccardo/",
#     recursive = True
# )

task_data.add_item(
    "/Snapshots/fiducial/0/snapdir_000/snap_000.0.hdf5",
    #"/media/fuffolo97/VolD/Riccardo/snap_000.0.hdf5",
    "/media/fuffolo97/HDD1/UNI/Tesi/snap_000.0.hdf5"
)

# submit, getting back the task ID
task_doc = transfer_client.submit_transfer(task_data)
task_id = task_doc["task_id"]
print(f"submitted transfer, task_id={task_id}")

# task_data.add_item(
#     "/Snapshots/fiducial/0/snapdir_000/snap_000.1.hdf5",
#     "/media/fuffolo97/VolD/Riccardo/snap_000.1.hdf5"
# )

# # submit, getting back the task ID
# task_doc = transfer_client.submit_transfer(task_data)
# task_id = task_doc["task_id"]
# print(f"submitted transfer, task_id={task_id}")

# while True:
#     task = transfer_client.get_task(task_id)
#     if task["status"] == "SUCCEEDED":
#         print("Begining? O.o")
#         task_data = globus_sdk.TransferData(
#             source_endpoint=source_endpoint_id,
#             destination_endpoint=dest_endpoint_id
#         )
#         task_data.add_item(
#             "/Snapshots/fiducial/0/snapdir_000/snap_000.1.hdf5",
#             "/media/fuffolo97/VolD/Riccardo/snap_000.1.hdf5"
#         )
#         task_doc = transfer_client.submit_transfer(task_data)
#         task_id = task_doc["task_id"]
#         # break
#     elif task["status"] == "FAILED":
#         print("Transfer task failed.")
#         break
#     elif task["status"] in ["ACTIVE", "INACTIVE"]:
#         print("Still " + task["status"])
#         # continue
#     else:
#         print("Passed here >.<")
#         break

#     time.sleep(8)

# SRECRET = "BVaTBYLMQn7BeSfZDM/dCJANRGDi/cUMKqTwEh134hY="
# https://groups.google.com/a/globus.org/g/discuss/c/Pz7g1wZhEJg