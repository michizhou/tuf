"""
These are the pyasn1-compatible ASN.1 definitions for TUF metadata. Please also
see tuf_metadata_definitions.asn1

This file is in part automatically generated by asn1ate (v.0.6.0), from
tuf_metadata_definitions.asn1


It is then hand-modified to do the following:

  - remove unneeded subtyping (almost all subtyping)

  - add MAX value

  - when providing a default value, rather than a subtyped object constrained to
     only have one value, provide a specific value (both seem to work, but I
     think this has the right semantics)
     e.g. use:   DefaultedNamedType('terminating', univ.Boolean(0))
     instead of: DefaultedNamedType('terminating', univ.Boolean().subtype(value=0))

  - Move superclass value overrides into bodies of classes
     e.g. use:
       class Positive(univ.Integer):
         subtypeSpec = constraint.ValueRangeConstraint(1, MAX)
     instead of:
       class Positive(univ.Integer):
         pass
       Positive.subtypeSpec = constraint.ValueRangeConstraint(1, MAX)

  - changed imports for style and readability

  - tab length 2, not 4 (per PEP 8)

  - re-ordered to better match order in tuf_metadata_definitions.asn1 for
    readability (but they must still appear such that depended-on classes appear
    before the classes that use them).

  - This comment is added to the top of the auto-generated file.

"""

import pyasn1.type.univ as univ
import pyasn1.type.char as char
import pyasn1.type.constraint as constraint
import pyasn1.type.namedtype as namedtype
# Likely imports for later:
# import pyasn1.type.namedval as namedval
# import pyasn1.type.tag as tag
from pyasn1.type.namedtype import NamedType, NamedTypes, \
    DefaultedNamedType, OptionalNamedType

# Maximum integer value when bounding integer values below.
# It does not seem possible to place a minimum without placing a maximum.
# For thresholds, versions, timestamps, etc., we want only non-negative
# integers, so we're stuck setting a maximum (or not placing any constraints
# at all in the ASN.1 metadata definition itself, would would also be fine).
# Note that the way this MAX value is used (ValueRangeConstraint) is inclusive.
MAX = 2**32-1


## Common types, for use in the various metadata types

class IntegerNatural(univ.Integer):
  subtypeSpec = constraint.ValueRangeConstraint(0, MAX) # 0 <= value <= MAX

class Signature(univ.Sequence):
  componentType = NamedTypes(
      NamedType('keyid', univ.OctetString()),
      NamedType('method', char.VisibleString()),
      NamedType('value', univ.OctetString()))

class Hash(univ.Sequence):
  componentType = NamedTypes(
      NamedType('function', char.VisibleString()),
      NamedType('digest', univ.OctetString()))

# TEMPORARY, FOR DEBUGGING ONLY; DO NOT MERGE
class Hashes(univ.SetOf):
  componentType = Hash()


# TEMPORARY: swap in content itself in class PublicKey
class KeyIDHashAlgorithms(univ.SequenceOf):
  componentType = char.VisibleString()

# TEMPORARY: swap in content itself in class PublicKey
# Structurally bizarre, since I'm limiting this to 'public', but still
# allowing keyval to have multiple of these in it......... to match the
# non-ASN.1 metadata definitions.
class KeyValue(univ.Sequence):
  componentType = NamedTypes(
      NamedType('public', char.VisibleString())) #univ.OctetString()))

class PublicKey(univ.Sequence):
  componentType = NamedTypes(
      NamedType('keytype', char.VisibleString()),
      NamedType('scheme', char.VisibleString()),
      NamedType('keyval', univ.Set(componentType=KeyValue())),
      NamedType('keyid-hash-algorithms', KeyIDHashAlgorithms()))

  # Old style:
  # componentType = NamedTypes(
  #     NamedType('publicKeyID', univ.OctetString()),
  #     NamedType('publicKeyType', char.VisibleString()),
  #     NamedType('publicKeyValue', univ.OctetString()))



## Types used only in Root metadata
class TopLevelDelegation(univ.Sequence):
  componentType = NamedTypes(
      NamedType('role', char.VisibleString()),
      NamedType('num-keyids', IntegerNatural()),
      NamedType('keyids', univ.SequenceOf(componentType=univ.OctetString())),
      NamedType('threshold', IntegerNatural()))

class RootMetadata(univ.Sequence):
  componentType = NamedTypes(
      NamedType('type', char.VisibleString()),
      NamedType('expires', IntegerNatural()),
      NamedType('version', IntegerNatural()),
      NamedType('consistent-snapshot', univ.Boolean()),
      NamedType('num-keys', IntegerNatural()),
      NamedType('keys', univ.SetOf(componentType=PublicKey())), # unordered
      NamedType('num-roles', IntegerNatural()),
      NamedType('roles', univ.SetOf(componentType=TopLevelDelegation()))) # unordered




## Types used only in Timestamp metadata
class HashOfSnapshot(univ.Sequence):
  componentType = NamedTypes(
      NamedType('filename', char.VisibleString()),
      NamedType('num-hashes', IntegerNatural()),
      NamedType('hashes', univ.SetOf(componentType=Hash()))) # unordered

class HashesOfSnapshot(univ.SetOf):
  componentType = HashOfSnapshot()

class TimestampMetadata(univ.Sequence):
  componentType = NamedTypes(
      NamedType('type', char.VisibleString()),
      NamedType('expires', IntegerNatural()),
      NamedType('version', IntegerNatural()),
      NamedType('num-meta', IntegerNatural()),
      NamedType('meta', HashesOfSnapshot()) #univ.SetOf(componentType=HashOfSnapshot())) # unordered
  )




## Types used only in Snapshot metadata
class RoleInfo(univ.Sequence):
  componentType = NamedTypes(
      NamedType('filename', char.VisibleString()),
      NamedType('version', IntegerNatural()))

class SnapshotMetadata(univ.Sequence):
  componentType = NamedTypes(
      NamedType('type', char.VisibleString()),
      NamedType('expires', IntegerNatural()),
      NamedType('version', IntegerNatural()),
      NamedType('num-meta', IntegerNatural()),
      NamedType('meta', univ.SetOf(componentType=RoleInfo())))




## Types used only in Targets (and delegated targets) metadata
class Delegation(univ.Sequence):
  componentType = NamedTypes(
      NamedType('name', char.VisibleString()),
      NamedType('num-keyids', IntegerNatural()),
      NamedType('keyids', univ.SequenceOf(componentType=univ.OctetString())),
      NamedType('num-paths', IntegerNatural()),
      NamedType('paths', univ.SequenceOf(componentType=char.VisibleString())),
      NamedType('threshold', IntegerNatural()),
      DefaultedNamedType('terminating', univ.Boolean(0)))

class Custom(univ.Sequence):
  componentType = NamedTypes(
      NamedType('key', char.VisibleString()),
      NamedType('value', char.VisibleString()))

class Target(univ.Sequence):
  componentType = NamedTypes(
      NamedType('target-name', char.VisibleString()),
      NamedType('length', IntegerNatural()),
      NamedType('num-hashes', IntegerNatural()),
      NamedType('hashes', univ.SetOf(componentType=Hash())),
      OptionalNamedType('num-custom', IntegerNatural()),
      OptionalNamedType('custom', univ.SetOf(componentType=Custom())))

class TargetsMetadata(univ.Sequence):
  componentType = NamedTypes(
      NamedType('type', char.VisibleString()),
      NamedType('expires', IntegerNatural()),
      NamedType('version', IntegerNatural()),
      NamedType('num-targets', IntegerNatural()),
      NamedType('targets', univ.SetOf(componentType=Target())),
      NamedType('delegations', univ.Sequence(componentType=NamedTypes(
          NamedType('num-keys', IntegerNatural()),
          NamedType('keys', univ.SetOf(componentType=PublicKey())),
          NamedType('num-roles', IntegerNatural()),
          NamedType('roles', univ.SequenceOf(componentType=Delegation()))
      ))) # tagFormatConstructed
  )
