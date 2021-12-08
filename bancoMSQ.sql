CREATE TABLE `shipay`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `role_id` INT NOT NULL,
  `created_at` DATE NOT NULL,
  `updated_at` DATE NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `shipay`.`roles` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `shipay`.`claims` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `description` VARCHAR(45) NOT NULL,
  `active` TINYINT NOT NULL,
  PRIMARY KEY (`id`));

ALTER TABLE `shipay`.`users` 
ADD CONSTRAINT `role_id`
  FOREIGN KEY (`role_id`)
  REFERENCES `shipay`.`roles` (`id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

CREATE TABLE `shipay`.`user_claims` (
  `id` INT NOT NULL,
  `user_id` INT NULL,
  `claim_id` INT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `claim_id`
    FOREIGN KEY (`id`)
    REFERENCES `shipay`.`claims` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `user_id`
    FOREIGN KEY (`id`)
    REFERENCES `shipay`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
