from time import sleep


class CommandContext:
    def __init__(self, client, chat_id, command):
        self.client = client
        self.chat_id = chat_id
        self.command = command
        self.step = 1


    def __enter__(self):
        self.message = self.client.send_message(chat_id=self.chat_id, text=self.command)
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        return
    

    def expect_next(self, correct_response, sleep_s=0.2, timeout_s=60):
        assert correct_response is not None, "correct_response should be specified"
        
        timer = 0
        while timer <= timeout_s:
            response = self.client.get_messages(self.chat_id, self.message.id + self.step).text
            if response is not None: # found target message
                self.step += 1
                assert response == correct_response, (
                    f"'{self.command}' failed due to wrong reaction on step {self.step - 1}"
                    f"\nreaction: {response}\nexpected: {correct_response}"
                )
                return

            timer += sleep_s
            sleep(sleep_s)

 
    def expect_next_prefix(self, correct_response_prefix, sleep_s=0.2, timeout_s=60):
        assert correct_response_prefix is not None, "correct_response should be specified"
        
        timer = 0
        while timer <= timeout_s:
            response = self.client.get_messages(self.chat_id, self.message.id + self.step).text
            if response is not None: # found target message
                self.step += 1
                assert response.startswith(correct_response_prefix), (
                    f"'{self.command}' failed due to wrong reaction prefix on step {self.step - 1}"
                    f"\nreaction: {response}\nexpected: {correct_response_prefix}"
                )
                return

            timer += sleep_s
            sleep(sleep_s)


    def expect_none(self, sleep_s=0.5, timeout_s=2):
        timer = 0
        while timer <= timeout_s:
            response = self.client.get_messages(self.chat_id, self.message.id + self.step).text
            assert response is None, (
                f"'{self.command}' failed due to presence of reaction on step {self.step}"
                f"\nreaction: {response}"
            )
            
            timer += sleep_s
            sleep(sleep_s)
    
    
    def expect_length(self, num_rows, sleep_s=0.5, timeout_s=60):
        raise NotImplementedError


    def expect_any(self, sleep_s=0.2, timeout_s=60):
        timer = 0
        while timer <= timeout_s:
            response = self.client.get_messages(self.chat_id, self.message.id + self.step).text
            if response is not None: # found target message
                self.step += 1
                break

            timer += sleep_s
            sleep(sleep_s)

        assert response is not None, (
            f"'{self.command}' failed due to absence of reaction on step {self.step - 1}"
        )


    def expect_any_multiple(self, number_of_responses, sleep_s=0.2, timeout_s=60):
        for i in range(number_of_responses):
            self.expect_any(sleep_s=sleep_s, timeout_s=timeout_s)


    def expect_next_number_of_rows(self, n_rows, sleep_s=0.2, timeout_s=60):
        timer = 0
        while timer <= timeout_s:
            response = self.client.get_messages(self.chat_id, self.message.id + self.step).text
            if response is not None: # found target message
                self.step += 1
                assert len(response.split("\n")) == n_rows, (
                    f"'{self.command}' failed due to wrong number of rows on step {self.step - 1}"
                    f"\nreaction: {response}\nexpected number of rows: {n_rows}"
                )
                return

            timer += sleep_s
            sleep(sleep_s)
