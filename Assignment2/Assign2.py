import json
import urllib.request as r
import requests

result = []
wpsServerUrl = "http://130.89.221.193:85/geoserver/ows?"

f = 'https://gisedu.itc.utwente.nl/cgi-bin/mapserv.exe?map=d:/iishome/exercise/data/afrialiance/layers.map&version=2.0.0&service=WFS&request=GetFeature&typeName=neighbourhood&outputFormat=geojson&srsname=EPSG:28992'
fopen = r.urlopen(f)
raw = fopen.read()
jsonStr = json.loads(raw)  # type(jsonStr) = list

for i in range(0, 8):
    buname = jsonStr['features'][i]['properties']['bu_name']
    buname = buname.replace(' ', '%20')

    # Some loop
    payload = '''
        <wps:Execute version="1.0.0" service="WPS" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.opengis.net/wps/1.0.0" xmlns:wfs="http://www.opengis.net/wfs" xmlns:wps="http://www.opengis.net/wps/1.0.0" xmlns:ows="http://www.opengis.net/ows/1.1" xmlns:gml="http://www.opengis.net/gml" xmlns:ogc="http://www.opengis.net/ogc" xmlns:wcs="http://www.opengis.net/wcs/1.1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsAll.xsd">
  <ows:Identifier>gs:Length</ows:Identifier>
  <wps:DataInputs>
    <wps:Input>
      <ows:Identifier>feature</ows:Identifier>
      <wps:Reference mimeType="text/xml" xlink:href="http://geoserver/wps" method="POST">
        <wps:Body>
          <wps:Execute version="1.0.0" service="WPS">
            <ows:Identifier>gs:IntersectionFeatureCollection</ows:Identifier>
            <wps:DataInputs>
              <wps:Input>
                <ows:Identifier>first feature collection</ows:Identifier>
               <!--first feature is street-->  
                <wps:Reference mimeType="application/json" xlink:href="https://gisedu.itc.utwente.nl/cgi-bin/mapserv.exe?map=d:/iishome/exercise/data/afrialiance/layers.map&amp;version=2.0.0&amp;service=WFS&amp;request=GetFeature&amp;typeName=streets&amp;outputFormat=geojson&amp;srsname=EPSG:28992" method="GET"/>
              </wps:Input>
              <wps:Input>
                <ows:Identifier>second feature collection</ows:Identifier>
                <!--second feature is neighbourhood's buffer-->   
                <wps:Reference mimeType="text/xml" xlink:href="http://geoserver/wps" method="POST">
                <wps:Body>
                <wps:Execute version="1.0.0" service="WPS">
                <ows:Identifier>gs:BufferFeatureCollection</ows:Identifier>
                  <wps:DataInputs>
                    <wps:Input>
                      <ows:Identifier>features</ows:Identifier>
                      <wps:Reference mimeType="text/xml" xlink:href="http://geoserver/wps" method="POST">
                        <wps:Body>
                          <wps:Execute version="1.0.0" service="WPS">
                          <!--get the centroid of the neighbourhood-->      
                          <ows:Identifier>gs:Centroid</ows:Identifier>
                            <wps:DataInputs>
                              <wps:Input>
                                <ows:Identifier>features</ows:Identifier>
                                <wps:Reference mimeType="application/json" xlink:href="https://gisedu.itc.utwente.nl/cgi-bin/mapserv.exe?map=d:/iishome/exercise/data/afrialiance/layers.map&amp;version=2.0.0&amp;service=WFS&amp;request=GetFeature&amp;typeName=neighbourhood&amp;outputFormat=geojson&amp;srsname=EPSG:28992&amp;buname=Boddenkamp" method="GET"/>
                              </wps:Input>
                            </wps:DataInputs>
                            <wps:ResponseForm>
                            <wps:RawDataOutput mimeType="application/json">
                          <ows:Identifier>result</ows:Identifier>
                          </wps:RawDataOutput>
                            </wps:ResponseForm>
                          <!---->
                         </wps:Execute>
                        </wps:Body>
                      </wps:Reference>

                    </wps:Input>
                    <wps:Input>
                      <ows:Identifier>distance</ows:Identifier>
                      <wps:Data>
                        <wps:LiteralData>1000</wps:LiteralData>
                      </wps:Data>
                    </wps:Input>
                  </wps:DataInputs>
                  <wps:ResponseForm>
                    <wps:RawDataOutput mimeType="application/json">
                      <ows:Identifier>result</ows:Identifier>
                    </wps:RawDataOutput>
                  </wps:ResponseForm>

                  </wps:Execute>
                        </wps:Body>
                      </wps:Reference>

              </wps:Input>
            </wps:DataInputs>
            <wps:ResponseForm>
              <wps:RawDataOutput mimeType="application/json">
                <ows:Identifier>result</ows:Identifier>
              </wps:RawDataOutput>
            </wps:ResponseForm>
          </wps:Execute>
        </wps:Body>
      </wps:Reference>
    </wps:Input>
  </wps:DataInputs>
  <wps:ResponseForm>
    <wps:RawDataOutput>
      <ows:Identifier>result</ows:Identifier>
    </wps:RawDataOutput>
  </wps:ResponseForm>
</wps:Execute>
        '''%(buname)

    length = requests.post(wpsServerUrl, data=payload).text
    result.append({'neighbourhood': buname, 'length': length})

print("Content-type: application/json")
print()
#print(result)

#print(jsonStr['features'][91]['properties']['bu_name'])