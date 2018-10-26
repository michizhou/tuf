#!/usr/bin/env python
"""
<Program>
  asn1_metadata_definitions.py

<Copyright>
  See LICENSE-MIT or LICENSE for licensing information.

<Purpose>
  These are the asn1crypto-compatible ASN.1 definitions for TUF metadata.
  Please also see tuf_metadata_definitions.asn1

  When changes are made to these metadata definitions, they should also be made
  to tuf_metadata_definitions.asn1 (and vice versa).

  When modifying the two files, it is important to take care to keep them
  consistent with each other.  This does not affect the implementation itself,
  but tuf_metadata_definitions.asn1 is the more abstract file that implementers
  using other languages may use for compatibility.

  It is not yet clear to me how to bound values in asn1crypto in the way that
  you can in pyasn1 using ValueRangeConstraint. For thresholds, versions,
  timestamps, etc., we want only non-negative integers.
"""

import asn1crypto.core as ac
# from asn1crypto.core import \
#     Sequence, SequenceOf, Set, SetOf, Integer, OctetString, IA5String



## Common types, for use in the various metadata types

# Not supported?
# class IntegerNatural(ac.Integer):
#   subtypeSpec = constraint.ValueRangeConstraint(0, MAX) # 0 <= value <= MAX

class Signature(ac.Sequence):
  _fields = [
      ('keyid', ac.OctetString),
      ('method', ac.VisibleString),
      ('value', ac.OctetString)]

class Hash(ac.Sequence):
  """
  Conceptual ASN.1 structure (Python pseudocode):
      {'function': 'sha256', 'digest': '...'}
  Equivalent TUF-internal JSON-compatible metadata:
      {'sha256': '...'}
  """
  _fields = [
      ('function', ac.VisibleString),
      ('digest', ac.OctetString)]

# TEMPORARY, FOR DEBUGGING ONLY; DO NOT MERGE
class Hashes(ac.SetOf):
  """
  List of Hash objects.
  Conceptual ASN.1 structure (Python pseudocode):
      [ {'function': 'sha256', 'digest': '...'},
        {'function': 'sha512', 'digest': '...'} ]
  Equivalent TUF-internal JSON-compatible metadata:
      {'sha256': '...', 'sha512': '...'}
  """
  _child_spec = Hash


# TEMPORARY: swap in content itself in class PublicKey
class KeyIDHashAlgorithms(ac.SequenceOf):
  _child_spec = ac.VisibleString


# TEMPORARY: swap in content itself in class PublicKey
# Structurally bizarre, since I'm limiting this to 'public', but still
# allowing keyval to have multiple of these in it......... to match the
# non-ASN.1 metadata definitions.
class KeyValue(ac.Sequence):
  _fields = [
      ('public', ac.VisibleString)] #ac.OctetString)]

class PublicKey(ac.Sequence):
  _fields = [
      ('keytype', ac.VisibleString),
      ('scheme', ac.VisibleString),
      ('keyval', ac.SetOf, {'_child_spec': KeyValue}),
      ('keyid-hash-algorithms', KeyIDHashAlgorithms)]



## Types used only in Root metadata
class TopLevelDelegation(ac.Sequence):
  _fields = [
      ('role', ac.VisibleString),
      ('keyids', ac.SequenceOf, {'_child_spec': ac.OctetString}),
      ('threshold', ac.Integer)]

class RootMetadata(ac.Sequence):
  _fields = [
      ('type', ac.VisibleString),
      ('expires', ac.Integer),
      ('version', ac.Integer),
      ('consistent-snapshot', ac.Boolean),
      ('keys', ac.SetOf, {'_child_spec': PublicKey}),
      ('roles', ac.SetOf, {'_child_spec': TopLevelDelegation})]



## Types used only in Timestamp metadata
class HashesContainer(ac.Sequence):
  """
  Single-element, vapid wrapper for Hashes, solely to match structure of the
  TUF-internal metadata. (This layer could be removed from both metadata
  formats without loss of semantics or clarity, but would break backward
  compatibility.)
  Conceptual ASN.1 structure (Python pseudocode):
      {'hashes': [
        {'function': 'sha256', 'digest': '...'},
        {'function': 'sha512', 'digest': '...'}
      ]}
  Equivalent TUF-internal JSON-compatible metadata:
      {'hashes': {'sha256': '...', 'sha512': '...'}}
  """
  _fields = [
      ('hashes', Hashes)]



class HashOfSnapshot(ac.Sequence):
  """
  Conceptual ASN.1 structure (Python pseudocode): {
      'filename': 'snapshot.json',
      'hashes': [
          {'function': 'sha256', 'digest': '...'},
          {'function': 'sha512', 'digest': '...'}
      ]
  }
  Equivalent TUF-internal JSON-compatible metadata: {
      'snapshot.json': { "hashes": {'sha256': '...', 'sha512': '...'}}
  """
  _fields = [
      ('filename', ac.VisibleString),
      ('hashes', HashesContainer)]

class HashesOfSnapshot(ac.SetOf):
  """
  Conceptual ASN.1 structure (Python pseudocode):
      [ {'filename': 'snapshot.json',
         'hashes': [
           {'function': 'sha256', 'digest': '...'},
           {'function': 'sha512', 'digest': '...'}
         ]},
        <no other values expected>
      ]
  Equivalent TUF-internal JSON-compatible metadata:
      {'snapshot.json': { "hashes": {'sha256': '...', 'sha512': '...'}},
        <no other values expected>
      }
  """
  _child_spec = HashOfSnapshot

class TimestampMetadata(ac.Sequence):
  _fields = [
      ('type', ac.VisibleString),
      ('expires', ac.Integer),
      ('version', ac.Integer),
      ('meta', ac.SetOf, {'_child_spec': HashOfSnapshot})]


## Types used only in Snapshot metadata
class RoleInfo(ac.Sequence):
  _fields = [
      ('filename', ac.VisibleString),
      ('version', ac.Integer)]

class SnapshotMetadata(ac.Sequence):
  _fields = [
      ('type', ac.VisibleString),
      ('expires', ac.Integer),
      ('version', ac.Integer),
      ('meta', ac.SetOf, {'_child_spec': RoleInfo})]




## Types used only in Targets (and delegated targets) metadata
class Delegation(ac.Sequence):
  _fields = [
      ('name', ac.VisibleString),
      ('keyids', ac.SequenceOf, {'_child_spec': ac.OctetString}),
      ('paths', ac.SequenceOf, {'_child_spec': ac.VisibleString}),
      ('threshold', ac.Integer),
      ('terminating', ac.Boolean, {'default': False})]

class Custom(ac.Sequence):
  _fields = [
      ('key', ac.VisibleString),
      ('value', ac.VisibleString)]

class Target(ac.Sequence):
  _fields = [
      ('target-name', ac.VisibleString),
      ('length', ac.Integer),
      ('hashes', ac.SetOf, {'_child_spec': Hash}),
      ('custom', ac.SetOf, {'_child_spec': Custom, 'optional': True})]

class TargetsMetadata(ac.Sequence):
  _fields = [
      ('type', ac.VisibleString),
      ('expires', ac.Integer),
      ('version', ac.Integer),
      ('targets', ac.SetOf, {'_child_spec': Target}),
      ('delegations', ac.Sequence, {'_fields': [
          ('keys', ac.SetOf, {'_child_spec': PublicKey}),
          ('roles', ac.SequenceOf, {'_child_spec': Delegation})]})]
