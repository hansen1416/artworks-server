CREATE TABLE published_images (
  uuid                character varying(64) NOT NULL PRIMARY KEY,  -- A unique and persistent GUID for the image
  iiifURL             character varying(512) NOT NULL,               -- The base IIIF URL for the image (see https://iiif.io/api/image/2.1/)
  iiifThumbURL        character varying(512),                         -- An example IIIF URL for a small thumbnail (200x200)
  viewtype            character varying(32),                         -- One of "primary" or "alternate" (primary view or alternate view)
  sequence            character varying(32),                         -- Order for sorting images (e.g., sequence for sculpture views)
  width               integer,                                     -- Full width of the IIIF source image at highest zoom
  height              integer,                                     -- Full height of the IIIF source image at highest zoom
  maxpixels           integer,                                     -- Limitation for fair use (image server enforces)
  created             timestamp with time zone NOT NULL,               -- Creation date of the source image uploaded to NGA's system
  modified            timestamp with time zone NOT NULL,               -- Modification date of the image metadata record
  depictstmsobjectid  integer REFERENCES objects(objectID) ON DELETE SET NULL, -- Object ID depicted (foreign key to objects.objectID)
  assistivetext       text                                         -- Text for visually impaired users with assistive devices
);

-- Images that have been published to NGA web properties either because the NGA owns the copyright or the images are being displayed in a much smaller resolution than the original images under fair use doctrine