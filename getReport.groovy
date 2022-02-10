import groovy.json.JsonSlurper
import java.io.File;

if (JSON_REPORT_ID){

def jsonSlurper = new JsonSlurper()
data = jsonSlurper.parse(new File('json-reports/' + JSON_REPORT_ID + '.json'))
 
return data
} else {
return ""
}