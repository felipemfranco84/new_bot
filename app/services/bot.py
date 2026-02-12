def realizar_login(self, user, password):
        try:
            self.logger.info("Tentando realizar login...")
            # Seletores baseados na imagem que voce enviou
            campo_user = self.wait.until(EC.presence_of_element_located((By.NAME, "name")))
            campo_pass = self.driver.find_element(By.NAME, "password")
            botao_login = self.driver.find_element(By.NAME, "s1") # Geralmente o botao verde

            campo_user.send_keys(user)
            campo_pass.send_keys(password)
            time.sleep(1)
            botao_login.click()
            
            # Espera carregar a aldeia
            self.wait.until(EC.presence_of_element_located((By.ID, "l1")))
            self.logger.info("Login realizado com sucesso!")
            return True
        except Exception as e:
            self.logger.error(f"Falha ao logar: {e}")
            return False