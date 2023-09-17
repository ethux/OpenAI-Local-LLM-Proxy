class Prompt:
    @staticmethod
    def prepare(messages):
        output_msg = ''
        for message in messages:
            output_msg += message['role'] + ': ' + message['content'] + '\n'
        return output_msg