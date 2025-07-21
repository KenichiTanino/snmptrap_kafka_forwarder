# SNMP MIB module (PEAKFLOW-DOS-MIB) expressed in pysnmp data model.
#
# This Python module is designed to be imported and executed by the
# pysnmp library.
#
# See https://www.pysnmp.com/pysnmp for further information.
#
# Notes
# -----
# ASN.1 source file://mibs/PEAKFLOW-DOS-MIB.mib
# Produced by pysmi-1.6.2 at Mon Jul 21 10:02:43 2025
# On host tanino-ryzen platform Linux version 6.6.87.2-microsoft-standard-WSL2 by user tanino
# Using Python version 3.12.3 (main, Apr 10 2024, 05:33:47) [GCC 13.2.0]

if 'mibBuilder' not in globals():
    import sys

    sys.stderr.write(__doc__)
    sys.exit(1)

# Import base ASN.1 objects even if this MIB does not use it

(Integer,
 OctetString,
 ObjectIdentifier) = mibBuilder.importSymbols(
    "ASN1",
    "Integer",
    "OctetString",
    "ObjectIdentifier")

(NamedValues,) = mibBuilder.importSymbols(
    "ASN1-ENUMERATION",
    "NamedValues")
(ConstraintsIntersection,
 ConstraintsUnion,
 SingleValueConstraint,
 ValueRangeConstraint,
 ValueSizeConstraint) = mibBuilder.importSymbols(
    "ASN1-REFINEMENT",
    "ConstraintsIntersection",
    "ConstraintsUnion",
    "SingleValueConstraint",
    "ValueRangeConstraint",
    "ValueSizeConstraint")

# Import SMI symbols from the MIBs this MIB depends on

(arbornetworksProducts,) = mibBuilder.importSymbols(
    "ARBOR-SMI",
    "arbornetworksProducts")

(ModuleCompliance,
 NotificationGroup) = mibBuilder.importSymbols(
    "SNMPv2-CONF",
    "ModuleCompliance",
    "NotificationGroup")

(Bits,
 Counter32,
 Counter64,
 Gauge32,
 Integer32,
 IpAddress,
 ModuleIdentity,
 MibIdentifier,
 NotificationType,
 ObjectIdentity,
 MibScalar,
 MibTable,
 MibTableRow,
 MibTableColumn,
 TimeTicks,
 Unsigned32,
 iso) = mibBuilder.importSymbols(
    "SNMPv2-SMI",
    "Bits",
    "Counter32",
    "Counter64",
    "Gauge32",
    "Integer32",
    "IpAddress",
    "ModuleIdentity",
    "MibIdentifier",
    "NotificationType",
    "ObjectIdentity",
    "MibScalar",
    "MibTable",
    "MibTableRow",
    "MibTableColumn",
    "TimeTicks",
    "Unsigned32",
    "iso")

(DisplayString,
 PhysAddress,
 TextualConvention) = mibBuilder.importSymbols(
    "SNMPv2-TC",
    "DisplayString",
    "PhysAddress",
    "TextualConvention")


# MODULE-IDENTITY

peakflowDosMIB = ModuleIdentity(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1)
)
if mibBuilder.loadTexts:
    peakflowDosMIB.setRevisions(
        ("2015-11-17 00:00",
         "2014-06-24 00:00",
         "2013-08-19 00:00",
         "2010-05-20 00:00",
         "2009-03-30 00:00",
         "2008-11-13 00:00",
         "2008-05-08 00:00",
         "2008-04-24 00:00",
         "2008-01-08 00:00",
         "2007-12-14 00:00",
         "2005-11-23 00:00",
         "2005-09-12 00:00")
    )


# Types definitions


# TEXTUAL-CONVENTIONS



# MIB Managed Objects in the order of their OIDs

_PdosAnomalyNotifications_ObjectIdentity = ObjectIdentity
pdosAnomalyNotifications = _PdosAnomalyNotifications_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 0)
)
_PdosAnomalyObjects_ObjectIdentity = ObjectIdentity
pdosAnomalyObjects = _PdosAnomalyObjects_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 1)
)


class _PdosAnomalyDirection_Type(Integer32):
    """Custom type pdosAnomalyDirection based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("inbound", 1),
          ("outbound", 2))
    )


_PdosAnomalyDirection_Type.__name__ = "Integer32"
_PdosAnomalyDirection_Object = MibScalar
pdosAnomalyDirection = _PdosAnomalyDirection_Object(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 1, 1),
    _PdosAnomalyDirection_Type()
)
pdosAnomalyDirection.setMaxAccess("not-accessible")
if mibBuilder.loadTexts:
    pdosAnomalyDirection.setStatus("current")
_PdosAnomalyStart_Type = TimeTicks
_PdosAnomalyStart_Object = MibScalar
pdosAnomalyStart = _PdosAnomalyStart_Object(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 1, 2),
    _PdosAnomalyStart_Type()
)
pdosAnomalyStart.setMaxAccess("not-accessible")
if mibBuilder.loadTexts:
    pdosAnomalyStart.setStatus("current")
_PdosAnomalyDuration_Type = TimeTicks
_PdosAnomalyDuration_Object = MibScalar
pdosAnomalyDuration = _PdosAnomalyDuration_Object(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 1, 3),
    _PdosAnomalyDuration_Type()
)
pdosAnomalyDuration.setMaxAccess("not-accessible")
if mibBuilder.loadTexts:
    pdosAnomalyDuration.setStatus("current")
_PdosAnomalyClassification_Type = DisplayString
_PdosAnomalyClassification_Object = MibScalar
pdosAnomalyClassification = _PdosAnomalyClassification_Object(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 1, 4),
    _PdosAnomalyClassification_Type()
)
pdosAnomalyClassification.setMaxAccess("not-accessible")
if mibBuilder.loadTexts:
    pdosAnomalyClassification.setStatus("current")


class _PdosAnomalyProto_Type(Integer32):
    """Custom type pdosAnomalyProto based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1,
              2,
              3,
              4,
              5,
              6,
              17,
              22,
              132)
        )
    )
    namedValues = NamedValues(
        *(("other", 0),
          ("icmp", 1),
          ("igmp", 2),
          ("ggp", 3),
          ("ip", 4),
          ("st", 5),
          ("tcp", 6),
          ("udp", 17),
          ("idp", 22),
          ("sctp", 132))
    )


_PdosAnomalyProto_Type.__name__ = "Integer32"
_PdosAnomalyProto_Object = MibScalar
pdosAnomalyProto = _PdosAnomalyProto_Object(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 1, 5),
    _PdosAnomalyProto_Type()
)
pdosAnomalyProto.setMaxAccess("not-accessible")
if mibBuilder.loadTexts:
    pdosAnomalyProto.setStatus("current")


class _PdosAnomalyTcpFlags_Type(Bits):
    """Custom type pdosAnomalyTcpFlags based on Bits"""
    namedValues = NamedValues(
        *(("fin", 0),
          ("syn", 1),
          ("rst", 2),
          ("psh", 3),
          ("ack", 4),
          ("urg", 5),
          ("ece", 6),
          ("cwr", 7))
    )

_PdosAnomalyTcpFlags_Type.__name__ = "Bits"
_PdosAnomalyTcpFlags_Object = MibScalar
pdosAnomalyTcpFlags = _PdosAnomalyTcpFlags_Object(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 1, 6),
    _PdosAnomalyTcpFlags_Type()
)
pdosAnomalyTcpFlags.setMaxAccess("not-accessible")
if mibBuilder.loadTexts:
    pdosAnomalyTcpFlags.setStatus("current")


class _PdosAnomalyIpVersion_Type(Integer32):
    """Custom type pdosAnomalyIpVersion based on Integer32"""
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(1,
              2)
        )
    )
    namedValues = NamedValues(
        *(("ipv4", 1),
          ("ipv6", 2))
    )


_PdosAnomalyIpVersion_Type.__name__ = "Integer32"
_PdosAnomalyIpVersion_Object = MibScalar
pdosAnomalyIpVersion = _PdosAnomalyIpVersion_Object(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 1, 7),
    _PdosAnomalyIpVersion_Type()
)
pdosAnomalyIpVersion.setMaxAccess("not-accessible")
if mibBuilder.loadTexts:
    pdosAnomalyIpVersion.setStatus("current")
_PdosUrl_Type = DisplayString
_PdosUrl_Object = MibScalar
pdosUrl = _PdosUrl_Object(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 1, 8),
    _PdosUrl_Type()
)
pdosUrl.setMaxAccess("read-only")
if mibBuilder.loadTexts:
    pdosUrl.setStatus("current")

# Managed Objects groups


# Notification objects

pdosAnomalyStartNotification = NotificationType(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 0, 1)
)
pdosAnomalyStartNotification.setObjects(
      *(("PEAKFLOW-DOS-MIB", "pdosAnomalyDirection"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyStart"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyDuration"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyClassification"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyIpVersion"))
)
if mibBuilder.loadTexts:
    pdosAnomalyStartNotification.setStatus(
        "current"
    )

pdosAnomalyEnd = NotificationType(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 0, 2)
)
pdosAnomalyEnd.setObjects(
      *(("PEAKFLOW-DOS-MIB", "pdosAnomalyDirection"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyStart"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyDuration"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyClassification"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyIpVersion"))
)
if mibBuilder.loadTexts:
    pdosAnomalyEnd.setStatus(
        "current"
    )

pdosAnomalyUpdate = NotificationType(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 0, 3)
)
pdosAnomalyUpdate.setObjects(
      *(("PEAKFLOW-DOS-MIB", "pdosAnomalyDirection"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyStart"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyDuration"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyClassification"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyIpVersion"))
)
if mibBuilder.loadTexts:
    pdosAnomalyUpdate.setStatus(
        "current"
    )

pdosAnomalyDnsMisuse = NotificationType(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 0, 4)
)
pdosAnomalyDnsMisuse.setObjects(
      *(("PEAKFLOW-DOS-MIB", "pdosAnomalyDirection"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyStart"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyDuration"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyClassification"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyProto"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyIpVersion"))
)
if mibBuilder.loadTexts:
    pdosAnomalyDnsMisuse.setStatus(
        "current"
    )

pdosAnomalyUdpMisuse = NotificationType(
    (1, 3, 6, 1, 4, 1, 9694, 1, 1, 0, 5)
)
pdosAnomalyUdpMisuse.setObjects(
      *(("PEAKFLOW-DOS-MIB", "pdosAnomalyDirection"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyStart"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyDuration"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyClassification"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyProto"),
        ("PEAKFLOW-DOS-MIB", "pdosAnomalyIpVersion"))
)
if mibBuilder.loadTexts:
    pdosAnomalyUdpMisuse.setStatus(
        "current"
    )


# Notifications groups


# Agent capabilities


# Module compliance


# Export all MIB objects to the MIB builder

mibBuilder.exportSymbols(
    "PEAKFLOW-DOS-MIB",
    **{"peakflowDosMIB": peakflowDosMIB,
       "pdosAnomalyNotifications": pdosAnomalyNotifications,
       "pdosAnomalyStartNotification": pdosAnomalyStartNotification,
       "pdosAnomalyEnd": pdosAnomalyEnd,
       "pdosAnomalyUpdate": pdosAnomalyUpdate,
       "pdosAnomalyDnsMisuse": pdosAnomalyDnsMisuse,
       "pdosAnomalyUdpMisuse": pdosAnomalyUdpMisuse,
       "pdosAnomalyObjects": pdosAnomalyObjects,
       "pdosAnomalyDirection": pdosAnomalyDirection,
       "pdosAnomalyStart": pdosAnomalyStart,
       "pdosAnomalyDuration": pdosAnomalyDuration,
       "pdosAnomalyClassification": pdosAnomalyClassification,
       "pdosAnomalyProto": pdosAnomalyProto,
       "pdosAnomalyTcpFlags": pdosAnomalyTcpFlags,
       "pdosAnomalyIpVersion": pdosAnomalyIpVersion,
       "pdosUrl": pdosUrl}
)
