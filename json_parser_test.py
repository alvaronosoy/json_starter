import requests
from requests import packages
import json

#x = dir(packages)
#print(x)

requests.packages.urllib3.disable_warnings()

encoded_body = json.dumps({
"aaaUser": {
"attributes": {
"name": "admin",
"pwd": "ciscopsdt"
}
}
})

resp = requests.post("https://sandboxapicdc.cisco.com/api/aaaLogin.json", data=encoded_body, verify=False)
#print(resp)

# apic cookie

header = {"Cookie": "APIC-cookie=" + resp.cookies["APIC-cookie"]}
#print(header)

tenants = requests.get("https://sandboxapicdc.cisco.com/api/node/class/fvTenant.json?rsp-subtree-include=health,faults", headers=header, verify=False)

#print(tenants.text)

"""
There is a lot of manipulation going on with the top part of this script, but most of it deals with the methods needed to authenticate towards the ACI fabric, needing a username and password to authenticate, receive the response from the fabric and gather a token, then send this token in a subsequent call to the fabric to pull the ACI tenant information out in JSON format.  However, this snippet:

  - imported the `request` library to easily interact with the ACI fabric's REST APIs
  - constructed a call to authenticate against the APIC and store the authentication token as a cookie to be used later
  - created a request to ask for all configured tenants in the fabric using the stored authentication cookie
  - accessed the response from the query and printed the raw JSON output to the console/terminal  <br>

4. Save the `get-tenant-json.py` file. To download or review the current code, you can get it from GitHub
   [here](https://github.com/CiscoDevNet/coding-skills-sample-code/blob/master/coding202-parsing-json/get-tenant-json-1.py).
"""

json_response = json.loads(tenants.text)

#print(json.dumps(json_response, sort_keys=True, indent=4))

json_tenants = json_response['imdata']
for tenant in json_tenants:
    tenant_name = tenant['fvTenant']['attributes']['name']
    tenant_dn = tenant['fvTenant']['attributes']['dn']
    tenant_health = tenant['fvTenant']['children'][0]['healthInst']['attributes']['cur']
    output = "Tenant: " + tenant_name + "\t Health Score: " + tenant_health + "\n DN: " + tenant_dn
    print(output.expandtabs(40))

#print(json_tenants)

"""
This snippet:

Starts the initial entry point inside of the imdata dictionary
Creates a for loop to iterate through the list of fvTenant objects sequentially
Gathers the name and dn values within the attributes dictionary contained within the fvTenant dictionary
Gathers the current health score by pulling the value from the children dictionary. This is pulled from the list of child objects (there's only a single item, which is why this can be safely set to 0), and then moving through the healthInst dictionary, followed by the attributes dictionary and pulling the value from cur
Prints the resulting data with nice formatting, using the expandtabs method. If the resulting printed data is not aligned, increase this value to 50 or so (results will vary due to length of configured tenant names on the fabric at any one time)

"""
