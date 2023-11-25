from fastapi import Body, FastAPI, Request,Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from kb_queries import *

app = FastAPI()

@app.get("/client", response_class=JSONResponse, tags=["client"])
async def get_all_clients(request:Request,):
    res = getAllClients(request)
    return res
    

@app.get("/client/{userID}", response_class=JSONResponse, tags=["client"])
async def get_client_details(request:Request,userID:str):
    res = getClient(userID)
    return res

@app.post("/client", response_class=JSONResponse, tags=["client"])  
async def create_client(request:Request,client_properties:dict = Body(...)):
    res = createClient(client_properties)
    return res
    

@app.patch("/client", response_class=JSONResponse, tags=["client"])
async def update_client(request:Request,userID:str,client_properties:dict = Body(...)):
    res = updateClientProperties(userID,client_properties)
    return res

@app.delete("/client", response_class=JSONResponse, tags=["client"])
async def remove_client(request:Request,userID:str,client_properties:list = Body(...)):
    res = removeClientProperties(userID,client_properties)
    return res



@app.get("/property", response_class=JSONResponse, tags=["property"])
async def get_all_properties_of_a_client(request:Request, userID:str,token:str):
    res = getAllProperties(userID,token)
    return res

@app.get("/property/{corp_Id}", response_class=JSONResponse, tags=["property"])
async def get_property_details(request:Request,corp_Id:str):
    res = getProperty(corp_Id)
    return res

@app.post("/property", response_class=JSONResponse, tags=["property"])
async def create_property(request:Request,userID:str,corp_Id:str,corporation_properties:dict=Body(...)):
    res = createProperty(userID,corp_Id,corporation_properties)
    return res

@app.patch("/property", response_class=JSONResponse, tags=["property"])
async def update_property():
    pass

@app.delete("/property", response_class=JSONResponse, tags=["property"])
async def remove_property():
    pass


@app.get("/vendor", response_class=JSONResponse, tags=["vendor"])
async def get_all_vendors(property_uuid:str):
    res = getAllVendors(property_uuid)
    return res

@app.get("/vendor/{id}", response_class=JSONResponse, tags=["vendor"])
async def get_vendor(request:Request,property_uuid:str,id:str):
    res = getVendor(property_uuid,id)
    return res

@app.post("/vendor", response_class=JSONResponse, tags=["vendor"])
async def create_vendor():
    pass

@app.patch("/vendor", response_class=JSONResponse, tags=["vendor"])
async def update_vendor():
    pass

@app.delete("/vendor", response_class=JSONResponse, tags=["vendor"])
async def remove_vendor():
    pass


@app.get("/vendor_of", response_class=JSONResponse, tags=["vendor_of"])
async def get_all_vendor_ofs():
    pass

@app.get("/vendor_of/{cname}", response_class=JSONResponse, tags=["vendor_of"])
async def get_vendor_of():
    pass

@app.post("/vendor_of", response_class=JSONResponse, tags=["vendor_of"])
async def create_vendor_of():
    pass

@app.patch("/vendor_of", response_class=JSONResponse, tags=["vendor_of"])
async def update_vendor_of():
    pass

@app.delete("/vendor_of", response_class=JSONResponse, tags=["vendor_of"])
async def remove_vendor_of():
    pass

@app.get("/property_of", response_class=JSONResponse, tags=["property_of"])
async def get_all_property_ofs():
    pass

@app.get("/property_of/{cname}", response_class=JSONResponse, tags=["property_of"])
async def get_property_of():
    pass

@app.post("/property_of", response_class=JSONResponse, tags=["property_of"])
async def create_property_of():
    pass

@app.patch("/property_of", response_class=JSONResponse, tags=["property_of"])
async def update_property_of():
    pass

@app.delete("/property_of", response_class=JSONResponse, tags=["property_of"])
async def remove_property_of():
    pass

