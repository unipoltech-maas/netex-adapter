import xml.etree.ElementTree as ET
from xml.dom.minidom import parse, Node

# Read Netex file and parse
sourceFilename = "IT-ITF4-FNB-NeTEx_L2"   # NOTE: Change source file name
doc = parse(f"{sourceFilename}.xml")

# Retrieve nodes
stopPlaces = doc.getElementsByTagName("StopPlace")
scheduledStopPoints = doc.getElementsByTagName("ScheduledStopPoint")
passengerStopAssignments = doc.getElementsByTagName("PassengerStopAssignment")

# Create a ValidBetween node
validBetweenNode = doc.createElement("ValidBetween")
fromDateNode = doc.createElement("FromDate")
dateText = doc.createTextNode("2021-01-01T00:00:00")
fromDateNode.appendChild(dateText)
validBetweenNode.appendChild(fromDateNode.cloneNode(True))


# Add to each passenger stop assignments the QuayRef node, the ValidBetween node
for assign in passengerStopAssignments:
    # Create the quay id assuming is like StopPlace with a different resource name
    stopPlaceRef = assign.getElementsByTagName("StopPlaceRef")
    quayId = stopPlaceRef[0].getAttribute("ref").replace("StopPlace", "Quay")

    # Create a QuayRef node
    quayRef = doc.createElement("QuayRef")
    quayRef.setAttribute("version", "1")
    quayRef.setAttribute("ref", quayId)

    # Add nodes to PassengerStopAssignment
    assign.appendChild(validBetweenNode.cloneNode(True))
    assign.appendChild(quayRef)


i = 1
for stopPlace in stopPlaces:
    attr_id = stopPlace.getAttribute("id").replace("StopPlace", "ScheduledStopPoint")

    refPoints = [
        stopPoint for stopPoint in scheduledStopPoints if stopPoint.getAttribute("id") == attr_id
    ]
    stopPoint = refPoints[0]
    stopPoint.appendChild(validBetweenNode.cloneNode(True))
    
    # Centroid
    location = stopPoint.getElementsByTagName("Location")[0]
    centroid = doc.createElement("Centroid")
    centroid.appendChild(location.cloneNode(True))
    stopPlace.appendChild(centroid.cloneNode(True))
    
    # Create a description for the Quay
    descrNode = doc.createElement("Description")
    text = doc.createTextNode(f"Banchina N.{i}")
    descrNode.appendChild(text)

    # Create quays with a main Quay inside
    quays = doc.createElement("quays")
    mainQuay = doc.createElement("Quay")
    mainQuay.appendChild(centroid.cloneNode(True))
    mainQuay.setAttribute("id", attr_id.replace("ScheduledStopPoint", "Quay"))
    mainQuay.setAttribute("version", "1")
    mainQuay.appendChild(descrNode)
    quays.appendChild(mainQuay)
    
    # Add nodes to StopPlace
    stopPlace.appendChild(validBetweenNode.cloneNode(True))
    stopPlace.appendChild(quays)

    i += 1

# Write the adapted Netex file
adaptedXml = open(f"{sourceFilename}-Adapted.xml", "+w")
doc.writexml(adaptedXml)
adaptedXml.close()