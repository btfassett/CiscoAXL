import RING.lib.AxlConnection as Axl
import RING.func.Build as Build
import RING.conf as Config
from zeep.exceptions import Fault

def Regions(ClusterNumber):
    try:
        conn = Axl.Connection(Config.WSDL)
        if conn.Open():
            base_regions = ["BROADCAST_", "SBC_", "CONF_", "E911_", "IVR-QUEUE_", "MoH_", "ONNET_", "VM_", ""]
            for region in base_regions:
                result, details = Build.Region(conn.Service, f"{region}CL{ClusterNumber}_R", "", False)
                if not result:
                    raise Exception(details)

            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def Locations(ClusterNumber):
    try:
        conn = Axl.Connection(Config.WSDL)
        if conn.Open():
            result, details = Build.Location(conn.Service, "E911", f"CL{ClusterNumber}", 999999, 384, False)
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def CMRGs(ClusterNumber):
    try:
        conn = Axl.Connection(Config.WSDL)
        service = None
        # history = None
        if conn.Open():
            service = conn.Service
            # history = conn.History
            try:
                for CallManagerGroup in range(1,4):
                    for groupLetter in ["A","B"]:
                        service.addCallManagerGroup(
                            callManagerGroup = {
                                'name' : f"CL{ClusterNumber}_CMRG_{CallManagerGroup}{groupLetter}",
                                'members' : {
                                    'member' : {
                                        'callManagerName' : 'CM_hq-cucm-pub',
                                        'priority' : 1
                                    }
                                }      
                            }
                        )
                    CallManagerGroup = CallManagerGroup + 1
            except Fault as err:
                print(f'Error Inserting CMRGs: {err}')
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def DTGroups():
    try:
        conn = Axl.Connection(Config.WSDL)
        service = None    
        if conn.Open():
            service = conn.Service
            base_DateTime_List = {'Eastern':'America/New_York','Central':'America/Chicago','Mountain':'America/Denver','Arizona':'America/Phoenix','Pacific':'America/Los_Angeles'}
            try:
                for key in base_DateTime_List:
                    service.addDateTimeGroup(
                        dateTimeGroup = {
                            'name' : f"{key}",
                            'timeZone' : f"{base_DateTime_List[key]}",
                            'separator' : '/',
                            'dateformat' : 'D/M/Y',
                            'timeFormat' : '12-hour'
                        }      
                    )
            except Fault as err:
                print(f'Error Inserting CMRGs: {err}')
        else:
            raise Exception("Error Opening Connection")
    except Exception as err:
            print(err)
            return False

def MediaResourceGroups(ClusterNumber):
    try:
        conn = Axl.Connection(Config.WSDL)
        if conn.Open():
            for CallManagerGroup in ["1","2"]:
                result, details = Build.MediaResourceGroup(conn.Service,f"CL{ClusterNumber}",CallManagerGroup, ResourceName='ANN_2')
                if not result:
                    raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def MediaResourceGroupLists(ClusterNumber):
    try:
        conn = Axl.Connection(Config.WSDL)
        if conn.Open():
            result, details = Build.MediaResourceGroupList(conn.Service,f"CL{ClusterNumber}")
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def RouteGroups(ClusterNumber):
    try:
        conn = Axl.Connection(Config.WSDL)
        if conn.Open():
            for Carrier in ["ATT","CTL","VZN"]:
                result, details = Build.RouteGroups(conn.Service,f"CL{ClusterNumber}",Carrier)
                if not result:
                    raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def Partitions(AbbrevCluster):
    try:
        partitionDict = {f'{AbbrevCluster}_Trans_PT':'Cluster Translation Partition',f'{AbbrevCluster}_DN_PT':f'{AbbrevCluster} DN Partition',f'{AbbrevCluster}_Outbound_PT':f'{AbbrevCluster} Outbound Partition',f'E911_{AbbrevCluster}_Hunt_PT':f'{AbbrevCluster} 911 Hunt Partition',f'{AbbrevCluster}_CMService_PT':f'{AbbrevCluster} Service Partition'}
        conn = Axl.Connection(Config.WSDL)
        if conn.Open():
            result, details = Build.Partitions(conn.Service,partitionDict)
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False

def CallingSearchSpaces(AbbrevCluster):
    try:
        conn = Axl.Connection(Config.WSDL)
        CssDict = {f"{AbbrevCluster}_Trans_CSS":f"Cluster TransPattern CSS",f"{AbbrevCluster}_Inbound_CSS":f"Cluster Inbound Access",f"{AbbrevCluster}_Internal_CSS":f"Cluster Internal Only CSS",f"{AbbrevCluster}_Local_CSS":f"Cluster Local Dialing CSS",f"{AbbrevCluster}_LongDistance_CSS":f"Cluster Long Distance Dialing CSS",f"{AbbrevCluster}_International_CSS":f"Cluster International Dialing CSS"}
        MemberListofList = [
            [f"{AbbrevCluster}_Trans_PT",f"{AbbrevCluster}_Outbound_PT",f"E911_{AbbrevCluster}_Hunt_PT",f"{AbbrevCluster}_CMService_PT"],
            [f"{AbbrevCluster}_DN_PT",f"E911_{AbbrevCluster}_Hunt_PT"],
            [f"{AbbrevCluster}_Trans_PT",f"{AbbrevCluster}_Outbound_PT"],
            [f"{AbbrevCluster}_DN_PT"],
            [f"{AbbrevCluster}_DN_PT",f"{AbbrevCluster}_Outbound_PT"],
            [f"{AbbrevCluster}_DN_PT",f"{AbbrevCluster}_Outbound_PT"]
        ]

        if conn.Open():
            result, details = Build.CallingSearchSpace(conn.Service, CssDict, MemberListofList)
            if not result:
                raise Exception(details)
            return True
        else:
            raise Exception("Error opening connection")
    except Exception as err:
        print(err)
        return False