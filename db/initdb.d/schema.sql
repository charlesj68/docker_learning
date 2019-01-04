/********************
 Data definition
 ********************/

/* We create have an "if not exists" because if the container is started
   with MYSQL_DATABASE defined in the environment then the database name
   will already exist. */
CREATE DATABASE IF NOT EXISTS `DockBeanBiz` ;
CREATE TABLE `DockBeanBiz`.`menu` (
  `menu_id` INT NOT NULL AUTO_INCREMENT,
  `item_name` CHAR(30) NOT NULL,
  PRIMARY KEY (`menu_id`),
  UNIQUE INDEX `menu_id_UNIQUE` (`menu_id` ASC) VISIBLE);

/********************
 Data creation
 ********************/

INSERT INTO `DockBeanBiz`.`menu` (`item_name`) VALUES ('Americano');
INSERT INTO `DockBeanBiz`.`menu` (`item_name`) VALUES ('Espresso');
INSERT INTO `DockBeanBiz`.`menu` (`item_name`) VALUES ('Hot Cocoa');

