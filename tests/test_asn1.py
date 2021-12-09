# -*- coding: utf-8 -*-
#
# This file is part of Python-ASN1. Python-ASN1 is free software that is
# made available under the MIT license. Consult the file "LICENSE" that
# is distributed together with this file for the exact licensing terms.
#
# Python-ASN1 is copyright (c) 2007-2016 by the Python-ASN1 authors. See the
# file "AUTHORS" for a complete overview.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import base64
from builtins import int

import pytest

import asn1


class TestEncoder(object):
    """Test suite for ASN1 Encoder."""

    def test_boolean(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(True, asn1.Numbers.Boolean)
        res = enc.output()
        assert res == b'\x01\x01\xff'

    def test_integer(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(1)
        res = enc.output()
        assert res == b'\x02\x01\x01'

    def test_long_integer(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(0x0102030405060708090a0b0c0d0e0f)
        res = enc.output()
        assert res == b'\x02\x0f\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'

    def test_negative_integer(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(-1)
        res = enc.output()
        assert res == b'\x02\x01\xff'

    def test_long_negative_integer(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(-0x0102030405060708090a0b0c0d0e0f)
        res = enc.output()
        assert res == b'\x02\x0f\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6\xf5\xf4\xf3\xf2\xf1\xf1'

    def test_twos_complement_boundaries(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(0)
        res = enc.output()
        assert res == b'\x02\x01\x00'
        enc = asn1.Encoder()
        enc.start()
        enc.write(1)
        res = enc.output()
        assert res == b'\x02\x01\x01'
        enc = asn1.Encoder()
        enc.start()
        enc.write(-0)
        res = enc.output()
        assert res == b'\x02\x01\x00'
        enc = asn1.Encoder()
        enc.start()
        enc.write(-1)
        res = enc.output()
        assert res == b'\x02\x01\xff'
        enc = asn1.Encoder()
        enc.start()
        enc.write(127)
        res = enc.output()
        assert res == b'\x02\x01\x7f'
        enc.start()
        enc.write(128)
        res = enc.output()
        assert res == b'\x02\x02\x00\x80'
        enc.start()
        enc.write(-127)
        res = enc.output()
        assert res == b'\x02\x01\x81'
        enc.start()
        enc.write(-128)
        res = enc.output()
        assert res == b'\x02\x01\x80'
        enc.start()
        enc.write(-129)
        res = enc.output()
        assert res == b'\x02\x02\xff\x7f'
        enc.start()
        enc.write(32767)
        res = enc.output()
        assert res == b'\x02\x02\x7f\xff'
        enc.start()
        enc.write(32768)
        res = enc.output()
        assert res == b'\x02\x03\x00\x80\x00'
        enc.start()
        enc.write(32769)
        res = enc.output()
        assert res == b'\x02\x03\x00\x80\x01'
        enc.start()
        enc.write(-32767)
        res = enc.output()
        assert res == b'\x02\x02\x80\x01'
        enc.start()
        enc.write(-32768)
        res = enc.output()
        assert res == b'\x02\x02\x80\x00'
        enc.start()
        enc.write(-32769)
        res = enc.output()
        assert res == b'\x02\x03\xff\x7f\xff'

    def test_octet_string(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(b'foo')
        res = enc.output()
        assert res == b'\x04\x03foo'

    def test_bitstring(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(b'\x12\x34\x56', asn1.Numbers.BitString)
        res = enc.output()
        assert res == b'\x03\x04\x00\x12\x34\x56'

    def test_printable_string(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(u'foo', nr=asn1.Numbers.PrintableString)
        res = enc.output()
        assert res == b'\x13\x03foo'

    def test_unicode_octet_string(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(u'fooé', nr=asn1.Numbers.OctetString)
        res = enc.output()
        assert res == b'\x04\x05\x66\x6f\x6f\xc3\xa9'

    def test_unicode_printable_string(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(u'fooé', nr=asn1.Numbers.PrintableString)
        res = enc.output()
        assert res == b'\x13\x05\x66\x6f\x6f\xc3\xa9'

    def test_null(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(None)
        res = enc.output()
        assert res == b'\x05\x00'

    def test_object_identifier(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write('1.2.3', asn1.Numbers.ObjectIdentifier)
        res = enc.output()
        assert res == b'\x06\x02\x2a\x03'

    def test_long_object_identifier(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write('39.2.3', asn1.Numbers.ObjectIdentifier)
        res = enc.output()
        assert res == b'\x06\x03\x8c\x1a\x03'
        enc.start()
        enc.write('1.39.3', asn1.Numbers.ObjectIdentifier)
        res = enc.output()
        assert res == b'\x06\x02\x4f\x03'
        enc.start()
        enc.write('1.2.300000', asn1.Numbers.ObjectIdentifier)
        res = enc.output()
        assert res == b'\x06\x04\x2a\x92\xa7\x60'

    def test_real_object_identifier(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write('1.2.840.113554.1.2.1.1', asn1.Numbers.ObjectIdentifier)
        res = enc.output()
        assert res == b'\x06\x0a\x2a\x86\x48\x86\xf7\x12\x01\x02\x01\x01'

    def test_enumerated(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(1, asn1.Numbers.Enumerated)
        res = enc.output()
        assert res == b'\x0a\x01\x01'

    def test_sequence(self):
        enc = asn1.Encoder()
        enc.start()
        enc.enter(asn1.Numbers.Sequence)
        enc.write(1)
        enc.write(b'foo')
        enc.leave()
        res = enc.output()
        assert res == b'\x30\x08\x02\x01\x01\x04\x03foo'

    def test_sequence_of(self):
        enc = asn1.Encoder()
        enc.start()
        enc.enter(asn1.Numbers.Sequence)
        enc.write(1)
        enc.write(2)
        enc.leave()
        res = enc.output()
        assert res == b'\x30\x06\x02\x01\x01\x02\x01\x02'

    def test_set(self):
        enc = asn1.Encoder()
        enc.start()
        enc.enter(asn1.Numbers.Set)
        enc.write(1)
        enc.write(b'foo')
        enc.leave()
        res = enc.output()
        assert res == b'\x31\x08\x02\x01\x01\x04\x03foo'

    def test_set_of(self):
        enc = asn1.Encoder()
        enc.start()
        enc.enter(asn1.Numbers.Set)
        enc.write(1)
        enc.write(2)
        enc.leave()
        res = enc.output()
        assert res == b'\x31\x06\x02\x01\x01\x02\x01\x02'

    def test_context(self):
        enc = asn1.Encoder()
        enc.start()
        enc.enter(1, asn1.Classes.Context)
        enc.write(1)
        enc.leave()
        res = enc.output()
        assert res == b'\xa1\x03\x02\x01\x01'

    def test_application(self):
        enc = asn1.Encoder()
        enc.start()
        enc.enter(1, asn1.Classes.Application)
        enc.write(1)
        enc.leave()
        res = enc.output()
        assert res == b'\x61\x03\x02\x01\x01'

    def test_private(self):
        enc = asn1.Encoder()
        enc.start()
        enc.enter(1, asn1.Classes.Private)
        enc.write(1)
        enc.leave()
        res = enc.output()
        assert res == b'\xe1\x03\x02\x01\x01'

    def test_long_tag_id(self):
        enc = asn1.Encoder()
        enc.start()
        enc.enter(0xffff)
        enc.write(1)
        enc.leave()
        res = enc.output()
        assert res == b'\x3f\x83\xff\x7f\x03\x02\x01\x01'

    def test_long_tag_length(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(b'x' * 0xffff)
        res = enc.output()
        assert res == b'\x04\x82\xff\xff' + b'x' * 0xffff

    def test_error_init(self):
        enc = asn1.Encoder()
        pytest.raises(asn1.Error, enc.enter, asn1.Numbers.Sequence)
        pytest.raises(asn1.Error, enc.leave)
        pytest.raises(asn1.Error, enc.write, 1)
        pytest.raises(asn1.Error, enc.output)

    def test_error_stack(self):
        enc = asn1.Encoder()
        enc.start()
        pytest.raises(asn1.Error, enc.leave)
        enc.enter(asn1.Numbers.Sequence)
        pytest.raises(asn1.Error, enc.output)
        enc.leave()
        pytest.raises(asn1.Error, enc.leave)

    def test_error_object_identifier(self):
        enc = asn1.Encoder()
        enc.start()
        pytest.raises(asn1.Error, enc.write, '1', asn1.Numbers.ObjectIdentifier)
        pytest.raises(asn1.Error, enc.write, '40.2.3', asn1.Numbers.ObjectIdentifier)
        pytest.raises(asn1.Error, enc.write, '1.40.3', asn1.Numbers.ObjectIdentifier)
        pytest.raises(asn1.Error, enc.write, '1.2.3.', asn1.Numbers.ObjectIdentifier)
        pytest.raises(asn1.Error, enc.write, '.1.2.3', asn1.Numbers.ObjectIdentifier)
        pytest.raises(asn1.Error, enc.write, 'foo', asn1.Numbers.ObjectIdentifier)
        pytest.raises(asn1.Error, enc.write, 'foo.bar', asn1.Numbers.ObjectIdentifier)

    def test_default_encoding(self):
        " Check that the encoder implicitly chooses the correct asn1 type "
        def check_defaults(value, number):
            default, explicit = asn1.Encoder(), asn1.Encoder()
            default.start()
            explicit.start()
            default.write(value)
            explicit.write(value, number)
            assert default.output() == explicit.output(), \
                    "default asn1 type for '{}' should be {!r}".format(type(value).__name__, number)

        check_defaults(True, asn1.Numbers.Boolean)
        check_defaults(12345, asn1.Numbers.Integer)
        check_defaults(b"byte string \x00\xff\xba\xdd", asn1.Numbers.OctetString)
        check_defaults(u"unicode string \U0001f4a9", asn1.Numbers.PrintableString)
        check_defaults(None, asn1.Numbers.Null)

    def test_context_no_tag_number(self):
        enc = asn1.Encoder()
        enc.start()
        with pytest.raises(asn1.Error):
            enc.write(b'\x00\x01\x02\x03\x04', typ=asn1.Types.Primitive, cls=asn1.Classes.Context)

    def test_context_with_tag_number_10(self):
        enc = asn1.Encoder()
        enc.start()
        enc.write(b'\x00\x01\x02\x03\x04', nr=10, typ=asn1.Types.Primitive, cls=asn1.Classes.Context)
        res = enc.output()
        assert res == b'\x8a\x05\x00\x01\x02\x03\x04'

    def test_encoding_implicit_tag(self):
        tag = asn1.Tag(5, asn1.Types.Primitive, asn1.Classes.Context)
        enc = asn1.Encoder()
        enc.start()
        enc.write_tagged(tag, '1.2.840.113554.1.2.1.1', encodingNr=asn1.Numbers.ObjectIdentifier)
        res = enc.output()
        assert res == b'\x85\x0a\x2a\x86\x48\x86\xf7\x12\x01\x02\x01\x01'
    
    def test_encoding_implicit_universal_tag(self):
        tag = asn1.Tag(asn1.Numbers.BitString, asn1.Types.Primitive, asn1.Classes.Universal)
        enc = asn1.Encoder()
        enc.start()
        with pytest.raises(asn1.Error):
            enc.write_tagged(tag, '1.2.840.113554.1.2.1.1', asn1.Numbers.ObjectIdentifier)

class TestDecoder(object):
    """Test suite for ASN1 Decoder."""

    def test_boolean(self):
        buf = b'\x01\x01\xff'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.Boolean, asn1.Types.Primitive, asn1.Classes.Universal)
        tag, val = dec.read()
        assert isinstance(val, int)
        assert val
        buf = b'\x01\x01\x01'
        dec.start(buf)
        tag, val = dec.read()
        assert isinstance(val, int)
        assert val
        buf = b'\x01\x01\x00'
        dec.start(buf)
        tag, val = dec.read()
        assert isinstance(val, int)
        assert not val

    def test_integer(self):
        buf = b'\x02\x01\x01'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.Integer, asn1.Types.Primitive, asn1.Classes.Universal)
        tag, val = dec.read()
        assert isinstance(val, int)
        assert val == 1

    def test_long_integer(self):
        buf = b'\x02\x0f\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        dec = asn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == 0x0102030405060708090a0b0c0d0e0f

    def test_negative_integer(self):
        buf = b'\x02\x01\xff'
        dec = asn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == -1

    def test_long_negative_integer(self):
        buf = b'\x02\x0f\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6\xf5\xf4\xf3\xf2\xf1\xf1'
        dec = asn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == -0x0102030405060708090a0b0c0d0e0f

    def test_twos_complement_boundaries(self):
        buf = b'\x02\x01\x7f'
        dec = asn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == 127
        buf = b'\x02\x02\x00\x80'
        dec.start(buf)
        tag, val = dec.read()
        assert val == 128
        buf = b'\x02\x01\x80'
        dec.start(buf)
        tag, val = dec.read()
        assert val == -128
        buf = b'\x02\x02\xff\x7f'
        dec.start(buf)
        tag, val = dec.read()
        assert val == -129

    def test_octet_string(self):
        buf = b'\x04\x03foo'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.OctetString, asn1.Types.Primitive, asn1.Classes.Universal)
        tag, val = dec.read()
        assert val == b'foo'

    def test_printable_string(self):
        buf = b'\x13\x03foo'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.PrintableString, asn1.Types.Primitive, asn1.Classes.Universal)
        tag, val = dec.read()
        assert val == u'foo'

    def test_unicode_printable_string(self):
        buf = b'\x13\x05\x66\x6f\x6f\xc3\xa9'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.PrintableString, asn1.Types.Primitive, asn1.Classes.Universal)
        tag, val = dec.read()
        assert val == u'fooé'

    def test_null(self):
        buf = b'\x05\x00'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.Null, asn1.Types.Primitive, asn1.Classes.Universal)
        tag, val = dec.read()
        assert val is None

    def test_object_identifier(self):
        dec = asn1.Decoder()
        buf = b'\x06\x02\x2a\x03'
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.ObjectIdentifier, asn1.Types.Primitive,
                       asn1.Classes.Universal)
        tag, val = dec.read()
        assert val == u'1.2.3'

    def test_long_object_identifier(self):
        dec = asn1.Decoder()
        buf = b'\x06\x03\x8c\x1a\x03'
        dec.start(buf)
        tag, val = dec.read()
        assert val == u'39.2.3'
        buf = b'\x06\x02\x4f\x03'
        dec.start(buf)
        tag, val = dec.read()
        assert val == u'1.39.3'
        buf = b'\x06\x04\x2a\x92\xa7\x60'
        dec.start(buf)
        tag, val = dec.read()
        assert val == u'1.2.300000'

    def test_real_object_identifier(self):
        dec = asn1.Decoder()
        buf = b'\x06\x0a\x2a\x86\x48\x86\xf7\x12\x01\x02\x01\x01'
        dec.start(buf)
        tag, val = dec.read()
        assert val == u'1.2.840.113554.1.2.1.1'

    def test_enumerated(self):
        buf = b'\x0a\x01\x01'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.Enumerated, asn1.Types.Primitive, asn1.Classes.Universal)
        tag, val = dec.read()
        assert isinstance(val, int)
        assert val == 1

    def test_sequence(self):
        buf = b'\x30\x08\x02\x01\x01\x04\x03foo'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.Sequence, asn1.Types.Constructed, asn1.Classes.Universal)
        dec.enter()
        tag, val = dec.read()
        assert val == 1
        tag, val = dec.read()
        assert val == b'foo'

    def test_sequence_of(self):
        buf = b'\x30\x06\x02\x01\x01\x02\x01\x02'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.Sequence, asn1.Types.Constructed, asn1.Classes.Universal)
        dec.enter()
        tag, val = dec.read()
        assert val == 1
        tag, val = dec.read()
        assert val == 2

    def test_set(self):
        buf = b'\x31\x08\x02\x01\x01\x04\x03foo'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.Set, asn1.Types.Constructed, asn1.Classes.Universal)
        dec.enter()
        tag, val = dec.read()
        assert val == 1
        tag, val = dec.read()
        assert val == b'foo'

    def test_set_of(self):
        buf = b'\x31\x06\x02\x01\x01\x02\x01\x02'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (asn1.Numbers.Set, asn1.Types.Constructed, asn1.Classes.Universal)
        dec.enter()
        tag, val = dec.read()
        assert val == 1
        tag, val = dec.read()
        assert val == 2

    def test_context(self):
        buf = b'\xa1\x03\x02\x01\x01'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (1, asn1.Types.Constructed, asn1.Classes.Context)
        dec.enter()
        tag, val = dec.read()
        assert val == 1

    def test_application(self):
        buf = b'\x61\x03\x02\x01\x01'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (1, asn1.Types.Constructed, asn1.Classes.Application)
        dec.enter()
        tag, val = dec.read()
        assert val == 1

    def test_private(self):
        buf = b'\xe1\x03\x02\x01\x01'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (1, asn1.Types.Constructed, asn1.Classes.Private)
        dec.enter()
        tag, val = dec.read()
        assert val == 1

    def test_long_tag_id(self):
        buf = b'\x3f\x83\xff\x7f\x03\x02\x01\x01'
        dec = asn1.Decoder()
        dec.start(buf)
        tag = dec.peek()
        assert tag == (0xffff, asn1.Types.Constructed, asn1.Classes.Universal)
        dec.enter()
        tag, val = dec.read()
        assert val == 1

    def test_long_tag_length(self):
        buf = b'\x04\x82\xff\xff' + b'x' * 0xffff
        dec = asn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == b'x' * 0xffff

    def test_read_multiple(self):
        buf = b'\x02\x01\x01\x02\x01\x02'
        dec = asn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == 1
        tag, val = dec.read()
        assert val == 2
        assert dec.eof()

    def test_skip_primitive(self):
        buf = b'\x02\x01\x01\x02\x01\x02'
        dec = asn1.Decoder()
        dec.start(buf)
        dec.read()
        tag, val = dec.read()
        assert val == 2
        assert dec.eof()

    def test_skip_constructed(self):
        buf = b'\x30\x06\x02\x01\x01\x02\x01\x02\x02\x01\x03'
        dec = asn1.Decoder()
        dec.start(buf)
        dec.read()
        tag, val = dec.read()
        assert val == 3
        assert dec.eof()

    def test_error_init(self):
        dec = asn1.Decoder()
        pytest.raises(asn1.Error, dec.peek)
        pytest.raises(asn1.Error, dec.read)
        pytest.raises(asn1.Error, dec.enter)
        pytest.raises(asn1.Error, dec.leave)

    def test_error_stack(self):
        buf = b'\x30\x08\x02\x01\x01\x04\x03foo'
        dec = asn1.Decoder()
        dec.start(buf)
        pytest.raises(asn1.Error, dec.leave)
        dec.enter()
        dec.leave()
        pytest.raises(asn1.Error, dec.leave)

    def test_no_input(self):
        dec = asn1.Decoder()
        dec.start(b'')
        tag = dec.peek()
        assert tag is None

    def test_error_missing_tag_bytes(self):
        buf = b'\x3f'
        dec = asn1.Decoder()
        dec.start(buf)
        pytest.raises(asn1.Error, dec.peek)
        buf = b'\x3f\x83'
        dec.start(buf)
        pytest.raises(asn1.Error, dec.peek)

    def test_error_no_length_bytes(self):
        buf = b'\x02'
        dec = asn1.Decoder()
        dec.start(buf)
        pytest.raises(asn1.Error, dec.read)

    def test_error_missing_length_bytes(self):
        buf = b'\x04\x82\xff'
        dec = asn1.Decoder()
        dec.start(buf)
        pytest.raises(asn1.Error, dec.read)

    def test_error_too_many_length_bytes(self):
        buf = b'\x04\xff' + b'\xff' * 0x7f
        dec = asn1.Decoder()
        dec.start(buf)
        pytest.raises(asn1.Error, dec.read)

    def test_error_no_value_bytes(self):
        buf = b'\x02\x01'
        dec = asn1.Decoder()
        dec.start(buf)
        pytest.raises(asn1.Error, dec.read)

    def test_error_missing_value_bytes(self):
        buf = b'\x02\x02\x01'
        dec = asn1.Decoder()
        dec.start(buf)
        pytest.raises(asn1.Error, dec.read)

    def test_error_non_normalized_positive_integer(self):
        buf = b'\x02\x02\x00\x01'
        dec = asn1.Decoder()
        dec.start(buf)
        pytest.raises(asn1.Error, dec.read)

    def test_error_non_normalized_negative_integer(self):
        buf = b'\x02\x02\xff\x80'
        dec = asn1.Decoder()
        dec.start(buf)
        pytest.raises(asn1.Error, dec.read)

    def test_error_non_normalised_object_identifier(self):
        buf = b'\x06\x02\x80\x01'
        dec = asn1.Decoder()
        dec.start(buf)
        pytest.raises(asn1.Error, dec.read)

    def test_error_object_identifier_with_too_large_first_component(self):
        buf = b'\x06\x02\x8c\x40'
        dec = asn1.Decoder()
        dec.start(buf)
        pytest.raises(asn1.Error, dec.read)

    def test_big_negative_integer(self):
        buf = b'\x02\x10\xff\x7f\x2b\x3a\x4d\xea\x48\x1e\x1f\x37\x7b\xa8\xbd\x7f\xb0\x16'
        dec = asn1.Decoder()
        dec.start(buf)
        tag, val = dec.read()
        assert val == -668929531791034950848739021124816874
        assert dec.eof()

    def test_mix_context_universal(self):
        encoded = 'tYHKgAETgwgBgDgJAGMS9aQGgAQBAAAChQUAh7Mfc6YGgAQBAAABhwx0ZXN0LnRlc3Quc2WIAgEhqQigBoAECtiCBIsBAawuM' \
                  'CyCDAIjYh+TlkBYdGMQQIMBAIQBAIUBAoYJFwkVAClUKwAAiAgAIvIQAG0Yj40JFwkUIylUKwAAjgIOEI8BAJEBAZIJRENQMk' \
                  'dHU04xlQEAlgmRI3cAUGBTA/CXAgAAmAEAmwMi8hCdCFOTKXBYgkMQngECnx8CgAGfIAgAIvIQAG0Yjw=='
        buf = base64.b64decode(encoded)

        dec = asn1.Decoder()
        dec.start(buf)

        tag = dec.peek()
        assert tag.typ == asn1.Types.Constructed
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 21

        dec.enter()
        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 0
        assert value == b'\x13'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 3
        assert value == b'\x01\x80\x38\x09\x00\x63\x12\xf5'

        tag = dec.peek()
        assert tag.typ == asn1.Types.Constructed
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 4

        dec.enter()
        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 0
        assert value == b'\x01\x00\x00\x02'
        dec.leave()

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 5
        assert value == b'\x00\x87\xB3\x1F\x73'

        tag = dec.peek()
        assert tag.typ == asn1.Types.Constructed
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 6

        dec.enter()
        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 0
        assert value == b'\x01\x00\x00\x01'
        dec.leave()

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 7
        assert value == b'test.test.se'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 8
        assert value == b'\x01\x21'

        tag = dec.peek()
        assert tag.typ == asn1.Types.Constructed
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 9

        dec.enter()

        tag = dec.peek()
        assert tag.typ == asn1.Types.Constructed
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 0

        dec.enter()
        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 0
        assert value == b'\x0A\xD8\x82\x04'
        dec.leave()
        dec.leave()

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 11
        assert value == b'\x01'

        tag = dec.peek()
        assert tag.typ == asn1.Types.Constructed
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 12

        dec.enter()
        tag = dec.peek()
        assert tag.typ == asn1.Types.Constructed
        assert tag.cls == asn1.Classes.Universal
        assert tag.nr == 16

        dec.enter()
        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 2
        assert value == b'\x02\x23\x62\x1F\x93\x96\x40\x58\x74\x63\x10\x40'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 3
        assert value == b'\x00'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 4
        assert value == b'\x00'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 5
        assert value == b'\x02'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 6
        assert value == b'\x17\x09\x15\x00\x29\x54\x2B\x00\x00'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 8
        assert value == b'\x00\x22\xF2\x10\x00\x6D\x18\x8F'

        dec.leave()
        dec.leave()

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 13
        assert value == b'\x17\x09\x14\x23\x29\x54\x2B\x00\x00'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 14
        assert value == b'\x0E\x10'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 15
        assert value == b'\x00'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 17
        assert value == b'\x01'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 18
        assert value == b'DCP2GGSN1'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 21
        assert value == b'\x00'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 22
        assert value == b'\x91\x23\x77\x00\x50\x60\x53\x03\xF0'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 23
        assert value == b'\x00\x00'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 24
        assert value == b'\x00'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 27
        assert value == b'\x22\xF2\x10'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 29
        assert value == b'\x53\x93\x29\x70\x58\x82\x43\x10'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 30
        assert value == b'\x02'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 31
        assert value == b'\x80\x01'

        tag, value = dec.read()
        assert tag.typ == asn1.Types.Primitive
        assert tag.cls == asn1.Classes.Context
        assert tag.nr == 32
        assert value == b'\x00\x22\xF2\x10\x00\x6D\x18\x8F'

        assert dec.peek() is None


class TestEncoderDecoder(object):
    """Test suite for ASN1 Encoder and Decoder."""

    def test_big_numbers(self):
        for v in \
        (
            668929531791034950848739021124816874,
            667441897913742713771034596334288035,
            664674827807729028941298133900846368,
            666811959353093594446621165172641478,
        ):
            encoder = asn1.Encoder()
            encoder.start()
            encoder.write(v, asn1.Numbers.Integer)
            encoded_bytes = encoder.output()
            decoder = asn1.Decoder()
            decoder.start(encoded_bytes)
            tag, value = decoder.read()
            assert value == v

    def test_big_negative_numbers(self):
        for v in \
        (
            -668929531791034950848739021124816874,
            -667441897913742713771034596334288035,
            -664674827807729028941298133900846368,
            -666811959353093594446621165172641478,
        ):
            encoder = asn1.Encoder()
            encoder.start()
            encoder.write(v, asn1.Numbers.Integer)
            encoded_bytes = encoder.output()
            decoder = asn1.Decoder()
            decoder.start(encoded_bytes)
            tag, value = decoder.read()
            assert value == v
