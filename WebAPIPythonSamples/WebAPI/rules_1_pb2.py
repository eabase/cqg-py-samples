# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: WebAPI/rules_1.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from common import shared_1_pb2 as common_dot_shared__1__pb2
from common import timestamp_pb2 as common_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='WebAPI/rules_1.proto',
  package='rules_1',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n\x14WebAPI/rules_1.proto\x12\x07rules_1\x1a\x15\x63ommon/shared_1.proto\x1a\x16\x63ommon/timestamp.proto\"\x8f\x02\n\x0bRuleRequest\x12\x12\n\nrequest_id\x18\x01 \x02(\t\x12\x31\n\x10set_rule_request\x18\x02 \x01(\x0b\x32\x17.rules_1.SetRuleRequest\x12\x37\n\x13\x64\x65lete_rule_request\x18\x03 \x01(\x0b\x32\x1a.rules_1.DeleteRuleRequest\x12\x35\n\x12rules_list_request\x18\x04 \x01(\x0b\x32\x19.rules_1.RulesListRequest\x12I\n\x1cnotification_history_request\x18\x05 \x01(\x0b\x32#.rules_1.NotificationHistoryRequest\"\xe4\x02\n\nRuleResult\x12\x12\n\nrequest_id\x18\x01 \x02(\t\x12\x13\n\x0bresult_code\x18\x02 \x02(\r\x12\x1f\n\x07\x64\x65tails\x18\x03 \x01(\x0b\x32\x0e.shared_1.Text\x12/\n\x0fset_rule_result\x18\x04 \x01(\x0b\x32\x16.rules_1.SetRuleResult\x12\x35\n\x12\x64\x65lete_rule_result\x18\x05 \x01(\x0b\x32\x19.rules_1.DeleteRuleResult\x12\x33\n\x11rules_list_result\x18\x06 \x01(\x0b\x32\x18.rules_1.RulesListResult\x12G\n\x1bnotification_history_result\x18\x07 \x01(\x0b\x32\".rules_1.NotificationHistoryResult\"&\n\nResultCode\x12\x0b\n\x07SUCCESS\x10\x00\x12\x0b\n\x07\x46\x41ILURE\x10\x65\"\xe4\x01\n\x0eRuleDefinition\x12\x0f\n\x07rule_id\x18\x01 \x02(\t\x12\x14\n\x08rule_tag\x18\x02 \x03(\tB\x02\x18\x01\x12@\n\x18\x65xpiration_utc_timestamp\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x02\x18\x01\x12\x1f\n\x06\x61\x63tion\x18\x04 \x03(\x0b\x32\x0f.rules_1.Action\x12\x31\n\x10order_event_rule\x18\x05 \x01(\x0b\x32\x17.rules_1.OrderEventRule\x12\x15\n\x07\x65nabled\x18\x06 \x01(\x08:\x04true\"4\n\x06\x41\x63tion\x12*\n\x0b\x64\x65stination\x18\x04 \x03(\x0b\x32\x15.shared_1.Destination\"V\n\x0eOrderEventRule\x12\x12\n\naccount_id\x18\x01 \x03(\x11\x12\x14\n\x0corder_status\x18\x02 \x03(\r\x12\x1a\n\x12transaction_status\x18\x03 \x03(\r\"\xd9\x01\n\x12NotificationReport\x12\x1d\n\x05title\x18\x01 \x02(\x0b\x32\x0e.shared_1.Text\x12\x1c\n\x04\x62ody\x18\x02 \x02(\x0b\x32\x0e.shared_1.Text\x12\x0f\n\x07rule_id\x18\x03 \x02(\t\x12=\n\x15notification_property\x18\x04 \x03(\x0b\x32\x1e.shared_1.NotificationProperty\x12\x36\n\x12when_utc_timestamp\x18\x05 \x02(\x0b\x32\x1a.google.protobuf.Timestamp\"B\n\x0eSetRuleRequest\x12\x30\n\x0frule_definition\x18\x01 \x02(\x0b\x32\x17.rules_1.RuleDefinition\"\x0f\n\rSetRuleResult\"$\n\x11\x44\x65leteRuleRequest\x12\x0f\n\x07rule_id\x18\x01 \x02(\t\"\x12\n\x10\x44\x65leteRuleResult\"(\n\x10RulesListRequest\x12\x14\n\x08rule_tag\x18\x01 \x03(\tB\x02\x18\x01\"C\n\x0fRulesListResult\x12\x30\n\x0frule_definition\x18\x01 \x03(\x0b\x32\x17.rules_1.RuleDefinition\"\x8a\x01\n\x1aNotificationHistoryRequest\x12\x36\n\x12\x66rom_utc_timestamp\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x34\n\x10to_utc_timestamp\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"U\n\x19NotificationHistoryResult\x12\x38\n\x13notification_report\x18\x01 \x03(\x0b\x32\x1b.rules_1.NotificationReport'
  ,
  dependencies=[common_dot_shared__1__pb2.DESCRIPTOR,common_dot_timestamp__pb2.DESCRIPTOR,])



_RULERESULT_RESULTCODE = _descriptor.EnumDescriptor(
  name='ResultCode',
  full_name='rules_1.RuleResult.ResultCode',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='SUCCESS', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FAILURE', index=1, number=101,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=673,
  serialized_end=711,
)
_sym_db.RegisterEnumDescriptor(_RULERESULT_RESULTCODE)


_RULEREQUEST = _descriptor.Descriptor(
  name='RuleRequest',
  full_name='rules_1.RuleRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_id', full_name='rules_1.RuleRequest.request_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_rule_request', full_name='rules_1.RuleRequest.set_rule_request', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='delete_rule_request', full_name='rules_1.RuleRequest.delete_rule_request', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rules_list_request', full_name='rules_1.RuleRequest.rules_list_request', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='notification_history_request', full_name='rules_1.RuleRequest.notification_history_request', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=81,
  serialized_end=352,
)


_RULERESULT = _descriptor.Descriptor(
  name='RuleResult',
  full_name='rules_1.RuleResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='request_id', full_name='rules_1.RuleResult.request_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='result_code', full_name='rules_1.RuleResult.result_code', index=1,
      number=2, type=13, cpp_type=3, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='details', full_name='rules_1.RuleResult.details', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='set_rule_result', full_name='rules_1.RuleResult.set_rule_result', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='delete_rule_result', full_name='rules_1.RuleResult.delete_rule_result', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rules_list_result', full_name='rules_1.RuleResult.rules_list_result', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='notification_history_result', full_name='rules_1.RuleResult.notification_history_result', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RULERESULT_RESULTCODE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=355,
  serialized_end=711,
)


_RULEDEFINITION = _descriptor.Descriptor(
  name='RuleDefinition',
  full_name='rules_1.RuleDefinition',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rule_id', full_name='rules_1.RuleDefinition.rule_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rule_tag', full_name='rules_1.RuleDefinition.rule_tag', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='expiration_utc_timestamp', full_name='rules_1.RuleDefinition.expiration_utc_timestamp', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='action', full_name='rules_1.RuleDefinition.action', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='order_event_rule', full_name='rules_1.RuleDefinition.order_event_rule', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enabled', full_name='rules_1.RuleDefinition.enabled', index=5,
      number=6, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=True,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=714,
  serialized_end=942,
)


_ACTION = _descriptor.Descriptor(
  name='Action',
  full_name='rules_1.Action',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='destination', full_name='rules_1.Action.destination', index=0,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=944,
  serialized_end=996,
)


_ORDEREVENTRULE = _descriptor.Descriptor(
  name='OrderEventRule',
  full_name='rules_1.OrderEventRule',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='rules_1.OrderEventRule.account_id', index=0,
      number=1, type=17, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='order_status', full_name='rules_1.OrderEventRule.order_status', index=1,
      number=2, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='transaction_status', full_name='rules_1.OrderEventRule.transaction_status', index=2,
      number=3, type=13, cpp_type=3, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=998,
  serialized_end=1084,
)


_NOTIFICATIONREPORT = _descriptor.Descriptor(
  name='NotificationReport',
  full_name='rules_1.NotificationReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='rules_1.NotificationReport.title', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='body', full_name='rules_1.NotificationReport.body', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rule_id', full_name='rules_1.NotificationReport.rule_id', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='notification_property', full_name='rules_1.NotificationReport.notification_property', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='when_utc_timestamp', full_name='rules_1.NotificationReport.when_utc_timestamp', index=4,
      number=5, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1087,
  serialized_end=1304,
)


_SETRULEREQUEST = _descriptor.Descriptor(
  name='SetRuleRequest',
  full_name='rules_1.SetRuleRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rule_definition', full_name='rules_1.SetRuleRequest.rule_definition', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1306,
  serialized_end=1372,
)


_SETRULERESULT = _descriptor.Descriptor(
  name='SetRuleResult',
  full_name='rules_1.SetRuleResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1374,
  serialized_end=1389,
)


_DELETERULEREQUEST = _descriptor.Descriptor(
  name='DeleteRuleRequest',
  full_name='rules_1.DeleteRuleRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rule_id', full_name='rules_1.DeleteRuleRequest.rule_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1391,
  serialized_end=1427,
)


_DELETERULERESULT = _descriptor.Descriptor(
  name='DeleteRuleResult',
  full_name='rules_1.DeleteRuleResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1429,
  serialized_end=1447,
)


_RULESLISTREQUEST = _descriptor.Descriptor(
  name='RulesListRequest',
  full_name='rules_1.RulesListRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rule_tag', full_name='rules_1.RulesListRequest.rule_tag', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\030\001', file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1449,
  serialized_end=1489,
)


_RULESLISTRESULT = _descriptor.Descriptor(
  name='RulesListResult',
  full_name='rules_1.RulesListResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rule_definition', full_name='rules_1.RulesListResult.rule_definition', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1491,
  serialized_end=1558,
)


_NOTIFICATIONHISTORYREQUEST = _descriptor.Descriptor(
  name='NotificationHistoryRequest',
  full_name='rules_1.NotificationHistoryRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='from_utc_timestamp', full_name='rules_1.NotificationHistoryRequest.from_utc_timestamp', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='to_utc_timestamp', full_name='rules_1.NotificationHistoryRequest.to_utc_timestamp', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1561,
  serialized_end=1699,
)


_NOTIFICATIONHISTORYRESULT = _descriptor.Descriptor(
  name='NotificationHistoryResult',
  full_name='rules_1.NotificationHistoryResult',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='notification_report', full_name='rules_1.NotificationHistoryResult.notification_report', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1701,
  serialized_end=1786,
)

_RULEREQUEST.fields_by_name['set_rule_request'].message_type = _SETRULEREQUEST
_RULEREQUEST.fields_by_name['delete_rule_request'].message_type = _DELETERULEREQUEST
_RULEREQUEST.fields_by_name['rules_list_request'].message_type = _RULESLISTREQUEST
_RULEREQUEST.fields_by_name['notification_history_request'].message_type = _NOTIFICATIONHISTORYREQUEST
_RULERESULT.fields_by_name['details'].message_type = common_dot_shared__1__pb2._TEXT
_RULERESULT.fields_by_name['set_rule_result'].message_type = _SETRULERESULT
_RULERESULT.fields_by_name['delete_rule_result'].message_type = _DELETERULERESULT
_RULERESULT.fields_by_name['rules_list_result'].message_type = _RULESLISTRESULT
_RULERESULT.fields_by_name['notification_history_result'].message_type = _NOTIFICATIONHISTORYRESULT
_RULERESULT_RESULTCODE.containing_type = _RULERESULT
_RULEDEFINITION.fields_by_name['expiration_utc_timestamp'].message_type = common_dot_timestamp__pb2._TIMESTAMP
_RULEDEFINITION.fields_by_name['action'].message_type = _ACTION
_RULEDEFINITION.fields_by_name['order_event_rule'].message_type = _ORDEREVENTRULE
_ACTION.fields_by_name['destination'].message_type = common_dot_shared__1__pb2._DESTINATION
_NOTIFICATIONREPORT.fields_by_name['title'].message_type = common_dot_shared__1__pb2._TEXT
_NOTIFICATIONREPORT.fields_by_name['body'].message_type = common_dot_shared__1__pb2._TEXT
_NOTIFICATIONREPORT.fields_by_name['notification_property'].message_type = common_dot_shared__1__pb2._NOTIFICATIONPROPERTY
_NOTIFICATIONREPORT.fields_by_name['when_utc_timestamp'].message_type = common_dot_timestamp__pb2._TIMESTAMP
_SETRULEREQUEST.fields_by_name['rule_definition'].message_type = _RULEDEFINITION
_RULESLISTRESULT.fields_by_name['rule_definition'].message_type = _RULEDEFINITION
_NOTIFICATIONHISTORYREQUEST.fields_by_name['from_utc_timestamp'].message_type = common_dot_timestamp__pb2._TIMESTAMP
_NOTIFICATIONHISTORYREQUEST.fields_by_name['to_utc_timestamp'].message_type = common_dot_timestamp__pb2._TIMESTAMP
_NOTIFICATIONHISTORYRESULT.fields_by_name['notification_report'].message_type = _NOTIFICATIONREPORT
DESCRIPTOR.message_types_by_name['RuleRequest'] = _RULEREQUEST
DESCRIPTOR.message_types_by_name['RuleResult'] = _RULERESULT
DESCRIPTOR.message_types_by_name['RuleDefinition'] = _RULEDEFINITION
DESCRIPTOR.message_types_by_name['Action'] = _ACTION
DESCRIPTOR.message_types_by_name['OrderEventRule'] = _ORDEREVENTRULE
DESCRIPTOR.message_types_by_name['NotificationReport'] = _NOTIFICATIONREPORT
DESCRIPTOR.message_types_by_name['SetRuleRequest'] = _SETRULEREQUEST
DESCRIPTOR.message_types_by_name['SetRuleResult'] = _SETRULERESULT
DESCRIPTOR.message_types_by_name['DeleteRuleRequest'] = _DELETERULEREQUEST
DESCRIPTOR.message_types_by_name['DeleteRuleResult'] = _DELETERULERESULT
DESCRIPTOR.message_types_by_name['RulesListRequest'] = _RULESLISTREQUEST
DESCRIPTOR.message_types_by_name['RulesListResult'] = _RULESLISTRESULT
DESCRIPTOR.message_types_by_name['NotificationHistoryRequest'] = _NOTIFICATIONHISTORYREQUEST
DESCRIPTOR.message_types_by_name['NotificationHistoryResult'] = _NOTIFICATIONHISTORYRESULT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RuleRequest = _reflection.GeneratedProtocolMessageType('RuleRequest', (_message.Message,), {
  'DESCRIPTOR' : _RULEREQUEST,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.RuleRequest)
  })
_sym_db.RegisterMessage(RuleRequest)

RuleResult = _reflection.GeneratedProtocolMessageType('RuleResult', (_message.Message,), {
  'DESCRIPTOR' : _RULERESULT,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.RuleResult)
  })
_sym_db.RegisterMessage(RuleResult)

RuleDefinition = _reflection.GeneratedProtocolMessageType('RuleDefinition', (_message.Message,), {
  'DESCRIPTOR' : _RULEDEFINITION,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.RuleDefinition)
  })
_sym_db.RegisterMessage(RuleDefinition)

Action = _reflection.GeneratedProtocolMessageType('Action', (_message.Message,), {
  'DESCRIPTOR' : _ACTION,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.Action)
  })
_sym_db.RegisterMessage(Action)

OrderEventRule = _reflection.GeneratedProtocolMessageType('OrderEventRule', (_message.Message,), {
  'DESCRIPTOR' : _ORDEREVENTRULE,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.OrderEventRule)
  })
_sym_db.RegisterMessage(OrderEventRule)

NotificationReport = _reflection.GeneratedProtocolMessageType('NotificationReport', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFICATIONREPORT,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.NotificationReport)
  })
_sym_db.RegisterMessage(NotificationReport)

SetRuleRequest = _reflection.GeneratedProtocolMessageType('SetRuleRequest', (_message.Message,), {
  'DESCRIPTOR' : _SETRULEREQUEST,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.SetRuleRequest)
  })
_sym_db.RegisterMessage(SetRuleRequest)

SetRuleResult = _reflection.GeneratedProtocolMessageType('SetRuleResult', (_message.Message,), {
  'DESCRIPTOR' : _SETRULERESULT,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.SetRuleResult)
  })
_sym_db.RegisterMessage(SetRuleResult)

DeleteRuleRequest = _reflection.GeneratedProtocolMessageType('DeleteRuleRequest', (_message.Message,), {
  'DESCRIPTOR' : _DELETERULEREQUEST,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.DeleteRuleRequest)
  })
_sym_db.RegisterMessage(DeleteRuleRequest)

DeleteRuleResult = _reflection.GeneratedProtocolMessageType('DeleteRuleResult', (_message.Message,), {
  'DESCRIPTOR' : _DELETERULERESULT,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.DeleteRuleResult)
  })
_sym_db.RegisterMessage(DeleteRuleResult)

RulesListRequest = _reflection.GeneratedProtocolMessageType('RulesListRequest', (_message.Message,), {
  'DESCRIPTOR' : _RULESLISTREQUEST,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.RulesListRequest)
  })
_sym_db.RegisterMessage(RulesListRequest)

RulesListResult = _reflection.GeneratedProtocolMessageType('RulesListResult', (_message.Message,), {
  'DESCRIPTOR' : _RULESLISTRESULT,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.RulesListResult)
  })
_sym_db.RegisterMessage(RulesListResult)

NotificationHistoryRequest = _reflection.GeneratedProtocolMessageType('NotificationHistoryRequest', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFICATIONHISTORYREQUEST,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.NotificationHistoryRequest)
  })
_sym_db.RegisterMessage(NotificationHistoryRequest)

NotificationHistoryResult = _reflection.GeneratedProtocolMessageType('NotificationHistoryResult', (_message.Message,), {
  'DESCRIPTOR' : _NOTIFICATIONHISTORYRESULT,
  '__module__' : 'WebAPI.rules_1_pb2'
  # @@protoc_insertion_point(class_scope:rules_1.NotificationHistoryResult)
  })
_sym_db.RegisterMessage(NotificationHistoryResult)


_RULEDEFINITION.fields_by_name['rule_tag']._options = None
_RULEDEFINITION.fields_by_name['expiration_utc_timestamp']._options = None
_RULESLISTREQUEST.fields_by_name['rule_tag']._options = None
# @@protoc_insertion_point(module_scope)
