import json,re
from neo4j import Driver, GraphDatabase
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
print(URI,AUTH)
driver = GraphDatabase.driver(uri=URI, auth=AUTH)




def getAllClients(request):
    with driver.session() as session:
        query = f"MATCH(c:Client) RETURN apoc.convert.toJson(c) as Total_clients_list"
        result = session.run(query)
        res = [json.loads(x.get("Total_clients_list"))for x in result]
        # print(res)
        return res

def getClient(userID):
    with driver.session() as session:
        print(userID)
        query = f"MATCH(c:Client{{userID:{userID}}}) RETURN apoc.convert.toJson(c) as Client_properties"
        result = session.run(query)
        res = [json.loads(x.get("Client_properties")) for x in result]
        # print(res)
        return res
    
def createClient(userID,c_properties):
    with driver.session() as session:
        # c_properties = json.loads(c_properties)
        print(c_properties)
        query = f"MERGE (c:Client{{userID:{userID}}}) ON CREATE \n SET "
        for key,value in c_properties.items():
            query += "c."+key+"=\""+value+"\","
        query = query[:-1]
        query += f" RETURN apoc.convert.toJson(c) as client_properties"
        
        print(query)
        
        result = session.run(query)
        res = [json.loads(x.get("client_properties")) for x in result]
        return res
            
def updateClientProperties(userID,c_properties):
    with driver.session() as session:
        print(userID,c_properties)
        query = f"MATCH (c:Client{{userID:{userID}}}) \n SET "
        for key,value in c_properties.items():
            print(key,value)
            query += "c."+key+"=\""+value+"\","
        query = query[:-1]
        query += f" RETURN apoc.convert.toJson(c) as client_properties"
        
        print(query)
        
        result = session.run(query)
        res = [json.loads(x.get("client_properties")) for x in result]
        # print = res
        return res
        
def removeClientProperties(userID,c_properties):
    with driver.session() as session:
        print(userID,c_properties)
        query = f"MATCH (c:Client{{userID:{userID}}}) \n SET "
        for key in c_properties:
            query += "c."+key+"=\"""\","
        query = query[:-1]
        query += f" RETURN apoc.convert.toJson(c) as client_properties"
        
        print(query)
        
        result = session.run(query)
        res = [json.loads(x.get("client_properties")) for x in result]
        # print = res
        return res
    
    
    

def getAllProperties(userID,token):
    with driver.session() as session:
        query = f"MATCH(c:Client{{userID:{userID},token:{token}}})<-[r:PROPERTY_OF]-(p:Property) \n"
        query += f"WHERE c.userID = r.client_uuid AND c.token = r.token \n"
        query += f"RETURN apoc.convert.toJson(p) as Total_properties_list"
        print(query)
        result = session.run(query)
        res = [json.loads(x.get("Total_properties_list"))for x in result]
        # print(res)
        return res

def getProperty(corp_Id):
    with driver.session() as session:
        query = f"MATCH(p:Property)-[r:PROPERTY_OF]-(c:Client) WHERE r.corporationID = {corp_Id}  RETURN DISTINCT apoc.convert.toJson(p) as Property_data"
        result = session.run(query)
        res = [json.loads(x.get("Property_data")) for x in result]
        # print(res)
        return res
   
def createProperty(userID,corp_Id,corporation_properties):
    with driver.session() as session:
        # print(corporation_properties)
        query = f"MERGE(c:Client{{userID:{userID}}})-[r:PROPERTY_OF{{corporationID:{corp_Id}}}]-(p:Property) \n SET "
        for key,value in corporation_properties.items():
            query += "p."+key+"=\""+value+"\","
        query = query[:-1]
        query += f" RETURN apoc.convert.toJson(p) as corporation_properties"
        
        print(query)
        
        result = session.run(query)
        res = [json.loads(x.get("corporation_properties")) for x in result]
        return res
    
def updatePropertyDetails(corp_Id,corporation_properties):
    with driver.session() as session:
        query = f"MATCH (c:Client)-[r:PROPERTY_OF{{corporationID:{corp_Id}}}]-(p:Property) \n SET "
        for key,value in corporation_properties.items():
            query += "p."+key+"=\""+value+"\","
        query = query[:-1]
        query += f" RETURN apoc.convert.toJson(p) as corporation_properties"
        
        print(query)
        
        result = session.run(query)
        res = [json.loads(x.get("corporation_properties")) for x in result]
        return res

def removePropertyDetails(corp_Id,corporation_properties):
    with driver.session() as session:
        query = f"MATCH (c:Client)-[r:PROPERTY_OF{{corporationID:{corp_Id}}}]-(p:Property) \n SET "
        for key,value in corporation_properties.items():
            query += "p."+key+"=\"""\","
        query = query[:-1]
        query += f" RETURN apoc.convert.toJson(p) as corporation_properties"
        
        print(query)
        
        result = session.run(query)
        res = [json.loads(x.get("corporation_properties")) for x in result]
        return res






def getAllVendors(property_uuid):
    with driver.session() as session:
        query = f"MATCH (p:Property)-[r:VENDOR_OF]-(v:Vendor) WHERE r.property_uuid={property_uuid} RETURN count(v) as vendor_count, apoc.convert.toJson(v) as Total_vendors_list"
        print(query)
        result = session.run(query)
        
        res = [json.loads(x.get("Total_vendors_list")) for x in result]
        # res1 = [x["vendor_count"] for x in result]
        # print(res1)
        # print(res)
        return res
    
def getVendor(property_uuid,id):
    with driver.session() as session:
        query = f"MATCH (v:Vendor)-[r:VENDOR_OF{{property_uuid:{property_uuid},id:{id}}}]-(p:Property) RETURN apoc.convert.toJson(v) as vendors_details"
        print(query)
        result = session.run(query)
        res = [json.loads(x.get("vendors_details"))for x in result]
        return res
        
        
def createVendor(property_uuid,id):
    with driver.session() as session:
        query = f"MERGE (v:Vendor)-[r:VENDOR_OF{{property_uuid:{property_uuid},id:{id}}}]-(p:Property) SET"
         
        query += "RETURN apoc.convert.toJson(v) as vendors_details"
        pass





        
def update_relPropsOf_Property_of(client_uuid,corporationID,relationship_properties):
    with driver.session() as session:
        print(client_uuid,corporationID,relationship_properties)
        query = f"MATCH(c:Client)-[r:PROPERTY_OF{{client_uuid:{client_uuid},corporationID:{corporationID}}}]-(p:Property) \n SET "
        for key,value in relationship_properties.items():
            query += "r."+key+"=\""+value+"\","
        query = query[:-1]
        query += f" RETURN apoc.convert.toJson(r) as rel_props"
        
        print(query)
        
        result = session.run(query)
        res = [json.loads(x.get("rel_props")) for x in result]
        return res
    
def remove_relPropsOf_Property_of(client_uuid,corporationID,relationship_properties):
    with driver.session() as session:
        query = f"MATCH(c:Client)-[r:PROPERTY_OF{{client_uuid:{client_uuid},corporationID:{corporationID}}}]-(p:Property) \n SET "
        for key,value in relationship_properties.items():
            query += "r."+key+"=\"""\","
        query = query[:-1]
        query += f" RETURN apoc.convert.toJson(r) as rel_props"
        
        print(query)
        
        result = session.run(query)
        res = [json.loads(x.get("rel_props")) for x in result]
        return res    
            
def update_relPropsOf_Vendor_of(client_uuid,corporationID,id,relationship_properties):
    with driver.session() as session:
        print(client_uuid,corporationID,relationship_properties)
        query = f"MATCH(v:Vendor)-[r:VENDOR_OF{{client_uuid:{client_uuid},corporationID:{corporationID},id:{id}}}]-(p:Property) \n SET "
        for key,value in relationship_properties.items():
            query += "r."+key+"=\""+value+"\","
        query = query[:-1]
        query += f" RETURN apoc.convert.toJson(r) as rel_props"
        
        print(query)
        
        result = session.run(query)
        res = [json.loads(x.get("rel_props")) for x in result]
        return res
    
def remove_relPropsOf_Vendor_of(client_uuid,corporationID,id,relationship_properties):
    with driver.session() as session:
        query = f"MATCH(v:Vendor)-[r:VENDOR_OF{{client_uuid:{client_uuid},corporationID:{corporationID}.id:{id}}}]-(p:Property) \n SET "
        for key,value in relationship_properties.items():
            query += "r."+key+"=\"""\","
        query = query[:-1]
        query += f" RETURN apoc.convert.toJson(r) as rel_props"
        
        print(query)
        
        result = session.run(query)
        res = [json.loads(x.get("rel_props")) for x in result]
        return res 


















def check_properties_of_client(query):
    with driver.session() as session:
        # print(query)
        cquery = f"MATCH (c:Client{{name:\"{query}\"}})-[r:PROPERTY_OF]-(p:Property) return apoc.convert.toJson(p) as jsondata"
        # print(cquery)
        result = session.run(cquery)
        

        res = [json.loads(x.get("jsondata")) for x in result]

        # print(res)

        return res
    
def check_vendors_of_property(query):
    with driver.session() as session:
        # print(query)
        cquery = f"MATCH (p:Property{{name:\"{query}\"}})-[r:VENDOR_OF]-(v:Vendor) return apoc.convert.toJson(v) as jsondata"
        # print(cquery)
        result = session.run(cquery)
        

        res = [json.loads(x.get("jsondata")) for x in result]
        
        # print(res)

        return res    
    

def setFieldValue(query):
    with driver.session() as session:
        
        query =json.loads(query)
        node_label,name,field,value = query.values()
        # print(node_label,name,field,value)
        cquery = f"MATCH (d:{node_label}{{name:\"{name}\"}}) \n SET d.{field} = \"{value}\" \n RETURN apoc.convert.toJson(d) as result" 

        print(cquery)  
        
        result = session.run(cquery)
        res = [json.loads(x.get("result")) for x in result]
        # res = res[0]["properties"][field]
        print(res)
        return res


def removeFieldValue(query):
    with driver.session() as session:
        
        query =json.loads(query)
        node_label,name,field = query.values()
        # print(node_label,name,field,value)
        cquery = f"MATCH (d:{node_label}{{name:\"{name}\"}}) \n SET d.{field} = \'\'\n RETURN apoc.convert.toJson(d) as result" 

        print(cquery)  
        
        result = session.run(cquery)
        res = [json.loads(x.get("result")) for x in result]
        print(res)
        return res    
    

def createNode(query):
        query = json.loads(query)
        node_label,node_properties = query.values()
        print(node_label,node_properties)
        cquery = f"MERGE(e:{node_label}) ON CREATE SET"
        for key,value in node_properties.items():
            cquery += "\n e."+key+"=\""+value+"\","
        cquery = cquery[:-1]  
        cquery += f" \n RETURN apoc.convert.toJson(e) as result"         
        print(cquery)
        
        with driver.session() as session:
            result =session.run(cquery)
            res = [json.loads(x.get("result")) for x in result] 
            print(res)
            return res
            
def createRelationship(query):
    query = json.loads(query)
    print(query)
    node1 = query["node1"]
    cquery = f"MATCH(e:Employee)"        

    