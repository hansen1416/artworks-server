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