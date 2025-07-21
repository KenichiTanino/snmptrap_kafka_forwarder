# SNMP MIB module (INET-ADDRESS-MIB) expressed in pysnmp data model.
#
# This Python module is designed to be imported and executed by the
# pysnmp library.
#
# See https://www.pysnmp.com/pysnmp for further information.
#
# Notes
# -----
# ASN.1 source file://mibs/INET-ADDRESS-MIB.mib
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
 iso,
 mib_2) = mibBuilder.importSymbols(
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
    "iso",
    "mib-2")

(DisplayString,
 PhysAddress,
 TextualConvention) = mibBuilder.importSymbols(
    "SNMPv2-TC",
    "DisplayString",
    "PhysAddress",
    "TextualConvention")


# MODULE-IDENTITY

inetAddressMIB = ModuleIdentity(
    (1, 3, 6, 1, 2, 1, 35)
)
if mibBuilder.loadTexts:
    inetAddressMIB.setRevisions(
        ("2005-02-04 00:00",)
    )


# Types definitions


# TEXTUAL-CONVENTIONS



class InetAddressType(TextualConvention, Integer32):
    status = "current"
    displayHint = "2d"
    subtypeSpec = Integer32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        SingleValueConstraint(
            *(0,
              1,
              2,
              3,
              4,
              16)
        )
    )
    namedValues = NamedValues(
        *(("unknown", 0),
          ("ipv4", 1),
          ("ipv6", 2),
          ("ipv4z", 3),
          ("ipv6z", 4),
          ("dns", 16))
    )



class InetAddress(TextualConvention, OctetString):
    status = "current"
    displayHint = "1d"
    subtypeSpec = OctetString.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueSizeConstraint(0, 255),
    )



class InetPortNumber(TextualConvention, Unsigned32):
    status = "current"
    displayHint = "1d"
    subtypeSpec = Unsigned32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 65535),
    )



class InetAutonomousSystemNumber(TextualConvention, Unsigned32):
    status = "current"
    displayHint = "1d"


class InetAddressPrefixLength(TextualConvention, Unsigned32):
    status = "current"
    displayHint = "1d"
    subtypeSpec = Unsigned32.subtypeSpec
    subtypeSpec += ConstraintsUnion(
        ValueRangeConstraint(0, 128),
    )



# MIB Managed Objects in the order of their OIDs


# Managed Objects groups


# Notification objects


# Notifications groups


# Agent capabilities


# Module compliance


# Export all MIB objects to the MIB builder

mibBuilder.exportSymbols(
    "INET-ADDRESS-MIB",
    **{"InetAddressType": InetAddressType,
       "InetAddress": InetAddress,
       "InetPortNumber": InetPortNumber,
       "InetAutonomousSystemNumber": InetAutonomousSystemNumber,
       "InetAddressPrefixLength": InetAddressPrefixLength,
       "inetAddressMIB": inetAddressMIB}
)
