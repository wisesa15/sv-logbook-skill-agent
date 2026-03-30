#!/usr/bin/env python3

import sys
import json
import argparse
import asyncio
from typing import Any, Dict

from core.api.project_service import ProjectService 
from core.session_manager import SessionManager 


async def async_business_logic(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Your async logic goes here.
    Example: API calls, DB queries, httpx, aiofiles, etc.
    """

    # Read Logbook
    session = SessionManager()
    await session.get_api_client()

    service = ProjectService(session)
    projects = await service.list_projects()
    await session.close()

    return projects


def parse_cli_args() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(description="Async JSON Processor")

    parser.add_argument("--id", type=str)

    args = parser.parse_args()
    
     # Convert Namespace → dict and remove None values
    args_dict = {k: v for k, v in vars(args).items() if v is not None}

    return args_dict


def parse_stdin() -> Dict[str, Any]:
    try:
        if not sys.stdin.isatty():
            return json.load(sys.stdin)
        return {}
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {e}")


async def main():
    try:
        # STDIN takes priority
        input_data = parse_stdin()
        if not input_data:
            input_data = parse_cli_args()
            
        result = await async_business_logic(input_data)
        result = result['data']
        if input_data: # masukkin id
            result = [r for r in result if r['fid'] == input_data['id']]

        print(json.dumps(result))

    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e)
        }
        print(json.dumps(error_response))
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
