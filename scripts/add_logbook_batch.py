#!/usr/bin/env python3
# other library
import sys
import json
import asyncio
from pydantic import BaseModel, ValidationError
import uuid
# personal library
from core.api.logbook_service import LogbookService
from core.model.logbook_model import LogbookEntry, LogbookDetail, Activity, Tool
from core.session_manager import SessionManager 
from core.utils import Utils

# ==============================
# Entrypoint
# ==============================

async def main():
    try:
        # input-related
        raw = sys.stdin.read()
        if not raw.strip():
            raise ValueError("No input provided")
        raw = json.loads(raw)

        # API
        session = SessionManager()
        await session.get_api_client()
        service = LogbookService(session)
      
        for i in range(len(raw)):
            # lengkapin data-nya
            raw[i]['current_team']= session._user_team
            raw[i]['user_id'] = session._user_id
            now = Utils.get_now_iso()
            raw[i]['created_at'] = now
            raw[i]['updated_at'] = now
        # Validate JSON + schema
        validated = []
        for r in raw:
            r = json.dumps(r)
            v = LogbookEntry.model_validate_json(r)
            validated.append(v)
        # add project
        add_resps = await service.add_logbooks_batch(validated)
        
        # Get the ID returned by the API
        for add_resp in add_resps:
            created_id = add_resp['data']['_id'] 
            created_fid = add_resp['data']['fid'] 
            if add_resp['status_code'] != 201:
                raise ValueError
            else:
                print(f"✅ Created Logbooks: {created_id} (fid: {created_fid})")


    except ValidationError as e:
        print(json.dumps({
            "success": False,
            "error_type": "validation_error",
            "details": e.errors()
        }))
        sys.exit(1)

    except Exception as e:
        print(json.dumps({
            "success": False,
            "error_type": "runtime_error",
            "message": str(e)
        }))
        sys.exit(1)
    finally:
        await session.close()



if __name__ == "__main__":
    asyncio.run(main())
