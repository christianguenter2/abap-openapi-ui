# OData converter provenance and verification

The bundled transformations derive from
[oasis-tcs/odata-openapi](https://github.com/oasis-tcs/odata-openapi), pinned to
[`7156db5bfc38302912a09c61818d265b976a44c7`](https://github.com/oasis-tcs/odata-openapi/tree/7156db5bfc38302912a09c61818d265b976a44c7).

| Local transformation | Upstream source |
| --- | --- |
| `src/zgw_odatav2_to_v4.xslt.source.xml` | `tools/V2-to-V4-CSDL.xsl` |
| `src/zgw_odatav4_to_openapi.xslt.source.xml` | `tools/V4-CSDL-to-OpenAPI.xsl` |

Upstream CRLF line endings are retained; seven trailing-whitespace additions are
trimmed. The V2-to-V4 transformation is otherwise unchanged. The V4-to-OpenAPI
transformation has one functional adaptation: its `responses` template accepts `include-no-content`,
which V4 update operations set to retain HTTP 204 alongside upstream's HTTP 200
response. Other operations keep upstream behavior. Both update outcomes are
allowed by the [OData protocol](https://docs.oasis-open.org/odata/odata/v4.01/odata-v4.01-part1-protocol.html#sec_UpdateanEntity).
Preserve this adaptation when refreshing the pinned files.

## ABAP integration

The converters continue to run through `CALL TRANSFORMATION`; there is no new
production runtime dependency. Output remains OpenAPI 3.0.0. V2 metadata is first
translated to V4 CSDL, but the final conversion must receive `odata-version=2.0`
because the service itself still uses V2 JSON envelopes and response semantics.
`ZCL_GW_OPENAPI_METADATA_V2` now passes that value explicitly; V4 remains the default.

The upstream update includes title/description escaping, computed defaults,
required create/update properties, duplicate V2 definitions, and external
`KeyAsSegmentSupported` annotations. The last change can turn an entity URL such
as `/Items('{ID}')` into `/Items/{ID}` when the metadata declares support.

## Offline regression tests

Use Python 3 with lxml (tested with 6.1.3):

```sh
python -m venv /tmp/abap-openapi-converter-tests
/tmp/abap-openapi-converter-tests/bin/pip install -r tests/requirements.txt
/tmp/abap-openapi-converter-tests/bin/python -m unittest discover -s tests -v
```

The synthetic fixtures contain no customer metadata. Tests cover JSON escaping,
computed defaults, required POST/PATCH properties, bound actions, external
key-as-segment annotations (true and false), V2 duplicate definitions, and
update responses. lxml is a development dependency only; these tests do not
replace verification with SAP's XSLT processor.

## SGE verification, 2026-09-16

Both transformations and the ABAP integration activated successfully. Metadata
and generated JSON were compared locally, and generation was repeated on SAP:

| Service sample | Paths | Schemas |
| --- | ---: | ---: |
| RAP Web API | 22 | 32 |
| Classic V4 catalog | 10 | 11 |
| Existing V2 test service | 3 | 5 |

For the two V4 samples, entity schemas remained unchanged. Key paths now honor
the services' external key-as-segment annotation. Update responses include both
200 and 204. The RAP bound actions remain present. V2 output uses the `d/results`
response envelope and retains update status 204. A synthetic fixture also verified
escaping and required properties using SAP's processor.

These checks generated specifications; they did not execute business writes or
validate every generated operation through Swagger UI. Older SAP releases were
not available for testing.

## Upstream file checksums

SHA-256 of the unmodified files at the pinned revision:

- `V4-CSDL-to-OpenAPI.xsl`: `8e4270c25414aa15df3b2afec9e20b4ab603cb72d587f67a40e6384cfa6e17b1`
- `V2-to-V4-CSDL.xsl`: `f3d7156b6ef2e8155bce63a8a4ceaf2983c2a94c7d15579ce3b44a8043ad0dbe`
