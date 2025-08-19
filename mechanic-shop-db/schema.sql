CREATE DATABASE IF NOT EXISTS mechanic_shop
  CHARACTER SET = utf8mb4
  COLLATE = utf8mb4_unicode_ci;
USE mechanic_shop;

-- 1) Customers
CREATE TABLE Customer (
  customer_id   INT          NOT NULL AUTO_INCREMENT,
  first_name    VARCHAR(50)  NOT NULL,
  last_name     VARCHAR(50)  NOT NULL,
  phone         VARCHAR(20),
  email         VARCHAR(100),
  address       VARCHAR(200),
  PRIMARY KEY (customer_id)
) ENGINE=InnoDB;

-- 2) Vehicles
CREATE TABLE Vehicle (
  vin           CHAR(17)     NOT NULL,
  customer_id   INT          NOT NULL,
  make          VARCHAR(50),
  model         VARCHAR(50),
  year          YEAR,
  license_plate VARCHAR(15),
  PRIMARY KEY (vin),
  KEY idx_vehicle_customer (customer_id),
  CONSTRAINT fk_vehicle_customer
    FOREIGN KEY (customer_id)
    REFERENCES Customer(customer_id)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- 3) Mechanics
CREATE TABLE Mechanic (
  mechanic_id   INT          NOT NULL AUTO_INCREMENT,
  name          VARCHAR(100) NOT NULL,
  email         VARCHAR(100),
  phone         VARCHAR(20),
  address       VARCHAR(200),
  salary        DECIMAL(10,2),
  PRIMARY KEY (mechanic_id)
) ENGINE=InnoDB;

-- 4) Service Tickets
CREATE TABLE ServiceTicket (
  ticket_id     INT          NOT NULL AUTO_INCREMENT,
  vin           CHAR(17)     NOT NULL,
  date_in       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_out      DATETIME     NULL,
  description   TEXT,
  status        ENUM('open','in_progress','closed') NOT NULL DEFAULT 'open',
  total_cost    DECIMAL(10,2) DEFAULT 0.00,
  PRIMARY KEY (ticket_id),
  KEY idx_ticket_vehicle (vin),
  CONSTRAINT fk_ticket_vehicle
    FOREIGN KEY (vin)
    REFERENCES Vehicle(vin)
    ON DELETE CASCADE
) ENGINE=InnoDB;

-- 5) Join table for many-to-many
CREATE TABLE ServiceAssignment (
  service_ticket_id  INT      NOT NULL,
  mechanic_id        INT      NOT NULL,
  hours_worked       DECIMAL(5,2) DEFAULT 0.00,
  PRIMARY KEY (service_ticket_id, mechanic_id),
  KEY idx_assign_mechanic (mechanic_id),
  CONSTRAINT fk_assign_ticket
    FOREIGN KEY (service_ticket_id)
    REFERENCES ServiceTicket(ticket_id)
    ON DELETE CASCADE,
  CONSTRAINT fk_assign_mechanic
    FOREIGN KEY (mechanic_id)
    REFERENCES Mechanic(mechanic_id)
    ON DELETE CASCADE
) ENGINE=InnoDB;
