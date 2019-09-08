#!/usr/bin/python3
# -*- coding: utf-8 -*-


"""
Types

Arrays and objects require new layouts?

object.key
object.value
object.schema

schema:
- type: type of value 
   "type": int, string, float, array, dict, undefined

an undefined type can be anything, but it will not be included in the interface (although it may be displayed as a string)


#example for array
{
   "value":<value>,
   "schema":{
      "type":"array",
      "schema:"{
         "key":<name>
         "type":<type>
      }
   }

}

"""

class SmartType:
   types = ["string", "int", "float", "bool", "array", "object"]

   ##
   # \brief Default initializer
   # \param [in] key name of the item
   # \param [in] value value to set the item to
   # \param [in] schema Json object that defines what the object may contain
   def __init__(self, key, value, schema=None):
       self.key = key
       self.type = "Unknown"

       self.schema= None
       if schema != None:
          self.setSchema( schema)

          try:
             self.type = schema["bsonType"]
          except: 
              pass

             

#       print(str(key)+" setting value to "+str(value)+" with schema: "+str(self.schema))
       
#       self.value = value

       #If a schema is undefined, the value is converted to a reado-only string
       if self.schema == None:
           print("No schema for key "+str(self.key))
           self.value = str( value )
           self.readOnly = True
       else:
          self.setValue( value)


   ##
   # \brief sets the schema for the Type
   # \param [in] schema Json object that specifies information about the object
   # \return true on success, false on failure
   #
   def setSchema( self, schema ):
       #If not specified, read only. 
       if schema == None:
           self.schema =schema 
           return True

       #Make sure we are a dictionary
       elif not isinstance( schema, dict ):
           print("Error: schema is not a object "+str(schema))
           return False

       self.schema = schema 

       return True

   ##
   # \brief specifies the value that the device should have
   # \param [in] Value to set. 
   # \return true on success, false on failure
   #
   # This function is used to set a new value to  item
   def setValue(self, value ):
       self.value = None
       #If a schema is undefined, the value is converted to a reado-only string
       if self.schema == None:
           print("No schema for key "+str(self.key))
           self.value = value
           self.readOnly = True
           return True

       #check schema type
       if self.schema["bsonType"] == "string":
           if isinstance( value, str):
               self.value = value
           elif self.value != None:
               print("SmartType::Error - Value type "+str(self.value)+" does not match schema type of \"string\"")
               return False

       elif self.schema["bsonType"] == "int":
           if isinstance( value, int ):
               self.value = value
           elif self.value != None:
               print("SmartType::Error - Value type does not match schema type of \"int\"")
               return False

       elif self.schema["bsonType"] == "number":
           if isinstance( value, float ):
               self.value = value
           elif self.value != None:
               print("SmartType::Error - Value type does not match schema type of \"number\"")
               return False

       elif self.schema["bsonType"] == "bool":
           if isinstance( value, bool ):
               self.value = value
           elif self.value != None:
               print("SmartType::Error - Value type does not match schema type of \"bool\"")
               return False

       elif self.schema["bsonType"] == "object":
           print(str(self.key)+" object value:"+str(value)+", schema:"+str(self.schema ))
         
           if isinstance( value, dict ):
               self.value = value
           elif self.value != None:
               print( "---- Value:"+str(self.value))
               print( "SmartType::Error - Value type does not match schema type of \"object\"")
               return False
#           print(str(self.key)+" set object value:"+str(self.value)+", schema:"+str(self.schema))

       #We are an array type
       elif self.schema["bsonType"] == "array":
           #if the value is not a list, return false. 
           if not isinstance( value, list ):
               print("SmartType::Error - unable to set an array type to a non-array value")
               return False

           #If any items are not of the correct type print an error and set valiu to False
           valid=True

           #Try/catch for unspecified schema. If the schema is not specified, treat it as mixed
           #Mixed type not validated since anything goes
           try:
               for item in value:
                   if self.schema["items"]["type"] == "string":
                       if not isinstance( item, str):
                           print("SmartType::Error array schema mismatch -"+ str(item)+" is not a string")
                           valid = False
                   elif self.schema["items"]["type"] == "integer":
                       if not isinstance( item, int):
                           print("SmartType::Error array schema mismatch -"+ str(item)+" is not an integer")
                           valid = False
                   elif self.schema["items"]["type"] == "number":
                       if not isinstance( item, float) and not isinstance( item, int):
                           print("SmartType::Error array schema mismatch -"+ str(item)+" is not a number")
                           valid = False
                   elif self.schema["items"]["type"] == "boolean":
                       if not isinstance( item, bool):
                           print("SmartType::Error array schema mismatch -"+ str(item)+" is not a boolean")
                           valid = False
                   elif self.schema["items"]["type"] == "array":
                       if not isinstance( item, list):
                           print("SmartType::Error array schema mismatch -"+ str(item)+" is not an array")
                           valid = False
                   elif self.schema["items"]["type"] == "object":
                       if not isinstance( item, dict):
                           print("SmartType::Error object schema mismatch -"+ str(item)+" is not an object")
                           valid = False
                       else:
                           print("Item: "+str(item)+" is an object")
                   else:
                       print("SmartType::Error unknown type: "+str(self.schema["items"]["type"]))
                       valid = False
           except:
               #SDF: Need a NOP....`
               print("SmartType::Warning Using mixed type as a default")

           #If any item fails, return false
           if not valid:
               print("SmartType::Error Failed to set value:" + str(value))
               return False

           else:
               self.value = value
               return True
               
   ##
   # \brief Append a vlue to an array
   # \param in value the new value to append to the array
   def appendValue( self, value ):
       #If we're not an array type, print ann erro and return false
       if self.type != "array":
           print("SmartType::error: Non-array types cannot append values") 
           return False

       #See if we have a schema. If not, add value by default and exit 
       if self.schema == None:
           self.value.append(value)
           return True
            
       #We should have a schema. Let's figure out if its a match
       valid = True
       try:
           #If the schema doesn't specify a type
           if isinstance(self.schema["items"]["type"], str):
               if self.schema["items"]["type"] == "string":
                   if not isinstance( value, str):
                       valid = False
               elif self.schema["items"]["type"] == "integer":
                   if not isinstance( value, int):
                       valid = False
               elif self.schema["items"]["type"] == "number":
                   if not isinstance( value, float) and not isinstance( value, int):
                       print(str(value)+" is not a number")
                       valid = False
               elif self.schema["items"]["type"] == "boolean":
                   if not isinstance( value, bool):
                       valid = False
               elif self.schema["items"]["type"] == "object":
                   if not isinstance( value, object):
                       valid = False
               elif self.schema["items"]["type"] == "array":
                   if not isinstance( value, list):
                       valid = False
               elif self.schema["items"]["type"] != "mixed":
                   valid = False


               if not valid:
                   print( str(item)+" is not of type "+str(self.schema["items"]["type"])) 
               else:
                   self.value.append( value  )
                   return True
           else:
              print("SmartType::Error: Schema type is not a string")
              return False
       except:
           print("SmartType::Error: Invalid schema "+str(self.schema))
           return False
       

   ##
   # \brief Tries to set the string to the given type
   def setStringAsValue( self, text ):
       #make sure the input is a string
       if not isinstance( text, str ):
           print("SmartType::setStringAsValue input not string")
           return False

       #Set to string
       if self.schema["bsonType"] == "string":
          try: 
              self.setValue( str(text))
          except:
              return False

       #Set to string
       if self.schema["bsonType"] == "int":
          try: 
              self.setValue( int(text))
          except:
              return False

       #Set to string
       if self.schema["bsonType"] == "number":
          try: 
              self.setValue( float(text))
          except:
              return False

       #Set to string
       if self.schema["bsonType"] == "bool":
          #Convert string to boolean type
          if text == "True":
              bval = True
          elif text == "False":
              bval = False
          else:
              return False;

          try: 
              self.setValue(bval)
          except:
              return False

       #Set to string
       if self.schema["bsonType"] == "object":
           print("SmartType::setStringAsValue Unable to convert string to object.")
           return False

       #Set to string
       if self.schema["bsonType"] == "array":
           print("SmartType::setStringAsValue Unable to convert string to array.")
           return False

       return True

##
# \brief Test function
def unitTest():
      ###############
      #Test strings
      ###############

      type1 = SmartType( "string", "value1", {"bsonType":"string"})
      if type1.value != "value1":
          print("key 1 Unable to set string value")
          return False

      if not type1.setStringAsValue("test2"):
          print("Unable to set string value for string")
          return False

      #try non-string values
      if type1.setValue(15):
          print("FAILURE set string to an int")
          return False

      ###############
      #Test Integers
      ###############
      type1 = SmartType( "int", 1, {"bsonType":"int"})
      if type1.value != 1:
          print("Failure: Value not set to 1")
          return False

      if not type1.setStringAsValue("2"):
          print("Unable to set string value for int")
          return False

      if type1.value != 2:
          print("Failure: Value not set to 1")
          return False

      #try non-string values
      if type1.setValue("test"):
          print("FAILURE set int to a string")
          return False

      ###############
      # Test Floats
      ###############
      type1 = SmartType( "float", 1.1, {"bsonType":"number"})
      if type1.value != 1.1:
          print("Failure: Float value not set to 1.1")
          return False

      if not type1.setStringAsValue("1.2"):
          print("Unable to set string value for float")
          return False

      if type1.value != 1.2:
          print("Failure: Float value not set to 1.1")
          return False

      #try non-string values
      if type1.setValue(99):
          print("FAILURE set float to a string")
          return False
      
      ###############
      # Test Bools
      ###############
      type1 = SmartType( "bool", True, {"bsonType":"bool"})
      if type1.value != True:
          print("Failure: Bool value not set to True")
          return False

      if not type1.setStringAsValue("False"):
          print("Unable to set string value for bool")
          return False

      if type1.value != False:
          print("Failure: Bool value not set to False")
          return False

      #try non-string values
      if type1.setValue(99):
          print("FAILURE set bool to an int")
          return False

      ###############
      # Test Lists
      ###############
      testArray = ({
         "string":{ "value":["A","B","C"],
                    "schema": {"bsonType":"array", "items":{"type":"string"}}
                   },
         "integer":{ "value":[1,2,3],
                    "schema": {"bsonType":"array", "items":{"type":"integer"}}
                    },
         "number":{"value":[1.1,2.1,3.1],
                    "schema": {"bsonType":"array", "items":{"type":"number"}}
                   },
         "boolean":{ "value":[True, False, True],
                    "schema": {"bsonType":"array", "items":{"type":"boolean"}}
                    },
         "mixed":{ "value":["A",2,True],
                    "schema": {"bsonType":"array", "items":{"type":"mixed"}}
                 },
         "array":{ "value":[[1,2,3],[4,5,6],[7,8,9]],
                    "schema": {"bsonType":"array", "items":{"type":"array"}}
                 },
         "object":{ "value":[{"key1":1},{"key2":2},{"key3":3}],
                    "schema": {"bsonType":"array", "items":{"type":"object"}}
                   }
      })

      valid = True

      #Get a list of all keys in the test array. This will be used for comparison
      keys = testArray.keys()

      #Try to create a SmartType for every key in the testArray and try to assign
      #all other keys to that key type.
      for k in testArray:
         #Try to create a type for each key
         for key in keys:
            smartType = SmartType( k, testArray[key]["value"], testArray[k]["schema"])

            #We should only succeed when k = key unless k is mixed or if an integer 
            #array is mapped to a number. The following statement should only be true
            #for compatible keys.
            if smartType.value == testArray[key]["value"]:
               #Good cases
               if( k == key or 
                   k == "mixed" or
                   (k == "integer" and key == "boolean") or 
                   (k == "number" and key == "boolean")  or 
                   (k == "number" and key == "integer")  
                 ):
                     continue
               #Not good. Print Failure and set valid to falks             
               else:
                   print("Failure: "+str(k)+","+str(key)+" values match: "+str(smartType.value))
                   valid = False

      print("Return valid = "+str(valid))
      return valid
               

      """


      intData = [1,2,3,4]
      intRefData  = [1,2,3,4]

      #test array with no type
#      type1 = SmartType( "array", data, {"bsonType":"array"})

      if type1.value != data:
          print("Failure: array value not set to "+str(data))
          return False

      #try non-string values
      if type1.setValue(99):
          print("FAILURE set array to a string")
          return False

      #test array with string type
      type2 = SmartType( "array", data, {"bsonType":"array", "items":{"type":"string"}})
      if type2.value == data:
         print("Failure: array of numbers set to a string type for array testing")
         return False

      #test float type for an array of ints
      type3 = SmartType( "array", data, {"bsonType":"array", "items":{"type":"number"}})
      if type3.value != data:
         print("Failure: array of integers are not mapped to floats")
         return False

      objectData=[{"test":1},"test",2}]
      

      #check appends
      print("Checking appends")
      #TODO Check all types
      type4 = SmartType( "array", data, {"bsonType":"array", "items":{"type":"number"}})
      if type4.appendValue("testString"):
         print("Failure: appended a string to a number array passed")
         return False


      #TODO Check all types
      type4 = SmartType( "array", data, {"bsonType":"array", "items":{"type":"number"}})
      if not type4.appendValue(1):
         print("Failure: unable append an integer to a number array passed")
         return False

      ref.append(1)
      if type4.value != ref:
         print("Failure: data mismatch after appending value")
         return False
      """


      ###############
      # Test Dicts
      ###############
      data = {"key":"value"}
      type1 = SmartType( "object", data, {"bsonType":"object"})
      if type1.value != data:
          print("Failure: object value not set to "+str(data))
          return False

      #try non-string values
      if type1.setValue(99):
          print("FAILURE set object to a string")
          return False
     
      ###############
      # Test Error States
      ###############
      return True

##
# \brief Main function
if __name__ == '__main__':
    result = unitTest()

    if result == True:
        print( "Unit test passed")
        exit(1)
    else:
        print( "Unit test FAILED")
