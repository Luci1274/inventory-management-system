-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Gestion_stock
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema Gestion_stock
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Gestion_stock` DEFAULT CHARACTER SET utf8 ;
USE `Gestion_stock` ;

-- -----------------------------------------------------
-- Table `Gestion_stock`.`categorias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Gestion_stock`.`categorias` (
  `idcategorias` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idcategorias`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Gestion_stock`.`productos`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Gestion_stock`.`productos` (
  `idproductos` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `precio` DECIMAL(10,2) NULL,
  `stock_actual` INT NOT NULL,
  `stock_minimo` INT NULL,
  `idcategorias` INT NOT NULL,
  PRIMARY KEY (`idproductos`, `idcategorias`),
  INDEX `fk_productos_categorias_idx` (`idcategorias` ASC) VISIBLE,
  CONSTRAINT `fk_productos_categorias`
    FOREIGN KEY (`idcategorias`)
    REFERENCES `Gestion_stock`.`categorias` (`idcategorias`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Gestion_stock`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Gestion_stock`.`usuarios` (
  `idusuarios` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(255) NOT NULL,
  `rol` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idusuarios`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Gestion_stock`.`movimientos_stock`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Gestion_stock`.`movimientos_stock` (
  `idmovimientos_stock` INT NOT NULL AUTO_INCREMENT,
  `idproductos` INT NOT NULL,
  `idusuarios` INT NOT NULL,
  `cantidad` INT NULL,
  `tipo_movimiento` VARCHAR(45) NOT NULL,
  `fecha_hora` DATETIME NOT NULL,
  PRIMARY KEY (`idmovimientos_stock`, `idproductos`, `idusuarios`),
  INDEX `fk_movimientos_stock_productos1_idx` (`idproductos` ASC) VISIBLE,
  INDEX `fk_movimientos_stock_usuarios1_idx` (`idusuarios` ASC) VISIBLE,
  CONSTRAINT `fk_movimientos_stock_productos1`
    FOREIGN KEY (`idproductos`)
    REFERENCES `Gestion_stock`.`productos` (`idproductos`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_movimientos_stock_usuarios1`
    FOREIGN KEY (`idusuarios`)
    REFERENCES `Gestion_stock`.`usuarios` (`idusuarios`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
