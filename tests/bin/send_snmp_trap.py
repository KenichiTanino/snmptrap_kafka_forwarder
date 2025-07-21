import asyncio
from pathlib import Path
from pysnmp.smi import builder, view, error
from pysnmp.hlapi.asyncio import *

async def send_flow_down_trap(
    trap_host,
    trap_port,
    community_string,
    sp_alert_id,
    sp_router_name
):
    """
    Sends an SNMPv2c trap for flowDown notification.
    """
    mibBuilder = builder.MibBuilder()
    default_mib_sources = mibBuilder.get_mib_sources()
    project_root = Path(__file__).resolve().parent.parent.parent
    compiled_mibs_dir = project_root / "tools" / "compiled_mibs"

    mibBuilder.set_mib_sources(
        *default_mib_sources,
        builder.DirMibSource(str(project_root)),
        builder.DirMibSource(str(compiled_mibs_dir))
    )

    try:
        mibBuilder.load_modules(
            'SNMPv2-SMI',
            'SNMPv2-TC',
            'SNMPv2-MIB',
            'SNMP-FRAMEWORK-MIB',
            'SNMP-COMMUNITY-MIB',
            'HCNUM-TC',
            'ARBOR-SMI',
            'INET-ADDRESS-MIB',
            'PEAKFLOW-DOS-MIB',
            'PEAKFLOW-SP-MIB'
        )
    except error.SmiError as e:
        print(f"Error loading MIB modules: {e}")
        print("Please ensure all dependent MIBs are accessible and correctly formatted.")
        return

    mibViewController = view.MibViewController(mibBuilder)

    flowdown = ObjectIdentity('PEAKFLOW-SP-MIB', 'flowDown')
    flowdown.resolve_with_mib(mibViewController)
    sp_alert_id_obj = ObjectIdentity('PEAKFLOW-SP-MIB', 'spAlertID')
    sp_alert_id_obj.resolve_with_mib(mibViewController)
    sp_router_obj  = ObjectIdentity('PEAKFLOW-SP-MIB', 'spRouter')
    sp_router_obj.resolve_with_mib(mibViewController)

    # Trap送信
    errorIndication, errorStatus, errorIndex, varBinds = await send_notification(
        SnmpEngine(),
        CommunityData(community_string, mpModel=0),
        await UdpTransportTarget.create((trap_host, trap_port)),
        ContextData(),
        'trap',
        NotificationType(
            flowdown
        ).add_varbinds(
            (sp_alert_id_obj, Integer(sp_alert_id)),
            (sp_router_obj, OctetString(sp_router_name))
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
    TRAP_HOST = '127.0.0.1'
    TRAP_PORT = 16200
    COMMUNITY_STRING = 'public'
    ALERT_ID = 12345
    ROUTER_NAME = 'MyTestRouter'

    asyncio.run(send_flow_down_trap(
        TRAP_HOST,
        TRAP_PORT,
        COMMUNITY_STRING,
        ALERT_ID,
        ROUTER_NAME
    ))
