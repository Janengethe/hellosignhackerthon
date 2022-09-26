#!/usr/bin/env python3
from pprint import pprint

from hellosign_sdk import ApiClient, ApiException, Configuration, apis, models

def hellosignsignature(name, email):
    configuration = Configuration(
        username="dd21f0e9b3c6e5f35b385306a99200ab1e23fb35c82c2f73a83ca885378d67f9",
    )
    
    with ApiClient(configuration) as api_client:
        api = apis.SignatureRequestApi(api_client)
        
        signer = models.SubSignatureRequestTemplateSigner(
            role="Customer",
            email_address=email,
            name=name,
        )
        
        custom_field = models.SubCustomField(
            name="",
            value="",
            editor="Customer",
            required=True,
        )
        
        signing_options = models.SubSigningOptions(
            draw=True,
            type=True,
            upload=True,
            phone=False,
            default_type="draw",
        )
        
        data = models.SignatureRequestSendWithTemplateRequest(
            template_ids=["e573944f4040d3bbb04b752c6e65e32ddb3788bb"],
            subject="M-Sahihi",
            message="Confirm and sign.",
            signers=[signer],
            custom_fields=[custom_field],
            signing_options=signing_options,
            test_mode=True,
        )
        
        try:
            response = api.signature_request_send_with_template(data)
            pprint(response)
        except ApiException as e:
            print("Exception when calling HelloSign API: %s\n" % e)


def logged_in(current_user: int) -> bool:
    """returns True if user is logged in"""
    try:
        _ = current_user.id
        return True
    except:
        return False


# def confi_g(email):
#     configuration = Configuration(
#         username="dce0f00c61588d23c47e6c1a2e530b549399c49f823e16b8db198ea3f904d9d5",
#     )
    
#     with ApiClient(configuration) as api_client:
#         api = apis.AccountApi(api_client)
        
#         data = models.AccountCreateRequest(
#             email_address=email,
#         )
        
#         try:
#             response = api.account_create(data)
#             pprint(response)
#         except ApiException as e:
#             print("Exception when calling HelloSign API: %s\n" % e)
# from pprint import pprint

# from hellosign_sdk import \
#     ApiClient, ApiException, Configuration, apis, models

# configuration = Configuration(
#     # Configure HTTP basic authorization: api_key
#     username="dce0f00c61588d23c47e6c1a2e530b549399c49f823e16b8db198ea3f904d9d5",

#     # or, configure Bearer (JWT) authorization: oauth2
#     # access_token="YOUR_ACCESS_TOKEN",
# )

# with ApiClient(configuration) as api_client:
#     api = apis.SignatureRequestApi(api_client)

#     signer_1 = models.SubSignatureRequestSigner(
#         email_address="janengethew@gmail.com",
#         name="Jack",
#         order=0,
#     )
#     signing_options = models.SubSigningOptions(
#         draw=True,
#         type=True,
#         upload=True,
#         phone=True,
#         default_type="draw",
#     )

#     field_options = models.SubFieldOptions(
#         date_format="DD - MM - YYYY",
#     )

#     data = models.SignatureRequestSendRequest(
#         title="NDA with Acme Co.",
#         subject="The NDA we talked about",
#         message="Please sign this NDA and then we can discuss more. Let me know if you have any questions.",
#         signers=[signer_1],
#         cc_email_addresses=[
#             "janengethej@gmail.com",
#         ],
#         file_url=["https://app.hellosign.com/docs/example_signature_request.pdf"],
#         metadata={
#             "custom_id": 1234,
#             "custom_text": "NDA #9",
#         },
#         signing_options=signing_options,
#         field_options=field_options,
#         test_mode=True,
#     )

#     try:
#         response = api.signature_request_send(data)
#         pprint(response)
#     except ApiException as e:
#         print("Exception when calling HelloSign API: %s\n" % e)