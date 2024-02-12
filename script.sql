-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Accounts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Accounts` (
  `e-mail` VARCHAR(320) NOT NULL,
  `acc_name` VARCHAR(255) NOT NULL,
  `password` VARCHAR(127) NULL DEFAULT NULL,
  `date_created` DATE NULL DEFAULT NULL,
  `admin` TINYINT(1) NULL DEFAULT NULL,
  PRIMARY KEY (`e-mail`),
  UNIQUE INDEX `e-mail_UNIQUE` (`e-mail` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Products` (
  `pro_ID` VARCHAR(12) NOT NULL,
  `pro_name` VARCHAR(255) NOT NULL,
  `pro_img` VARCHAR(255) NULL DEFAULT NULL,
  `pro_info` VARCHAR(1023) NULL DEFAULT NULL,
  `qty` INT NOT NULL,
  `price` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`pro_ID`),
  UNIQUE INDEX `pro_ID_UNIQUE` (`pro_ID` ASC) VISIBLE,
  UNIQUE INDEX `pro_name_UNIQUE` (`pro_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Reviews`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Reviews` (
  `re_ID` VARCHAR(12) NOT NULL,
  `comment` VARCHAR(255) NULL DEFAULT NULL,
  `nr_stars` TINYINT(1) NOT NULL,
  `date_created` DATE NULL DEFAULT NULL,
  `acc_e-mail` VARCHAR(320) NOT NULL,
  `pro_ID` VARCHAR(12) NOT NULL,
  PRIMARY KEY (`re_ID`),
  UNIQUE INDEX `re_ID_UNIQUE` (`re_ID` ASC) VISIBLE,
  INDEX `fk_Reviews_Accounts_idx` (`acc_e-mail` ASC) VISIBLE,
  INDEX `fk_Reviews_Products1_idx` (`pro_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Reviews_Accounts`
    FOREIGN KEY (`acc_e-mail`)
    REFERENCES `mydb`.`Accounts` (`e-mail`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Reviews_Products1`
    FOREIGN KEY (`pro_ID`)
    REFERENCES `mydb`.`Products` (`pro_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Balance_Changes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Balance_Changes` (
  `change_ID` VARCHAR(12) NOT NULL,
  `is_purchase` TINYINT(1) NOT NULL,
  `qty` INT NOT NULL,
  `date` DATETIME NOT NULL,
  `acc_e-mail` VARCHAR(320) NOT NULL,
  `pro_ID` VARCHAR(12) NOT NULL,
  PRIMARY KEY (`change_ID`),
  UNIQUE INDEX `change_ID_UNIQUE` (`change_ID` ASC) VISIBLE,
  UNIQUE INDEX `date_UNIQUE` (`date` ASC) VISIBLE,
  INDEX `fk_Balance_Changes_Accounts1_idx` (`acc_e-mail` ASC) VISIBLE,
  INDEX `fk_Balance_Changes_Products1_idx` (`pro_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Balance_Changes_Accounts1`
    FOREIGN KEY (`acc_e-mail`)
    REFERENCES `mydb`.`Accounts` (`e-mail`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Balance_Changes_Products1`
    FOREIGN KEY (`pro_ID`)
    REFERENCES `mydb`.`Products` (`pro_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Cart`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Cart` (
  `qty` INT NOT NULL,
  `acc_e-mail` VARCHAR(320) NOT NULL,
  `pro_ID` VARCHAR(12) NOT NULL,
  `cart_ID` VARCHAR(12) NOT NULL,
  PRIMARY KEY (`cart_ID`),
  INDEX `fk_Cart_Accounts1_idx` (`acc_e-mail` ASC) VISIBLE,
  INDEX `fk_Cart_Products1_idx` (`pro_ID` ASC) VISIBLE,
  UNIQUE INDEX `cart_ID_UNIQUE` (`cart_ID` ASC) VISIBLE,
  CONSTRAINT `fk_Cart_Accounts1`
    FOREIGN KEY (`acc_e-mail`)
    REFERENCES `mydb`.`Accounts` (`e-mail`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Cart_Products1`
    FOREIGN KEY (`pro_ID`)
    REFERENCES `mydb`.`Products` (`pro_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`Orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Orders` (
  `ord_ID` VARCHAR(12) NOT NULL,
  `qty` INT UNSIGNED NOT NULL,
  `price` INT UNSIGNED NULL,
  `pro_ID` VARCHAR(12) NOT NULL,
  `acc_e-mail` VARCHAR(320) NOT NULL,
  PRIMARY KEY (`ord_ID`, `pro_ID`),
  INDEX `fk_Orders_Products1_idx` (`pro_ID` ASC) VISIBLE,
  INDEX `fk_Orders_Accounts1_idx` (`acc_e-mail` ASC) VISIBLE,
  CONSTRAINT `fk_Orders_Products1`
    FOREIGN KEY (`pro_ID`)
    REFERENCES `mydb`.`Products` (`pro_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Orders_Accounts1`
    FOREIGN KEY (`acc_e-mail`)
    REFERENCES `mydb`.`Accounts` (`e-mail`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
