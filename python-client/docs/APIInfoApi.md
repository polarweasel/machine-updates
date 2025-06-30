# swagger_client.APIInfoApi

All URIs are relative to *http://pi-hole4/machine-status*

Method | HTTP request | Description
------------- | ------------- | -------------
[**a_pi_version_list**](APIInfoApi.md#a_pi_version_list) | **GET** /version | Get API version

# **a_pi_version_list**
> InlineResponse200 a_pi_version_list()

Get API version

Returns the current version of the API. Call this to verify the API is alive.

### Example
```python
from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint


# create an instance of the API class
api_instance = swagger_client.APIInfoApi(swagger_client.ApiClient(configuration))

try:
    # Get API version
    api_response = api_instance.a_pi_version_list()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling APIInfoApi->a_pi_version_list: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**InlineResponse200**](InlineResponse200.md)

### Authorization

[authorization](../README.md#authorization)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

