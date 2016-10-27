CREATE TABLE "available_restaurants" (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`name` TEXT NOT NULL,
	`menu_url` TEXT DEFAULT NULL
);

CREATE TABLE "orders" (
	`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`ordered_at` INT NOT NULL,
	`ordered_by` TEXT NOT NULL,
	`order_text` TEXT NOT NULL
);
CREATE INDEX "idx_orders_ordered_at" ON "orders" (`ordered_at`);
