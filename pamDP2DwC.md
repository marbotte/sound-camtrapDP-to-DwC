# From pamDP to DwC
Marius Bottin

This document is to show quickly how to analyse the structure and
variables of pamDP data formats and to transform it to the DarwinCore
format (event + Audiovisual Media Description + registers). Of course,
it would be better to make a python code that could be integrated with
the codes the soundscape team develop in the institute, but the
objective here is only to show a proof of concept.

# Reading data

I put the data in the a directory `data_transformacion` at level -1 of
this repository.

First, we read the mapping xlsx file:

``` r
require(openxlsx)
```

    Loading required package: openxlsx

``` r
wb<-loadWorkbook("../data_transformacion/Sistematización de datos - pamDP.xlsx")
mapping<-lapply(names(wb),function(x)read.xlsx(xlsxFile=wb,sheet=x))
names(mapping)<-names(wb)
```

The structure of the mapping file is somewhat dirty, if we want to
automatize more the process in the future, we will need to clean that:

``` r
lapply(mapping,colnames)
```

    $media.csv
     [1] "Inlcuir.en.PAMFLOW"                 "pamDP.Field.Name"                  
     [3] "Description"                        "Required"                          
     [5] "Type"                               "Example"                           
     [7] "Incluir.en.DarwinCore"              "DarwinCore"                        
     [9] "Core/Extensión"                     "DarwinCore"                        
    [11] "Observaciones"                      "pamflow.(audio_metadata)"          
    [13] "Formato.de.migración.CSA.-.Pasivos" "Formato.de.migración.CSA"          

    $deployments.csv
     [1] "Inlcuir.en.PAMFLOW"                                                                                                  
     [2] "FDM.-.Included.-.Son.campos.que.deben.venir.del.FDM,.pueden.ser.obligatorios.o.facultativos,.según.columna.required."
     [3] "pamDP.-.Field.Name"                                                                                                  
     [4] "Descripción.del.campo.(basado.en.camtrapDP)"                                                                         
     [5] "Required"                                                                                                            
     [6] "Type"                                                                                                                
     [7] "Example"                                                                                                             
     [8] "Incluir.en.DarwinCore"                                                                                               
     [9] "DarwinCore"                                                                                                          
    [10] "Core/Extensión"                                                                                                      
    [11] "Comentarios"                                                                                                         
    [12] "DarwinCore"                                                                                                          
    [13] "pamflow.(metadata_summary)"                                                                                          
    [14] "Formato.de.migración.CSA"                                                                                            

    $observation.csv
     [1] "Inlcuir.en.PAMFLOW"                         
     [2] "pamDP.-.Field.Name"                         
     [3] "Descripción.del.campo"                      
     [4] "Required"                                   
     [5] "Type"                                       
     [6] "Example"                                    
     [7] "DarwinCore"                                 
     [8] "Core/Extensión"                             
     [9] "Incluir.en.DarwinCore"                      
    [10] "pamflow.(detected_species)"                 
    [11] "DarwinCore"                                 
    [12] "Formato.de.migración.CSA.(detected_species)"

    $`summary of changes from camtrap`
    [1] "File"                   "Field"                  "Change.type"           
    [4] "Observations"           "Darwin.Core.equivalent" "status"                

    $QuestionsPreguntas
    [1] "Preguntas.pendientes" "File"                 "status"              
    [4] "Notes"               

Now we read the csv files containing the data:

``` r
csvFiles<-c(media="../data_transformacion/media.csv",deployments="../data_transformacion/deployments.csv",observations="../data_transformacion/observations.csv")
data<-lapply(csvFiles,read.csv)
```

# Checking on variables

The name of the fields are not very clean neither:

``` r
mapping$media.csv$pamDP.Field.Name
```

     [1] "mediaID *"       "deploymentID *"  "captureMethod"   "timestamp *"    
     [5] "filePath *"      "filePublic *"    "fileName"        "fileMediatype *"
     [9] "sampleRate"      "bitDepth"        "fileLength"      "numChannels"    
    [13] "favorite"        "mediaComments"   NA               

``` r
mapping$deployments.csv$`pamDP.-.Field.Name`
```

     [1] "deploymentID"          "locationID"            "locationName"         
     [4] "latitude"              "longitude"             "coordinateUncertainty"
     [7] "deploymentStart"       "deploymentEnd"         "setupBy"              
    [10] "recorderID"            "recorderModel"         "recorderDelay"        
    [13] "recorderHeight"        "recorderDepth"         "recorderTilt"         
    [16] "recorderHeading"       "recorderConfiguration" "detectionDistance"    
    [19] "timestampIssues"       "baitUse"               "featureType"          
    [22] "habitat"               "deploymentGroups"      "deploymentTags"       
    [25] "deploymentComments"    NA                      NA                     
    [28] NA                      NA                      NA                     
    [31] NA                      NA                     

``` r
mapping$observation.csv$`pamDP.-.Field.Name`
```

     [1] "observationID *"           "deploymentID *"           
     [3] "mediaID"                   "eventID"                  
     [5] "observationLevel"          "observationType"          
     [7] "scientificName"            "count"                    
     [9] "lifeStage"                 "sex"                      
    [11] "behavior"                  "vocalActivity"            
    [13] "individualID"              "individualPositionRadius" 
    [15] "bboxTime"                  "bboxFrequency"            
    [17] "bboxDuration"              "bboxBandwidth"            
    [19] "classificationMethod"      "classifiedBy"             
    [21] "classificationTimestamp"   "classificationProbability"
    [23] "observationTags"           "observationComments"      

We will need to trim the names of the fields (to suppress the ’ \*’) at
the end of the character strings:

``` r
(mapping$media.csv$pamDP_field<-gsub(" \\*$","",mapping$media.csv$pamDP.Field.Name))
```

     [1] "mediaID"       "deploymentID"  "captureMethod" "timestamp"    
     [5] "filePath"      "filePublic"    "fileName"      "fileMediatype"
     [9] "sampleRate"    "bitDepth"      "fileLength"    "numChannels"  
    [13] "favorite"      "mediaComments" NA             

``` r
(mapping$deployments.csv$pamDP_field<-gsub(" \\*$","",mapping$deployments.csv$`pamDP.-.Field.Name`))
```

     [1] "deploymentID"          "locationID"            "locationName"         
     [4] "latitude"              "longitude"             "coordinateUncertainty"
     [7] "deploymentStart"       "deploymentEnd"         "setupBy"              
    [10] "recorderID"            "recorderModel"         "recorderDelay"        
    [13] "recorderHeight"        "recorderDepth"         "recorderTilt"         
    [16] "recorderHeading"       "recorderConfiguration" "detectionDistance"    
    [19] "timestampIssues"       "baitUse"               "featureType"          
    [22] "habitat"               "deploymentGroups"      "deploymentTags"       
    [25] "deploymentComments"    NA                      NA                     
    [28] NA                      NA                      NA                     
    [31] NA                      NA                     

``` r
(mapping$observation.csv$pamDP_field<-gsub(" \\*$","",mapping$observation.csv$`pamDP.-.Field.Name`))
```

     [1] "observationID"             "deploymentID"             
     [3] "mediaID"                   "eventID"                  
     [5] "observationLevel"          "observationType"          
     [7] "scientificName"            "count"                    
     [9] "lifeStage"                 "sex"                      
    [11] "behavior"                  "vocalActivity"            
    [13] "individualID"              "individualPositionRadius" 
    [15] "bboxTime"                  "bboxFrequency"            
    [17] "bboxDuration"              "bboxBandwidth"            
    [19] "classificationMethod"      "classifiedBy"             
    [21] "classificationTimestamp"   "classificationProbability"
    [23] "observationTags"           "observationComments"      

Now we can check which fields from the mappings are present in data
files

``` r
(m_media<-match(colnames(data$media),mapping$media.csv$pamDP_field))
```

     [1]  1  2  3  4  5  7  8  9 10 11 12 13 14

``` r
(m_deployments<-match(colnames(data$deployments),mapping$deployments.csv$pamDP_field))
```

     [1]  1  2  3  4  5  6  7  8  9 10 11 13 17 22 23 25

``` r
(m_observations<-match(colnames(data$observations),mapping$observation.csv$pamDP_field))
```

     [1]  1  2  3  4  6  7 15 16 17 18 19 20 21 22 24

We put in the mapping whether the variables are in the data or not:

``` r
mapping$media.csv$presentInData<-F
mapping$media.csv$presentInData[m_media]<-T
mapping$deployments.csv$presentInData<-F
mapping$deployments.csv$presentInData[m_deployments]<-T
mapping$observation.csv$presentInData<-F
mapping$observation.csv$presentInData[m_observations]<-T
```

Let’s consider that the required variables for DwC are the ones marked
as required for pamDP + the ones not having any equivalent in pamDP,
that were added in the mapping. In the future, we should have a system
to map from DwC to all the variables allowing to create the DwC
variables, and to document whether the variable is required in the DwC.

``` r
mapping$media.csv$DwC_required<-ifelse(is.na(mapping$media.csv$Required),T,mapping$media.csv$Required)
mapping$deployments.csv$DwC_required<-ifelse(is.na(mapping$deployments.csv$Required),T,mapping$deployments.csv$Required)
mapping$observation.csv$DwC_required<-ifelse(is.na(mapping$observation.csv$Required),T,mapping$observation.csv$Required)
```

Tables present vs required:

``` r
table(mapping$media.csv[c("DwC_required","presentInData")])
```

                presentInData
    DwC_required FALSE TRUE
           FALSE     0    4
           TRUE      2    9

``` r
table(mapping$deployments.csv[c("DwC_required","presentInData")])
```

                presentInData
    DwC_required FALSE TRUE
           FALSE     9    9
           TRUE      7    7

``` r
table(mapping$observation.csv[c("DwC_required","presentInData")])
```

                presentInData
    DwC_required FALSE TRUE
           FALSE     8   11
           TRUE      1    4

## Missing variables

Media.csv:

``` r
mapping$media.csv[!mapping$media.csv$presentInData&mapping$media.csv$DwC_required,c("pamDP.Field.Name","DarwinCore")]
```

|     | pamDP.Field.Name | DarwinCore    |
|:----|:-----------------|:--------------|
| 6   | filePublic \*    | available     |
| 15  | NA               | captureDevice |

Deployments.csv

``` r
mapping$deployments.csv[!mapping$deployments.csv$presentInData&mapping$deployments.csv$DwC_required,c("pamDP.-.Field.Name","DarwinCore")]
```

|     | pamDP.-.Field.Name | DarwinCore      |
|:----|:-------------------|:----------------|
| 26  | NA                 | continent       |
| 27  | NA                 | country         |
| 28  | NA                 | countryCode     |
| 29  | NA                 | stateProvince   |
| 30  | NA                 | county          |
| 31  | NA                 | locality        |
| 32  | NA                 | institutionCode |

Observation.csv

``` r
mapping$observation.csv[!mapping$observation.csv$presentInData&mapping$observation.csv$DwC_required,c("pamDP.-.Field.Name","DarwinCore")]
```

|     | pamDP.-.Field.Name | DarwinCore |
|:----|:-------------------|:-----------|
| 5   | observationLevel   | NA         |
