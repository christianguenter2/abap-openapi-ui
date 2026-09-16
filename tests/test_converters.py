"""Offline converter regressions: python -m unittest discover -s tests -v."""
import json
from pathlib import Path
import unittest

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]


def converter(name):
    return etree.XSLT(etree.parse(str(ROOT / 'src' / name)))


def convert(document, version='4.0', **parameters):
    options = {'odata-version': version, 'openapi-version': '3.0.0', **parameters}
    result = converter('zgw_odatav4_to_openapi.xslt.source.xml')(
        document, **{k: etree.XSLT.strparam(v) for k, v in options.items()})
    return json.loads(str(result))


class ConverterTests(unittest.TestCase):
    def setUp(self):
        self.xml = etree.parse(str(ROOT / 'tests/fixtures/converter-v4.xml'))

    def test_quoted_metadata_is_valid_json(self):
        text = 'Contract "object" \\ API\nSecond line'
        doc = convert(self.xml, **{'info-title': text, 'info-description': text})
        self.assertEqual(doc['info']['title'], text)
        self.assertEqual(doc['info']['description'], text)

    def test_create_required_properties_and_server_defaults(self):
        schema = convert(self.xml)['components']['schemas']['Test.Item-create']
        self.assertEqual(schema['required'], ['Name'])
        self.assertIn('ID', schema['properties'])
        self.assertNotIn('ServerValue', schema['properties'])

    def test_update_required_properties(self):
        schema = convert(self.xml)['components']['schemas']['Test.Item-update']
        self.assertEqual(schema['required'], ['Name'])
        self.assertNotIn('ID', schema['properties'])
        self.assertNotIn('ServerValue', schema['properties'])

    def test_v4_update_allows_representation_and_no_content(self):
        paths = convert(self.xml)['paths']
        responses = paths['/Items/{ID}']['patch']['responses']
        self.assertIn('200', responses)
        self.assertIn('204', responses)
        self.assertNotIn('content', responses['204'])
        self.assertNotIn('204', paths['/Items']['get']['responses'])

    def test_external_key_as_segment_and_bound_action(self):
        paths = convert(self.xml)['paths']
        self.assertIn('/Items/{ID}', paths)
        action = paths['/Items/{ID}/Test.Approve']['post']
        self.assertIn('Comment', action['requestBody']['content']['application/json']['schema']['properties'])

    def test_explicit_false_key_as_segment(self):
        ns = {'edm': 'http://docs.oasis-open.org/odata/ns/edm'}
        self.xml.xpath('//edm:Annotation[@Term="Capabilities.KeyAsSegmentSupported"]', namespaces=ns)[0].set('Bool', 'false')
        self.assertIn('/Items({ID})', convert(self.xml)['paths'])

    def test_v2_duplicates_and_update_response(self):
        source = etree.parse(str(ROOT / 'tests/fixtures/converter-v2.xml'))
        converted = converter('zgw_odatav2_to_v4.xslt.source.xml')(source)
        ns = {'edm': 'http://docs.oasis-open.org/odata/ns/edm'}
        self.assertEqual(len(converted.xpath('//edm:EntityType', namespaces=ns)), 1)
        self.assertEqual(len(converted.xpath('//edm:EntitySet', namespaces=ns)), 1)
        doc = convert(converted, version='2.0')
        responses = doc['paths']["/Items('{ID}')"]['patch']['responses']
        self.assertIn('204', responses)
        self.assertNotIn('200', responses)


if __name__ == '__main__':
    unittest.main()
