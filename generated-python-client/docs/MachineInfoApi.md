# swagger_client.MachineInfoApi

All URIs are relative to *http://pi-hole4/machine-status*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_machines**](MachineInfoApi.md#get_all_machines) | **GET** /machines | Get status for all machines
[**get_machine**](MachineInfoApi.md#get_machine) | **GET** /machines/{machineId} | Get status for a single machine
[**vibe_check**](MachineInfoApi.md#vibe_check) | **GET** /vibe | Get the overall vibe

# **get_all_machines**
> MachineCollection get_all_machines()

Get status for all machines

Returns the status of all machines, or 404 if no machines have reported status.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.MachineInfoApi(swagger_client.ApiClient(configuration))

try:
    # Get status for all machines
    api_response = api_instance.get_all_machines()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MachineInfoApi->get_all_machines: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**MachineCollection**](MachineCollection.md)

### Authorization

[authorization](../README.md#authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_machine**
> Machine get_machine(machine_id)

Get status for a single machine

Returns the status of the specified machine, or 404 if the machine is unknown.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.MachineInfoApi(swagger_client.ApiClient(configuration))
machine_id = 'machine_id_example' # str | Unique identifier for a machine. This should be the machine's DNS name, optionally as a fully-qualified domain name (FQDN).  (Nothing is stopping us from naming two machines the same thing, nor from providing other irritating names, but let's not make our lives difficult here.) 

try:
    # Get status for a single machine
    api_response = api_instance.get_machine(machine_id)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MachineInfoApi->get_machine: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **machine_id** | **str**| Unique identifier for a machine. This should be the machine&#x27;s DNS name, optionally as a fully-qualified domain name (FQDN).  (Nothing is stopping us from naming two machines the same thing, nor from providing other irritating names, but let&#x27;s not make our lives difficult here.)  | 

### Return type

[**Machine**](Machine.md)

### Authorization

[authorization](../README.md#authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vibe_check**
> InlineResponse2001 vibe_check()

Get the overall vibe

Returns overall status (happy, missing-machine, or oh-shit).  If status is `happy`, the rest of the return object is empty.  If status is `missing-machine` or `oh-shit`, the return object contains additional information about the failure condition. 

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.MachineInfoApi(swagger_client.ApiClient(configuration))

try:
    # Get the overall vibe
    api_response = api_instance.vibe_check()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MachineInfoApi->vibe_check: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**InlineResponse2001**](InlineResponse2001.md)

### Authorization

[authorization](../README.md#authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

