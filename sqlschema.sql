CREATE TABLE "default_menus" (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name` TEXT NOT NULL,
	`url` TEXT NOT NULL,
	CONSTRAINT `uq_default_menus_name` UNIQUE (`name`)
);

CREATE TABLE "daily_menus" (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name` TEXT NOT NULL,
	`url` TEXT DEFAULT NULL,
	`date` INTEGER NOT NULL
);
CREATE INDEX "idx_daily_menus_date" ON "daily_menus" (`date`);

CREATE TABLE "orders" (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`ordered_at` INTEGER NOT NULL,
	`ordered_by` TEXT NOT NULL,
	`text` TEXT NOT NULL
);
CREATE INDEX "idx_orders_ordered_at" ON "orders" (`ordered_at`);
