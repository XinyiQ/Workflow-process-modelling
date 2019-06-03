from osgeo import ogr
from osgeo import osr
 
def title():
    return "Union of geometries" # title of the function
 
def abstract():
    return "A function that union two geometries into one." # short description of the function
 
def inputs():
    return [
        ['first', 'First feature','The first inputfeature.','application/json', True],
        ['second', 'Second feature', 'The second inputfeature.', 'application/json', True]
    ]
 
def outputs():
    return [['result', 'Union feature','The feature in the union of two input features','application/json']]
 
def execute(parameters):
    first = parameters.get('first')
    second = parameters.get('second')
    if (first is not None) and (second is not None):
        first = first['value']
        second = second['value']

    firstf = ogr.CreateGeometryFromWkt(first)
    secondf = ogr.CreateGeometryFromWkt(second)

    union = firstf.Union(secondf)
    
    print("Content-type: application/json")
    print()
    print(union.ExportToJson())