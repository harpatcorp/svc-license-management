CREATE TABLE "users" (
  "id" int PRIMARY KEY,
  "email" varchar,
  "first_name" varchar,
  "last_name" varchar,
  "password_1" varchar,
  "password_2" varchar,
  "otp_varified" boolean,
  "is_admin" boolean,
  "created_on" datetime
);

CREATE TABLE "product" (
  "id" int PRIMARY KEY,
  "name" varchar,
  "description" varchar,
  "image" varchar,
  "created_on" datetime,
  "modified_on" datetime
);

CREATE TABLE "version" (
  "id" int PRIMARY KEY,
  "product_id" int,
  "tag" varchar,
  "currency" varchar,
  "price" float,
  "path" varchar,
  "created_on" datetime,
  "modified_on" datetime
);

CREATE TABLE "transactions" (
  "id" int PRIMARY KEY,
  "user_id" int,
  "product_id" int,
  "version_id" int,
  "qty" float,
  "currency" varchar,
  "price" float,
  "total_amt" float,
  "order_id" varchar,
  "paid" boolean,
  "active" boolean,
  "ordered_on" datetime,
  "expired_on" datetime
);

ALTER TABLE "transactions" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "product" ADD FOREIGN KEY ("id") REFERENCES "transactions" ("product_id");

ALTER TABLE "version" ADD FOREIGN KEY ("id") REFERENCES "transactions" ("version_id");
