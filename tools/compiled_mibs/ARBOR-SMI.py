# SNMP MIB module (ARBOR-SMI) expressed in pysnmp data model.
#
# This Python module is designed to be imported and executed by the
# pysnmp library.
#
# See https://www.pysnmp.com/pysnmp for further information.
#
# Notes
# -----
# ASN.1 source file://mibs/ARBOR-SMI.mib
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
 enterprises,
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
    "enterprises",
    "iso")

(DisplayString,
 PhysAddress,
 TextualConvention) = mibBuilder.importSymbols(
    "SNMPv2-TC",
    "DisplayString",
    "PhysAddress",
    "TextualConvention")


# MODULE-IDENTITY

arbornetworks = ModuleIdentity(
    (1, 3, 6, 1, 4, 1, 9694)
)
if mibBuilder.loadTexts:
    arbornetworks.setRevisions(
        ("2013-08-19 00:00",
         "2011-07-20 00:00",
         "2009-03-30 00:00",
         "2008-11-13 00:00",
         "2005-09-12 00:00")
    )


# Types definitions


# TEXTUAL-CONVENTIONS



# MIB Managed Objects in the order of their OIDs

_ArbornetworksProducts_ObjectIdentity = ObjectIdentity
arbornetworksProducts = _ArbornetworksProducts_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 9694, 1)
)
if mibBuilder.loadTexts:
    arbornetworksProducts.setStatus("current")
_ArborExperimental_ObjectIdentity = ObjectIdentity
arborExperimental = _ArborExperimental_ObjectIdentity(
    (1, 3, 6, 1, 4, 1, 9694, 2)
)
if mibBuilder.loadTexts:
    arborExperimental.setStatus("current")

# Managed Objects groups


# Notification objects


# Notifications groups


# Agent capabilities


# Module compliance


# Export all MIB objects to the MIB builder

mibBuilder.exportSymbols(
    "ARBOR-SMI",
    **{"arbornetworks": arbornetworks,
       "arbornetworksProducts": arbornetworksProducts,
       "arborExperimental": arborExperimental}
)
