#!/usr/bin/env python3
# other library
import sys
import json
import asyncio
from pydantic import BaseModel, ValidationError
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
        fid = raw['fid']

        # API
        session = SessionManager()
        await session.get_api_client()
        service = LogbookService(session)
      
      
        # lengkapin data-nya
        raw = json.dumps(raw)
        # Validate JSON + schema
        validated = LogbookEntry.model_validate_json(raw)
        
        # add project
        add_resp = await service.edit_logbook(validated)
        
        # Get the ID returned by the API
        if add_resp['status_code'] != 200:
            raise ValueError
        else:
          print(f"✅ Successfully edited Logbook: {fid}")


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
