from pathlib import Path
from pysnmp.entity.rfc3413 import cmdgen
from pysnmp.smi import builder, view, error

def send_flow_down_trap(
    mib_dir,
    trap_host,
    trap_port,
    community_string,
    sp_alert_id,
    sp_router_name
):
    """
    Sends an SNMPv2c trap for flowDown notification.
    """
    # Create MIB loader/builder
    mibBuilder = builder.MibBuilder()

    # Optionally set an alternative path to compiled MIBs
    mibBuilder.add_mib_sources(builder.DirMibSource(mib_dir))

    # Load MIB modules -- ARBORNET-PEAKFLOW-SP-MIB depends on ARBOR-SMI, PEAKFLOW-DOS-MIB, INET-ADDRESS-MIB
    # For simplicity, we'll assume these are available or will be loaded by pysnmp's default paths.
    # In a real scenario, you might need to specify paths to all dependent MIBs.
    try:
        mibBuilder.load_modules(
            'SNMPv2-MIB',
            'SNMP-FRAMEWORK-MIB',
            'SNMP-COMMUNITY-MIB',
            'ARBORNET-PEAKFLOW-SP-MIB'
        )
    except error.SmiError as e:
        print(f"Error loading MIB modules: {e}")
        print("Please ensure all dependent MIBs (ARBOR-SMI, PEAKFLOW-DOS-MIB, INET-ADDRESS-MIB) are accessible.")
        return

    # Get trap OID from MIB
    (mibNode, ) = mibBuilder.get  ('ARBORNET-PEAKFLOW-SP-MIB', 'flowDown')
    trap_oid = mibNode.name
    
    # Get object definitions for var-binds
    (spAlertID, ) = mibBuilder.get('ARBORNET-PEAKFLOW-SP-MIB', 'spAlertID')
    (spRouter, ) = mibBuilder.get('ARBORNET-PEAKFLOW-SP-MIB', 'spRouter')

    # Create command generator
    cmdGen = cmdgen.CommandGenerator()

    # Send trap
    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.sendTrap(
        cmdgen.CommunityData(community_string),
        cmdgen.UdpTransportTarget((trap_host, trap_port)),
        cmdgen.NotificationType(
            (1,3,6,1,6,3,1,1,4,1,0), # snmpTrapOID.0
            (mibNode.name, ()), # flowDown OID
            (spAlertID.name, sp_alert_id),
            (spRouter.name, sp_router_name)
        )
    )

    if errorIndication:
        print(f"Error sending trap: {errorIndication}")
    else:
        print("Trap sent successfully!")
        print(f"Trap Host: {trap_host}:{trap_port}")
        print(f"Community: {community_string}")
        print(f"Variables: {varBinds}")

if __name__ == "__main__":
    # Configuration for sending the trap
    TRAP_HOST = '127.0.0.1'  # Replace with your trap receiver's IP
    TRAP_PORT = 16200          # Standard SNMP trap port
    COMMUNITY_STRING = 'public' # Replace with your SNMP community string
    MIB_DIRECTORY = str(Path(__file__).resolve().parent.parent)

    # Trap specific values for flowDown
    ALERT_ID = 12345
    ROUTER_NAME = 'MyTestRouter'

    # Call the function to send the trap
    send_flow_down_trap(
        MIB_DIRECTORY,
        TRAP_HOST,
        TRAP_PORT,
        COMMUNITY_STRING,
        ALERT_ID,
        ROUTER_NAME
    )
