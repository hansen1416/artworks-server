
CREATE TABLE objects (
  objectID integer NOT NULL PRIMARY KEY,  -- the primary identifier for an art object
  uuid varchar(36) NULL,                 -- a persistent unique identifier
  accessioned integer NOT NULL,            -- flag indicating NGA accessioned work
  accessionNum character varying(32) NULL, -- accession number assigned
  objectLeonardoID character varying(16) NULL, -- prior legacy CMS system ID
  locationID integer NULL,                 -- location identifier
  title character varying(2048) NULL,     -- title of the art object
  displayDate character varying(256) NULL, -- human readable creation date
  beginYear integer NULL,                   -- computer readable creation start year
  endYear integer NULL,                     -- computer readable creation end year
  visualBrowserTimeSpan character varying(32) NULL, -- computer-generated timeframe
  medium character varying(2048) NULL,     -- materials comprising the art object
  dimensions character varying(2048) NULL, -- human readable dimensions
  inscription character varying NULL,        -- text description of writings
  markings character varying NULL,           -- text description of other marks
  attributionInverted character varying(1024) NULL, -- artist(s) attributed (inverted)
  attribution character varying(1024) NULL, -- artist(s) attributed
  creditLine character varying(2048) NULL,  -- acknowledgement of credit
  classification character varying(64) NULL, -- type of art object
  subClassification character varying(64) NULL, -- sub-type of art object
  visualBrowserClassification character varying(32) NULL, -- normalized classification
  provenanceText text NULL,                 -- provenance description
  parentID integer NULL,                   -- foreign key to parent object
  isVirtual integer NOT NULL,               -- flag indicating virtual object
  departmentAbbr character varying(32) NOT NULL, -- NGA department abbreviation
  portfolio character varying(2048) NULL,  -- portfolio associated
  series character varying(850) NULL,       -- series associated
  volume character varying(850) NULL,       -- volume associated
  watermarks character varying(512) NULL,    -- description of watermarks
  lastDetectedModification timestamp with time zone NULL, -- last modification timestamp
  wikidataid character varying(64) NULL,    -- Wikidata ID for NGA object
  customPrintURL character varying(2048) NULL  -- URL for custom print ordering
);

CREATE TABLE alternative_identifiers (
  uuid VARCHAR(64) NOT NULL PRIMARY KEY,  -- universally unique identifier
  idschemelabel VARCHAR(64) NOT NULL,      -- key name for identification scheme
  identifier VARCHAR(64) NOT NULL          -- The value of the identifier
);

CREATE TABLE constituents (
  constituentID INTEGER NOT NULL PRIMARY KEY,  -- primary key (tms identifier)
  uuid VARCHAR(36) NULL,                       -- a persistent unique identifier
  ULANID VARCHAR(32) NULL,                      -- Getty ULAN ID
  preferredDisplayName VARCHAR(256) NULL,       -- inverted full name
  forwardDisplayName VARCHAR(256) NULL,        -- forward direction preferred full name
  lastName VARCHAR(256) NULL,                   -- preferred last name
  displayDate VARCHAR(256) NULL,                -- birth and death dates
  artistOfNGAObject INTEGER NOT NULL,           -- artist flag (0/1)
  beginYear INTEGER NULL,                       -- birth year
  endYear INTEGER NULL,                         -- death year
  visualBrowserTimeSpan VARCHAR(32) NULL,       -- computed time-span
  nationality VARCHAR(128) NULL,                 -- nationality
  visualBrowserNationality VARCHAR(128) NULL,   -- normalized nationality
  constituentType VARCHAR(30) NOT NULL CHECK (  -- enforce valid constituent type
      constituentType IN ('anonymous', 'corporate', 'couple', 'individual', 'purchase_fund')
  ),
  wikidataid VARCHAR(64) NULL                   -- Wikidata ID
);

CREATE TABLE constituents_altnames (
  altnameid SERIAL PRIMARY KEY,  -- primary key (auto-increment)
  -- constituentid INTEGER NOT NULL REFERENCES constituents(constituentID), -- foreign key to constituents table
  constituentid INTEGER NOT NULL, -- foreign key to constituents table
  lastname VARCHAR(256),        -- alternate last name
  displayname VARCHAR(256),       -- alternate display name
  forwarddisplayname VARCHAR(256), -- alternate display name forwards direction
  nametype VARCHAR(32) NOT NULL  -- type of alternate name, one of:Birth Name, Full Name, Maiden Name, Married Name, Nickname/Pseudonym, Original Name, Preferred Name, Spouse, Unicode Display Name, Variant, Variant Index Name
);

CREATE TABLE constituents_text_entries (
  -- constituentID INTEGER NOT NULL REFERENCES constituents(constituentID), -- foreign key to constituents table
  constituentID INTEGER NOT NULL, -- foreign key to constituents table
  text TEXT NOT NULL,  -- the text itself
  textType VARCHAR(32) NOT NULL,  -- text type
  year VARCHAR(4) NULL  -- the year the text was published
);

CREATE TABLE locations (
  locationID INTEGER NOT NULL PRIMARY KEY,  -- primary key
  site VARCHAR(64) NOT NULL,                -- building site
  room VARCHAR(64) NOT NULL,                -- room within the site
  publicAccess INTEGER NOT NULL,             -- public access flag (0/1)
  description VARCHAR(256) NOT NULL,         -- full text description
  unitPosition VARCHAR(64) NULL             -- location within the room
);

CREATE TABLE media_items (
  mediaID BIGINT NOT NULL PRIMARY KEY,  -- numerical identifier for media
  mediaType VARCHAR(32) NOT NULL,      -- audio or video type
  title VARCHAR(2048) NULL,            -- title of the media item
  description TEXT NULL,                -- HTML fragment description
  duration INTEGER NULL,                -- duration in seconds
  language VARCHAR(12) NOT NULL,       -- two letter language code
  thumbnailURL VARCHAR(1024) NULL,      -- full URL to the thumbnail
  playURL VARCHAR(1024) NULL,           -- URL to play the media file
  downloadURL VARCHAR(1024) NULL,       -- URL to download the media file (optional)
  keywords VARCHAR(2048) NULL,          -- non-controlled keywords
  tags VARCHAR(2048) NULL,              -- AEM tags assigned by authors
  imageURL VARCHAR(1024) NULL,          -- URL to a full-size image
  presentationDate TIMESTAMP WITH TIME ZONE NULL, -- presentation date
  releaseDate TIMESTAMP WITH TIME ZONE NULL, -- publication date
  lastModified TIMESTAMP WITH TIME ZONE NULL  -- last modification date
);

CREATE TABLE media_relationships (
  -- mediaID BIGINT NOT NULL REFERENCES media_items(mediaID),  -- foreign key to media_items table
  mediaID BIGINT NOT NULL,  -- foreign key to media_items table
  relatedID BIGINT NOT NULL,
  relatedEntity VARCHAR(32) NOT NULL,
  PRIMARY KEY (mediaID, relatedID, relatedEntity)
);

CREATE TABLE object_associations (
  -- parentObjectID INTEGER NOT NULL REFERENCES objects(objectID),  -- foreign key to objects table
  parentObjectID INTEGER NOT NULL,  -- foreign key to objects table
  -- childObjectID INTEGER NOT NULL REFERENCES objects(objectID),  -- foreign key to objects table
  childObjectID INTEGER NOT NULL,  -- foreign key to objects table
  relationship VARCHAR(32) NOT NULL,
  PRIMARY KEY (parentObjectID, childObjectID, relationship)
);

CREATE TABLE objects_altnums (
  -- objectid INTEGER NOT NULL REFERENCES objects(objectID),  -- foreign key to objects table
  objectid INTEGER NOT NULL,  -- foreign key to objects table
  altnumtype VARCHAR(64) NOT NULL,
  altnum VARCHAR(64) NOT NULL,
  PRIMARY KEY (objectid, altnumtype, altnum)
);

CREATE TABLE objects_constituents (
  -- objectID INTEGER NOT NULL REFERENCES objects(objectID),  -- foreign key to objects table
  objectID INTEGER NOT NULL,  -- foreign key to objects table
  -- constituentID INTEGER NOT NULL REFERENCES constituents(constituentID),  -- foreign key to constituents table
  constituentID INTEGER NOT NULL,  -- foreign key to constituents table
  displayOrder INTEGER NOT NULL,
  roleType VARCHAR(64) NOT NULL,
  role VARCHAR(64) NOT NULL,
  prefix VARCHAR(64) NULL,
  suffix VARCHAR(64) NULL,
  displayDate VARCHAR(128) NULL,
  beginYear INTEGER NULL,
  endYear INTEGER NULL,
  country VARCHAR(64) NULL,
  zipCode VARCHAR(16) NULL,
  PRIMARY KEY (objectID, constituentID, displayOrder, roleType, role)  -- composite primary key
);

CREATE TABLE objects_dimensions (
  -- objectID INTEGER NOT NULL REFERENCES objects(objectID),  -- foreign key to objects table
  objectID INTEGER NOT NULL,  -- foreign key to objects table
  element VARCHAR(32) NOT NULL,
  dimensionType VARCHAR(32) NOT NULL,
  dimension DECIMAL(22, 10) NOT NULL,
  unitName VARCHAR(32) NOT NULL,
  PRIMARY KEY (objectID, element, dimensionType)  -- composite primary key
);

CREATE TABLE objects_historical_data (
  dataType VARCHAR(32) NOT NULL,
  -- objectID INTEGER NOT NULL REFERENCES objects(objectID),  -- foreign key to objects table
  objectID INTEGER NOT NULL,  -- foreign key to objects table
  displayOrder INTEGER NOT NULL,
  forwardText VARCHAR NULL,
  invertedText VARCHAR NULL,
  remarks VARCHAR NULL,
  effectiveDate VARCHAR(10) NULL,
  PRIMARY KEY (objectID, dataType, displayOrder)  -- composite primary key
);


CREATE TABLE objects_terms (
  termID INTEGER NOT NULL,
  -- objectID INTEGER NOT NULL REFERENCES objects(objectID),  -- foreign key to objects table
  objectID INTEGER NOT NULL,  -- foreign key to objects table
  termType VARCHAR(64) NOT NULL,
  term VARCHAR(256) NULL,
  visualBrowserTheme VARCHAR(32) NULL,
  visualBrowserStyle VARCHAR(64) NULL,
  PRIMARY KEY (objectID, termID, termType)  -- composite primary key
);

CREATE TABLE objects_text_entries (
  -- objectID INTEGER NOT NULL REFERENCES objects(objectID),  -- foreign key to objects table
  objectID INTEGER NOT NULL,  -- foreign key to objects table
  text TEXT NOT NULL,  -- the text itself
  textType VARCHAR(32) NOT NULL,  -- text type
  year VARCHAR(4) NULL,  -- the year the text was published
  PRIMARY KEY (objectID, textType)  -- composite primary key
);

CREATE TABLE preferred_locations (
  locationKey VARCHAR(32) NOT NULL PRIMARY KEY,  -- unique key as primary key
  locationType VARCHAR(32) NOT NULL,
  description VARCHAR(512) NOT NULL,
  isPublicVenue INTEGER NOT NULL,
  mapImageURL VARCHAR(1024) NULL,
  mapShapeType VARCHAR(32) NULL,
  mapShapeCoords VARCHAR(1024) NULL,
  -- partof VARCHAR(32) REFERENCES preferred_locations(locationKey)  -- foreign key referencing itself
  partof VARCHAR(32) NULL  -- foreign key referencing itself
);

CREATE TABLE preferred_locations_tms_locations (
  -- preferredLocationKey VARCHAR(32) NOT NULL REFERENCES preferred_locations(locationKey),  -- foreign key to preferred_locations table
  preferredLocationKey VARCHAR(32) NOT NULL,  -- foreign key to preferred_locations table
  -- tmsLocationID INTEGER NOT NULL REFERENCES locations(locationID),  -- foreign key to locations table
  tmsLocationID INTEGER NOT NULL,  -- foreign key to locations table
  PRIMARY KEY (preferredLocationKey, tmsLocationID)  -- composite primary key
);

CREATE TABLE published_images (
  uuid VARCHAR(64) NOT NULL PRIMARY KEY,  -- unique identifier for image
  iiifURL VARCHAR(512) NOT NULL,        -- base IIIF URL for the image
  iiifThumbURL VARCHAR(512) NULL,        -- IIIF URL for thumbnail
  viewtype VARCHAR(32) NOT NULL,         -- primary or alternate view
  sequence VARCHAR(32) NULL,            -- order for sorting images
  width INTEGER NULL,                   -- full width of the image
  height INTEGER NULL,                  -- full height of the image
  maxpixels INTEGER NULL,                -- limit for fair use doctrine
  created TIMESTAMP WITH TIME ZONE NULL,  -- creation date of source image
  modified TIMESTAMP WITH TIME ZONE NULL, -- modification date of metadata
  -- depictstmsobjectid INTEGER REFERENCES objects(objectID), -- foreign key to objects table (optional)
  depictstmsobjectid INTEGER NULL, -- foreign key to objects table (optional)
  assistivetext TEXT NULL                -- text for visually impaired
);

-- sudo -u postgres psql

-- ALTER USER postgres WITH PASSWORD 'new_password';

-- psql -h 127.0.0.1 -U postgres

-- psql -d "dbname='postgres' user='postgres' password='yourPasswd' host='localhost'" -f yourFileName.sql

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
     
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;