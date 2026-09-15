# ABAP OpenAPI UI
OpenAPI / Swagger UI integration for SAP NetWeaver Gateway

![abap-open-api-1](docs/abap-openapi-ui-1.png)
![abap-open-api-2](docs/abap-openapi-ui-2.png)
![abap-open-api-3](docs/abap-openapi-ui-3.png)

# Installation
1.  Install this repository using [abapGit](https://github.com/larshp/abapGit)
2.  Run transaction ZGW_OPENAPI

# Testing OData V4 and RAP services

In `ZGW_OPENAPI`, select OData V4 and filter by service group, service ID,
repository, or version. For RAP, the service group is the published service
binding; the service ID is the service definition. Execute the report and click
the service ID to open Swagger UI, or select JSON output to inspect the OpenAPI
document.

The report reads published groups through the Gateway registry, including RAP
assignments that are not stored in the classic service tables. Older Gateway
releases without this registry API retain the classic table lookup. Metadata
loading uses the selected repository and service identity, and Gateway's URL
utility supplies the service path and default namespace.

Service descriptions are read from their owning repositories, including RAP.
Faulty assignments and groups with registry errors are skipped so other published
services remain available. The description lookup falls back to classic texts
when the repository API is unavailable.

# FAQ
For questions, bugs or feature requests please create an [issue](https://gitlab.com/geertjanklaps/abap-openapi-ui/issues)

# Contributing
Check the contributing / development guidelines [here](CONTRIBUTING.md)

# Credits
ABAP OpenAPI UI is based on 2 open source projects:
*  [Swagger UI](https://github.com/swagger-api/swagger-ui)
*  [Odata-OpenAPI](https://github.com/oasis-tcs/odata-openapi)

The ABAP OpenAPI UI code is automatically checked and validated by [abaplint](https://github.com/abaplint/abaplint).

This personal project was started (and is still being maintained) on a development system provided by TheValueChain:

[![tvc-logo](docs/tvc-banner.jpg)](https://www.thevaluechain.eu)
