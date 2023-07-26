-- Create main tables
-- depends:

CREATE TABLE IF NOT EXISTS "nft" (
	"metadata"	TEXT,
	"tokenId"	INTEGER,
	"creatorId"	INTEGER,
	"address"	TEXT,
	PRIMARY KEY("tokenId"),
	FOREIGN KEY("creatorId") REFERENCES "user"("id")
);

CREATE TABLE IF NOT EXISTS "user" (
	"id"	INTEGER,
	"vkId"	INTEGER,
	PRIMARY KEY("id")
);