import asyncio
from datetime import date, datetime, timezone
import uuid

from core.session_manager import SessionManager 
from core.api.logbook_service import LogbookService 

# IMPORT ONLY THE NEW MODELS
from core.model.logbook_model import (
    LogbookEntry, 
    LogbookDetail, 
    Activity, 
    Progress, 
    UsecaseInfo, 
    Tool
)

from core.utils import Utils


def get_iso_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

async def run_integration_test():
    session = SessionManager()
    
    try:
        print("--- [1/4] Authenticating ---")
        await session.get_api_client()
        
        service = LogbookService(session)
        user_id = session._user_id
        
        # --- [2/4] GET Data ---
        print("\n--- [2/4] Fetching Metadata ---")
        projects_resp = await service.list_projects()
        tools_resp = await service.list_tools()
        print("total project: {}".format(len(projects_resp['data'])))
        print("total tools: {}".format(len(tools_resp['data'])))
        
        # --- [3/4] ADD TEST ---
        print("\n--- [3/4] Testing ADD ---")
        
        # Pick valid references
        sample_proj = projects_resp['data'][0]
        sample_usecase = sample_proj['usecases'][0] # {'name': '...', 'deadline': '...'}
        sample_tool = tools_resp['data'][0]         # {'name': '...', 'fid': '...'}
        print(session._user_team)
        # --- ADD TEST ---
        new_entry = LogbookEntry(
            user_id=user_id,
            current_team=session._user_team,
            work_mode="WFO",
            # USE UTILS HERE:
            selected_date=Utils.get_now_iso(), 
            created_at=Utils.get_now_iso(),
            updated_at=Utils.get_now_iso(),
            project=sample_proj['name'],
            detail=[
                LogbookDetail(
                    usecase=UsecaseInfo(
                        name=sample_usecase['name'],
                        # USE UTILS HERE (assuming sample_usecase['deadline'] is a string from DB, it's fine. 
                        # If it's a date object, wrap it in Utils.date_to_iso)
                        deadline=sample_usecase['deadline'] 
                    ),
                    activity=[
                        Activity(
                            description="Testing New Model Add",
                            progress=Progress(type="Alur Proses", value=1, percentage=10)
                        )
                    ],
                    next_activity=["Test Edit Next"]
                )
            ],
            tools=[
                Tool(name=sample_tool['name'], fid=sample_tool['fid'])
            ]
        )
        
        # Send it
        print(new_entry.model_dump(by_alias=True, exclude_none=True))
        add_result = await service.add_logbooks_batch([new_entry])
        created_log = add_result[0]['data']
        created_id = created_log['_id']
        print(f"✅ Added Logbook. ID: {created_id}")
        # --- [4/4] EDIT TEST ---
        print("\n--- [4/4] Testing EDIT ---")
        
        # 1. Modify the object we just got back (or create a new one with that ID)
        # We Hydrate the JSON response back into a LogbookEntry model
        entry_to_edit = LogbookEntry(**created_log)
        # entry_to_edit = LogbookEntry(**new_entry.model_dump(by_alias=True))
        
        # 2. Make Changes directly on the object
        entry_to_edit.work_mode = "WFH"
        
        # Let's Modify the existing activity description
        entry_to_edit.detail[0].activity[0].description = "UPDATED Description via New Model"
        entry_to_edit.detail[0].activity[0].progress.percentage = 100
        
        # Let's Add a NEW activity to the list
        entry_to_edit.detail[0].activity.append(
            Activity(
                description="I am a new activity added during edit",
                progress=Progress(type="Attributes", value=2, percentage=50)
            )
        )

        # 3. Send the updated object
        print(entry_to_edit.model_dump(by_alias=True, exclude_none=True))
        edit_result = await service.edit_logbook(entry_to_edit)
        print(edit_result)
        
        # 4. Verify
        updated_data = edit_result['data']
        print(f"✅ Edit Success. Work Mode: {updated_data['work_mode']}")
        print(f"✅ Activities count: {len(updated_data['detail'][0]['activity'])}")
        print(f"✅ Activity 1: {updated_data['detail'][0]['activity'][0]['value']}")

    except Exception as e:
        print(f"🚨 Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(run_integration_test())