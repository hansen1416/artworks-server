from sqlalchemy import Column, Integer, String, Text, Boolean, VARCHAR, DateTime


class Objects(db.Model):
    __tablename__ = "objects"

    objectID = Column(Integer, primary_key=True)
    uuid = Column(VARCHAR(36))
    accessioned = Column(Boolean, nullable=False)
    accessionNum = Column(VARCHAR(32))
    objectLeonardoID = Column(VARCHAR(16))
    locationID = Column(Integer)
    title = Column(VARCHAR(2048))
    displayDate = Column(VARCHAR(256))
    beginYear = Column(Integer)
    endYear = Column(Integer)
    visualBrowserTimeSpan = Column(VARCHAR(32))
    medium = Column(VARCHAR(2048))
    dimensions = Column(VARCHAR(2048))
    inscription = Column(Text)
    markings = Column(Text)
    attributionInverted = Column(VARCHAR(1024))
    attribution = Column(VARCHAR(1024))
    creditLine = Column(VARCHAR(2048))
    classification = Column(VARCHAR(64))
    subClassification = Column(VARCHAR(64))
    visualBrowserClassification = Column(VARCHAR(32))
    provenanceText = Column(Text)
    parentID = Column(Integer)
    isVirtual = Column(Boolean, nullable=False)
    departmentAbbr = Column(VARCHAR(32), nullable=False)
    portfolio = Column(VARCHAR(2048))
    series = Column(VARCHAR(850))
    volume = Column(VARCHAR(850))
    watermarks = Column(VARCHAR(512))
    lastDetectedModification = Column(DateTime)
    wikidataid = Column(VARCHAR(64))
    customPrintURL = Column(VARCHAR(2048))

    def to_dict(self):
        return {
            "objectID": self.objectID,
            "uuid": self.uuid,
            "accessioned": self.accessioned,
            "accessionNum": self.accessionNum,
            "objectLeonardoID": self.objectLeonardoID,
            "locationID": self.locationID,
            "title": self.title,
            "displayDate": self.displayDate,
            "beginYear": self.beginYear,
            "endYear": self.endYear,
            "visualBrowserTimeSpan": self.visualBrowserTimeSpan,
            "medium": self.medium,
            "dimensions": self.dimensions,
            "inscription": self.inscription,
            "markings": self.markings,
            "attributionInverted": self.attributionInverted,
            "attribution": self.attribution,
            "creditLine": self.creditLine,
            "classification": self.classification,
            "subClassification": self.subClassification,
            "visualBrowserClassification": self.visualBrowserClassification,
            "provenanceText": self.provenanceText,
            "parentID": self.parentID,
            "isVirtual": self.isVirtual,
            "departmentAbbr": self.departmentAbbr,
            "portfolio": self.portfolio,
            "series": self.series,
            "volume": self.volume,
            "watermarks": self.watermarks,
            "lastDetectedModification": self.lastDetectedModification,
            "wikidataid": self.wikidataid,
            "customPrintURL": self.customPrintURL,
        }


class PublishedImages(db.Model):
    __tablename__ = "published_images"

    uuid = Column(String(64), primary_key=True)
    iiifURL = Column(String(512), nullable=False)
    iiifThumbURL = Column(String(512))
    viewtype = Column(String(32))
    sequence = Column(String(32))
    width = Column(Integer)
    height = Column(Integer)
    maxpixels = Column(Integer)
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    # depictstmsobjectid = Column(Integer, ForeignKey("objects.objectID"), nullable=False)
    depictstmsobjectid = Column(Integer, nullable=True)
    assistivetext = Column(Text)

    #   object = relationship(Objects, foreign_keys=[depictstmsobjectid])

    def to_dict(self):
        return {
            "uuid": self.uuid,
            "iiifURL": self.iiifURL,
            "iiifThumbURL": self.iiifThumbURL,
            "viewtype": self.viewtype,
            "sequence": self.sequence,
            "width": self.width,
            "height": self.height,
            "maxpixels": self.maxpixels,
            "created": self.created,
            "modified": self.modified,
            "depictstmsobjectid": self.depictstmsobjectid,
            "assistivetext": self.assistivetext,
        }
