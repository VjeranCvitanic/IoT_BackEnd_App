from fastapi import FastAPI, HTTPException
import requests
import uvicorn
import json

app = FastAPI()

# Configuration (replace with your details)
HOMEASSISTANT_URL = "https://najjacagrupa.ninja"
API_PASSWORD = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmNTU3YzNjOWY0N2Q0NmFjOWVlYjY3ZDRjMTU2OWM4NyIsImlhdCI6MTcxNzUxNzk0NywiZXhwIjoyMDMyODc3OTQ3fQ.3GHy5DYqEDIoc8SzXiWnBRRwVH1qvIlM7irDromKHkQ"

# GET
# "/"
# "/all"
# "/sensor"
# "/chair"
# "/all_locations"
#
# "/start_info"         ----------->   fetches data from every location and room
# "/{location}/{room}"  ----------->   fetches data from specific room

# Helper function to make authenticated requests to HomeAssistant
def call_ha_api(method: str, endpoint: str, json: dict = None):
    url = f"{HOMEASSISTANT_URL}/api{endpoint}"
    headers = {"Authorization": f"Bearer {API_PASSWORD}"}
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        else:
            raise NotImplementedError(f"Method {method} not supported")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=response.status_code, detail=str(http_err))
    except requests.exceptions.ConnectTimeout as timeout_err:
        raise HTTPException(status_code=504, detail=f"Connection timed out: {str(timeout_err)}")
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))

# Path operation to get all states
@app.get("/all")
async def get_states():
    endpoint = "/states"
    #return {"message": "Welcome to the Home Assistant API integration"}
    states = call_ha_api("GET", endpoint)

    for elem in states:
        partial_data = {
            "entity_id": elem.get("entity_id"),
            "state": elem.get("state"),
        }
        print(partial_data)  # Print the filtered partial data
    
    return 0


@app.get("/")
async def get_states():
    endpoint = "/states"
    #return {"message": "Welcome to the Home Assistant API integration"}
    states = call_ha_api("GET", endpoint)
    allowed_types = ["counter", "sensor", "binary_sensor", "automation", "weather"]  # Example types

    filtered_entities = []

    for elem in states:
        entity_id = elem.get("entity_id")
        
        # Check if the entity_id starts with any of the allowed types
        if any(entity_id.startswith(allowed_type + ".") for allowed_type in allowed_types):
            partial_data = {
                "entity_id": entity_id,
                "state": elem.get("state"),
            }
            filtered_entities.append(partial_data)
            print(partial_data)  # Print the filtered partial data
    
    return filtered_entities


@app.get("/sensor")
async def get_states():
    endpoint = "/states"
    #return {"message": "Welcome to the Home Assistant API integration"}
    states = call_ha_api("GET", endpoint)

    allowed_types = ["sensor"]  # Example types

    filtered_entities = []

    for elem in states:
        entity_id = elem.get("entity_id")
        
        # Check if the entity_id starts with any of the allowed types
        if any(entity_id.startswith(allowed_type + ".") for allowed_type in allowed_types):
            partial_data = {
                "entity_id": entity_id,
                "state": elem.get("state"),
            }
            filtered_entities.append(partial_data)
            print(partial_data)  # Print the filtered partial data
    
    return filtered_entities

@app.get("/chair")
async def get_states():
    endpoint = "/states"
    #return {"message": "Welcome to the Home Assistant API integration"}
    states = call_ha_api("GET", endpoint)

    allowed_types = ["binary_sensor"]  # Example types

    filtered_entities = []

    for elem in states:
        entity_id = elem.get("entity_id")
        
        # Check if the entity_id starts with any of the allowed types
        if any(entity_id.startswith(allowed_type + ".") for allowed_type in allowed_types):
            partial_data = {
                "entity_id": entity_id,
                "state": elem.get("state"),
            }
            filtered_entities.append(partial_data)
            print(partial_data)  # Print the filtered partial data
    
    return filtered_entities

@app.get("/all_locations")
async def get_states():
    endpoint = "/states"
    #return {"message": "Welcome to the Home Assistant API integration"}
    states = call_ha_api("GET", endpoint)

    allowed_types = ["zone"]  # Example types

    locations = []

    for elem in states:
        entity_id = elem.get("entity_id")
        
        # Check if the entity_id starts with any of the allowed types
        if any(entity_id.startswith(allowed_type + ".") for allowed_type in allowed_types):
            entity_id = entity_id.split(".")[1]
            partial_data = {
                "entity_id": entity_id,
            }

            locations.append(partial_data)
    
    return locations

@app.get("/start_info")
async def get_states():
    endpoint = "/states"
    #return {"message": "Welcome to the Home Assistant API integration"}
    states = call_ha_api("GET", endpoint)

    allowed_types = ["zone"]  # Example types

    locations = []

    for elem in states:
        entity_id = elem.get("entity_id")
        
        # Check if the entity_id starts with any of the allowed types
        if any(entity_id.startswith(allowed_type + ".") for allowed_type in allowed_types):
            entity_id = entity_id.split(".")[1]

            locations.append(entity_id)
    
    info = []
    for location in locations:
        loc_info = []
        loc_info.append(location)
        loc_info.append(get_location_info(location))
        info.append(loc_info)

    print(info)
    return info

def get_location_info(location):
    endpoint = "/states"
    #return {"message": "Welcome to the Home Assistant API integration"}
    states = call_ha_api("GET", endpoint)

    allowed_types = ["counter"]  # Example types

    #rooms in this location
    rooms = []
    rooms_info = []

    for elem in states:
        entity_id = elem.get("entity_id")
        
        # Check if the entity_id starts with any of the allowed types
        if any(entity_id.startswith(allowed_type + ".") for allowed_type in allowed_types):
            # Split entity_id by underscores
            parts = entity_id.split("_")
            if len(parts) >= 2:
                # Extract the location from the first part
                entity_location = parts[0].split(".")[1]  # Extract location from "counter.location1"
                # Check if the entity's location matches the provided location
                if entity_location == location:
                    entity_id = parts[1]
                    partial_data = {
                        "room_id": entity_id,
                    }
                    rooms.append(partial_data)

    for room in rooms:
        room_info = []
        room_info.append(room)
        room_info.append(get_room_info(location, room.get("room_id")))

        rooms_info.append(room_info)
    
    return json.dumps(rooms_info)

@app.get("/{location}/{room}")
def get_room_info(location, room):
    endpoint = "/states"
    #return {"message": "Welcome to the Home Assistant API integration"}
    states = call_ha_api("GET", endpoint)

    allowed_types = ["counter", "sensor", "binary_sensor"]  # Example types

    #rooms in this location
    room_info = []

    for elem in states:
        entity_id = elem.get("entity_id")
        
        # Check if the entity_id starts with any of the allowed types
        if any(entity_id.startswith(allowed_type + ".") for allowed_type in allowed_types):
            # Split entity_id by underscores
            parts = entity_id.split("_")
            if len(parts) >= 2:
                # Extract the location from the first partž
                try:
                    entity_location = parts[0].split(".")[1]  # Extract location from "counter.location1"
                    room_id = parts[1]
                except:
                    entity_location = parts[1].split(".")[1]  # Extract location from "counter.location1"
                    room_id = parts[2]
                # Check if the entity's location matches the provided location
                if entity_location == location:
                    if(room_id == room):
                        try:
                            entity_id = parts[3]
                        except:
                            entity_id = parts[2]
                        partial_data = {
                            "entity_id": entity_id,
                            "state": elem.get("state"),
                        }
                        room_info.append(partial_data)

    return room_info
