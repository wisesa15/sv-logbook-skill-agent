import asyncio
from core.session_manager import SessionManager
from core.api.project_service import ProjectService
from core.model.project_model import Project, UseCase
from core.utils import Utils

async def run_project_test():
    session = SessionManager()
    await session.get_api_client()
    service = ProjectService(session)
    
    print("\n--- [1] ADD PROJECT ---")
    # Define New Project
    new_project = Project(
        name="Project Alpha",
        user_id=session._user_id, # Will be ensured by service anyway
        usecases=[
            UseCase(
                name="Initial Use Case", 
                deadline=Utils.get_now_iso()
            )
        ]
    )
    
    add_resp = await service.add_project(new_project)
    # Get the ID returned by the API
    created_id = add_resp['data']['_id'] 
    created_fid = add_resp['data']['fid'] 
    print(f"✅ Created Project: {created_id} (fid: {created_fid})")

    
    print("\n--- [2] EDIT PROJECT (Add/Edit/Delete Use Cases) ---")
    
    # 1. Fetch the project we just created (to simulate real app flow)
    # In a real app, you'd probably get this from the 'add_resp' or a 'list' call
    # We hydrate it back into our Model
    try:
      del add_resp['data']['__v']
    except:
      print("gaada itu variabel gajelas")
    current_project = Project(**add_resp['data'])
    
    # 2. Modify the Object
    
    # A. Change Project Name
    current_project.name = "Project Alpha (REBRANDED)"
    
    # B. Edit the Existing Use Case (Update name, Keep ID)
    # We know index 0 exists because we just added it
    current_project.usecases[0].name = "Initial Use Case (UPDATED)"
    
    # C. Add a New Use Case (No ID)
    current_project.usecases.append(
        UseCase(
            name="Brand New Use Case",
            deadline=Utils.get_now_iso()
        )
    )
    
    # D. Delete? 
    # To delete, simply remove an item from current_project.usecases list.
    # Since we kept index 0 and appended index 1, we now have 2 use cases.
    
    # 3. Send Update
    # edit_resp = await service.edit_project(current_project)
    
    # print(f"✅ Edit Status: {edit_resp['status_code'] if 'status_code' in edit_resp else 'OK'}")
    # print(f"   Name: {edit_resp['data']['name']}")
    # print(f"   Use Cases Count: {len(edit_resp['data']['usecases'])}")
    
    # # Verify IDs
    # ucs = edit_resp['data']['usecases']
    # print(f"   UC 1 ID (Old): {ucs[0].get('_id')} - {ucs[0]['name']}")
    # print(f"   UC 2 ID (New): {ucs[1].get('_id')} - {ucs[1]['name']}")

    await session.close()

if __name__ == "__main__":
    asyncio.run(run_project_test())