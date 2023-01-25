import globus_sdk

# this is the tutorial client ID
# replace this string with your ID for production use
CLIENT_ID = "566c2f96-0b59-486c-bd4f-5683805cbdda"
client = globus_sdk.NativeAppAuthClient(CLIENT_ID)

client.oauth2_start_flow()
authorize_url = client.oauth2_get_authorize_url()
print(f"Please go to this URL and login:\n\n{authorize_url}\n")

auth_code = input("Please enter the code you get after login here: ").strip()
token_response = client.oauth2_exchange_code_for_tokens(auth_code)

globus_auth_data = token_response.by_resource_server["auth.globus.org"]
globus_transfer_data = token_response.by_resource_server["transfer.api.globus.org"]

# most specifically, you want these tokens as strings
AUTH_TOKEN = globus_auth_data["access_token"]
TRANSFER_TOKEN = globus_transfer_data["access_token"]