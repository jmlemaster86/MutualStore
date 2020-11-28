# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mutualStore.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='mutualStore.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x11mutualStore.proto\"%\n\x08StoreReq\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\"&\n\x0bRetrieveReq\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\n\n\x02ip\x18\x02 \x01(\t\"(\n\x07JoinReq\x12\n\n\x02ip\x18\x01 \x01(\t\x12\x11\n\tnumBlocks\x18\x02 \x01(\x05\"\x18\n\x08\x42lockMsg\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\"\x1e\n\x0c\x43onfirmation\x12\x0e\n\x06status\x18\x01 \x01(\x05\x32\x8e\x01\n\x0fSecureMessaging\x12(\n\nStoreBlock\x12\t.StoreReq\x1a\r.Confirmation\"\x00\x12*\n\rRetrieveBlock\x12\x0c.RetrieveReq\x1a\t.BlockMsg\"\x00\x12%\n\x08JoinNode\x12\x08.JoinReq\x1a\r.Confirmation\"\x00\x62\x06proto3'
)




_STOREREQ = _descriptor.Descriptor(
  name='StoreReq',
  full_name='StoreReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='StoreReq.key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='data', full_name='StoreReq.data', index=1,
      number=2, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=21,
  serialized_end=58,
)


_RETRIEVEREQ = _descriptor.Descriptor(
  name='RetrieveReq',
  full_name='RetrieveReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='RetrieveReq.key', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ip', full_name='RetrieveReq.ip', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=60,
  serialized_end=98,
)


_JOINREQ = _descriptor.Descriptor(
  name='JoinReq',
  full_name='JoinReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='ip', full_name='JoinReq.ip', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='numBlocks', full_name='JoinReq.numBlocks', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=100,
  serialized_end=140,
)


_BLOCKMSG = _descriptor.Descriptor(
  name='BlockMsg',
  full_name='BlockMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='BlockMsg.data', index=0,
      number=1, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value=b"",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=142,
  serialized_end=166,
)


_CONFIRMATION = _descriptor.Descriptor(
  name='Confirmation',
  full_name='Confirmation',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='status', full_name='Confirmation.status', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=168,
  serialized_end=198,
)

DESCRIPTOR.message_types_by_name['StoreReq'] = _STOREREQ
DESCRIPTOR.message_types_by_name['RetrieveReq'] = _RETRIEVEREQ
DESCRIPTOR.message_types_by_name['JoinReq'] = _JOINREQ
DESCRIPTOR.message_types_by_name['BlockMsg'] = _BLOCKMSG
DESCRIPTOR.message_types_by_name['Confirmation'] = _CONFIRMATION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StoreReq = _reflection.GeneratedProtocolMessageType('StoreReq', (_message.Message,), {
  'DESCRIPTOR' : _STOREREQ,
  '__module__' : 'mutualStore_pb2'
  # @@protoc_insertion_point(class_scope:StoreReq)
  })
_sym_db.RegisterMessage(StoreReq)

RetrieveReq = _reflection.GeneratedProtocolMessageType('RetrieveReq', (_message.Message,), {
  'DESCRIPTOR' : _RETRIEVEREQ,
  '__module__' : 'mutualStore_pb2'
  # @@protoc_insertion_point(class_scope:RetrieveReq)
  })
_sym_db.RegisterMessage(RetrieveReq)

JoinReq = _reflection.GeneratedProtocolMessageType('JoinReq', (_message.Message,), {
  'DESCRIPTOR' : _JOINREQ,
  '__module__' : 'mutualStore_pb2'
  # @@protoc_insertion_point(class_scope:JoinReq)
  })
_sym_db.RegisterMessage(JoinReq)

BlockMsg = _reflection.GeneratedProtocolMessageType('BlockMsg', (_message.Message,), {
  'DESCRIPTOR' : _BLOCKMSG,
  '__module__' : 'mutualStore_pb2'
  # @@protoc_insertion_point(class_scope:BlockMsg)
  })
_sym_db.RegisterMessage(BlockMsg)

Confirmation = _reflection.GeneratedProtocolMessageType('Confirmation', (_message.Message,), {
  'DESCRIPTOR' : _CONFIRMATION,
  '__module__' : 'mutualStore_pb2'
  # @@protoc_insertion_point(class_scope:Confirmation)
  })
_sym_db.RegisterMessage(Confirmation)



_SECUREMESSAGING = _descriptor.ServiceDescriptor(
  name='SecureMessaging',
  full_name='SecureMessaging',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=201,
  serialized_end=343,
  methods=[
  _descriptor.MethodDescriptor(
    name='StoreBlock',
    full_name='SecureMessaging.StoreBlock',
    index=0,
    containing_service=None,
    input_type=_STOREREQ,
    output_type=_CONFIRMATION,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='RetrieveBlock',
    full_name='SecureMessaging.RetrieveBlock',
    index=1,
    containing_service=None,
    input_type=_RETRIEVEREQ,
    output_type=_BLOCKMSG,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='JoinNode',
    full_name='SecureMessaging.JoinNode',
    index=2,
    containing_service=None,
    input_type=_JOINREQ,
    output_type=_CONFIRMATION,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_SECUREMESSAGING)

DESCRIPTOR.services_by_name['SecureMessaging'] = _SECUREMESSAGING

# @@protoc_insertion_point(module_scope)
